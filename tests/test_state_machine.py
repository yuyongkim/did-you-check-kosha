import unittest

from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.state_machine import OrchestratorState
from src.shared.errors import StateTransitionError


class StateMachineTests(unittest.TestCase):
    def test_happy_path_transition(self) -> None:
        orch = Orchestrator()
        orch.start_run()
        orch.advance(OrchestratorState.VALIDATED)
        orch.advance(OrchestratorState.CLASSIFIED)
        self.assertEqual(orch.current_run.state_machine.state, OrchestratorState.CLASSIFIED)

    def test_blocked_transition_when_critical_flag_exists(self) -> None:
        orch = Orchestrator()
        orch.start_run()
        orch.add_flag("STD.INVALID_REFERENCE")
        with self.assertRaises(StateTransitionError):
            orch.advance(OrchestratorState.VALIDATED)


if __name__ == "__main__":
    unittest.main()
