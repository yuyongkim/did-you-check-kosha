from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


VIBRATION_LIMIT_MM_PER_S: Dict[str, float] = {
    "pump": 3.0,
    "compressor": 4.5,
    "steam_turbine": 4.0,
    "gas_turbine": 4.5,
    "blower": 4.8,
    "fan": 5.0,
    "gearbox": 3.5,
}

STANDARD_REFERENCES = {
    "vibration": "API 610/API 617 vibration acceptance context [verify edition]",
    "nozzle_load": "API 610 nozzle load context [verify edition]",
    "monitoring": "API 670 monitoring context [verify edition]",
    "steam_turbine": "API 611/API 612 steam turbine reliability context [verify edition]",
    "steam_properties": "IAPWS IF97 steam property context [verify edition]",
}

CONSENSUS_REL_TOLERANCE = 0.01


@dataclass(frozen=True)
class RotatingThresholds:
    min_speed_rpm: float = 100.0
    max_speed_rpm: float = 25000.0
    max_vibration_mm_per_s: float = 25.0
    max_bearing_temp_c: float = 180.0
    reverse_check_tolerance_percent: float = 5.0
    min_steam_pressure_bar: float = 0.1
    max_steam_pressure_bar: float = 250.0
    min_steam_temperature_c: float = 10.0
    max_steam_temperature_c: float = 650.0
    min_steam_quality_warning: float = 0.9
    steam_phase_change_risk_block: float = 7.0

