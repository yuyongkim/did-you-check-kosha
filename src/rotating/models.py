from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class RotatingInput:
    machine_type: str
    vibration_mm_per_s: float
    nozzle_load_ratio: float
    bearing_temperature_c: float
    speed_rpm: float
    steam_pressure_bar: float | None = None
    steam_temperature_c: float | None = None
    steam_quality_x: float | None = None
    inlet_enthalpy_kj_per_kg: float | None = None
    outlet_enthalpy_kj_per_kg: float | None = None


class InputPayloadError(ValueError):
    pass


def _pick(payload: Mapping[str, Any], aliases: list[str], default: Any = None) -> Any:
    for key in aliases:
        if key in payload:
            return payload[key]
    return default


def parse_rotating_input(payload: Mapping[str, Any]) -> RotatingInput:
    machine_type = str(_pick(payload, ["machine_type"], "pump")).lower()
    vibration = _pick(payload, ["vibration_mm_per_s", "vibration_mms", "vibration"])
    nozzle = _pick(payload, ["nozzle_load_ratio", "nozzle_load"])
    bearing_temp = _pick(payload, ["bearing_temperature_c", "bearing_temp_c", "bearing_temp"])
    speed = _pick(payload, ["speed_rpm", "rpm"], 1800)

    steam_pressure = _pick(payload, ["steam_pressure_bar", "steam_pressure_barg", "steam_pressure"])
    steam_temperature = _pick(payload, ["steam_temperature_c", "steam_temp_c", "steam_temperature"])
    steam_quality = _pick(payload, ["steam_quality_x", "steam_quality", "quality_x"])
    inlet_enthalpy = _pick(payload, ["inlet_enthalpy_kj_per_kg", "inlet_enthalpy", "h_in"])
    outlet_enthalpy = _pick(payload, ["outlet_enthalpy_kj_per_kg", "outlet_enthalpy", "h_out"])

    missing = []
    if vibration is None:
        missing.append("vibration_mm_per_s")
    if nozzle is None:
        missing.append("nozzle_load_ratio")
    if bearing_temp is None:
        missing.append("bearing_temperature_c")

    if missing:
        raise InputPayloadError(f"Missing required fields: {missing}")

    supported = {
        "pump",
        "compressor",
        "steam_turbine",
        "gas_turbine",
        "blower",
        "fan",
        "gearbox",
    }
    if machine_type not in supported:
        raise InputPayloadError(f"Unsupported machine_type: {machine_type}")

    try:
        return RotatingInput(
            machine_type=machine_type,
            vibration_mm_per_s=float(vibration),
            nozzle_load_ratio=float(nozzle),
            bearing_temperature_c=float(bearing_temp),
            speed_rpm=float(speed),
            steam_pressure_bar=float(steam_pressure) if steam_pressure is not None else None,
            steam_temperature_c=float(steam_temperature) if steam_temperature is not None else None,
            steam_quality_x=float(steam_quality) if steam_quality is not None else None,
            inlet_enthalpy_kj_per_kg=float(inlet_enthalpy) if inlet_enthalpy is not None else None,
            outlet_enthalpy_kj_per_kg=float(outlet_enthalpy) if outlet_enthalpy is not None else None,
        )
    except (TypeError, ValueError) as exc:
        raise InputPayloadError(f"Invalid numeric value in rotating payload: {exc}") from exc
