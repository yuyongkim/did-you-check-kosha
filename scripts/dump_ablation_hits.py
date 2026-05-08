#!/usr/bin/env python3
"""Partition the cross-discipline-blocked scenarios by failure-mode family.

Goal (manuscript §6.3): split the blocked scenarios from the cross-discipline
ablation (validator ON) into the three failure-mode families the validator
was designed to surface --

  - piping/vessel nozzle-margin family (piping<->vessel, piping<->rotating,
    vessel<->rotating, instrumentation<->piping, steel<->piping)
  - electrical/rotating coupling family (electrical<->rotating,
    electrical<->instrumentation, steel<->electrical)
  - civil/rotating foundation-vibration family (civil<->rotating,
    civil<->instrumentation)

Each scenario is assigned to the family whose checks fired the most blocking
issues; ties are broken by family priority (piping/vessel > electrical >
civil) for determinism. A scenario can list secondary families in its row.

Hard rule: family counts must sum to the total number of blocked scenarios.
Output:
  outputs/ablation_failure_mode_partition.json
  outputs/ablation_failure_mode_partition.md
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.benchmark_cross_discipline import (
    PROFILE_PATH,
    build_indices_aligned,
    build_indices_mixed_first,
    build_indices_mixed_random,
    build_payload,
    load_cases,
    load_profiles,
    split_by_category,
)
from src.cross_discipline import CrossDisciplineThresholds, CrossDisciplineValidator
from src.civil.service import CivilVerificationService
from src.electrical.service import ElectricalVerificationService
from src.instrumentation.service import InstrumentationVerificationService
from src.piping.service import PipingVerificationService
from src.rotating.service import RotatingVerificationService
from src.steel.service import SteelVerificationService
from src.vessel.service import VesselVerificationService


OUT_JSON = ROOT / "outputs" / "ablation_failure_mode_partition.json"
OUT_MD = ROOT / "outputs" / "ablation_failure_mode_partition.md"


# Mapping from validator `check` field -> failure-mode family.
# Derived directly from src/cross_discipline/validator.py :: _CHECK_PAIRS and
# the `check=...` argument in each `_issue(...)` call.
CHECK_TO_FAMILY: Dict[str, str] = {
    # piping <-> vessel
    "piping_vessel_nozzle_margin": "piping_vessel_nozzle",
    # piping <-> rotating
    "piping_rotating_vibration_coupling": "piping_vessel_nozzle",
    "piping_rotating_nozzle_load": "piping_vessel_nozzle",
    # vessel <-> rotating
    "vessel_rotating_nozzle_load": "piping_vessel_nozzle",
    "vessel_rotating_pulsation": "piping_vessel_nozzle",
    # instrumentation <-> piping (drift / model confidence affecting piping)
    "instrumentation_piping_drift_margin": "piping_vessel_nozzle",
    "instrumentation_piping_model_confidence": "piping_vessel_nozzle",
    # steel <-> piping (pipe-rack overload / deflection / corrosion at piping interface)
    "steel_piping_pipe_rack_load": "piping_vessel_nozzle",
    "steel_piping_deflection_coupling": "piping_vessel_nozzle",
    "steel_piping_corrosion_interface": "piping_vessel_nozzle",
    # electrical <-> rotating
    "electrical_rotating_harmonic_bearing": "electrical_rotating_bearing",
    "electrical_rotating_power_quality": "electrical_rotating_bearing",
    # electrical <-> instrumentation (electrical noise into SIS)
    "electrical_instrumentation_noise_sis": "electrical_rotating_bearing",
    # steel <-> electrical (support degradation / electrical distortion)
    "structure_electrical_support_condition": "electrical_rotating_bearing",
    # civil <-> rotating
    "civil_rotating_foundation_settlement": "civil_rotating_foundation",
    "civil_rotating_crack_vibration": "civil_rotating_foundation",
    # civil <-> instrumentation (structural degradation -> SIS)
    "structure_instrumentation_sis_coupling": "civil_rotating_foundation",
}

FAMILY_ORDER: List[str] = [
    "piping_vessel_nozzle",
    "electrical_rotating_bearing",
    "civil_rotating_foundation",
    "other",
]

FAMILY_LABELS: Dict[str, str] = {
    "piping_vessel_nozzle": "Piping/Vessel nozzle-margin family",
    "electrical_rotating_bearing": "Electrical/Rotating bearing-coupling family",
    "civil_rotating_foundation": "Civil/Rotating foundation-vibration family",
    "other": "Other (unclassified)",
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


def classify_scenario(issues: List[Mapping[str, Any]]) -> Tuple[str, Dict[str, int], List[str]]:
    """Return (primary_family, per_family_blocking_count, secondary_families).

    Only blocking issues count towards family assignment (matches the
    ablation report's blocking-status definition). Ties are broken by
    FAMILY_ORDER for determinism.
    """
    family_counts: Counter[str] = Counter()
    unknown_checks: List[str] = []
    for issue in issues:
        if not issue.get("blocking"):
            continue
        check = str(issue.get("check") or "")
        family = CHECK_TO_FAMILY.get(check, "other")
        if family == "other":
            unknown_checks.append(check)
        family_counts[family] += 1

    if not family_counts:
        return "other", dict(family_counts), unknown_checks

    max_count = max(family_counts.values())
    candidates = [f for f, c in family_counts.items() if c == max_count]
    primary = next((f for f in FAMILY_ORDER if f in candidates), candidates[0])
    secondary = [f for f in FAMILY_ORDER if f in family_counts and f != primary]
    return primary, dict(family_counts), unknown_checks


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
    validator = CrossDisciplineValidator(CrossDisciplineThresholds.from_mapping(threshold_map))

    blocked_rows: List[Dict[str, Any]] = []
    family_totals: Counter[str] = Counter()
    total_scenarios = 0
    total_blocked = 0
    unknown_checks_global: Counter[str] = Counter()

    for set_name, indices in scenario_sets:
        for scenario_id, (pi, vi, ri, ei, ii, si, ci) in enumerate(indices, start=1):
            total_scenarios += 1
            p_res = engines["piping"].evaluate(all_cases["piping"][pi]["inputs"])
            v_res = engines["vessel"].evaluate(all_cases["vessel"][vi]["inputs"])
            r_res = engines["rotating"].evaluate(all_cases["rotating"][ri]["inputs"])
            e_res = engines["electrical"].evaluate(all_cases["electrical"][ei]["inputs"])
            i_res = engines["instrumentation"].evaluate(all_cases["instrumentation"][ii]["inputs"])
            s_res = engines["steel"].evaluate(all_cases["steel"][si]["inputs"])
            c_res = engines["civil"].evaluate(all_cases["civil"][ci]["inputs"])

            payload = build_payload(
                p_res=p_res, v_res=v_res, r_res=r_res, e_res=e_res,
                i_res=i_res, s_res=s_res, c_res=c_res,
            )
            cross = validator.evaluate(payload)
            if cross["status"] != "blocked":
                continue
            total_blocked += 1
            issues = list(cross.get("issues", []))
            primary, per_family, unknowns = classify_scenario(issues)
            for u in unknowns:
                unknown_checks_global[u] += 1
            family_totals[primary] += 1
            blocked_rows.append(
                {
                    "set_name": set_name,
                    "scenario_id": scenario_id,
                    "case_indices": {
                        "piping": pi, "vessel": vi, "rotating": ri,
                        "electrical": ei, "instrumentation": ii,
                        "steel": si, "civil": ci,
                    },
                    "primary_family": primary,
                    "per_family_blocking_counts": per_family,
                    "blocking_issue_codes": sorted({
                        str(i.get("code")) for i in issues if i.get("blocking")
                    }),
                    "blocking_issue_checks": sorted({
                        str(i.get("check")) for i in issues if i.get("blocking")
                    }),
                }
            )

    family_counts_ordered = {f: int(family_totals.get(f, 0)) for f in FAMILY_ORDER}
    family_sum = sum(family_counts_ordered.values())
    if family_sum != total_blocked:
        raise RuntimeError(
            f"Family count sum ({family_sum}) does not equal total blocked ({total_blocked}). "
            f"Refusing to emit a misleading partition."
        )

    return {
        "profile": active_profile,
        "profile_path": str(PROFILE_PATH),
        "total_scenarios": total_scenarios,
        "total_blocked": total_blocked,
        "family_counts": family_counts_ordered,
        "family_labels": {f: FAMILY_LABELS[f] for f in FAMILY_ORDER},
        "unknown_checks_observed": dict(unknown_checks_global),
        "blocked_rows": blocked_rows,
    }


def write_reports(report: Dict[str, Any]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines: List[str] = [
        "# Cross-Discipline Ablation: Failure-Mode Partition",
        "",
        f"- Profile: {report['profile']}",
        f"- Total Scenarios: {report['total_scenarios']}",
        f"- Total Blocked: {report['total_blocked']}",
        "",
        "## Per-Family Counts (primary family per blocked scenario)",
        "",
        "| Family | Count | Share |",
        "|---|---:|---:|",
    ]
    total = max(int(report["total_blocked"]), 1)
    for fam in FAMILY_ORDER:
        n = int(report["family_counts"].get(fam, 0))
        share = n / total
        lines.append(f"| {FAMILY_LABELS[fam]} | {n} | {share:.4f} |")
    lines.append(f"| **Sum** | **{sum(report['family_counts'].values())}** | |")
    lines.append("")
    if report.get("unknown_checks_observed"):
        lines.append("## Unknown Checks Observed (not in CHECK_TO_FAMILY)")
        for k, v in sorted(report["unknown_checks_observed"].items()):
            lines.append(f"- `{k}`: {v}")
        lines.append("")
    lines.extend(
        [
            "## Blocked Scenarios (per-row family assignment)",
            "",
            "| Set | Scenario | Primary Family | Per-Family Blocking Counts | Blocking Codes |",
            "|---|---:|---|---|---|",
        ]
    )
    for row in report["blocked_rows"]:
        per_family = ", ".join(f"{k}={v}" for k, v in sorted(row["per_family_blocking_counts"].items()))
        codes = ", ".join(row["blocking_issue_codes"]) or "-"
        lines.append(
            f"| {row['set_name']} | {row['scenario_id']} | {FAMILY_LABELS[row['primary_family']]} | "
            f"{per_family} | {codes} |"
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
