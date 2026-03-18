from __future__ import annotations

import json
import pathlib
import random
import sys
from typing import Any, Dict, List

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.vessel.service import VesselVerificationService


DATASET_PATH = ROOT / "datasets" / "golden_standards" / "vessel_golden_dataset_v1.json"


def split_counts(total: int) -> Dict[str, int]:
    standard = int(total * 0.60)
    boundary = int(total * 0.25)
    failure = total - standard - boundary
    return {"standard": standard, "boundary": boundary, "failure_mode": failure}


def make_case(case_id: str, category: str, payload: Dict[str, Any], service: VesselVerificationService) -> Dict[str, Any]:
    result = service.evaluate(payload)
    final = result.get("final_results", {})
    flags = result.get("flags", {"red_flags": [], "warnings": []})

    return {
        "case_id": case_id,
        "category": category,
        "criticality": "critical" if category == "failure_mode" else "normal",
        "inputs": payload,
        "expected_outputs": {
            "t_required_shell_mm": final.get("t_required_shell_mm"),
            "remaining_life_years": final.get("remaining_life_years"),
            "inspection_interval_years": final.get("inspection_interval_years"),
            "corrosion_rate_selected_mm_per_year": final.get("corrosion_rate_selected_mm_per_year"),
        },
        "expected_red_flags": flags.get("red_flags", []),
        "expected_warnings": flags.get("warnings", []),
        "validation_points": [
            "ASME VIII UG-27 shell thickness",
            "API 510 interval policy",
            "Layer-3 vessel physics checks",
        ],
        "standards_referenced": [
            "ASME Section VIII Div.1 UG-27",
            "API 510",
            "API 579-1 Level 1 context",
        ],
    }


def _gen_payload(category: str) -> Dict[str, Any]:
    material = random.choice(["SA-516-70", "SA-240-304"])

    if category == "standard":
        return {
            "material": material,
            "design_pressure_mpa": round(random.uniform(1.0, 4.0), 3),
            "design_temperature_c": round(random.uniform(80.0, 260.0), 1),
            "inside_radius_mm": random.choice([600.0, 750.0]),
            "joint_efficiency": random.choice([1.0, 0.85]),
            "t_current_mm": round(random.uniform(24.0, 55.0), 3),
            "corrosion_allowance_mm": 1.5,
            "assumed_corrosion_rate_mm_per_year": round(random.uniform(0.10, 0.25), 4),
        }

    if category == "boundary":
        return {
            "material": material,
            "design_pressure_mpa": round(random.uniform(3.0, 9.0), 3),
            "design_temperature_c": round(random.uniform(300.0, 500.0), 1),
            "inside_radius_mm": random.choice([750.0, 900.0, 1200.0]),
            "joint_efficiency": random.choice([1.0, 0.85, 0.7]),
            "t_current_mm": round(random.uniform(12.0, 38.0), 3),
            "corrosion_allowance_mm": 1.5,
            "assumed_corrosion_rate_mm_per_year": round(random.uniform(0.18, 0.35), 4),
        }

    return {
        "material": material,
        "design_pressure_mpa": round(random.uniform(8.0, 16.0), 3),
        "design_temperature_c": round(random.uniform(250.0, 520.0), 1),
        "inside_radius_mm": random.choice([900.0, 1200.0]),
        "joint_efficiency": random.choice([0.6, 0.7, 0.85]),
        "t_current_mm": round(random.uniform(6.0, 16.0), 3),
        "corrosion_allowance_mm": 1.5,
        "assumed_corrosion_rate_mm_per_year": round(random.uniform(0.25, 0.45), 4),
    }


def _accepted(category: str, red_flags: List[str]) -> bool:
    if category == "standard":
        return len(red_flags) == 0
    if category == "failure_mode":
        return len(red_flags) >= 1
    return True


def generate_dataset(seed: int = 43) -> Dict[str, Any]:
    random.seed(seed)
    service = VesselVerificationService()
    cases: List[Dict[str, Any]] = []

    counts = split_counts(30)
    idx = 1

    for category in ["standard", "boundary", "failure_mode"]:
        for _ in range(counts[category]):
            selected_case = None
            for _attempt in range(200):
                payload = _gen_payload(category)
                case = make_case(f"VES-GOLD-{idx:03d}", category, payload, service)
                reds = case["expected_red_flags"]
                if _accepted(category, reds):
                    selected_case = case
                    break
                selected_case = case
            assert selected_case is not None
            cases.append(selected_case)
            idx += 1

    return {
        "dataset_id": "VESSEL_GOLDEN_V1",
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

