from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any, Dict, List, Mapping, Tuple

from src.piping.calculations import (
    calculate_corrosion_rates_mm_per_year,
    calculate_inspection_interval_years,
    calculate_remaining_life_years,
    calculate_t_min_mm,
    relative_difference,
    reverse_design_pressure_mpa,
    reverse_initial_thickness_mm,
    screen_hoop_stress_mpa,
    screen_hoop_stress_ratio,
    screen_hydrotest_pressure_mpa,
)
from src.piping.constants import CONSENSUS_REL_TOLERANCE, PipingThresholds, STANDARD_REFERENCES
from src.piping.constants import FLUID_CORROSION_FACTOR, SERVICE_CORROSION_FACTOR
from src.piping.models import InputPayloadError, PipingInput, parse_piping_input
from src.piping.standards import (
    get_allowable_stress_mpa,
    get_chloride_limit_ppm,
    get_material_group,
    get_temperature_window_c,
    get_weld_efficiency,
    get_y_coefficient,
    supported_material,
)
from src.piping.verification import (
    LayerResult,
    ValidationIssue,
    build_layer1_result,
    build_layer2_consensus,
    issue_from_flag,
    split_flags,
)


@dataclass
class AgentCalcContext:
    allowable_stress_mpa: float
    weld_efficiency: float
    y_coefficient: float


class PipingVerificationService:
    """Full piping calculation and 4-layer verification service."""

    def __init__(self, thresholds: PipingThresholds | None = None) -> None:
        self.thresholds = thresholds or PipingThresholds()

    def evaluate(self, payload: Mapping[str, Any], calculation_type: str = "remaining_life") -> Dict[str, Any]:
        started = perf_counter()

        layer_results: List[LayerResult] = []
        all_issues: List[ValidationIssue] = []

        try:
            piping_input = parse_piping_input(payload)
        except InputPayloadError as exc:
            issue = issue_from_flag(
                "FMT.SCHEMA_VALIDATION_FAILED",
                str(exc),
                "Input schema contract",
            )
            layer = build_layer1_result([issue], details={"payload_keys": sorted(payload.keys())})
            return self._build_error_response(calculation_type, payload, [layer], perf_counter() - started)

        layer1 = self._run_layer1_input_validation(piping_input)
        layer_results.append(layer1)
        all_issues.extend(layer1.issues)

        if self._has_blocking_issue(layer1.issues):
            return self._build_response(
                calculation_type=calculation_type,
                piping_input=piping_input,
                layer_results=layer_results,
                core_result=None,
                reverse_details={},
                started=started,
            )

        context, lookup_refs, lookup_issues = self._lookup_standard_context(piping_input)
        all_issues.extend(lookup_issues)
        if lookup_issues:
            layer_results.append(
                LayerResult(
                    layer="layer1_standard_context",
                    passed=not self._has_blocking_issue(lookup_issues),
                    issues=lookup_issues,
                    details={"references": lookup_refs},
                )
            )

        if self._has_blocking_issue(lookup_issues):
            return self._build_response(
                calculation_type=calculation_type,
                piping_input=piping_input,
                layer_results=layer_results,
                core_result=None,
                reverse_details={},
                started=started,
            )

        agent_candidates = self._run_maker_candidates(piping_input, context)
        layer2, selected = build_layer2_consensus(agent_candidates, tolerance=CONSENSUS_REL_TOLERANCE)
        layer_results.append(layer2)
        all_issues.extend(layer2.issues)

        layer3 = self._run_layer3_physics_and_standards(piping_input, selected)
        layer_results.append(layer3)
        all_issues.extend(layer3.issues)

        reverse_details, layer4 = self._run_layer4_reverse_checks(piping_input, selected, context)
        layer_results.append(layer4)
        all_issues.extend(layer4.issues)

        return self._build_response(
            calculation_type=calculation_type,
            piping_input=piping_input,
            layer_results=layer_results,
            core_result=selected,
            reverse_details=reverse_details,
            started=started,
            context=context,
        )

    def _run_layer1_input_validation(self, piping_input: PipingInput) -> LayerResult:
        issues: List[ValidationIssue] = []
        t = self.thresholds

        if not supported_material(piping_input.material):
            issues.append(
                issue_from_flag(
                    "STD.UNAPPROVED_MATERIAL",
                    f"Unsupported material for allowable stress lookup: {piping_input.material}",
                    STANDARD_REFERENCES["allowable_stress"],
                )
            )

        if piping_input.design_pressure_mpa <= t.min_pressure_mpa or piping_input.design_pressure_mpa >= t.max_pressure_mpa:
            issues.append(
                issue_from_flag(
                    "DATA.MISSING_MANDATORY_FIELD",
                    f"design_pressure_mpa out of range: {piping_input.design_pressure_mpa}",
                    "Input boundary policy",
                )
            )

        if piping_input.design_temperature_c <= t.min_temperature_c or piping_input.design_temperature_c >= t.max_temperature_c:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"design_temperature_c out of range: {piping_input.design_temperature_c}",
                    "Input boundary policy",
                )
            )

        if piping_input.od_mm <= 0:
            issues.append(
                issue_from_flag(
                    "PHY.NEGATIVE_THICKNESS",
                    f"od_mm must be > 0, got {piping_input.od_mm}",
                    "Physical sanity",
                )
            )

        if piping_input.corrosion_allowance_mm < 0:
            issues.append(
                issue_from_flag(
                    "PHY.NEGATIVE_THICKNESS",
                    f"corrosion_allowance_mm cannot be negative, got {piping_input.corrosion_allowance_mm}",
                    "Physical sanity",
                )
            )

        if len(piping_input.thickness_history) < 2:
            issues.append(
                issue_from_flag(
                    "DATA.INVALID_THICKNESS_HISTORY",
                    "thickness_history must contain at least two records",
                    STANDARD_REFERENCES["corrosion_rate"],
                )
            )

        for idx, record in enumerate(piping_input.thickness_history):
            if record.thickness_mm <= 0:
                issues.append(
                    issue_from_flag(
                        "PHY.NEGATIVE_THICKNESS",
                        f"thickness_history[{idx}] is non-positive: {record.thickness_mm}",
                        "Physical sanity",
                    )
                )

        return build_layer1_result(
            issues,
            details={
                "material": piping_input.material,
                "pressure_mpa": piping_input.design_pressure_mpa,
                "temperature_c": piping_input.design_temperature_c,
                "history_count": len(piping_input.thickness_history),
            },
        )

    def _lookup_standard_context(
        self,
        piping_input: PipingInput,
    ) -> Tuple[AgentCalcContext, Dict[str, str], List[ValidationIssue]]:
        issues: List[ValidationIssue] = []
        refs: Dict[str, str] = {}

        try:
            allowable_stress, ref_s = get_allowable_stress_mpa(
                material=piping_input.material,
                temperature_c=piping_input.design_temperature_c,
            )
            refs["allowable_stress"] = ref_s
        except KeyError:
            issues.append(
                issue_from_flag(
                    "STD.UNAPPROVED_MATERIAL",
                    f"allowable stress lookup failed for {piping_input.material}",
                    STANDARD_REFERENCES["allowable_stress"],
                )
            )
            allowable_stress = 0.0

        weld_efficiency, ref_e = get_weld_efficiency(piping_input.weld_type)
        y_coeff, ref_y = get_y_coefficient(piping_input.material, piping_input.design_temperature_c)
        refs["weld_efficiency"] = ref_e
        refs["y_coefficient"] = ref_y

        return (
            AgentCalcContext(
                allowable_stress_mpa=allowable_stress,
                weld_efficiency=weld_efficiency,
                y_coefficient=y_coeff,
            ),
            refs,
            issues,
        )

    def _run_single_agent_calc(self, piping_input: PipingInput, context: AgentCalcContext, variant: str) -> Dict[str, float]:
        t_min = calculate_t_min_mm(
            design_pressure_mpa=piping_input.design_pressure_mpa,
            od_mm=piping_input.od_mm,
            allowable_stress_mpa=context.allowable_stress_mpa,
            weld_efficiency=context.weld_efficiency,
            y_coefficient=context.y_coefficient,
            corrosion_allowance_mm=piping_input.corrosion_allowance_mm,
        )

        cr_long, cr_short, cr_selected, _, _ = calculate_corrosion_rates_mm_per_year(piping_input.thickness_history)
        service_factor = SERVICE_CORROSION_FACTOR.get(piping_input.service_type, 1.0)
        fluid_factor = FLUID_CORROSION_FACTOR.get(piping_input.fluid_type, 1.0)
        coating_factor = 0.85 if piping_input.has_internal_coating else 1.0

        cr_long *= service_factor * fluid_factor * coating_factor
        cr_short *= service_factor * fluid_factor * coating_factor
        cr_selected *= service_factor * fluid_factor * coating_factor

        if variant == "agent_b":
            cr_selected = cr_long if cr_long >= cr_short else cr_short
        elif variant == "agent_c":
            cr_selected = round(max(cr_long, cr_short), 6)

        rl = calculate_remaining_life_years(
            current_thickness_mm=piping_input.current_thickness_mm,
            t_min_mm=t_min,
            corrosion_rate_mm_per_year=cr_selected,
        )

        interval = calculate_inspection_interval_years(rl, cr_selected)

        return {
            "t_min_mm": t_min,
            "cr_long_term_mm_per_year": cr_long,
            "cr_short_term_mm_per_year": cr_short,
            "cr_selected_mm_per_year": cr_selected,
            "service_factor": service_factor,
            "fluid_factor": fluid_factor,
            "coating_factor": coating_factor,
            "remaining_life_years": rl,
            "inspection_interval_years": interval,
        }

    def _run_maker_candidates(self, piping_input: PipingInput, context: AgentCalcContext) -> List[Dict[str, float]]:
        return [
            self._run_single_agent_calc(piping_input, context, "agent_a"),
            self._run_single_agent_calc(piping_input, context, "agent_b"),
            self._run_single_agent_calc(piping_input, context, "agent_c"),
        ]

    def _run_layer3_physics_and_standards(self, piping_input: PipingInput, core: Dict[str, float]) -> LayerResult:
        issues: List[ValidationIssue] = []

        cr_selected = core["cr_selected_mm_per_year"]
        t_min = core["t_min_mm"]
        rl = core["remaining_life_years"]
        current = piping_input.current_thickness_mm

        if cr_selected < 0 and not piping_input.has_internal_coating:
            issues.append(
                issue_from_flag(
                    "PHY.UNREALISTIC_CORROSION_RATE",
                    "Negative corrosion rate without coating indicates measurement inconsistency",
                    STANDARD_REFERENCES["corrosion_rate"],
                )
            )

        if current < t_min:
            issues.append(
                issue_from_flag(
                    "PHY.CURRENT_THICKNESS_BELOW_MINIMUM",
                    "Current thickness is below minimum required thickness",
                    STANDARD_REFERENCES["thickness_formula"],
                )
            )

        temp_window, ref_limit = get_temperature_window_c(piping_input.material, piping_input.temperature_profile)
        material_group = get_material_group(piping_input.material)
        if temp_window is not None:
            soft_limit, hard_limit = temp_window
        else:
            soft_limit, hard_limit = (None, None)

        if hard_limit is not None and piping_input.design_temperature_c > hard_limit:
            issues.append(
                issue_from_flag(
                    "PHY.TEMPERATURE_LIMIT_EXCEEDED",
                    (
                        f"Design temperature {piping_input.design_temperature_c}C exceeds hard limit "
                        f"{hard_limit}C for profile={piping_input.temperature_profile}, material_group={material_group}"
                    ),
                    ref_limit,
                )
            )
        elif soft_limit is not None and piping_input.design_temperature_c > soft_limit:
            issues.append(
                issue_from_flag(
                    "STD.TEMPERATURE_OVERRIDE_REVIEW_REQUIRED",
                    (
                        f"Design temperature {piping_input.design_temperature_c}C exceeds conservative limit "
                        f"{soft_limit}C but is within managed envelope {hard_limit}C "
                        f"(profile={piping_input.temperature_profile})"
                    ),
                    ref_limit,
                )
            )

        if rl > self.thresholds.max_reasonable_rl_years:
            issues.append(
                issue_from_flag(
                    "PHY.UNREALISTIC_REMAINING_LIFE",
                    f"Remaining life {rl:.2f} years exceeds reasonability threshold",
                    STANDARD_REFERENCES["inspection_interval"],
                )
            )

        if piping_input.chloride_ppm is not None:
            chloride_limit, chloride_ref = get_chloride_limit_ppm(piping_input.material)
            if chloride_limit is not None and piping_input.chloride_ppm > chloride_limit:
                issues.append(
                    issue_from_flag(
                        "STD.OUT_OF_SCOPE_APPLICATION",
                        f"Hydrotest chloride {piping_input.chloride_ppm} ppm exceeds limit {chloride_limit} ppm",
                        chloride_ref,
                    )
                )

        has_blocking = self._has_blocking_issue(issues)
        return LayerResult(
            layer="layer3_physics_standards",
            passed=not has_blocking,
            issues=issues,
            details={
                "t_min_mm": t_min,
                "current_thickness_mm": current,
                "remaining_life_years": rl,
                "corrosion_rate_selected": cr_selected,
                "temperature_profile": piping_input.temperature_profile,
                "temperature_soft_limit_c": soft_limit,
                "temperature_hard_limit_c": hard_limit,
            },
        )

    def _run_layer4_reverse_checks(
        self,
        piping_input: PipingInput,
        core: Dict[str, float],
        context: AgentCalcContext,
    ) -> Tuple[Dict[str, Any], LayerResult]:
        issues: List[ValidationIssue] = []

        first = piping_input.thickness_history[0]
        last = piping_input.thickness_history[-1]
        years = max((last.as_datetime() - first.as_datetime()).days / 365.25, 1e-9)

        initial_est = reverse_initial_thickness_mm(
            current_thickness_mm=piping_input.current_thickness_mm,
            corrosion_rate_mm_per_year=core["cr_selected_mm_per_year"],
            service_years=years,
        )
        initial_actual = first.thickness_mm
        initial_dev_pct = relative_difference(initial_est, initial_actual) * 100.0

        if initial_dev_pct > self.thresholds.reverse_check_tolerance_percent:
            issues.append(
                issue_from_flag(
                    "LOG.REVERSE_CHECK_DEVIATION",
                    f"Reverse initial-thickness deviation {initial_dev_pct:.2f}% exceeds tolerance",
                    "Reverse check policy",
                )
            )

        pressure_est = reverse_design_pressure_mpa(
            t_min_mm=core["t_min_mm"],
            corrosion_allowance_mm=piping_input.corrosion_allowance_mm,
            od_mm=piping_input.od_mm,
            allowable_stress_mpa=context.allowable_stress_mpa,
            weld_efficiency=context.weld_efficiency,
            y_coefficient=context.y_coefficient,
        )

        pressure_dev_pct = None
        if pressure_est is not None:
            pressure_dev_pct = relative_difference(pressure_est, piping_input.design_pressure_mpa) * 100.0
            if pressure_dev_pct > self.thresholds.reverse_check_tolerance_percent:
                issues.append(
                    issue_from_flag(
                        "LOG.REVERSE_CHECK_DEVIATION",
                        f"Reverse pressure deviation {pressure_dev_pct:.2f}% exceeds tolerance",
                        STANDARD_REFERENCES["thickness_formula"],
                    )
                )

        layer = LayerResult(
            layer="layer4_reverse_validation",
            passed=not self._has_blocking_issue(issues),
            issues=issues,
            details={
                "initial_thickness_estimated_mm": initial_est,
                "initial_thickness_actual_mm": initial_actual,
                "initial_thickness_deviation_percent": initial_dev_pct,
                "pressure_reversed_mpa": pressure_est,
                "pressure_deviation_percent": pressure_dev_pct,
            },
        )

        return layer.details, layer

    def _build_response(
        self,
        calculation_type: str,
        piping_input: PipingInput,
        layer_results: List[LayerResult],
        core_result: Dict[str, float] | None,
        reverse_details: Dict[str, Any],
        started: float,
        context: AgentCalcContext | None = None,
    ) -> Dict[str, Any]:
        all_issues = [issue for layer in layer_results for issue in layer.issues]
        flags = split_flags(all_issues)

        final_results: Dict[str, Any] = dict(core_result or {})
        temp_window, _ = get_temperature_window_c(piping_input.material, piping_input.temperature_profile)
        material_group = get_material_group(piping_input.material)
        soft_limit = temp_window[0] if temp_window else None
        hard_limit = temp_window[1] if temp_window else None
        if core_result is not None:
            if hard_limit is not None and piping_input.design_temperature_c > hard_limit:
                temperature_mode = "exceeded_hard_limit"
            elif soft_limit is not None and piping_input.design_temperature_c > soft_limit:
                temperature_mode = "override_review_required"
            else:
                temperature_mode = "within_conservative_limit"

            final_results.update(
                {
                    "material": piping_input.material,
                    "material_group": material_group,
                    "temperature_profile": piping_input.temperature_profile,
                    "temperature_soft_limit_c": soft_limit,
                    "temperature_hard_limit_c": hard_limit,
                    "temperature_limit_mode": temperature_mode,
                }
            )

            # Screening-level stress and hydrotest outputs
            hoop = screen_hoop_stress_mpa(piping_input.design_pressure_mpa, piping_input.od_mm, piping_input.current_thickness_mm)
            final_results["hoop_stress_screening_mpa"] = round(hoop, 4)
            if context is not None and context.allowable_stress_mpa > 0:
                final_results["hoop_stress_ratio"] = round(screen_hoop_stress_ratio(hoop, context.allowable_stress_mpa), 4)
            else:
                final_results["hoop_stress_ratio"] = 0.0
            final_results["hydrotest_pressure_mpa"] = round(screen_hydrotest_pressure_mpa(piping_input.design_pressure_mpa), 4)

        recommendations = self._build_recommendations(final_results, flags)

        confidence = "high"
        if flags["red_flags"]:
            confidence = "low"
        elif flags["warnings"]:
            confidence = "medium"

        standards_applied = [
            STANDARD_REFERENCES["allowable_stress"],
            STANDARD_REFERENCES["thickness_formula"],
            STANDARD_REFERENCES["corrosion_rate"],
            STANDARD_REFERENCES["inspection_interval"],
        ]

        return {
            "calculation_summary": {
                "discipline": "piping",
                "calculation_type": calculation_type,
                "standards_applied": standards_applied,
                "confidence": confidence,
                "execution_time_sec": round(perf_counter() - started, 6),
            },
            "input_data": {
                "material": piping_input.material,
                "nps": piping_input.nps,
                "od_mm": piping_input.od_mm,
                "design_pressure_mpa": piping_input.design_pressure_mpa,
                "design_temperature_c": piping_input.design_temperature_c,
                "thickness_history": [
                    {"date": t.date, "thickness_mm": t.thickness_mm}
                    for t in piping_input.thickness_history
                ],
                "corrosion_allowance_mm": piping_input.corrosion_allowance_mm,
                "weld_type": piping_input.weld_type,
                "service_type": piping_input.service_type,
                "fluid_type": piping_input.fluid_type,
                "has_internal_coating": piping_input.has_internal_coating,
                "chloride_ppm": piping_input.chloride_ppm,
                "temperature_profile": piping_input.temperature_profile,
            },
            "calculation_steps": self._build_calculation_steps(final_results),
            "layer_results": [layer.to_dict() for layer in layer_results],
            "final_results": final_results,
            "reverse_validation": reverse_details,
            "recommendations": recommendations,
            "flags": flags,
        }

    def _build_error_response(
        self,
        calculation_type: str,
        payload: Mapping[str, Any],
        layer_results: List[LayerResult],
        execution_time: float,
    ) -> Dict[str, Any]:
        all_issues = [issue for layer in layer_results for issue in layer.issues]
        flags = split_flags(all_issues)

        return {
            "calculation_summary": {
                "discipline": "piping",
                "calculation_type": calculation_type,
                "standards_applied": [],
                "confidence": "low",
                "execution_time_sec": round(execution_time, 6),
            },
            "input_data": dict(payload),
            "calculation_steps": [],
            "layer_results": [layer.to_dict() for layer in layer_results],
            "final_results": {},
            "reverse_validation": {},
            "recommendations": [
                {
                    "priority": "high",
                    "action": "fix_input_data",
                    "timeline": "immediate",
                    "description": "Input payload failed schema/range validation",
                }
            ],
            "flags": flags,
        }

    def _build_calculation_steps(self, final_results: Dict[str, float]) -> List[Dict[str, Any]]:
        if not final_results:
            return []

        return [
            {
                "step_number": 1,
                "description": "Minimum required thickness",
                "formula_used": "t_min = (P*D)/(2*(S*E + P*Y)) + CA",
                "standard_reference": STANDARD_REFERENCES["thickness_formula"],
                "result": {"value": final_results.get("t_min_mm"), "unit": "mm"},
            },
            {
                "step_number": 2,
                "description": "Corrosion rates and selected corrosion rate",
                "formula_used": "CR_selected = max(CR_long_term, CR_short_term)",
                "standard_reference": STANDARD_REFERENCES["corrosion_rate"],
                "result": {
                    "cr_long_term_mm_per_year": final_results.get("cr_long_term_mm_per_year"),
                    "cr_short_term_mm_per_year": final_results.get("cr_short_term_mm_per_year"),
                    "cr_selected_mm_per_year": final_results.get("cr_selected_mm_per_year"),
                },
            },
            {
                "step_number": 3,
                "description": "Remaining life",
                "formula_used": "RL = (t_current - t_min) / CR_selected",
                "standard_reference": STANDARD_REFERENCES["corrosion_rate"],
                "result": {"value": final_results.get("remaining_life_years"), "unit": "years"},
            },
            {
                "step_number": 4,
                "description": "Inspection interval",
                "formula_used": "API 570 interval policy function",
                "standard_reference": STANDARD_REFERENCES["inspection_interval"],
                "result": {"value": final_results.get("inspection_interval_years"), "unit": "years"},
            },
        ]

    def _build_recommendations(self, final_results: Dict[str, float], flags: Dict[str, List[str]]) -> List[Dict[str, str]]:
        recs: List[Dict[str, str]] = []

        if "PHY.CURRENT_THICKNESS_BELOW_MINIMUM" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "replace",
                    "timeline": "immediate",
                    "description": "Current thickness is below minimum required thickness",
                }
            )

        rl = final_results.get("remaining_life_years")
        if isinstance(rl, (int, float)):
            if rl < 2:
                recs.append(
                    {
                        "priority": "high",
                        "action": "inspect",
                        "timeline": "immediate",
                        "description": "Remaining life below 2 years",
                    }
                )
            elif rl < 5:
                recs.append(
                    {
                        "priority": "medium",
                        "action": "monitor",
                        "timeline": "1month",
                        "description": "Remaining life below 5 years",
                    }
                )

        if "STD.OUT_OF_SCOPE_APPLICATION" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "review_standard_applicability",
                    "timeline": "immediate",
                    "description": "Operating condition exceeds standard/material applicability",
                }
            )

        if "STD.TEMPERATURE_OVERRIDE_REVIEW_REQUIRED" in flags["warnings"]:
            recs.append(
                {
                    "priority": "medium",
                    "action": "attach_engineering_justification",
                    "timeline": "1month",
                    "description": "Temperature is above conservative code limit. Attach managed-operation basis and increase monitoring.",
                }
            )

        if not recs:
            recs.append(
                {
                    "priority": "low",
                    "action": "continue_monitoring",
                    "timeline": "nextyear",
                    "description": "No critical issues detected in current evaluation",
                }
            )

        return recs

    @staticmethod
    def _has_blocking_issue(issues: List[ValidationIssue]) -> bool:
        return any(issue.severity in {"critical", "high"} for issue in issues)

