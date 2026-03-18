import unittest

from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.state_machine import OrchestratorState
from src.workflows.runner import WorkflowRunner


class WorkflowRunnerTests(unittest.TestCase):
    def test_standard_workflow_reaches_ready_for_report(self) -> None:
        orchestrator = Orchestrator()
        orchestrator.start_run()
        WorkflowRunner.run_standard_happy_path(orchestrator)
        self.assertEqual(
            orchestrator.current_run.state_machine.state,
            OrchestratorState.READY_FOR_REPORT,
        )


if __name__ == "__main__":
    unittest.main()

