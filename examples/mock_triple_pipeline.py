from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.agents.runtime_builder import build_mock_runtime
from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.triple_pipeline import TripleDisciplinePipelineService
from src.shared.config_loader import load_and_validate_config


def main() -> None:
    config, errors = load_and_validate_config(ROOT / "configs" / "sample_config.json")
    if errors:
        print("CONFIG_INVALID", errors)
        return

    service = TripleDisciplinePipelineService(Orchestrator(runtime=build_mock_runtime(config)))
    result = service.run(
        piping_input={
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
        vessel_input={
            "material": "SA-516-70",
            "design_pressure_mpa": 2.0,
            "design_temperature_c": 200.0,
            "inside_radius_mm": 750.0,
            "joint_efficiency": 0.85,
            "t_current_mm": 18.0,
            "corrosion_allowance_mm": 1.5,
            "assumed_corrosion_rate_mm_per_year": 0.2,
        },
        rotating_input={
            "machine_type": "pump",
            "vibration_mm_per_s": 2.5,
            "nozzle_load_ratio": 0.85,
            "bearing_temperature_c": 72.0,
            "speed_rpm": 1800,
        },
    )

    print("status:", result.status)
    print("state:", result.state)
    print("cross_status:", result.cross_discipline.get("status"))
    print("cross_red_flags:", result.cross_discipline.get("flags", {}).get("red_flags"))


if __name__ == "__main__":
    main()
