from __future__ import annotations

from dataclasses import dataclass
from math import pi
from time import perf_counter
from typing import Any, Dict, List, Mapping

from src.vessel.calculations import (
    calculate_inspection_interval_years,
    calculate_remaining_life_years,
    calculate_required_shell_thickness_mm,
    relative_difference,
    reverse_design_pressure_mpa,
    screen_ffs_level,
    screen_repair_scope,
)
from src.vessel.constants import (
    ALLOWABLE_STRESS_TABLE_MPA,
    CONSENSUS_REL_TOLERANCE,
    MATERIAL_TEMP_LIMIT_C,
    STANDARD_REFERENCES,
    VALID_JOINT_EFFICIENCIES,
    VesselThresholds,
)
from src.vessel.models import InputPayloadError, VesselInput, parse_vessel_input
from src.vessel.screening import (
    calculate_external_pressure_allowable_screen_mpa,
    calculate_nozzle_reinforcement_index,
)
from src.vessel.verification import (
    LayerResult,
    ValidationIssue,
    has_blocking_issue,
    issue_from_flag,
    maker_select,
    split_flags,
)


@dataclass
class VesselCalcContext:
    allowable_stress_mpa: float


class VesselVerificationService:
    def __init__(self, thresholds: VesselThresholds | None = None) -> None:
        self.thresholds = thresholds or VesselThresholds()

    def evaluate(self, payload: Mapping[str, Any], calculation_type: str = "vessel_integrity") -> Dict[str, Any]:
        started = perf_counter()
        layers: List[LayerResult] = []

        try:
            vin = parse_vessel_input(payload)
        except InputPayloadError as exc:
            issue = issue_from_flag("FMT.SCHEMA_VALIDATION_FAILED", str(exc), "Vessel input schema")
            layer = LayerResult(
                layer="layer1_input_validation",
                passed=False,
                issues=[issue],
                details={"payload_keys": sorted(payload.keys())},
            )
            return self._error_response(calculation_type, payload, [layer], started)

        layer1 = self._layer1(vin)
        layers.append(layer1)
        if has_blocking_issue(layer1.issues):
            return self._response(calculation_type, vin, layers, None, {}, started)

        context, lookup_issues = self._lookup_context(vin)
        if lookup_issues:
            layers.append(
                LayerResult(
                    layer="layer1_standard_context",
                    passed=not has_blocking_issue(lookup_issues),
                    issues=lookup_issues,
                    details={},
                )
            )
        if has_blocking_issue(lookup_issues):
            return self._response(calculation_type, vin, layers, None, {}, started)

        candidates = [
            self._single_calc(vin, context, "a"),
            self._single_calc(vin, context, "b"),
            self._single_calc(vin, context, "c"),
        ]
        layer2, selected = maker_select(candidates, CONSENSUS_REL_TOLERANCE)
        layers.append(layer2)

        layer3 = self._layer3(vin, selected)
        layers.append(layer3)

        reverse_details, layer4 = self._layer4(vin, selected, context)
        layers.append(layer4)

        return self._response(calculation_type, vin, layers, selected, reverse_details, started)

    def _layer1(self, vin: VesselInput) -> LayerResult:
        issues: List[ValidationIssue] = []
        t = self.thresholds

        if vin.material not in ALLOWABLE_STRESS_TABLE_MPA:
            issues.append(issue_from_flag("STD.UNAPPROVED_MATERIAL", f"Unsupported material {vin.material}", STANDARD_REFERENCES["shell_thickness"]))
        if vin.design_pressure_mpa <= t.min_pressure_mpa or vin.design_pressure_mpa >= t.max_pressure_mpa:
            issues.append(issue_from_flag("STD.OUT_OF_SCOPE_APPLICATION", f"Pressure out of range: {vin.design_pressure_mpa}", "Vessel pressure range policy"))
        if vin.design_temperature_c <= t.min_temperature_c or vin.design_temperature_c >= t.max_temperature_c:
            issues.append(issue_from_flag("STD.OUT_OF_SCOPE_APPLICATION", f"Temperature out of range: {vin.design_temperature_c}", "Vessel temperature range policy"))
        if vin.inside_radius_mm <= 0 or vin.current_thickness_mm <= 0:
            issues.append(issue_from_flag("PHY.NEGATIVE_THICKNESS", "Radius and thickness must be positive", "Physical sanity"))
        if vin.shell_length_mm is not None and vin.shell_length_mm <= 0:
            issues.append(issue_from_flag("PHY.NEGATIVE_THICKNESS", "Shell length must be positive", "Physical sanity"))
        if vin.straight_shell_height_mm is not None and vin.straight_shell_height_mm <= 0:
            issues.append(issue_from_flag("PHY.NEGATIVE_THICKNESS", "Straight shell height must be positive", "Physical sanity"))
        if vin.head_depth_mm is not None and vin.head_depth_mm < 0:
            issues.append(issue_from_flag("PHY.NEGATIVE_THICKNESS", "Head depth cannot be negative", "Physical sanity"))
        if vin.nozzle_od_mm is not None and vin.nozzle_od_mm <= 0:
            issues.append(issue_from_flag("PHY.NEGATIVE_THICKNESS", "Nozzle OD must be positive", "Physical sanity"))
        if vin.external_pressure_mpa is not None and vin.external_pressure_mpa < 0:
            issues.append(issue_from_flag("PHY.NEGATIVE_THICKNESS", "External pressure cannot be negative", "Physical sanity"))
        if vin.reinforcement_pad_thickness_mm is not None and vin.reinforcement_pad_thickness_mm < 0:
            issues.append(issue_from_flag("PHY.NEGATIVE_THICKNESS", "Reinforcement pad thickness cannot be negative", "Physical sanity"))
        if vin.reinforcement_pad_width_mm is not None and vin.reinforcement_pad_width_mm < 0:
            issues.append(issue_from_flag("PHY.NEGATIVE_THICKNESS", "Reinforcement pad width cannot be negative", "Physical sanity"))
        if vin.joint_efficiency not in VALID_JOINT_EFFICIENCIES:
            issues.append(issue_from_flag("STD.JOINT_EFFICIENCY_INVALID", f"Invalid joint efficiency: {vin.joint_efficiency}", STANDARD_REFERENCES["joint_efficiency"]))

        if self._is_vertical_type(vin.vessel_type) and vin.straight_shell_height_mm is None:
            issues.append(
                issue_from_flag(
                    "DATA.VESSEL_DIMENSION_CONTEXT_MISSING",
                    "Vertical/column vessels should include straight shell height for screening context",
                    STANDARD_REFERENCES["shell_thickness"],
                )
            )
        if not self._is_vertical_type(vin.vessel_type) and vin.shell_length_mm is None:
            issues.append(
                issue_from_flag(
                    "DATA.VESSEL_DIMENSION_CONTEXT_MISSING",
                    "Horizontal/shell-side vessels should include shell length for screening context",
                    STANDARD_REFERENCES["shell_thickness"],
                )
            )
        if vin.head_type != "flat" and vin.head_depth_mm is None:
            issues.append(
                issue_from_flag(
                    "DATA.VESSEL_DIMENSION_CONTEXT_MISSING",
                    "Head depth is missing; default geometry estimate will be used",
                    STANDARD_REFERENCES["shell_thickness"],
                )
            )

        return LayerResult(
            layer="layer1_input_validation",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "material": vin.material,
                "vessel_type": vin.vessel_type,
                "head_type": vin.head_type,
                "pressure_mpa": vin.design_pressure_mpa,
                "temperature_c": vin.design_temperature_c,
                "joint_efficiency": vin.joint_efficiency,
            },
        )

    def _lookup_context(self, vin: VesselInput) -> tuple[VesselCalcContext, List[ValidationIssue]]:
        issues: List[ValidationIssue] = []
        table = ALLOWABLE_STRESS_TABLE_MPA.get(vin.material, {})
        if not table:
            return VesselCalcContext(allowable_stress_mpa=0.0), [
                issue_from_flag("STD.UNAPPROVED_MATERIAL", f"No stress table for {vin.material}", STANDARD_REFERENCES["shell_thickness"])
            ]

        keys = sorted(table.keys())
        if vin.design_temperature_c <= keys[0]:
            stress = table[keys[0]]
        elif vin.design_temperature_c >= keys[-1]:
            stress = table[keys[-1]]
        else:
            stress = table[keys[0]]
            for i in range(len(keys) - 1):
                left = keys[i]
                right = keys[i + 1]
                if left <= vin.design_temperature_c <= right:
                    lv = table[left]
                    rv = table[right]
                    ratio = (vin.design_temperature_c - left) / (right - left)
                    stress = lv + ratio * (rv - lv)
                    break

        return VesselCalcContext(allowable_stress_mpa=stress), issues

    def _single_calc(self, vin: VesselInput, context: VesselCalcContext, variant: str) -> Dict[str, float]:
        e = vin.joint_efficiency
        _ = variant

        t_req = calculate_required_shell_thickness_mm(
            design_pressure_mpa=vin.design_pressure_mpa,
            inside_radius_mm=vin.inside_radius_mm,
            allowable_stress_mpa=context.allowable_stress_mpa,
            joint_efficiency=e,
            corrosion_allowance_mm=vin.corrosion_allowance_mm,
        )
        rl = calculate_remaining_life_years(
            current_thickness_mm=vin.current_thickness_mm,
            required_thickness_mm=t_req,
            corrosion_rate_mm_per_year=vin.assumed_corrosion_rate_mm_per_year,
        )
        interval = calculate_inspection_interval_years(rl)
        return {
            "t_required_shell_mm": t_req,
            "remaining_life_years": rl,
            "inspection_interval_years": interval,
            "corrosion_rate_selected_mm_per_year": vin.assumed_corrosion_rate_mm_per_year,
        }

    @staticmethod
    def _is_vertical_type(vessel_type: str) -> bool:
        return vessel_type in {"vertical_vessel", "column_tower", "reactor"}

    @staticmethod
    def _default_head_depth_mm(head_type: str, inside_radius_mm: float) -> float:
        if head_type == "flat":
            return 0.0
        if head_type == "hemispherical":
            return inside_radius_mm
        if head_type == "torispherical":
            return 0.36 * inside_radius_mm
        return 0.5 * inside_radius_mm

    @staticmethod
    def _head_volume_factor(head_type: str) -> float:
        if head_type == "flat":
            return 0.0
        if head_type == "hemispherical":
            return 4.0 / 3.0
        if head_type == "torispherical":
            return 0.5
        return 2.0 / 3.0

    def _dimension_metrics(self, vin: VesselInput) -> Dict[str, Any]:
        diameter_mm = 2.0 * vin.inside_radius_mm
        if self._is_vertical_type(vin.vessel_type):
            span_mm = vin.straight_shell_height_mm or vin.shell_length_mm or (4.0 * diameter_mm)
            span_source = (
                "straight_shell_height_mm"
                if vin.straight_shell_height_mm is not None
                else "shell_length_mm"
                if vin.shell_length_mm is not None
                else "estimated_4D"
            )
        else:
            span_mm = vin.shell_length_mm or vin.straight_shell_height_mm or (4.0 * diameter_mm)
            span_source = (
                "shell_length_mm"
                if vin.shell_length_mm is not None
                else "straight_shell_height_mm"
                if vin.straight_shell_height_mm is not None
                else "estimated_4D"
            )

        head_depth_mm = vin.head_depth_mm if vin.head_depth_mm is not None else self._default_head_depth_mm(vin.head_type, vin.inside_radius_mm)
        slenderness_ld = span_mm / max(diameter_mm, 1e-9)

        body_volume_m3 = (pi * (vin.inside_radius_mm**2) * span_mm) / 1_000_000_000.0
        heads_volume_m3 = (self._head_volume_factor(vin.head_type) * pi * (vin.inside_radius_mm**3)) / 1_000_000_000.0
        shell_area_m2 = (pi * diameter_mm * span_mm) / 1_000_000.0
        opening_ratio = (vin.nozzle_od_mm / diameter_mm) if vin.nozzle_od_mm is not None and diameter_mm > 0 else None

        return {
            "diameter_mm": round(diameter_mm, 2),
            "governing_span_mm": round(span_mm, 2),
            "span_source": span_source,
            "head_type": vin.head_type,
            "head_depth_mm_used": round(head_depth_mm, 2),
            "nozzle_od_mm": None if vin.nozzle_od_mm is None else round(vin.nozzle_od_mm, 2),
            "external_pressure_mpa_input": None if vin.external_pressure_mpa is None else round(vin.external_pressure_mpa, 4),
            "reinforcement_pad_thickness_mm_used": None if vin.reinforcement_pad_thickness_mm is None else round(vin.reinforcement_pad_thickness_mm, 2),
            "reinforcement_pad_width_mm_used": None if vin.reinforcement_pad_width_mm is None else round(vin.reinforcement_pad_width_mm, 2),
            "nozzle_opening_ratio": None if opening_ratio is None else round(opening_ratio, 3),
            "slenderness_ld_ratio": round(slenderness_ld, 3),
            "shell_surface_area_m2": round(shell_area_m2, 3),
            "estimated_internal_volume_m3": round(body_volume_m3 + heads_volume_m3, 3),
        }

    def _layer3(self, vin: VesselInput, selected: Dict[str, float]) -> LayerResult:
        issues: List[ValidationIssue] = []
        dim_metrics = self._dimension_metrics(vin)

        if vin.current_thickness_mm < selected["t_required_shell_mm"]:
            issues.append(
                issue_from_flag(
                    "PHY.CURRENT_THICKNESS_BELOW_MINIMUM",
                    "Vessel current thickness is below required shell thickness",
                    STANDARD_REFERENCES["shell_thickness"],
                )
            )

        limit = MATERIAL_TEMP_LIMIT_C.get(vin.material)
        if limit is not None and vin.design_temperature_c > limit:
            issues.append(
                issue_from_flag(
                    "PHY.TEMPERATURE_LIMIT_EXCEEDED",
                    f"Design temperature {vin.design_temperature_c}C exceeds {vin.material} limit {limit}C",
                    STANDARD_REFERENCES["shell_thickness"],
                )
            )

        ld_ratio = float(dim_metrics["slenderness_ld_ratio"])
        if ld_ratio > 8.0:
            issues.append(
                issue_from_flag(
                    "PHY.VESSEL_HIGH_LD_RATIO",
                    f"High vessel L/D ratio ({ld_ratio:.2f}) may require additional stiffness/nozzle-load screening",
                    STANDARD_REFERENCES["local_thinning"],
                )
            )

        ext_allowable = None
        ext_utilization = None
        if vin.external_pressure_mpa is not None:
            ext_allowable = calculate_external_pressure_allowable_screen_mpa(
                shell_thickness_mm=vin.current_thickness_mm,
                diameter_mm=float(dim_metrics["diameter_mm"]),
                span_mm=float(dim_metrics["governing_span_mm"]),
            )
            if ext_allowable > 0:
                ext_utilization = vin.external_pressure_mpa / ext_allowable
                if ext_utilization > 1.2:
                    issues.append(
                        issue_from_flag(
                            "PHY.VESSEL_EXTERNAL_PRESSURE_RISK",
                            f"External pressure utilization {ext_utilization:.2f} exceeds screening limit",
                            STANDARD_REFERENCES["external_pressure"],
                        )
                    )
                elif ext_utilization > 1.0:
                    issues.append(
                        issue_from_flag(
                            "PHY.VESSEL_EXTERNAL_PRESSURE_REVIEW",
                            f"External pressure utilization {ext_utilization:.2f} is above review threshold",
                            STANDARD_REFERENCES["external_pressure"],
                        )
                    )

        nozzle_index = None
        opening_ratio = dim_metrics.get("nozzle_opening_ratio")
        if vin.nozzle_od_mm is not None and opening_ratio is not None:
            nozzle_index = calculate_nozzle_reinforcement_index(
                nozzle_od_mm=vin.nozzle_od_mm,
                shell_thickness_mm=vin.current_thickness_mm,
                required_shell_thickness_mm=selected["t_required_shell_mm"],
                reinforcement_pad_thickness_mm=vin.reinforcement_pad_thickness_mm or 0.0,
                reinforcement_pad_width_mm=vin.reinforcement_pad_width_mm or 0.0,
            )
            if nozzle_index is not None:
                if nozzle_index < 0.8:
                    issues.append(
                        issue_from_flag(
                            "PHY.VESSEL_NOZZLE_REINFORCEMENT_RISK",
                            f"Nozzle reinforcement index {nozzle_index:.2f} below screening minimum",
                            STANDARD_REFERENCES["nozzle_reinforcement"],
                        )
                    )
                elif nozzle_index < 1.0:
                    issues.append(
                        issue_from_flag(
                            "PHY.VESSEL_NOZZLE_REINFORCEMENT_REVIEW",
                            f"Nozzle reinforcement index {nozzle_index:.2f} requires detailed check",
                            STANDARD_REFERENCES["nozzle_reinforcement"],
                        )
                    )

            if float(opening_ratio) > 0.8:
                issues.append(
                    issue_from_flag(
                        "PHY.VESSEL_NOZZLE_REINFORCEMENT_REVIEW",
                        f"Nozzle opening ratio {float(opening_ratio):.2f} is high for shell screen",
                        STANDARD_REFERENCES["nozzle_reinforcement"],
                    )
                )

        margin = vin.current_thickness_mm - selected["t_required_shell_mm"]
        if margin < 0.5 and margin >= 0:
            issues.append(
                issue_from_flag(
                    "LOG.REVERSE_CHECK_DEVIATION",
                    "Low thickness margin indicates local thinning risk screening required",
                    STANDARD_REFERENCES["local_thinning"],
                )
            )

        return LayerResult(
            layer="layer3_physics_standards",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "current_thickness_mm": vin.current_thickness_mm,
                "required_thickness_mm": selected["t_required_shell_mm"],
                "margin_mm": margin,
                "slenderness_ld_ratio": ld_ratio,
                "span_source": dim_metrics["span_source"],
                "external_pressure_allowable_screen_mpa": ext_allowable,
                "external_pressure_utilization": ext_utilization,
                "nozzle_reinforcement_index": nozzle_index,
                "nozzle_opening_ratio": opening_ratio,
            },
        )

    def _layer4(self, vin: VesselInput, selected: Dict[str, float], context: VesselCalcContext) -> tuple[Dict[str, Any], LayerResult]:
        issues: List[ValidationIssue] = []

        p_rev = reverse_design_pressure_mpa(
            required_thickness_mm=selected["t_required_shell_mm"],
            corrosion_allowance_mm=vin.corrosion_allowance_mm,
            inside_radius_mm=vin.inside_radius_mm,
            allowable_stress_mpa=context.allowable_stress_mpa,
            joint_efficiency=vin.joint_efficiency,
        )

        dev_pct = None
        if p_rev is not None:
            dev_pct = relative_difference(p_rev, vin.design_pressure_mpa) * 100.0
            if dev_pct > self.thresholds.reverse_check_tolerance_percent:
                issues.append(
                    issue_from_flag(
                        "LOG.REVERSE_CHECK_DEVIATION",
                        f"Reverse pressure deviation {dev_pct:.2f}% exceeds threshold",
                        STANDARD_REFERENCES["shell_thickness"],
                    )
                )

        layer = LayerResult(
            layer="layer4_reverse_validation",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "reverse_pressure_mpa": p_rev,
                "pressure_deviation_percent": dev_pct,
            },
        )
        return layer.details, layer

    def _response(
        self,
        calculation_type: str,
        vin: VesselInput,
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

        final: Dict[str, Any] = dict(core or {})
        final.update(self._dimension_metrics(vin))
        if "t_required_shell_mm" in final:
            t_required = float(final["t_required_shell_mm"])
            ext_allowable = None
            ext_utilization = None
            if vin.external_pressure_mpa is not None:
                ext_allowable = calculate_external_pressure_allowable_screen_mpa(
                    shell_thickness_mm=vin.current_thickness_mm,
                    diameter_mm=float(final.get("diameter_mm", 0.0)),
                    span_mm=float(final.get("governing_span_mm", 0.0)),
                )
                if ext_allowable > 0:
                    ext_utilization = vin.external_pressure_mpa / ext_allowable
            nozzle_index = None
            if vin.nozzle_od_mm is not None:
                nozzle_index = calculate_nozzle_reinforcement_index(
                    nozzle_od_mm=vin.nozzle_od_mm,
                    shell_thickness_mm=vin.current_thickness_mm,
                    required_shell_thickness_mm=t_required,
                    reinforcement_pad_thickness_mm=vin.reinforcement_pad_thickness_mm or 0.0,
                    reinforcement_pad_width_mm=vin.reinforcement_pad_width_mm or 0.0,
                )
            final.update(
                {
                    "external_pressure_allowable_screen_mpa": None if ext_allowable is None else round(ext_allowable, 4),
                    "external_pressure_utilization": None if ext_utilization is None else round(ext_utilization, 3),
                    "nozzle_reinforcement_index": None if nozzle_index is None else round(nozzle_index, 3),
                }
            )
            ffs_level = screen_ffs_level(
                vin.current_thickness_mm,
                t_required,
                vin.assumed_corrosion_rate_mm_per_year,
                float(final.get("remaining_life_years", 0)),
            )
            final["ffs_screening_level"] = ffs_level
            final["repair_scope_screening"] = screen_repair_scope(ffs_level, vin.assumed_corrosion_rate_mm_per_year)
        recommendations = self._recommendations(final, flags)

        return {
            "calculation_summary": {
                "discipline": "vessel",
                "calculation_type": calculation_type,
                "standards_applied": [
                    STANDARD_REFERENCES["shell_thickness"],
                    STANDARD_REFERENCES["external_pressure"],
                    STANDARD_REFERENCES["nozzle_reinforcement"],
                    STANDARD_REFERENCES["inspection_interval"],
                    STANDARD_REFERENCES["local_thinning"],
                ],
                "confidence": confidence,
                "execution_time_sec": round(perf_counter() - started, 6),
            },
            "input_data": {
                "material": vin.material,
                "vessel_type": vin.vessel_type,
                "design_pressure_mpa": vin.design_pressure_mpa,
                "design_temperature_c": vin.design_temperature_c,
                "inside_radius_mm": vin.inside_radius_mm,
                "shell_length_mm": vin.shell_length_mm,
                "straight_shell_height_mm": vin.straight_shell_height_mm,
                "head_type": vin.head_type,
                "head_depth_mm": vin.head_depth_mm,
                "nozzle_od_mm": vin.nozzle_od_mm,
                "external_pressure_mpa": vin.external_pressure_mpa,
                "reinforcement_pad_thickness_mm": vin.reinforcement_pad_thickness_mm,
                "reinforcement_pad_width_mm": vin.reinforcement_pad_width_mm,
                "joint_efficiency": vin.joint_efficiency,
                "current_thickness_mm": vin.current_thickness_mm,
                "corrosion_allowance_mm": vin.corrosion_allowance_mm,
            },
            "calculation_steps": self._steps(final),
            "layer_results": [l.to_dict() for l in layers],
            "final_results": final,
            "reverse_validation": reverse_details,
            "recommendations": recommendations,
            "flags": flags,
        }

    def _error_response(self, calculation_type: str, payload: Mapping[str, Any], layers: List[LayerResult], started: float) -> Dict[str, Any]:
        issues = [i for l in layers for i in l.issues]
        flags = split_flags(issues)

        return {
            "calculation_summary": {
                "discipline": "vessel",
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
                    "description": "Vessel input payload failed validation",
                }
            ],
            "flags": flags,
        }

    def _steps(self, final: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not final:
            return []
        steps: List[Dict[str, Any]] = [
            {
                "step_number": 1,
                "description": "Required shell thickness",
                "formula_used": "t = (P*R)/(S*E - 0.6P) + CA",
                "standard_reference": STANDARD_REFERENCES["shell_thickness"],
                "result": {"value": final.get("t_required_shell_mm"), "unit": "mm"},
            },
            {
                "step_number": 2,
                "description": "Remaining life",
                "formula_used": "RL = (t_current - t_required)/CR",
                "standard_reference": STANDARD_REFERENCES["inspection_interval"],
                "result": {"value": final.get("remaining_life_years"), "unit": "years"},
            },
            {
                "step_number": 3,
                "description": "Inspection interval",
                "formula_used": "API 510 interval policy",
                "standard_reference": STANDARD_REFERENCES["inspection_interval"],
                "result": {"value": final.get("inspection_interval_years"), "unit": "years"},
            },
        ]
        if final.get("external_pressure_allowable_screen_mpa") is not None:
            steps.append(
                {
                    "step_number": 4,
                    "description": "External pressure screening",
                    "formula_used": "P_allow_screen ~ f(E, t/D, L/D) (conservative screen)",
                    "standard_reference": STANDARD_REFERENCES["external_pressure"],
                    "result": {
                        "allowable_screen_mpa": final.get("external_pressure_allowable_screen_mpa"),
                        "utilization": final.get("external_pressure_utilization"),
                    },
                }
            )
        if final.get("nozzle_reinforcement_index") is not None:
            steps.append(
                {
                    "step_number": 5,
                    "description": "Nozzle reinforcement screening",
                    "formula_used": "Index = A_available / A_required (screening)",
                    "standard_reference": STANDARD_REFERENCES["nozzle_reinforcement"],
                    "result": {"value": final.get("nozzle_reinforcement_index"), "unit": "ratio"},
                }
            )
        return steps

    def _recommendations(self, final: Dict[str, Any], flags: Dict[str, List[str]]) -> List[Dict[str, str]]:
        recs: List[Dict[str, str]] = []
        if "PHY.CURRENT_THICKNESS_BELOW_MINIMUM" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "repair_or_replace",
                    "timeline": "immediate",
                    "description": "Current vessel thickness below required minimum",
                }
            )
        if "PHY.TEMPERATURE_LIMIT_EXCEEDED" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "review_material_selection",
                    "timeline": "immediate",
                    "description": "Material temperature applicability exceeded",
                }
            )
        if "PHY.VESSEL_EXTERNAL_PRESSURE_RISK" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "perform_detailed_external_pressure_assessment",
                    "timeline": "immediate",
                    "description": "External pressure screening indicates potential shell instability risk",
                }
            )
        if "PHY.VESSEL_NOZZLE_REINFORCEMENT_RISK" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "perform_detailed_nozzle_reinforcement_check",
                    "timeline": "immediate",
                    "description": "Nozzle reinforcement screening index is below minimum threshold",
                }
            )
        if "PHY.VESSEL_HIGH_LD_RATIO" in flags["warnings"]:
            recs.append(
                {
                    "priority": "medium",
                    "action": "perform_additional_structural_screening",
                    "timeline": "1month",
                    "description": "High L/D ratio indicates additional shell/nozzle-support screening is recommended",
                }
            )
        if "DATA.VESSEL_DIMENSION_CONTEXT_MISSING" in flags["warnings"]:
            recs.append(
                {
                    "priority": "medium",
                    "action": "complete_dimension_dataset",
                    "timeline": "1month",
                    "description": "Provide missing vessel dimensions for richer integrity context",
                }
            )
        if "PHY.VESSEL_EXTERNAL_PRESSURE_REVIEW" in flags["warnings"]:
            recs.append(
                {
                    "priority": "medium",
                    "action": "confirm_external_pressure_case_with_ug28",
                    "timeline": "1month",
                    "description": "External pressure utilization is near or above screening threshold",
                }
            )
        if "PHY.VESSEL_NOZZLE_REINFORCEMENT_REVIEW" in flags["warnings"]:
            recs.append(
                {
                    "priority": "medium",
                    "action": "review_nozzle_reinforcement_with_ug37",
                    "timeline": "1month",
                    "description": "Nozzle reinforcement screening suggests detailed UG-37 check",
                }
            )

        rl = final.get("remaining_life_years")
        if isinstance(rl, (float, int)) and rl >= 0 and rl < 2:
            recs.append(
                {
                    "priority": "high",
                    "action": "increase_inspection_frequency",
                    "timeline": "immediate",
                    "description": "Remaining life below 2 years",
                }
            )

        if not recs:
            recs.append(
                {
                    "priority": "low",
                    "action": "continue_monitoring",
                    "timeline": "nextyear",
                    "description": "No immediate vessel integrity issue detected",
                }
            )
        return recs
