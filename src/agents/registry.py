from __future__ import annotations

from dataclasses import dataclass
from typing import List


REQUIRED_AGENTS = [
    "orchestrator",
    "spec_explorer",
    "piping_specialist",
    "static_equipment_specialist",
    "rotating_specialist",
    "electrical_specialist",
    "instrumentation_specialist",
    "steel_specialist",
    "civil_specialist",
    "calculator_worker",
    "verification_agent",
]


def missing_required_agents(configured_names: List[str]) -> List[str]:
    configured = set(configured_names)
    return [name for name in REQUIRED_AGENTS if name not in configured]
