from __future__ import annotations

import math


def calculate_reduced_area_mm2(gross_area_mm2: float, corrosion_loss_percent: float) -> float:
    loss = max(0.0, min(corrosion_loss_percent, 95.0)) / 100.0
    return gross_area_mm2 * (1.0 - loss)


def calculate_lambda_c(
    *,
    k_factor: float,
    length_m: float,
    radius_of_gyration_mm: float,
    fy_mpa: float,
    e_modulus_mpa: float,
) -> float:
    kl_over_r = (k_factor * length_m * 1000.0) / max(radius_of_gyration_mm, 1e-9)
    return (kl_over_r / math.pi) * math.sqrt(fy_mpa / max(e_modulus_mpa, 1e-9))


def calculate_fcr_mpa(lambda_c: float, fy_mpa: float) -> float:
    if lambda_c <= 2.25:
        return (0.658 ** (lambda_c**2)) * fy_mpa
    return (0.877 / max(lambda_c**2, 1e-9)) * fy_mpa


def calculate_phi_pn_kn(fcr_mpa: float, reduced_area_mm2: float, phi: float = 0.9) -> float:
    pn_n = fcr_mpa * reduced_area_mm2  # MPa * mm2 = N
    return phi * pn_n / 1000.0


def calculate_dc_ratio(axial_demand_kn: float, phi_pn_kn: float) -> float:
    if phi_pn_kn <= 0:
        return float("inf")
    return axial_demand_kn / phi_pn_kn


def calculate_deflection_ratio(deflection_mm: float, span_mm: float) -> float:
    if span_mm <= 0:
        return 0.0
    allowable = span_mm / 240.0
    if allowable <= 0:
        return 0.0
    return deflection_mm / allowable


def status_from_dc(dc_ratio: float) -> str:
    if dc_ratio >= 1.5:
        return "CRITICAL"
    if dc_ratio >= 1.05:
        return "OVERSTRESSED"
    if dc_ratio >= 1.0:
        return "MARGINAL"
    return "ACCEPTABLE"


def inspection_interval_years(status: str) -> float:
    if status == "CRITICAL":
        return 0.1
    if status == "OVERSTRESSED":
        return 0.5
    if status == "MARGINAL":
        return 1.0
    return 2.0


def reverse_axial_demand_kn(dc_ratio: float, phi_pn_kn: float) -> float:
    if not math.isfinite(dc_ratio):
        return float("inf")
    return dc_ratio * phi_pn_kn


def relative_difference(a: float, b: float) -> float:
    base = max(abs(a), abs(b), 1e-12)
    return abs(a - b) / base


def screen_reinforcement_need(dc_ratio: float, corrosion_loss_percent: float) -> str:
    """Screening-level reinforcement need indicator."""
    if dc_ratio >= 1.5 or corrosion_loss_percent >= 50.0:
        return "REPLACEMENT_RECOMMENDED"
    if dc_ratio >= 1.05 or corrosion_loss_percent >= 30.0:
        return "REINFORCEMENT_RECOMMENDED"
    if dc_ratio >= 0.9 or corrosion_loss_percent >= 15.0:
        return "MONITOR_AND_EVALUATE"
    return "NO_ACTION"


def screen_connection_status(connection_failure_detected: bool, dc_ratio: float) -> str:
    """Screening connection status."""
    if connection_failure_detected:
        return "FAILED_REPAIR_REQUIRED"
    if dc_ratio >= 1.05:
        return "REVIEW_CONNECTION_ADEQUACY"
    return "ACCEPTABLE"


# TODO: screen_load_redistribution_path - requires structural model connectivity not yet available

