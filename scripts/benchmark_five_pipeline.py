from __future__ import annotations

import json
import pathlib
import sys
from collections import Counter
from typing import Any, Dict, List, Mapping

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.agents.runtime_builder import build_mock_runtime
from src.orchestrator.five_pipeline import FiveDisciplinePipelineService
from src.orchestrator.orchestrator import Orchestrator
from src.shared.config_loader import load_and_validate_config


OUT_JSON = ROOT / "outputs" / "five_pipeline_report.json"
OUT_MD = ROOT / "outputs" / "five_pipeline_report.md"


def load_cases(path: pathlib.Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["cases"]


def split_by_category(cases: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {"standard": [], "boundary": [], "failure_mode": []}
    for case in cases:
        category = str(case.get("category", "standard"))
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(case)
    return grouped


def run_set(
    *,
    name: str,
    scenarios: int,
    p_cases: List[Dict[str, Any]],
    v_cases: List[Dict[str, Any]],
    r_cases: List[Dict[str, Any]],
    e_cases: List[Dict[str, Any]],
    i_cases: List[Dict[str, Any]],
    service: FiveDisciplinePipelineService,
) -> Dict[str, Any]:
    n = min(scenarios, len(p_cases), len(v_cases), len(r_cases), len(e_cases), len(i_cases))
    completed = 0
    blocked = 0
    cross_flag_counter = Counter()
    rows = []

    for i in range(n):
        result = service.run(
            piping_input=p_cases[i]["inputs"],
            vessel_input=v_cases[i]["inputs"],
            rotating_input=r_cases[i]["inputs"],
            electrical_input=e_cases[i]["inputs"],
            instrumentation_input=i_cases[i]["inputs"],
        )

        if result.status == "completed":
            completed += 1
        else:
            blocked += 1

        red_flags = result.cross_discipline.get("flags", {}).get("red_flags", [])
        if isinstance(red_flags, list):
            for code in red_flags:
                if isinstance(code, str):
                    cross_flag_counter[code] += 1

        rows.append(
            {
                "scenario_id": i + 1,
                "status": result.status,
                "cross_status": result.cross_discipline.get("status"),
                "cross_red_flags": red_flags,
            }
        )

    return {
        "set_name": name,
        "total_scenarios": n,
        "completed": completed,
        "blocked": blocked,
        "completion_ratio": (completed / n) if n else 0.0,
        "blocking_ratio": (blocked / n) if n else 0.0,
        "top_cross_red_flags": cross_flag_counter.most_common(10),
        "scenarios": rows,
    }


def run_nominal_set(*, service: FiveDisciplinePipelineService, scenarios: int = 5) -> Dict[str, Any]:
    completed = 0
    blocked = 0
    cross_flag_counter = Counter()
    rows = []

    payloads = {
        "piping_input": {
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
        "vessel_input": {
            "material": "SA-516-70",
            "design_pressure_mpa": 2.0,
            "design_temperature_c": 200.0,
            "inside_radius_mm": 750.0,
            "joint_efficiency": 0.85,
            "t_current_mm": 18.0,
            "corrosion_allowance_mm": 1.5,
            "assumed_corrosion_rate_mm_per_year": 0.2,
        },
        "rotating_input": {
            "machine_type": "pump",
            "vibration_mm_per_s": 2.5,
            "nozzle_load_ratio": 0.85,
            "bearing_temperature_c": 72.0,
            "speed_rpm": 1800,
        },
        "electrical_input": {
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
        "instrumentation_input": {
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
    }

    for i in range(scenarios):
        result = service.run(**payloads)
        if result.status == "completed":
            completed += 1
        else:
            blocked += 1

        red_flags = result.cross_discipline.get("flags", {}).get("red_flags", [])
        if isinstance(red_flags, list):
            for code in red_flags:
                if isinstance(code, str):
                    cross_flag_counter[code] += 1

        rows.append(
            {
                "scenario_id": i + 1,
                "status": result.status,
                "cross_status": result.cross_discipline.get("status"),
                "cross_red_flags": red_flags,
            }
        )

    return {
        "set_name": "nominal_handcrafted",
        "total_scenarios": scenarios,
        "completed": completed,
        "blocked": blocked,
        "completion_ratio": (completed / scenarios) if scenarios else 0.0,
        "blocking_ratio": (blocked / scenarios) if scenarios else 0.0,
        "top_cross_red_flags": cross_flag_counter.most_common(10),
        "scenarios": rows,
    }


def main() -> int:
    config, errors = load_and_validate_config(ROOT / "configs" / "sample_config.json")
    if errors:
        print(f"CONFIG_INVALID={errors}")
        return 1

    service = FiveDisciplinePipelineService(Orchestrator(runtime=build_mock_runtime(config)))

    p_all = load_cases(ROOT / "datasets" / "golden_standards" / "piping_golden_dataset_v1.json")
    v_all = load_cases(ROOT / "datasets" / "golden_standards" / "vessel_golden_dataset_v1.json")
    r_all = load_cases(ROOT / "datasets" / "golden_standards" / "rotating_golden_dataset_v1.json")
    e_all = load_cases(ROOT / "datasets" / "golden_standards" / "electrical_golden_dataset_v1.json")
    i_all = load_cases(ROOT / "datasets" / "golden_standards" / "instrumentation_golden_dataset_v1.json")

    p = split_by_category(p_all)
    v = split_by_category(v_all)
    r = split_by_category(r_all)
    e = split_by_category(e_all)
    i = split_by_category(i_all)

    set_reports = [
        run_nominal_set(service=service, scenarios=5),
        run_set(
            name="standard_aligned",
            scenarios=10,
            p_cases=p["standard"],
            v_cases=v["standard"],
            r_cases=r["standard"],
            e_cases=e["standard"],
            i_cases=i["standard"],
            service=service,
        ),
        run_set(
            name="boundary_aligned",
            scenarios=8,
            p_cases=p["boundary"],
            v_cases=v["boundary"],
            r_cases=r["boundary"],
            e_cases=e["boundary"],
            i_cases=i["boundary"],
            service=service,
        ),
        run_set(
            name="failure_aligned",
            scenarios=5,
            p_cases=p["failure_mode"],
            v_cases=v["failure_mode"],
            r_cases=r["failure_mode"],
            e_cases=e["failure_mode"],
            i_cases=i["failure_mode"],
            service=service,
        ),
        run_set(
            name="mixed_first15",
            scenarios=15,
            p_cases=p_all,
            v_cases=v_all,
            r_cases=r_all,
            e_cases=e_all,
            i_cases=i_all,
            service=service,
        ),
    ]

    total_scenarios = sum(s["total_scenarios"] for s in set_reports)
    total_completed = sum(s["completed"] for s in set_reports)
    total_blocked = sum(s["blocked"] for s in set_reports)

    summary = {
        "total_scenarios": total_scenarios,
        "completed": total_completed,
        "blocked": total_blocked,
        "completion_ratio": (total_completed / total_scenarios) if total_scenarios else 0.0,
        "blocking_ratio": (total_blocked / total_scenarios) if total_scenarios else 0.0,
        "scenario_sets": set_reports,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [
        "# Five-Discipline Pipeline Runtime Report",
        "",
        f"- Total Scenarios: {summary['total_scenarios']}",
        f"- Completed: {summary['completed']}",
        f"- Blocked: {summary['blocked']}",
        f"- Completion Ratio: {summary['completion_ratio']:.4f}",
        f"- Blocking Ratio: {summary['blocking_ratio']:.4f}",
        "",
        "## Scenario Sets",
    ]
    for s in set_reports:
        lines.append(
            f"- {s['set_name']}: completion_ratio={s['completion_ratio']:.4f}, "
            f"blocked={s['blocked']}/{s['total_scenarios']}"
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"REPORT_JSON={OUT_JSON}")
    print(f"REPORT_MD={OUT_MD}")
    print(f"COMPLETION_RATIO={summary['completion_ratio']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
