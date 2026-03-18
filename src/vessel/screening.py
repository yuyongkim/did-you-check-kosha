from __future__ import annotations

from math import sqrt


def calculate_external_pressure_allowable_screen_mpa(
    *,
    shell_thickness_mm: float,
    diameter_mm: float,
    span_mm: float,
    elastic_modulus_mpa: float = 200_000.0,
    poisson_ratio: float = 0.3,
) -> float:
    """
    Conservative screening-only estimate for external pressure capacity.
    This is not a replacement for ASME UG-28 chart/procedure checks.
    """
    if shell_thickness_mm <= 0 or diameter_mm <= 0 or span_mm <= 0:
        return 0.0

    thickness_ratio = shell_thickness_mm / diameter_mm
    ld_ratio = span_mm / diameter_mm

    # Elastic buckling style baseline scaled down for conservative screening.
    elastic_capacity = (
        (2.0 * elastic_modulus_mpa) / sqrt(3.0 * (1.0 - poisson_ratio**2))
    ) * (thickness_ratio**3)
    slenderness_factor = min(1.0, 4.0 / max(ld_ratio, 1.0))
    screening_factor = 0.5
    return elastic_capacity * slenderness_factor * screening_factor


def calculate_nozzle_reinforcement_index(
    *,
    nozzle_od_mm: float,
    shell_thickness_mm: float,
    required_shell_thickness_mm: float,
    reinforcement_pad_thickness_mm: float = 0.0,
    reinforcement_pad_width_mm: float = 0.0,
) -> float | None:
    """
    Screening-only reinforcement adequacy index.
    Index >= 1 suggests available metal area is at/above screening demand.
    """
    if nozzle_od_mm <= 0 or shell_thickness_mm <= 0 or required_shell_thickness_mm <= 0:
        return None

    required_area = nozzle_od_mm * required_shell_thickness_mm
    shell_excess = max(shell_thickness_mm - required_shell_thickness_mm, 0.0)
    available_shell_area = 2.0 * nozzle_od_mm * shell_excess
    available_pad_area = max(reinforcement_pad_thickness_mm, 0.0) * max(reinforcement_pad_width_mm, 0.0)
    available_area = available_shell_area + available_pad_area

    if required_area <= 0:
        return None
    return available_area / required_area
