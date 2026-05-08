from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Status = Literal["ok", "warning", "escalation"]


@dataclass
class ReverseCheckResult:
    passed: bool
    deviation_percent: float
    note: str
    status: Status = "ok"


def reverse_remaining_life_check(
    current_thickness_mm: float,
    corrosion_rate_mm_per_year: float,
    service_years: float,
    historical_initial_thickness_mm: float,
    warning_threshold_percent: float = 2.0,
    escalation_threshold_percent: float = 5.0,
    tolerance_percent: float | None = None,
) -> ReverseCheckResult:
    if tolerance_percent is not None:
        escalation_threshold_percent = tolerance_percent

    estimated_initial = current_thickness_mm + (corrosion_rate_mm_per_year * service_years)
    deviation = abs(estimated_initial - historical_initial_thickness_mm)

    if historical_initial_thickness_mm == 0:
        return ReverseCheckResult(False, 100.0, "historical initial thickness is zero", "escalation")

    deviation_percent = (deviation / historical_initial_thickness_mm) * 100.0
    if deviation_percent > escalation_threshold_percent:
        return ReverseCheckResult(False, deviation_percent, "exceeds escalation threshold", "escalation")
    if deviation_percent > warning_threshold_percent:
        return ReverseCheckResult(True, deviation_percent, "within escalation but warrants warning", "warning")
    return ReverseCheckResult(True, deviation_percent, "within tolerance", "ok")
