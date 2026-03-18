from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping

from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.state_machine import OrchestratorState
from src.shared.message_factory import create_message
from src.workflows.runner import WorkflowRunner


@dataclass
class PipelineResult:
    status: str
    workflow_id: str
    state: str
    calculation: Mapping[str, Any]
    verification: Mapping[str, Any]
    blocking_flags: bool


class PipelineService:
    """Minimal end-to-end pipeline wrapper for mock runtime integration."""

    def __init__(self, orchestrator: Orchestrator) -> None:
        self.orchestrator = orchestrator

    def run_standard_pipeline(
        self,
        *,
        discipline_agent: str,
        calculation_type: str,
        input_data: Mapping[str, Any],
    ) -> PipelineResult:
        run = self.orchestrator.start_run("standard_calculation")
        WorkflowRunner.run_standard_happy_path(self.orchestrator)

        calc_message = create_message(
            message_type="calculation_request",
            from_agent="orchestrator",
            to_agent=discipline_agent,
            payload={"calculation_type": calculation_type, "input_data": dict(input_data)},
            correlation_id=run.trace.correlation_id,
            trace_id=run.trace.trace_id,
            meta={"workflow_id": "standard_calculation"},
        )
        calc_result = self.orchestrator.handle_message(calc_message)

        verify_message = create_message(
            message_type="verification_request",
            from_agent="orchestrator",
            to_agent="verification_agent",
            payload={
                "verification_type": "maker_voting",
                "inputs": dict(input_data),
                "results": calc_result.get("results", {}),
            },
            correlation_id=run.trace.correlation_id,
            trace_id=run.trace.trace_id,
            meta={"workflow_id": "standard_calculation"},
        )
        verify_result = self.orchestrator.handle_message(verify_message)

        status = "success"
        if self.orchestrator.has_blocking_flag():
            status = "blocked"
        elif self.orchestrator.can_release():
            self.orchestrator.advance(OrchestratorState.COMPLETED)
            status = "completed"

        return PipelineResult(
            status=status,
            workflow_id=run.trace.workflow_id,
            state=run.state_machine.state.value,
            calculation=calc_result,
            verification=verify_result,
            blocking_flags=self.orchestrator.has_blocking_flag(),
        )

