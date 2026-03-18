from __future__ import annotations

from dataclasses import dataclass


STANDARD_REFERENCES = {
    "compression": "AISC 360-16 Chapter E compression strength context [verify edition]",
    "dc_ratio": "AISC 360 strength interaction/D-C context [verify edition]",
    "serviceability": "AISC serviceability deflection context [verify edition]",
    "corrosion": "Steel section loss assessment context [verify edition]",
}

CONSENSUS_REL_TOLERANCE = 0.01


@dataclass(frozen=True)
class SteelThresholds:
    min_length_m: float = 0.5
    max_length_m: float = 30.0
    min_yield_strength_mpa: float = 150.0
    max_yield_strength_mpa: float = 700.0
    min_radius_gyration_mm: float = 10.0
    max_radius_gyration_mm: float = 300.0
    reverse_check_tolerance_percent: float = 5.0

