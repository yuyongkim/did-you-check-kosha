from __future__ import annotations

from time import perf_counter
from typing import Any, Dict, List, Mapping

from src.electrical.calculations import (
    calculate_arc_flash_energy_cal_cm2,
    calculate_inspection_interval_years,
    calculate_status,
    calculate_transformer_health_index,
    determine_arc_ppe_category,
    relative_difference,
    reverse_clearing_time_sec,
    screen_breaker_coordination_margin,
    screen_load_utilization,
)
from src.electrical.constants import (
    CONSENSUS_REL_TOLERANCE,
    EQUIPMENT_ARC_FACTOR,
    EQUIPMENT_HI_BIAS,
    STANDARD_REFERENCES,
    ElectricalThresholds,
)
from src.electrical.models import ElectricalInput, InputPayloadError, parse_electrical_input
from src.electrical.verification import (
    LayerResult,
    ValidationIssue,
    has_blocking_issue,
    issue_from_flag,
    maker_select,
    split_flags,
)


class ElectricalVerificationService:
    def __init__(self, thresholds: ElectricalThresholds | None = None) -> None:
        self.thresholds = thresholds or ElectricalThresholds()

    def evaluate(self, payload: Mapping[str, Any], calculation_type: str = "electrical_integrity") -> Dict[str, Any]:
        started = perf_counter()
        layers: List[LayerResult] = []

        try:
            ein = parse_electrical_input(payload)
        except InputPayloadError as exc:
            issue = issue_from_flag("FMT.SCHEMA_VALIDATION_FAILED", str(exc), "Electrical input schema")
            layer = LayerResult(
                layer="layer1_input_validation",
                passed=False,
                issues=[issue],
                details={"payload_keys": sorted(payload.keys())},
            )
            return self._error_response(calculation_type, payload, [layer], started)

        layer1 = self._layer1(ein)
        layers.append(layer1)
        if has_blocking_issue(layer1.issues):
            return self._response(calculation_type, ein, layers, None, {}, started)

        candidates = [
            self._single_calc(ein, "a"),
            self._single_calc(ein, "b"),
            self._single_calc(ein, "c"),
        ]
        layer2, selected = maker_select(candidates, CONSENSUS_REL_TOLERANCE)
        layers.append(layer2)

        layer3 = self._layer3(ein, selected)
        layers.append(layer3)

        reverse_details, layer4 = self._layer4(ein, selected)
        layers.append(layer4)

        return self._response(calculation_type, ein, layers, selected, reverse_details, started)

    def _layer1(self, ein: ElectricalInput) -> LayerResult:
        issues: List[ValidationIssue] = []
        t = self.thresholds

        if ein.system_voltage_kv < t.min_voltage_kv or ein.system_voltage_kv > t.max_voltage_kv:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"system_voltage_kv out of range: {ein.system_voltage_kv}",
                    STANDARD_REFERENCES["voltage_drop"],
                )
            )

        if ein.bolted_fault_current_ka < t.min_fault_current_ka or ein.bolted_fault_current_ka > t.max_fault_current_ka:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"bolted_fault_current_ka out of range: {ein.bolted_fault_current_ka}",
                    STANDARD_REFERENCES["short_circuit"],
                )
            )

        if ein.clearing_time_sec <= 0 or ein.clearing_time_sec > t.max_clearing_time_sec:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"clearing_time_sec out of range: {ein.clearing_time_sec}",
                    STANDARD_REFERENCES["arc_flash"],
                )
            )

        if ein.working_distance_mm < t.min_working_distance_mm or ein.working_distance_mm > t.max_working_distance_mm:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"working_distance_mm out of range: {ein.working_distance_mm}",
                    STANDARD_REFERENCES["arc_flash"],
                )
            )

        for score_name, value in {
            "dga_score": ein.dga_score,
            "oil_quality_score": ein.oil_quality_score,
            "insulation_score": ein.insulation_score,
            "load_factor_score": ein.load_factor_score,
        }.items():
            if value < 0 or value > 10:
                issues.append(
                    issue_from_flag(
                        "STD.OUT_OF_SCOPE_APPLICATION",
                        f"{score_name} must be in [0,10], got {value}",
                        STANDARD_REFERENCES["health_index"],
                    )
                )

        return LayerResult(
            layer="layer1_input_validation",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "system_voltage_kv": ein.system_voltage_kv,
                "fault_current_ka": ein.bolted_fault_current_ka,
                "clearing_time_sec": ein.clearing_time_sec,
            },
        )

    def _single_calc(self, ein: ElectricalInput, variant: str) -> Dict[str, float]:
        dga = ein.dga_score
        oil = ein.oil_quality_score
        ins = ein.insulation_score
        load = ein.load_factor_score
        clearing = ein.clearing_time_sec
        vdrop = ein.voltage_drop_percent

        if variant == "b":
            dga = dga * 1.001
            clearing = clearing * 1.001
        elif variant == "c":
            oil = oil * 0.999
            vdrop = vdrop * 1.001

        equipment_arc_factor = EQUIPMENT_ARC_FACTOR.get(ein.equipment_type, 1.0)
        equipment_hi_bias = EQUIPMENT_HI_BIAS.get(ein.equipment_type, 0.0)

        hi = calculate_transformer_health_index(
            dga_score=dga,
            oil_quality_score=oil,
            insulation_score=ins,
            load_factor_score=load,
        )
        hi = max(0.0, min(10.0, hi + equipment_hi_bias))
        arc_energy = calculate_arc_flash_energy_cal_cm2(
            bolted_fault_current_ka=ein.bolted_fault_current_ka,
            clearing_time_sec=clearing,
            working_distance_mm=ein.working_distance_mm,
            system_voltage_kv=ein.system_voltage_kv,
        )
        arc_energy *= equipment_arc_factor

        return {
            "transformer_health_index": hi,
            "arc_flash_energy_cal_cm2": arc_energy,
            "voltage_drop_percent": vdrop,
            "fault_current_ka": ein.bolted_fault_current_ka,
            "breaker_interrupt_rating_ka": ein.breaker_interrupt_rating_ka,
            "thd_voltage_percent": ein.thd_voltage_percent,
            "motor_current_thd_percent": ein.motor_current_thd_percent,
            "power_factor": ein.power_factor,
            "inspection_interval_years": calculate_inspection_interval_years(hi, arc_energy),
        }

    def _layer3(self, ein: ElectricalInput, selected: Dict[str, float]) -> LayerResult:
        _ = ein
        issues: List[ValidationIssue] = []

        if selected["transformer_health_index"] < 3.0:
            issues.append(
                issue_from_flag(
                    "PHY.TRANSFORMER_HEALTH_CRITICAL",
                    "Transformer health index below critical threshold",
                    STANDARD_REFERENCES["health_index"],
                )
            )

        if selected["arc_flash_energy_cal_cm2"] > 40.0:
            issues.append(
                issue_from_flag(
                    "PHY.ARC_FLASH_ENERGY_EXCEEDED",
                    "Arc-flash energy exceeds 40 cal/cm^2 limit",
                    STANDARD_REFERENCES["arc_flash"],
                )
            )

        if selected["voltage_drop_percent"] > 5.0:
            issues.append(
                issue_from_flag(
                    "PHY.VOLTAGE_DROP_EXCEEDED",
                    "Voltage drop exceeds 5% recommended limit",
                    STANDARD_REFERENCES["voltage_drop"],
                )
            )

        if selected["fault_current_ka"] > selected["breaker_interrupt_rating_ka"]:
            issues.append(
                issue_from_flag(
                    "PHY.BREAKER_INTERRUPT_RATING_EXCEEDED",
                    "Fault current exceeds breaker interrupt rating",
                    STANDARD_REFERENCES["short_circuit"],
                )
            )

        if selected["thd_voltage_percent"] > 8.0:
            issues.append(
                issue_from_flag(
                    "PHY.HARMONIC_DISTORTION_EXCEEDED",
                    "Voltage THD exceeds 8% threshold",
                    STANDARD_REFERENCES["harmonic"],
                )
            )

        return LayerResult(
            layer="layer3_physics_standards",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "health_index": selected["transformer_health_index"],
                "arc_flash_energy_cal_cm2": selected["arc_flash_energy_cal_cm2"],
                "voltage_drop_percent": selected["voltage_drop_percent"],
                "fault_current_ka": selected["fault_current_ka"],
                "breaker_interrupt_rating_ka": selected["breaker_interrupt_rating_ka"],
                "thd_voltage_percent": selected["thd_voltage_percent"],
            },
        )

    def _layer4(self, ein: ElectricalInput, selected: Dict[str, float]) -> tuple[Dict[str, Any], LayerResult]:
        issues: List[ValidationIssue] = []

        clearing_rev = reverse_clearing_time_sec(
            arc_flash_energy_cal_cm2=selected["arc_flash_energy_cal_cm2"],
            bolted_fault_current_ka=selected["fault_current_ka"],
            working_distance_mm=ein.working_distance_mm,
            system_voltage_kv=ein.system_voltage_kv,
        )

        dev_pct = None
        if clearing_rev is not None:
            dev_pct = relative_difference(clearing_rev, ein.clearing_time_sec) * 100.0
            if dev_pct > self.thresholds.reverse_check_tolerance_percent:
                issues.append(
                    issue_from_flag(
                        "LOG.REVERSE_CHECK_DEVIATION",
                        f"Reverse clearing-time deviation {dev_pct:.2f}% exceeds threshold",
                        STANDARD_REFERENCES["arc_flash"],
                    )
                )

        layer = LayerResult(
            layer="layer4_reverse_validation",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "reverse_clearing_time_sec": clearing_rev,
                "clearing_time_deviation_percent": dev_pct,
            },
        )
        return layer.details, layer

    def _response(
        self,
        calculation_type: str,
        ein: ElectricalInput,
        layers: List[LayerResult],
        core: Dict[str, float] | None,
        reverse_details: Dict[str, Any],
        started: float,
    ) -> Dict[str, Any]:
        issues = [i for l in layers for i in l.issues]
        flags = split_flags(issues)

        confidence = "high"
        if flags["red_flags"]:
            confidence = "low"
        elif flags["warnings"]:
            confidence = "medium"

        final = core or {}
        if final:
            final["equipment_type"] = ein.equipment_type
            final["ppe_category"] = determine_arc_ppe_category(final["arc_flash_energy_cal_cm2"])
            final["status"] = calculate_status(
                health_index=final["transformer_health_index"],
                arc_flash_energy_cal_cm2=final["arc_flash_energy_cal_cm2"],
                voltage_drop_percent=final["voltage_drop_percent"],
                fault_current_ka=final["fault_current_ka"],
                breaker_interrupt_rating_ka=final["breaker_interrupt_rating_ka"],
            )
            final["breaker_coordination_margin"] = round(screen_breaker_coordination_margin(
                final["fault_current_ka"], final["breaker_interrupt_rating_ka"]
            ), 3)
            final["load_utilization"] = screen_load_utilization(ein.load_factor_score)

        return {
            "calculation_summary": {
                "discipline": "electrical",
                "calculation_type": calculation_type,
                "standards_applied": [
                    STANDARD_REFERENCES["health_index"],
                    STANDARD_REFERENCES["arc_flash"],
                    STANDARD_REFERENCES["safety"],
                    STANDARD_REFERENCES["voltage_drop"],
                    STANDARD_REFERENCES["short_circuit"],
                ],
                "confidence": confidence,
                "execution_time_sec": round(perf_counter() - started, 6),
            },
            "input_data": {
                "equipment_type": ein.equipment_type,
                "system_voltage_kv": ein.system_voltage_kv,
                "bolted_fault_current_ka": ein.bolted_fault_current_ka,
                "clearing_time_sec": ein.clearing_time_sec,
                "working_distance_mm": ein.working_distance_mm,
                "breaker_interrupt_rating_ka": ein.breaker_interrupt_rating_ka,
                "voltage_drop_percent": ein.voltage_drop_percent,
                "thd_voltage_percent": ein.thd_voltage_percent,
                "motor_current_thd_percent": ein.motor_current_thd_percent,
                "power_factor": ein.power_factor,
                "dga_score": ein.dga_score,
                "oil_quality_score": ein.oil_quality_score,
                "insulation_score": ein.insulation_score,
                "load_factor_score": ein.load_factor_score,
            },
            "calculation_steps": self._steps(final),
            "layer_results": [l.to_dict() for l in layers],
            "final_results": final,
            "reverse_validation": reverse_details,
            "recommendations": self._recommendations(final, flags),
            "flags": flags,
        }

    def _error_response(self, calculation_type: str, payload: Mapping[str, Any], layers: List[LayerResult], started: float) -> Dict[str, Any]:
        issues = [i for l in layers for i in l.issues]
        flags = split_flags(issues)
        return {
            "calculation_summary": {
                "discipline": "electrical",
                "calculation_type": calculation_type,
                "standards_applied": [],
                "confidence": "low",
                "execution_time_sec": round(perf_counter() - started, 6),
            },
            "input_data": dict(payload),
            "calculation_steps": [],
            "layer_results": [l.to_dict() for l in layers],
            "final_results": {},
            "reverse_validation": {},
            "recommendations": [
                {
                    "priority": "high",
                    "action": "fix_input_data",
                    "timeline": "immediate",
                    "description": "Electrical input payload failed validation",
                }
            ],
            "flags": flags,
        }

    def _steps(self, final: Dict[str, float]) -> List[Dict[str, Any]]:
        if not final:
            return []
        return [
            {
                "step_number": 1,
                "description": "Transformer health index",
                "formula_used": "HI = sum(weight_i * score_i)",
                "standard_reference": STANDARD_REFERENCES["health_index"],
                "result": {"value": final.get("transformer_health_index"), "unit": "index"},
            },
            {
                "step_number": 2,
                "description": "Arc-flash energy",
                "formula_used": "IEEE 1584 incident energy model (simplified)",
                "standard_reference": STANDARD_REFERENCES["arc_flash"],
                "result": {"value": final.get("arc_flash_energy_cal_cm2"), "unit": "cal/cm2"},
            },
            {
                "step_number": 3,
                "description": "Voltage drop / short-circuit checks",
                "formula_used": "voltage_drop<=5%, Ifault<=breaker_rating",
                "standard_reference": STANDARD_REFERENCES["short_circuit"],
                "result": {
                    "voltage_drop_percent": final.get("voltage_drop_percent"),
                    "fault_current_ka": final.get("fault_current_ka"),
                    "breaker_interrupt_rating_ka": final.get("breaker_interrupt_rating_ka"),
                },
            },
        ]

    def _recommendations(self, final: Dict[str, float], flags: Dict[str, List[str]]) -> List[Dict[str, str]]:
        recs: List[Dict[str, str]] = []

        if "PHY.ARC_FLASH_ENERGY_EXCEEDED" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "set_arc_flash_prohibited_zone",
                    "timeline": "immediate",
                    "description": "Incident energy exceeds 40 cal/cm2",
                }
            )
        if "PHY.BREAKER_INTERRUPT_RATING_EXCEEDED" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "upgrade_breaker_or_reduce_fault_level",
                    "timeline": "immediate",
                    "description": "Breaker interrupt rating is insufficient",
                }
            )
        if "PHY.VOLTAGE_DROP_EXCEEDED" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "review_cable_sizing",
                    "timeline": "1month",
                    "description": "Voltage drop exceeds IEEE recommendation",
                }
            )
        if "PHY.HARMONIC_DISTORTION_EXCEEDED" in flags["warnings"]:
            recs.append(
                {
                    "priority": "medium",
                    "action": "install_harmonic_filter_or_reactor",
                    "timeline": "1month",
                    "description": "Voltage THD is above recommended threshold",
                }
            )

        if not recs:
            recs.append(
                {
                    "priority": "low",
                    "action": "continue_monitoring",
                    "timeline": "nextyear",
                    "description": "No immediate electrical integrity issue detected",
                }
            )

        return recs
