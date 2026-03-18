from __future__ import annotations

import json
import pathlib
import random
import sys
from typing import Any, Dict, List

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.electrical.service import ElectricalVerificationService


DATASET_PATH = ROOT / "datasets" / "golden_standards" / "electrical_golden_dataset_v1.json"


def split_counts(total: int) -> Dict[str, int]:
    standard = int(total * 0.60)
    boundary = int(total * 0.25)
    failure = total - standard - boundary
    return {"standard": standard, "boundary": boundary, "failure_mode": failure}


def make_case(case_id: str, category: str, payload: Dict[str, Any], service: ElectricalVerificationService) -> Dict[str, Any]:
    result = service.evaluate(payload)
    final = result.get("final_results", {})
    flags = result.get("flags", {"red_flags": [], "warnings": []})

    return {
        "case_id": case_id,
        "category": category,
        "criticality": "critical" if category == "failure_mode" else "normal",
        "inputs": payload,
        "expected_outputs": {
            "transformer_health_index": final.get("transformer_health_index"),
            "arc_flash_energy_cal_cm2": final.get("arc_flash_energy_cal_cm2"),
            "ppe_category": final.get("ppe_category"),
            "voltage_drop_percent": final.get("voltage_drop_percent"),
            "fault_current_ka": final.get("fault_current_ka"),
            "breaker_interrupt_rating_ka": final.get("breaker_interrupt_rating_ka"),
            "thd_voltage_percent": final.get("thd_voltage_percent"),
            "motor_current_thd_percent": final.get("motor_current_thd_percent"),
            "power_factor": final.get("power_factor"),
            "inspection_interval_years": final.get("inspection_interval_years"),
            "status": final.get("status"),
        },
        "expected_red_flags": flags.get("red_flags", []),
        "expected_warnings": flags.get("warnings", []),
        "validation_points": [
            "IEEE C57.104 health index context",
            "IEEE 1584 arc-flash context",
            "NFPA 70E safety categorization context",
        ],
        "standards_referenced": ["IEEE C57.104", "IEEE 1584-2018", "IEEE 3002", "NFPA 70E"],
    }


def _gen_payload(category: str) -> Dict[str, Any]:
    if category == "standard":
        return {
            "system_voltage_kv": random.choice([4.16, 6.6, 13.8]),
            "bolted_fault_current_ka": round(random.uniform(10.0, 24.0), 3),
            "clearing_time_sec": round(random.uniform(0.08, 0.22), 3),
            "working_distance_mm": random.choice([455.0, 610.0, 750.0]),
            "breaker_interrupt_rating_ka": random.choice([25.0, 31.5, 40.0, 50.0]),
            "voltage_drop_percent": round(random.uniform(1.5, 4.5), 3),
            "thd_voltage_percent": round(random.uniform(2.0, 6.5), 3),
            "dga_score": round(random.uniform(7.0, 9.2), 3),
            "oil_quality_score": round(random.uniform(7.0, 9.2), 3),
            "insulation_score": round(random.uniform(7.0, 9.2), 3),
            "load_factor_score": round(random.uniform(6.5, 8.8), 3),
            "motor_current_thd_percent": round(random.uniform(2.0, 4.8), 3),
            "power_factor": round(random.uniform(0.88, 0.98), 3),
        }

    if category == "boundary":
        return {
            "system_voltage_kv": random.choice([6.6, 13.8]),
            "bolted_fault_current_ka": round(random.uniform(20.0, 42.0), 3),
            "clearing_time_sec": round(random.uniform(0.18, 0.35), 3),
            "working_distance_mm": random.choice([455.0, 610.0]),
            "breaker_interrupt_rating_ka": random.choice([25.0, 31.5, 40.0]),
            "voltage_drop_percent": round(random.uniform(4.2, 6.2), 3),
            "thd_voltage_percent": round(random.uniform(7.0, 9.2), 3),
            "dga_score": round(random.uniform(4.5, 6.8), 3),
            "oil_quality_score": round(random.uniform(4.5, 6.8), 3),
            "insulation_score": round(random.uniform(4.5, 6.8), 3),
            "load_factor_score": round(random.uniform(4.5, 6.8), 3),
            "motor_current_thd_percent": round(random.uniform(4.5, 6.5), 3),
            "power_factor": round(random.uniform(0.82, 0.90), 3),
        }

    return {
        "system_voltage_kv": random.choice([6.6, 13.8]),
        "bolted_fault_current_ka": round(random.uniform(45.0, 80.0), 3),
        "clearing_time_sec": round(random.uniform(0.35, 0.9), 3),
        "working_distance_mm": random.choice([455.0, 610.0]),
        "breaker_interrupt_rating_ka": random.choice([25.0, 31.5, 40.0]),
        "voltage_drop_percent": round(random.uniform(5.5, 8.5), 3),
        "thd_voltage_percent": round(random.uniform(8.5, 12.5), 3),
        "dga_score": round(random.uniform(1.2, 3.2), 3),
        "oil_quality_score": round(random.uniform(1.2, 3.2), 3),
        "insulation_score": round(random.uniform(1.2, 3.2), 3),
        "load_factor_score": round(random.uniform(1.2, 3.2), 3),
        "motor_current_thd_percent": round(random.uniform(6.0, 12.0), 3),
        "power_factor": round(random.uniform(0.70, 0.85), 3),
    }


def _accepted(category: str, red_flags: List[str]) -> bool:
    if category == "standard":
        return len(red_flags) == 0
    if category == "failure_mode":
        return len(red_flags) >= 1
    return True


def generate_dataset(seed: int = 45) -> Dict[str, Any]:
    random.seed(seed)
    service = ElectricalVerificationService()
    cases: List[Dict[str, Any]] = []
    counts = split_counts(30)
    idx = 1

    for category in ["standard", "boundary", "failure_mode"]:
        for _ in range(counts[category]):
            selected_case = None
            for _attempt in range(200):
                payload = _gen_payload(category)
                case = make_case(f"ELE-GOLD-{idx:03d}", category, payload, service)
                reds = case["expected_red_flags"]
                if _accepted(category, reds):
                    selected_case = case
                    break
                selected_case = case
            assert selected_case is not None
            cases.append(selected_case)
            idx += 1

    return {
        "dataset_id": "ELECTRICAL_GOLDEN_V1",
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

