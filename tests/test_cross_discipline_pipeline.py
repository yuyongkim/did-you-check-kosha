import pathlib
import unittest

from src.agents.runtime_builder import build_mock_runtime
from src.cross_discipline.validator import CrossDisciplineValidator
from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.triple_pipeline import TripleDisciplinePipelineService
from src.shared.config_loader import load_and_validate_config


class CrossDisciplineValidatorTests(unittest.TestCase):
    def test_no_issue_status_ok(self) -> None:
        validator = CrossDisciplineValidator()
        result = validator.evaluate(
            {
                "piping": {"current_thickness_mm": 7.5, "t_min_mm": 5.5, "remaining_life_years": 8.0},
                "vessel": {"current_thickness_mm": 10.0, "t_required_shell_mm": 8.2, "remaining_life_years": 12.0},
                "rotating": {
                    "vibration_mm_per_s": 2.0,
                    "vibration_limit_mm_per_s": 3.0,
                    "nozzle_load_ratio": 0.8,
                    "bearing_health_index": 8.0,
                },
            }
        )

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["flags"]["red_flags"], [])
        self.assertEqual(result["flags"]["warnings"], [])
        self.assertFalse(result["summary"]["blocking"])

    def test_cross_discipline_mismatch_warning(self) -> None:
        validator = CrossDisciplineValidator()
        result = validator.evaluate(
            {
                "piping": {"current_thickness_mm": 9.5, "t_min_mm": 5.0, "remaining_life_years": 10.0},
                "vessel": {"current_thickness_mm": 10.0, "t_required_shell_mm": 9.0, "remaining_life_years": 12.0},
                "rotating": {
                    "vibration_mm_per_s": 2.0,
                    "vibration_limit_mm_per_s": 3.0,
                    "nozzle_load_ratio": 0.7,
                    "bearing_health_index": 8.5,
                },
            }
        )

        self.assertEqual(result["status"], "ok")
        self.assertIn("LOG.CROSS_DISCIPLINE_MISMATCH", result["flags"]["warnings"])
        self.assertFalse(result["summary"]["blocking"])

    def test_electrical_instrumentation_coupling_risk(self) -> None:
        validator = CrossDisciplineValidator()
        result = validator.evaluate(
            {
                "electrical": {
                    "thd_voltage_percent": 9.2,
                    "motor_current_thd_percent": 7.0,
                    "power_factor": 0.82,
                },
                "instrumentation": {
                    "pfdavg": 0.002,
                    "sil_target": 2,
                    "predicted_drift_pct": 1.2,
                    "drift_r_squared": 0.45,
                },
                "rotating": {
                    "vibration_mm_per_s": 4.2,
                    "vibration_limit_mm_per_s": 3.0,
                    "nozzle_load_ratio": 0.9,
                    "bearing_health_index": 5.2,
                    "bearing_temperature_c": 84.0,
                },
            }
        )

        self.assertEqual(result["status"], "blocked")
        self.assertIn("PHY.ELECTRICAL_NOISE_TO_SIS_RISK", result["flags"]["red_flags"])
        self.assertIn("PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK", result["flags"]["red_flags"])

    def test_interface_overload_flag(self) -> None:
        validator = CrossDisciplineValidator()
        result = validator.evaluate(
            {
                "piping": {"current_thickness_mm": 4.0, "t_min_mm": 3.9, "remaining_life_years": 1.5},
                "vessel": {"current_thickness_mm": 8.0, "t_required_shell_mm": 8.5, "remaining_life_years": 1.2},
                "rotating": {
                    "vibration_mm_per_s": 5.5,
                    "vibration_limit_mm_per_s": 3.0,
                    "nozzle_load_ratio": 1.25,
                    "bearing_health_index": 3.0,
                },
            }
        )

        self.assertEqual(result["status"], "blocked")
        self.assertIn("PHY.NOZZLE_INTERFACE_OVERLOAD", result["flags"]["red_flags"])

    def test_structure_coupling_risks(self) -> None:
        validator = CrossDisciplineValidator()
        result = validator.evaluate(
            {
                "piping": {
                    "current_thickness_mm": 5.4,
                    "t_min_mm": 4.9,
                    "remaining_life_years": 2.1,
                    "nps_inch": 10.0,
                },
                "rotating": {
                    "vibration_mm_per_s": 5.2,
                    "vibration_limit_mm_per_s": 3.0,
                    "nozzle_load_ratio": 1.05,
                    "bearing_health_index": 4.2,
                    "bearing_temperature_c": 82.0,
                },
                "electrical": {
                    "thd_voltage_percent": 9.1,
                    "motor_current_thd_percent": 6.1,
                    "power_factor": 0.84,
                },
                "instrumentation": {
                    "pfdavg": 0.0015,
                    "sil_target": 2,
                    "predicted_drift_pct": 1.0,
                    "drift_r_squared": 0.42,
                },
                "steel": {
                    "dc_ratio": 0.96,
                    "deflection_ratio": 1.08,
                    "corrosion_loss_percent": 33.0,
                },
                "civil": {
                    "foundation_settlement_mm": 31.0,
                    "crack_width_mm": 0.48,
                    "spalling_area_percent": 24.0,
                },
            }
        )
        self.assertEqual(result["status"], "blocked")
        self.assertIn("PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK", result["flags"]["red_flags"])
        self.assertIn("PHY.FOUNDATION_TO_ROTATING_MISALIGNMENT_RISK", result["flags"]["red_flags"])
        self.assertIn("PHY.STRUCTURE_TO_SIS_RELIABILITY_RISK", result["flags"]["red_flags"])


class TriplePipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        config, errors = load_and_validate_config(pathlib.Path("configs/sample_config.json"))
        assert not errors, errors
        runtime = build_mock_runtime(config)
        self.service = TripleDisciplinePipelineService(Orchestrator(runtime=runtime))

    def test_nominal_triple_pipeline(self) -> None:
        result = self.service.run(
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

        self.assertEqual(result.status, "completed")
        self.assertFalse(result.blocking_flags)

    def test_triple_pipeline_blocked_when_discipline_flags_exist(self) -> None:
        result = self.service.run(
            piping_input={
                "material": "SA-106 Gr.B",
                "nps": 6.0,
                "design_pressure_mpa": 4.5,
                "design_temperature_c": 250.0,
                "thickness_history": [
                    {"date": "2015-01-01", "thickness_mm": 9.0},
                    {"date": "2020-01-01", "thickness_mm": 6.1},
                    {"date": "2025-01-01", "thickness_mm": 4.3},
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
                "t_current_mm": 12.0,
                "corrosion_allowance_mm": 1.5,
                "assumed_corrosion_rate_mm_per_year": 0.3,
            },
            rotating_input={
                "machine_type": "pump",
                "vibration_mm_per_s": 5.1,
                "nozzle_load_ratio": 1.2,
                "bearing_temperature_c": 84.0,
                "speed_rpm": 1800,
            },
        )

        self.assertEqual(result.status, "blocked")
        self.assertTrue(result.blocking_flags)
        self.assertEqual(result.cross_discipline["status"], "blocked")
        self.assertIn("PHY.NOZZLE_INTERFACE_OVERLOAD", result.cross_discipline["flags"]["red_flags"])


if __name__ == "__main__":
    unittest.main()
