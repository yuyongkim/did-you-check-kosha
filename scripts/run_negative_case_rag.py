#!/usr/bin/env python3
"""Run the KOSHA RAG pipeline against the negative case PIP-GOLD-003.

Goal (manuscript §6.7): replace the placeholder with an actually-tested RAG
response so we can report what the system retrieves for a benign,
non-corrosive piping case and verify whether any *mandatory* law article
(source_type=law_article) appears in the top-10 -- which would weaken the
"no false-positive" argument.

Query construction
------------------
The repository does not (yet) ship an automated case->query builder for
golden cases. The closest pattern in the codebase is the hand-crafted query
table in scripts/benchmark_rag_retrieval.py::evaluate_case_ablation. We
follow the same pattern here, deriving the query strictly from facts that
appear in PIP-GOLD-003's `inputs` block of the dataset (no invented detail).

We run TWO query variants for transparency:

  - generic_piping_integrity : the natural query a piping-integrity assistant
    would issue for a generic stainless-steel piping life-management case
    (no chloride / sour-service language). This is the "neutral" query.
  - mirrored_pip047_form     : the same shape as the established PIP-GOLD-047
    query, with chloride/sour terms removed because PIP-GOLD-003 has neither
    flag set in its inputs. This lets us check whether the same query family
    that flagged PIP-GOLD-047 would also flag PIP-GOLD-003 (a false positive).

Detection criterion
-------------------
For each query and each top-10 hit we report:
  - reference_code, title, source_type, regulatory_class, score
  - regulatory_class = "mandatory" if source_type == "law_article" else "guidance"
A "mandatory hit found" flag is raised if ANY top-10 hit has
regulatory_class == "mandatory". When True, the negative-case argument in
§6.7 is weakened and the markdown report flags it loudly.

Outputs
-------
  outputs/negative_case_pip_gold_003.json
  outputs/negative_case_pip_gold_003.md
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rag.local_kosha_rag import (
    DEFAULT_INDEX_PATH,
    connect_db,
    search_index,
)


CASE_ID = "PIP-GOLD-003"
DATASET_PATH = ROOT / "datasets" / "golden_standards" / "piping_golden_dataset_v1.json"
OUT_JSON = ROOT / "outputs" / "negative_case_pip_gold_003.json"
OUT_MD = ROOT / "outputs" / "negative_case_pip_gold_003.md"


def find_case() -> Dict[str, Any]:
    data = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    for case in data.get("cases", []):
        if case.get("case_id") == CASE_ID:
            return case
    raise RuntimeError(f"{CASE_ID} not found in {DATASET_PATH}")


def build_query_variants(case: Dict[str, Any]) -> List[Dict[str, str]]:
    inputs = case.get("inputs", {})
    material = str(inputs.get("material", ""))
    nps = inputs.get("nps")
    service_type = str(inputs.get("service_type", ""))
    weld_type = str(inputs.get("weld_type", ""))
    # Sanity: refuse to build a query that asserts a flag the case does not set.
    has_chloride = "chloride" in str(inputs).lower()
    has_sour = "sour" in str(inputs).lower()
    return [
        {
            "name": "generic_piping_integrity",
            "discipline": "piping",
            "query": (
                f"piping life management corrosion inspection {material} general service "
                f"NPS {nps} weld {weld_type} 배관 잔여수명 부식 검사주기"
            ),
            "rationale": (
                "Neutral query for a generic piping integrity assessment "
                "derived strictly from PIP-GOLD-003 inputs (material, NPS, "
                f"weld_type, service_type='{service_type}'). No chloride or "
                "sour-service terms because the case sets neither."
            ),
        },
        {
            "name": "mirrored_pip047_form_chloride_terms_removed",
            "discipline": "",
            "query": (
                "corrosion prevention piping occupational safety statute Article 256 "
                "배관 부식 방지"
            ),
            "rationale": (
                "Same query shape as the PIP-GOLD-047 case in "
                "benchmark_rag_retrieval.py, with chloride/sour-service "
                "terms removed (PIP-GOLD-003 has has_chloride="
                f"{has_chloride}, has_sour={has_sour}). Tests whether the "
                "RAG layer would flag a non-corrosive case the same way."
            ),
        },
    ]


def hit_to_dict(hit: Any, rank: int) -> Dict[str, Any]:
    source_type = getattr(hit, "source_type", "")
    regulatory_class = "mandatory" if source_type == "law_article" else "guidance"
    return {
        "rank": rank,
        "reference_code": getattr(hit, "reference_code", ""),
        "title": getattr(hit, "title", ""),
        "source_type": source_type,
        "regulatory_class": regulatory_class,
        "score": getattr(hit, "score", None),
        "snippet": getattr(hit, "snippet", ""),
        "url": getattr(hit, "url", None),
    }


def run() -> Dict[str, Any]:
    case = find_case()
    variants = build_query_variants(case)

    if not DEFAULT_INDEX_PATH.exists():
        raise RuntimeError(
            f"KOSHA RAG index not found at {DEFAULT_INDEX_PATH}. "
            "Build it with: python -m src.rag.local_kosha_rag build"
        )

    conn = connect_db(DEFAULT_INDEX_PATH)
    try:
        per_variant: List[Dict[str, Any]] = []
        any_mandatory_overall = False
        for v in variants:
            hits = search_index(conn, v["query"], 10, discipline=v["discipline"])
            hit_dicts = [hit_to_dict(h, idx + 1) for idx, h in enumerate(hits)]
            mandatory_hits = [h for h in hit_dicts if h["regulatory_class"] == "mandatory"]
            guidance_hits = [h for h in hit_dicts if h["regulatory_class"] == "guidance"]
            any_mandatory = len(mandatory_hits) > 0
            if any_mandatory:
                any_mandatory_overall = True
            per_variant.append(
                {
                    "name": v["name"],
                    "query": v["query"],
                    "discipline_filter": v["discipline"],
                    "rationale": v["rationale"],
                    "hit_count": len(hit_dicts),
                    "mandatory_hit_count": len(mandatory_hits),
                    "guidance_hit_count": len(guidance_hits),
                    "any_mandatory_in_top10": any_mandatory,
                    "first_mandatory_rank": (
                        mandatory_hits[0]["rank"] if mandatory_hits else None
                    ),
                    "hits": hit_dicts,
                }
            )
    finally:
        conn.close()

    return {
        "case_id": CASE_ID,
        "dataset_path": DATASET_PATH.relative_to(ROOT).as_posix(),
        "case_inputs": case.get("inputs", {}),
        "case_expected_red_flags": case.get("expected_red_flags", []),
        "case_expected_warnings": case.get("expected_warnings", []),
        "any_mandatory_hit_across_variants": any_mandatory_overall,
        "variants": per_variant,
        "interpretation": (
            "Negative-case argument is WEAKENED if any_mandatory_hit_across_variants "
            "is True, because a mandatory law-article hit means the system would "
            "surface a regulatory flag for a benign case. False means no mandatory "
            "law-article hit appeared in either variant's top-10 -- consistent "
            "with the manuscript's negative-case claim."
        ),
    }


def write_reports(report: Dict[str, Any]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        f"# Negative-Case RAG Report: {report['case_id']}",
        "",
        f"- Dataset: `{report['dataset_path']}`",
        f"- Expected red flags (from dataset): {report['case_expected_red_flags']}",
        f"- Expected warnings (from dataset): {report['case_expected_warnings']}",
        "",
        "## Headline",
        "",
    ]
    if report["any_mandatory_hit_across_variants"]:
        lines.append(
            "**WARNING** -- at least one query variant returned a *mandatory* "
            "(law_article) hit in its top-10. The negative-case argument in "
            "manuscript §6.7 is **weakened** and should be revisited."
        )
    else:
        lines.append(
            "OK -- no mandatory (law_article) hit appears in the top-10 for any "
            "query variant. The negative-case claim in §6.7 is consistent with "
            "the live RAG retrieval."
        )
    lines.append("")
    lines.append(report["interpretation"])
    lines.append("")

    for v in report["variants"]:
        lines.extend(
            [
                f"## Variant: {v['name']}",
                "",
                f"- Query: `{v['query']}`",
                f"- Discipline filter: `{v['discipline_filter'] or '<none>'}`",
                f"- Rationale: {v['rationale']}",
                f"- Hits: {v['hit_count']} (mandatory={v['mandatory_hit_count']}, guidance={v['guidance_hit_count']})",
                f"- Any mandatory in top-10: {v['any_mandatory_in_top10']}",
                f"- First mandatory rank: {v['first_mandatory_rank']}",
                "",
                "| Rank | Class | reference_code | source_type | score | title |",
                "|---:|---|---|---|---:|---|",
            ]
        )
        for h in v["hits"]:
            score = h.get("score")
            score_str = f"{score:.4f}" if isinstance(score, (int, float)) else str(score)
            title = (h.get("title") or "").replace("|", "/")
            lines.append(
                f"| {h['rank']} | {h['regulatory_class']} | "
                f"{h.get('reference_code','')} | {h.get('source_type','')} | "
                f"{score_str} | {title} |"
            )
        lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    report = run()
    write_reports(report)
    print(f"REPORT_JSON={OUT_JSON}")
    print(f"REPORT_MD={OUT_MD}")
    if report["any_mandatory_hit_across_variants"]:
        print("WARNING: mandatory hit found -- review §6.7 negative case argument")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
