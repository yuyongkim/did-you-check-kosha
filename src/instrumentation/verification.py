from __future__ import annotations

from typing import Dict, List

from src.shared.verification import (
    LayerResult,
    ValidationIssue,
    dispersion,
    has_blocking_issue,
    issue_from_flag,
    median_of,
    split_flags,
)


def maker_select(candidates: List[Dict[str, float]], tolerance: float) -> tuple[LayerResult, Dict[str, float]]:
    issues: List[ValidationIssue] = []

    pfd_vals = [c["pfdavg"] for c in candidates]
    drift_vals = [c["predicted_drift_pct"] for c in candidates]

    d_pfd = dispersion(pfd_vals)
    d_drift = dispersion(drift_vals)
    passed = d_pfd < tolerance and d_drift < tolerance

    if not passed:
        issues.append(
            issue_from_flag(
                "LOG.NO_CONSENSUS_AFTER_TIEBREAKER",
                "Instrumentation MAKER candidates diverged beyond tolerance",
                "MAKER consensus policy",
            )
        )

    selected = {
        "drift_rate_pct_per_day": median_of([c["drift_rate_pct_per_day"] for c in candidates]),
        "drift_intercept_pct": median_of([c["drift_intercept_pct"] for c in candidates]),
        "drift_r_squared": median_of([c["drift_r_squared"] for c in candidates]),
        "predicted_drift_pct": median_of(drift_vals),
        "pfdavg": median_of(pfd_vals),
        "sil_target": median_of([c["sil_target"] for c in candidates]),
        "sil_achieved": median_of([c["sil_achieved"] for c in candidates]),
        "combined_uncertainty_pct": median_of([c["combined_uncertainty_pct"] for c in candidates]),
        "calibration_interval_optimal_days": median_of([c["calibration_interval_optimal_days"] for c in candidates]),
        "inspection_interval_days": median_of([c["inspection_interval_days"] for c in candidates]),
        "cv_required": median_of([c["cv_required"] for c in candidates]),
        "cv_rated": median_of([c["cv_rated"] for c in candidates]),
        "cv_margin_ratio": median_of([c["cv_margin_ratio"] for c in candidates]),
    }

    layer = LayerResult(
        layer="layer2_maker_consensus",
        passed=passed,
        issues=issues,
        details={
            "tolerance": tolerance,
            "dispersion_pfdavg": d_pfd,
            "dispersion_predicted_drift": d_drift,
            "candidates": candidates,
            "selected": selected,
        },
    )
    return layer, selected
