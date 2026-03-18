from __future__ import annotations

import json
import pathlib
import random
from typing import Any, Dict, List

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLDEN_DIR = ROOT / "golden"


def split_counts(total: int) -> Dict[str, int]:
    standard = int(total * 0.60)
    boundary = int(total * 0.25)
    failure = int(total * 0.15)
    assigned = standard + boundary + failure
    remainder = total - assigned
    # Allocate residual cases to boundary first, then failure, then standard.
    if remainder > 0:
        add_boundary = min(1, remainder)
        boundary += add_boundary
        remainder -= add_boundary
    if remainder > 0:
        add_failure = min(1, remainder)
        failure += add_failure
        remainder -= add_failure
    if remainder > 0:
        standard += remainder
    return {"standard": standard, "boundary": boundary, "failure_mode": failure}


def gen_piping_case(case_id: str, category: str) -> Dict[str, Any]:
    material = random.choice(["SA-106 Gr.B", "SA-53 Gr.B", "SA-312 TP304"])
    nps = random.choice([4, 6, 8, 10, 12])
    pressure = round(random.uniform(1.0, 20.0), 3)
    temp = round(random.uniform(-40, 450), 1)

    t0 = round(random.uniform(8.0, 18.0), 3)
    cr_long = round(random.uniform(0.08, 0.55), 4)
    cr_short = round(random.uniform(0.10, 0.70), 4)
    t1 = round(t0 - cr_long * 5, 3)
    t2 = round(t1 - cr_short * 5, 3)

    if category == "failure_mode":
        t2 = round(max(0.8, t2 - 1.8), 3)

    expected_t_min = round((pressure * (168.3 if nps == 6 else 114.3)) / 220 + 1.5, 3)
    cr_selected = max(cr_long, cr_short)
    rl = round((t2 - expected_t_min) / max(cr_selected, 1e-6), 3)

    red_flags: List[str] = []
    if t2 < expected_t_min:
        red_flags.append("PHY.CURRENT_THICKNESS_BELOW_MINIMUM")
    if material in {"SA-106 Gr.B", "SA-53 Gr.B"} and temp > 425:
        red_flags.append("PHY.TEMPERATURE_LIMIT_EXCEEDED")
    if category == "failure_mode" and not red_flags:
        red_flags.append("PHY.UNREALISTIC_CORROSION_RATE")

    return {
        "case_id": case_id,
        "discipline": "piping",
        "category": category,
        "subtype": f"{material}-NPS{nps}",
        "inputs": {
            "material": material,
            "NPS": nps,
            "design_pressure_MPa": pressure,
            "design_temperature_C": temp,
            "thickness_history": [
                {"date": "2015-01-01", "thickness_mm": t0},
                {"date": "2020-01-01", "thickness_mm": t1},
                {"date": "2025-01-01", "thickness_mm": t2}
            ],
            "CA_mm": 1.5
        },
        "expected_outputs": {
            "t_min_mm": expected_t_min,
            "CR_long": cr_long,
            "CR_short": cr_short,
            "CR_selected": cr_selected,
            "RL_years": rl,
            "inspection_interval_years": max(0.1, round(min(10.0, 0.5 * max(rl, 0.0)), 3)),
            "status": "CRITICAL" if red_flags else "NORMAL"
        },
        "validation_points": [
            "ASME B31.3 thickness equation context",
            "API 570 corrosion and RL context",
            "Layer-3 red-flag evaluation"
        ],
        "standards_referenced": [
            "ASME B31.3 Para 304.1.2",
            "ASME B31.3 Table A-1",
            "API 570 Section 7"
        ],
        "criticality_level": "safety" if red_flags else "normal",
        "cross_discipline_checks": [
            "vessel_nozzle_interface_check",
            "rotating_nozzle_load_coupling_check"
        ],
        "expected_red_flags": red_flags
    }


def gen_vessel_case(case_id: str, category: str) -> Dict[str, Any]:
    material = random.choice(["SA-516-70", "SA-240-304"])
    radius_mm = random.choice([600, 750, 900, 1200])
    pressure = round(random.uniform(0.8, 12.0), 3)
    temp = round(random.uniform(20, 420), 1)
    e = random.choice([1.0, 0.85])
    s_allow = 138.0 if material == "SA-240-304" else 120.0

    t_required = round((pressure * radius_mm) / max((s_allow * e - 0.6 * pressure), 1e-6) + 1.5, 3)
    t_current = round(t_required + random.uniform(-2.0, 5.0), 3)
    if category == "failure_mode":
        t_current = round(t_required - random.uniform(0.2, 2.5), 3)

    red_flags: List[str] = []
    if t_current < t_required:
        red_flags.append("PHY.CURRENT_THICKNESS_BELOW_MINIMUM")

    return {
        "case_id": case_id,
        "discipline": "vessel",
        "category": category,
        "subtype": f"{material}-shell",
        "inputs": {
            "material": material,
            "design_pressure_MPa": pressure,
            "design_temperature_C": temp,
            "inside_radius_mm": radius_mm,
            "joint_efficiency": e,
            "t_current_mm": t_current,
            "CA_mm": 1.5
        },
        "expected_outputs": {
            "t_required_shell_mm": t_required,
            "remaining_life_years": round(max((t_current - t_required) / 0.2, 0.0), 3),
            "inspection_interval_years": round(min(10.0, max((t_current - t_required) / 0.4, 0.1)), 3),
            "status": "CRITICAL" if red_flags else "NORMAL"
        },
        "validation_points": [
            "ASME VIII UG-27 shell equation",
            "API 510 inspection interval context",
            "FFS screening trigger check"
        ],
        "standards_referenced": [
            "ASME Section VIII Div.1 UG-27",
            "API 510",
            "API 579-1 Level 1 context"
        ],
        "criticality_level": "safety" if red_flags else "normal",
        "cross_discipline_checks": [
            "piping_vessel_nozzle_thickness_consistency"
        ],
        "expected_red_flags": red_flags
    }


def gen_rotating_case(case_id: str, category: str) -> Dict[str, Any]:
    machine = random.choice(["pump", "compressor"])
    vibration_limit = 3.0 if machine == "pump" else 4.5
    vibration = round(random.uniform(1.0, 6.5), 3)
    nozzle_load_ratio = round(random.uniform(0.4, 1.3), 3)
    bearing_temp = round(random.uniform(55, 95), 1)

    if category == "failure_mode":
        vibration = round(random.uniform(4.5, 8.0), 3)
        nozzle_load_ratio = round(random.uniform(1.05, 1.6), 3)

    red_flags: List[str] = []
    if vibration > vibration_limit:
        red_flags.append("STD.OUT_OF_SCOPE_APPLICATION")
    if nozzle_load_ratio > 1.0:
        red_flags.append("PHY.ALLOWABLE_STRESS_EXCEEDED")

    return {
        "case_id": case_id,
        "discipline": "rotating",
        "category": category,
        "subtype": machine,
        "inputs": {
            "machine_type": machine,
            "vibration_mm_per_s": vibration,
            "nozzle_load_ratio": nozzle_load_ratio,
            "bearing_temperature_C": bearing_temp,
            "speed_rpm": random.choice([1500, 1800, 3000])
        },
        "expected_outputs": {
            "vibration_status": "ALARM" if vibration > vibration_limit else "OK",
            "nozzle_load_status": "EXCEEDED" if nozzle_load_ratio > 1.0 else "OK",
            "bearing_health_index": round(max(0.0, min(10.0, 10 - (bearing_temp - 60) * 0.15)), 3),
            "status": "CRITICAL" if red_flags else "NORMAL"
        },
        "validation_points": [
            "API 610/617 acceptance context",
            "API 670 monitoring context",
            "piping coupling check requirement"
        ],
        "standards_referenced": [
            "API 610",
            "API 617",
            "API 670"
        ],
        "criticality_level": "safety" if red_flags else "normal",
        "cross_discipline_checks": [
            "piping_nozzle_load_transfer_check"
        ],
        "expected_red_flags": red_flags
    }


def build_cases(total: int, generator, prefix: str) -> List[Dict[str, Any]]:
    counts = split_counts(total)
    cases: List[Dict[str, Any]] = []
    idx = 1
    for category in ["standard", "boundary", "failure_mode"]:
        for _ in range(counts[category]):
            case = generator(f"{prefix}-{idx:03d}", category)
            cases.append(case)
            idx += 1
    return cases


def write_dataset(filename: str, discipline: str, total: int, generator, prefix: str) -> None:
    cases = build_cases(total, generator, prefix)
    data = {
        "dataset_id": f"{discipline.upper()}_CASES_SPEC_V1",
        "discipline": discipline,
        "total_cases": len(cases),
        "ratio_policy": {"standard": 0.60, "boundary": 0.25, "failure_mode": 0.15},
        "cases": cases
    }
    path = GOLDEN_DIR / filename
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"WRITTEN={path}")


def main() -> int:
    random.seed(42)
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)

    write_dataset("piping_cases_spec.json", "piping", 50, gen_piping_case, "PIP-GOLD")
    write_dataset("vessel_cases_spec.json", "vessel", 30, gen_vessel_case, "VES-GOLD")
    write_dataset("rotating_cases_spec.json", "rotating", 30, gen_rotating_case, "ROT-GOLD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
