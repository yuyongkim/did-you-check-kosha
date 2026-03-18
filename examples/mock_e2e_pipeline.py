from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.agents.runtime_builder import build_mock_runtime
from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.state_machine import OrchestratorState
from src.shared.config_loader import load_and_validate_config
from src.shared.message_factory import create_message
from src.workflows.runner import WorkflowRunner


def main() -> None:
    config, errors = load_and_validate_config(ROOT / "configs" / "sample_config.json")
    if errors:
        print("CONFIG_INVALID")
        for error in errors:
            print("-", error)
        return

    runtime = build_mock_runtime(config)
    orchestrator = Orchestrator(runtime=runtime)
    run = orchestrator.start_run("standard_calculation")
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
        correlation_id=run.trace.correlation_id,
        trace_id=run.trace.trace_id,
        meta={"workflow_id": "standard_calculation", "discipline": "piping"},
    )
    calc_result = orchestrator.handle_message(calc_message)

    verify_message = create_message(
        message_type="verification_request",
        from_agent="orchestrator",
        to_agent="verification_agent",
        payload={
            "verification_type": "maker_voting",
            "inputs": calc_message["payload"]["input_data"],
            "results": calc_result["results"],
        },
        correlation_id=run.trace.correlation_id,
        trace_id=run.trace.trace_id,
        meta={"workflow_id": "standard_calculation"},
    )
    verify_result = orchestrator.handle_message(verify_message)

    if orchestrator.can_release():
        orchestrator.advance(OrchestratorState.COMPLETED)

    print("workflow_id:", run.trace.workflow_id)
    print("state:", run.state_machine.state.value)
    print("calc_status:", calc_result["status"])
    print("verify_status:", verify_result["status"])
    print("blocking_flags:", orchestrator.has_blocking_flag())


if __name__ == "__main__":
    main()
