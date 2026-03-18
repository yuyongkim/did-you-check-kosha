#!/usr/bin/env python3
"""Compare cross-discipline benchmark results with validator OFF vs ON."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.benchmark_cross_discipline import (
    PROFILE_PATH,
    build_indices_aligned,
    build_indices_mixed_first,
    build_indices_mixed_random,
    evaluate_scenario_set,
    load_cases,
    load_profiles,
    split_by_category,
)
from src.civil.service import CivilVerificationService
from src.cross_discipline import CrossDisciplineThresholds, CrossDisciplineValidator
from src.electrical.service import ElectricalVerificationService
from src.instrumentation.service import InstrumentationVerificationService
from src.piping.service import PipingVerificationService
from src.rotating.service import RotatingVerificationService
from src.steel.service import SteelVerificationService
from src.vessel.service import VesselVerificationService


OUT_JSON = ROOT / "outputs" / "cross_discipline_ablation_report.json"
OUT_MD = ROOT / "outputs" / "cross_discipline_ablation_report.md"


class NullCrossDisciplineValidator:
    def evaluate(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        return {
            "status": "ok",
            "issues": [],
            "flags": {"red_flags": [], "warnings": []},
            "recommendations": [],
            "summary": {"checks_run": 0, "issues_found": 0, "blocking": False},
        }


def load_all_cases() -> Dict[str, list[dict[str, Any]]]:
    return {
        "piping": load_cases(ROOT / "datasets" / "golden_standards" / "piping_golden_dataset_v1.json"),
        "vessel": load_cases(ROOT / "datasets" / "golden_standards" / "vessel_golden_dataset_v1.json"),
        "rotating": load_cases(ROOT / "datasets" / "golden_standards" / "rotating_golden_dataset_v1.json"),
        "electrical": load_cases(ROOT / "datasets" / "golden_standards" / "electrical_golden_dataset_v1.json"),
        "instrumentation": load_cases(ROOT / "datasets" / "golden_standards" / "instrumentation_golden_dataset_v1.json"),
        "steel": load_cases(ROOT / "datasets" / "golden_standards" / "steel_golden_dataset_v1.json"),
        "civil": load_cases(ROOT / "datasets" / "golden_standards" / "civil_golden_dataset_v1.json"),
    }


def build_grouped(all_cases: Dict[str, list[dict[str, Any]]]) -> Dict[str, Any]:
    return {
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


def build_engines() -> Dict[str, Any]:
    return {
        "piping": PipingVerificationService(),
        "vessel": VesselVerificationService(),
        "rotating": RotatingVerificationService(),
        "electrical": ElectricalVerificationService(),
        "instrumentation": InstrumentationVerificationService(),
        "steel": SteelVerificationService(),
        "civil": CivilVerificationService(),
    }


def run() -> Dict[str, Any]:
    profile_data = load_profiles()
    profiles: Dict[str, Dict[str, Any]] = profile_data.get("profiles", {})
    active_profile = str(profile_data.get("active_profile", "balanced"))
    threshold_map = profiles.get(active_profile) or profiles.get("balanced") or {}

    all_cases = load_all_cases()
    grouped = build_grouped(all_cases)
    scenario_sets = [
        ("aligned_standard", build_indices_aligned(grouped, "standard", 10)),
        ("aligned_boundary", build_indices_aligned(grouped, "boundary", 8)),
        ("aligned_failure", build_indices_aligned(grouped, "failure_mode", 5)),
        ("mixed_first20", build_indices_mixed_first(all_cases, 20)),
        ("mixed_random20", build_indices_mixed_random(all_cases, 20)),
    ]

    engines = build_engines()
    validator_on = CrossDisciplineValidator(CrossDisciplineThresholds.from_mapping(threshold_map))
    validator_off = NullCrossDisciplineValidator()

    set_reports = []
    for set_name, indices in scenario_sets:
        off_report = evaluate_scenario_set(
            name=set_name,
            case_indices=indices,
            all_cases=all_cases,
            validator=validator_off,
            engines=engines,
        )
        on_report = evaluate_scenario_set(
            name=set_name,
            case_indices=indices,
            all_cases=all_cases,
            validator=validator_on,
            engines=engines,
        )
        delta_blocked = on_report["blocked_scenarios"] - off_report["blocked_scenarios"]
        set_reports.append(
            {
                "set_name": set_name,
                "total_scenarios": on_report["total_scenarios"],
                "validator_off": off_report,
                "validator_on": on_report,
                "absolute_blocked_delta": delta_blocked,
                "blocking_ratio_delta": on_report["blocking_ratio"] - off_report["blocking_ratio"],
            }
        )

    total = sum(item["total_scenarios"] for item in set_reports)
    blocked_off = sum(item["validator_off"]["blocked_scenarios"] for item in set_reports)
    blocked_on = sum(item["validator_on"]["blocked_scenarios"] for item in set_reports)
    return {
        "profile": active_profile,
        "profile_path": str(PROFILE_PATH),
        "total_scenarios": total,
        "validator_off": {
            "blocked_scenarios": blocked_off,
            "blocking_ratio": (blocked_off / total) if total else 0.0,
        },
        "validator_on": {
            "blocked_scenarios": blocked_on,
            "blocking_ratio": (blocked_on / total) if total else 0.0,
        },
        "absolute_blocked_delta": blocked_on - blocked_off,
        "blocking_ratio_delta": ((blocked_on - blocked_off) / total) if total else 0.0,
        "scenario_sets": set_reports,
    }


def write_reports(report: Dict[str, Any]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# Cross-Discipline Ablation Report",
        "",
        f"- Total Scenarios: {report['total_scenarios']}",
        f"- Validator OFF blocked: {report['validator_off']['blocked_scenarios']} ({report['validator_off']['blocking_ratio']:.4f})",
        f"- Validator ON blocked: {report['validator_on']['blocked_scenarios']} ({report['validator_on']['blocking_ratio']:.4f})",
        f"- Absolute blocked delta: {report['absolute_blocked_delta']}",
        f"- Blocking ratio delta: {report['blocking_ratio_delta']:.4f}",
        "",
        "## Scenario Sets",
    ]
    for item in report["scenario_sets"]:
        lines.append(
            f"- {item['set_name']}: OFF={item['validator_off']['blocked_scenarios']}/{item['total_scenarios']} "
            f"({item['validator_off']['blocking_ratio']:.4f}), "
            f"ON={item['validator_on']['blocked_scenarios']}/{item['total_scenarios']} "
            f"({item['validator_on']['blocking_ratio']:.4f}), "
            f"delta={item['absolute_blocked_delta']} ({item['blocking_ratio_delta']:.4f})"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    report = run()
    write_reports(report)
    print(f"REPORT_JSON={OUT_JSON}")
    print(f"REPORT_MD={OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
