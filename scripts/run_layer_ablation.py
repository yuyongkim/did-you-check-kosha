#!/usr/bin/env python3
"""Layer-by-layer ablation matching manuscript Table 7b.

Goal (manuscript §6.6 Table 7b): replace the logically-inferred row 3 ("Calc +
KOSHA RAG (no validator)") with computed numbers.

Four configurations are evaluated explicitly, each producing two metrics:
  - "cross-discipline blocks" on the 60-scenario set
  - "KOSHA-jurisdiction detections" on the 3-case set
    (VES-GOLD-001, VES-GOLD-009, PIP-GOLD-047). A detection here means: the
    RAG retrieval returned a hit -- mandatory or guidance -- whose
    first_relevant_rank is <=10 against the case's expected reference code(s)
    or title substrings.

Configurations:
  (a) Calc engines only           : validator OFF, RAG OFF
  (b) Calc + Cross-discipline val : validator ON,  RAG OFF
  (c) Calc + KOSHA RAG only       : validator OFF, RAG ON
  (d) Full system                 : validator ON,  RAG ON

K-voting note: the manuscript itself states K-voting does not affect either
of the two measured columns ("K-voting is a verification-quality layer that
does not, by itself, contribute new detections"). It is therefore ON in (d)
and treated as a no-op for column counts; we surface this assumption in the
report.

Acceptance: each configuration produces non-null integer counts for both
metrics. If any layer cannot be cleanly disabled, this script does NOT
fabricate the result -- it emits null and an explanation.

Outputs:
  outputs/layer_ablation_report.json
  outputs/layer_ablation_report.md
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping

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

from src.rag.local_kosha_rag import (
    DEFAULT_INDEX_PATH,
    connect_db,
    search_index,
)
from scripts.benchmark_rag_retrieval import first_relevant_rank


OUT_JSON = ROOT / "outputs" / "layer_ablation_report.json"
OUT_MD = ROOT / "outputs" / "layer_ablation_report.md"


# Mirrors the 3-case set from scripts/benchmark_rag_retrieval.py::evaluate_case_ablation
RAG_CASE_SET = [
    {
        "case_id": "VES-GOLD-001",
        "query": "pressure vessel remaining life assessment",
        "discipline": "vessel",
        "expected_ref_codes": {"M-69-2012"},
        "expected_title_substrings": [],
    },
    {
        "case_id": "VES-GOLD-009",
        "query": "risk based inspection vessel",
        "discipline": "",
        "expected_ref_codes": {"C-C-23-2026", "B-M-18-2026"},
        "expected_title_substrings": [],
    },
    {
        "case_id": "PIP-GOLD-047",
        "query": "chloride sour service corrosion prevention piping occupational safety statute Article 256",
        "discipline": "",
        "expected_ref_codes": {"B-M-18-2026", "C-C-75-2026"},
        "expected_title_substrings": ["제256조 부식 방지"],
    },
]


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


def evaluate_cross_discipline_blocks(
    *,
    all_cases: Dict[str, list[dict[str, Any]]],
    threshold_map: Mapping[str, Any],
    validator_on: bool,
) -> Dict[str, Any]:
    """Run the same 60-scenario set the ablation paper uses.

    When validator_on is False, this function does NOT call the validator at
    all -- equivalent to disabling the cross-discipline coupling layer.
    When True, the active threshold profile is used.
    """
    grouped = build_grouped(all_cases)
    scenario_sets = [
        ("aligned_standard", build_indices_aligned(grouped, "standard", 10)),
        ("aligned_boundary", build_indices_aligned(grouped, "boundary", 8)),
        ("aligned_failure", build_indices_aligned(grouped, "failure_mode", 5)),
        ("mixed_first20", build_indices_mixed_first(all_cases, 20)),
        ("mixed_random20", build_indices_mixed_random(all_cases, 20)),
    ]

    engines = build_engines()
    validator = CrossDisciplineValidator(CrossDisciplineThresholds.from_mapping(threshold_map)) if validator_on else None

    total = 0
    blocked = 0
    per_set: List[Dict[str, Any]] = []

    for set_name, indices in scenario_sets:
        set_total = 0
        set_blocked = 0
        for (pi, vi, ri, ei, ii, si, ci) in indices:
            set_total += 1
            total += 1
            if validator is None:
                # validator OFF -> by construction no cross-discipline blocks
                continue
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
            if cross["status"] == "blocked":
                blocked += 1
                set_blocked += 1
        per_set.append({"set_name": set_name, "total": set_total, "blocked": set_blocked})

    return {"total": total, "blocked": blocked, "per_set": per_set}


def evaluate_kosha_detections(*, rag_on: bool) -> Dict[str, Any]:
    """Run the 3-case RAG detection evaluation.

    When rag_on is False, the RAG layer is disabled and the detected count is
    0/3 by construction (the calculation engines alone do not consult KOSHA).
    """
    rows: List[Dict[str, Any]] = []
    detected = 0

    if not rag_on:
        for item in RAG_CASE_SET:
            rows.append(
                {
                    "case_id": item["case_id"],
                    "rag_detected": False,
                    "first_relevant_rank": None,
                }
            )
        return {"total": len(RAG_CASE_SET), "detected": 0, "rows": rows}

    conn = connect_db(DEFAULT_INDEX_PATH)
    try:
        for item in RAG_CASE_SET:
            hits = search_index(conn, item["query"], 10, discipline=item["discipline"])
            rank = first_relevant_rank(
                hits, item["expected_ref_codes"], list(item["expected_title_substrings"]), 10
            )
            row_detected = rank is not None and rank <= 10
            if row_detected:
                detected += 1
            rows.append(
                {
                    "case_id": item["case_id"],
                    "rag_detected": row_detected,
                    "first_relevant_rank": rank,
                }
            )
    finally:
        conn.close()

    return {"total": len(RAG_CASE_SET), "detected": detected, "rows": rows}


def run() -> Dict[str, Any]:
    profile_data = load_profiles()
    profiles = profile_data.get("profiles", {})
    active_profile = str(profile_data.get("active_profile", "balanced"))
    threshold_map = profiles.get(active_profile) or profiles.get("balanced") or {}

    all_cases = load_all_cases()

    configurations = [
        {
            "key": "calc_only",
            "label": "Calc engines only",
            "validator_on": False,
            "rag_on": False,
            "k_voting_on": False,
        },
        {
            "key": "calc_plus_validator",
            "label": "Calc + Cross-discipline validator",
            "validator_on": True,
            "rag_on": False,
            "k_voting_on": False,
        },
        {
            "key": "calc_plus_rag",
            "label": "Calc + KOSHA RAG (no K-voting, no validator)",
            "validator_on": False,
            "rag_on": True,
            "k_voting_on": False,
        },
        {
            "key": "full_system",
            "label": "Full system (Calc + K-voting + Validator + RAG)",
            "validator_on": True,
            "rag_on": True,
            "k_voting_on": True,
        },
    ]

    rows: List[Dict[str, Any]] = []
    for cfg in configurations:
        cd = evaluate_cross_discipline_blocks(
            all_cases=all_cases,
            threshold_map=threshold_map,
            validator_on=cfg["validator_on"],
        )
        kr = evaluate_kosha_detections(rag_on=cfg["rag_on"])
        rows.append(
            {
                **cfg,
                "cross_discipline_blocks": {
                    "blocked": cd["blocked"],
                    "total": cd["total"],
                    "per_set": cd["per_set"],
                },
                "kosha_jurisdiction_detections": {
                    "detected": kr["detected"],
                    "total": kr["total"],
                    "rows": kr["rows"],
                },
            }
        )

    return {
        "profile": active_profile,
        "profile_path": str(PROFILE_PATH),
        "k_voting_assumption": (
            "K-voting is a verification-quality layer that does not, by "
            "itself, change either of the two columns measured here. Per "
            "the manuscript (PAPER_JLP_REVISED_v2.md, §6.6, last paragraph "
            "of Layer-B), K-voting suppresses numerical-precision artefacts "
            "but does not contribute new cross-discipline blocks or new "
            "KOSHA detections. The K-voting toggle therefore has no effect "
            "on these two counts."
        ),
        "configurations": rows,
    }


def write_reports(report: Dict[str, Any]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# Layer-by-Layer Ablation Report (Table 7b)",
        "",
        f"- Profile: {report['profile']}",
        "",
        "## Table 7b: Internal Ablation by System Layer",
        "",
        "| Configuration | Cross-discipline blocks (60-case set) | KOSHA-jurisdiction detections (3-case set) |",
        "|---|---:|---:|",
    ]
    for cfg in report["configurations"]:
        cd = cfg["cross_discipline_blocks"]
        kr = cfg["kosha_jurisdiction_detections"]
        lines.append(
            f"| {cfg['label']} | {cd['blocked']} / {cd['total']} | {kr['detected']} / {kr['total']} |"
        )
    lines.extend(
        [
            "",
            "## K-voting Assumption",
            "",
            report["k_voting_assumption"],
            "",
            "## Per-Configuration Detail",
            "",
        ]
    )
    for cfg in report["configurations"]:
        lines.append(f"### {cfg['label']}")
        lines.append("")
        lines.append(
            f"- validator_on={cfg['validator_on']}, rag_on={cfg['rag_on']}, k_voting_on={cfg['k_voting_on']}"
        )
        lines.append(f"- cross-discipline blocks: {cfg['cross_discipline_blocks']['blocked']} / {cfg['cross_discipline_blocks']['total']}")
        for s in cfg["cross_discipline_blocks"]["per_set"]:
            lines.append(f"  - {s['set_name']}: {s['blocked']}/{s['total']}")
        lines.append(
            f"- KOSHA detections: {cfg['kosha_jurisdiction_detections']['detected']} / {cfg['kosha_jurisdiction_detections']['total']}"
        )
        for r in cfg["kosha_jurisdiction_detections"]["rows"]:
            lines.append(f"  - {r['case_id']}: rag_detected={r['rag_detected']}, first_relevant_rank={r['first_relevant_rank']}")
        lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    report = run()
    write_reports(report)
    print(f"REPORT_JSON={OUT_JSON}")
    print(f"REPORT_MD={OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
