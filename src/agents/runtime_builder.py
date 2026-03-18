from __future__ import annotations

from typing import Mapping

from src.agents.runtime import AgentRuntime
from src.agents.specialists.civil_agent import CivilSpecialistAgent
from src.agents.specialists.electrical_agent import ElectricalSpecialistAgent
from src.agents.specialists.instrumentation_agent import InstrumentationSpecialistAgent
from src.agents.specialists.mock_impl import MockSpecialist
from src.agents.specialists.piping_agent import PipingSpecialistAgent
from src.agents.specialists.rotating_agent import RotatingSpecialistAgent
from src.agents.specialists.steel_agent import SteelSpecialistAgent
from src.agents.specialists.vessel_agent import VesselSpecialistAgent
from src.agents.support.mock_impl import (
    MockCalculatorWorker,
    MockSpecExplorer,
    MockVerificationAgent,
)


SPECIALIST_DISCIPLINE_MAP = {
    "piping_specialist": "piping",
    "static_equipment_specialist": "static_equipment",
    "rotating_specialist": "rotating",
    "electrical_specialist": "electrical",
    "instrumentation_specialist": "instrumentation",
    "steel_specialist": "steel",
    "civil_specialist": "civil",
}


def build_mock_runtime(config: Mapping[str, object]) -> AgentRuntime:
    runtime = AgentRuntime()
    runtime.register("orchestrator", object())
    runtime.register("spec_explorer", MockSpecExplorer())
    runtime.register("calculator_worker", MockCalculatorWorker())
    runtime.register("verification_agent", MockVerificationAgent())

    agents = config.get("agents", {})
    if not isinstance(agents, Mapping):
        agents = {}

    for specialist_name, discipline in SPECIALIST_DISCIPLINE_MAP.items():
        if specialist_name not in agents:
            continue

        if specialist_name == "piping_specialist":
            runtime.register(specialist_name, PipingSpecialistAgent())
            continue
        if specialist_name == "static_equipment_specialist":
            runtime.register(specialist_name, VesselSpecialistAgent())
            continue
        if specialist_name == "rotating_specialist":
            runtime.register(specialist_name, RotatingSpecialistAgent())
            continue
        if specialist_name == "electrical_specialist":
            runtime.register(specialist_name, ElectricalSpecialistAgent())
            continue
        if specialist_name == "instrumentation_specialist":
            runtime.register(specialist_name, InstrumentationSpecialistAgent())
            continue
        if specialist_name == "steel_specialist":
            runtime.register(specialist_name, SteelSpecialistAgent())
            continue
        if specialist_name == "civil_specialist":
            runtime.register(specialist_name, CivilSpecialistAgent())
            continue

        runtime.register(
            specialist_name,
            MockSpecialist(name=specialist_name, discipline=discipline),
        )

    return runtime
