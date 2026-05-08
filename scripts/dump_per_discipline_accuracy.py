#!/usr/bin/env python3
"""Per-discipline accuracy breakdown for the 220-case golden benchmark.

Goal (manuscript revision, R1 follow-up): the existing
`outputs/verification_report_runtime.md` collapses 220 cases into a single
"220/220 = 1.0000" line. Reviewer 1 asked whether the system has differential
strengths and weaknesses across disciplines (civil, electrical, etc.).
This script reuses the same code path as `scripts/benchmark_all_runtime.py`
to emit per-discipline metrics:
  * total cases / passes / fails / accuracy
  * mean and max absolute relative error of the primary metric per discipline
  * red-flag detection precision and recall
"""

from __future__ import annotations

import json
import math
import pathlib
import sys
from typing import Any, Callable, Dict, List, Mapping

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.benchmark_all_runtime import DATASETS, KEY_MAP, pass_metric, rel_error
from src.civil.service import CivilVerificationService
from src.electrical.service import ElectricalVerificationService
from src.instrumentation.service import InstrumentationVerificationService
from src.piping.service import PipingVerificationService
from src.rotating.service import RotatingVerificationService
from src.steel.service import SteelVerificationService
from src.vessel.service import VesselVerificationService

OUT_JSON = ROOT / "outputs" / "per_discipline_accuracy.json"
OUT_MD = ROOT / "outputs" / "per_discipline_accuracy.md"

# Primary metric per discipline used to compute the headline relative-error column.
# Choices follow the same load-bearing metric from each service's response.
PRIMARY_METRIC = {
    "piping": "t_min_mm",
    "vessel": "t_required_shell_mm",
    "rotating": "vibration_mm_per_s",
    "electrical": "transformer_health_index",
    "instrumentation": "pfdavg",
    "steel": "phi_pn_kn",
    "civil": "phi_mn_knm",
}

EXPECTED_DISTRIBUTION = {
    "piping": 50,
    "vessel": 30,
    "rotating": 30,
    "electrical": 30,
    "instrumentation": 30,
    "steel": 25,
    "civil": 25,
}


def benchmark_discipline_detailed(
    discipline: str,
    dataset_path: pathlib.Path,
    evaluator: Callable[[Mapping[str, Any]], Mapping[str, Any]],
) -> Dict[str, Any]:
    data = json.loads(dataset_path.read_text(encoding="utf-8"))
    cases = data["cases"]

    total = len(cases)
    passed = 0
    failed_case_ids: List[str] = []

    primary_key_expected = PRIMARY_METRIC[discipline]
    primary_key_actual = KEY_MAP[discipline][primary_key_expected]
    primary_rel_errors: List[float] = []

    # Red-flag confusion across the dataset.
    rf_tp = 0
    rf_fp = 0
    rf_fn = 0

    per_case_records: List[Dict[str, Any]] = []

    for case in cases:
        critical = case.get("criticality") == "critical"
        tolerance = 0.01 if critical else 0.03

        result = evaluator(case["inputs"])
        final = result.get("final_results", {})

        expected_outputs = case.get("expected_outputs", {})
        numeric_ok = True
        for expected_key, actual_key in KEY_MAP[discipline].items():
            exp_val = expected_outputs.get(expected_key)
            act_val = final.get(actual_key)
            ok = pass_metric(act_val, exp_val, tolerance)
            numeric_ok = numeric_ok and ok

        steps = result.get("calculation_steps", [])
        has_refs = isinstance(steps, list) and all(
            isinstance(s, dict) and bool(s.get("standard_reference")) for s in steps
        )

        expected_red = set(case.get("expected_red_flags", []))
        actual_red = set(result.get("flags", {}).get("red_flags", []))
        red_ok = expected_red.issubset(actual_red)

        # Red-flag confusion: per-flag, per-case.
        rf_tp += len(expected_red & actual_red)
        rf_fp += len(actual_red - expected_red)
        rf_fn += len(expected_red - actual_red)

        # Primary-metric relative error (only when both sides are numeric).
        exp_primary = expected_outputs.get(primary_key_expected)
        act_primary = final.get(primary_key_actual)
        if (
            isinstance(exp_primary, (int, float))
            and isinstance(act_primary, (int, float))
            and not (isinstance(exp_primary, bool) or isinstance(act_primary, bool))
            and not math.isinf(float(exp_primary))
            and not math.isinf(float(act_primary))
        ):
            primary_rel_errors.append(rel_error(float(act_primary), float(exp_primary)))

        case_pass = numeric_ok and has_refs and red_ok
        if case_pass:
            passed += 1
        else:
            failed_case_ids.append(str(case.get("case_id")))

        per_case_records.append(
            {
                "case_id": case.get("case_id"),
                "criticality": case.get("criticality"),
                "case_pass": case_pass,
                "numeric_ok": numeric_ok,
                "references_ok": has_refs,
                "red_flags_ok": red_ok,
                "expected_red_flags": sorted(expected_red),
                "actual_red_flags": sorted(actual_red),
            }
        )

    failed = total - passed
    accuracy = passed / total if total else 0.0

    if primary_rel_errors:
        mean_rel_err = float(sum(primary_rel_errors) / len(primary_rel_errors))
        max_rel_err = float(max(primary_rel_errors))
    else:
        mean_rel_err = 0.0
        max_rel_err = 0.0

    rf_precision = (rf_tp / (rf_tp + rf_fp)) if (rf_tp + rf_fp) else None
    rf_recall = (rf_tp / (rf_tp + rf_fn)) if (rf_tp + rf_fn) else None

    return {
        "discipline": discipline,
        "total_cases": total,
        "passed_cases": passed,
        "failed_cases": failed,
        "accuracy": accuracy,
        "primary_metric_expected_key": primary_key_expected,
        "primary_metric_actual_key": primary_key_actual,
        "primary_metric_rel_error_mean": mean_rel_err,
        "primary_metric_rel_error_max": max_rel_err,
        "primary_metric_sample_size": len(primary_rel_errors),
        "red_flag_true_positives": rf_tp,
        "red_flag_false_positives": rf_fp,
        "red_flag_false_negatives": rf_fn,
        "red_flag_precision": rf_precision,
        "red_flag_recall": rf_recall,
        "failed_case_ids": failed_case_ids,
        "cases": per_case_records,
    }


def main() -> int:
    missing = [name for name, path in DATASETS.items() if not path.exists()]
    if missing:
        raise RuntimeError(f"Missing golden datasets: {missing}")

    services = {
        "piping": PipingVerificationService(),
        "vessel": VesselVerificationService(),
        "rotating": RotatingVerificationService(),
        "electrical": ElectricalVerificationService(),
        "instrumentation": InstrumentationVerificationService(),
        "steel": SteelVerificationService(),
        "civil": CivilVerificationService(),
    }

    reports: List[Dict[str, Any]] = []
    for discipline in (
        "piping",
        "vessel",
        "rotating",
        "electrical",
        "instrumentation",
        "steel",
        "civil",
    ):
        svc = services[discipline]
        reports.append(
            benchmark_discipline_detailed(
                discipline,
                DATASETS[discipline],
                lambda x, _svc=svc: _svc.evaluate(x),
            )
        )

    # Sanity: counts per discipline must match the published distribution.
    actual_distribution = {r["discipline"]: r["total_cases"] for r in reports}
    if actual_distribution != EXPECTED_DISTRIBUTION:
        raise RuntimeError(
            f"Discipline case counts {actual_distribution} != expected {EXPECTED_DISTRIBUTION}"
        )
    total_cases = sum(r["total_cases"] for r in reports)
    if total_cases != 220:
        raise RuntimeError(f"Total cases {total_cases} != 220")

    total_passed = sum(r["passed_cases"] for r in reports)
    overall_accuracy = total_passed / total_cases

    summary = {
        "total_cases": total_cases,
        "passed_cases": total_passed,
        "overall_accuracy": overall_accuracy,
        "expected_distribution": EXPECTED_DISTRIBUTION,
        "disciplines": reports,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Per-Discipline Calculation Accuracy Breakdown",
        "",
        f"- Total cases: {total_cases}",
        f"- Passed cases: {total_passed}",
        f"- Overall accuracy: {overall_accuracy:.4f}",
        "- Source dataset: `datasets/golden_standards/*_golden_dataset_v1.json`",
        "- Code path: `scripts/benchmark_all_runtime.py` (re-used).",
        "",
        "## Per-Discipline Table",
        "",
        "| Discipline | Cases | Pass | Fail | Accuracy | Primary metric | Mean rel. err | Max rel. err | RF precision | RF recall |",
        "|---|---:|---:|---:|---:|---|---:|---:|---:|---:|",
    ]
    for r in reports:
        prec = r["red_flag_precision"]
        rec = r["red_flag_recall"]
        prec_str = f"{prec:.4f}" if prec is not None else "n/a"
        rec_str = f"{rec:.4f}" if rec is not None else "n/a"
        lines.append(
            f"| {r['discipline']} | {r['total_cases']} | {r['passed_cases']} | "
            f"{r['failed_cases']} | {r['accuracy']:.4f} | {r['primary_metric_expected_key']} | "
            f"{r['primary_metric_rel_error_mean']:.6f} | {r['primary_metric_rel_error_max']:.6f} | "
            f"{prec_str} | {rec_str} |"
        )
    lines.extend(
        [
            "",
            "## Red-flag Confusion (Per-Discipline)",
            "",
            "Per-flag, per-case counts: TP = expected and predicted; FP = predicted but not expected; FN = expected but not predicted.",
            "",
            "| Discipline | TP | FP | FN |",
            "|---|---:|---:|---:|",
        ]
    )
    for r in reports:
        lines.append(
            f"| {r['discipline']} | {r['red_flag_true_positives']} | "
            f"{r['red_flag_false_positives']} | {r['red_flag_false_negatives']} |"
        )

    # List failures, if any.
    failure_section = []
    for r in reports:
        if r["failed_case_ids"]:
            failure_section.append(f"- {r['discipline']}: {r['failed_case_ids']}")
    if failure_section:
        lines.extend(["", "## Failed Cases", ""])
        lines.extend(failure_section)

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"REPORT_JSON={OUT_JSON}")
    print(f"REPORT_MD={OUT_MD}")
    print(f"OVERALL_ACCURACY={overall_accuracy:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
