from __future__ import annotations

from enum import Enum
from typing import Dict, Iterable, Set

from src.shared.errors import StateTransitionError


class OrchestratorState(str, Enum):
    RECEIVED = "received"
    VALIDATED = "validated"
    CLASSIFIED = "classified"
    STANDARDS_IDENTIFIED = "standards_identified"
    SPEC_EXTRACTED = "spec_extracted"
    CALCULATION_IN_PROGRESS = "calculation_in_progress"
    VERIFICATION_IN_PROGRESS = "verification_in_progress"
    READY_FOR_REPORT = "ready_for_report"
    COMPLETED = "completed"
    ESCALATED = "escalated"
    FAILED = "failed"


ALLOWED_TRANSITIONS: Dict[OrchestratorState, Set[OrchestratorState]] = {
    OrchestratorState.RECEIVED: {OrchestratorState.VALIDATED, OrchestratorState.FAILED},
    OrchestratorState.VALIDATED: {OrchestratorState.CLASSIFIED, OrchestratorState.FAILED},
    OrchestratorState.CLASSIFIED: {OrchestratorState.STANDARDS_IDENTIFIED, OrchestratorState.FAILED},
    OrchestratorState.STANDARDS_IDENTIFIED: {OrchestratorState.SPEC_EXTRACTED, OrchestratorState.FAILED},
    OrchestratorState.SPEC_EXTRACTED: {OrchestratorState.CALCULATION_IN_PROGRESS, OrchestratorState.FAILED},
    OrchestratorState.CALCULATION_IN_PROGRESS: {OrchestratorState.VERIFICATION_IN_PROGRESS, OrchestratorState.FAILED},
    OrchestratorState.VERIFICATION_IN_PROGRESS: {
        OrchestratorState.READY_FOR_REPORT,
        OrchestratorState.ESCALATED,
        OrchestratorState.FAILED,
    },
    OrchestratorState.READY_FOR_REPORT: {OrchestratorState.COMPLETED, OrchestratorState.ESCALATED},
    OrchestratorState.COMPLETED: set(),
    OrchestratorState.ESCALATED: set(),
    OrchestratorState.FAILED: set(),
}


class StateMachine:
    def __init__(self) -> None:
        self.state: OrchestratorState = OrchestratorState.RECEIVED

    def transition(self, target: OrchestratorState, blocking_flag_present: bool = False) -> None:
        if blocking_flag_present:
            raise StateTransitionError("Transition blocked by blocking red flag")

        allowed = ALLOWED_TRANSITIONS[self.state]
        if target not in allowed:
            raise StateTransitionError(f"Invalid transition: {self.state.value} -> {target.value}")
        self.state = target
