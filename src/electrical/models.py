from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class ElectricalInput:
    equipment_type: str
    system_voltage_kv: float
    bolted_fault_current_ka: float
    clearing_time_sec: float
    working_distance_mm: float
    breaker_interrupt_rating_ka: float
    voltage_drop_percent: float
    thd_voltage_percent: float
    dga_score: float
    oil_quality_score: float
    insulation_score: float
    load_factor_score: float
    motor_current_thd_percent: float
    power_factor: float


class InputPayloadError(ValueError):
    pass


def _pick(payload: Mapping[str, Any], aliases: list[str], default: Any = None) -> Any:
    for key in aliases:
        if key in payload:
            return payload[key]
    return default


def parse_electrical_input(payload: Mapping[str, Any]) -> ElectricalInput:
    equipment_type = str(_pick(payload, ["equipment_type"], "transformer")).lower()
    v_kv = _pick(payload, ["system_voltage_kv", "voltage_kv"])
    ifault = _pick(payload, ["bolted_fault_current_ka", "fault_current_ka"])
    clearing = _pick(payload, ["clearing_time_sec", "trip_time_sec"])
    dist = _pick(payload, ["working_distance_mm", "distance_mm"])
    breaker = _pick(payload, ["breaker_interrupt_rating_ka", "breaker_rating_ka"])
    vdrop = _pick(payload, ["voltage_drop_percent", "voltage_drop_pct"])
    thd_v = _pick(payload, ["thd_voltage_percent", "voltage_thd_percent", "thd_percent"])
    dga = _pick(payload, ["dga_score"])
    oil = _pick(payload, ["oil_quality_score", "oil_score"])
    ins = _pick(payload, ["insulation_score"])
    load = _pick(payload, ["load_factor_score", "load_score"])

    missing = []
    if v_kv is None:
        missing.append("system_voltage_kv")
    if ifault is None:
        missing.append("bolted_fault_current_ka")
    if clearing is None:
        missing.append("clearing_time_sec")
    if dist is None:
        missing.append("working_distance_mm")
    if breaker is None:
        missing.append("breaker_interrupt_rating_ka")
    if vdrop is None:
        missing.append("voltage_drop_percent")
    if thd_v is None:
        missing.append("thd_voltage_percent")
    if dga is None:
        missing.append("dga_score")
    if oil is None:
        missing.append("oil_quality_score")
    if ins is None:
        missing.append("insulation_score")
    if load is None:
        missing.append("load_factor_score")

    if missing:
        raise InputPayloadError(f"Missing required fields: {missing}")

    i_thd = _pick(payload, ["motor_current_thd_percent", "current_thd_percent"], thd_v)
    pf = _pick(payload, ["power_factor", "pf"], 0.9)

    return ElectricalInput(
        equipment_type=equipment_type,
        system_voltage_kv=float(v_kv),
        bolted_fault_current_ka=float(ifault),
        clearing_time_sec=float(clearing),
        working_distance_mm=float(dist),
        breaker_interrupt_rating_ka=float(breaker),
        voltage_drop_percent=float(vdrop),
        thd_voltage_percent=float(thd_v),
        dga_score=float(dga),
        oil_quality_score=float(oil),
        insulation_score=float(ins),
        load_factor_score=float(load),
        motor_current_thd_percent=float(i_thd),
        power_factor=float(pf),
    )
