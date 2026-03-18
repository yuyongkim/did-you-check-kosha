from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class VesselInput:
    material: str
    vessel_type: str
    design_pressure_mpa: float
    design_temperature_c: float
    inside_radius_mm: float
    shell_length_mm: float | None
    straight_shell_height_mm: float | None
    head_type: str
    head_depth_mm: float | None
    nozzle_od_mm: float | None
    external_pressure_mpa: float | None
    reinforcement_pad_thickness_mm: float | None
    reinforcement_pad_width_mm: float | None
    joint_efficiency: float
    current_thickness_mm: float
    corrosion_allowance_mm: float
    assumed_corrosion_rate_mm_per_year: float


class InputPayloadError(ValueError):
    pass


def _pick(payload: Mapping[str, Any], aliases: list[str], default: Any = None) -> Any:
    for key in aliases:
        if key in payload:
            return payload[key]
    return default


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, str) and not value.strip():
        return None
    return float(value)


def parse_vessel_input(payload: Mapping[str, Any]) -> VesselInput:
    material = str(_pick(payload, ["material"]))
    vessel_type = str(_pick(payload, ["vessel_type"], "horizontal_drum"))
    head_type = str(_pick(payload, ["head_type"], "ellipsoidal_2_1"))
    if not material or material == "None":
        raise InputPayloadError("material is required")

    p = _pick(payload, ["design_pressure_mpa", "design_pressure_MPa"])
    t = _pick(payload, ["design_temperature_c", "design_temperature_C"])
    r = _pick(payload, ["inside_radius_mm", "radius_mm", "inside_radius"])
    shell_length = _pick(payload, ["shell_length_mm", "tangent_to_tangent_length_mm", "tt_length_mm"])
    shell_height = _pick(payload, ["straight_shell_height_mm", "vessel_height_mm", "straight_height_mm"])
    head_depth = _pick(payload, ["head_depth_mm", "head_height_mm"])
    nozzle_od = _pick(payload, ["nozzle_od_mm", "nozzle_diameter_mm"])
    external_pressure = _pick(payload, ["external_pressure_mpa", "external_pressure_MPa"])
    reinforcement_pad_thickness = _pick(payload, ["reinforcement_pad_thickness_mm", "pad_thickness_mm"])
    reinforcement_pad_width = _pick(payload, ["reinforcement_pad_width_mm", "pad_width_mm"])
    e = _pick(payload, ["joint_efficiency", "E"], 0.85)
    tc = _pick(payload, ["t_current_mm", "current_thickness_mm"])
    ca = _pick(payload, ["corrosion_allowance_mm", "CA_mm"], 1.5)
    cr = _pick(payload, ["assumed_corrosion_rate_mm_per_year", "corrosion_rate_mm_per_year"], 0.2)

    missing = []
    if p is None:
        missing.append("design_pressure_mpa")
    if t is None:
        missing.append("design_temperature_c")
    if r is None:
        missing.append("inside_radius_mm")
    if tc is None:
        missing.append("t_current_mm")

    if missing:
        raise InputPayloadError(f"Missing required fields: {missing}")

    return VesselInput(
        material=material,
        vessel_type=vessel_type,
        design_pressure_mpa=float(p),
        design_temperature_c=float(t),
        inside_radius_mm=float(r),
        shell_length_mm=_optional_float(shell_length),
        straight_shell_height_mm=_optional_float(shell_height),
        head_type=head_type,
        head_depth_mm=_optional_float(head_depth),
        nozzle_od_mm=_optional_float(nozzle_od),
        external_pressure_mpa=_optional_float(external_pressure),
        reinforcement_pad_thickness_mm=_optional_float(reinforcement_pad_thickness),
        reinforcement_pad_width_mm=_optional_float(reinforcement_pad_width),
        joint_efficiency=float(e),
        current_thickness_mm=float(tc),
        corrosion_allowance_mm=float(ca),
        assumed_corrosion_rate_mm_per_year=float(cr),
    )

