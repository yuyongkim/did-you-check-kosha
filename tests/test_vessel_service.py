import unittest

from src.vessel.service import VesselVerificationService


class VesselServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = VesselVerificationService()

    def test_nominal_vessel_case(self) -> None:
        payload = {
            "material": "SA-516-70",
            "design_pressure_mpa": 2.0,
            "design_temperature_c": 200.0,
            "inside_radius_mm": 750.0,
            "joint_efficiency": 0.85,
            "t_current_mm": 18.0,
            "corrosion_allowance_mm": 1.5,
            "assumed_corrosion_rate_mm_per_year": 0.2,
        }
        result = self.service.evaluate(payload)
        self.assertIn("final_results", result)
        self.assertIn("t_required_shell_mm", result["final_results"])
        self.assertFalse(result["flags"]["red_flags"])

    def test_vessel_below_required_thickness_flag(self) -> None:
        payload = {
            "material": "SA-516-70",
            "design_pressure_mpa": 8.0,
            "design_temperature_c": 250.0,
            "inside_radius_mm": 900.0,
            "joint_efficiency": 0.85,
            "t_current_mm": 6.0,
            "corrosion_allowance_mm": 1.5,
            "assumed_corrosion_rate_mm_per_year": 0.2,
        }
        result = self.service.evaluate(payload)
        self.assertIn("PHY.CURRENT_THICKNESS_BELOW_MINIMUM", result["flags"]["red_flags"])

    def test_low_alloy_vessel_material_supported(self) -> None:
        payload = {
            "material": "SA-387 Gr22 Cl2",
            "vessel_type": "reactor",
            "design_pressure_mpa": 3.2,
            "design_temperature_c": 420.0,
            "inside_radius_mm": 900.0,
            "joint_efficiency": 0.85,
            "t_current_mm": 24.0,
            "corrosion_allowance_mm": 1.5,
            "assumed_corrosion_rate_mm_per_year": 0.15,
        }
        result = self.service.evaluate(payload)
        self.assertNotIn("STD.UNAPPROVED_MATERIAL", result["flags"]["red_flags"])
        self.assertIn("t_required_shell_mm", result["final_results"])

    def test_dimension_context_warning_for_vertical_vessel(self) -> None:
        payload = {
            "material": "SA-516-70",
            "vessel_type": "vertical_vessel",
            "design_pressure_mpa": 2.0,
            "design_temperature_c": 200.0,
            "inside_radius_mm": 750.0,
            "joint_efficiency": 0.85,
            "t_current_mm": 18.0,
            "corrosion_allowance_mm": 1.5,
            "assumed_corrosion_rate_mm_per_year": 0.2,
        }
        result = self.service.evaluate(payload)
        self.assertIn("DATA.VESSEL_DIMENSION_CONTEXT_MISSING", result["flags"]["warnings"])

    def test_high_ld_ratio_warning(self) -> None:
        payload = {
            "material": "SA-516-70",
            "vessel_type": "column_tower",
            "design_pressure_mpa": 2.0,
            "design_temperature_c": 200.0,
            "inside_radius_mm": 750.0,
            "straight_shell_height_mm": 15000.0,
            "head_type": "ellipsoidal_2_1",
            "head_depth_mm": 375.0,
            "joint_efficiency": 0.85,
            "t_current_mm": 18.0,
            "corrosion_allowance_mm": 1.5,
            "assumed_corrosion_rate_mm_per_year": 0.2,
        }
        result = self.service.evaluate(payload)
        self.assertIn("PHY.VESSEL_HIGH_LD_RATIO", result["flags"]["warnings"])

    def test_external_pressure_risk_flag(self) -> None:
        payload = {
            "material": "SA-516-70",
            "vessel_type": "horizontal_drum",
            "design_pressure_mpa": 2.0,
            "design_temperature_c": 200.0,
            "inside_radius_mm": 750.0,
            "shell_length_mm": 3000.0,
            "joint_efficiency": 0.85,
            "t_current_mm": 8.0,
            "external_pressure_mpa": 0.8,
            "corrosion_allowance_mm": 1.5,
            "assumed_corrosion_rate_mm_per_year": 0.2,
        }
        result = self.service.evaluate(payload)
        self.assertIn("PHY.VESSEL_EXTERNAL_PRESSURE_RISK", result["flags"]["red_flags"])

    def test_nozzle_reinforcement_review_warning(self) -> None:
        payload = {
            "material": "SA-516-70",
            "vessel_type": "horizontal_drum",
            "design_pressure_mpa": 2.0,
            "design_temperature_c": 200.0,
            "inside_radius_mm": 750.0,
            "shell_length_mm": 3000.0,
            "head_type": "ellipsoidal_2_1",
            "head_depth_mm": 375.0,
            "nozzle_od_mm": 450.0,
            "reinforcement_pad_thickness_mm": 0.0,
            "reinforcement_pad_width_mm": 0.0,
            "joint_efficiency": 0.85,
            "t_current_mm": 23.0,
            "corrosion_allowance_mm": 1.5,
            "assumed_corrosion_rate_mm_per_year": 0.2,
        }
        result = self.service.evaluate(payload)
        self.assertIn("PHY.VESSEL_NOZZLE_REINFORCEMENT_REVIEW", result["flags"]["warnings"])


    def test_ffs_screening_present(self) -> None:
        payload = {
            "material": "SA-516-70",
            "design_pressure_mpa": 2.0,
            "design_temperature_c": 200.0,
            "inside_radius_mm": 500.0,
            "t_current_mm": 20.0,
            "corrosion_allowance_mm": 3.0,
            "joint_efficiency": 0.85,
            "assumed_corrosion_rate_mm_per_year": 0.2,
        }
        result = self.service.evaluate(payload)
        fr = result["final_results"]
        self.assertIn("ffs_screening_level", fr)
        self.assertIn("repair_scope_screening", fr)
        self.assertIn("LEVEL", fr["ffs_screening_level"])


if __name__ == "__main__":
    unittest.main()
