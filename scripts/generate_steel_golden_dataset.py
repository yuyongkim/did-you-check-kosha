from __future__ import annotations

import json
import pathlib
import random
import sys
from typing import Any, Dict, List

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.steel.service import SteelVerificationService


DATASET_PATH = ROOT / "datasets" / "golden_standards" / "steel_golden_dataset_v1.json"


def split_counts(total: int) -> Dict[str, int]:
    standard = int(total * 0.60)
    boundary = int(total * 0.25)
    failure = total - standard - boundary
    return {"standard": standard, "boundary": boundary, "failure_mode": failure}


def make_case(case_id: str, category: str, payload: Dict[str, Any], service: SteelVerificationService) -> Dict[str, Any]:
    result = service.evaluate(payload)
    final = result.get("final_results", {})
    flags = result.get("flags", {"red_flags": [], "warnings": []})

    return {
        "case_id": case_id,
        "category": category,
        "criticality": "critical" if category == "failure_mode" else "normal",
        "inputs": payload,
        "expected_outputs": {
            "reduced_area_mm2": final.get("reduced_area_mm2"),
            "lambda_c": final.get("lambda_c"),
            "fcr_mpa": final.get("fcr_mpa"),
            "phi_pn_kn": final.get("phi_pn_kn"),
            "dc_ratio": final.get("dc_ratio"),
            "deflection_ratio": final.get("deflection_ratio"),
            "corrosion_loss_percent": final.get("corrosion_loss_percent"),
            "inspection_interval_years": final.get("inspection_interval_years"),
            "status": final.get("status"),
        },
        "expected_red_flags": flags.get("red_flags", []),
        "expected_warnings": flags.get("warnings", []),
        "validation_points": [
            "AISC compression strength context",
            "D/C utilization and deflection checks",
            "Section-loss and connection integrity checks",
        ],
        "standards_referenced": ["AISC 360"],
    }


def _gen_payload(category: str) -> Dict[str, Any]:
    if category == "standard":
        span_mm = random.uniform(5000.0, 8000.0)
        allowable_deflection = span_mm / 240.0
        return {
            "member_type": random.choice(["column", "beam", "brace"]),
            "section_label": random.choice(["W310x60", "W360x72", "H300x300"]),
            "length_m": round(random.uniform(4.5, 8.5), 3),
            "k_factor": round(random.uniform(0.8, 1.1), 3),
            "radius_of_gyration_mm": round(random.uniform(70.0, 120.0), 3),
            "yield_strength_mpa": round(random.uniform(280.0, 380.0), 3),
            "elasticity_mpa": 200000.0,
            "gross_area_mm2": round(random.uniform(5200.0, 9800.0), 3),
            "corrosion_loss_percent": round(random.uniform(0.0, 18.0), 3),
            "axial_demand_kn": round(random.uniform(300.0, 950.0), 3),
            "moment_demand_knm": round(random.uniform(20.0, 120.0), 3),
            "deflection_mm": round(random.uniform(0.2, allowable_deflection * 0.85), 3),
            "span_mm": round(span_mm, 3),
            "connection_failure_detected": False,
        }

    if category == "boundary":
        span_mm = random.uniform(5000.0, 9000.0)
        allowable_deflection = span_mm / 240.0
        return {
            "member_type": random.choice(["column", "beam", "brace"]),
            "section_label": random.choice(["W250x33", "W310x38", "H250x250"]),
            "length_m": round(random.uniform(6.0, 11.0), 3),
            "k_factor": round(random.uniform(1.0, 1.3), 3),
            "radius_of_gyration_mm": round(random.uniform(45.0, 85.0), 3),
            "yield_strength_mpa": round(random.uniform(250.0, 355.0), 3),
            "elasticity_mpa": 200000.0,
            "gross_area_mm2": round(random.uniform(3800.0, 7000.0), 3),
            "corrosion_loss_percent": round(random.uniform(15.0, 45.0), 3),
            "axial_demand_kn": round(random.uniform(800.0, 1800.0), 3),
            "moment_demand_knm": round(random.uniform(60.0, 220.0), 3),
            "deflection_mm": round(random.uniform(allowable_deflection * 0.8, allowable_deflection * 1.2), 3),
            "span_mm": round(span_mm, 3),
            "connection_failure_detected": random.choice([False, False, True]),
        }

    span_mm = random.uniform(6000.0, 10000.0)
    allowable_deflection = span_mm / 240.0
    return {
        "member_type": random.choice(["column", "beam", "brace"]),
        "section_label": random.choice(["W200x22", "W250x28", "H200x200"]),
        "length_m": round(random.uniform(8.0, 14.0), 3),
        "k_factor": round(random.uniform(1.1, 1.5), 3),
        "radius_of_gyration_mm": round(random.uniform(30.0, 65.0), 3),
        "yield_strength_mpa": round(random.uniform(240.0, 330.0), 3),
        "elasticity_mpa": 200000.0,
        "gross_area_mm2": round(random.uniform(2500.0, 5200.0), 3),
        "corrosion_loss_percent": round(random.uniform(45.0, 70.0), 3),
        "axial_demand_kn": round(random.uniform(1600.0, 3200.0), 3),
        "moment_demand_knm": round(random.uniform(150.0, 360.0), 3),
        "deflection_mm": round(random.uniform(allowable_deflection * 1.1, allowable_deflection * 1.8), 3),
        "span_mm": round(span_mm, 3),
        "connection_failure_detected": True,
    }


def _accepted(category: str, red_flags: List[str]) -> bool:
    if category == "standard":
        return len(red_flags) == 0
    if category == "failure_mode":
        return len(red_flags) >= 1
    return True


def generate_dataset(seed: int = 47) -> Dict[str, Any]:
    random.seed(seed)
    service = SteelVerificationService()
    cases: List[Dict[str, Any]] = []
    counts = split_counts(25)
    idx = 1

    for category in ["standard", "boundary", "failure_mode"]:
        for _ in range(counts[category]):
            selected_case = None
            for _attempt in range(200):
                payload = _gen_payload(category)
                case = make_case(f"STL-GOLD-{idx:03d}", category, payload, service)
                reds = case["expected_red_flags"]
                if _accepted(category, reds):
                    selected_case = case
                    break
                selected_case = case
            assert selected_case is not None
            cases.append(selected_case)
            idx += 1

    return {
        "dataset_id": "STEEL_GOLDEN_V1",
        "generated_at": "2026-02-27T00:00:00Z",
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
