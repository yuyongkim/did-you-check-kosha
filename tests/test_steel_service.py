import unittest

from src.steel.service import SteelVerificationService


class SteelServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = SteelVerificationService()

    def test_nominal_steel_case(self) -> None:
        payload = {
            "member_type": "column",
            "section_label": "W310x60",
            "length_m": 6.0,
            "k_factor": 1.0,
            "radius_of_gyration_mm": 90.0,
            "yield_strength_mpa": 345.0,
            "elasticity_mpa": 200000.0,
            "gross_area_mm2": 7600.0,
            "corrosion_loss_percent": 8.0,
            "axial_demand_kn": 650.0,
            "moment_demand_knm": 90.0,
            "deflection_mm": 10.0,
            "span_mm": 6000.0,
            "connection_failure_detected": False,
        }
        result = self.service.evaluate(payload)
        self.assertIn("final_results", result)
        self.assertIn("dc_ratio", result["final_results"])
        self.assertFalse(result["flags"]["red_flags"])

    def test_steel_failure_flags(self) -> None:
        payload = {
            "member_type": "column",
            "section_label": "W250x33",
            "length_m": 8.5,
            "k_factor": 1.2,
            "radius_of_gyration_mm": 42.0,
            "yield_strength_mpa": 250.0,
            "elasticity_mpa": 200000.0,
            "gross_area_mm2": 4200.0,
            "corrosion_loss_percent": 55.0,
            "axial_demand_kn": 1850.0,
            "moment_demand_knm": 220.0,
            "deflection_mm": 45.0,
            "span_mm": 7000.0,
            "connection_failure_detected": True,
        }
        result = self.service.evaluate(payload)
        self.assertIn("PHY.STRUCTURAL_DC_CRITICAL", result["flags"]["red_flags"])
        self.assertIn("PHY.STEEL_CORROSION_SECTION_LOSS_HIGH", result["flags"]["red_flags"])
        self.assertIn("PHY.STEEL_DEFLECTION_EXCEEDED", result["flags"]["red_flags"])
        self.assertIn("PHY.CONNECTION_FAILURE_DETECTED", result["flags"]["red_flags"])

    def test_expanded_member_type_supported(self) -> None:
        payload = {
            "member_type": "truss_member",
            "steel_grade": "a992",
            "section_label": "HSS200x200x8",
            "length_m": 5.5,
            "k_factor": 1.0,
            "radius_of_gyration_mm": 55.0,
            "yield_strength_mpa": 345.0,
            "elasticity_mpa": 200000.0,
            "gross_area_mm2": 5200.0,
            "corrosion_loss_percent": 6.0,
            "axial_demand_kn": 420.0,
            "moment_demand_knm": 35.0,
            "deflection_mm": 8.0,
            "span_mm": 5500.0,
            "connection_failure_detected": False,
        }
        result = self.service.evaluate(payload)
        self.assertIn("final_results", result)
        self.assertIn("dc_ratio", result["final_results"])


    def test_reinforcement_and_connection_screening(self) -> None:
        payload = {
            "member_type": "column",
            "length_m": 4.0,
            "radius_of_gyration_mm": 50.0,
            "yield_strength_mpa": 345.0,
            "gross_area_mm2": 5000.0,
            "axial_demand_kn": 200.0,
            "corrosion_loss_percent": 5.0,
        }
        result = self.service.evaluate(payload)
        fr = result["final_results"]
        self.assertIn("reinforcement_need", fr)
        self.assertIn("connection_status", fr)


if __name__ == "__main__":
    unittest.main()
