from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set


ALLOWABLE_STRESS_TABLE_MPA: Dict[str, Dict[float, float]] = {
    "SA-516-60": {
        20.0: 131.0,
        100.0: 124.0,
        200.0: 117.0,
        300.0: 110.0,
        400.0: 103.0,
    },
    "SA-516-65": {
        20.0: 135.0,
        100.0: 128.0,
        200.0: 121.0,
        300.0: 114.0,
        400.0: 107.0,
    },
    "SA-516-70": {
        20.0: 138.0,
        100.0: 131.0,
        200.0: 124.0,
        300.0: 117.0,
        400.0: 110.0,
    },
    "SA-515-70": {
        20.0: 131.0,
        100.0: 124.0,
        200.0: 117.0,
        300.0: 110.0,
        400.0: 103.0,
    },
    "SA-537 Cl1": {
        20.0: 155.0,
        100.0: 148.0,
        200.0: 141.0,
        300.0: 134.0,
        400.0: 127.0,
    },
    "SA-387 Gr11 Cl2": {
        20.0: 138.0,
        100.0: 138.0,
        200.0: 132.0,
        300.0: 126.0,
        400.0: 120.0,
        500.0: 108.0,
        550.0: 101.0,
    },
    "SA-387 Gr22 Cl2": {
        20.0: 138.0,
        100.0: 138.0,
        200.0: 134.0,
        300.0: 128.0,
        400.0: 122.0,
        500.0: 112.0,
        550.0: 105.0,
    },
    "SA-240-304": {
        20.0: 138.0,
        100.0: 131.0,
        200.0: 124.0,
        300.0: 117.0,
        400.0: 110.0,
        500.0: 97.0,
    },
    "SA-240-304L": {
        20.0: 132.0,
        100.0: 125.0,
        200.0: 118.0,
        300.0: 111.0,
        400.0: 104.0,
        500.0: 90.0,
    },
    "SA-240-316": {
        20.0: 138.0,
        100.0: 131.0,
        200.0: 124.0,
        300.0: 117.0,
        400.0: 110.0,
        500.0: 97.0,
    },
    "SA-240-316L": {
        20.0: 132.0,
        100.0: 125.0,
        200.0: 118.0,
        300.0: 111.0,
        400.0: 104.0,
        500.0: 90.0,
    },
    "SA-240-321": {
        20.0: 138.0,
        100.0: 131.0,
        200.0: 125.0,
        300.0: 119.0,
        400.0: 113.0,
        500.0: 97.0,
    },
    "SA-240-347": {
        20.0: 138.0,
        100.0: 131.0,
        200.0: 126.0,
        300.0: 120.0,
        400.0: 114.0,
        500.0: 99.0,
    },
}

MATERIAL_TEMP_LIMIT_C: Dict[str, float] = {
    "SA-516-60": 425.0,
    "SA-516-65": 425.0,
    "SA-516-70": 425.0,
    "SA-515-70": 425.0,
    "SA-537 Cl1": 425.0,
    "SA-387 Gr11 Cl2": 593.0,
    "SA-387 Gr22 Cl2": 593.0,
    "SA-240-304": 538.0,
    "SA-240-304L": 538.0,
    "SA-240-316": 538.0,
    "SA-240-316L": 538.0,
    "SA-240-321": 538.0,
    "SA-240-347": 538.0,
}

VALID_JOINT_EFFICIENCIES: Set[float] = {1.0, 0.95, 0.9, 0.85, 0.8, 0.7, 0.6}

STANDARD_REFERENCES = {
    "shell_thickness": "ASME Section VIII Div.1 UG-27 [verify edition]",
    "external_pressure": "ASME Section VIII Div.1 UG-28 external pressure procedure [verify edition]",
    "nozzle_reinforcement": "ASME Section VIII Div.1 UG-37 nozzle reinforcement [verify edition]",
    "joint_efficiency": "ASME Section VIII joint efficiency tables [verify edition]",
    "inspection_interval": "API 510 interval guidance [verify edition]",
    "local_thinning": "API 579-1 Level 1 screening context [verify edition]",
}

CONSENSUS_REL_TOLERANCE = 0.01


@dataclass(frozen=True)
class VesselThresholds:
    min_pressure_mpa: float = 0.0
    max_pressure_mpa: float = 35.0
    min_temperature_c: float = -50.0
    max_temperature_c: float = 650.0
    reverse_check_tolerance_percent: float = 5.0

