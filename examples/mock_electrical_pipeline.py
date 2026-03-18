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
    result = orchestrator.handle_message(
        create_message(
            message_type="calculation_request",
            from_agent="orchestrator",
            to_agent="electrical_specialist",
            payload={
                "calculation_type": "electrical_integrity",
                "input_data": {
                    "system_voltage_kv": 13.8,
                    "bolted_fault_current_ka": 22.0,
                    "clearing_time_sec": 0.2,
                    "working_distance_mm": 455.0,
                    "breaker_interrupt_rating_ka": 31.5,
                    "voltage_drop_percent": 3.2,
                    "thd_voltage_percent": 4.8,
                    "dga_score": 8.2,
                    "oil_quality_score": 7.9,
                    "insulation_score": 8.3,
                    "load_factor_score": 7.5,
                    "motor_current_thd_percent": 4.5,
                    "power_factor": 0.91,
                },
            },
            meta={"workflow_id": "standard_calculation", "discipline": "electrical"},
        )
    )

    print("status:", result.get("status"))
    print("discipline:", result.get("discipline"))
    print("health_index:", result.get("results", {}).get("transformer_health_index"))
    print("arc_flash_energy_cal_cm2:", result.get("results", {}).get("arc_flash_energy_cal_cm2"))


if __name__ == "__main__":
    main()

