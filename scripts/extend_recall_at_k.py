#!/usr/bin/env python3
"""Recall@K curve extension (K = 1..10) for the 50-query KOSHA RAG benchmark.

Goal (manuscript §6.5 / R2.3 follow-up): the existing
`outputs/rag_retrieval_report.md` reports R@1, R@3, R@5 and MRR@10. Adding
the full Recall@K curve through K = 10 (with R@7 and R@10 explicitly
called out) closes the upper end and exposes the saturation behaviour of
the synonym-aware variant.

This script reuses the retrieval logic from `scripts/benchmark_rag_retrieval.py`
verbatim (same first-relevant-rank extractor, same eval queries, same DB).
It also runs a paired bootstrap (1000 draws, seed = 20260508) per K so the
manuscript can quote a 95% CI on every K.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

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
from scripts.benchmark_rag_retrieval import (
    QUERY_DATASET,
    first_relevant_rank,
    read_query_dataset,
)


OUT_JSON = ROOT / "outputs" / "rag_retrieval_extended.json"
OUT_MD = ROOT / "outputs" / "rag_retrieval_extended.md"

K_VALUES = list(range(1, 11))  # 1..10
HIGHLIGHT_K = (7, 10)
BOOTSTRAP_DRAWS = 1000
SEED = 20260508


def collect_per_query_ranks(conn) -> Tuple[List[Dict[str, Any]], List[Optional[int]], List[Optional[int]]]:
    data = read_query_dataset()
    groups = list(data.get("groups", []))

    query_records: List[Dict[str, Any]] = []
    plain_ranks: List[Optional[int]] = []
    enhanced_ranks: List[Optional[int]] = []

    for group in groups:
        discipline = str(group.get("discipline") or "")
        expected_ref_codes = set(group.get("expected_ref_codes", []))
        expected_title_substrings = list(group.get("expected_title_substrings", []))
        for query in group.get("queries", []):
            plain_hits = search_index_with_fts_query(
                conn, make_plain_fts_query(query), query, 10, discipline=discipline
            )
            enhanced_hits = search_index(conn, query, 10, discipline=discipline)
            p_rank = first_relevant_rank(plain_hits, expected_ref_codes, expected_title_substrings, 10)
            e_rank = first_relevant_rank(enhanced_hits, expected_ref_codes, expected_title_substrings, 10)
            query_records.append(
                {
                    "group": group["label"],
                    "query": query,
                    "plain_rank": p_rank,
                    "enhanced_rank": e_rank,
                }
            )
            plain_ranks.append(p_rank)
            enhanced_ranks.append(e_rank)

    return query_records, plain_ranks, enhanced_ranks


def rank_array(ranks: List[Optional[int]]) -> np.ndarray:
    return np.asarray([0 if r is None else int(r) for r in ranks], dtype=np.int32)


def recall_at_k(arr: np.ndarray, k: int) -> float:
    if arr.size == 0:
        return 0.0
    return float(np.mean((arr >= 1) & (arr <= k)))


def percentile_ci(samples: np.ndarray) -> Dict[str, float]:
    return {
        "mean": float(np.mean(samples)),
        "ci_lo_2_5": float(np.percentile(samples, 2.5)),
        "ci_hi_97_5": float(np.percentile(samples, 97.5)),
    }


def bootstrap_recall(
    plain_arr: np.ndarray, enh_arr: np.ndarray, k_values: List[int], n_draws: int, seed: int
) -> Dict[str, Any]:
    n = plain_arr.shape[0]
    if n == 0:
        raise RuntimeError("No queries available for bootstrap.")
    rng = np.random.default_rng(seed)
    plain_samples = {k: np.zeros(n_draws, dtype=np.float64) for k in k_values}
    enh_samples = {k: np.zeros(n_draws, dtype=np.float64) for k in k_values}
    delta_samples = {k: np.zeros(n_draws, dtype=np.float64) for k in k_values}
    for d in range(n_draws):
        idx = rng.integers(low=0, high=n, size=n)
        p_sample = plain_arr[idx]
        e_sample = enh_arr[idx]
        for k in k_values:
            p_val = recall_at_k(p_sample, k)
            e_val = recall_at_k(e_sample, k)
            plain_samples[k][d] = p_val
            enh_samples[k][d] = e_val
            delta_samples[k][d] = e_val - p_val
    return {
        "plain": {str(k): percentile_ci(plain_samples[k]) for k in k_values},
        "enhanced": {str(k): percentile_ci(enh_samples[k]) for k in k_values},
        "delta": {str(k): percentile_ci(delta_samples[k]) for k in k_values},
    }


def run() -> Dict[str, Any]:
    if not DEFAULT_INDEX_PATH.exists():
        raise RuntimeError(
            f"KOSHA RAG index not found at {DEFAULT_INDEX_PATH}. "
            "Build it with: python -m src.rag.local_kosha_rag build"
        )

    conn = connect_db(DEFAULT_INDEX_PATH)
    try:
        records, plain_ranks, enhanced_ranks = collect_per_query_ranks(conn)
    finally:
        conn.close()

    plain_arr = rank_array(plain_ranks)
    enh_arr = rank_array(enhanced_ranks)

    point_plain = {str(k): recall_at_k(plain_arr, k) for k in K_VALUES}
    point_enhanced = {str(k): recall_at_k(enh_arr, k) for k in K_VALUES}
    point_delta = {str(k): point_enhanced[str(k)] - point_plain[str(k)] for k in K_VALUES}

    boot = bootstrap_recall(plain_arr, enh_arr, K_VALUES, BOOTSTRAP_DRAWS, SEED)

    return {
        "dataset": QUERY_DATASET.relative_to(ROOT).as_posix(),
        "query_count": int(plain_arr.shape[0]),
        "k_values": K_VALUES,
        "highlight_k": list(HIGHLIGHT_K),
        "bootstrap_draws": BOOTSTRAP_DRAWS,
        "seed": SEED,
        "point_estimates": {
            "plain": point_plain,
            "enhanced": point_enhanced,
            "delta": point_delta,
        },
        "bootstrap_ci": boot,
        "per_query_records": records,
    }


def write_reports(report: Dict[str, Any]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# RAG Retrieval Recall@K Extension (K=1..10)",
        "",
        f"- Dataset: `{report['dataset']}`",
        f"- Queries: {report['query_count']}",
        f"- Bootstrap draws: {report['bootstrap_draws']} (seed={report['seed']})",
        "- Highlight K (added beyond the headline R@5): "
        + ", ".join(f"R@{k}" for k in report["highlight_k"]),
        "",
        "## Point Estimates per K",
        "",
        "| K | Plain | Enhanced | Delta (E - P) |",
        "|---:|---:|---:|---:|",
    ]
    pe = report["point_estimates"]
    for k in report["k_values"]:
        sk = str(k)
        lines.append(
            f"| {k} | {pe['plain'][sk]:.4f} | {pe['enhanced'][sk]:.4f} | {pe['delta'][sk]:+.4f} |"
        )

    lines.extend(
        [
            "",
            "## Bootstrap 95% CI per K (Plain mode)",
            "",
            "| K | Mean | 2.5% | 97.5% |",
            "|---:|---:|---:|---:|",
        ]
    )
    for k in report["k_values"]:
        v = report["bootstrap_ci"]["plain"][str(k)]
        lines.append(f"| {k} | {v['mean']:.4f} | {v['ci_lo_2_5']:.4f} | {v['ci_hi_97_5']:.4f} |")
    lines.extend(
        [
            "",
            "## Bootstrap 95% CI per K (Enhanced mode)",
            "",
            "| K | Mean | 2.5% | 97.5% |",
            "|---:|---:|---:|---:|",
        ]
    )
    for k in report["k_values"]:
        v = report["bootstrap_ci"]["enhanced"][str(k)]
        lines.append(f"| {k} | {v['mean']:.4f} | {v['ci_lo_2_5']:.4f} | {v['ci_hi_97_5']:.4f} |")
    lines.extend(
        [
            "",
            "## Paired Difference (Enhanced - Plain) per K",
            "",
            "| K | Mean | 2.5% | 97.5% | CI excludes 0? |",
            "|---:|---:|---:|---:|---|",
        ]
    )
    for k in report["k_values"]:
        v = report["bootstrap_ci"]["delta"][str(k)]
        excludes = "yes" if (v["ci_lo_2_5"] > 0 or v["ci_hi_97_5"] < 0) else "no"
        lines.append(
            f"| {k} | {v['mean']:+.4f} | {v['ci_lo_2_5']:+.4f} | {v['ci_hi_97_5']:+.4f} | {excludes} |"
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
