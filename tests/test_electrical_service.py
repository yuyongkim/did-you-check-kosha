import unittest

from src.electrical.service import ElectricalVerificationService


class ElectricalServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = ElectricalVerificationService()

    def test_nominal_electrical_case(self) -> None:
        payload = {
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
        }
        result = self.service.evaluate(payload)
        self.assertIn("final_results", result)
        self.assertIn("transformer_health_index", result["final_results"])
        self.assertIn("arc_flash_energy_cal_cm2", result["final_results"])
        self.assertFalse(result["flags"]["red_flags"])

    def test_critical_electrical_flags(self) -> None:
        payload = {
            "system_voltage_kv": 13.8,
            "bolted_fault_current_ka": 75.0,
            "clearing_time_sec": 0.8,
            "working_distance_mm": 455.0,
            "breaker_interrupt_rating_ka": 31.5,
            "voltage_drop_percent": 6.8,
            "thd_voltage_percent": 10.5,
            "dga_score": 2.0,
            "oil_quality_score": 2.5,
            "insulation_score": 2.2,
            "load_factor_score": 2.0,
            "motor_current_thd_percent": 9.2,
            "power_factor": 0.78,
        }
        result = self.service.evaluate(payload)
        self.assertIn("PHY.TRANSFORMER_HEALTH_CRITICAL", result["flags"]["red_flags"])
        self.assertIn("PHY.ARC_FLASH_ENERGY_EXCEEDED", result["flags"]["red_flags"])
        self.assertIn("PHY.BREAKER_INTERRUPT_RATING_EXCEEDED", result["flags"]["red_flags"])


    def test_coordination_margin_present(self) -> None:
        payload = {
            "system_voltage_kv": 4.16,
            "bolted_fault_current_ka": 20.0,
            "clearing_time_sec": 0.5,
            "working_distance_mm": 610.0,
            "breaker_interrupt_rating_ka": 25.0,
            "voltage_drop_percent": 3.0,
            "thd_voltage_percent": 4.0,
            "dga_score": 7.0,
            "oil_quality_score": 7.0,
            "insulation_score": 6.0,
            "load_factor_score": 6.0,
        }
        result = self.service.evaluate(payload)
        fr = result["final_results"]
        self.assertIn("breaker_coordination_margin", fr)
        self.assertIn("load_utilization", fr)
        self.assertGreater(fr["breaker_coordination_margin"], 1.0)


if __name__ == "__main__":
    unittest.main()
