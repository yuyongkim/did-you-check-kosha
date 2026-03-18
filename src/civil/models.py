from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class CivilInput:
    element_type: str
    environment_exposure: str
    fc_mpa: float
    fy_mpa: float
    width_mm: float
    effective_depth_mm: float
    rebar_area_mm2: float
    demand_moment_knm: float
    lateral_capacity_loss_percent: float
    affected_area_percent: float
    vertical_capacity_loss_percent: float
    carbonation_coeff_mm_sqrt_year: float
    service_years: float
    cover_thickness_mm: float
    crack_width_mm: float
    spalling_area_percent: float
    foundation_settlement_mm: float


class InputPayloadError(ValueError):
    pass


def _pick(payload: Mapping[str, Any], aliases: list[str], default: Any = None) -> Any:
    for key in aliases:
        if key in payload:
            return payload[key]
    return default


def parse_civil_input(payload: Mapping[str, Any]) -> CivilInput:
    element_type = str(_pick(payload, ["element_type"], "beam")).lower()
    environment_exposure = str(_pick(payload, ["environment_exposure"], "outdoor_urban")).lower()

    fc_mpa = _pick(payload, ["fc_mpa", "fck_mpa", "compressive_strength_mpa"])
    fy_mpa = _pick(payload, ["fy_mpa", "yield_strength_mpa"], 420.0)
    width_mm = _pick(payload, ["width_mm", "b_mm"])
    effective_depth_mm = _pick(payload, ["effective_depth_mm", "d_mm"])
    rebar_area_mm2 = _pick(payload, ["rebar_area_mm2", "as_mm2", "steel_area_mm2"])
    demand_moment_knm = _pick(payload, ["demand_moment_knm", "mu_knm"])

    lateral_capacity_loss_percent = _pick(payload, ["lateral_capacity_loss_percent"], 0.0)
    affected_area_percent = _pick(payload, ["affected_area_percent"], 0.0)
    vertical_capacity_loss_percent = _pick(payload, ["vertical_capacity_loss_percent"], 0.0)

    carbonation_coeff_mm_sqrt_year = _pick(
        payload,
        ["carbonation_coeff_mm_sqrt_year", "carbonation_k", "k_mm_sqrt_year"],
        2.0,
    )
    service_years = _pick(payload, ["service_years", "years_in_service"])
    cover_thickness_mm = _pick(payload, ["cover_thickness_mm", "cover_mm"])
    crack_width_mm = _pick(payload, ["crack_width_mm"], 0.0)
    spalling_area_percent = _pick(payload, ["spalling_area_percent"], 0.0)
    foundation_settlement_mm = _pick(payload, ["foundation_settlement_mm"], 0.0)

    missing = []
    if fc_mpa is None:
        missing.append("fc_mpa")
    if width_mm is None:
        missing.append("width_mm")
    if effective_depth_mm is None:
        missing.append("effective_depth_mm")
    if rebar_area_mm2 is None:
        missing.append("rebar_area_mm2")
    if demand_moment_knm is None:
        missing.append("demand_moment_knm")
    if service_years is None:
        missing.append("service_years")
    if cover_thickness_mm is None:
        missing.append("cover_thickness_mm")

    if missing:
        raise InputPayloadError(f"Missing required fields: {missing}")

    if element_type not in {"beam", "column", "slab", "foundation", "retaining_wall", "pedestal", "pile_cap", "mat_foundation"}:
        raise InputPayloadError(f"Unsupported element_type: {element_type}")

    return CivilInput(
        element_type=element_type,
        environment_exposure=environment_exposure,
        fc_mpa=float(fc_mpa),
        fy_mpa=float(fy_mpa),
        width_mm=float(width_mm),
        effective_depth_mm=float(effective_depth_mm),
        rebar_area_mm2=float(rebar_area_mm2),
        demand_moment_knm=float(demand_moment_knm),
        lateral_capacity_loss_percent=float(lateral_capacity_loss_percent),
        affected_area_percent=float(affected_area_percent),
        vertical_capacity_loss_percent=float(vertical_capacity_loss_percent),
        carbonation_coeff_mm_sqrt_year=float(carbonation_coeff_mm_sqrt_year),
        service_years=float(service_years),
        cover_thickness_mm=float(cover_thickness_mm),
        crack_width_mm=float(crack_width_mm),
        spalling_area_percent=float(spalling_area_percent),
        foundation_settlement_mm=float(foundation_settlement_mm),
    )
