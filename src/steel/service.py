from __future__ import annotations

from time import perf_counter
from typing import Any, Dict, List, Mapping

from src.steel.calculations import (
    calculate_dc_ratio,
    calculate_deflection_ratio,
    calculate_fcr_mpa,
    calculate_lambda_c,
    calculate_phi_pn_kn,
    calculate_reduced_area_mm2,
    inspection_interval_years,
    relative_difference,
    reverse_axial_demand_kn,
    screen_connection_status,
    screen_reinforcement_need,
    status_from_dc,
)
from src.steel.constants import CONSENSUS_REL_TOLERANCE, STANDARD_REFERENCES, SteelThresholds
from src.steel.models import InputPayloadError, SteelInput, parse_steel_input
from src.steel.verification import (
    LayerResult,
    ValidationIssue,
    has_blocking_issue,
    issue_from_flag,
    maker_select,
    split_flags,
)


class SteelVerificationService:
    def __init__(self, thresholds: SteelThresholds | None = None) -> None:
        self.thresholds = thresholds or SteelThresholds()

    def evaluate(self, payload: Mapping[str, Any], calculation_type: str = "steel_integrity") -> Dict[str, Any]:
        started = perf_counter()
        layers: List[LayerResult] = []

        try:
            sin = parse_steel_input(payload)
        except InputPayloadError as exc:
            issue = issue_from_flag("FMT.SCHEMA_VALIDATION_FAILED", str(exc), "Steel input schema")
            layer = LayerResult(
                layer="layer1_input_validation",
                passed=False,
                issues=[issue],
                details={"payload_keys": sorted(payload.keys())},
            )
            return self._error_response(calculation_type, payload, [layer], started)

        layer1 = self._layer1(sin)
        layers.append(layer1)
        if has_blocking_issue(layer1.issues):
            return self._response(calculation_type, sin, layers, None, {}, started)

        candidates = [
            self._single_calc(sin, "a"),
            self._single_calc(sin, "b"),
            self._single_calc(sin, "c"),
        ]
        layer2, selected = maker_select(candidates, CONSENSUS_REL_TOLERANCE)
        layers.append(layer2)

        layer3 = self._layer3(sin, selected)
        layers.append(layer3)

        reverse_details, layer4 = self._layer4(sin, selected)
        layers.append(layer4)

        return self._response(calculation_type, sin, layers, selected, reverse_details, started)

    def _layer1(self, sin: SteelInput) -> LayerResult:
        issues: List[ValidationIssue] = []
        t = self.thresholds

        if sin.length_m < t.min_length_m or sin.length_m > t.max_length_m:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"length_m out of range: {sin.length_m}",
                    STANDARD_REFERENCES["compression"],
                )
            )
        if sin.radius_of_gyration_mm < t.min_radius_gyration_mm or sin.radius_of_gyration_mm > t.max_radius_gyration_mm:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"radius_of_gyration_mm out of range: {sin.radius_of_gyration_mm}",
                    STANDARD_REFERENCES["compression"],
                )
            )
        if sin.yield_strength_mpa < t.min_yield_strength_mpa or sin.yield_strength_mpa > t.max_yield_strength_mpa:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"yield_strength_mpa out of range: {sin.yield_strength_mpa}",
                    STANDARD_REFERENCES["compression"],
                )
            )
        if sin.gross_area_mm2 <= 0 or sin.axial_demand_kn < 0:
            issues.append(
                issue_from_flag(
                    "DATA.MISSING_MANDATORY_FIELD",
                    "gross_area_mm2 must be >0 and axial_demand_kn >=0",
                    STANDARD_REFERENCES["dc_ratio"],
                )
            )
        if sin.corrosion_loss_percent < 0 or sin.corrosion_loss_percent > 95:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"corrosion_loss_percent out of range: {sin.corrosion_loss_percent}",
                    STANDARD_REFERENCES["corrosion"],
                )
            )

        return LayerResult(
            layer="layer1_input_validation",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "member_type": sin.member_type,
                "steel_grade": sin.steel_grade,
                "length_m": sin.length_m,
                "fy_mpa": sin.yield_strength_mpa,
                "corrosion_loss_percent": sin.corrosion_loss_percent,
            },
        )

    def _single_calc(self, sin: SteelInput, variant: str) -> Dict[str, float]:
        corrosion = sin.corrosion_loss_percent
        pu = sin.axial_demand_kn
        rg = sin.radius_of_gyration_mm
        if variant == "b":
            corrosion *= 1.001
        elif variant == "c":
            pu *= 0.999
            rg *= 1.001

        reduced_area = calculate_reduced_area_mm2(sin.gross_area_mm2, corrosion)
        lambda_c = calculate_lambda_c(
            k_factor=sin.k_factor,
            length_m=sin.length_m,
            radius_of_gyration_mm=rg,
            fy_mpa=sin.yield_strength_mpa,
            e_modulus_mpa=sin.elasticity_mpa,
        )
        fcr = calculate_fcr_mpa(lambda_c, sin.yield_strength_mpa)
        phi_pn = calculate_phi_pn_kn(fcr, reduced_area)
        dc = calculate_dc_ratio(pu, phi_pn)
        defl_ratio = calculate_deflection_ratio(sin.deflection_mm, sin.span_mm)

        return {
            "reduced_area_mm2": reduced_area,
            "lambda_c": lambda_c,
            "fcr_mpa": fcr,
            "phi_pn_kn": phi_pn,
            "dc_ratio": dc,
            "deflection_ratio": defl_ratio,
            "corrosion_loss_percent": corrosion,
        }

    def _layer3(self, sin: SteelInput, selected: Dict[str, float]) -> LayerResult:
        _ = sin
        issues: List[ValidationIssue] = []

        if selected["dc_ratio"] >= 1.5:
            issues.append(
                issue_from_flag(
                    "PHY.STRUCTURAL_DC_CRITICAL",
                    "Structural D/C ratio exceeds 1.5",
                    STANDARD_REFERENCES["dc_ratio"],
                )
            )
        elif selected["dc_ratio"] >= 1.05:
            issues.append(
                issue_from_flag(
                    "PHY.STRUCTURAL_DC_OVERSTRESSED",
                    "Structural D/C ratio exceeds 1.05",
                    STANDARD_REFERENCES["dc_ratio"],
                )
            )

        if selected["corrosion_loss_percent"] >= 50.0:
            issues.append(
                issue_from_flag(
                    "PHY.STEEL_CORROSION_SECTION_LOSS_HIGH",
                    "Steel section loss exceeds 50%",
                    STANDARD_REFERENCES["corrosion"],
                )
            )

        if selected["deflection_ratio"] > 1.0:
            issues.append(
                issue_from_flag(
                    "PHY.STEEL_DEFLECTION_EXCEEDED",
                    "Deflection exceeds L/240 serviceability limit",
                    STANDARD_REFERENCES["serviceability"],
                )
            )

        if sin.connection_failure_detected:
            issues.append(
                issue_from_flag(
                    "PHY.CONNECTION_FAILURE_DETECTED",
                    "Connection failure detected",
                    STANDARD_REFERENCES["dc_ratio"],
                )
            )

        return LayerResult(
            layer="layer3_physics_standards",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "dc_ratio": selected["dc_ratio"],
                "corrosion_loss_percent": selected["corrosion_loss_percent"],
                "deflection_ratio": selected["deflection_ratio"],
            },
        )

    def _layer4(self, sin: SteelInput, selected: Dict[str, float]) -> tuple[Dict[str, Any], LayerResult]:
        issues: List[ValidationIssue] = []
        pu_rev = reverse_axial_demand_kn(selected["dc_ratio"], selected["phi_pn_kn"])
        dev_pct = relative_difference(pu_rev, sin.axial_demand_kn) * 100.0
        if dev_pct > self.thresholds.reverse_check_tolerance_percent:
            issues.append(
                issue_from_flag(
                    "LOG.REVERSE_CHECK_DEVIATION",
                    f"Reverse axial-demand deviation {dev_pct:.2f}% exceeds threshold",
                    STANDARD_REFERENCES["dc_ratio"],
                )
            )
        layer = LayerResult(
            layer="layer4_reverse_validation",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={"reverse_axial_demand_kn": pu_rev, "axial_demand_deviation_percent": dev_pct},
        )
        return layer.details, layer

    def _response(
        self,
        calculation_type: str,
        sin: SteelInput,
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
            final["steel_grade"] = sin.steel_grade
            final["status"] = status_from_dc(final["dc_ratio"])
            final["inspection_interval_years"] = inspection_interval_years(final["status"])
            final["reinforcement_need"] = screen_reinforcement_need(final["dc_ratio"], final["corrosion_loss_percent"])
            final["connection_status"] = screen_connection_status(sin.connection_failure_detected, final["dc_ratio"])

        return {
            "calculation_summary": {
                "discipline": "steel",
                "calculation_type": calculation_type,
                "standards_applied": [
                    STANDARD_REFERENCES["compression"],
                    STANDARD_REFERENCES["dc_ratio"],
                    STANDARD_REFERENCES["serviceability"],
                    STANDARD_REFERENCES["corrosion"],
                ],
                "confidence": confidence,
                "execution_time_sec": round(perf_counter() - started, 6),
            },
            "input_data": {
                "member_type": sin.member_type,
                "steel_grade": sin.steel_grade,
                "section_label": sin.section_label,
                "length_m": sin.length_m,
                "k_factor": sin.k_factor,
                "radius_of_gyration_mm": sin.radius_of_gyration_mm,
                "yield_strength_mpa": sin.yield_strength_mpa,
                "elasticity_mpa": sin.elasticity_mpa,
                "gross_area_mm2": sin.gross_area_mm2,
                "corrosion_loss_percent": sin.corrosion_loss_percent,
                "axial_demand_kn": sin.axial_demand_kn,
                "moment_demand_knm": sin.moment_demand_knm,
                "deflection_mm": sin.deflection_mm,
                "span_mm": sin.span_mm,
                "connection_failure_detected": sin.connection_failure_detected,
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
                "discipline": "steel",
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
                    "description": "Steel input payload failed validation",
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
                "description": "Column compression strength",
                "formula_used": "AISC 360 Chapter E lambda_c -> Fcr -> phiPn",
                "standard_reference": STANDARD_REFERENCES["compression"],
                "result": {
                    "lambda_c": final.get("lambda_c"),
                    "fcr_mpa": final.get("fcr_mpa"),
                    "phi_pn_kn": final.get("phi_pn_kn"),
                },
            },
            {
                "step_number": 2,
                "description": "D/C and section loss",
                "formula_used": "D/C = Pu/(phiPn)",
                "standard_reference": STANDARD_REFERENCES["dc_ratio"],
                "result": {
                    "dc_ratio": final.get("dc_ratio"),
                    "corrosion_loss_percent": final.get("corrosion_loss_percent"),
                },
            },
            {
                "step_number": 3,
                "description": "Serviceability",
                "formula_used": "deflection <= L/240",
                "standard_reference": STANDARD_REFERENCES["serviceability"],
                "result": {"deflection_ratio": final.get("deflection_ratio")},
            },
        ]

    def _recommendations(self, final: Dict[str, float], flags: Dict[str, List[str]]) -> List[Dict[str, str]]:
        recs: List[Dict[str, str]] = []
        if "PHY.STRUCTURAL_DC_CRITICAL" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "remove_load_and_shore_immediately",
                    "timeline": "immediate",
                    "description": "D/C indicates critical overload",
                }
            )
        if "PHY.STEEL_CORROSION_SECTION_LOSS_HIGH" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "replace_or_reinforce_member",
                    "timeline": "immediate",
                    "description": "Section loss exceeds acceptable limit",
                }
            )
        if "PHY.STEEL_DEFLECTION_EXCEEDED" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "add_stiffening_or_support",
                    "timeline": "1month",
                    "description": "Deflection exceeds serviceability limit",
                }
            )
        if "PHY.CONNECTION_FAILURE_DETECTED" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "repair_connection",
                    "timeline": "immediate",
                    "description": "Connection failure reported",
                }
            )

        if not recs:
            recs.append(
                {
                    "priority": "low",
                    "action": "continue_monitoring",
                    "timeline": "nextyear",
                    "description": "No immediate steel structural issue detected",
                }
            )
        return recs
