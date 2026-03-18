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

    t_vals = [c["t_required_shell_mm"] for c in candidates]
    rl_vals = [c["remaining_life_years"] for c in candidates]

    d_t = dispersion(t_vals)
    d_rl = dispersion(rl_vals)
    passed = d_t < tolerance and d_rl < tolerance

    if not passed:
        issues.append(
            issue_from_flag(
                "LOG.NO_CONSENSUS_AFTER_TIEBREAKER",
                "Vessel MAKER candidates diverged beyond tolerance",
                "MAKER consensus policy",
            )
        )

    selected = {
        "t_required_shell_mm": median_of(t_vals),
        "remaining_life_years": median_of(rl_vals),
        "inspection_interval_years": median_of([c["inspection_interval_years"] for c in candidates]),
        "corrosion_rate_selected_mm_per_year": median_of([c["corrosion_rate_selected_mm_per_year"] for c in candidates]),
    }

    layer = LayerResult(
        layer="layer2_maker_consensus",
        passed=passed,
        issues=issues,
        details={
            "tolerance": tolerance,
            "dispersion_t_required": d_t,
            "dispersion_rl": d_rl,
            "candidates": candidates,
            "selected": selected,
        },
    )
    return layer, selected
