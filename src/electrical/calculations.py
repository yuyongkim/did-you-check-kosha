from __future__ import annotations

import math

from src.electrical.constants import HI_WEIGHTS


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def calculate_transformer_health_index(
    *,
    dga_score: float,
    oil_quality_score: float,
    insulation_score: float,
    load_factor_score: float,
) -> float:
    hi = (
        HI_WEIGHTS["dga"] * dga_score
        + HI_WEIGHTS["oil_quality"] * oil_quality_score
        + HI_WEIGHTS["insulation"] * insulation_score
        + HI_WEIGHTS["load_factor"] * load_factor_score
    )
    return round(clamp(hi, 0.0, 10.0), 6)


def calculate_arc_flash_energy_cal_cm2(
    *,
    bolted_fault_current_ka: float,
    clearing_time_sec: float,
    working_distance_mm: float,
    system_voltage_kv: float,
) -> float:
    cf = 1.5 if system_voltage_kv <= 1.0 else 1.0
    exponent = 1.473
    en = max(0.05, 0.03 * bolted_fault_current_ka + 0.20)
    energy = 4.184 * cf * en * (clearing_time_sec / 0.2) * ((610.0 / working_distance_mm) ** exponent)
    return round(max(energy, 0.0), 6)


def reverse_clearing_time_sec(
    *,
    arc_flash_energy_cal_cm2: float,
    bolted_fault_current_ka: float,
    working_distance_mm: float,
    system_voltage_kv: float,
) -> float | None:
    cf = 1.5 if system_voltage_kv <= 1.0 else 1.0
    exponent = 1.473
    en = max(0.05, 0.03 * bolted_fault_current_ka + 0.20)

    denom = 4.184 * cf * en * ((610.0 / working_distance_mm) ** exponent)
    if denom <= 0:
        return None

    t_sec = 0.2 * (arc_flash_energy_cal_cm2 / denom)
    return round(max(t_sec, 0.0), 6)


def determine_arc_ppe_category(arc_flash_energy_cal_cm2: float) -> str:
    e = arc_flash_energy_cal_cm2
    if e > 40.0:
        return "PROHIBITED"
    if e > 25.0:
        return "CAT4"
    if e > 8.0:
        return "CAT3"
    if e > 4.0:
        return "CAT2"
    if e > 1.2:
        return "CAT1"
    return "CAT0"


def calculate_inspection_interval_years(health_index: float, arc_flash_energy_cal_cm2: float) -> float:
    if health_index < 3.0 or arc_flash_energy_cal_cm2 > 40.0:
        return 0.25
    if health_index < 5.0 or arc_flash_energy_cal_cm2 > 25.0:
        return 0.5
    if health_index < 7.0 or arc_flash_energy_cal_cm2 > 8.0:
        return 1.0
    return 2.0


def calculate_status(
    *,
    health_index: float,
    arc_flash_energy_cal_cm2: float,
    voltage_drop_percent: float,
    fault_current_ka: float,
    breaker_interrupt_rating_ka: float,
) -> str:
    if health_index < 3.0 or arc_flash_energy_cal_cm2 > 40.0 or fault_current_ka > breaker_interrupt_rating_ka:
        return "CRITICAL"
    if health_index < 5.0 or arc_flash_energy_cal_cm2 > 25.0 or voltage_drop_percent > 5.0:
        return "WARNING"
    return "NORMAL"


def relative_difference(a: float, b: float) -> float:
    base = max(abs(a), abs(b), 1e-12)
    return abs(a - b) / base


def screen_breaker_coordination_margin(fault_current_ka: float, breaker_interrupt_rating_ka: float) -> float:
    """Screening coordination margin (ratio of breaker capacity to fault duty)."""
    if fault_current_ka <= 0:
        return float("inf")
    return breaker_interrupt_rating_ka / fault_current_ka


def screen_load_utilization(load_factor_score: float) -> str:
    """Screening load utilization category from load factor score (0-10 scale)."""
    # load_factor_score: higher = better condition, lower = more loaded
    if load_factor_score < 3.0:
        return "HEAVILY_LOADED"
    if load_factor_score < 5.0:
        return "MODERATELY_LOADED"
    return "LIGHTLY_LOADED"

