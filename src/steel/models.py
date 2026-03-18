from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class SteelInput:
    member_type: str
    steel_grade: str
    section_label: str
    length_m: float
    k_factor: float
    radius_of_gyration_mm: float
    yield_strength_mpa: float
    elasticity_mpa: float
    gross_area_mm2: float
    corrosion_loss_percent: float
    axial_demand_kn: float
    moment_demand_knm: float
    deflection_mm: float
    span_mm: float
    connection_failure_detected: bool


class InputPayloadError(ValueError):
    pass


def _pick(payload: Mapping[str, Any], aliases: list[str], default: Any = None) -> Any:
    for key in aliases:
        if key in payload:
            return payload[key]
    return default


def parse_steel_input(payload: Mapping[str, Any]) -> SteelInput:
    member_type = str(_pick(payload, ["member_type"], "column")).lower()
    steel_grade = str(_pick(payload, ["steel_grade"], "a572_gr50")).lower()
    section_label = str(_pick(payload, ["section_label", "section"], "UNKNOWN"))

    length_m = _pick(payload, ["length_m"])
    k_factor = _pick(payload, ["k_factor"], 1.0)
    rg_mm = _pick(payload, ["radius_of_gyration_mm", "r_mm"])
    fy = _pick(payload, ["yield_strength_mpa", "fy_mpa"])
    e_mod = _pick(payload, ["elasticity_mpa", "e_modulus_mpa"], 200000.0)
    area = _pick(payload, ["gross_area_mm2", "area_mm2"])
    corrosion = _pick(payload, ["corrosion_loss_percent"], 0.0)
    pu = _pick(payload, ["axial_demand_kn", "pu_kn"])
    mu = _pick(payload, ["moment_demand_knm", "mu_knm"], 0.0)
    defl = _pick(payload, ["deflection_mm"], 0.0)
    span = _pick(payload, ["span_mm"], 0.0)
    conn_fail = bool(_pick(payload, ["connection_failure_detected"], False))

    missing = []
    if length_m is None:
        missing.append("length_m")
    if rg_mm is None:
        missing.append("radius_of_gyration_mm")
    if fy is None:
        missing.append("yield_strength_mpa")
    if area is None:
        missing.append("gross_area_mm2")
    if pu is None:
        missing.append("axial_demand_kn")

    if missing:
        raise InputPayloadError(f"Missing required fields: {missing}")

    if member_type not in {"column", "beam", "brace", "girder", "truss_member", "pipe_rack_leg", "portal_frame"}:
        raise InputPayloadError(f"Unsupported member_type: {member_type}")

    return SteelInput(
        member_type=member_type,
        steel_grade=steel_grade,
        section_label=section_label,
        length_m=float(length_m),
        k_factor=float(k_factor),
        radius_of_gyration_mm=float(rg_mm),
        yield_strength_mpa=float(fy),
        elasticity_mpa=float(e_mod),
        gross_area_mm2=float(area),
        corrosion_loss_percent=float(corrosion),
        axial_demand_kn=float(pu),
        moment_demand_knm=float(mu),
        deflection_mm=float(defl),
        span_mm=float(span),
        connection_failure_detected=conn_fail,
    )
