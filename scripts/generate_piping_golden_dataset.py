from __future__ import annotations

import json
import pathlib
import random
import sys
from typing import Any, Dict, List

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.piping.service import PipingVerificationService


DATASET_PATH = ROOT / "datasets" / "golden_standards" / "piping_golden_dataset_v1.json"


def history_three_points(base_mm: float, cr_long: float, cr_short: float) -> List[Dict[str, Any]]:
    # 2015 -> 2020 -> 2025
    t0 = base_mm
    t1 = t0 - cr_long * 5.0
    t2 = t1 - cr_short * 5.0
    return [
        {"date": "2015-01-01", "thickness_mm": round(t0, 4)},
        {"date": "2020-01-01", "thickness_mm": round(t1, 4)},
        {"date": "2025-01-01", "thickness_mm": round(max(t2, 0.5), 4)},
    ]


def make_case(case_id: str, category: str, payload: Dict[str, Any], service: PipingVerificationService) -> Dict[str, Any]:
    result = service.evaluate(payload)
    final = result.get("final_results", {})
    flags = result.get("flags", {"red_flags": [], "warnings": []})

    expected_outputs = {
        "t_min_mm": final.get("t_min_mm"),
        "CR_long_term": final.get("cr_long_term_mm_per_year"),
        "CR_short_term": final.get("cr_short_term_mm_per_year"),
        "CR_selected": final.get("cr_selected_mm_per_year"),
        "RL_years": final.get("remaining_life_years"),
        "inspection_interval_years": final.get("inspection_interval_years"),
    }

    validation_points = []
    for step in result.get("calculation_steps", []):
        if isinstance(step, dict):
            ref = step.get("standard_reference")
            if ref:
                validation_points.append(str(ref))

    confidence = result.get("calculation_summary", {}).get("confidence", "low")

    return {
        "case_id": case_id,
        "category": category,
        "criticality": "critical" if category == "failure_mode" else "normal",
        "inputs": payload,
        "expected_outputs": expected_outputs,
        "expected_red_flags": flags.get("red_flags", []),
        "expected_warnings": flags.get("warnings", []),
        "validation_points": validation_points[:4],
        "expected_confidence": confidence,
    }


def generate_dataset(seed: int = 42) -> Dict[str, Any]:
    random.seed(seed)
    service = PipingVerificationService()

    materials = ["SA-106 Gr.B", "SA-53 Gr.B", "SA-312 TP304", "SA-312 TP316"]
    nps_options = [4.0, 6.0, 8.0, 10.0, 12.0]

    cases: List[Dict[str, Any]] = []
    idx = 1

    # Standard cases (20) - intended to be healthy baseline
    for _ in range(20):
        material = random.choice(materials)
        payload = {
            "material": material,
            "nps": random.choice([4.0, 6.0, 8.0]),
            "design_pressure_mpa": round(random.uniform(0.8, 3.5), 3),
            "design_temperature_c": round(random.uniform(50.0, 300.0), 1),
            "thickness_history": history_three_points(
                base_mm=round(random.uniform(12.0, 22.0), 3),
                cr_long=round(random.uniform(0.08, 0.25), 4),
                cr_short=round(random.uniform(0.10, 0.30), 4),
            ),
            "corrosion_allowance_mm": 1.5,
            "weld_type": random.choice(["seamless", "erw", "smaw"]),
            "service_type": "general",
            "has_internal_coating": False,
        }
        cases.append(make_case(f"PIP-GOLD-{idx:03d}", "standard", payload, service))
        idx += 1

    # Boundary cases (15)
    for i in range(15):
        material = "SA-106 Gr.B" if i % 2 == 0 else random.choice(materials)
        temp = [424.0, -49.0, 649.0, 420.0, 425.0][i % 5]
        pressure = [19.5, 0.2, 20.0, 15.0, 49.5][i % 5]
        payload = {
            "material": material,
            "nps": random.choice([6.0, 8.0, 10.0, 12.0]),
            "design_pressure_mpa": pressure,
            "design_temperature_c": temp,
            "thickness_history": history_three_points(
                base_mm=round(random.uniform(7.5, 12.0), 3),
                cr_long=round(random.uniform(0.05, 0.5), 4),
                cr_short=round(random.uniform(0.05, 0.6), 4),
            ),
            "corrosion_allowance_mm": 1.5,
            "weld_type": random.choice(["seamless", "erw", "smaw"]),
            "service_type": "general",
            "has_internal_coating": False,
        }
        cases.append(make_case(f"PIP-GOLD-{idx:03d}", "boundary", payload, service))
        idx += 1

    # Failure modes (10)
    for i in range(10):
        failure_type = i % 4
        payload: Dict[str, Any]

        if failure_type == 0:
            # Negative corrosion rate without coating
            payload = {
                "material": "SA-106 Gr.B",
                "nps": 6.0,
                "design_pressure_mpa": 4.5,
                "design_temperature_c": 220.0,
                "thickness_history": [
                    {"date": "2015-01-01", "thickness_mm": 8.0},
                    {"date": "2020-01-01", "thickness_mm": 8.6},
                    {"date": "2025-01-01", "thickness_mm": 9.1},
                ],
                "corrosion_allowance_mm": 1.5,
                "weld_type": "erw",
                "service_type": "general",
                "has_internal_coating": False,
            }
        elif failure_type == 1:
            # Current thickness below minimum (high pressure + thin wall)
            payload = {
                "material": "SA-106 Gr.B",
                "nps": 12.0,
                "design_pressure_mpa": 20.0,
                "design_temperature_c": 300.0,
                "thickness_history": [
                    {"date": "2015-01-01", "thickness_mm": 6.5},
                    {"date": "2020-01-01", "thickness_mm": 5.5},
                    {"date": "2025-01-01", "thickness_mm": 4.4},
                ],
                "corrosion_allowance_mm": 1.5,
                "weld_type": "smaw",
                "service_type": "general",
                "has_internal_coating": False,
            }
        elif failure_type == 2:
            # Temperature beyond carbon steel limit
            payload = {
                "material": "SA-106 Gr.B",
                "nps": 8.0,
                "design_pressure_mpa": 6.0,
                "design_temperature_c": 500.0,
                "thickness_history": history_three_points(10.0, 0.2, 0.24),
                "corrosion_allowance_mm": 1.5,
                "weld_type": "seamless",
                "service_type": "general",
                "has_internal_coating": False,
            }
        else:
            # Unrealistic remaining life
            payload = {
                "material": "SA-312 TP316",
                "nps": 4.0,
                "design_pressure_mpa": 1.2,
                "design_temperature_c": 80.0,
                "thickness_history": history_three_points(20.0, 0.01, 0.01),
                "corrosion_allowance_mm": 1.5,
                "weld_type": "seamless",
                "service_type": "general",
                "has_internal_coating": True,
            }

        cases.append(make_case(f"PIP-GOLD-{idx:03d}", "failure_mode", payload, service))
        idx += 1

    # Composite environments (5) - mixed stressors, not always failing
    for i in range(5):
        material = "SA-312 TP304" if i % 2 == 0 else "SA-106 Gr.B"
        chloride_ppm = 60.0 if material.startswith("SA-312") else 300.0
        if i in {1, 3}:
            chloride_ppm = 20.0 if material.startswith("SA-312") else 200.0
        payload = {
            "material": material,
            "nps": random.choice([4.0, 6.0, 8.0]),
            "design_pressure_mpa": round(random.uniform(3.0, 8.0), 3),
            "design_temperature_c": round(random.uniform(180.0, 380.0), 1),
            "thickness_history": history_three_points(
                base_mm=round(random.uniform(14.0, 22.0), 3),
                cr_long=round(random.uniform(0.12, 0.45), 4),
                cr_short=round(random.uniform(0.15, 0.60), 4),
            ),
            "corrosion_allowance_mm": 1.5,
            "weld_type": random.choice(["erw", "smaw"]),
            "service_type": "sour_chloride_high_temp",
            "has_internal_coating": False,
            "chloride_ppm": chloride_ppm,
        }
        cases.append(make_case(f"PIP-GOLD-{idx:03d}", "composite", payload, service))
        idx += 1

    return {
        "dataset_id": "PIPING_GOLDEN_V1",
        "generated_at": "2026-02-26T00:00:00Z",
        "total_cases": len(cases),
        "category_distribution": {
            "standard": 20,
            "boundary": 15,
            "failure_mode": 10,
            "composite": 5,
        },
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
