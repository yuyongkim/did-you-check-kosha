# KOSHA Local RAG SQLite Reindex Report

Run by `scripts/reindex_kosha_sqlite.py`. Builds a fresh FTS5 index at
a *new* path so the original `kosha_local_rag.sqlite3` is preserved.

## Inputs
- law articles (UTF-8 corrected): `C:\Users\USER\Desktop\EPC engineering\datasets\kosha\normalized\law_articles.utf8.json`
- guide chunks: `C:\Users\USER\Desktop\EPC engineering\datasets\kosha_guide\normalized\guide_chunks.jsonl.gz`

## Output
- new index path: `C:\Users\USER\Desktop\EPC engineering\datasets\kosha_rag\kosha_local_rag.utf8.sqlite3`
- documents inserted: **16174**

## Index totals
- documents table rows: **16174**
- documents_fts rows: **16174**
- by source_type:
    - `guide_chunk`: 13084
    - `law_article`: 3090

## Spot-check: Article 256 (`제256조 부식 방지`)
- present in `documents`: **True**
- title: `제256조 부식 방지`
- title contains `제256조` AND `부식`: **True**
- content length: 218 chars
- content contains `사업주는` AND `부식` AND `도장`: **True**
- FTS query `"부식" AND "방지"` returns Article 256 in top-5: **True**
- top-5 FTS hit ids:
    - `law:KOSHA04_002000002000004000000000256000`
    - `guide:A-141-2018#6`
    - `guide:B-M-18-2026#5`
    - `guide:C-113-2020#17`
    - `guide:B-M-23-2026#5`
