import unittest

from src.cross_discipline import CrossDisciplineThresholds, CrossDisciplineValidator


class CrossDisciplineThresholdTests(unittest.TestCase):
    def test_permissive_threshold_reduces_blocking_for_marginal_case(self) -> None:
        payload = {
            "electrical": {
                "thd_voltage_percent": 9.0,
                "motor_current_thd_percent": 5.8,
                "power_factor": 0.84,
            },
            "instrumentation": {
                "pfdavg": 0.0012,
                "sil_target": 2,
                "predicted_drift_pct": 1.1,
                "drift_r_squared": 0.35,
            },
            "rotating": {
                "vibration_mm_per_s": 3.2,
                "vibration_limit_mm_per_s": 3.0,
                "nozzle_load_ratio": 0.95,
                "bearing_health_index": 5.5,
                "bearing_temperature_c": 82.0,
            },
            "piping": {
                "current_thickness_mm": 6.0,
                "t_min_mm": 5.1,
                "remaining_life_years": 2.5,
            },
        }

        default_result = CrossDisciplineValidator().evaluate(payload)
        permissive = CrossDisciplineThresholds(
            instrumentation_pfd_high=0.0015,
            instrumentation_drift_high_pct=1.3,
            piping_remaining_life_low_years=2.0,
            piping_margin_low_mm=0.7,
            electrical_current_thd_high_pct=6.0,
            rotating_bearing_temp_high_c=85.0,
        )
        permissive_result = CrossDisciplineValidator(thresholds=permissive).evaluate(payload)

        self.assertEqual(default_result["status"], "blocked")
        self.assertEqual(permissive_result["status"], "ok")

    def test_conservative_threshold_blocks_milder_case(self) -> None:
        payload = {
            "electrical": {
                "thd_voltage_percent": 7.9,
                "motor_current_thd_percent": 4.8,
                "power_factor": 0.87,
            },
            "rotating": {
                "vibration_mm_per_s": 3.5,
                "vibration_limit_mm_per_s": 3.0,
                "nozzle_load_ratio": 0.9,
                "bearing_health_index": 6.0,
                "bearing_temperature_c": 79.0,
            },
        }

        default_result = CrossDisciplineValidator().evaluate(payload)
        conservative = CrossDisciplineThresholds(
            electrical_current_thd_high_pct=4.5,
            rotating_bearing_temp_high_c=78.0,
            electrical_power_factor_low=0.88,
        )
        conservative_result = CrossDisciplineValidator(thresholds=conservative).evaluate(payload)

        self.assertEqual(default_result["status"], "ok")
        self.assertEqual(conservative_result["status"], "blocked")
        self.assertIn("PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK", conservative_result["flags"]["red_flags"])


if __name__ == "__main__":
    unittest.main()

