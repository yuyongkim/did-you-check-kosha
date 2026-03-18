from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.state_machine import OrchestratorState
from src.workflows.runner import WorkflowRunner


def main() -> None:
    orchestrator = Orchestrator()
    run = orchestrator.start_run(workflow_id="standard_calculation")

    WorkflowRunner.run_standard_happy_path(orchestrator)

    if orchestrator.can_release():
        orchestrator.advance(OrchestratorState.COMPLETED)

    print("workflow_id:", run.trace.workflow_id)
    print("correlation_id:", run.trace.correlation_id)
    print("trace_id:", run.trace.trace_id)
    print("state:", run.state_machine.state.value)
    print("blocking_flags:", orchestrator.has_blocking_flag())


if __name__ == "__main__":
    main()
