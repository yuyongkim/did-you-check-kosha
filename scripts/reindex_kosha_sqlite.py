#!/usr/bin/env python3
"""
Rebuild the local KOSHA RAG SQLite FTS5 index from the corrected `.utf8.` files.

Reads:
  datasets/kosha/normalized/law_articles.utf8.json   (output of reencode_kosha_corpus.py)
  datasets/kosha_guide/normalized/guide_chunks.jsonl.gz   (existing, already UTF-8)

Writes:
  datasets/kosha_rag/kosha_local_rag.utf8.sqlite3   (NEW — original index untouched)
  outputs/kosha_reindex_report.md                    (totals + spot-check evidence)

Reuses `src.rag.local_kosha_rag.build_documents` and `upsert_documents` so the
schema stays identical to the production builder; the only change is the
input/output paths.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.rag.local_kosha_rag import (  # noqa: E402  (after sys.path tweak)
    build_documents,
    init_schema,
    upsert_documents,
)

DEFAULT_LAW_UTF8 = REPO_ROOT / "datasets" / "kosha" / "normalized" / "law_articles.utf8.json"
DEFAULT_GUIDE_CHUNKS = REPO_ROOT / "datasets" / "kosha_guide" / "normalized" / "guide_chunks.jsonl.gz"
DEFAULT_INDEX_PATH = REPO_ROOT / "datasets" / "kosha_rag" / "kosha_local_rag.utf8.sqlite3"
DEFAULT_REPORT_PATH = REPO_ROOT / "outputs" / "kosha_reindex_report.md"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--law-articles", default=str(DEFAULT_LAW_UTF8))
    p.add_argument("--guide-chunks", default=str(DEFAULT_GUIDE_CHUNKS))
    p.add_argument("--index-path", default=str(DEFAULT_INDEX_PATH))
    p.add_argument("--report-path", default=str(DEFAULT_REPORT_PATH))
    return p.parse_args(argv)


def spot_check(conn: sqlite3.Connection) -> Dict[str, Any]:
    """Confirm Article 256 is in the index and FTS finds a Korean query for it."""
    out: Dict[str, Any] = {}
    target_id = "law:KOSHA04_002000002000004000000000256000"
    row = conn.execute(
        "SELECT id, title, content FROM documents WHERE id = ?", (target_id,)
    ).fetchone()
    if row is None:
        out["article_256_present"] = False
        out["fts_finds_부식"] = False
        return out
    title = str(row["title"])
    content = str(row["content"])
    out["article_256_present"] = True
    out["article_256_title"] = title
    out["article_256_title_ok"] = "제256조" in title and "부식" in title
    out["article_256_content_len"] = len(content)
    out["article_256_content_ok"] = (
        "사업주는" in content and "부식" in content and "도장" in content
    )

    # FTS query
    hits = conn.execute(
        """
        SELECT documents_fts.id, bm25(documents_fts) AS rank
        FROM documents_fts
        WHERE documents_fts MATCH ?
        ORDER BY rank
        LIMIT 5
        """,
        ('"부식" AND "방지"',),
    ).fetchall()
    out["fts_부식_방지_top5_ids"] = [str(h["id"]) for h in hits]
    out["fts_finds_article_256"] = any(str(h["id"]) == target_id for h in hits)

    # Total documents and FTS rows
    out["total_documents"] = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    out["total_fts_rows"] = conn.execute("SELECT COUNT(*) FROM documents_fts").fetchone()[0]
    by_source = conn.execute(
        "SELECT source_type, COUNT(*) AS n FROM documents GROUP BY source_type ORDER BY source_type"
    ).fetchall()
    out["by_source_type"] = {str(r["source_type"]): int(r["n"]) for r in by_source}
    return out


def write_report(
    index_path: Path,
    law_articles_path: Path,
    guide_chunks_path: Path,
    docs_count: int,
    spot: Dict[str, Any],
    report_path: Path,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    L: List[str] = []
    L.append("# KOSHA Local RAG SQLite Reindex Report\n\n")
    L.append("Run by `scripts/reindex_kosha_sqlite.py`. Builds a fresh FTS5 index at\n")
    L.append("a *new* path so the original `kosha_local_rag.sqlite3` is preserved.\n\n")

    L.append("## Inputs\n")
    L.append(f"- law articles (UTF-8 corrected): `{law_articles_path}`\n")
    L.append(f"- guide chunks: `{guide_chunks_path}`\n\n")

    L.append("## Output\n")
    L.append(f"- new index path: `{index_path}`\n")
    L.append(f"- documents inserted: **{docs_count}**\n\n")

    L.append("## Index totals\n")
    L.append(f"- documents table rows: **{spot.get('total_documents')}**\n")
    L.append(f"- documents_fts rows: **{spot.get('total_fts_rows')}**\n")
    by_src = spot.get("by_source_type", {})
    if by_src:
        L.append("- by source_type:\n")
        for k, v in by_src.items():
            L.append(f"    - `{k}`: {v}\n")
    L.append("\n")

    L.append("## Spot-check: Article 256 (`제256조 부식 방지`)\n")
    if spot.get("article_256_present"):
        L.append(f"- present in `documents`: **True**\n")
        L.append(f"- title: `{spot.get('article_256_title')}`\n")
        L.append(f"- title contains `제256조` AND `부식`: **{spot.get('article_256_title_ok')}**\n")
        L.append(f"- content length: {spot.get('article_256_content_len')} chars\n")
        L.append(f"- content contains `사업주는` AND `부식` AND `도장`: **{spot.get('article_256_content_ok')}**\n")
        L.append(f"- FTS query `\"부식\" AND \"방지\"` returns Article 256 in top-5: **{spot.get('fts_finds_article_256')}**\n")
        L.append(f"- top-5 FTS hit ids:\n")
        for h in spot.get("fts_부식_방지_top5_ids", []):
            L.append(f"    - `{h}`\n")
    else:
        L.append("- Article 256 NOT in index — investigate.\n")

    report_path.write_text("".join(L), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    law_path = Path(args.law_articles).resolve()
    guide_path = Path(args.guide_chunks).resolve()
    index_path = Path(args.index_path).resolve()
    report_path = Path(args.report_path).resolve()

    if not law_path.exists():
        raise RuntimeError(
            f"Corrected law articles not found at {law_path}. "
            "Run scripts/reencode_kosha_corpus.py first."
        )
    if not guide_path.exists():
        raise RuntimeError(f"Guide chunks not found at {guide_path}.")

    # Start fresh: delete the existing utf8 index if any.
    if index_path.exists():
        index_path.unlink()
    index_path.parent.mkdir(parents=True, exist_ok=True)

    docs = build_documents(guide_path, law_path)
    print(f"[OK] built {len(docs)} candidate documents")

    conn = sqlite3.connect(str(index_path))
    conn.row_factory = sqlite3.Row
    try:
        init_schema(conn)
        upsert_documents(conn, docs)
        spot = spot_check(conn)
    finally:
        conn.close()

    write_report(index_path, law_path, guide_path, len(docs), spot, report_path)
    print(f"[OK] index -> {index_path}")
    print(f"[OK] report -> {report_path}")
    print(json.dumps(spot, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
