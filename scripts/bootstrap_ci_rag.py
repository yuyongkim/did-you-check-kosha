#!/usr/bin/env python3
"""Bootstrap 95% CIs for the 50-query KOSHA RAG benchmark.

Goal (manuscript §6.5 / §6.6 sensitivity-analysis follow-up): produce
bootstrap confidence intervals for Recall@1, Recall@3, Recall@5, MRR@10
under both Plain and Enhanced FTS modes, plus the paired-difference
(Enhanced - Plain) CI for each metric -- the latter is the more meaningful
test for the manuscript claim of an Enhanced-mode improvement.

Approach
--------
1. Load the 50-query benchmark used by scripts/benchmark_rag_retrieval.py.
2. For each query, run retrieval ONCE per mode and store the per-query rank
   (1..10 if a relevant hit appeared, None otherwise). Bootstrap is over
   query indices, not over retrieval randomness (retrieval is deterministic
   given the SQLite FTS index).
3. Resample query indices with replacement (n=50 each draw), 1000 draws,
   seed=20260508. For each draw recompute Recall@k and MRR@10 in both modes
   plus the paired delta. Report mean, 2.5/97.5 percentiles.

Outputs
-------
  outputs/rag_bootstrap_ci_report.json
  outputs/rag_bootstrap_ci_report.md
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

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


OUT_JSON = ROOT / "outputs" / "rag_bootstrap_ci_report.json"
OUT_MD = ROOT / "outputs" / "rag_bootstrap_ci_report.md"

BOOTSTRAP_DRAWS = 1000
SEED = 20260508


def collect_per_query_ranks(conn) -> Tuple[List[Dict[str, Any]], List[Optional[int]], List[Optional[int]]]:
    """Return (query_records, plain_ranks, enhanced_ranks) aligned by index."""
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


def metric_array(ranks: List[Optional[int]]) -> np.ndarray:
    """Encode ranks as integer array; None -> 0 (sentinel meaning 'no relevant hit'),
    otherwise the rank in [1, 10]. Recall@k tests rank in [1..k].
    """
    return np.asarray([0 if r is None else int(r) for r in ranks], dtype=np.int32)


def recall_at_k(ranks: np.ndarray, k: int) -> float:
    if ranks.size == 0:
        return 0.0
    return float(np.mean((ranks >= 1) & (ranks <= k)))


def mrr_at_10(ranks: np.ndarray) -> float:
    if ranks.size == 0:
        return 0.0
    contrib = np.where((ranks >= 1) & (ranks <= 10), 1.0 / np.maximum(ranks, 1), 0.0)
    return float(np.mean(contrib))


def compute_metric_set(ranks: np.ndarray) -> Dict[str, float]:
    return {
        "recall_at_1": recall_at_k(ranks, 1),
        "recall_at_3": recall_at_k(ranks, 3),
        "recall_at_5": recall_at_k(ranks, 5),
        "mrr_at_10": mrr_at_10(ranks),
    }


def percentile_ci(samples: np.ndarray) -> Dict[str, float]:
    return {
        "mean": float(np.mean(samples)),
        "ci_lo_2_5": float(np.percentile(samples, 2.5)),
        "ci_hi_97_5": float(np.percentile(samples, 97.5)),
    }


def bootstrap_run(
    plain_arr: np.ndarray, enh_arr: np.ndarray, n_draws: int, seed: int
) -> Dict[str, Any]:
    n = plain_arr.shape[0]
    if n == 0:
        raise RuntimeError("No queries available for bootstrap.")
    if enh_arr.shape[0] != n:
        raise RuntimeError("Plain/Enhanced rank arrays must have identical length.")

    rng = np.random.default_rng(seed)
    metrics_plain = {k: np.zeros(n_draws, dtype=np.float64) for k in ("recall_at_1", "recall_at_3", "recall_at_5", "mrr_at_10")}
    metrics_enhanced = {k: np.zeros(n_draws, dtype=np.float64) for k in ("recall_at_1", "recall_at_3", "recall_at_5", "mrr_at_10")}
    metrics_delta = {k: np.zeros(n_draws, dtype=np.float64) for k in ("recall_at_1", "recall_at_3", "recall_at_5", "mrr_at_10")}

    for d in range(n_draws):
        idx = rng.integers(low=0, high=n, size=n)
        p_sample = plain_arr[idx]
        e_sample = enh_arr[idx]
        p_metrics = compute_metric_set(p_sample)
        e_metrics = compute_metric_set(e_sample)
        for k in metrics_plain:
            metrics_plain[k][d] = p_metrics[k]
            metrics_enhanced[k][d] = e_metrics[k]
            metrics_delta[k][d] = e_metrics[k] - p_metrics[k]

    return {
        "plain": {k: percentile_ci(v) for k, v in metrics_plain.items()},
        "enhanced": {k: percentile_ci(v) for k, v in metrics_enhanced.items()},
        "delta": {k: percentile_ci(v) for k, v in metrics_delta.items()},
    }


def run() -> Dict[str, Any]:
    if not DEFAULT_INDEX_PATH.exists():
        raise RuntimeError(
            f"KOSHA RAG index not found at {DEFAULT_INDEX_PATH}. "
            "Build it with: python -m src.rag.local_kosha_rag build"
        )

    conn = connect_db(DEFAULT_INDEX_PATH)
    try:
        query_records, plain_ranks, enhanced_ranks = collect_per_query_ranks(conn)
    finally:
        conn.close()

    plain_arr = metric_array(plain_ranks)
    enh_arr = metric_array(enhanced_ranks)
    point_plain = compute_metric_set(plain_arr)
    point_enhanced = compute_metric_set(enh_arr)
    point_delta = {k: point_enhanced[k] - point_plain[k] for k in point_plain}

    boot = bootstrap_run(plain_arr, enh_arr, BOOTSTRAP_DRAWS, SEED)

    return {
        "dataset": QUERY_DATASET.relative_to(ROOT).as_posix(),
        "query_count": int(plain_arr.shape[0]),
        "bootstrap_draws": BOOTSTRAP_DRAWS,
        "seed": SEED,
        "point_estimates": {
            "plain": point_plain,
            "enhanced": point_enhanced,
            "delta": point_delta,
        },
        "bootstrap_ci": boot,
        "per_query_records": query_records,
    }


def write_reports(report: Dict[str, Any]) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# KOSHA RAG Bootstrap 95% CI Report",
        "",
        f"- Dataset: `{report['dataset']}`",
        f"- Queries: {report['query_count']}",
        f"- Bootstrap draws: {report['bootstrap_draws']}",
        f"- Seed: {report['seed']}",
        "",
        "## Point Estimates (deterministic, full sample)",
        "",
        "| Metric | Plain | Enhanced | Delta (E - P) |",
        "|---|---:|---:|---:|",
    ]
    pe = report["point_estimates"]
    for k in ("recall_at_1", "recall_at_3", "recall_at_5", "mrr_at_10"):
        lines.append(f"| {k} | {pe['plain'][k]:.4f} | {pe['enhanced'][k]:.4f} | {pe['delta'][k]:+.4f} |")

    lines.extend(
        [
            "",
            "## Bootstrap 95% CI (percentile method)",
            "",
            "### Plain mode",
            "",
            "| Metric | Mean | 2.5% | 97.5% |",
            "|---|---:|---:|---:|",
        ]
    )
    for k in ("recall_at_1", "recall_at_3", "recall_at_5", "mrr_at_10"):
        v = report["bootstrap_ci"]["plain"][k]
        lines.append(f"| {k} | {v['mean']:.4f} | {v['ci_lo_2_5']:.4f} | {v['ci_hi_97_5']:.4f} |")
    lines.extend(
        [
            "",
            "### Enhanced mode",
            "",
            "| Metric | Mean | 2.5% | 97.5% |",
            "|---|---:|---:|---:|",
        ]
    )
    for k in ("recall_at_1", "recall_at_3", "recall_at_5", "mrr_at_10"):
        v = report["bootstrap_ci"]["enhanced"][k]
        lines.append(f"| {k} | {v['mean']:.4f} | {v['ci_lo_2_5']:.4f} | {v['ci_hi_97_5']:.4f} |")
    lines.extend(
        [
            "",
            "### Paired difference (Enhanced - Plain)",
            "",
            "_This is the most meaningful CI for the manuscript improvement claim:_",
            "_a CI strictly above zero supports the Enhanced-mode advantage._",
            "",
            "| Metric | Mean | 2.5% | 97.5% | CI excludes 0? |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for k in ("recall_at_1", "recall_at_3", "recall_at_5", "mrr_at_10"):
        v = report["bootstrap_ci"]["delta"][k]
        excludes_zero = "yes" if (v["ci_lo_2_5"] > 0 or v["ci_hi_97_5"] < 0) else "no"
        lines.append(
            f"| {k} | {v['mean']:+.4f} | {v['ci_lo_2_5']:+.4f} | {v['ci_hi_97_5']:+.4f} | {excludes_zero} |"
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
