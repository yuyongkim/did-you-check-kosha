from __future__ import annotations

import json
import math
import pathlib
import sys
from typing import Any, Dict, List, Mapping

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.piping.service import PipingVerificationService


DATASET_PATH = ROOT / "datasets" / "golden_standards" / "piping_golden_dataset_v1.json"
REPORT_JSON_PATH = ROOT / "docs" / "piping" / "VERIFICATION_REPORT.json"
REPORT_MD_PATH = ROOT / "docs" / "piping" / "VERIFICATION_REPORT.md"


KEY_MAP = {
    "t_min_mm": "t_min_mm",
    "CR_long_term": "cr_long_term_mm_per_year",
    "CR_short_term": "cr_short_term_mm_per_year",
    "CR_selected": "cr_selected_mm_per_year",
    "RL_years": "remaining_life_years",
    "inspection_interval_years": "inspection_interval_years",
}


def rel_error(actual: float, expected: float) -> float:
    if expected == 0:
        return abs(actual - expected)
    return abs(actual - expected) / max(abs(expected), 1e-12)


def within_tolerance(actual: float, expected: float, tolerance: float) -> bool:
    if math.isinf(actual) and math.isinf(expected):
        return True
    return rel_error(actual, expected) <= tolerance


def benchmark() -> Dict[str, Any]:
    dataset = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    service = PipingVerificationService()

    cases: List[Mapping[str, Any]] = dataset["cases"]

    total = len(cases)
    passed = 0
    passed_critical = 0
    critical_total = 0
    standard_ref_ok = 0
    red_flag_ok = 0
    per_case: List[Dict[str, Any]] = []

    for case in cases:
        case_id = str(case["case_id"])
        expected = case["expected_outputs"]
        expected_flags = set(case.get("expected_red_flags", []))
        critical = case.get("criticality") == "critical"

        if critical:
            critical_total += 1

        result = service.evaluate(case["inputs"])
        final = result.get("final_results", {})

        tolerance = 0.01 if critical else 0.03
        numeric_ok = True

        comparisons: Dict[str, Dict[str, Any]] = {}
        for expected_key, actual_key in KEY_MAP.items():
            exp_val = expected.get(expected_key)
            act_val = final.get(actual_key)
            if exp_val is None or act_val is None:
                comparisons[expected_key] = {"passed": False, "expected": exp_val, "actual": act_val}
                numeric_ok = False
                continue

            passed_metric = within_tolerance(float(act_val), float(exp_val), tolerance)
            comparisons[expected_key] = {
                "passed": passed_metric,
                "expected": exp_val,
                "actual": act_val,
                "relative_error": rel_error(float(act_val), float(exp_val)),
            }
            numeric_ok = numeric_ok and passed_metric

        steps = result.get("calculation_steps", [])
        references_ok = isinstance(steps, list) and all(
            isinstance(step, dict) and bool(step.get("standard_reference"))
            for step in steps
        )

        actual_red_flags = set(result.get("flags", {}).get("red_flags", []))
        red_flags_match = expected_flags.issubset(actual_red_flags)

        case_pass = numeric_ok and references_ok and red_flags_match

        if case_pass:
            passed += 1
        if critical and case_pass:
            passed_critical += 1
        if references_ok:
            standard_ref_ok += 1
        if red_flags_match:
            red_flag_ok += 1

        per_case.append(
            {
                "case_id": case_id,
                "critical": critical,
                "tolerance": tolerance,
                "case_pass": case_pass,
                "numeric_ok": numeric_ok,
                "references_ok": references_ok,
                "red_flags_match": red_flags_match,
                "comparisons": comparisons,
                "expected_red_flags": sorted(expected_flags),
                "actual_red_flags": sorted(actual_red_flags),
            }
        )

    overall_accuracy = passed / total if total else 0.0
    critical_accuracy = passed_critical / critical_total if critical_total else 0.0
    standard_ref_accuracy = standard_ref_ok / total if total else 0.0
    red_flag_accuracy = red_flag_ok / total if total else 0.0

    return {
        "dataset_id": dataset.get("dataset_id"),
        "total_cases": total,
        "critical_cases": critical_total,
        "passed_cases": passed,
        "passed_critical_cases": passed_critical,
        "overall_accuracy": overall_accuracy,
        "critical_accuracy": critical_accuracy,
        "standard_reference_accuracy": standard_ref_accuracy,
        "red_flag_detection_accuracy": red_flag_accuracy,
        "success_criteria": {
            "overall_accuracy_target": 0.99,
            "critical_accuracy_target": 1.0,
            "standard_reference_accuracy_target": 1.0,
            "red_flag_detection_accuracy_target": 1.0,
        },
        "per_case": per_case,
    }


def render_markdown(report: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# Piping Verification Report",
            "",
            f"- Dataset: {report['dataset_id']}",
            f"- Total Cases: {report['total_cases']}",
            f"- Critical Cases: {report['critical_cases']}",
            f"- Passed Cases: {report['passed_cases']}",
            f"- Passed Critical Cases: {report['passed_critical_cases']}",
            f"- Overall Accuracy: {report['overall_accuracy']:.4f}",
            f"- Critical Accuracy: {report['critical_accuracy']:.4f}",
            f"- Standards Reference Accuracy: {report['standard_reference_accuracy']:.4f}",
            f"- Red-Flag Detection Accuracy: {report['red_flag_detection_accuracy']:.4f}",
            "",
            "## Criteria Check",
            f"- Overall >= 0.99: {'PASS' if report['overall_accuracy'] >= 0.99 else 'FAIL'}",
            f"- Critical == 1.00: {'PASS' if report['critical_accuracy'] >= 1.0 else 'FAIL'}",
            f"- Standards Ref == 1.00: {'PASS' if report['standard_reference_accuracy'] >= 1.0 else 'FAIL'}",
            f"- Red-Flag == 1.00: {'PASS' if report['red_flag_detection_accuracy'] >= 1.0 else 'FAIL'}",
        ]
    )


def main() -> int:
    if not DATASET_PATH.exists():
        print(f"DATASET_NOT_FOUND={DATASET_PATH}")
        return 1

    report = benchmark()

    REPORT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    REPORT_MD_PATH.write_text(render_markdown(report), encoding="utf-8")

    print(f"REPORT_JSON={REPORT_JSON_PATH}")
    print(f"REPORT_MD={REPORT_MD_PATH}")
    print(f"OVERALL_ACCURACY={report['overall_accuracy']:.4f}")
    print(f"CRITICAL_ACCURACY={report['critical_accuracy']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
