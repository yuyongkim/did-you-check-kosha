from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys
from typing import Any, Dict, List, Mapping, Tuple

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.cross_discipline import CrossDisciplineThresholds, CrossDisciplineValidator
from src.civil.service import CivilVerificationService
from src.electrical.service import ElectricalVerificationService
from src.instrumentation.service import InstrumentationVerificationService
from src.piping.service import PipingVerificationService
from src.rotating.service import RotatingVerificationService
from src.steel.service import SteelVerificationService
from src.vessel.service import VesselVerificationService


PROFILE_PATH = ROOT / "config" / "cross_discipline_threshold_profiles.json"
OUT_JSON = ROOT / "outputs" / "cross_discipline_tuning_report.json"
OUT_MD = ROOT / "outputs" / "cross_discipline_tuning_report.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tune cross-discipline thresholds")
    parser.add_argument("--rounds", type=int, default=50, help="Number of random search rounds")
    parser.add_argument("--seed", type=int, default=20260227, help="Random seed")
    parser.add_argument(
        "--activate-best",
        dest="activate_best",
        action="store_true",
        default=True,
        help="Set best profile as active_profile in config file",
    )
    parser.add_argument(
        "--no-activate-best",
        dest="activate_best",
        action="store_false",
        help="Do not update active_profile",
    )
    return parser.parse_args()


def load_cases(path: pathlib.Path) -> List[Dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))["cases"]


def split_by_category(cases: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {"standard": [], "boundary": [], "failure_mode": []}
    for case in cases:
        category = str(case.get("category", "standard"))
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(case)
    return grouped


def precompute_results() -> Dict[str, List[Mapping[str, Any]]]:
    cases = {
        "piping": load_cases(ROOT / "datasets" / "golden_standards" / "piping_golden_dataset_v1.json"),
        "vessel": load_cases(ROOT / "datasets" / "golden_standards" / "vessel_golden_dataset_v1.json"),
        "rotating": load_cases(ROOT / "datasets" / "golden_standards" / "rotating_golden_dataset_v1.json"),
        "electrical": load_cases(ROOT / "datasets" / "golden_standards" / "electrical_golden_dataset_v1.json"),
        "instrumentation": load_cases(ROOT / "datasets" / "golden_standards" / "instrumentation_golden_dataset_v1.json"),
        "steel": load_cases(ROOT / "datasets" / "golden_standards" / "steel_golden_dataset_v1.json"),
        "civil": load_cases(ROOT / "datasets" / "golden_standards" / "civil_golden_dataset_v1.json"),
    }

    engines = {
        "piping": PipingVerificationService(),
        "vessel": VesselVerificationService(),
        "rotating": RotatingVerificationService(),
        "electrical": ElectricalVerificationService(),
        "instrumentation": InstrumentationVerificationService(),
        "steel": SteelVerificationService(),
        "civil": CivilVerificationService(),
    }

    outputs: Dict[str, List[Mapping[str, Any]]] = {}
    for name, items in cases.items():
        outputs[name] = [engines[name].evaluate(item["inputs"]) for item in items]
    return outputs


def build_payload(
    p_res: Mapping[str, Any],
    v_res: Mapping[str, Any],
    r_res: Mapping[str, Any],
    e_res: Mapping[str, Any],
    i_res: Mapping[str, Any],
    s_res: Mapping[str, Any],
    c_res: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "piping": {
            "current_thickness_mm": p_res.get("input_data", {}).get("thickness_history", [{}])[-1].get("thickness_mm")
            if isinstance(p_res.get("input_data", {}).get("thickness_history"), list) and p_res.get("input_data", {}).get("thickness_history")
            else None,
            "t_min_mm": p_res.get("final_results", {}).get("t_min_mm"),
            "remaining_life_years": p_res.get("final_results", {}).get("remaining_life_years"),
            "nps_inch": p_res.get("input_data", {}).get("nps"),
        },
        "vessel": {
            "current_thickness_mm": v_res.get("input_data", {}).get("current_thickness_mm") or v_res.get("input_data", {}).get("t_current_mm"),
            "t_required_shell_mm": v_res.get("final_results", {}).get("t_required_shell_mm"),
            "remaining_life_years": v_res.get("final_results", {}).get("remaining_life_years"),
        },
        "rotating": {
            "vibration_mm_per_s": r_res.get("final_results", {}).get("vibration_mm_per_s"),
            "vibration_limit_mm_per_s": r_res.get("final_results", {}).get("vibration_limit_mm_per_s"),
            "nozzle_load_ratio": r_res.get("final_results", {}).get("nozzle_load_ratio"),
            "bearing_health_index": r_res.get("final_results", {}).get("bearing_health_index"),
            "bearing_temperature_c": r_res.get("final_results", {}).get("bearing_temperature_c"),
        },
        "electrical": {
            "motor_current_thd_percent": e_res.get("final_results", {}).get("motor_current_thd_percent"),
            "thd_voltage_percent": e_res.get("final_results", {}).get("thd_voltage_percent"),
            "power_factor": e_res.get("final_results", {}).get("power_factor"),
        },
        "instrumentation": {
            "predicted_drift_pct": i_res.get("final_results", {}).get("predicted_drift_pct"),
            "drift_r_squared": i_res.get("final_results", {}).get("drift_r_squared"),
            "pfdavg": i_res.get("final_results", {}).get("pfdavg"),
            "sil_target": i_res.get("final_results", {}).get("sil_target"),
        },
        "steel": {
            "dc_ratio": s_res.get("final_results", {}).get("dc_ratio"),
            "deflection_ratio": s_res.get("final_results", {}).get("deflection_ratio"),
            "corrosion_loss_percent": s_res.get("final_results", {}).get("corrosion_loss_percent"),
        },
        "civil": {
            "foundation_settlement_mm": c_res.get("final_results", {}).get("foundation_settlement_mm"),
            "crack_width_mm": c_res.get("final_results", {}).get("crack_width_mm"),
            "spalling_area_percent": c_res.get("final_results", {}).get("spalling_area_percent"),
        },
    }


def scenario_indices(seed: int = 112) -> Dict[str, List[Tuple[int, int, int, int, int, int, int]]]:
    p = load_cases(ROOT / "datasets" / "golden_standards" / "piping_golden_dataset_v1.json")
    v = load_cases(ROOT / "datasets" / "golden_standards" / "vessel_golden_dataset_v1.json")
    r = load_cases(ROOT / "datasets" / "golden_standards" / "rotating_golden_dataset_v1.json")
    e = load_cases(ROOT / "datasets" / "golden_standards" / "electrical_golden_dataset_v1.json")
    i = load_cases(ROOT / "datasets" / "golden_standards" / "instrumentation_golden_dataset_v1.json")
    s = load_cases(ROOT / "datasets" / "golden_standards" / "steel_golden_dataset_v1.json")
    c = load_cases(ROOT / "datasets" / "golden_standards" / "civil_golden_dataset_v1.json")

    gp, gv, gr, ge, gi, gs, gc = (
        split_by_category(p),
        split_by_category(v),
        split_by_category(r),
        split_by_category(e),
        split_by_category(i),
        split_by_category(s),
        split_by_category(c),
    )

    def idx(cases: List[Dict[str, Any]], case: Dict[str, Any]) -> int:
        return cases.index(case)

    standard_n = min(10, len(gp["standard"]), len(gv["standard"]), len(gr["standard"]), len(ge["standard"]), len(gi["standard"]), len(gs["standard"]), len(gc["standard"]))
    boundary_n = min(8, len(gp["boundary"]), len(gv["boundary"]), len(gr["boundary"]), len(ge["boundary"]), len(gi["boundary"]), len(gs["boundary"]), len(gc["boundary"]))
    failure_n = min(5, len(gp["failure_mode"]), len(gv["failure_mode"]), len(gr["failure_mode"]), len(ge["failure_mode"]), len(gi["failure_mode"]), len(gs["failure_mode"]), len(gc["failure_mode"]))

    standard = [
        (
            idx(p, gp["standard"][k]),
            idx(v, gv["standard"][k]),
            idx(r, gr["standard"][k]),
            idx(e, ge["standard"][k]),
            idx(i, gi["standard"][k]),
            idx(s, gs["standard"][k]),
            idx(c, gc["standard"][k]),
        )
        for k in range(standard_n)
    ]
    boundary = [
        (
            idx(p, gp["boundary"][k]),
            idx(v, gv["boundary"][k]),
            idx(r, gr["boundary"][k]),
            idx(e, ge["boundary"][k]),
            idx(i, gi["boundary"][k]),
            idx(s, gs["boundary"][k]),
            idx(c, gc["boundary"][k]),
        )
        for k in range(boundary_n)
    ]
    failure = [
        (
            idx(p, gp["failure_mode"][k]),
            idx(v, gv["failure_mode"][k]),
            idx(r, gr["failure_mode"][k]),
            idx(e, ge["failure_mode"][k]),
            idx(i, gi["failure_mode"][k]),
            idx(s, gs["failure_mode"][k]),
            idx(c, gc["failure_mode"][k]),
        )
        for k in range(failure_n)
    ]

    rnd = random.Random(seed)
    mixed_n = min(20, len(p), len(v), len(r), len(e), len(i), len(s), len(c))
    mixed = [
        (
            rnd.randrange(len(p)),
            rnd.randrange(len(v)),
            rnd.randrange(len(r)),
            rnd.randrange(len(e)),
            rnd.randrange(len(i)),
            rnd.randrange(len(s)),
            rnd.randrange(len(c)),
        )
        for _ in range(mixed_n)
    ]

    return {"standard": standard, "boundary": boundary, "failure": failure, "mixed": mixed}


def evaluate_thresholds(
    thresholds: Mapping[str, Any],
    precomputed: Dict[str, List[Mapping[str, Any]]],
    indices: Dict[str, List[Tuple[int, int, int, int, int, int, int]]],
) -> Dict[str, Any]:
    validator = CrossDisciplineValidator(thresholds=CrossDisciplineThresholds.from_mapping(thresholds))

    def block_ratio(rows: List[Tuple[int, int, int, int, int, int, int]]) -> float:
        if not rows:
            return 0.0
        blocked = 0
        for pi, vi, ri, ei, ii, si, ci in rows:
            payload = build_payload(
                precomputed["piping"][pi],
                precomputed["vessel"][vi],
                precomputed["rotating"][ri],
                precomputed["electrical"][ei],
                precomputed["instrumentation"][ii],
                precomputed["steel"][si],
                precomputed["civil"][ci],
            )
            result = validator.evaluate(payload)
            if result["status"] == "blocked":
                blocked += 1
        return blocked / len(rows)

    br_std = block_ratio(indices["standard"])
    br_bnd = block_ratio(indices["boundary"])
    br_fail = block_ratio(indices["failure"])
    br_mix = block_ratio(indices["mixed"])

    standard_completion = 1.0 - br_std
    boundary_completion = 1.0 - br_bnd
    mixed_completion = 1.0 - br_mix
    failure_blocking = br_fail

    sensitivity = sensitivity_metrics(validator)
    hard_block_recall = sensitivity["hard_block_recall"]
    sensitivity_accuracy = sensitivity["weighted_accuracy"]

    # Safety-weighted objective with sensitivity discrimination.
    score = (
        0.30 * standard_completion
        + 0.10 * boundary_completion
        + 0.10 * mixed_completion
        + 0.20 * failure_blocking
        + 0.30 * sensitivity_accuracy
    )

    if hard_block_recall < 1.0:
        score -= (1.0 - hard_block_recall) * 0.50

    return {
        "score": score,
        "blocking": {
            "standard": br_std,
            "boundary": br_bnd,
            "failure": br_fail,
            "mixed": br_mix,
        },
        "completion": {
            "standard": standard_completion,
            "boundary": boundary_completion,
            "mixed": mixed_completion,
        },
        "sensitivity": sensitivity,
    }


def sensitivity_scenarios() -> List[Dict[str, Any]]:
    return [
        {
            "name": "safe_all_low",
            "payload": {
                "piping": {"current_thickness_mm": 7.5, "t_min_mm": 5.5, "remaining_life_years": 8.0},
                "vessel": {"current_thickness_mm": 12.0, "t_required_shell_mm": 9.5, "remaining_life_years": 10.0},
                "rotating": {
                    "vibration_mm_per_s": 2.2,
                    "vibration_limit_mm_per_s": 3.0,
                    "nozzle_load_ratio": 0.85,
                    "bearing_health_index": 7.0,
                    "bearing_temperature_c": 72.0,
                },
                "electrical": {"motor_current_thd_percent": 4.2, "thd_voltage_percent": 5.0, "power_factor": 0.90},
                "instrumentation": {"predicted_drift_pct": 0.5, "drift_r_squared": 0.75, "pfdavg": 5.0e-4, "sil_target": 2},
            },
            "expect_block": False,
            "weight": 1.0,
            "hard": False,
        },
        {
            "name": "clear_electrical_rotating_risk",
            "payload": {
                "electrical": {"motor_current_thd_percent": 7.5, "thd_voltage_percent": 7.0, "power_factor": 0.83},
                "rotating": {
                    "vibration_mm_per_s": 3.5,
                    "vibration_limit_mm_per_s": 3.0,
                    "nozzle_load_ratio": 0.95,
                    "bearing_health_index": 5.2,
                    "bearing_temperature_c": 88.0,
                },
            },
            "expect_block": True,
            "weight": 1.0,
            "hard": True,
        },
        {
            "name": "clear_instrument_piping_risk",
            "payload": {
                "instrumentation": {"predicted_drift_pct": 1.8, "drift_r_squared": 0.40, "pfdavg": 8.0e-4, "sil_target": 2},
                "piping": {"current_thickness_mm": 5.9, "t_min_mm": 5.0, "remaining_life_years": 2.2},
            },
            "expect_block": True,
            "weight": 1.0,
            "hard": True,
        },
        {
            "name": "clear_noise_to_sis_risk",
            "payload": {
                "electrical": {"motor_current_thd_percent": 5.2, "thd_voltage_percent": 9.5, "power_factor": 0.86},
                "instrumentation": {"predicted_drift_pct": 0.6, "drift_r_squared": 0.72, "pfdavg": 2.0e-3, "sil_target": 2},
            },
            "expect_block": True,
            "weight": 1.0,
            "hard": True,
        },
        {
            "name": "near_threshold_electrical_rotating",
            "payload": {
                "electrical": {"motor_current_thd_percent": 5.2, "thd_voltage_percent": 6.5, "power_factor": 0.86},
                "rotating": {
                    "vibration_mm_per_s": 3.05,
                    "vibration_limit_mm_per_s": 3.0,
                    "nozzle_load_ratio": 0.98,
                    "bearing_health_index": 5.8,
                    "bearing_temperature_c": 81.0,
                },
            },
            "expect_block": True,
            "weight": 0.8,
            "hard": False,
        },
        {
            "name": "near_threshold_instrument_piping",
            "payload": {
                "instrumentation": {"predicted_drift_pct": 1.05, "drift_r_squared": 0.34, "pfdavg": 9.0e-4, "sil_target": 2},
                "piping": {"current_thickness_mm": 6.2, "t_min_mm": 5.3, "remaining_life_years": 2.8},
            },
            "expect_block": True,
            "weight": 0.8,
            "hard": False,
        },
        {
            "name": "safe_but_low_pf_only_warning",
            "payload": {
                "electrical": {"motor_current_thd_percent": 4.6, "thd_voltage_percent": 5.5, "power_factor": 0.82},
                "rotating": {
                    "vibration_mm_per_s": 2.7,
                    "vibration_limit_mm_per_s": 3.0,
                    "nozzle_load_ratio": 0.88,
                    "bearing_health_index": 6.6,
                    "bearing_temperature_c": 76.0,
                },
            },
            "expect_block": False,
            "weight": 0.8,
            "hard": False,
        },
        {
            "name": "safe_piping_vessel_interface",
            "payload": {
                "piping": {"current_thickness_mm": 7.2, "t_min_mm": 5.8, "remaining_life_years": 7.5},
                "vessel": {"current_thickness_mm": 11.0, "t_required_shell_mm": 9.7, "remaining_life_years": 8.0},
            },
            "expect_block": False,
            "weight": 1.0,
            "hard": False,
        },
        {
            "name": "clear_structure_piping_risk",
            "payload": {
                "steel": {"dc_ratio": 0.97, "deflection_ratio": 1.05, "corrosion_loss_percent": 34.0},
                "piping": {"current_thickness_mm": 5.6, "t_min_mm": 5.0, "remaining_life_years": 2.4, "nps_inch": 10.0},
            },
            "expect_block": True,
            "weight": 1.0,
            "hard": True,
        },
        {
            "name": "clear_civil_rotating_risk",
            "payload": {
                "civil": {"foundation_settlement_mm": 30.0, "crack_width_mm": 0.5, "spalling_area_percent": 18.0},
                "rotating": {
                    "vibration_mm_per_s": 4.0,
                    "vibration_limit_mm_per_s": 3.0,
                    "nozzle_load_ratio": 0.92,
                    "bearing_health_index": 5.5,
                    "bearing_temperature_c": 81.0,
                },
            },
            "expect_block": True,
            "weight": 1.0,
            "hard": True,
        },
    ]


def sensitivity_metrics(validator: CrossDisciplineValidator) -> Dict[str, float]:
    cases = sensitivity_scenarios()
    weighted_total = 0.0
    weighted_correct = 0.0
    hard_total = 0
    hard_correct = 0

    for case in cases:
        payload = case["payload"]
        expect_block = bool(case["expect_block"])
        weight = float(case["weight"])
        hard = bool(case["hard"])

        result = validator.evaluate(payload)
        actual_block = result["status"] == "blocked"
        is_correct = actual_block == expect_block

        weighted_total += weight
        if is_correct:
            weighted_correct += weight

        if hard and expect_block:
            hard_total += 1
            if actual_block:
                hard_correct += 1

    weighted_accuracy = (weighted_correct / weighted_total) if weighted_total else 0.0
    hard_block_recall = (hard_correct / hard_total) if hard_total else 1.0
    return {
        "weighted_accuracy": weighted_accuracy,
        "hard_block_recall": hard_block_recall,
    }


def perturb(base: Mapping[str, Any], rnd: random.Random) -> Dict[str, Any]:
    out = dict(base)
    out.setdefault("steel_dc_high", 0.9)
    out.setdefault("steel_corrosion_high_percent", 30.0)
    out.setdefault("steel_deflection_ratio_high", 1.0)
    out.setdefault("piping_large_bore_nps_in", 8.0)
    out.setdefault("civil_settlement_high_mm", 25.0)
    out.setdefault("civil_crack_width_high_mm", 0.4)
    out.setdefault("civil_spalling_high_percent", 20.0)
    out.setdefault("rotating_vibration_ratio_high", 1.0)

    def scale(key: str, low: float, high: float, sigma: float = 0.15) -> None:
        v = float(out[key])
        f = 1.0 + rnd.uniform(-sigma, sigma)
        out[key] = max(low, min(high, v * f))

    scale("piping_vessel_margin_diff_mm", 0.8, 3.0, 0.30)
    scale("piping_vessel_margin_ratio", 0.5, 1.2, 0.25)
    scale("piping_margin_low_mm", 0.4, 2.0, 0.30)
    scale("piping_remaining_life_low_years", 1.5, 6.0, 0.30)
    scale("piping_nozzle_margin_low_mm", 0.6, 2.5, 0.30)
    scale("rotating_nozzle_overload_ratio", 0.9, 1.2, 0.20)
    scale("vessel_nozzle_margin_low_mm", 0.5, 2.0, 0.30)
    scale("vessel_remaining_life_low_years", 3.0, 8.0, 0.30)
    scale("rotating_bearing_hi_low", 2.5, 6.0, 0.25)
    scale("electrical_current_thd_high_pct", 3.5, 8.0, 0.25)
    scale("rotating_bearing_temp_high_c", 72.0, 95.0, 0.20)
    scale("electrical_power_factor_low", 0.75, 0.95, 0.15)
    scale("instrumentation_drift_high_pct", 0.6, 2.0, 0.25)
    scale("instrumentation_r2_low", 0.15, 0.5, 0.25)
    scale("instrumentation_pfd_high", 5e-4, 3e-3, 0.35)
    scale("instrumentation_sil_target_high", 1.0, 3.0, 0.0)
    scale("steel_dc_high", 0.75, 1.1, 0.20)
    scale("steel_corrosion_high_percent", 15.0, 50.0, 0.25)
    scale("steel_deflection_ratio_high", 0.8, 1.3, 0.20)
    scale("piping_large_bore_nps_in", 4.0, 12.0, 0.25)
    scale("civil_settlement_high_mm", 15.0, 40.0, 0.25)
    scale("civil_crack_width_high_mm", 0.25, 0.7, 0.25)
    scale("civil_spalling_high_percent", 10.0, 35.0, 0.25)
    scale("rotating_vibration_ratio_high", 0.85, 1.2, 0.20)
    out["instrumentation_sil_target_high"] = round(float(out["instrumentation_sil_target_high"]))

    return out


def main() -> int:
    args = parse_args()
    rnd = random.Random(args.seed)

    profiles_doc = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    profiles = profiles_doc.get("profiles", {})
    active_name = str(profiles_doc.get("active_profile", "balanced"))
    base = profiles.get(active_name, profiles.get("balanced"))
    if not isinstance(base, dict):
        print("BASE_PROFILE_NOT_FOUND")
        return 1

    precomputed = precompute_results()
    indices = scenario_indices(seed=112)

    results = []
    seeds = [("baseline", dict(base))]
    for k in ("conservative", "balanced", "permissive"):
        v = profiles.get(k)
        if isinstance(v, dict):
            seeds.append((k, dict(v)))

    for name, candidate in seeds:
        eval_result = evaluate_thresholds(candidate, precomputed, indices)
        results.append({"round": name, "thresholds": candidate, **eval_result})

    for r in range(1, args.rounds + 1):
        candidate = perturb(base, rnd)
        eval_result = evaluate_thresholds(candidate, precomputed, indices)
        results.append({"round": r, "thresholds": candidate, **eval_result})

    ranked = sorted(results, key=lambda x: x["score"], reverse=True)
    best = ranked[0]

    tuned_name = f"tuned_round_{args.rounds}"
    profiles_doc.setdefault("profiles", {})
    profiles_doc["profiles"][tuned_name] = best["thresholds"]
    if args.activate_best:
        profiles_doc["active_profile"] = tuned_name
    PROFILE_PATH.write_text(json.dumps(profiles_doc, indent=2), encoding="utf-8")

    report = {
        "rounds": args.rounds,
        "seed": args.seed,
        "active_profile_before": active_name,
        "active_profile_after": profiles_doc.get("active_profile"),
        "best_profile_name": tuned_name,
        "best": best,
        "top10": ranked[:10],
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# Cross-Discipline Threshold Tuning Report",
        "",
        f"- Rounds: {args.rounds}",
        f"- Seed: {args.seed}",
        f"- Active Profile (before): {active_name}",
        f"- Active Profile (after): {profiles_doc.get('active_profile')}",
        f"- Best Profile Name: {tuned_name}",
        f"- Best Score: {best['score']:.6f}",
        "",
        "## Best Metrics",
        f"- blocking.standard: {best['blocking']['standard']:.4f}",
        f"- blocking.boundary: {best['blocking']['boundary']:.4f}",
        f"- blocking.failure: {best['blocking']['failure']:.4f}",
        f"- blocking.mixed: {best['blocking']['mixed']:.4f}",
        f"- sensitivity.weighted_accuracy: {best['sensitivity']['weighted_accuracy']:.4f}",
        f"- sensitivity.hard_block_recall: {best['sensitivity']['hard_block_recall']:.4f}",
        "",
        "## Top 10",
    ]
    for idx, row in enumerate(ranked[:10], start=1):
        lines.append(
            f"- {idx}. round={row['round']} score={row['score']:.6f} "
            f"(std={row['blocking']['standard']:.3f}, fail={row['blocking']['failure']:.3f}, "
            f"mix={row['blocking']['mixed']:.3f}, sens={row['sensitivity']['weighted_accuracy']:.3f})"
        )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"REPORT_JSON={OUT_JSON}")
    print(f"REPORT_MD={OUT_MD}")
    print(f"BEST_PROFILE={tuned_name}")
    print(f"BEST_SCORE={best['score']:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
