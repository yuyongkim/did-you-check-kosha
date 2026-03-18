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

    hi = [c["bearing_health_index"] for c in candidates]
    vib = [c["vibration_mm_per_s"] for c in candidates]

    d_hi = dispersion(hi)
    d_v = dispersion(vib)
    passed = d_hi < tolerance and d_v < tolerance

    if not passed:
        issues.append(
            issue_from_flag(
                "LOG.NO_CONSENSUS_AFTER_TIEBREAKER",
                "Rotating MAKER candidates diverged beyond tolerance",
                "MAKER consensus policy",
            )
        )

    selected = {
        "vibration_mm_per_s": median_of([c["vibration_mm_per_s"] for c in candidates]),
        "vibration_limit_mm_per_s": median_of([c["vibration_limit_mm_per_s"] for c in candidates]),
        "nozzle_load_ratio": median_of([c["nozzle_load_ratio"] for c in candidates]),
        "bearing_temperature_c": median_of([c["bearing_temperature_c"] for c in candidates]),
        "bearing_health_index": median_of(hi),
        "inspection_interval_years": median_of([c["inspection_interval_years"] for c in candidates]),
        "steam_pressure_bar": median_of([c["steam_pressure_bar"] for c in candidates]),
        "steam_temperature_c": median_of([c["steam_temperature_c"] for c in candidates]),
        "steam_quality_x": median_of([c["steam_quality_x"] for c in candidates]),
        "steam_specific_energy_drop_kj_per_kg": median_of(
            [c["steam_specific_energy_drop_kj_per_kg"] for c in candidates],
        ),
        "steam_superheat_margin_c": median_of([c["steam_superheat_margin_c"] for c in candidates]),
        "phase_change_risk_index": median_of([c["phase_change_risk_index"] for c in candidates]),
    }

    layer = LayerResult(
        layer="layer2_maker_consensus",
        passed=passed,
        issues=issues,
        details={
            "tolerance": tolerance,
            "dispersion_health_index": d_hi,
            "dispersion_vibration": d_v,
            "candidates": candidates,
            "selected": selected,
        },
    )
    return layer, selected
