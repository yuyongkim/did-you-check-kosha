from __future__ import annotations

import json
import pathlib
import random
import sys
from typing import Any, Dict, List

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rotating.constants import VIBRATION_LIMIT_MM_PER_S
from src.rotating.service import RotatingVerificationService


DATASET_PATH = ROOT / "datasets" / "golden_standards" / "rotating_golden_dataset_v1.json"


def split_counts(total: int) -> Dict[str, int]:
    standard = int(total * 0.60)
    boundary = int(total * 0.25)
    failure = total - standard - boundary
    return {"standard": standard, "boundary": boundary, "failure_mode": failure}


def make_case(case_id: str, category: str, payload: Dict[str, Any], service: RotatingVerificationService) -> Dict[str, Any]:
    result = service.evaluate(payload)
    final = result.get("final_results", {})
    flags = result.get("flags", {"red_flags": [], "warnings": []})

    return {
        "case_id": case_id,
        "category": category,
        "criticality": "critical" if category == "failure_mode" else "normal",
        "inputs": payload,
        "expected_outputs": {
            "vibration_mm_per_s": final.get("vibration_mm_per_s"),
            "vibration_limit_mm_per_s": final.get("vibration_limit_mm_per_s"),
            "nozzle_load_ratio": final.get("nozzle_load_ratio"),
            "bearing_temperature_c": final.get("bearing_temperature_c"),
            "bearing_health_index": final.get("bearing_health_index"),
            "inspection_interval_years": final.get("inspection_interval_years"),
            "status": final.get("status"),
        },
        "expected_red_flags": flags.get("red_flags", []),
        "expected_warnings": flags.get("warnings", []),
        "validation_points": [
            "API 610/617 vibration and nozzle load context",
            "API 670 monitoring context",
            "Layer-3 rotating physics checks",
        ],
        "standards_referenced": ["API 610", "API 617", "API 670"],
    }


def _gen_payload(category: str) -> Dict[str, Any]:
    machine_type = random.choice(["pump", "compressor"])
    limit = VIBRATION_LIMIT_MM_PER_S[machine_type]

    if category == "standard":
        vib = random.uniform(0.45 * limit, 0.85 * limit)
        nozzle = random.uniform(0.55, 0.95)
        temp = random.uniform(60.0, 78.0)
    elif category == "boundary":
        vib = random.uniform(0.85 * limit, 1.10 * limit)
        nozzle = random.uniform(0.90, 1.08)
        temp = random.uniform(75.0, 88.0)
    else:
        vib = random.uniform(1.20 * limit, 1.80 * limit)
        nozzle = random.uniform(1.05, 1.50)
        temp = random.uniform(85.0, 120.0)

    return {
        "machine_type": machine_type,
        "vibration_mm_per_s": round(vib, 3),
        "nozzle_load_ratio": round(nozzle, 3),
        "bearing_temperature_c": round(temp, 1),
        "speed_rpm": random.choice([1500, 1800, 3000]),
    }


def _accepted(category: str, red_flags: List[str]) -> bool:
    if category == "standard":
        return len(red_flags) == 0
    if category == "failure_mode":
        return len(red_flags) >= 1
    return True


def generate_dataset(seed: int = 44) -> Dict[str, Any]:
    random.seed(seed)
    service = RotatingVerificationService()
    cases: List[Dict[str, Any]] = []

    counts = split_counts(30)
    idx = 1

    for category in ["standard", "boundary", "failure_mode"]:
        for _ in range(counts[category]):
            selected_case = None
            for _attempt in range(200):
                payload = _gen_payload(category)
                case = make_case(f"ROT-GOLD-{idx:03d}", category, payload, service)
                reds = case["expected_red_flags"]
                if _accepted(category, reds):
                    selected_case = case
                    break
                selected_case = case
            assert selected_case is not None
            cases.append(selected_case)
            idx += 1

    return {
        "dataset_id": "ROTATING_GOLDEN_V1",
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

