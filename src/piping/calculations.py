from __future__ import annotations

from datetime import datetime
from statistics import median
from typing import List, Sequence, Tuple

from src.piping.models import ThicknessRecord


def years_between(date_a: str, date_b: str) -> float:
    da = datetime.fromisoformat(date_a)
    db = datetime.fromisoformat(date_b)
    days = (db - da).days
    return max(days / 365.25, 1e-9)


def calculate_t_min_mm(
    design_pressure_mpa: float,
    od_mm: float,
    allowable_stress_mpa: float,
    weld_efficiency: float,
    y_coefficient: float,
    corrosion_allowance_mm: float,
) -> float:
    denominator = 2.0 * (allowable_stress_mpa * weld_efficiency + design_pressure_mpa * y_coefficient)
    if denominator <= 0:
        return float("inf")
    required_without_ca = (design_pressure_mpa * od_mm) / denominator
    return required_without_ca + corrosion_allowance_mm


def calculate_corrosion_rates_mm_per_year(history: Sequence[ThicknessRecord]) -> Tuple[float, float, float, float, float]:
    if len(history) < 2:
        return 0.0, 0.0, 0.0, 0.0, 0.0

    first = history[0]
    prev = history[-2]
    last = history[-1]

    total_years = years_between(first.date, last.date)
    recent_years = years_between(prev.date, last.date)

    cr_long = (first.thickness_mm - last.thickness_mm) / total_years
    cr_short = (prev.thickness_mm - last.thickness_mm) / recent_years
    cr_selected = max(cr_long, cr_short)
    return cr_long, cr_short, cr_selected, total_years, recent_years


def calculate_remaining_life_years(current_thickness_mm: float, t_min_mm: float, corrosion_rate_mm_per_year: float) -> float:
    if corrosion_rate_mm_per_year <= 0:
        return float("inf")
    return (current_thickness_mm - t_min_mm) / corrosion_rate_mm_per_year


def calculate_inspection_interval_years(remaining_life_years: float, corrosion_rate_mm_per_year: float) -> float:
    if remaining_life_years <= 0:
        return 0.0

    interval = min(10.0, 0.5 * remaining_life_years)

    if corrosion_rate_mm_per_year > 2.0:
        interval = min(interval, 1.0)
    elif corrosion_rate_mm_per_year > 1.0:
        interval = min(interval, 2.0)
    elif corrosion_rate_mm_per_year > 0.5:
        interval = min(interval, 3.0)

    return max(0.5, round(interval, 3))


def reverse_initial_thickness_mm(current_thickness_mm: float, corrosion_rate_mm_per_year: float, service_years: float) -> float:
    return current_thickness_mm + corrosion_rate_mm_per_year * service_years


def reverse_design_pressure_mpa(
    t_min_mm: float,
    corrosion_allowance_mm: float,
    od_mm: float,
    allowable_stress_mpa: float,
    weld_efficiency: float,
    y_coefficient: float,
) -> float | None:
    t_required = t_min_mm - corrosion_allowance_mm
    if t_required <= 0:
        return None

    denominator = od_mm - 2.0 * t_required * y_coefficient
    if denominator <= 0:
        return None

    return (2.0 * t_required * allowable_stress_mpa * weld_efficiency) / denominator


def relative_difference(a: float, b: float) -> float:
    base = max(abs(a), abs(b), 1e-12)
    return abs(a - b) / base


def median_of(values: List[float]) -> float:
    return float(median(values))


def screen_hoop_stress_mpa(design_pressure_mpa: float, od_mm: float, current_thickness_mm: float) -> float:
    """Barlow hoop-stress screening estimate (screening-level, not detailed FEA)."""
    if current_thickness_mm <= 0:
        return float("inf")
    return (design_pressure_mpa * od_mm) / (2.0 * current_thickness_mm)


def screen_hoop_stress_ratio(hoop_stress_mpa: float, allowable_stress_mpa: float) -> float:
    """Screening-level hoop stress utilization ratio."""
    if allowable_stress_mpa <= 0:
        return float("inf")
    return hoop_stress_mpa / allowable_stress_mpa


def screen_hydrotest_pressure_mpa(design_pressure_mpa: float, test_factor: float = 1.5) -> float:
    """Screening hydrotest pressure recommendation (ASME B31.3 standard factor)."""
    return design_pressure_mpa * test_factor


def screen_hydrotest_hoop_stress_mpa(hydrotest_pressure_mpa: float, od_mm: float, current_thickness_mm: float) -> float:
    """Hoop stress at hydrotest pressure (screening-level)."""
    if current_thickness_mm <= 0:
        return float("inf")
    return (hydrotest_pressure_mpa * od_mm) / (2.0 * current_thickness_mm)


def screen_hydrotest_margin_ratio(hydrotest_hoop_mpa: float, yield_stress_mpa: float) -> float:
    """Screening ratio of hydrotest hoop to estimated yield (should be < 0.9 for margin)."""
    if yield_stress_mpa <= 0:
        return float("inf")
    return hydrotest_hoop_mpa / yield_stress_mpa


# TODO: screen_water_hammer_risk - requires flow velocity and pipe length inputs not yet available
# TODO: screen_insulation_surface_temperature - requires insulation thickness, ambient temp inputs not yet available
# TODO: screen_pressure_drop - requires flow rate, pipe length, roughness inputs not yet available

