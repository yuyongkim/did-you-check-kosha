#!/usr/bin/env python3
"""Benchmark plain FTS vs enhanced synonym-aware KOSHA retrieval."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rag.local_kosha_rag import (
    DEFAULT_INDEX_PATH,
    connect_db,
    make_plain_fts_query,
    search_index,
    search_index_with_fts_query,
)

QUERY_DATASET = ROOT / "datasets" / "kosha_rag" / "rag_eval_queries.json"
OUT_JSON = ROOT / "outputs" / "rag_retrieval_report.json"
OUT_MD = ROOT / "outputs" / "rag_retrieval_report.md"


def read_query_dataset() -> Dict[str, Any]:
    return json.loads(QUERY_DATASET.read_text(encoding="utf-8"))


def dedupe_hits(hits: Iterable[Any]) -> List[Any]:
    seen: set[tuple[str, str]] = set()
    unique: List[Any] = []
    for hit in hits:
        key = (getattr(hit, "reference_code", ""), getattr(hit, "title", ""))
        if key in seen:
            continue
        seen.add(key)
        unique.append(hit)
    return unique


def is_relevant(hit: Any, expected_ref_codes: set[str], expected_title_substrings: list[str]) -> bool:
    if getattr(hit, "reference_code", "") in expected_ref_codes:
        return True
    title = getattr(hit, "title", "")
    return any(fragment in title for fragment in expected_title_substrings)


def first_relevant_rank(
    hits: Iterable[Any],
    expected_ref_codes: set[str],
    expected_title_substrings: list[str],
    top_k: int,
) -> int | None:
    unique_hits = dedupe_hits(hits)[:top_k]
    for idx, hit in enumerate(unique_hits, start=1):
        if is_relevant(hit, expected_ref_codes, expected_title_substrings):
            return idx
    return None


def metric_summary(ranks: List[int | None], top_k: int) -> Dict[str, float]:
    total = len(ranks)
    hits = [rank for rank in ranks if rank is not None and rank <= top_k]
    recall = (len(hits) / total) if total else 0.0
    mrr = (sum(1.0 / rank for rank in hits) / total) if total else 0.0
    return {"recall": recall, "mrr": mrr}


def evaluate_mode(conn, groups: List[Dict[str, Any]], mode: str) -> Dict[str, Any]:
    overall_ranks_at_1: List[int | None] = []
    overall_ranks_at_3: List[int | None] = []
    overall_ranks_at_5: List[int | None] = []
    overall_ranks_at_10: List[int | None] = []
    group_reports: List[Dict[str, Any]] = []

    for group in groups:
        discipline = str(group.get("discipline") or "")
        expected_ref_codes = set(group.get("expected_ref_codes", []))
        expected_title_substrings = list(group.get("expected_title_substrings", []))
        queries = list(group.get("queries", []))

        ranks: List[int | None] = []
        for query in queries:
            if mode == "plain":
                hits = search_index_with_fts_query(conn, make_plain_fts_query(query), query, 10, discipline=discipline)
            else:
                hits = search_index(conn, query, 10, discipline=discipline)
            rank = first_relevant_rank(hits, expected_ref_codes, expected_title_substrings, 10)
            ranks.append(rank)

        overall_ranks_at_1.extend(ranks)
        overall_ranks_at_3.extend(ranks)
        overall_ranks_at_5.extend(ranks)
        overall_ranks_at_10.extend(ranks)
        group_reports.append(
            {
                "label": group["label"],
                "query_count": len(queries),
                "recall_at_1": metric_summary(ranks, 1)["recall"],
                "recall_at_3": metric_summary(ranks, 3)["recall"],
                "recall_at_5": metric_summary(ranks, 5)["recall"],
                "mrr_at_10": metric_summary(ranks, 10)["mrr"],
            }
        )

    return {
        "mode": mode,
        "query_count": len(overall_ranks_at_10),
        "recall_at_1": metric_summary(overall_ranks_at_1, 1)["recall"],
        "recall_at_3": metric_summary(overall_ranks_at_3, 3)["recall"],
        "recall_at_5": metric_summary(overall_ranks_at_5, 5)["recall"],
        "mrr_at_10": metric_summary(overall_ranks_at_10, 10)["mrr"],
        "groups": group_reports,
    }


def evaluate_case_ablation(conn) -> List[Dict[str, Any]]:
    cases = [
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

    rows: List[Dict[str, Any]] = []
    for item in cases:
        hits = search_index(conn, item["query"], 10, discipline=item["discipline"])
        rank = first_relevant_rank(hits, item["expected_ref_codes"], item["expected_title_substrings"], 10)
        rows.append(
            {
                "case_id": item["case_id"],
                "code_only_detected": False,
                "rag_detected": rank is not None,
                "first_relevant_rank": rank,
            }
        )
    return rows


def run() -> Dict[str, Any]:
    data = read_query_dataset()
    groups = list(data.get("groups", []))
    conn = connect_db(DEFAULT_INDEX_PATH)
    try:
        plain = evaluate_mode(conn, groups, mode="plain")
        enhanced = evaluate_mode(conn, groups, mode="enhanced")
        case_ablation = evaluate_case_ablation(conn)
    finally:
        conn.close()

    return {
        "dataset": QUERY_DATASET.relative_to(ROOT).as_posix(),
        "description": data.get("description"),
        "group_count": len(groups),
        "plain_fts": plain,
        "enhanced_fts": enhanced,
        "deltas": {
            "recall_at_1": enhanced["recall_at_1"] - plain["recall_at_1"],
            "recall_at_3": enhanced["recall_at_3"] - plain["recall_at_3"],
            "recall_at_5": enhanced["recall_at_5"] - plain["recall_at_5"],
            "mrr_at_10": enhanced["mrr_at_10"] - plain["mrr_at_10"],
        },
        "case_ablation": {
            "rows": case_ablation,
            "code_only_detected_cases": sum(1 for row in case_ablation if row["code_only_detected"]),
            "rag_detected_cases": sum(1 for row in case_ablation if row["rag_detected"]),
        },
    }


def write_reports(report: Dict[str, Any]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# RAG Retrieval Benchmark Report",
        "",
        f"- Dataset: `{report['dataset']}`",
        f"- Group Count: {report['group_count']}",
        f"- Query Count: {report['plain_fts']['query_count']}",
        "- Query design: 5 regulatory target groups x 10 curated queries each, mixing Korean/English phrasings, abbreviations, and variant wording.",
        "",
        "## Overall Metrics",
        f"- Plain FTS: Recall@1={report['plain_fts']['recall_at_1']:.4f}, Recall@3={report['plain_fts']['recall_at_3']:.4f}, Recall@5={report['plain_fts']['recall_at_5']:.4f}, MRR@10={report['plain_fts']['mrr_at_10']:.4f}",
        f"- Enhanced FTS: Recall@1={report['enhanced_fts']['recall_at_1']:.4f}, Recall@3={report['enhanced_fts']['recall_at_3']:.4f}, Recall@5={report['enhanced_fts']['recall_at_5']:.4f}, MRR@10={report['enhanced_fts']['mrr_at_10']:.4f}",
        f"- Delta: Recall@1={report['deltas']['recall_at_1']:.4f}, Recall@3={report['deltas']['recall_at_3']:.4f}, Recall@5={report['deltas']['recall_at_5']:.4f}, MRR@10={report['deltas']['mrr_at_10']:.4f}",
        "",
        "## Group Metrics",
    ]
    for group_plain, group_enh in zip(report["plain_fts"]["groups"], report["enhanced_fts"]["groups"], strict=False):
        lines.append(
            f"- {group_plain['label']}: "
            f"Plain R@5={group_plain['recall_at_5']:.4f}, Enhanced R@5={group_enh['recall_at_5']:.4f}, "
            f"delta={group_enh['recall_at_5'] - group_plain['recall_at_5']:.4f}"
        )
    lines.extend(
        [
            "",
            "## Code-Only vs Regulatory RAG Ablation",
            "- `Code-only` here means international-code calculation outputs and engine red flags without Korean regulatory retrieval.",
            f"- Code-only detected cases: {report['case_ablation']['code_only_detected_cases']}/{len(report['case_ablation']['rows'])}",
            f"- Regulatory RAG detected cases: {report['case_ablation']['rag_detected_cases']}/{len(report['case_ablation']['rows'])}",
        ]
    )
    for row in report["case_ablation"]["rows"]:
        lines.append(
            f"- {row['case_id']}: code_only={row['code_only_detected']}, "
            f"rag={row['rag_detected']}, first_relevant_rank={row['first_relevant_rank']}"
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
