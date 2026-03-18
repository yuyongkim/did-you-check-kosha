from __future__ import annotations

from time import perf_counter
from typing import Any, Dict, List, Mapping

from src.rotating.calculations import (
    calculate_health_index,
    calculate_inspection_interval_years,
    calculate_status,
    relative_difference,
    screen_maintenance_urgency,
    screen_monitoring_escalation,
)
from src.rotating.constants import (
    CONSENSUS_REL_TOLERANCE,
    STANDARD_REFERENCES,
    VIBRATION_LIMIT_MM_PER_S,
    RotatingThresholds,
)
from src.rotating.models import InputPayloadError, RotatingInput, parse_rotating_input
from src.rotating.steam_state import screen_steam_state
from src.rotating.verification import (
    LayerResult,
    ValidationIssue,
    has_blocking_issue,
    issue_from_flag,
    maker_select,
    split_flags,
)


class RotatingVerificationService:
    def __init__(self, thresholds: RotatingThresholds | None = None) -> None:
        self.thresholds = thresholds or RotatingThresholds()

    def evaluate(
        self,
        payload: Mapping[str, Any],
        calculation_type: str = "rotating_integrity",
    ) -> Dict[str, Any]:
        started = perf_counter()
        layers: List[LayerResult] = []

        try:
            rin = parse_rotating_input(payload)
        except InputPayloadError as exc:
            issue = issue_from_flag(
                "FMT.SCHEMA_VALIDATION_FAILED",
                str(exc),
                "Rotating input schema",
            )
            layer = LayerResult(
                layer="layer1_input_validation",
                passed=False,
                issues=[issue],
                details={"payload_keys": sorted(payload.keys())},
            )
            return self._error_response(calculation_type, payload, [layer], started)

        layer1 = self._layer1(rin)
        layers.append(layer1)
        if has_blocking_issue(layer1.issues):
            return self._response(calculation_type, rin, layers, None, {}, started)

        candidates = [
            self._single_calc(rin, "a"),
            self._single_calc(rin, "b"),
            self._single_calc(rin, "c"),
        ]
        layer2, selected = maker_select(candidates, CONSENSUS_REL_TOLERANCE)
        layers.append(layer2)

        layer3 = self._layer3(rin, selected)
        layers.append(layer3)

        reverse_details, layer4 = self._layer4(rin, selected)
        layers.append(layer4)

        return self._response(calculation_type, rin, layers, selected, reverse_details, started)

    def _layer1(self, rin: RotatingInput) -> LayerResult:
        issues: List[ValidationIssue] = []
        t = self.thresholds

        if rin.speed_rpm < t.min_speed_rpm or rin.speed_rpm > t.max_speed_rpm:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"speed_rpm out of range: {rin.speed_rpm}",
                    STANDARD_REFERENCES["monitoring"],
                )
            )
        if rin.vibration_mm_per_s < 0 or rin.vibration_mm_per_s > t.max_vibration_mm_per_s:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"vibration out of range: {rin.vibration_mm_per_s}",
                    STANDARD_REFERENCES["vibration"],
                )
            )
        if rin.nozzle_load_ratio < 0:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"nozzle_load_ratio cannot be negative: {rin.nozzle_load_ratio}",
                    STANDARD_REFERENCES["nozzle_load"],
                )
            )
        if rin.bearing_temperature_c < 0 or rin.bearing_temperature_c > t.max_bearing_temp_c:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"bearing_temperature_c out of range: {rin.bearing_temperature_c}",
                    STANDARD_REFERENCES["monitoring"],
                )
            )

        if rin.machine_type == "steam_turbine":
            if rin.steam_pressure_bar is None:
                issues.append(
                    issue_from_flag(
                        "DATA.MISSING_MANDATORY_FIELD",
                        "steam_pressure_bar is required for steam_turbine",
                        STANDARD_REFERENCES["steam_turbine"],
                    )
                )
            elif rin.steam_pressure_bar < t.min_steam_pressure_bar or rin.steam_pressure_bar > t.max_steam_pressure_bar:
                issues.append(
                    issue_from_flag(
                        "STD.OUT_OF_SCOPE_APPLICATION",
                        f"steam_pressure_bar out of range: {rin.steam_pressure_bar}",
                        STANDARD_REFERENCES["steam_properties"],
                    )
                )

            if rin.steam_temperature_c is not None and (
                rin.steam_temperature_c < t.min_steam_temperature_c or rin.steam_temperature_c > t.max_steam_temperature_c
            ):
                issues.append(
                    issue_from_flag(
                        "STD.OUT_OF_SCOPE_APPLICATION",
                        f"steam_temperature_c out of range: {rin.steam_temperature_c}",
                        STANDARD_REFERENCES["steam_properties"],
                    )
                )

            if rin.steam_quality_x is not None and (rin.steam_quality_x < 0.0 or rin.steam_quality_x > 1.0):
                issues.append(
                    issue_from_flag(
                        "STD.OUT_OF_SCOPE_APPLICATION",
                        f"steam_quality_x out of range: {rin.steam_quality_x}",
                        STANDARD_REFERENCES["steam_properties"],
                    )
                )

            has_state_anchor = rin.steam_temperature_c is not None or rin.steam_quality_x is not None
            has_enthalpy_pair = (
                rin.inlet_enthalpy_kj_per_kg is not None and rin.outlet_enthalpy_kj_per_kg is not None
            )
            if not has_state_anchor and not has_enthalpy_pair:
                issues.append(
                    issue_from_flag(
                        "STD.STEAM_TABLE_LOOKUP_REQUIRED",
                        "steam_turbine requires (pressure + temperature/quality) or enthalpy pair",
                        STANDARD_REFERENCES["steam_properties"],
                    )
                )

        return LayerResult(
            layer="layer1_input_validation",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "machine_type": rin.machine_type,
                "speed_rpm": rin.speed_rpm,
                "vibration_mm_per_s": rin.vibration_mm_per_s,
                "steam_pressure_bar": rin.steam_pressure_bar,
                "steam_temperature_c": rin.steam_temperature_c,
                "steam_quality_x": rin.steam_quality_x,
            },
        )

    def _single_calc(self, rin: RotatingInput, variant: str) -> Dict[str, float]:
        limit = VIBRATION_LIMIT_MM_PER_S[rin.machine_type]
        vib = rin.vibration_mm_per_s
        temp = rin.bearing_temperature_c
        nozzle = rin.nozzle_load_ratio

        if variant == "b":
            vib = vib * 1.001
        elif variant == "c":
            temp = temp * 0.999

        steam_screen = screen_steam_state(
            pressure_bar=rin.steam_pressure_bar,
            temperature_c=rin.steam_temperature_c,
            quality_x=rin.steam_quality_x,
        )

        base_hi = calculate_health_index(
            vibration_mm_per_s=vib,
            vibration_limit_mm_per_s=limit,
            nozzle_load_ratio=nozzle,
            bearing_temperature_c=temp,
        )

        phase_risk = steam_screen.phase_change_risk_index if rin.machine_type == "steam_turbine" else 0.0
        steam_penalty = phase_risk * 0.3
        hi = max(0.0, min(10.0, base_hi - steam_penalty))
        interval = calculate_inspection_interval_years(hi)

        energy_drop = 0.0
        if rin.inlet_enthalpy_kj_per_kg is not None and rin.outlet_enthalpy_kj_per_kg is not None:
            energy_drop = rin.inlet_enthalpy_kj_per_kg - rin.outlet_enthalpy_kj_per_kg

        return {
            "vibration_mm_per_s": vib,
            "vibration_limit_mm_per_s": limit,
            "nozzle_load_ratio": nozzle,
            "bearing_temperature_c": temp,
            "bearing_health_index": hi,
            "inspection_interval_years": interval,
            "steam_pressure_bar": rin.steam_pressure_bar if rin.steam_pressure_bar is not None else 0.0,
            "steam_temperature_c": rin.steam_temperature_c if rin.steam_temperature_c is not None else 0.0,
            "steam_quality_x": steam_screen.effective_quality,
            "steam_specific_energy_drop_kj_per_kg": energy_drop,
            "steam_superheat_margin_c": steam_screen.superheat_margin_c if steam_screen.superheat_margin_c is not None else 0.0,
            "phase_change_risk_index": phase_risk,
        }

    def _layer3(self, rin: RotatingInput, selected: Dict[str, float]) -> LayerResult:
        issues: List[ValidationIssue] = []

        if selected["vibration_mm_per_s"] > selected["vibration_limit_mm_per_s"]:
            issues.append(
                issue_from_flag(
                    "PHY.VIBRATION_LIMIT_EXCEEDED",
                    "Vibration exceeds machine limit",
                    STANDARD_REFERENCES["vibration"],
                )
            )

        if selected["nozzle_load_ratio"] > 1.0:
            issues.append(
                issue_from_flag(
                    "PHY.NOZZLE_LOAD_EXCEEDED",
                    "Nozzle load ratio exceeds allowable limit",
                    STANDARD_REFERENCES["nozzle_load"],
                )
            )

        if selected["bearing_temperature_c"] >= 80.0:
            issues.append(
                issue_from_flag(
                    "PHY.BEARING_TEMPERATURE_HIGH",
                    "Bearing temperature is above recommended caution threshold",
                    STANDARD_REFERENCES["monitoring"],
                )
            )

        if rin.machine_type == "steam_turbine":
            if selected["steam_quality_x"] < self.thresholds.min_steam_quality_warning:
                issues.append(
                    issue_from_flag(
                        "PHY.STEAM_WETNESS_EROSION_RISK",
                        "Steam quality indicates wet-steam erosion risk",
                        STANDARD_REFERENCES["steam_turbine"],
                    )
                )

            if selected["phase_change_risk_index"] >= self.thresholds.steam_phase_change_risk_block:
                issues.append(
                    issue_from_flag(
                        "PHY.STEAM_PHASE_CHANGE_RISK",
                        "Steam state is close to phase-change boundary",
                        STANDARD_REFERENCES["steam_properties"],
                    )
                )

            if (
                rin.inlet_enthalpy_kj_per_kg is not None
                and rin.outlet_enthalpy_kj_per_kg is not None
                and selected["steam_specific_energy_drop_kj_per_kg"] <= 0.0
            ):
                issues.append(
                    issue_from_flag(
                        "LOG.STEAM_STATE_INCONSISTENT",
                        "Steam enthalpy drop is non-positive",
                        STANDARD_REFERENCES["steam_properties"],
                    )
                )

        return LayerResult(
            layer="layer3_physics_standards",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "vibration_mm_per_s": selected["vibration_mm_per_s"],
                "vibration_limit_mm_per_s": selected["vibration_limit_mm_per_s"],
                "nozzle_load_ratio": selected["nozzle_load_ratio"],
                "bearing_temperature_c": selected["bearing_temperature_c"],
                "steam_quality_x": selected["steam_quality_x"],
                "steam_superheat_margin_c": selected["steam_superheat_margin_c"],
                "phase_change_risk_index": selected["phase_change_risk_index"],
            },
        )

    def _layer4(self, rin: RotatingInput, selected: Dict[str, float]) -> tuple[Dict[str, Any], LayerResult]:
        issues: List[ValidationIssue] = []

        hi = selected["bearing_health_index"]
        vib_pen = max(selected["vibration_mm_per_s"] - selected["vibration_limit_mm_per_s"], 0.0) * 1.5
        noz_pen = max(selected["nozzle_load_ratio"] - 1.0, 0.0) * 3.0
        phase_pen = selected["phase_change_risk_index"] * 0.3
        temp_pen = max(10.0 - hi - vib_pen - noz_pen - phase_pen, 0.0)
        temp_rev = 70.0 + temp_pen / 0.1

        dev_pct = relative_difference(temp_rev, rin.bearing_temperature_c) * 100.0
        if dev_pct > self.thresholds.reverse_check_tolerance_percent:
            issues.append(
                issue_from_flag(
                    "LOG.REVERSE_CHECK_DEVIATION",
                    f"Reverse bearing-temperature deviation {dev_pct:.2f}% exceeds threshold",
                    STANDARD_REFERENCES["monitoring"],
                )
            )

        enthalpy_dev_pct = 0.0
        if rin.machine_type == "steam_turbine":
            if rin.inlet_enthalpy_kj_per_kg is not None and rin.outlet_enthalpy_kj_per_kg is not None:
                reconstructed_outlet = (
                    rin.inlet_enthalpy_kj_per_kg - selected["steam_specific_energy_drop_kj_per_kg"]
                )
                enthalpy_dev_pct = relative_difference(reconstructed_outlet, rin.outlet_enthalpy_kj_per_kg) * 100.0
                if enthalpy_dev_pct > self.thresholds.reverse_check_tolerance_percent:
                    issues.append(
                        issue_from_flag(
                            "LOG.REVERSE_CHECK_DEVIATION",
                            f"Steam enthalpy reverse deviation {enthalpy_dev_pct:.2f}% exceeds threshold",
                            STANDARD_REFERENCES["steam_properties"],
                        )
                    )

        layer = LayerResult(
            layer="layer4_reverse_validation",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "reverse_bearing_temperature_c": temp_rev,
                "bearing_temperature_deviation_percent": dev_pct,
                "steam_enthalpy_deviation_percent": enthalpy_dev_pct,
            },
        )

        return layer.details, layer

    def _response(
        self,
        calculation_type: str,
        rin: RotatingInput,
        layers: List[LayerResult],
        core: Dict[str, float] | None,
        reverse_details: Dict[str, Any],
        started: float,
    ) -> Dict[str, Any]:
        issues = [issue for layer in layers for issue in layer.issues]
        flags = split_flags(issues)

        confidence = "high"
        if flags["red_flags"]:
            confidence = "low"
        elif flags["warnings"]:
            confidence = "medium"

        final = core or {}
        status = (
            calculate_status(
                final.get("vibration_mm_per_s", rin.vibration_mm_per_s),
                final.get("vibration_limit_mm_per_s", VIBRATION_LIMIT_MM_PER_S[rin.machine_type]),
                final.get("nozzle_load_ratio", rin.nozzle_load_ratio),
            )
            if final
            else "UNKNOWN"
        )
        if final:
            final["status"] = status
            final["machine_type"] = rin.machine_type
            final["monitoring_escalation"] = screen_monitoring_escalation(
                final.get("bearing_health_index", 10.0),
                final.get("vibration_mm_per_s", 0.0),
                final.get("vibration_limit_mm_per_s", 1.0),
                final.get("bearing_temperature_c", 25.0),
            )
            final["maintenance_urgency"] = screen_maintenance_urgency(
                final.get("bearing_health_index", 10.0),
                final.get("nozzle_load_ratio", 0.0),
            )

        standards_applied = [
            STANDARD_REFERENCES["vibration"],
            STANDARD_REFERENCES["nozzle_load"],
            STANDARD_REFERENCES["monitoring"],
        ]
        if rin.machine_type == "steam_turbine":
            standards_applied.extend(
                [
                    STANDARD_REFERENCES["steam_turbine"],
                    STANDARD_REFERENCES["steam_properties"],
                ]
            )

        return {
            "calculation_summary": {
                "discipline": "rotating",
                "calculation_type": calculation_type,
                "standards_applied": standards_applied,
                "confidence": confidence,
                "execution_time_sec": round(perf_counter() - started, 6),
            },
            "input_data": {
                "machine_type": rin.machine_type,
                "vibration_mm_per_s": rin.vibration_mm_per_s,
                "nozzle_load_ratio": rin.nozzle_load_ratio,
                "bearing_temperature_c": rin.bearing_temperature_c,
                "speed_rpm": rin.speed_rpm,
                "steam_pressure_bar": rin.steam_pressure_bar,
                "steam_temperature_c": rin.steam_temperature_c,
                "steam_quality_x": rin.steam_quality_x,
                "inlet_enthalpy_kj_per_kg": rin.inlet_enthalpy_kj_per_kg,
                "outlet_enthalpy_kj_per_kg": rin.outlet_enthalpy_kj_per_kg,
            },
            "calculation_steps": self._steps(final, rin.machine_type),
            "layer_results": [layer.to_dict() for layer in layers],
            "final_results": final,
            "reverse_validation": reverse_details,
            "recommendations": self._recommendations(final, flags),
            "flags": flags,
        }

    def _error_response(
        self,
        calculation_type: str,
        payload: Mapping[str, Any],
        layers: List[LayerResult],
        started: float,
    ) -> Dict[str, Any]:
        issues = [issue for layer in layers for issue in layer.issues]
        flags = split_flags(issues)

        return {
            "calculation_summary": {
                "discipline": "rotating",
                "calculation_type": calculation_type,
                "standards_applied": [],
                "confidence": "low",
                "execution_time_sec": round(perf_counter() - started, 6),
            },
            "input_data": dict(payload),
            "calculation_steps": [],
            "layer_results": [layer.to_dict() for layer in layers],
            "final_results": {},
            "reverse_validation": {},
            "recommendations": [
                {
                    "priority": "high",
                    "action": "fix_input_data",
                    "timeline": "immediate",
                    "description": "Rotating input payload failed validation",
                }
            ],
            "flags": flags,
        }

    def _steps(self, final: Dict[str, float], machine_type: str) -> List[Dict[str, Any]]:
        if not final:
            return []

        steps = [
            {
                "step_number": 1,
                "description": "Vibration check",
                "formula_used": "vibration <= machine limit",
                "standard_reference": STANDARD_REFERENCES["vibration"],
                "result": {
                    "vibration_mm_per_s": final.get("vibration_mm_per_s"),
                    "limit_mm_per_s": final.get("vibration_limit_mm_per_s"),
                },
            },
            {
                "step_number": 2,
                "description": "Nozzle load check",
                "formula_used": "nozzle_load_ratio <= 1.0",
                "standard_reference": STANDARD_REFERENCES["nozzle_load"],
                "result": {"nozzle_load_ratio": final.get("nozzle_load_ratio")},
            },
            {
                "step_number": 3,
                "description": "Bearing health index",
                "formula_used": "HI = f(vibration, nozzle_load, bearing_temperature, steam_phase_risk)",
                "standard_reference": STANDARD_REFERENCES["monitoring"],
                "result": {
                    "bearing_health_index": final.get("bearing_health_index"),
                    "inspection_interval_years": final.get("inspection_interval_years"),
                },
            },
        ]

        if machine_type == "steam_turbine":
            steps.append(
                {
                    "step_number": 4,
                    "description": "Steam state and phase-change screening",
                    "formula_used": "phase_risk = f(Psteam, Tsteam, quality, superheat_margin)",
                    "standard_reference": STANDARD_REFERENCES["steam_properties"],
                    "result": {
                        "steam_quality_x": final.get("steam_quality_x"),
                        "steam_superheat_margin_c": final.get("steam_superheat_margin_c"),
                        "phase_change_risk_index": final.get("phase_change_risk_index"),
                    },
                }
            )

        return steps

    def _recommendations(
        self,
        final: Dict[str, float],
        flags: Dict[str, List[str]],
    ) -> List[Dict[str, str]]:
        recs: List[Dict[str, str]] = []

        if "PHY.NOZZLE_LOAD_EXCEEDED" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "reduce_nozzle_load",
                    "timeline": "immediate",
                    "description": "Nozzle load ratio exceeds allowable limit",
                }
            )

        if "PHY.VIBRATION_LIMIT_EXCEEDED" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "perform_vibration_diagnosis",
                    "timeline": "immediate",
                    "description": "Machine vibration exceeds acceptance limit",
                }
            )

        if "PHY.BEARING_TEMPERATURE_HIGH" in flags["warnings"]:
            recs.append(
                {
                    "priority": "medium",
                    "action": "increase_monitoring_frequency",
                    "timeline": "1month",
                    "description": "Bearing temperature above caution threshold",
                }
            )

        if "PHY.STEAM_WETNESS_EROSION_RISK" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "dryness_fraction_review",
                    "timeline": "immediate",
                    "description": "Steam wetness risk detected. Review turbine inlet condition and moisture separation.",
                }
            )

        if "PHY.STEAM_PHASE_CHANGE_RISK" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "increase_superheat_margin",
                    "timeline": "immediate",
                    "description": "Steam condition is near phase boundary. Review steam table state and operating window.",
                }
            )

        if not recs:
            recs.append(
                {
                    "priority": "low",
                    "action": "continue_monitoring",
                    "timeline": "nextyear",
                    "description": "No immediate rotating integrity issue detected",
                }
            )

        return recs
