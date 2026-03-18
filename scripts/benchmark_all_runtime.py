from __future__ import annotations

import json
import math
import pathlib
import sys
from typing import Any, Callable, Dict, List, Mapping

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.piping.service import PipingVerificationService
from src.vessel.service import VesselVerificationService
from src.rotating.service import RotatingVerificationService
from src.electrical.service import ElectricalVerificationService
from src.instrumentation.service import InstrumentationVerificationService
from src.steel.service import SteelVerificationService
from src.civil.service import CivilVerificationService


DATASETS = {
    "piping": ROOT / "datasets" / "golden_standards" / "piping_golden_dataset_v1.json",
    "vessel": ROOT / "datasets" / "golden_standards" / "vessel_golden_dataset_v1.json",
    "rotating": ROOT / "datasets" / "golden_standards" / "rotating_golden_dataset_v1.json",
    "electrical": ROOT / "datasets" / "golden_standards" / "electrical_golden_dataset_v1.json",
    "instrumentation": ROOT / "datasets" / "golden_standards" / "instrumentation_golden_dataset_v1.json",
    "steel": ROOT / "datasets" / "golden_standards" / "steel_golden_dataset_v1.json",
    "civil": ROOT / "datasets" / "golden_standards" / "civil_golden_dataset_v1.json",
}

REPORT_JSON = ROOT / "outputs" / "verification_report_runtime.json"
REPORT_MD = ROOT / "outputs" / "verification_report_runtime.md"


KEY_MAP = {
    "piping": {
        "t_min_mm": "t_min_mm",
        "CR_long_term": "cr_long_term_mm_per_year",
        "CR_short_term": "cr_short_term_mm_per_year",
        "CR_selected": "cr_selected_mm_per_year",
        "RL_years": "remaining_life_years",
        "inspection_interval_years": "inspection_interval_years",
    },
    "vessel": {
        "t_required_shell_mm": "t_required_shell_mm",
        "remaining_life_years": "remaining_life_years",
        "inspection_interval_years": "inspection_interval_years",
        "corrosion_rate_selected_mm_per_year": "corrosion_rate_selected_mm_per_year",
    },
    "rotating": {
        "vibration_mm_per_s": "vibration_mm_per_s",
        "vibration_limit_mm_per_s": "vibration_limit_mm_per_s",
        "nozzle_load_ratio": "nozzle_load_ratio",
        "bearing_temperature_c": "bearing_temperature_c",
        "bearing_health_index": "bearing_health_index",
        "inspection_interval_years": "inspection_interval_years",
        "status": "status",
    },
    "electrical": {
        "transformer_health_index": "transformer_health_index",
        "arc_flash_energy_cal_cm2": "arc_flash_energy_cal_cm2",
        "ppe_category": "ppe_category",
        "voltage_drop_percent": "voltage_drop_percent",
        "fault_current_ka": "fault_current_ka",
        "breaker_interrupt_rating_ka": "breaker_interrupt_rating_ka",
        "thd_voltage_percent": "thd_voltage_percent",
        "motor_current_thd_percent": "motor_current_thd_percent",
        "power_factor": "power_factor",
        "inspection_interval_years": "inspection_interval_years",
        "status": "status",
    },
    "instrumentation": {
        "drift_rate_pct_per_day": "drift_rate_pct_per_day",
        "drift_r_squared": "drift_r_squared",
        "predicted_drift_pct": "predicted_drift_pct",
        "pfdavg": "pfdavg",
        "sil_target": "sil_target",
        "sil_achieved": "sil_achieved",
        "combined_uncertainty_pct": "combined_uncertainty_pct",
        "calibration_interval_optimal_days": "calibration_interval_optimal_days",
        "inspection_interval_days": "inspection_interval_days",
        "cv_margin_ratio": "cv_margin_ratio",
        "status": "status",
    },
    "steel": {
        "reduced_area_mm2": "reduced_area_mm2",
        "lambda_c": "lambda_c",
        "fcr_mpa": "fcr_mpa",
        "phi_pn_kn": "phi_pn_kn",
        "dc_ratio": "dc_ratio",
        "deflection_ratio": "deflection_ratio",
        "corrosion_loss_percent": "corrosion_loss_percent",
        "inspection_interval_years": "inspection_interval_years",
        "status": "status",
    },
    "civil": {
        "a_mm": "a_mm",
        "phi_mn_knm": "phi_mn_knm",
        "dc_ratio": "dc_ratio",
        "carbonation_depth_mm": "carbonation_depth_mm",
        "substantial_damage": "substantial_damage",
        "damage_mode": "damage_mode",
        "corrosion_initiated": "corrosion_initiated",
        "years_to_corrosion_init": "years_to_corrosion_init",
        "crack_width_mm": "crack_width_mm",
        "spalling_area_percent": "spalling_area_percent",
        "foundation_settlement_mm": "foundation_settlement_mm",
        "inspection_interval_years": "inspection_interval_years",
        "status": "status",
    },
}


def rel_error(actual: float, expected: float) -> float:
    if expected == 0:
        return abs(actual - expected)
    return abs(actual - expected) / max(abs(expected), 1e-12)


def pass_metric(actual: Any, expected: Any, tolerance: float) -> bool:
    if isinstance(expected, str):
        return str(actual) == expected
    if expected is None or actual is None:
        return False
    if isinstance(expected, (float, int)) and isinstance(actual, (float, int)):
        if math.isinf(float(expected)) and math.isinf(float(actual)):
            return True
        return rel_error(float(actual), float(expected)) <= tolerance
    return actual == expected


def benchmark_discipline(
    discipline: str,
    dataset_path: pathlib.Path,
    evaluator: Callable[[Mapping[str, Any]], Mapping[str, Any]],
) -> Dict[str, Any]:
    data = json.loads(dataset_path.read_text(encoding="utf-8"))
    cases = data["cases"]

    total = len(cases)
    passed = 0
    references_ok = 0
    red_flag_ok = 0
    case_results: List[Dict[str, Any]] = []

    for case in cases:
        critical = case.get("criticality") == "critical"
        tolerance = 0.01 if critical else 0.03

        result = evaluator(case["inputs"])
        final = result.get("final_results", {})

        expected_outputs = case.get("expected_outputs", {})
        comparisons: Dict[str, Any] = {}
        numeric_ok = True

        for expected_key, actual_key in KEY_MAP[discipline].items():
            exp_val = expected_outputs.get(expected_key)
            act_val = final.get(actual_key)
            ok = pass_metric(act_val, exp_val, tolerance)
            comparisons[expected_key] = {"expected": exp_val, "actual": act_val, "passed": ok}
            numeric_ok = numeric_ok and ok

        steps = result.get("calculation_steps", [])
        has_refs = isinstance(steps, list) and all(isinstance(s, dict) and bool(s.get("standard_reference")) for s in steps)

        expected_red = set(case.get("expected_red_flags", []))
        actual_red = set(result.get("flags", {}).get("red_flags", []))
        red_ok = expected_red.issubset(actual_red)

        case_pass = numeric_ok and has_refs and red_ok
        if case_pass:
            passed += 1
        if has_refs:
            references_ok += 1
        if red_ok:
            red_flag_ok += 1

        case_results.append(
            {
                "case_id": case.get("case_id"),
                "critical": critical,
                "case_pass": case_pass,
                "numeric_ok": numeric_ok,
                "references_ok": has_refs,
                "red_flags_ok": red_ok,
                "comparisons": comparisons,
            }
        )

    return {
        "discipline": discipline,
        "total_cases": total,
        "passed_cases": passed,
        "accuracy": passed / total if total else 0.0,
        "standard_reference_accuracy": references_ok / total if total else 0.0,
        "red_flag_accuracy": red_flag_ok / total if total else 0.0,
        "cases": case_results,
    }


def main() -> int:
    missing = [name for name, path in DATASETS.items() if not path.exists()]
    if missing:
        print(f"MISSING_DATASETS={missing}")
        return 1

    piping = PipingVerificationService()
    vessel = VesselVerificationService()
    rotating = RotatingVerificationService()
    electrical = ElectricalVerificationService()
    instrumentation = InstrumentationVerificationService()
    steel = SteelVerificationService()
    civil = CivilVerificationService()

    reports = [
        benchmark_discipline("piping", DATASETS["piping"], lambda x: piping.evaluate(x)),
        benchmark_discipline("vessel", DATASETS["vessel"], lambda x: vessel.evaluate(x)),
        benchmark_discipline("rotating", DATASETS["rotating"], lambda x: rotating.evaluate(x)),
        benchmark_discipline("electrical", DATASETS["electrical"], lambda x: electrical.evaluate(x)),
        benchmark_discipline("instrumentation", DATASETS["instrumentation"], lambda x: instrumentation.evaluate(x)),
        benchmark_discipline("steel", DATASETS["steel"], lambda x: steel.evaluate(x)),
        benchmark_discipline("civil", DATASETS["civil"], lambda x: civil.evaluate(x)),
    ]

    total_cases = sum(r["total_cases"] for r in reports)
    total_passed = sum(r["passed_cases"] for r in reports)

    summary = {
        "total_cases": total_cases,
        "passed_cases": total_passed,
        "overall_accuracy": total_passed / total_cases if total_cases else 0.0,
        "disciplines": reports,
    }

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [
        "# Runtime Verification Report (Piping + Vessel + Rotating + Electrical + Instrumentation + Steel + Civil)",
        "",
        f"- Total Cases: {summary['total_cases']}",
        f"- Passed Cases: {summary['passed_cases']}",
        f"- Overall Accuracy: {summary['overall_accuracy']:.4f}",
        "",
        "## Discipline Metrics",
    ]
    for r in reports:
        lines.append(f"- {r['discipline']}: accuracy={r['accuracy']:.4f}, standards={r['standard_reference_accuracy']:.4f}, red_flag={r['red_flag_accuracy']:.4f}")

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"REPORT_JSON={REPORT_JSON}")
    print(f"REPORT_MD={REPORT_MD}")
    print(f"OVERALL_ACCURACY={summary['overall_accuracy']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
