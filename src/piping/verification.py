from __future__ import annotations

from typing import Any, Dict, List, Tuple

from src.piping.calculations import median_of, relative_difference
from src.shared.verification import (
    LayerResult,
    ValidationIssue,
    has_blocking_issue,
    issue_from_flag,
    split_flags,
)


def build_layer1_result(issues: List[ValidationIssue], details: Dict[str, Any]) -> LayerResult:
    blocking = has_blocking_issue(issues)
    return LayerResult(layer="layer1_input_validation", passed=not blocking, issues=issues, details=details)


def build_layer2_consensus(
    candidate_results: List[Dict[str, float]],
    tolerance: float,
) -> Tuple[LayerResult, Dict[str, float]]:
    issues: List[ValidationIssue] = []

    tmins = [x["t_min_mm"] for x in candidate_results]
    rls = [x["remaining_life_years"] for x in candidate_results]

    tmin_dispersion = max(relative_difference(tmins[i], tmins[j]) for i in range(3) for j in range(i + 1, 3))
    rl_dispersion = max(relative_difference(rls[i], rls[j]) for i in range(3) for j in range(i + 1, 3))

    passed = tmin_dispersion < tolerance and rl_dispersion < tolerance

    if not passed:
        issues.append(
            issue_from_flag(
                "LOG.NO_CONSENSUS_AFTER_TIEBREAKER",
                "MAKER agents disagreed above tolerance; tie-breaker median applied",
                "MAKER consensus policy",
            )
        )

    selected = {
        "t_min_mm": median_of(tmins),
        "cr_long_term_mm_per_year": median_of([x["cr_long_term_mm_per_year"] for x in candidate_results]),
        "cr_short_term_mm_per_year": median_of([x["cr_short_term_mm_per_year"] for x in candidate_results]),
        "cr_selected_mm_per_year": median_of([x["cr_selected_mm_per_year"] for x in candidate_results]),
        "remaining_life_years": median_of(rls),
        "inspection_interval_years": median_of([x["inspection_interval_years"] for x in candidate_results]),
    }

    layer = LayerResult(
        layer="layer2_maker_consensus",
        passed=passed,
        issues=issues,
        details={
            "tolerance": tolerance,
            "agent_candidates": candidate_results,
            "tmin_dispersion": tmin_dispersion,
            "rl_dispersion": rl_dispersion,
            "selected": selected,
        },
    )
    return layer, selected
