# KOSHA Data Sync Guide (EN)

## Purpose

Download full KOSHA smart-search records (selected categories) into local files so regulatory mapping can be audited and refreshed without relying only on live query-time calls.

## Script

`scripts/sync_kosha_corpus.py`

Implementation project:
- `tools/kosha-ingestion/`

## Default coverage

- Categories: `1,2,3,4,5,7,8,9,11`
- Meaning:
  - `7`: KOSHA guide records
  - `1,2,3,4,5,8,9,11`: legal and related rule categories

## Run

```powershell
python scripts/sync_kosha_corpus.py --force
```

Optional:

```powershell
python scripts/sync_kosha_corpus.py --categories 1,2,3,4,5,6,7,8,9,11 --num-rows 200 --force
```

Use category `6` only when you also need broad media/archive records (much larger and less calculation-specific).

## Service key resolution order

1. `--service-key`
2. Environment variables:
   - `KOSHA_API_KEY_ENCODING`
   - `KOSHA_API_KEY_ENCODED`
   - `KOSHA_SERVICE_KEY`
   - `KOSHA_API_KEY`
   - `KOSHA_API_KEY_DECODING`
   - `KOSHA_API_KEY_DECODED`
3. `frontend/.env.local` with same keys

## Output

- Raw pages (per category): `datasets/kosha/raw/category_<n>.jsonl.gz`
- Normalized:
  - `datasets/kosha/normalized/guide_documents.json`
  - `datasets/kosha/normalized/law_articles.json`
  - `datasets/kosha/normalized/guide_sections.jsonl.gz`
  - `datasets/kosha/normalized/retrieval_corpus.jsonl.gz`
- Manifest:
  - `datasets/kosha/manifest.json`

## Latest snapshot result (generated on 2026-03-01 KST)

- Rows (all categories): `12,171`
- Guide section rows: `9,069`
- Guide documents (grouped): `1,327`
- Law articles: `3,102`

## Notes

- This sync is snapshot-style, not an automatic scheduler.
- Re-run periodically or attach to CI/cron if policy requires freshness.
- Keep legal/compliance interpretation in human review loop.

## Attachment/PDF Pass (Best Effort)

```powershell
python scripts/sync_kosha_assets.py --max-items 300 --force
```

Output:
- `datasets/kosha/assets/`
- `datasets/kosha/assets_manifest.json`

## Direct Guide API PDF Sync (Recommended for Full Guide Files)

`koshaguide/getKoshaGuide` returns direct `fileDownloadUrl` values.

```powershell
python scripts/sync_kosha_guide_api.py --download
```

Output:
- `datasets/kosha_guide/guides.json`
- `datasets/kosha_guide/files/`
- `datasets/kosha_guide/manifest.json`
- `datasets/kosha_guide/downloads_manifest.json`

## Parse Guide PDFs into Text Dataset

```powershell
python scripts/parse_kosha_guide_pdfs.py
```

Output:
- `datasets/kosha_guide/normalized/guide_pages.jsonl.gz`
- `datasets/kosha_guide/normalized/guide_documents_text.json`
- `datasets/kosha_guide/normalized/guide_chunks.jsonl.gz`
- `datasets/kosha_guide/normalized/manifest_text.json`
