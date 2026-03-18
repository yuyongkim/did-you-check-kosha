import pathlib
import unittest

from src.agents.runtime_builder import build_mock_runtime
from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.state_machine import OrchestratorState
from src.shared.config_loader import load_and_validate_config
from src.shared.message_factory import create_message
from src.workflows.runner import WorkflowRunner


class E2EPipelineTests(unittest.TestCase):
    def test_mock_e2e_standard_pipeline(self) -> None:
        config, errors = load_and_validate_config(pathlib.Path("configs/sample_config.json"))
        self.assertEqual(errors, [])
        runtime = build_mock_runtime(config)
        orchestrator = Orchestrator(runtime=runtime)
        orchestrator.start_run("standard_calculation")

        WorkflowRunner.run_standard_happy_path(orchestrator)

        calc_message = create_message(
            message_type="calculation_request",
            from_agent="orchestrator",
            to_agent="piping_specialist",
            payload={
                "calculation_type": "remaining_life",
                "input_data": {
                    "material": "SA-106 Gr.B",
                    "nps": 6.0,
                    "design_pressure_mpa": 4.5,
                    "design_temperature_c": 250.0,
                    "thickness_history": [
                        {"date": "2015-01-01", "thickness_mm": 10.0},
                        {"date": "2020-01-01", "thickness_mm": 8.6},
                        {"date": "2025-01-01", "thickness_mm": 7.3},
                    ],
                    "corrosion_allowance_mm": 1.5,
                    "weld_type": "seamless",
                    "service_type": "general",
                    "has_internal_coating": False,
                },
            },
            correlation_id=orchestrator.current_run.trace.correlation_id,
            trace_id=orchestrator.current_run.trace.trace_id,
            meta={"workflow_id": "standard_calculation"},
        )
        calc_result = orchestrator.handle_message(calc_message)
        self.assertEqual(calc_result["status"], "success")

        verify_message = create_message(
            message_type="verification_request",
            from_agent="orchestrator",
            to_agent="verification_agent",
            payload={
                "verification_type": "maker_voting",
                "inputs": calc_message["payload"]["input_data"],
                "results": calc_result["results"],
            },
            correlation_id=orchestrator.current_run.trace.correlation_id,
            trace_id=orchestrator.current_run.trace.trace_id,
            meta={"workflow_id": "standard_calculation"},
        )
        verify_result = orchestrator.handle_message(verify_message)
        self.assertEqual(verify_result["status"], "success")
        self.assertFalse(orchestrator.has_blocking_flag())

        if orchestrator.can_release():
            orchestrator.advance(OrchestratorState.COMPLETED)
        self.assertEqual(orchestrator.current_run.state_machine.state, OrchestratorState.COMPLETED)


if __name__ == "__main__":
    unittest.main()
