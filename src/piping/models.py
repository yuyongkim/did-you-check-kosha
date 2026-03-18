from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Mapping

from src.piping.constants import NPS_TO_OD_MM


@dataclass(frozen=True)
class ThicknessRecord:
    date: str
    thickness_mm: float

    def as_datetime(self) -> datetime:
        return datetime.fromisoformat(self.date)


@dataclass(frozen=True)
class PipingInput:
    material: str
    nps: float | None
    od_mm: float
    design_pressure_mpa: float
    design_temperature_c: float
    thickness_history: List[ThicknessRecord]
    corrosion_allowance_mm: float = 1.5
    weld_type: str = "seamless"
    service_type: str = "general"
    fluid_type: str = "hydrocarbon_dry"
    has_internal_coating: bool = False
    chloride_ppm: float | None = None
    temperature_profile: str = "strict_process"
    design_factor: float = 1.0

    @property
    def current_thickness_mm(self) -> float:
        return self.thickness_history[-1].thickness_mm


class InputPayloadError(ValueError):
    """Raised when piping payload cannot be parsed."""


REQUIRED_FIELDS = {
    "material",
    "design_pressure_mpa",
    "design_temperature_c",
    "thickness_history",
}


def parse_piping_input(payload: Mapping[str, Any]) -> PipingInput:
    missing = REQUIRED_FIELDS - set(payload.keys())
    if missing:
        raise InputPayloadError(f"Missing required fields: {sorted(missing)}")

    material = str(payload["material"]).strip()
    nps_raw = payload.get("nps")
    nps = float(nps_raw) if nps_raw is not None else None

    od_raw = payload.get("od_mm")
    if od_raw is None:
        if nps is None:
            raise InputPayloadError("Either od_mm or nps is required")
        if nps not in NPS_TO_OD_MM:
            raise InputPayloadError(f"Unsupported NPS for OD lookup: {nps}")
        od_mm = NPS_TO_OD_MM[nps]
    else:
        od_mm = float(od_raw)

    history_raw = payload["thickness_history"]
    if not isinstance(history_raw, list) or len(history_raw) < 2:
        raise InputPayloadError("thickness_history must have at least 2 records")

    records: List[ThicknessRecord] = []
    for row in history_raw:
        if not isinstance(row, Mapping):
            raise InputPayloadError("thickness_history rows must be objects")
        if "date" not in row or "thickness_mm" not in row:
            raise InputPayloadError("thickness_history row requires date and thickness_mm")
        date = str(row["date"])
        try:
            datetime.fromisoformat(date)
        except ValueError as exc:
            raise InputPayloadError(f"Invalid date format in thickness_history: {date}") from exc

        records.append(ThicknessRecord(date=date, thickness_mm=float(row["thickness_mm"])))

    records.sort(key=lambda r: r.as_datetime())

    return PipingInput(
        material=material,
        nps=nps,
        od_mm=od_mm,
        design_pressure_mpa=float(payload["design_pressure_mpa"]),
        design_temperature_c=float(payload["design_temperature_c"]),
        thickness_history=records,
        corrosion_allowance_mm=float(payload.get("corrosion_allowance_mm", payload.get("CA_mm", 1.5))),
        weld_type=str(payload.get("weld_type", "seamless")).lower(),
        service_type=str(payload.get("service_type", "general")).lower(),
        fluid_type=str(payload.get("fluid_type", "hydrocarbon_dry")).lower(),
        has_internal_coating=bool(payload.get("has_internal_coating", False)),
        chloride_ppm=(float(payload["chloride_ppm"]) if payload.get("chloride_ppm") is not None else None),
        temperature_profile=str(payload.get("temperature_profile", "strict_process")).strip().lower(),
        design_factor=float(payload.get("design_factor", 1.0)),
    )

