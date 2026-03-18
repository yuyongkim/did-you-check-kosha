#!/usr/bin/env python3
"""Build a repo-layout publication bundle for manuscript submission and review."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLE_DIR = ROOT / "publication_bundle"
BUNDLE_ZIP = ROOT / "publication_bundle" / "publication_bundle.zip"

INCLUDE_PATHS = [
    Path("README.md"),
    Path("requirements.txt"),
    Path("config"),
    Path("docs/publication"),
    Path("docs/KOSHA_DATA_SYNC_GUIDE.md"),
    Path("outputs"),
    Path("scripts"),
    Path("src"),
    Path("tests"),
    Path("tools/kosha-ingestion"),
    Path("datasets/golden_standards"),
    Path("datasets/kosha/normalized/law_articles.json"),
    Path("datasets/kosha_rag/kosha_local_rag.sqlite3"),
    Path("datasets/kosha_guide/normalized/guide_chunks.jsonl.gz"),
]


def copy_path(relative_path: Path) -> None:
    source = ROOT / relative_path
    target = BUNDLE_DIR / relative_path
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def write_manifest() -> None:
    readme = BUNDLE_DIR / "README_PUBLICATION_BUNDLE.md"
    lines = [
        "# Publication Bundle",
        "",
        "This bundle preserves repository-relative paths so manuscript references such as `src/...` and `scripts/...` remain valid.",
        "",
        "Included high-level contents:",
        "- `src/` full source tree",
        "- `scripts/` benchmark, sync, and bundle scripts",
        "- `tests/` targeted verification tests",
        "- `docs/publication/` manuscript and code map",
        "- `datasets/` subset required for golden benchmarks and local KOSHA RAG",
        "- `outputs/` generated benchmark and verification reports",
        "",
        "Build command:",
        "```powershell",
        "python scripts/build_publication_bundle.py",
        "```",
    ]
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if BUNDLE_DIR.exists():
        shutil.rmtree(BUNDLE_DIR)
    BUNDLE_DIR.mkdir(parents=True, exist_ok=True)

    for relative_path in INCLUDE_PATHS:
        copy_path(relative_path)

    write_manifest()

    archive_base = BUNDLE_DIR / "publication_bundle"
    shutil.make_archive(str(archive_base), "zip", root_dir=BUNDLE_DIR)
    print(f"[DONE] publication bundle rebuilt at {BUNDLE_DIR}")
    print(f"[ZIP] {BUNDLE_ZIP}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
