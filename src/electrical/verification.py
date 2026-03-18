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

    hi_vals = [c["transformer_health_index"] for c in candidates]
    arc_vals = [c["arc_flash_energy_cal_cm2"] for c in candidates]

    d_hi = dispersion(hi_vals)
    d_arc = dispersion(arc_vals)
    passed = d_hi < tolerance and d_arc < tolerance

    if not passed:
        issues.append(
            issue_from_flag(
                "LOG.NO_CONSENSUS_AFTER_TIEBREAKER",
                "Electrical MAKER candidates diverged beyond tolerance",
                "MAKER consensus policy",
            )
        )

    selected = {
        "transformer_health_index": median_of(hi_vals),
        "arc_flash_energy_cal_cm2": median_of(arc_vals),
        "voltage_drop_percent": median_of([c["voltage_drop_percent"] for c in candidates]),
        "fault_current_ka": median_of([c["fault_current_ka"] for c in candidates]),
        "breaker_interrupt_rating_ka": median_of([c["breaker_interrupt_rating_ka"] for c in candidates]),
        "thd_voltage_percent": median_of([c["thd_voltage_percent"] for c in candidates]),
        "motor_current_thd_percent": median_of([c["motor_current_thd_percent"] for c in candidates]),
        "power_factor": median_of([c["power_factor"] for c in candidates]),
        "inspection_interval_years": median_of([c["inspection_interval_years"] for c in candidates]),
    }

    layer = LayerResult(
        layer="layer2_maker_consensus",
        passed=passed,
        issues=issues,
        details={
            "tolerance": tolerance,
            "dispersion_health_index": d_hi,
            "dispersion_arc_flash": d_arc,
            "candidates": candidates,
            "selected": selected,
        },
    )
    return layer, selected
