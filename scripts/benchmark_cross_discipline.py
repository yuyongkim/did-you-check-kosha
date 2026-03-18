from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys
from collections import Counter
from typing import Any, Dict, Iterable, List, Mapping

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


OUT_JSON = ROOT / "outputs" / "cross_discipline_report.json"
OUT_MD = ROOT / "outputs" / "cross_discipline_report.md"
PROFILE_PATH = ROOT / "config" / "cross_discipline_threshold_profiles.json"


def load_cases(path: pathlib.Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["cases"]


def load_profiles() -> Dict[str, Any]:
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def split_by_category(cases: Iterable[Mapping[str, Any]]) -> Dict[str, List[Mapping[str, Any]]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = {"standard": [], "boundary": [], "failure_mode": []}
    for case in cases:
        category = str(case.get("category", "standard"))
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(case)
    return grouped


def build_payload(
    *,
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


def evaluate_scenario_set(
    *,
    name: str,
    case_indices: List[tuple[int, int, int, int, int, int, int]],
    all_cases: Dict[str, List[Dict[str, Any]]],
    validator: CrossDisciplineValidator,
    engines: Dict[str, Any],
) -> Dict[str, Any]:
    blocked = 0
    scenario_rows: List[Dict[str, Any]] = []
    flags = Counter()

    for scenario_id, (pi, vi, ri, ei, ii, si, ci) in enumerate(case_indices, start=1):
        p_res = engines["piping"].evaluate(all_cases["piping"][pi]["inputs"])
        v_res = engines["vessel"].evaluate(all_cases["vessel"][vi]["inputs"])
        r_res = engines["rotating"].evaluate(all_cases["rotating"][ri]["inputs"])
        e_res = engines["electrical"].evaluate(all_cases["electrical"][ei]["inputs"])
        i_res = engines["instrumentation"].evaluate(all_cases["instrumentation"][ii]["inputs"])
        s_res = engines["steel"].evaluate(all_cases["steel"][si]["inputs"])
        c_res = engines["civil"].evaluate(all_cases["civil"][ci]["inputs"])

        payload = build_payload(p_res=p_res, v_res=v_res, r_res=r_res, e_res=e_res, i_res=i_res, s_res=s_res, c_res=c_res)
        cross = validator.evaluate(payload)
        is_blocked = cross["status"] == "blocked"
        if is_blocked:
            blocked += 1
        for code in cross["flags"]["red_flags"]:
            flags[code] += 1

        scenario_rows.append(
            {
                "scenario_id": scenario_id,
                "status": cross["status"],
                "red_flags": cross["flags"]["red_flags"],
                "warnings": cross["flags"]["warnings"],
            }
        )

    total = len(case_indices)
    return {
        "set_name": name,
        "total_scenarios": total,
        "blocked_scenarios": blocked,
        "pass_scenarios": total - blocked,
        "blocking_ratio": (blocked / total) if total else 0.0,
        "top_red_flags": flags.most_common(5),
        "scenarios": scenario_rows,
    }


def build_indices_aligned(grouped: Dict[str, Dict[str, List[Mapping[str, Any]]]], category: str, limit: int) -> List[tuple[int, int, int, int, int, int, int]]:
    n = min(
        limit,
        len(grouped["piping"].get(category, [])),
        len(grouped["vessel"].get(category, [])),
        len(grouped["rotating"].get(category, [])),
        len(grouped["electrical"].get(category, [])),
        len(grouped["instrumentation"].get(category, [])),
        len(grouped["steel"].get(category, [])),
        len(grouped["civil"].get(category, [])),
    )
    if n <= 0:
        return []

    def idx_of(discipline: str, case: Mapping[str, Any]) -> int:
        for i, c in enumerate(grouped[f"{discipline}_all"]):  # type: ignore[index]
            if c is case:
                return i
        return -1

    indices: List[tuple[int, int, int, int, int, int, int]] = []
    for i in range(n):
        p_case = grouped["piping"][category][i]
        v_case = grouped["vessel"][category][i]
        r_case = grouped["rotating"][category][i]
        e_case = grouped["electrical"][category][i]
        i_case = grouped["instrumentation"][category][i]
        s_case = grouped["steel"][category][i]
        c_case = grouped["civil"][category][i]
        indices.append(
            (
                idx_of("piping", p_case),
                idx_of("vessel", v_case),
                idx_of("rotating", r_case),
                idx_of("electrical", e_case),
                idx_of("instrumentation", i_case),
                idx_of("steel", s_case),
                idx_of("civil", c_case),
            )
        )
    return [x for x in indices if -1 not in x]


def build_indices_mixed_first(all_cases: Dict[str, List[Dict[str, Any]]], limit: int) -> List[tuple[int, int, int, int, int, int, int]]:
    n = min(limit, *(len(v) for v in all_cases.values()))
    return [(i, i, i, i, i, i, i) for i in range(n)]


def build_indices_mixed_random(all_cases: Dict[str, List[Dict[str, Any]]], limit: int, seed: int = 112) -> List[tuple[int, int, int, int, int, int, int]]:
    rnd = random.Random(seed)
    n = min(limit, *(len(v) for v in all_cases.values()))
    return [
        (
            rnd.randrange(len(all_cases["piping"])),
            rnd.randrange(len(all_cases["vessel"])),
            rnd.randrange(len(all_cases["rotating"])),
            rnd.randrange(len(all_cases["electrical"])),
            rnd.randrange(len(all_cases["instrumentation"])),
            rnd.randrange(len(all_cases["steel"])),
            rnd.randrange(len(all_cases["civil"])),
        )
        for _ in range(n)
    ]


def run_profile(profile_name: str, threshold_map: Mapping[str, Any], all_cases: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    grouped = {
        "piping": split_by_category(all_cases["piping"]),
        "vessel": split_by_category(all_cases["vessel"]),
        "rotating": split_by_category(all_cases["rotating"]),
        "electrical": split_by_category(all_cases["electrical"]),
        "instrumentation": split_by_category(all_cases["instrumentation"]),
        "steel": split_by_category(all_cases["steel"]),
        "civil": split_by_category(all_cases["civil"]),
        "piping_all": all_cases["piping"],
        "vessel_all": all_cases["vessel"],
        "rotating_all": all_cases["rotating"],
        "electrical_all": all_cases["electrical"],
        "instrumentation_all": all_cases["instrumentation"],
        "steel_all": all_cases["steel"],
        "civil_all": all_cases["civil"],
    }

    thresholds = CrossDisciplineThresholds.from_mapping(threshold_map)
    validator = CrossDisciplineValidator(thresholds=thresholds)
    engines = {
        "piping": PipingVerificationService(),
        "vessel": VesselVerificationService(),
        "rotating": RotatingVerificationService(),
        "electrical": ElectricalVerificationService(),
        "instrumentation": InstrumentationVerificationService(),
        "steel": SteelVerificationService(),
        "civil": CivilVerificationService(),
    }

    scenario_sets = [
        ("aligned_standard", build_indices_aligned(grouped, "standard", 10)),
        ("aligned_boundary", build_indices_aligned(grouped, "boundary", 8)),
        ("aligned_failure", build_indices_aligned(grouped, "failure_mode", 5)),
        ("mixed_first20", build_indices_mixed_first(all_cases, 20)),
        ("mixed_random20", build_indices_mixed_random(all_cases, 20)),
    ]

    set_reports = []
    total_scenarios = 0
    total_blocked = 0

    for set_name, indices in scenario_sets:
        report = evaluate_scenario_set(
            name=set_name,
            case_indices=indices,
            all_cases=all_cases,
            validator=validator,
            engines=engines,
        )
        set_reports.append(report)
        total_scenarios += report["total_scenarios"]
        total_blocked += report["blocked_scenarios"]

    return {
        "profile": profile_name,
        "thresholds": dict(threshold_map),
        "total_scenarios": total_scenarios,
        "blocked_scenarios": total_blocked,
        "pass_scenarios": total_scenarios - total_blocked,
        "blocking_ratio": (total_blocked / total_scenarios) if total_scenarios else 0.0,
        "scenario_sets": set_reports,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cross-discipline benchmark with threshold profiles")
    parser.add_argument(
        "--profile",
        default="active",
        choices=["active", "all", "conservative", "balanced", "permissive"],
        help="Profile to run. 'active' uses profile file's active_profile.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    profile_data = load_profiles()
    profiles: Dict[str, Dict[str, Any]] = profile_data.get("profiles", {})
    active_profile = str(profile_data.get("active_profile", "balanced"))

    all_cases = {
        "piping": load_cases(ROOT / "datasets" / "golden_standards" / "piping_golden_dataset_v1.json"),
        "vessel": load_cases(ROOT / "datasets" / "golden_standards" / "vessel_golden_dataset_v1.json"),
        "rotating": load_cases(ROOT / "datasets" / "golden_standards" / "rotating_golden_dataset_v1.json"),
        "electrical": load_cases(ROOT / "datasets" / "golden_standards" / "electrical_golden_dataset_v1.json"),
        "instrumentation": load_cases(ROOT / "datasets" / "golden_standards" / "instrumentation_golden_dataset_v1.json"),
        "steel": load_cases(ROOT / "datasets" / "golden_standards" / "steel_golden_dataset_v1.json"),
        "civil": load_cases(ROOT / "datasets" / "golden_standards" / "civil_golden_dataset_v1.json"),
    }

    if args.profile == "all":
        selected_profiles = [p for p in ["conservative", "balanced", "permissive"] if p in profiles]
    elif args.profile == "active":
        selected_profiles = [active_profile] if active_profile in profiles else ["balanced"]
    else:
        selected_profiles = [args.profile]

    reports = []
    for name in selected_profiles:
        threshold_map = profiles.get(name)
        if threshold_map is None:
            continue
        reports.append(run_profile(name, threshold_map, all_cases))

    if not reports:
        print("NO_PROFILES_TO_RUN")
        return 1

    selected = reports[0] if len(reports) == 1 else {
        "profiles": reports,
        "best_profile_by_lowest_blocking": min(reports, key=lambda r: r["blocking_ratio"])["profile"],
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(selected, indent=2), encoding="utf-8")

    lines = ["# Cross-Discipline Runtime Report (7 Disciplines)"]
    if "profiles" in selected:
        lines.append("")
        lines.append(f"- Profiles evaluated: {len(selected['profiles'])}")
        lines.append(f"- Best profile (lowest blocking): {selected['best_profile_by_lowest_blocking']}")
        for p in selected["profiles"]:
            lines.append(f"- {p['profile']}: blocking_ratio={p['blocking_ratio']:.4f}, scenarios={p['total_scenarios']}")
    else:
        lines.append("")
        lines.append(f"- Profile: {selected['profile']}")
        lines.append(f"- Total Scenarios: {selected['total_scenarios']}")
        lines.append(f"- Blocked Scenarios: {selected['blocked_scenarios']}")
        lines.append(f"- Passed Scenarios: {selected['pass_scenarios']}")
        lines.append(f"- Blocking Ratio: {selected['blocking_ratio']:.4f}")
        lines.append("")
        lines.append("## Scenario Sets")
        for s in selected["scenario_sets"]:
            lines.append(
                f"- {s['set_name']}: blocking_ratio={s['blocking_ratio']:.4f}, "
                f"blocked={s['blocked_scenarios']}/{s['total_scenarios']}"
            )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"REPORT_JSON={OUT_JSON}")
    print(f"REPORT_MD={OUT_MD}")
    if "profiles" in selected:
        print(f"BEST_PROFILE={selected['best_profile_by_lowest_blocking']}")
    else:
        print(f"PROFILE={selected['profile']}")
        print(f"BLOCKING_RATIO={selected['blocking_ratio']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
