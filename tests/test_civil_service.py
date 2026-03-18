import unittest

from src.civil.service import CivilVerificationService


class CivilServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = CivilVerificationService()

    def test_nominal_civil_case(self) -> None:
        payload = {
            "element_type": "beam",
            "fc_mpa": 35.0,
            "fy_mpa": 420.0,
            "width_mm": 300.0,
            "effective_depth_mm": 550.0,
            "rebar_area_mm2": 2450.0,
            "demand_moment_knm": 280.0,
            "lateral_capacity_loss_percent": 8.0,
            "affected_area_percent": 12.0,
            "vertical_capacity_loss_percent": 6.0,
            "carbonation_coeff_mm_sqrt_year": 1.8,
            "service_years": 18.0,
            "cover_thickness_mm": 40.0,
            "crack_width_mm": 0.22,
            "spalling_area_percent": 5.0,
            "foundation_settlement_mm": 8.0,
        }
        result = self.service.evaluate(payload)
        self.assertIn("final_results", result)
        self.assertIn("dc_ratio", result["final_results"])
        self.assertFalse(result["flags"]["red_flags"])

    def test_civil_failure_flags(self) -> None:
        payload = {
            "element_type": "foundation",
            "fc_mpa": 24.0,
            "fy_mpa": 420.0,
            "width_mm": 350.0,
            "effective_depth_mm": 620.0,
            "rebar_area_mm2": 2200.0,
            "demand_moment_knm": 620.0,
            "lateral_capacity_loss_percent": 36.0,
            "affected_area_percent": 35.0,
            "vertical_capacity_loss_percent": 24.0,
            "carbonation_coeff_mm_sqrt_year": 4.2,
            "service_years": 28.0,
            "cover_thickness_mm": 20.0,
            "crack_width_mm": 0.55,
            "spalling_area_percent": 26.0,
            "foundation_settlement_mm": 34.0,
        }
        result = self.service.evaluate(payload)
        self.assertIn("PHY.CIVIL_SUBSTANTIAL_DAMAGE", result["flags"]["red_flags"])
        self.assertIn("PHY.CIVIL_CARBONATION_CORROSION_INITIATED", result["flags"]["red_flags"])
        self.assertIn("PHY.CIVIL_CRACK_WIDTH_EXCEEDED", result["flags"]["red_flags"])
        self.assertIn("PHY.CIVIL_SPALLING_SEVERE", result["flags"]["red_flags"])
        self.assertIn("PHY.CIVIL_FOUNDATION_SETTLEMENT_HIGH", result["flags"]["red_flags"])

    def test_expanded_element_type_supported(self) -> None:
        payload = {
            "element_type": "retaining_wall",
            "environment_exposure": "coastal_marine",
            "fc_mpa": 32.0,
            "fy_mpa": 420.0,
            "width_mm": 400.0,
            "effective_depth_mm": 700.0,
            "rebar_area_mm2": 3200.0,
            "demand_moment_knm": 260.0,
            "lateral_capacity_loss_percent": 10.0,
            "affected_area_percent": 8.0,
            "vertical_capacity_loss_percent": 5.0,
            "carbonation_coeff_mm_sqrt_year": 2.1,
            "service_years": 20.0,
            "cover_thickness_mm": 50.0,
            "crack_width_mm": 0.2,
            "spalling_area_percent": 4.0,
            "foundation_settlement_mm": 6.0,
        }
        result = self.service.evaluate(payload)
        self.assertIn("final_results", result)
        self.assertIn("dc_ratio", result["final_results"])


    def test_repair_priority_and_consequence(self) -> None:
        payload = {
            "fc_mpa": 30.0,
            "width_mm": 300.0,
            "effective_depth_mm": 450.0,
            "rebar_area_mm2": 1200.0,
            "demand_moment_knm": 80.0,
            "service_years": 25.0,
            "cover_thickness_mm": 40.0,
        }
        result = self.service.evaluate(payload)
        fr = result["final_results"]
        self.assertIn("repair_priority", fr)
        self.assertIn("consequence_category", fr)


if __name__ == "__main__":
    unittest.main()
