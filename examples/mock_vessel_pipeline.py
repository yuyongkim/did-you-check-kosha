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
        to_agent="static_equipment_specialist",
        payload={
            "calculation_type": "vessel_integrity",
            "input_data": {
                "material": "SA-516-70",
                "design_pressure_mpa": 2.0,
                "design_temperature_c": 200.0,
                "inside_radius_mm": 750.0,
                "joint_efficiency": 0.85,
                "t_current_mm": 18.0,
                "corrosion_allowance_mm": 1.5,
                "assumed_corrosion_rate_mm_per_year": 0.2,
            },
        },
        meta={"workflow_id": "standard_calculation", "discipline": "vessel"},
    )

    result = orchestrator.handle_message(message)
    print("status:", result.get("status"))
    print("discipline:", result.get("discipline"))
    print("t_required_shell_mm:", result.get("results", {}).get("t_required_shell_mm"))
    print("red_flags:", result.get("flags", {}).get("red_flags"))


if __name__ == "__main__":
    main()
