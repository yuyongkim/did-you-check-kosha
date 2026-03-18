#!/usr/bin/env python3
"""Backfill law-article metadata into existing normalized KOSHA datasets."""

from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rag.law_article_metadata import build_law_article_metadata


LAW_ARTICLES_PATH = ROOT / "datasets" / "kosha" / "normalized" / "law_articles.json"
RETRIEVAL_CORPUS_PATH = ROOT / "datasets" / "kosha" / "normalized" / "retrieval_corpus.jsonl.gz"


def enrich_row(row: dict) -> dict:
    enriched = dict(row)
    metadata = build_law_article_metadata(
        raw_id=str(row.get("id") or ""),
        title=str(row.get("title") or ""),
        category=str(row.get("category") or ""),
        filepath=str(row.get("filepath") or ""),
    )
    enriched.update(
        {
            "law_name": metadata.get("law_name"),
            "article_label": metadata.get("article_label"),
            "article_number": metadata.get("article_number"),
            "query_seed": metadata.get("query_seed"),
            "direct_url": metadata.get("direct_url"),
            "search_url": metadata.get("search_url"),
            "resolved_url": metadata.get("resolved_url"),
        }
    )
    return enriched


def enrich_law_articles() -> int:
    rows = json.loads(LAW_ARTICLES_PATH.read_text(encoding="utf-8"))
    enriched = [enrich_row(row) for row in rows if isinstance(row, dict)]
    LAW_ARTICLES_PATH.write_text(json.dumps(enriched, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(enriched)


def enrich_retrieval_corpus() -> int:
    rows = []
    with gzip.open(RETRIEVAL_CORPUS_PATH, "rt", encoding="utf-8") as stream:
        for line in stream:
            item = json.loads(line)
            if not isinstance(item, dict):
                continue
            category = str(item.get("category") or "")
            if category in {"1", "2", "3", "4", "5", "8", "9", "11"}:
                item = enrich_row(item)
            rows.append(item)

    with gzip.open(RETRIEVAL_CORPUS_PATH, "wt", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False))
            stream.write("\n")
    return len(rows)


def main() -> int:
    law_count = enrich_law_articles()
    corpus_count = enrich_retrieval_corpus()
    print(f"ENRICHED_LAW_ARTICLES={law_count}")
    print(f"ENRICHED_RETRIEVAL_ROWS={corpus_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
