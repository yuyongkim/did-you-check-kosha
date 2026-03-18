from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


ENVIRONMENT_EXPOSURE_FACTOR: Dict[str, float] = {
    "indoor_dry": 0.8,
    "outdoor_urban": 1.0,
    "coastal_marine": 1.25,
    "industrial_chemical": 1.2,
    "splash_zone": 1.35,
    "buried_soil": 1.1,
}


STANDARD_REFERENCES = {
    "damage_classification": "ACI 562 substantial damage classification context [verify edition]",
    "flexure_strength": "ACI 318 flexural strength context [verify edition]",
    "carbonation": "Concrete carbonation depth assessment context [verify edition]",
    "durability": "Concrete crack/spalling durability limits context [verify edition]",
}

CONSENSUS_REL_TOLERANCE = 0.01


@dataclass(frozen=True)
class CivilThresholds:
    min_fc_mpa: float = 15.0
    max_fc_mpa: float = 80.0
    min_fy_mpa: float = 250.0
    max_fy_mpa: float = 700.0
    min_service_years: float = 0.0
    max_service_years: float = 120.0
    min_cover_mm: float = 15.0
    max_cover_mm: float = 100.0
    crack_width_limit_mm: float = 0.4
    spalling_area_limit_percent: float = 20.0
    foundation_settlement_limit_mm: float = 25.0
    reverse_check_tolerance_percent: float = 5.0
