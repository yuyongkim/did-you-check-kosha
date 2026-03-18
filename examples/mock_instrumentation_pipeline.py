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
            to_agent="instrumentation_specialist",
            payload={
                "calculation_type": "instrumentation_integrity",
                "input_data": {
                    "sil_target": 2,
                    "failure_rate_per_hour": 1.0e-7,
                    "proof_test_interval_hours": 8760.0,
                    "mttr_hours": 8.0,
                    "calibration_interval_days": 180.0,
                    "calibration_history": [
                        {"days_since_ref": 0.0, "error_pct": 0.05},
                        {"days_since_ref": 90.0, "error_pct": 0.16},
                        {"days_since_ref": 180.0, "error_pct": 0.28},
                        {"days_since_ref": 270.0, "error_pct": 0.39},
                    ],
                    "tolerance_pct": 1.0,
                    "sensor_mtbf_years": 8.0,
                    "cv_required": 45.0,
                    "cv_rated": 80.0,
                    "uncertainty_components_pct": [0.2, 0.3, 0.1],
                },
            },
            meta={"workflow_id": "standard_calculation", "discipline": "instrumentation"},
        )
    )

    print("status:", result.get("status"))
    print("discipline:", result.get("discipline"))
    print("pfdavg:", result.get("results", {}).get("pfdavg"))
    print("sil_achieved:", result.get("results", {}).get("sil_achieved"))


if __name__ == "__main__":
    main()

