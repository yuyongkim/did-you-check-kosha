import pathlib
import unittest

from src.agents.runtime_builder import build_mock_runtime
from src.orchestrator.five_pipeline import FiveDisciplinePipelineService
from src.orchestrator.orchestrator import Orchestrator
from src.shared.config_loader import load_and_validate_config


class FivePipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        config, errors = load_and_validate_config(pathlib.Path("configs/sample_config.json"))
        assert not errors, errors
        runtime = build_mock_runtime(config)
        self.service = FiveDisciplinePipelineService(Orchestrator(runtime=runtime))

    def test_nominal_five_pipeline(self) -> None:
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
            electrical_input={
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
            instrumentation_input={
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
        )

        self.assertEqual(result.status, "completed")
        self.assertFalse(result.blocking_flags)

    def test_five_pipeline_blocked_for_ei_coupling(self) -> None:
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
            electrical_input={
                "system_voltage_kv": 13.8,
                "bolted_fault_current_ka": 40.0,
                "clearing_time_sec": 0.25,
                "working_distance_mm": 455.0,
                "breaker_interrupt_rating_ka": 31.5,
                "voltage_drop_percent": 6.0,
                "thd_voltage_percent": 9.2,
                "dga_score": 5.5,
                "oil_quality_score": 5.2,
                "insulation_score": 5.0,
                "load_factor_score": 5.1,
                "motor_current_thd_percent": 7.0,
                "power_factor": 0.82,
            },
            instrumentation_input={
                "sil_target": 2,
                "failure_rate_per_hour": 1.0e-6,
                "proof_test_interval_hours": 8760.0,
                "mttr_hours": 8.0,
                "calibration_interval_days": 180.0,
                "calibration_history": [
                    {"days_since_ref": 0.0, "error_pct": 0.10},
                    {"days_since_ref": 90.0, "error_pct": 1.10},
                    {"days_since_ref": 180.0, "error_pct": 2.15},
                    {"days_since_ref": 270.0, "error_pct": 3.20},
                ],
                "tolerance_pct": 1.0,
                "sensor_mtbf_years": 3.0,
                "cv_required": 95.0,
                "cv_rated": 100.0,
                "uncertainty_components_pct": [0.4, 0.5, 0.2],
            },
        )

        self.assertEqual(result.status, "blocked")
        self.assertTrue(result.blocking_flags)
        self.assertEqual(result.cross_discipline["status"], "blocked")
        self.assertIn("PHY.ELECTRICAL_NOISE_TO_SIS_RISK", result.cross_discipline["flags"]["red_flags"])


if __name__ == "__main__":
    unittest.main()

