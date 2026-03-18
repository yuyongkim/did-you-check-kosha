from __future__ import annotations


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def calculate_health_index(
    vibration_mm_per_s: float,
    vibration_limit_mm_per_s: float,
    nozzle_load_ratio: float,
    bearing_temperature_c: float,
) -> float:
    vibration_penalty = max(vibration_mm_per_s - vibration_limit_mm_per_s, 0.0) * 1.5
    nozzle_penalty = max(nozzle_load_ratio - 1.0, 0.0) * 3.0
    temp_penalty = max(bearing_temperature_c - 70.0, 0.0) * 0.1
    hi = 10.0 - vibration_penalty - nozzle_penalty - temp_penalty
    return clamp(hi, 0.0, 10.0)


def calculate_inspection_interval_years(health_index: float) -> float:
    if health_index >= 8.0:
        return 3.0
    if health_index >= 6.0:
        return 1.0
    if health_index >= 4.0:
        return 0.5
    return 0.1


def calculate_status(
    vibration_mm_per_s: float,
    vibration_limit_mm_per_s: float,
    nozzle_load_ratio: float,
) -> str:
    if vibration_mm_per_s > vibration_limit_mm_per_s or nozzle_load_ratio > 1.0:
        return "CRITICAL"
    return "NORMAL"


def relative_difference(a: float, b: float) -> float:
    base = max(abs(a), abs(b), 1e-12)
    return abs(a - b) / base


def screen_monitoring_escalation(
    health_index: float,
    vibration_mm_per_s: float,
    vibration_limit_mm_per_s: float,
    bearing_temperature_c: float,
) -> str:
    """Screening-level monitoring escalation recommendation."""
    vib_ratio = vibration_mm_per_s / max(vibration_limit_mm_per_s, 1e-9)
    if health_index < 3.0 or vib_ratio > 1.2 or bearing_temperature_c > 90.0:
        return "CONTINUOUS_ONLINE"
    if health_index < 5.0 or vib_ratio > 0.8 or bearing_temperature_c > 80.0:
        return "WEEKLY_ROUTE"
    if health_index < 7.0 or vib_ratio > 0.6:
        return "MONTHLY_ROUTE"
    return "QUARTERLY_ROUTE"


def screen_maintenance_urgency(health_index: float, nozzle_load_ratio: float) -> str:
    """Screening-level maintenance action urgency."""
    if health_index < 3.0 or nozzle_load_ratio > 1.2:
        return "IMMEDIATE_SHUTDOWN_REVIEW"
    if health_index < 5.0 or nozzle_load_ratio > 1.0:
        return "NEXT_AVAILABLE_WINDOW"
    if health_index < 7.0:
        return "PLANNED_TURNAROUND"
    return "ROUTINE"

