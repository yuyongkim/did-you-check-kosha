from __future__ import annotations

from time import perf_counter
from typing import Any, Dict, List, Mapping

from src.civil.calculations import (
    calculate_a_mm,
    calculate_dc_ratio,
    calculate_phi_mn_knm,
    carbonation_depth_mm,
    classify_substantial_damage,
    inspection_interval_years,
    relative_difference,
    reverse_demand_moment_knm,
    screen_consequence_category,
    screen_repair_priority,
    status_from_checks,
    years_until_corrosion_init,
)
from src.civil.constants import CONSENSUS_REL_TOLERANCE, ENVIRONMENT_EXPOSURE_FACTOR, STANDARD_REFERENCES, CivilThresholds
from src.civil.models import CivilInput, InputPayloadError, parse_civil_input
from src.civil.verification import (
    LayerResult,
    ValidationIssue,
    has_blocking_issue,
    issue_from_flag,
    maker_select,
    split_flags,
)


class CivilVerificationService:
    def __init__(self, thresholds: CivilThresholds | None = None) -> None:
        self.thresholds = thresholds or CivilThresholds()

    def evaluate(self, payload: Mapping[str, Any], calculation_type: str = "civil_integrity") -> Dict[str, Any]:
        started = perf_counter()
        layers: List[LayerResult] = []

        try:
            cin = parse_civil_input(payload)
        except InputPayloadError as exc:
            issue = issue_from_flag("FMT.SCHEMA_VALIDATION_FAILED", str(exc), "Civil input schema")
            layer = LayerResult(
                layer="layer1_input_validation",
                passed=False,
                issues=[issue],
                details={"payload_keys": sorted(payload.keys())},
            )
            return self._error_response(calculation_type, payload, [layer], started)

        layer1 = self._layer1(cin)
        layers.append(layer1)
        if has_blocking_issue(layer1.issues):
            return self._response(calculation_type, cin, layers, None, {}, started)

        candidates = [
            self._single_calc(cin, "a"),
            self._single_calc(cin, "b"),
            self._single_calc(cin, "c"),
        ]
        layer2, selected = maker_select(candidates, CONSENSUS_REL_TOLERANCE)
        layers.append(layer2)

        layer3 = self._layer3(cin, selected)
        layers.append(layer3)

        reverse_details, layer4 = self._layer4(cin, selected)
        layers.append(layer4)

        return self._response(calculation_type, cin, layers, selected, reverse_details, started)

    def _layer1(self, cin: CivilInput) -> LayerResult:
        issues: List[ValidationIssue] = []
        t = self.thresholds

        if cin.fc_mpa < t.min_fc_mpa or cin.fc_mpa > t.max_fc_mpa:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"fc_mpa out of range: {cin.fc_mpa}",
                    STANDARD_REFERENCES["flexure_strength"],
                )
            )
        if cin.fy_mpa < t.min_fy_mpa or cin.fy_mpa > t.max_fy_mpa:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"fy_mpa out of range: {cin.fy_mpa}",
                    STANDARD_REFERENCES["flexure_strength"],
                )
            )
        if cin.service_years < t.min_service_years or cin.service_years > t.max_service_years:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"service_years out of range: {cin.service_years}",
                    STANDARD_REFERENCES["carbonation"],
                )
            )
        if cin.cover_thickness_mm < t.min_cover_mm or cin.cover_thickness_mm > t.max_cover_mm:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"cover_thickness_mm out of range: {cin.cover_thickness_mm}",
                    STANDARD_REFERENCES["carbonation"],
                )
            )
        if cin.width_mm <= 0 or cin.effective_depth_mm <= 0 or cin.rebar_area_mm2 <= 0:
            issues.append(
                issue_from_flag(
                    "DATA.MISSING_MANDATORY_FIELD",
                    "width_mm, effective_depth_mm, and rebar_area_mm2 must be > 0",
                    STANDARD_REFERENCES["flexure_strength"],
                )
            )
        if cin.demand_moment_knm < 0:
            issues.append(
                issue_from_flag(
                    "DATA.MISSING_MANDATORY_FIELD",
                    "demand_moment_knm must be >= 0",
                    STANDARD_REFERENCES["flexure_strength"],
                )
            )
        for name, value in {
            "lateral_capacity_loss_percent": cin.lateral_capacity_loss_percent,
            "affected_area_percent": cin.affected_area_percent,
            "vertical_capacity_loss_percent": cin.vertical_capacity_loss_percent,
            "spalling_area_percent": cin.spalling_area_percent,
        }.items():
            if value < 0 or value > 100:
                issues.append(
                    issue_from_flag(
                        "STD.OUT_OF_SCOPE_APPLICATION",
                        f"{name} out of range: {value}",
                        STANDARD_REFERENCES["damage_classification"],
                    )
                )

        return LayerResult(
            layer="layer1_input_validation",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "element_type": cin.element_type,
                "environment_exposure": cin.environment_exposure,
                "fc_mpa": cin.fc_mpa,
                "fy_mpa": cin.fy_mpa,
                "service_years": cin.service_years,
            },
        )

    def _single_calc(self, cin: CivilInput, variant: str) -> Dict[str, float]:
        fc = cin.fc_mpa
        fy = cin.fy_mpa
        demand = cin.demand_moment_knm
        exposure_factor = ENVIRONMENT_EXPOSURE_FACTOR.get(cin.environment_exposure, 1.0)
        carb_k = cin.carbonation_coeff_mm_sqrt_year * exposure_factor

        if variant == "b":
            fc = fc * 1.001
        elif variant == "c":
            demand = demand * 0.999
            carb_k = carb_k * 1.001

        a_mm = calculate_a_mm(cin.rebar_area_mm2, fy, fc, cin.width_mm)
        phi_mn_knm = calculate_phi_mn_knm(cin.rebar_area_mm2, fy, cin.effective_depth_mm, a_mm)
        dc_ratio = calculate_dc_ratio(demand, phi_mn_knm)
        xc = carbonation_depth_mm(carb_k, cin.service_years)

        return {
            "a_mm": a_mm,
            "phi_mn_knm": phi_mn_knm,
            "dc_ratio": dc_ratio,
            "carbonation_depth_mm": xc,
            "exposure_factor": exposure_factor,
        }

    def _layer3(self, cin: CivilInput, selected: Dict[str, float]) -> LayerResult:
        issues: List[ValidationIssue] = []
        t = self.thresholds

        substantial_damage, mode = classify_substantial_damage(
            lateral_capacity_loss_percent=cin.lateral_capacity_loss_percent,
            affected_area_percent=cin.affected_area_percent,
            vertical_capacity_loss_percent=cin.vertical_capacity_loss_percent,
        )

        corrosion_initiated = selected["carbonation_depth_mm"] >= cin.cover_thickness_mm

        if selected["dc_ratio"] >= 1.2:
            issues.append(
                issue_from_flag(
                    "PHY.CIVIL_FLEXURE_OVERSTRESS",
                    "Civil member flexural D/C ratio exceeds 1.2",
                    STANDARD_REFERENCES["flexure_strength"],
                )
            )

        if substantial_damage:
            issues.append(
                issue_from_flag(
                    "PHY.CIVIL_SUBSTANTIAL_DAMAGE",
                    f"Substantial damage condition met ({mode})",
                    STANDARD_REFERENCES["damage_classification"],
                )
            )

        if corrosion_initiated:
            issues.append(
                issue_from_flag(
                    "PHY.CIVIL_CARBONATION_CORROSION_INITIATED",
                    "Carbonation front reached reinforcement cover depth",
                    STANDARD_REFERENCES["carbonation"],
                )
            )

        if cin.crack_width_mm > t.crack_width_limit_mm:
            issues.append(
                issue_from_flag(
                    "PHY.CIVIL_CRACK_WIDTH_EXCEEDED",
                    f"Crack width exceeds limit ({cin.crack_width_mm} mm)",
                    STANDARD_REFERENCES["durability"],
                )
            )

        if cin.spalling_area_percent > t.spalling_area_limit_percent:
            issues.append(
                issue_from_flag(
                    "PHY.CIVIL_SPALLING_SEVERE",
                    f"Spalling area exceeds {t.spalling_area_limit_percent}%",
                    STANDARD_REFERENCES["durability"],
                )
            )

        if cin.foundation_settlement_mm > t.foundation_settlement_limit_mm:
            issues.append(
                issue_from_flag(
                    "PHY.CIVIL_FOUNDATION_SETTLEMENT_HIGH",
                    f"Foundation settlement exceeds {t.foundation_settlement_limit_mm} mm",
                    STANDARD_REFERENCES["damage_classification"],
                )
            )

        return LayerResult(
            layer="layer3_physics_standards",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "dc_ratio": selected["dc_ratio"],
                "substantial_damage": substantial_damage,
                "damage_mode": mode,
                "carbonation_depth_mm": selected["carbonation_depth_mm"],
                "cover_thickness_mm": cin.cover_thickness_mm,
            },
        )

    def _layer4(self, cin: CivilInput, selected: Dict[str, float]) -> tuple[Dict[str, Any], LayerResult]:
        issues: List[ValidationIssue] = []

        moment_rev = reverse_demand_moment_knm(selected["dc_ratio"], selected["phi_mn_knm"])
        dev_pct = relative_difference(moment_rev, cin.demand_moment_knm) * 100.0
        if dev_pct > self.thresholds.reverse_check_tolerance_percent:
            issues.append(
                issue_from_flag(
                    "LOG.REVERSE_CHECK_DEVIATION",
                    f"Reverse demand-moment deviation {dev_pct:.2f}% exceeds threshold",
                    STANDARD_REFERENCES["flexure_strength"],
                )
            )

        layer = LayerResult(
            layer="layer4_reverse_validation",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={"reverse_demand_moment_knm": moment_rev, "demand_moment_deviation_percent": dev_pct},
        )
        return layer.details, layer

    def _response(
        self,
        calculation_type: str,
        cin: CivilInput,
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
            substantial_damage, damage_mode = classify_substantial_damage(
                lateral_capacity_loss_percent=cin.lateral_capacity_loss_percent,
                affected_area_percent=cin.affected_area_percent,
                vertical_capacity_loss_percent=cin.vertical_capacity_loss_percent,
            )
            corrosion_initiated = final["carbonation_depth_mm"] >= cin.cover_thickness_mm
            final["substantial_damage"] = substantial_damage
            final["damage_mode"] = damage_mode
            final["corrosion_initiated"] = corrosion_initiated
            final["years_to_corrosion_init"] = years_until_corrosion_init(
                carbonation_coeff_mm_sqrt_year=cin.carbonation_coeff_mm_sqrt_year,
                cover_thickness_mm=cin.cover_thickness_mm,
                current_carbonation_depth_mm=final["carbonation_depth_mm"],
            )
            final["crack_width_mm"] = cin.crack_width_mm
            final["spalling_area_percent"] = cin.spalling_area_percent
            final["foundation_settlement_mm"] = cin.foundation_settlement_mm
            final["environment_exposure"] = cin.environment_exposure
            final["status"] = status_from_checks(
                dc_ratio=final["dc_ratio"],
                substantial_damage=substantial_damage,
                corrosion_initiated=corrosion_initiated,
                crack_width_mm=cin.crack_width_mm,
                spalling_area_percent=cin.spalling_area_percent,
            )
            final["inspection_interval_years"] = inspection_interval_years(final["status"])
            final["repair_priority"] = screen_repair_priority(
                final["status"], final["dc_ratio"], cin.crack_width_mm,
                cin.spalling_area_percent, cin.foundation_settlement_mm,
            )
            final["consequence_category"] = screen_consequence_category(
                cin.element_type, substantial_damage, cin.foundation_settlement_mm,
            )

        return {
            "calculation_summary": {
                "discipline": "civil",
                "calculation_type": calculation_type,
                "standards_applied": [
                    STANDARD_REFERENCES["damage_classification"],
                    STANDARD_REFERENCES["flexure_strength"],
                    STANDARD_REFERENCES["carbonation"],
                    STANDARD_REFERENCES["durability"],
                ],
                "confidence": confidence,
                "execution_time_sec": round(perf_counter() - started, 6),
            },
            "input_data": {
                "element_type": cin.element_type,
                "environment_exposure": cin.environment_exposure,
                "fc_mpa": cin.fc_mpa,
                "fy_mpa": cin.fy_mpa,
                "width_mm": cin.width_mm,
                "effective_depth_mm": cin.effective_depth_mm,
                "rebar_area_mm2": cin.rebar_area_mm2,
                "demand_moment_knm": cin.demand_moment_knm,
                "lateral_capacity_loss_percent": cin.lateral_capacity_loss_percent,
                "affected_area_percent": cin.affected_area_percent,
                "vertical_capacity_loss_percent": cin.vertical_capacity_loss_percent,
                "carbonation_coeff_mm_sqrt_year": cin.carbonation_coeff_mm_sqrt_year,
                "service_years": cin.service_years,
                "cover_thickness_mm": cin.cover_thickness_mm,
                "crack_width_mm": cin.crack_width_mm,
                "spalling_area_percent": cin.spalling_area_percent,
                "foundation_settlement_mm": cin.foundation_settlement_mm,
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
                "discipline": "civil",
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
                    "description": "Civil input payload failed validation",
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
                "description": "Flexural strength and D/C ratio",
                "formula_used": "a = As*fy/(0.85*fc*b); phiMn = phi*As*fy*(d-a/2); D/C = Mu/phiMn",
                "standard_reference": STANDARD_REFERENCES["flexure_strength"],
                "result": {
                    "a_mm": final.get("a_mm"),
                    "phi_mn_knm": final.get("phi_mn_knm"),
                    "dc_ratio": final.get("dc_ratio"),
                },
            },
            {
                "step_number": 2,
                "description": "Substantial damage screening",
                "formula_used": "Type1: lateral_loss>=33%; Type2: area>=30% and vertical_loss>=20%",
                "standard_reference": STANDARD_REFERENCES["damage_classification"],
                "result": {
                    "substantial_damage": final.get("substantial_damage"),
                    "damage_mode": final.get("damage_mode"),
                },
            },
            {
                "step_number": 3,
                "description": "Carbonation and durability checks",
                "formula_used": "Xc = k*sqrt(t)",
                "standard_reference": STANDARD_REFERENCES["carbonation"],
                "result": {
                    "carbonation_depth_mm": final.get("carbonation_depth_mm"),
                    "corrosion_initiated": final.get("corrosion_initiated"),
                    "years_to_corrosion_init": final.get("years_to_corrosion_init"),
                },
            },
        ]

    def _recommendations(self, final: Dict[str, float], flags: Dict[str, List[str]]) -> List[Dict[str, str]]:
        recs: List[Dict[str, str]] = []

        if "PHY.CIVIL_SUBSTANTIAL_DAMAGE" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "initiate_structural_retrofit_or_shutdown",
                    "timeline": "immediate",
                    "description": "ACI 562 substantial damage threshold exceeded",
                }
            )
        if "PHY.CIVIL_CARBONATION_CORROSION_INITIATED" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "repair_cover_and_protect_rebar",
                    "timeline": "immediate",
                    "description": "Carbonation front reached reinforcement depth",
                }
            )
        if "PHY.CIVIL_CRACK_WIDTH_EXCEEDED" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "seal_and_reassess_cracks",
                    "timeline": "1month",
                    "description": "Crack width exceeds durability criterion",
                }
            )
        if "PHY.CIVIL_SPALLING_SEVERE" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "remove_loose_concrete_and_patch_repair",
                    "timeline": "1month",
                    "description": "Spalling area exceeds threshold",
                }
            )
        if "PHY.CIVIL_FOUNDATION_SETTLEMENT_HIGH" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "perform_foundation_underpinning_study",
                    "timeline": "immediate",
                    "description": "Foundation settlement exceeds allowable limit",
                }
            )

        if not recs:
            recs.append(
                {
                    "priority": "low",
                    "action": "continue_monitoring",
                    "timeline": "nextyear",
                    "description": "No immediate civil integrity issue detected",
                }
            )
        return recs
