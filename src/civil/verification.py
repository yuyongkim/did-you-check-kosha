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
    phi_vals = [c["phi_mn_knm"] for c in candidates]

    d_dc = dispersion(dc_vals)
    d_phi = dispersion(phi_vals)
    passed = d_dc < tolerance and d_phi < tolerance

    if not passed:
        issues.append(
            issue_from_flag(
                "LOG.NO_CONSENSUS_AFTER_TIEBREAKER",
                "Civil MAKER candidates diverged beyond tolerance",
                "MAKER consensus policy",
            )
        )

    selected = {
        "a_mm": median_of([c["a_mm"] for c in candidates]),
        "phi_mn_knm": median_of(phi_vals),
        "dc_ratio": median_of(dc_vals),
        "carbonation_depth_mm": median_of([c["carbonation_depth_mm"] for c in candidates]),
    }

    layer = LayerResult(
        layer="layer2_maker_consensus",
        passed=passed,
        issues=issues,
        details={
            "tolerance": tolerance,
            "dispersion_dc_ratio": d_dc,
            "dispersion_phi_mn": d_phi,
            "candidates": candidates,
            "selected": selected,
        },
    )
    return layer, selected
