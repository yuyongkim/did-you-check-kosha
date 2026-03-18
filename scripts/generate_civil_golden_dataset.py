from __future__ import annotations

import json
import pathlib
import random
import sys
from typing import Any, Dict, List

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.civil.service import CivilVerificationService


DATASET_PATH = ROOT / "datasets" / "golden_standards" / "civil_golden_dataset_v1.json"


def split_counts(total: int) -> Dict[str, int]:
    standard = int(total * 0.60)
    boundary = int(total * 0.25)
    failure = total - standard - boundary
    return {"standard": standard, "boundary": boundary, "failure_mode": failure}


def make_case(case_id: str, category: str, payload: Dict[str, Any], service: CivilVerificationService) -> Dict[str, Any]:
    result = service.evaluate(payload)
    final = result.get("final_results", {})
    flags = result.get("flags", {"red_flags": [], "warnings": []})

    return {
        "case_id": case_id,
        "category": category,
        "criticality": "critical" if category == "failure_mode" else "normal",
        "inputs": payload,
        "expected_outputs": {
            "a_mm": final.get("a_mm"),
            "phi_mn_knm": final.get("phi_mn_knm"),
            "dc_ratio": final.get("dc_ratio"),
            "carbonation_depth_mm": final.get("carbonation_depth_mm"),
            "substantial_damage": final.get("substantial_damage"),
            "damage_mode": final.get("damage_mode"),
            "corrosion_initiated": final.get("corrosion_initiated"),
            "years_to_corrosion_init": final.get("years_to_corrosion_init"),
            "crack_width_mm": final.get("crack_width_mm"),
            "spalling_area_percent": final.get("spalling_area_percent"),
            "foundation_settlement_mm": final.get("foundation_settlement_mm"),
            "inspection_interval_years": final.get("inspection_interval_years"),
            "status": final.get("status"),
        },
        "expected_red_flags": flags.get("red_flags", []),
        "expected_warnings": flags.get("warnings", []),
        "validation_points": [
            "ACI 562 substantial damage screening context",
            "ACI 318 flexure capacity context",
            "Carbonation and durability context",
        ],
        "standards_referenced": ["ACI 318", "ACI 562"],
    }


def _gen_payload(category: str) -> Dict[str, Any]:
    if category == "standard":
        return {
            "element_type": random.choice(["beam", "column", "slab"]),
            "fc_mpa": round(random.uniform(28.0, 45.0), 3),
            "fy_mpa": round(random.uniform(380.0, 500.0), 3),
            "width_mm": round(random.uniform(250.0, 450.0), 3),
            "effective_depth_mm": round(random.uniform(450.0, 700.0), 3),
            "rebar_area_mm2": round(random.uniform(1600.0, 3200.0), 3),
            "demand_moment_knm": round(random.uniform(120.0, 320.0), 3),
            "lateral_capacity_loss_percent": round(random.uniform(0.0, 15.0), 3),
            "affected_area_percent": round(random.uniform(0.0, 20.0), 3),
            "vertical_capacity_loss_percent": round(random.uniform(0.0, 12.0), 3),
            "carbonation_coeff_mm_sqrt_year": round(random.uniform(1.2, 2.4), 3),
            "service_years": round(random.uniform(8.0, 22.0), 3),
            "cover_thickness_mm": round(random.uniform(38.0, 55.0), 3),
            "crack_width_mm": round(random.uniform(0.05, 0.28), 3),
            "spalling_area_percent": round(random.uniform(0.0, 10.0), 3),
            "foundation_settlement_mm": round(random.uniform(0.0, 12.0), 3),
        }

    if category == "boundary":
        return {
            "element_type": random.choice(["beam", "column", "foundation"]),
            "fc_mpa": round(random.uniform(22.0, 35.0), 3),
            "fy_mpa": round(random.uniform(350.0, 450.0), 3),
            "width_mm": round(random.uniform(250.0, 450.0), 3),
            "effective_depth_mm": round(random.uniform(420.0, 680.0), 3),
            "rebar_area_mm2": round(random.uniform(1500.0, 3000.0), 3),
            "demand_moment_knm": round(random.uniform(250.0, 520.0), 3),
            "lateral_capacity_loss_percent": round(random.uniform(20.0, 34.0), 3),
            "affected_area_percent": round(random.uniform(20.0, 35.0), 3),
            "vertical_capacity_loss_percent": round(random.uniform(14.0, 22.0), 3),
            "carbonation_coeff_mm_sqrt_year": round(random.uniform(2.0, 3.8), 3),
            "service_years": round(random.uniform(20.0, 35.0), 3),
            "cover_thickness_mm": round(random.uniform(32.0, 45.0), 3),
            "crack_width_mm": round(random.uniform(0.25, 0.46), 3),
            "spalling_area_percent": round(random.uniform(8.0, 22.0), 3),
            "foundation_settlement_mm": round(random.uniform(10.0, 28.0), 3),
        }

    return {
        "element_type": random.choice(["foundation", "column"]),
        "fc_mpa": round(random.uniform(18.0, 30.0), 3),
        "fy_mpa": round(random.uniform(350.0, 450.0), 3),
        "width_mm": round(random.uniform(250.0, 420.0), 3),
        "effective_depth_mm": round(random.uniform(420.0, 650.0), 3),
        "rebar_area_mm2": round(random.uniform(1400.0, 2600.0), 3),
        "demand_moment_knm": round(random.uniform(500.0, 950.0), 3),
        "lateral_capacity_loss_percent": round(random.uniform(33.0, 55.0), 3),
        "affected_area_percent": round(random.uniform(30.0, 55.0), 3),
        "vertical_capacity_loss_percent": round(random.uniform(20.0, 45.0), 3),
        "carbonation_coeff_mm_sqrt_year": round(random.uniform(3.0, 5.5), 3),
        "service_years": round(random.uniform(25.0, 45.0), 3),
        "cover_thickness_mm": round(random.uniform(30.0, 40.0), 3),
        "crack_width_mm": round(random.uniform(0.42, 0.85), 3),
        "spalling_area_percent": round(random.uniform(20.0, 45.0), 3),
        "foundation_settlement_mm": round(random.uniform(25.0, 60.0), 3),
    }


def _accepted(category: str, red_flags: List[str]) -> bool:
    if category == "standard":
        return len(red_flags) == 0
    if category == "failure_mode":
        return len(red_flags) >= 1
    return True


def generate_dataset(seed: int = 48) -> Dict[str, Any]:
    random.seed(seed)
    service = CivilVerificationService()
    cases: List[Dict[str, Any]] = []
    counts = split_counts(25)
    idx = 1

    for category in ["standard", "boundary", "failure_mode"]:
        for _ in range(counts[category]):
            selected_case = None
            for _attempt in range(250):
                payload = _gen_payload(category)
                case = make_case(f"CIV-GOLD-{idx:03d}", category, payload, service)
                reds = case["expected_red_flags"]
                if _accepted(category, reds):
                    selected_case = case
                    break
                selected_case = case
            assert selected_case is not None
            cases.append(selected_case)
            idx += 1

    return {
        "dataset_id": "CIVIL_GOLDEN_V1",
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
