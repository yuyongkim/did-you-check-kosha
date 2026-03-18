from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.agents.runtime_builder import build_mock_runtime
from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.pipeline import PipelineService
from src.shared.config_loader import load_and_validate_config


def main() -> None:
    config, errors = load_and_validate_config(ROOT / "configs" / "sample_config.json")
    if errors:
        print("CONFIG_INVALID")
        for error in errors:
            print("-", error)
        return

    orchestrator = Orchestrator(runtime=build_mock_runtime(config))
    service = PipelineService(orchestrator)
    result = service.run_standard_pipeline(
        discipline_agent="piping_specialist",
        calculation_type="remaining_life",
        input_data={
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
    )

    print("status:", result.status)
    print("workflow_id:", result.workflow_id)
    print("state:", result.state)
    print("calc_status:", result.calculation.get("status"))
    print("verify_status:", result.verification.get("status"))
    print("blocking_flags:", result.blocking_flags)


if __name__ == "__main__":
    main()
