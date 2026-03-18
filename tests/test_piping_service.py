import unittest

from src.piping.service import PipingVerificationService


class PipingServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = PipingVerificationService()

    def test_nominal_case_passes_without_red_flags(self) -> None:
        payload = {
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
        }
        result = self.service.evaluate(payload)
        self.assertIn("final_results", result)
        self.assertAlmostEqual(result["final_results"]["cr_selected_mm_per_year"], 0.28, delta=0.05)
        self.assertFalse(result["flags"]["red_flags"])

    def test_current_thickness_below_minimum_triggers_flag(self) -> None:
        payload = {
            "material": "SA-106 Gr.B",
            "nps": 12.0,
            "design_pressure_mpa": 20.0,
            "design_temperature_c": 300.0,
            "thickness_history": [
                {"date": "2015-01-01", "thickness_mm": 6.5},
                {"date": "2020-01-01", "thickness_mm": 5.5},
                {"date": "2025-01-01", "thickness_mm": 4.4},
            ],
            "corrosion_allowance_mm": 1.5,
            "weld_type": "smaw",
            "service_type": "general",
            "has_internal_coating": False,
        }
        result = self.service.evaluate(payload)
        self.assertIn("PHY.CURRENT_THICKNESS_BELOW_MINIMUM", result["flags"]["red_flags"])

    def test_negative_corrosion_without_coating_triggers_flag(self) -> None:
        payload = {
            "material": "SA-106 Gr.B",
            "nps": 6.0,
            "design_pressure_mpa": 4.0,
            "design_temperature_c": 200.0,
            "thickness_history": [
                {"date": "2015-01-01", "thickness_mm": 8.0},
                {"date": "2020-01-01", "thickness_mm": 8.6},
                {"date": "2025-01-01", "thickness_mm": 9.1},
            ],
            "corrosion_allowance_mm": 1.5,
            "weld_type": "erw",
            "service_type": "general",
            "has_internal_coating": False,
        }
        result = self.service.evaluate(payload)
        self.assertIn("PHY.UNREALISTIC_CORROSION_RATE", result["flags"]["red_flags"])

    def test_low_alloy_material_is_supported(self) -> None:
        payload = {
            "material": "SA-335 P22",
            "nps": 6.0,
            "design_pressure_mpa": 4.5,
            "design_temperature_c": 350.0,
            "thickness_history": [
                {"date": "2015-01-01", "thickness_mm": 10.0},
                {"date": "2020-01-01", "thickness_mm": 8.9},
                {"date": "2025-01-01", "thickness_mm": 7.9},
            ],
            "corrosion_allowance_mm": 1.5,
            "weld_type": "seamless",
            "service_type": "general",
            "has_internal_coating": False,
            "chloride_ppm": 100,
        }
        result = self.service.evaluate(payload)
        self.assertNotIn("STD.UNAPPROVED_MATERIAL", result["flags"]["red_flags"])
        self.assertNotIn("STD.UNAPPROVED_MATERIAL", result["flags"]["warnings"])
        self.assertIn("t_min_mm", result["final_results"])

    def test_high_temp_cs_strict_profile_blocks(self) -> None:
        payload = {
            "material": "SA-106 Gr.B",
            "nps": 6.0,
            "design_pressure_mpa": 4.0,
            "design_temperature_c": 500.0,
            "temperature_profile": "strict_process",
            "thickness_history": [
                {"date": "2015-01-01", "thickness_mm": 10.0},
                {"date": "2020-01-01", "thickness_mm": 8.8},
                {"date": "2025-01-01", "thickness_mm": 7.6},
            ],
            "corrosion_allowance_mm": 1.5,
            "weld_type": "seamless",
            "service_type": "high_temp",
            "fluid_type": "steam_condensate",
            "has_internal_coating": False,
        }
        result = self.service.evaluate(payload)
        self.assertIn("PHY.TEMPERATURE_LIMIT_EXCEEDED", result["flags"]["red_flags"])

    def test_high_temp_cs_legacy_profile_warns_not_blocks(self) -> None:
        payload = {
            "material": "SA-106 Gr.B",
            "nps": 6.0,
            "design_pressure_mpa": 4.0,
            "design_temperature_c": 500.0,
            "temperature_profile": "legacy_power_steam",
            "thickness_history": [
                {"date": "2015-01-01", "thickness_mm": 10.0},
                {"date": "2020-01-01", "thickness_mm": 8.8},
                {"date": "2025-01-01", "thickness_mm": 7.6},
            ],
            "corrosion_allowance_mm": 1.5,
            "weld_type": "seamless",
            "service_type": "high_temp",
            "fluid_type": "steam_condensate",
            "has_internal_coating": False,
        }
        result = self.service.evaluate(payload)
        self.assertNotIn("PHY.TEMPERATURE_LIMIT_EXCEEDED", result["flags"]["red_flags"])
        self.assertIn("STD.TEMPERATURE_OVERRIDE_REVIEW_REQUIRED", result["flags"]["warnings"])
        self.assertEqual(result["final_results"]["temperature_profile"], "legacy_power_steam")


    def test_screening_outputs_present_in_results(self) -> None:
        payload = {
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
        }
        result = self.service.evaluate(payload)
        fr = result["final_results"]
        self.assertIn("hoop_stress_screening_mpa", fr)
        self.assertIn("hydrotest_pressure_mpa", fr)
        self.assertIn("hoop_stress_ratio", fr)
        self.assertGreater(fr["hoop_stress_screening_mpa"], 0)
        self.assertAlmostEqual(fr["hydrotest_pressure_mpa"], 4.5 * 1.5, places=2)
        self.assertGreater(fr["hoop_stress_ratio"], 0)
        self.assertLess(fr["hoop_stress_ratio"], 2.0)  # Should be reasonable


if __name__ == "__main__":
    unittest.main()
