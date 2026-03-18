from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReverseCheckResult:
    passed: bool
    deviation_percent: float
    note: str


def reverse_remaining_life_check(
    current_thickness_mm: float,
    corrosion_rate_mm_per_year: float,
    service_years: float,
    historical_initial_thickness_mm: float,
    tolerance_percent: float = 5.0,
) -> ReverseCheckResult:
    estimated_initial = current_thickness_mm + (corrosion_rate_mm_per_year * service_years)
    deviation = abs(estimated_initial - historical_initial_thickness_mm)

    if historical_initial_thickness_mm == 0:
        return ReverseCheckResult(False, 100.0, "historical initial thickness is zero")

    deviation_percent = (deviation / historical_initial_thickness_mm) * 100.0
    passed = deviation_percent <= tolerance_percent
    note = "within tolerance" if passed else "exceeds tolerance"
    return ReverseCheckResult(passed, deviation_percent, note)
