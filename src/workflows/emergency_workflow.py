from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.workflows.steps import EMERGENCY_WORKFLOW_STEPS


@dataclass(frozen=True)
class EmergencyWorkflow:
    workflow_id: str = "emergency_assessment"
    fast_track: bool = True
    escalation_required: bool = True

    def steps(self) -> List[str]:
        return list(EMERGENCY_WORKFLOW_STEPS)
