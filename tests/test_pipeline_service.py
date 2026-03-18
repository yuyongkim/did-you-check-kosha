import pathlib
import unittest

from src.agents.runtime_builder import build_mock_runtime
from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.pipeline import PipelineService
from src.shared.config_loader import load_and_validate_config


class PipelineServiceTests(unittest.TestCase):
    def test_run_standard_pipeline_completes(self) -> None:
        config, errors = load_and_validate_config(pathlib.Path("configs/sample_config.json"))
        self.assertEqual(errors, [])
        runtime = build_mock_runtime(config)

        orchestrator = Orchestrator(runtime=runtime)
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

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.state, "completed")
        self.assertFalse(result.blocking_flags)
        self.assertEqual(result.calculation["status"], "success")
        self.assertEqual(result.verification["status"], "success")


if __name__ == "__main__":
    unittest.main()
