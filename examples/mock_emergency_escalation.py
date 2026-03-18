from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.state_machine import OrchestratorState
from src.shared.errors import StateTransitionError


def main() -> None:
    orchestrator = Orchestrator()
    run = orchestrator.start_run(workflow_id="emergency_assessment")
    orchestrator.add_flag("STD.INVALID_REFERENCE")

    try:
        orchestrator.advance(OrchestratorState.VALIDATED)
    except StateTransitionError as exc:
        print("workflow_id:", run.trace.workflow_id)
        print("state:", run.state_machine.state.value)
        print("blocked_by_flag:", orchestrator.has_blocking_flag())
        print("error:", str(exc))
        return

    print("unexpected_state:", run.state_machine.state.value)


if __name__ == "__main__":
    main()

