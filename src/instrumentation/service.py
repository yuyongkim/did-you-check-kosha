from __future__ import annotations

from time import perf_counter
from typing import Any, Dict, List, Mapping

from src.instrumentation.calculations import (
    calculate_pfdavg,
    calculate_status,
    combined_uncertainty_pct,
    linear_regression,
    optimal_calibration_interval_days,
    predicted_drift_pct,
    relative_difference,
    reverse_failure_rate_from_pfdavg,
    screen_calibration_health,
    screen_proof_test_adequacy,
    sil_achieved_from_pfd,
    sil_target_limit,
)
from src.instrumentation.constants import (
    ARCHITECTURE_PFD_FACTOR,
    CONSENSUS_REL_TOLERANCE,
    INSTRUMENT_TYPE_DRIFT_FACTOR,
    STANDARD_REFERENCES,
    InstrumentationThresholds,
)
from src.instrumentation.models import InputPayloadError, InstrumentationInput, parse_instrumentation_input
from src.instrumentation.verification import (
    LayerResult,
    ValidationIssue,
    has_blocking_issue,
    issue_from_flag,
    maker_select,
    split_flags,
)


class InstrumentationVerificationService:
    def __init__(self, thresholds: InstrumentationThresholds | None = None) -> None:
        self.thresholds = thresholds or InstrumentationThresholds()

    def evaluate(self, payload: Mapping[str, Any], calculation_type: str = "instrumentation_integrity") -> Dict[str, Any]:
        started = perf_counter()
        layers: List[LayerResult] = []

        try:
            iin = parse_instrumentation_input(payload)
        except InputPayloadError as exc:
            issue = issue_from_flag("FMT.SCHEMA_VALIDATION_FAILED", str(exc), "Instrumentation input schema")
            layer = LayerResult(
                layer="layer1_input_validation",
                passed=False,
                issues=[issue],
                details={"payload_keys": sorted(payload.keys())},
            )
            return self._error_response(calculation_type, payload, [layer], started)

        layer1 = self._layer1(iin)
        layers.append(layer1)
        if has_blocking_issue(layer1.issues):
            return self._response(calculation_type, iin, layers, None, {}, started)

        candidates = [
            self._single_calc(iin, "a"),
            self._single_calc(iin, "b"),
            self._single_calc(iin, "c"),
        ]
        layer2, selected = maker_select(candidates, CONSENSUS_REL_TOLERANCE)
        layers.append(layer2)

        layer3 = self._layer3(iin, selected)
        layers.append(layer3)

        reverse_details, layer4 = self._layer4(iin, selected)
        layers.append(layer4)

        return self._response(calculation_type, iin, layers, selected, reverse_details, started)

    def _layer1(self, iin: InstrumentationInput) -> LayerResult:
        issues: List[ValidationIssue] = []
        t = self.thresholds

        if iin.sil_target < 1 or iin.sil_target > 4:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"sil_target out of range: {iin.sil_target}",
                    STANDARD_REFERENCES["sil_validation"],
                )
            )

        if iin.failure_rate_per_hour < t.min_failure_rate_per_hour or iin.failure_rate_per_hour > t.max_failure_rate_per_hour:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"failure_rate_per_hour out of range: {iin.failure_rate_per_hour}",
                    STANDARD_REFERENCES["sil_validation"],
                )
            )

        if iin.proof_test_interval_hours <= 0 or iin.proof_test_interval_hours > t.max_test_interval_hours:
            issues.append(
                issue_from_flag(
                    "STD.OUT_OF_SCOPE_APPLICATION",
                    f"proof_test_interval_hours out of range: {iin.proof_test_interval_hours}",
                    STANDARD_REFERENCES["sil_validation"],
                )
            )

        if iin.tolerance_pct <= 0:
            issues.append(
                issue_from_flag(
                    "DATA.MISSING_MANDATORY_FIELD",
                    f"tolerance_pct must be positive: {iin.tolerance_pct}",
                    STANDARD_REFERENCES["drift_analysis"],
                )
            )

        if iin.cv_rated <= 0 or iin.cv_required <= 0:
            issues.append(
                issue_from_flag(
                    "DATA.MISSING_MANDATORY_FIELD",
                    "cv_required and cv_rated must be positive",
                    STANDARD_REFERENCES["valve_sizing"],
                )
            )

        return LayerResult(
            layer="layer1_input_validation",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "sil_target": iin.sil_target,
                "failure_rate_per_hour": iin.failure_rate_per_hour,
                "proof_test_interval_hours": iin.proof_test_interval_hours,
                "calibration_history_count": len(iin.calibration_history),
            },
        )

    def _single_calc(self, iin: InstrumentationInput, variant: str) -> Dict[str, float]:
        history = iin.calibration_history
        if variant == "b":
            history = [
                type(p)(days_since_ref=p.days_since_ref, error_pct=p.error_pct * 1.001)
                for p in iin.calibration_history
            ]
        elif variant == "c":
            history = [
                type(p)(days_since_ref=p.days_since_ref, error_pct=p.error_pct * 0.999)
                for p in iin.calibration_history
            ]

        slope, intercept, r2 = linear_regression(history)
        architecture_factor = ARCHITECTURE_PFD_FACTOR.get(iin.voting_architecture, 1.0)
        instrument_drift_factor = INSTRUMENT_TYPE_DRIFT_FACTOR.get(iin.instrument_type, 1.0)
        slope_adjusted = slope * instrument_drift_factor
        drift_pred = predicted_drift_pct(
            slope_pct_per_day=slope_adjusted,
            intercept_pct=intercept,
            interval_days=iin.calibration_interval_days,
        )
        pfd = calculate_pfdavg(
            failure_rate_per_hour=iin.failure_rate_per_hour,
            proof_test_interval_hours=iin.proof_test_interval_hours,
            mttr_hours=iin.mttr_hours,
        )
        pfd *= architecture_factor
        sil_ach = sil_achieved_from_pfd(pfd)
        unc = combined_uncertainty_pct(iin.uncertainty_components_pct)
        opt_interval = optimal_calibration_interval_days(
            slope_pct_per_day=slope_adjusted,
            intercept_pct=intercept,
            tolerance_pct=iin.tolerance_pct,
        )

        return {
            "drift_rate_pct_per_day": slope_adjusted,
            "drift_intercept_pct": intercept,
            "drift_r_squared": r2,
            "predicted_drift_pct": drift_pred,
            "pfdavg": pfd,
            "sil_target": float(iin.sil_target),
            "sil_achieved": float(sil_ach),
            "combined_uncertainty_pct": unc,
            "calibration_interval_optimal_days": opt_interval,
            "inspection_interval_days": min(opt_interval, iin.calibration_interval_days),
            "cv_required": iin.cv_required,
            "cv_rated": iin.cv_rated,
            "cv_margin_ratio": iin.cv_required / max(iin.cv_rated, 1e-12),
        }

    def _layer3(self, iin: InstrumentationInput, selected: Dict[str, float]) -> LayerResult:
        _ = iin
        issues: List[ValidationIssue] = []

        if selected["pfdavg"] > sil_target_limit(int(selected["sil_target"])):
            issues.append(
                issue_from_flag(
                    "PHY.SIL_TARGET_NOT_MET",
                    "Calculated PFDavg does not satisfy SIL target",
                    STANDARD_REFERENCES["sil_validation"],
                )
            )

        if selected["predicted_drift_pct"] > iin.tolerance_pct:
            issues.append(
                issue_from_flag(
                    "PHY.DRIFT_RATE_EXCEEDED",
                    "Predicted drift exceeds allowed tolerance",
                    STANDARD_REFERENCES["drift_analysis"],
                )
            )

        if selected["drift_r_squared"] < 0.3:
            issues.append(
                issue_from_flag(
                    "LOG.DRIFT_MODEL_LOW_CONFIDENCE",
                    "Drift regression confidence too low for optimization",
                    STANDARD_REFERENCES["drift_analysis"],
                )
            )

        if iin.sensor_mtbf_years < 5.0:
            issues.append(
                issue_from_flag(
                    "PHY.SENSOR_MTBF_LOW",
                    "Sensor MTBF below 5-year threshold",
                    STANDARD_REFERENCES["instrument_id"],
                )
            )

        if selected["cv_required"] > selected["cv_rated"] * 0.9:
            issues.append(
                issue_from_flag(
                    "PHY.CONTROL_VALVE_CAPACITY_LOW",
                    "Control valve required Cv exceeds 90% of rated Cv",
                    STANDARD_REFERENCES["valve_sizing"],
                )
            )

        return LayerResult(
            layer="layer3_physics_standards",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "pfdavg": selected["pfdavg"],
                "sil_target": selected["sil_target"],
                "sil_achieved": selected["sil_achieved"],
                "predicted_drift_pct": selected["predicted_drift_pct"],
                "tolerance_pct": iin.tolerance_pct,
                "drift_r_squared": selected["drift_r_squared"],
                "cv_margin_ratio": selected["cv_margin_ratio"],
            },
        )

    def _layer4(self, iin: InstrumentationInput, selected: Dict[str, float]) -> tuple[Dict[str, Any], LayerResult]:
        issues: List[ValidationIssue] = []

        failure_rate_rev = reverse_failure_rate_from_pfdavg(
            pfdavg=selected["pfdavg"],
            proof_test_interval_hours=iin.proof_test_interval_hours,
            mttr_hours=iin.mttr_hours,
        )

        failure_rate_dev_pct = None
        if failure_rate_rev is not None:
            failure_rate_dev_pct = relative_difference(failure_rate_rev, iin.failure_rate_per_hour) * 100.0
            if failure_rate_dev_pct > self.thresholds.reverse_check_tolerance_percent:
                issues.append(
                    issue_from_flag(
                        "LOG.REVERSE_CHECK_DEVIATION",
                        f"Reverse failure-rate deviation {failure_rate_dev_pct:.2f}% exceeds threshold",
                        STANDARD_REFERENCES["sil_validation"],
                    )
                )

        layer = LayerResult(
            layer="layer4_reverse_validation",
            passed=not has_blocking_issue(issues),
            issues=issues,
            details={
                "reverse_failure_rate_per_hour": failure_rate_rev,
                "failure_rate_deviation_percent": failure_rate_dev_pct,
            },
        )
        return layer.details, layer

    def _response(
        self,
        calculation_type: str,
        iin: InstrumentationInput,
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
            final["instrument_type"] = iin.instrument_type
            final["voting_architecture"] = iin.voting_architecture
            final["sil_target"] = int(round(final["sil_target"]))
            final["sil_achieved"] = int(round(final["sil_achieved"]))
            final["status"] = calculate_status(
                pfdavg=final["pfdavg"],
                sil_target=final["sil_target"],
                predicted_drift=final["predicted_drift_pct"],
                tolerance_pct=iin.tolerance_pct,
                cv_required=final["cv_required"],
                cv_rated=final["cv_rated"],
            )
            final["proof_test_adequacy"] = screen_proof_test_adequacy(
                final["pfdavg"], final["sil_target"]
            )
            final["calibration_health"] = screen_calibration_health(
                final["predicted_drift_pct"], iin.tolerance_pct
            )

        return {
            "calculation_summary": {
                "discipline": "instrumentation",
                "calculation_type": calculation_type,
                "standards_applied": [
                    STANDARD_REFERENCES["sil_validation"],
                    STANDARD_REFERENCES["drift_analysis"],
                    STANDARD_REFERENCES["instrument_id"],
                    STANDARD_REFERENCES["valve_sizing"],
                ],
                "confidence": confidence,
                "execution_time_sec": round(perf_counter() - started, 6),
            },
            "input_data": {
                "instrument_type": iin.instrument_type,
                "voting_architecture": iin.voting_architecture,
                "sil_target": iin.sil_target,
                "failure_rate_per_hour": iin.failure_rate_per_hour,
                "proof_test_interval_hours": iin.proof_test_interval_hours,
                "mttr_hours": iin.mttr_hours,
                "calibration_interval_days": iin.calibration_interval_days,
                "calibration_history": [
                    {"days_since_ref": p.days_since_ref, "error_pct": p.error_pct}
                    for p in iin.calibration_history
                ],
                "tolerance_pct": iin.tolerance_pct,
                "sensor_mtbf_years": iin.sensor_mtbf_years,
                "cv_required": iin.cv_required,
                "cv_rated": iin.cv_rated,
                "uncertainty_components_pct": iin.uncertainty_components_pct,
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
                "discipline": "instrumentation",
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
                    "description": "Instrumentation input payload failed validation",
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
                "description": "Drift regression and calibration optimization",
                "formula_used": "Drift = a*t + b",
                "standard_reference": STANDARD_REFERENCES["drift_analysis"],
                "result": {
                    "drift_rate_pct_per_day": final.get("drift_rate_pct_per_day"),
                    "drift_r_squared": final.get("drift_r_squared"),
                    "calibration_interval_optimal_days": final.get("calibration_interval_optimal_days"),
                },
            },
            {
                "step_number": 2,
                "description": "SIL validation",
                "formula_used": "PFDavg = lambda*(TI/2 + MTTR/2)",
                "standard_reference": STANDARD_REFERENCES["sil_validation"],
                "result": {
                    "pfdavg": final.get("pfdavg"),
                    "sil_target": final.get("sil_target"),
                    "sil_achieved": final.get("sil_achieved"),
                },
            },
            {
                "step_number": 3,
                "description": "Uncertainty and valve capacity checks",
                "formula_used": "uc = sqrt(sum(u_i^2)); Cv_required <= 0.9*Cv_rated",
                "standard_reference": STANDARD_REFERENCES["valve_sizing"],
                "result": {
                    "combined_uncertainty_pct": final.get("combined_uncertainty_pct"),
                    "cv_margin_ratio": final.get("cv_margin_ratio"),
                },
            },
        ]

    def _recommendations(self, final: Dict[str, float], flags: Dict[str, List[str]]) -> List[Dict[str, str]]:
        recs: List[Dict[str, str]] = []

        if "PHY.SIL_TARGET_NOT_MET" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "reconfigure_sis_architecture",
                    "timeline": "immediate",
                    "description": "SIL target is not satisfied by current design",
                }
            )
        if "PHY.DRIFT_RATE_EXCEEDED" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "shorten_calibration_interval",
                    "timeline": "immediate",
                    "description": "Predicted drift exceeds tolerance at current interval",
                }
            )
        if "PHY.CONTROL_VALVE_CAPACITY_LOW" in flags["red_flags"]:
            recs.append(
                {
                    "priority": "high",
                    "action": "upgrade_control_valve",
                    "timeline": "1month",
                    "description": "Control valve rated capacity margin is insufficient",
                }
            )
        if "LOG.DRIFT_MODEL_LOW_CONFIDENCE" in flags["warnings"]:
            recs.append(
                {
                    "priority": "medium",
                    "action": "collect_more_calibration_points",
                    "timeline": "1month",
                    "description": "Drift model confidence is low; increase data quality",
                }
            )

        if not recs:
            recs.append(
                {
                    "priority": "low",
                    "action": "continue_monitoring",
                    "timeline": "nextyear",
                    "description": "No immediate instrumentation integrity issue detected",
                }
            )
        return recs
