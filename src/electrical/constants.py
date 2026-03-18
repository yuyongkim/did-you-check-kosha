from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


EQUIPMENT_ARC_FACTOR: Dict[str, float] = {
    "transformer": 1.0,
    "switchgear": 1.15,
    "mcc": 1.05,
    "motor": 0.95,
    "ups": 0.9,
    "feeder_panel": 1.1,
}

EQUIPMENT_HI_BIAS: Dict[str, float] = {
    "transformer": 0.0,
    "switchgear": -0.2,
    "mcc": -0.1,
    "motor": 0.1,
    "ups": 0.2,
    "feeder_panel": -0.15,
}

HI_WEIGHTS: Dict[str, float] = {
    "dga": 0.35,
    "oil_quality": 0.25,
    "insulation": 0.20,
    "load_factor": 0.20,
}

STANDARD_REFERENCES = {
    "health_index": "IEEE C57.104 health assessment context [verify edition]",
    "arc_flash": "IEEE 1584-2018 incident energy context [verify edition]",
    "safety": "NFPA 70E electrical safety context [verify edition]",
    "voltage_drop": "IEEE 3002.2 voltage drop context [verify edition]",
    "short_circuit": "IEEE 3002.3 short-circuit context [verify edition]",
    "harmonic": "IEEE 519 harmonic distortion context [verify edition]",
}

CONSENSUS_REL_TOLERANCE = 0.01


@dataclass(frozen=True)
class ElectricalThresholds:
    min_voltage_kv: float = 0.2
    max_voltage_kv: float = 230.0
    min_fault_current_ka: float = 0.1
    max_fault_current_ka: float = 100.0
    max_clearing_time_sec: float = 2.0
    min_working_distance_mm: float = 300.0
    max_working_distance_mm: float = 1200.0
    reverse_check_tolerance_percent: float = 5.0
