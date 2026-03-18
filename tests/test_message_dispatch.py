import pathlib
import unittest

from src.agents.runtime_builder import build_mock_runtime
from src.orchestrator.orchestrator import Orchestrator
from src.shared.config_loader import load_and_validate_config
from src.shared.message_factory import create_message


class MessageDispatchTests(unittest.TestCase):
    def setUp(self) -> None:
        config, errors = load_and_validate_config(pathlib.Path("configs/sample_config.json"))
        assert not errors, errors
        runtime = build_mock_runtime(config)
        self.orchestrator = Orchestrator(runtime=runtime)

    def test_calculation_request_dispatch(self) -> None:
        message = create_message(
            message_type="calculation_request",
            from_agent="orchestrator",
            to_agent="piping_specialist",
            payload={
                "calculation_type": "remaining_life",
                "input_data": {
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
            },
            meta={"workflow_id": "standard_calculation", "discipline": "piping"},
        )
        result = self.orchestrator.handle_message(message)
        self.assertEqual(result["status"], "success")
        self.assertIn("remaining_life_years", result["results"])

    def test_spec_lookup_dispatch(self) -> None:
        message = create_message(
            message_type="spec_lookup_request",
            from_agent="orchestrator",
            to_agent="spec_explorer",
            payload={
                "query": "allowable stress",
                "filters": {"discipline": "piping"},
            },
            meta={"workflow_id": "standard_calculation"},
        )
        result = self.orchestrator.handle_message(message)
        self.assertEqual(result["status"], "success")
        self.assertTrue(len(result["results"]) >= 1)

    def test_vessel_calculation_dispatch(self) -> None:
        message = create_message(
            message_type="calculation_request",
            from_agent="orchestrator",
            to_agent="static_equipment_specialist",
            payload={
                "calculation_type": "vessel_integrity",
                "input_data": {
                    "material": "SA-516-70",
                    "design_pressure_mpa": 2.0,
                    "design_temperature_c": 200.0,
                    "inside_radius_mm": 750.0,
                    "joint_efficiency": 0.85,
                    "t_current_mm": 18.0,
                    "corrosion_allowance_mm": 1.5,
                    "assumed_corrosion_rate_mm_per_year": 0.2,
                },
            },
            meta={"workflow_id": "standard_calculation", "discipline": "vessel"},
        )
        result = self.orchestrator.handle_message(message)
        self.assertEqual(result["status"], "success")
        self.assertIn("t_required_shell_mm", result["results"])

    def test_rotating_calculation_dispatch(self) -> None:
        message = create_message(
            message_type="calculation_request",
            from_agent="orchestrator",
            to_agent="rotating_specialist",
            payload={
                "calculation_type": "rotating_integrity",
                "input_data": {
                    "machine_type": "pump",
                    "vibration_mm_per_s": 2.5,
                    "nozzle_load_ratio": 0.85,
                    "bearing_temperature_c": 72.0,
                    "speed_rpm": 1800,
                },
            },
            meta={"workflow_id": "standard_calculation", "discipline": "rotating"},
        )
        result = self.orchestrator.handle_message(message)
        self.assertEqual(result["status"], "success")
        self.assertIn("bearing_health_index", result["results"])

    def test_electrical_calculation_dispatch(self) -> None:
        message = create_message(
            message_type="calculation_request",
            from_agent="orchestrator",
            to_agent="electrical_specialist",
            payload={
                "calculation_type": "electrical_integrity",
                "input_data": {
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
            },
            meta={"workflow_id": "standard_calculation", "discipline": "electrical"},
        )
        result = self.orchestrator.handle_message(message)
        self.assertEqual(result["status"], "success")
        self.assertIn("transformer_health_index", result["results"])

    def test_instrumentation_calculation_dispatch(self) -> None:
        message = create_message(
            message_type="calculation_request",
            from_agent="orchestrator",
            to_agent="instrumentation_specialist",
            payload={
                "calculation_type": "instrumentation_integrity",
                "input_data": {
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
            },
            meta={"workflow_id": "standard_calculation", "discipline": "instrumentation"},
        )
        result = self.orchestrator.handle_message(message)
        self.assertEqual(result["status"], "success")
        self.assertIn("pfdavg", result["results"])

    def test_steel_calculation_dispatch(self) -> None:
        message = create_message(
            message_type="calculation_request",
            from_agent="orchestrator",
            to_agent="steel_specialist",
            payload={
                "calculation_type": "steel_integrity",
                "input_data": {
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
                },
            },
            meta={"workflow_id": "standard_calculation", "discipline": "steel"},
        )
        result = self.orchestrator.handle_message(message)
        self.assertEqual(result["status"], "success")
        self.assertIn("dc_ratio", result["results"])

    def test_civil_calculation_dispatch(self) -> None:
        message = create_message(
            message_type="calculation_request",
            from_agent="orchestrator",
            to_agent="civil_specialist",
            payload={
                "calculation_type": "civil_integrity",
                "input_data": {
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
                },
            },
            meta={"workflow_id": "standard_calculation", "discipline": "civil"},
        )
        result = self.orchestrator.handle_message(message)
        self.assertEqual(result["status"], "success")
        self.assertIn("dc_ratio", result["results"])

    def test_escalation_event_creates_blocking_flag(self) -> None:
        message = create_message(
            message_type="escalation_event",
            from_agent="verification_agent",
            to_agent="orchestrator",
            payload={
                "reason_code": "STD.INVALID_REFERENCE",
                "severity": "critical",
                "summary": "invalid citation",
                "recommended_action": "human_review_required",
                "blocking": True,
            },
            meta={"workflow_id": "emergency_assessment"},
        )
        result = self.orchestrator.handle_message(message)
        self.assertEqual(result["status"], "escalated")
        self.assertTrue(self.orchestrator.has_blocking_flag())


if __name__ == "__main__":
    unittest.main()
