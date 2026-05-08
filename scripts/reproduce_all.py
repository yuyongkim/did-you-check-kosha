#!/usr/bin/env python3
"""End-to-end reproducibility runner for the JLP revision artefact set.

Goal: a single command that regenerates every figure, table, and
`outputs/*.md` referenced in the manuscript from a clean repo state.

Order of operations is dependency-driven:
  1. Per-discipline runtime verification (220-case engine accuracy)
  2. Cross-discipline validator ablation
  3. Seven-pipeline benchmark
  4. RAG retrieval benchmark + ablation hits dump
  5. Layer ablation
  6. Negative-case RAG sanity
  7. Bootstrap CI on RAG retrieval
  8. Per-discipline accuracy breakdown (this revision)
  9. Recall@K extension (this revision)
  10. Pipeline latency (this revision)
  11. Retrieval failure inventory (this revision)
  12. Paper figures

KOSHA corpus rebuild scripts are intentionally NOT included: those need
network access and produce a ~200 MB SQLite. The pre-built index is
expected at `datasets/kosha_rag/kosha_local_rag.sqlite3`.

Outputs
-------
- Prints a per-step header + result, captures exit codes.
- Final manifest of every file in `outputs/` (size + mtime).
- Returns nonzero exit if ANY step failed.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = ROOT / "outputs"

# (script_path_relative_to_root, label)
STEPS: List[Tuple[str, str]] = [
    ("scripts/benchmark_all_runtime.py", "Runtime verification (220-case engine accuracy)"),
    ("scripts/benchmark_cross_discipline_ablation.py", "Cross-discipline validator ablation"),
    ("scripts/benchmark_seven_pipeline.py", "Seven-discipline pipeline benchmark"),
    ("scripts/benchmark_rag_retrieval.py", "KOSHA RAG retrieval benchmark"),
    ("scripts/dump_ablation_hits.py", "Ablation hits dump"),
    ("scripts/run_layer_ablation.py", "Layer ablation"),
    ("scripts/run_negative_case_rag.py", "Negative-case RAG"),
    ("scripts/bootstrap_ci_rag.py", "Bootstrap CI on RAG"),
    ("scripts/dump_per_discipline_accuracy.py", "Per-discipline accuracy breakdown (NEW)"),
    ("scripts/extend_recall_at_k.py", "Recall@K extension (NEW)"),
    ("scripts/measure_pipeline_latency.py", "Pipeline latency (NEW)"),
    ("scripts/dump_retrieval_failures.py", "Retrieval failure inventory (NEW)"),
    ("scripts/generate_paper_figures.py", "Generate paper figures"),
]

SKIPPED_NETWORK_SCRIPTS = [
    "scripts/sync_kosha_corpus.py",
    "scripts/sync_kosha_assets.py",
    "scripts/sync_kosha_guide_api.py",
    "scripts/parse_kosha_guide_pdfs.py",
    "scripts/refetch_missing_law_articles.py",
    "scripts/resolve_law_article_direct_urls.py",
    "scripts/reencode_kosha_corpus.py",
    "scripts/reindex_kosha_sqlite.py",
    "scripts/enrich_law_article_metadata.py",
]


def banner(text: str) -> None:
    bar = "=" * max(60, len(text) + 4)
    print(bar)
    print(f"  {text}")
    print(bar, flush=True)


def run_step(script_rel: str, label: str) -> Tuple[int, float]:
    script_path = ROOT / script_rel
    if not script_path.exists():
        print(f"[SKIP] script not found: {script_rel}")
        return 127, 0.0
    banner(f"RUN: {label}  ({script_rel})")
    t0 = time.perf_counter()
    env = os.environ.copy()
    # Force UTF-8 so Korean characters print on Windows consoles.
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    proc = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(ROOT),
        env=env,
        capture_output=False,
        check=False,
    )
    elapsed = time.perf_counter() - t0
    code = proc.returncode
    status = "OK" if code == 0 else "FAIL"
    print(f"[{status}] {script_rel}  exit={code}  elapsed={elapsed:.2f}s\n", flush=True)
    return code, elapsed


def emit_outputs_manifest() -> None:
    banner("OUTPUTS MANIFEST")
    if not OUTPUTS_DIR.exists():
        print("(outputs/ does not exist)")
        return
    rows = []
    for entry in sorted(OUTPUTS_DIR.iterdir()):
        try:
            st = entry.stat()
        except OSError:
            continue
        if entry.is_file():
            rows.append((entry.name, st.st_size, st.st_mtime))
    print(f"{'name':<60} {'size_bytes':>12} {'mtime':>20}")
    print("-" * 96)
    for name, size, mtime in rows:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime))
        print(f"{name:<60} {size:>12} {ts:>20}")
    print(f"\nTotal files: {len(rows)}")


def main() -> int:
    banner("REPRODUCE-ALL: JLP-D-26-00414 revision artefacts")
    print(f"Repo root: {ROOT}")
    print(f"Python:    {sys.version.split()[0]}")
    print(f"Steps:     {len(STEPS)}")
    print(f"Skipped (network/corpus rebuild, intentional): {SKIPPED_NETWORK_SCRIPTS}\n", flush=True)

    failures: List[Tuple[str, int]] = []
    successes = 0
    timings: List[Tuple[str, float, int]] = []

    for script_rel, label in STEPS:
        code, elapsed = run_step(script_rel, label)
        timings.append((script_rel, elapsed, code))
        if code == 0:
            successes += 1
        else:
            failures.append((script_rel, code))

    emit_outputs_manifest()

    banner(f"SUMMARY: OK {successes}/{len(STEPS)} scripts completed")
    print(f"{'script':<60} {'elapsed_s':>10} {'exit':>6}")
    print("-" * 80)
    for script_rel, elapsed, code in timings:
        print(f"{script_rel:<60} {elapsed:>10.2f} {code:>6}")

    if failures:
        print("\nFAILURES:")
        for script_rel, code in failures:
            print(f"  - {script_rel} (exit={code})")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
