from __future__ import annotations

from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.state_machine import OrchestratorState


class WorkflowRunner:
    """Executes orchestrator state transitions for baseline workflow paths."""

    @staticmethod
    def run_standard_happy_path(orchestrator: Orchestrator) -> None:
        orchestrator.advance(OrchestratorState.VALIDATED)
        orchestrator.advance(OrchestratorState.CLASSIFIED)
        orchestrator.advance(OrchestratorState.STANDARDS_IDENTIFIED)
        orchestrator.advance(OrchestratorState.SPEC_EXTRACTED)
        orchestrator.advance(OrchestratorState.CALCULATION_IN_PROGRESS)
        orchestrator.advance(OrchestratorState.VERIFICATION_IN_PROGRESS)
        orchestrator.advance(OrchestratorState.READY_FOR_REPORT)

