from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.agents.runtime_builder import build_mock_runtime
from src.orchestrator.orchestrator import Orchestrator
from src.shared.config_loader import load_and_validate_config
from src.shared.message_factory import create_message


def main() -> None:
    config, errors = load_and_validate_config(ROOT / "configs" / "sample_config.json")
    if errors:
        print("CONFIG_INVALID", errors)
        return

    orchestrator = Orchestrator(runtime=build_mock_runtime(config))
    message = create_message(
        message_type="calculation_request",
        from_agent="orchestrator",
        to_agent="rotating_specialist",
        payload={
            "calculation_type": "rotating_integrity",
            "input_data": {
                "machine_type": "pump",
                "vibration_mm_per_s": 2.5,
                "nozzle_load_ratio": 0.85,
                "bearing_temperature_c": 72.0,
                "speed_rpm": 1800,
            },
        },
        meta={"workflow_id": "standard_calculation", "discipline": "rotating"},
    )

    result = orchestrator.handle_message(message)
    print("status:", result.get("status"))
    print("discipline:", result.get("discipline"))
    print("bearing_health_index:", result.get("results", {}).get("bearing_health_index"))
    print("red_flags:", result.get("flags", {}).get("red_flags"))


if __name__ == "__main__":
    main()
