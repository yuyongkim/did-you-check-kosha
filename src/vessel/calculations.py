from __future__ import annotations


def calculate_required_shell_thickness_mm(
    design_pressure_mpa: float,
    inside_radius_mm: float,
    allowable_stress_mpa: float,
    joint_efficiency: float,
    corrosion_allowance_mm: float,
) -> float:
    denominator = allowable_stress_mpa * joint_efficiency - 0.6 * design_pressure_mpa
    if denominator <= 0:
        return float("inf")
    t_required = (design_pressure_mpa * inside_radius_mm) / denominator
    return t_required + corrosion_allowance_mm


def calculate_remaining_life_years(
    current_thickness_mm: float,
    required_thickness_mm: float,
    corrosion_rate_mm_per_year: float,
) -> float:
    if corrosion_rate_mm_per_year <= 0:
        return float("inf")
    return (current_thickness_mm - required_thickness_mm) / corrosion_rate_mm_per_year


def calculate_inspection_interval_years(remaining_life_years: float) -> float:
    if remaining_life_years <= 0:
        return 0.0
    return max(0.1, min(10.0, round(0.5 * remaining_life_years, 3)))


def reverse_design_pressure_mpa(
    required_thickness_mm: float,
    corrosion_allowance_mm: float,
    inside_radius_mm: float,
    allowable_stress_mpa: float,
    joint_efficiency: float,
) -> float | None:
    t = required_thickness_mm - corrosion_allowance_mm
    if t <= 0:
        return None
    denominator = inside_radius_mm + 0.6 * t
    if denominator <= 0:
        return None
    return (t * allowable_stress_mpa * joint_efficiency) / denominator


def relative_difference(a: float, b: float) -> float:
    base = max(abs(a), abs(b), 1e-12)
    return abs(a - b) / base


def screen_ffs_level(
    current_thickness_mm: float,
    required_thickness_mm: float,
    corrosion_rate_mm_per_year: float,
    remaining_life_years: float,
) -> str:
    """Screening-level FFS classification (API 579 Level 1 analogy, not a substitute)."""
    margin = current_thickness_mm - required_thickness_mm
    if margin < 0:
        return "LEVEL3_DETAILED_ASSESSMENT_REQUIRED"
    if remaining_life_years < 2.0 or margin < 0.5:
        return "LEVEL2_ENGINEERING_REVIEW"
    if corrosion_rate_mm_per_year > 0.5 or remaining_life_years < 5.0:
        return "LEVEL1_MONITOR_CLOSELY"
    return "LEVEL0_FIT_FOR_SERVICE"


def screen_repair_scope(ffs_level: str, corrosion_rate_mm_per_year: float) -> str:
    """Screening-level repair scope indicator."""
    if ffs_level == "LEVEL3_DETAILED_ASSESSMENT_REQUIRED":
        return "REPAIR_OR_REPLACE"
    if ffs_level == "LEVEL2_ENGINEERING_REVIEW":
        return "EVALUATE_REPAIR_FEASIBILITY"
    if corrosion_rate_mm_per_year > 0.5:
        return "CONSIDER_WELD_OVERLAY_OR_COATING"
    return "NO_REPAIR_ACTION"

