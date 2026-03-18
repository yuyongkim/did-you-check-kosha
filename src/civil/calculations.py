from __future__ import annotations

import math
from typing import Tuple


def calculate_a_mm(rebar_area_mm2: float, fy_mpa: float, fc_mpa: float, width_mm: float) -> float:
    den = 0.85 * max(fc_mpa, 1e-12) * max(width_mm, 1e-12)
    return (rebar_area_mm2 * fy_mpa) / den


def calculate_phi_mn_knm(
    rebar_area_mm2: float,
    fy_mpa: float,
    effective_depth_mm: float,
    a_mm: float,
    phi: float = 0.9,
) -> float:
    mn_n_mm = rebar_area_mm2 * fy_mpa * max(effective_depth_mm - a_mm / 2.0, 0.0)
    return phi * mn_n_mm / 1_000_000.0


def calculate_dc_ratio(demand_moment_knm: float, phi_mn_knm: float) -> float:
    if phi_mn_knm <= 0:
        return float("inf")
    return demand_moment_knm / phi_mn_knm


def classify_substantial_damage(
    *,
    lateral_capacity_loss_percent: float,
    affected_area_percent: float,
    vertical_capacity_loss_percent: float,
) -> Tuple[bool, str]:
    if lateral_capacity_loss_percent >= 33.0:
        return True, "TYPE1_LATERAL"
    if affected_area_percent >= 30.0 and vertical_capacity_loss_percent >= 20.0:
        return True, "TYPE2_VERTICAL"
    return False, "NONE"


def carbonation_depth_mm(carbonation_coeff_mm_sqrt_year: float, service_years: float) -> float:
    return max(carbonation_coeff_mm_sqrt_year, 0.0) * math.sqrt(max(service_years, 0.0))


def years_until_corrosion_init(
    *,
    carbonation_coeff_mm_sqrt_year: float,
    cover_thickness_mm: float,
    current_carbonation_depth_mm: float,
) -> float:
    k = max(carbonation_coeff_mm_sqrt_year, 1e-12)
    remaining_depth = cover_thickness_mm - current_carbonation_depth_mm
    if remaining_depth <= 0:
        return 0.0
    return (remaining_depth / k) ** 2


def status_from_checks(
    *,
    dc_ratio: float,
    substantial_damage: bool,
    corrosion_initiated: bool,
    crack_width_mm: float,
    spalling_area_percent: float,
) -> str:
    if substantial_damage or dc_ratio >= 1.2:
        return "CRITICAL"
    if corrosion_initiated or crack_width_mm > 0.4 or spalling_area_percent > 20.0 or dc_ratio >= 1.0:
        return "WARNING"
    return "ACCEPTABLE"


def inspection_interval_years(status: str) -> float:
    if status == "CRITICAL":
        return 0.1
    if status == "WARNING":
        return 0.5
    return 2.0


def reverse_demand_moment_knm(dc_ratio: float, phi_mn_knm: float) -> float:
    if not math.isfinite(dc_ratio):
        return float("inf")
    return dc_ratio * phi_mn_knm


def relative_difference(a: float, b: float) -> float:
    base = max(abs(a), abs(b), 1e-12)
    return abs(a - b) / base


def screen_repair_priority(
    status: str,
    dc_ratio: float,
    crack_width_mm: float,
    spalling_area_percent: float,
    foundation_settlement_mm: float,
) -> str:
    """Screening-level repair priority classification."""
    if status == "CRITICAL":
        return "PRIORITY_1_IMMEDIATE"
    urgent_count = sum([
        crack_width_mm > 0.4,
        spalling_area_percent > 20.0,
        foundation_settlement_mm > 25.0,
        dc_ratio >= 1.0,
    ])
    if urgent_count >= 2:
        return "PRIORITY_2_NEXT_SHUTDOWN"
    if urgent_count >= 1:
        return "PRIORITY_3_PLANNED_REPAIR"
    return "PRIORITY_4_ROUTINE_MAINTENANCE"


def screen_consequence_category(
    element_type: str,
    substantial_damage: bool,
    foundation_settlement_mm: float,
) -> str:
    """Screening consequence category based on element criticality and damage."""
    critical_elements = {"foundation", "pile_cap", "mat_foundation", "column"}
    is_critical = element_type in critical_elements
    if substantial_damage and is_critical:
        return "HIGH_CONSEQUENCE"
    if substantial_damage or (is_critical and foundation_settlement_mm > 25.0):
        return "MEDIUM_CONSEQUENCE"
    return "LOW_CONSEQUENCE"


# TODO: screen_anchor_distress - requires anchor bolt condition inputs not yet available
