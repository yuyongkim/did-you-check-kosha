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

    dc_vals = [c["dc_ratio"] for c in candidates]
    phi_vals = [c["phi_pn_kn"] for c in candidates]

    d_dc = dispersion(dc_vals)
    d_phi = dispersion(phi_vals)
    passed = d_dc < tolerance and d_phi < tolerance

    if not passed:
        issues.append(
            issue_from_flag(
                "LOG.NO_CONSENSUS_AFTER_TIEBREAKER",
                "Steel MAKER candidates diverged beyond tolerance",
                "MAKER consensus policy",
            )
        )

    selected = {
        "reduced_area_mm2": median_of([c["reduced_area_mm2"] for c in candidates]),
        "lambda_c": median_of([c["lambda_c"] for c in candidates]),
        "fcr_mpa": median_of([c["fcr_mpa"] for c in candidates]),
        "phi_pn_kn": median_of(phi_vals),
        "dc_ratio": median_of(dc_vals),
        "deflection_ratio": median_of([c["deflection_ratio"] for c in candidates]),
        "corrosion_loss_percent": median_of([c["corrosion_loss_percent"] for c in candidates]),
    }

    layer = LayerResult(
        layer="layer2_maker_consensus",
        passed=passed,
        issues=issues,
        details={
            "tolerance": tolerance,
            "dispersion_dc_ratio": d_dc,
            "dispersion_phi_pn": d_phi,
            "candidates": candidates,
            "selected": selected,
        },
    )
    return layer, selected
