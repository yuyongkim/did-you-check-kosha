import unittest

from src.rotating.service import RotatingVerificationService


class RotatingServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = RotatingVerificationService()

    def test_nominal_rotating_case(self) -> None:
        payload = {
            "machine_type": "pump",
            "vibration_mm_per_s": 2.5,
            "nozzle_load_ratio": 0.85,
            "bearing_temperature_c": 72.0,
            "speed_rpm": 1800,
        }
        result = self.service.evaluate(payload)
        self.assertIn("final_results", result)
        self.assertEqual(result["final_results"]["status"], "NORMAL")

    def test_rotating_critical_flags(self) -> None:
        payload = {
            "machine_type": "pump",
            "vibration_mm_per_s": 5.5,
            "nozzle_load_ratio": 1.2,
            "bearing_temperature_c": 90.0,
            "speed_rpm": 1800,
        }
        result = self.service.evaluate(payload)
        self.assertIn("PHY.VIBRATION_LIMIT_EXCEEDED", result["flags"]["red_flags"])
        self.assertIn("PHY.NOZZLE_LOAD_EXCEEDED", result["flags"]["red_flags"])

    def test_expanded_machine_type_supported(self) -> None:
        payload = {
            "machine_type": "fan",
            "vibration_mm_per_s": 3.8,
            "nozzle_load_ratio": 0.9,
            "bearing_temperature_c": 68.0,
            "speed_rpm": 1450,
        }
        result = self.service.evaluate(payload)
        self.assertIn("final_results", result)
        self.assertEqual(result["final_results"]["status"], "NORMAL")

    def test_steam_turbine_requires_steam_state_context(self) -> None:
        payload = {
            "machine_type": "steam_turbine",
            "vibration_mm_per_s": 3.2,
            "nozzle_load_ratio": 0.8,
            "bearing_temperature_c": 70.0,
            "speed_rpm": 3600,
            "steam_pressure_bar": 80.0,
        }
        result = self.service.evaluate(payload)
        self.assertIn("STD.STEAM_TABLE_LOOKUP_REQUIRED", result["flags"]["red_flags"])

    def test_steam_turbine_wetness_risk_flag(self) -> None:
        payload = {
            "machine_type": "steam_turbine",
            "vibration_mm_per_s": 3.6,
            "nozzle_load_ratio": 0.92,
            "bearing_temperature_c": 73.0,
            "speed_rpm": 3600,
            "steam_pressure_bar": 80.0,
            "steam_temperature_c": 296.0,
            "steam_quality_x": 0.84,
            "inlet_enthalpy_kj_per_kg": 3300.0,
            "outlet_enthalpy_kj_per_kg": 2850.0,
        }
        result = self.service.evaluate(payload)
        self.assertIn("PHY.STEAM_WETNESS_EROSION_RISK", result["flags"]["red_flags"])


    def test_monitoring_escalation_present(self) -> None:
        payload = {
            "machine_type": "pump",
            "vibration_mm_per_s": 3.0,
            "nozzle_load_ratio": 0.5,
            "bearing_temperature_c": 55.0,
            "speed_rpm": 3000,
        }
        result = self.service.evaluate(payload)
        fr = result["final_results"]
        self.assertIn("monitoring_escalation", fr)
        self.assertIn("maintenance_urgency", fr)


if __name__ == "__main__":
    unittest.main()
