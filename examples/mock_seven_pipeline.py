from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.agents.runtime_builder import build_mock_runtime
from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.seven_pipeline import SevenDisciplinePipelineService
from src.shared.config_loader import load_and_validate_config


def main() -> None:
    config, errors = load_and_validate_config(ROOT / "configs" / "sample_config.json")
    if errors:
        print("CONFIG_INVALID", errors)
        return

    service = SevenDisciplinePipelineService(Orchestrator(runtime=build_mock_runtime(config)))
    result = service.run(
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
        steel_input={
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
        civil_input={
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
    )

    print("status:", result.status)
    print("state:", result.state)
    print("cross_status:", result.cross_discipline.get("status"))
    print("cross_red_flags:", result.cross_discipline.get("flags", {}).get("red_flags"))


if __name__ == "__main__":
    main()
