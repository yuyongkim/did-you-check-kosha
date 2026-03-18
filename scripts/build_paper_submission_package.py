#!/usr/bin/env python3
"""Build a compact paper-submission source package."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAMP = datetime.now().strftime("%Y%m%d")
PACKAGE_DIR = ROOT / "exports" / f"paper_submission_source_pack_{STAMP}"
ZIP_BASE = ROOT / "exports" / f"paper_submission_source_pack_{STAMP}"

INCLUDE_PATHS = [
    Path("README.md"),
    Path("requirements.txt"),
    Path("submission_requirements.txt"),
    Path("config/cross_discipline_threshold_profiles.json"),
    Path("config/law_article_link_overrides.json"),
    Path("docs/publication/PAPER_EN_v2.md"),
    Path("docs/publication/CODE_MAP.md"),
    Path("docs/publication/README.md"),
    Path("docs/publication/SUBMISSION_CHECKLIST.md"),
    Path("docs/publication/SUBMISSION_TABLES.md"),
    Path("docs/publication/REVIEWER_RESPONSE_QA.md"),
    Path("outputs/verification_report_runtime.json"),
    Path("outputs/verification_report_runtime.md"),
    Path("outputs/seven_pipeline_report.json"),
    Path("outputs/seven_pipeline_report.md"),
    Path("outputs/cross_discipline_report.json"),
    Path("outputs/cross_discipline_report.md"),
    Path("outputs/cross_discipline_tuning_report.json"),
    Path("outputs/cross_discipline_tuning_report.md"),
    Path("outputs/cross_discipline_ablation_report.json"),
    Path("outputs/cross_discipline_ablation_report.md"),
    Path("outputs/rag_retrieval_report.json"),
    Path("outputs/rag_retrieval_report.md"),
    Path("scripts/sync_kosha_corpus.py"),
    Path("scripts/sync_kosha_guide_api.py"),
    Path("scripts/parse_kosha_guide_pdfs.py"),
    Path("scripts/kosha_rag_local.py"),
    Path("scripts/benchmark_all_runtime.py"),
    Path("scripts/benchmark_seven_pipeline.py"),
    Path("scripts/benchmark_cross_discipline.py"),
    Path("scripts/benchmark_cross_discipline_ablation.py"),
    Path("scripts/benchmark_rag_retrieval.py"),
    Path("scripts/enrich_law_article_metadata.py"),
    Path("scripts/resolve_law_article_direct_urls.py"),
    Path("scripts/build_paper_submission_package.py"),
    Path("src"),
    Path("tests/test_rag_synonyms.py"),
    Path("tests/test_maker.py"),
    Path("tests/test_reverse_check.py"),
    Path("tests/test_piping_service.py"),
    Path("tests/test_vessel_service.py"),
    Path("tests/test_rotating_service.py"),
    Path("tests/test_electrical_service.py"),
    Path("tests/test_instrumentation_service.py"),
    Path("tests/test_steel_service.py"),
    Path("tests/test_civil_service.py"),
    Path("tests/test_cross_discipline_thresholds.py"),
    Path("tests/test_cross_discipline_pipeline.py"),
    Path("tests/test_seven_discipline_pipeline.py"),
    Path("tests/test_e2e_pipeline.py"),
    Path("tools/kosha-ingestion/src/kosha_ingestion"),
    Path("datasets/golden_standards"),
    Path("datasets/kosha/normalized/law_articles.json"),
    Path("datasets/kosha/normalized/retrieval_corpus.jsonl.gz"),
    Path("datasets/kosha_guide/normalized/guide_chunks.jsonl.gz"),
    Path("datasets/kosha_rag/rag_eval_queries.json"),
]


def copy_path(relative_path: Path) -> None:
    source = ROOT / relative_path
    if not source.exists():
        return
    target = PACKAGE_DIR / relative_path
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def write_readme() -> None:
    readme_path = PACKAGE_DIR / "README_SUBMISSION_PACKAGE.md"
    lines = [
        "# Submission Source Package",
        "",
        "This package is curated for paper submission and review.",
        "",
        "Included:",
        "- manuscript and code map",
        "- compact submission checklist",
        "- insertable submission tables and reviewer-response Q&A",
        "- backend source code under `src/`",
        "- benchmark and reproduction scripts",
        "- selected regression / runtime tests",
        "- minimal datasets required to rebuild the local legal / RAG evaluation context",
        "- KOSHA ingestion source tree under `tools/kosha-ingestion/src/kosha_ingestion/`",
        "- generated benchmark reports cited in the paper",
        "",
        "Excluded on purpose:",
        "- frontend",
        "- logs and local caches",
        "- broad development tooling bundles",
        "- the prebuilt SQLite RAG index",
        "",
        "Main rebuild commands:",
        "```powershell",
        "python -m pip install -r submission_requirements.txt",
        "python scripts/enrich_law_article_metadata.py",
        "python scripts/resolve_law_article_direct_urls.py",
        "python scripts/kosha_rag_local.py build --rebuild",
        "python scripts/benchmark_all_runtime.py",
        "python scripts/benchmark_cross_discipline_ablation.py",
        "python scripts/benchmark_rag_retrieval.py",
        "```",
    ]
    readme_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)

    for relative_path in INCLUDE_PATHS:
        copy_path(relative_path)

    write_readme()

    shutil.make_archive(str(ZIP_BASE), "zip", root_dir=PACKAGE_DIR)
    print(f"[DONE] paper submission source package built at {PACKAGE_DIR}")
    print(f"[ZIP] {ZIP_BASE}.zip")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
