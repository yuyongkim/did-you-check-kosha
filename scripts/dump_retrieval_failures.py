#!/usr/bin/env python3
"""Inventory of retrieval failures on the 50-query KOSHA RAG benchmark.

Goal (manuscript §7 honest-weakness paragraph): of the 50 curated queries,
list every Enhanced-mode failure (rank > 5 OR no relevant hit at all in
top-10), report the actual top-3 hits, the relevant target's true rank
(or "not in top-10"), and tag each failure with a diagnosis category from
a small fixed vocabulary.

Diagnosis vocabulary (chosen by inspection - never invented):
  - paraphrase_too_loose             query is so loose that BM25 can't link it to the target
  - target_buried_under_high_BM25_overlap   target is in top-10 but ranked > 5 because
                                            other chunks share more surface tokens
  - target_indexed_under_different_chunk    expected target appears in a different chunk
                                            than the one the index returns first
  - regulatory_class_mismatch        retrieved hits are off-topic regulatory class
  - other                            anything not clearly fitting the above
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rag.local_kosha_rag import (
    DEFAULT_INDEX_PATH,
    SearchHit,
    connect_db,
    search_index,
)
from scripts.benchmark_rag_retrieval import (
    QUERY_DATASET,
    dedupe_hits,
    is_relevant,
    read_query_dataset,
)


OUT_JSON = ROOT / "outputs" / "retrieval_failure_inventory.json"
OUT_MD = ROOT / "outputs" / "retrieval_failure_inventory.md"

TARGET_K = 5  # failure threshold: rank > TARGET_K under Enhanced FTS


def true_rank_in_topk(
    hits: Iterable[SearchHit],
    expected_ref_codes: set[str],
    expected_title_substrings: list[str],
    top_k: int = 10,
) -> Optional[int]:
    """Return rank of first relevant hit within top_k, else None."""
    unique_hits = dedupe_hits(hits)[:top_k]
    for idx, hit in enumerate(unique_hits, start=1):
        if is_relevant(hit, expected_ref_codes, expected_title_substrings):
            return idx
    return None


def diagnose_failure(
    query: str,
    hits: List[SearchHit],
    expected_ref_codes: set[str],
    expected_title_substrings: list[str],
    true_rank: Optional[int],
    target_label: str,
) -> str:
    """Pick a diagnosis tag from observable evidence; default to 'other' when ambiguous."""
    unique_hits = dedupe_hits(hits)
    top10 = unique_hits[:10]

    # If the relevant target appears within top-10 but worse than TARGET_K,
    # the target is "buried" by surface-overlap alternatives.
    if true_rank is not None and true_rank > TARGET_K:
        return "target_buried_under_high_BM25_overlap"

    # If the relevant target is not in top-10 at all but appears anywhere
    # later in the candidate set, classify as 'target_indexed_under_different_chunk'.
    later_hit = next(
        (
            idx
            for idx, hit in enumerate(unique_hits, start=1)
            if is_relevant(hit, expected_ref_codes, expected_title_substrings)
        ),
        None,
    )
    if true_rank is None and later_hit is not None:
        return "target_indexed_under_different_chunk"

    # If no relevant hit at all and the top-10 retrievers share no
    # reference_code prefix with the expected target group, call it
    # 'regulatory_class_mismatch'.
    if true_rank is None and not later_hit:
        # Heuristic: if expected_ref_codes is non-empty and none of top-10
        # reference codes share the leading 3-character prefix, regulatory class mismatch.
        if expected_ref_codes:
            expected_prefixes = {c.split("-")[0] for c in expected_ref_codes if c}
            top_prefixes = {
                (h.reference_code or "").split("-")[0]
                for h in top10
                if h.reference_code
            }
            if expected_prefixes and not (expected_prefixes & top_prefixes):
                return "regulatory_class_mismatch"
        # Otherwise paraphrase too loose
        return "paraphrase_too_loose"

    return "other"


def collect_failures(conn) -> Dict[str, Any]:
    data = read_query_dataset()
    groups = list(data.get("groups", []))

    failures: List[Dict[str, Any]] = []
    queries_total = 0

    for group in groups:
        discipline = str(group.get("discipline") or "")
        expected_ref_codes = set(group.get("expected_ref_codes", []))
        expected_title_substrings = list(group.get("expected_title_substrings", []))
        target_label = str(group.get("label") or "")

        for query in group.get("queries", []):
            queries_total += 1
            hits = search_index(conn, query, 10, discipline=discipline)
            rank = true_rank_in_topk(hits, expected_ref_codes, expected_title_substrings, top_k=10)
            is_failure = (rank is None) or (rank > TARGET_K)
            if not is_failure:
                continue

            top3 = dedupe_hits(hits)[:3]
            top3_pairs = [
                {"reference_code": h.reference_code, "title": h.title}
                for h in top3
            ]
            diagnosis = diagnose_failure(
                query, hits, expected_ref_codes, expected_title_substrings, rank, target_label
            )
            failures.append(
                {
                    "group_label": target_label,
                    "discipline_filter": discipline or None,
                    "query": query,
                    "expected_ref_codes": sorted(expected_ref_codes),
                    "expected_title_substrings": expected_title_substrings,
                    "actual_first_relevant_rank": rank,  # None means not in top-10
                    "top3_hits": top3_pairs,
                    "diagnosis": diagnosis,
                }
            )

    diagnosis_counts: Dict[str, int] = {}
    for row in failures:
        diagnosis_counts[row["diagnosis"]] = diagnosis_counts.get(row["diagnosis"], 0) + 1

    return {
        "dataset": QUERY_DATASET.relative_to(ROOT).as_posix(),
        "total_queries": queries_total,
        "failure_threshold_K": TARGET_K,
        "failure_rule": f"failure := first_relevant_rank > {TARGET_K} OR no relevant hit in top-10",
        "failure_count": len(failures),
        "failure_rate": (len(failures) / queries_total) if queries_total else 0.0,
        "diagnosis_counts": diagnosis_counts,
        "failures": failures,
    }


def write_reports(report: Dict[str, Any]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# KOSHA RAG Retrieval Failure Inventory (Enhanced FTS, K=5 threshold)",
        "",
        f"- Dataset: `{report['dataset']}`",
        f"- Total queries: {report['total_queries']}",
        f"- Failure rule: `{report['failure_rule']}`",
        f"- Failure count: {report['failure_count']}",
        f"- Failure rate: {report['failure_rate']:.4f}",
        "",
        "## Diagnosis Summary",
        "",
        "| Diagnosis | Count |",
        "|---|---:|",
    ]
    if report["diagnosis_counts"]:
        for tag in sorted(report["diagnosis_counts"]):
            lines.append(f"| {tag} | {report['diagnosis_counts'][tag]} |")
    else:
        lines.append("| (no failures) | 0 |")

    lines.extend(["", "## Failure Details", ""])
    if not report["failures"]:
        lines.append("_No queries failed under the configured threshold._")
    for row in report["failures"]:
        rank_str = "not in top-10" if row["actual_first_relevant_rank"] is None else str(row["actual_first_relevant_rank"])
        lines.append(f"### {row['group_label']} | {row['diagnosis']}")
        lines.append("")
        lines.append(f"- Query: `{row['query']}`")
        lines.append(f"- Discipline filter: `{row['discipline_filter']}`")
        lines.append(f"- Expected ref codes: {row['expected_ref_codes']}")
        if row["expected_title_substrings"]:
            lines.append(f"- Expected title substrings: {row['expected_title_substrings']}")
        lines.append(f"- Actual first relevant rank: {rank_str}")
        lines.append("- Top-3 hits:")
        for i, hit in enumerate(row["top3_hits"], start=1):
            lines.append(f"  {i}. ref=`{hit['reference_code']}` title=`{hit['title']}`")
        lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> Dict[str, Any]:
    if not DEFAULT_INDEX_PATH.exists():
        raise RuntimeError(
            f"KOSHA RAG index not found at {DEFAULT_INDEX_PATH}. "
            "Build it with: python -m src.rag.local_kosha_rag build"
        )
    conn = connect_db(DEFAULT_INDEX_PATH)
    try:
        report = collect_failures(conn)
    finally:
        conn.close()
    return report


def main() -> int:
    report = run()
    write_reports(report)
    print(f"REPORT_JSON={OUT_JSON}")
    print(f"REPORT_MD={OUT_MD}")
    print(f"FAILURE_COUNT={report['failure_count']}/{report['total_queries']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
