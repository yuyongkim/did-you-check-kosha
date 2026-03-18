import unittest

from src.instrumentation.service import InstrumentationVerificationService


class InstrumentationServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = InstrumentationVerificationService()

    def test_nominal_instrumentation_case(self) -> None:
        payload = {
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
        }
        result = self.service.evaluate(payload)
        self.assertIn("final_results", result)
        self.assertIn("pfdavg", result["final_results"])
        self.assertIn("predicted_drift_pct", result["final_results"])
        self.assertFalse(result["flags"]["red_flags"])

    def test_instrumentation_failure_flags(self) -> None:
        payload = {
            "sil_target": 2,
            "failure_rate_per_hour": 1.0e-5,
            "proof_test_interval_hours": 8760.0,
            "mttr_hours": 12.0,
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
        }
        result = self.service.evaluate(payload)
        self.assertIn("PHY.SIL_TARGET_NOT_MET", result["flags"]["red_flags"])
        self.assertIn("PHY.DRIFT_RATE_EXCEEDED", result["flags"]["red_flags"])
        self.assertIn("PHY.CONTROL_VALVE_CAPACITY_LOW", result["flags"]["red_flags"])
        self.assertIn("PHY.SENSOR_MTBF_LOW", result["flags"]["warnings"])


    def test_proof_test_and_calibration_health(self) -> None:
        payload = {
            "sil_target": 2,
            "failure_rate_per_hour": 1e-6,
            "proof_test_interval_hours": 8760,
            "mttr_hours": 8.0,
            "calibration_interval_days": 180,
            "calibration_history": [
                {"days_since_ref": 0, "error_pct": 0.1},
                {"days_since_ref": 90, "error_pct": 0.3},
                {"days_since_ref": 180, "error_pct": 0.5},
            ],
            "tolerance_pct": 1.0,
            "sensor_mtbf_years": 10.0,
            "cv_required": 50.0,
            "cv_rated": 80.0,
            "uncertainty_components_pct": [0.2, 0.3, 0.1],
        }
        result = self.service.evaluate(payload)
        fr = result["final_results"]
        self.assertIn("proof_test_adequacy", fr)
        self.assertIn("calibration_health", fr)


if __name__ == "__main__":
    unittest.main()

