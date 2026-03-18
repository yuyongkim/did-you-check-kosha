from __future__ import annotations

import json
import pathlib
import random
import sys
from typing import Any, Dict, List

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.instrumentation.service import InstrumentationVerificationService


DATASET_PATH = ROOT / "datasets" / "golden_standards" / "instrumentation_golden_dataset_v1.json"


def split_counts(total: int) -> Dict[str, int]:
    standard = int(total * 0.60)
    boundary = int(total * 0.25)
    failure = total - standard - boundary
    return {"standard": standard, "boundary": boundary, "failure_mode": failure}


def _history(base_slope: float, base_intercept: float) -> List[Dict[str, float]]:
    return [
        {"days_since_ref": 0.0, "error_pct": round(base_intercept + base_slope * 0.0, 5)},
        {"days_since_ref": 90.0, "error_pct": round(base_intercept + base_slope * 90.0, 5)},
        {"days_since_ref": 180.0, "error_pct": round(base_intercept + base_slope * 180.0, 5)},
        {"days_since_ref": 270.0, "error_pct": round(base_intercept + base_slope * 270.0, 5)},
    ]


def make_case(case_id: str, category: str, payload: Dict[str, Any], service: InstrumentationVerificationService) -> Dict[str, Any]:
    result = service.evaluate(payload)
    final = result.get("final_results", {})
    flags = result.get("flags", {"red_flags": [], "warnings": []})

    return {
        "case_id": case_id,
        "category": category,
        "criticality": "critical" if category == "failure_mode" else "normal",
        "inputs": payload,
        "expected_outputs": {
            "drift_rate_pct_per_day": final.get("drift_rate_pct_per_day"),
            "drift_r_squared": final.get("drift_r_squared"),
            "predicted_drift_pct": final.get("predicted_drift_pct"),
            "pfdavg": final.get("pfdavg"),
            "sil_target": final.get("sil_target"),
            "sil_achieved": final.get("sil_achieved"),
            "combined_uncertainty_pct": final.get("combined_uncertainty_pct"),
            "calibration_interval_optimal_days": final.get("calibration_interval_optimal_days"),
            "inspection_interval_days": final.get("inspection_interval_days"),
            "cv_margin_ratio": final.get("cv_margin_ratio"),
            "status": final.get("status"),
        },
        "expected_red_flags": flags.get("red_flags", []),
        "expected_warnings": flags.get("warnings", []),
        "validation_points": [
            "IEC 61511 SIL check context",
            "ISO GUM drift/uncertainty context",
            "Control valve capacity margin check",
        ],
        "standards_referenced": ["IEC 61511", "ISA-TR84.00.02", "ISA 5.1", "ISO GUM"],
    }


def _gen_payload(category: str) -> Dict[str, Any]:
    sil_target = random.choice([1, 2, 3])

    if category == "standard":
        base_slope = random.uniform(0.0006, 0.0018)
        base_intercept = random.uniform(0.02, 0.07)
        return {
            "sil_target": sil_target,
            "failure_rate_per_hour": random.uniform(2.0e-8, 1.0e-7),
            "proof_test_interval_hours": random.choice([4380.0, 8760.0]),
            "mttr_hours": random.choice([6.0, 8.0]),
            "calibration_interval_days": random.choice([90.0, 180.0]),
            "calibration_history": _history(base_slope, base_intercept),
            "tolerance_pct": random.choice([1.0, 1.5]),
            "sensor_mtbf_years": random.uniform(6.0, 12.0),
            "cv_required": random.uniform(30.0, 60.0),
            "cv_rated": random.uniform(85.0, 130.0),
            "uncertainty_components_pct": [0.2, 0.3, 0.1],
        }

    if category == "boundary":
        base_slope = random.uniform(0.0025, 0.0060)
        base_intercept = random.uniform(0.06, 0.12)
        return {
            "sil_target": sil_target,
            "failure_rate_per_hour": random.uniform(2.0e-7, 1.2e-6),
            "proof_test_interval_hours": random.choice([8760.0, 13140.0]),
            "mttr_hours": random.choice([8.0, 12.0]),
            "calibration_interval_days": random.choice([180.0, 270.0]),
            "calibration_history": _history(base_slope, base_intercept),
            "tolerance_pct": random.choice([0.8, 1.0]),
            "sensor_mtbf_years": random.uniform(4.8, 7.0),
            "cv_required": random.uniform(65.0, 90.0),
            "cv_rated": random.uniform(90.0, 110.0),
            "uncertainty_components_pct": [0.25, 0.35, 0.15],
        }

    base_slope = random.uniform(0.008, 0.02)
    base_intercept = random.uniform(0.08, 0.2)
    return {
        "sil_target": sil_target,
        "failure_rate_per_hour": random.uniform(3.0e-6, 2.0e-5),
        "proof_test_interval_hours": random.choice([8760.0, 17520.0]),
        "mttr_hours": random.choice([8.0, 12.0]),
        "calibration_interval_days": random.choice([180.0, 270.0]),
        "calibration_history": _history(base_slope, base_intercept),
        "tolerance_pct": random.choice([0.8, 1.0]),
        "sensor_mtbf_years": random.uniform(2.0, 4.5),
        "cv_required": random.uniform(92.0, 130.0),
        "cv_rated": random.uniform(95.0, 120.0),
        "uncertainty_components_pct": [0.4, 0.5, 0.2],
    }


def _accepted(category: str, red_flags: List[str]) -> bool:
    if category == "standard":
        return len(red_flags) == 0
    if category == "failure_mode":
        return len(red_flags) >= 1
    return True


def generate_dataset(seed: int = 46) -> Dict[str, Any]:
    random.seed(seed)
    service = InstrumentationVerificationService()
    cases: List[Dict[str, Any]] = []
    counts = split_counts(30)
    idx = 1

    for category in ["standard", "boundary", "failure_mode"]:
        for _ in range(counts[category]):
            selected_case = None
            for _attempt in range(200):
                payload = _gen_payload(category)
                case = make_case(f"INS-GOLD-{idx:03d}", category, payload, service)
                reds = case["expected_red_flags"]
                if _accepted(category, reds):
                    selected_case = case
                    break
                selected_case = case
            assert selected_case is not None
            cases.append(selected_case)
            idx += 1

    return {
        "dataset_id": "INSTRUMENTATION_GOLDEN_V1",
        "generated_at": "2026-02-26T00:00:00Z",
        "total_cases": len(cases),
        "category_distribution": counts,
        "cases": cases,
    }


def main() -> int:
    dataset = generate_dataset()
    DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATASET_PATH.write_text(json.dumps(dataset, indent=2), encoding="utf-8")
    print(f"DATASET_WRITTEN={DATASET_PATH}")
    print(f"TOTAL_CASES={dataset['total_cases']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

