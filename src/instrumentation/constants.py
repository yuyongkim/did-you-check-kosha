from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


SIL_TARGET_PFD_LIMIT: Dict[int, float] = {
    1: 1e-2,
    2: 1e-3,
    3: 1e-4,
    4: 1e-5,
}

ARCHITECTURE_PFD_FACTOR: Dict[str, float] = {
    "1oo1": 1.0,
    "1oo2": 0.45,
    "2oo2": 0.55,
    "2oo3": 0.3,
}

INSTRUMENT_TYPE_DRIFT_FACTOR: Dict[str, float] = {
    "pressure_transmitter": 1.0,
    "temperature_transmitter": 0.9,
    "flow_meter": 1.15,
    "level_transmitter": 1.05,
    "control_valve_positioner": 1.2,
    "analyzer": 1.25,
    "vibration_probe": 1.1,
}

STANDARD_REFERENCES = {
    "drift_analysis": "ISO GUM drift and uncertainty context [verify edition]",
    "sil_validation": "IEC 61511 / ISA-TR84.00.02 SIL validation context [verify edition]",
    "instrument_id": "ISA 5.1 instrument identification context [verify edition]",
    "valve_sizing": "Control valve sizing context [verify edition]",
}

CONSENSUS_REL_TOLERANCE = 0.01


@dataclass(frozen=True)
class InstrumentationThresholds:
    min_failure_rate_per_hour: float = 1e-10
    max_failure_rate_per_hour: float = 1e-3
    max_test_interval_hours: float = 24.0 * 365.0 * 5.0
    reverse_check_tolerance_percent: float = 5.0
