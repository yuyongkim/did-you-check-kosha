# KOSHA Ingestion Project

This folder is a dedicated ingestion project for KOSHA data collection and asset resolution.

## Scope

- Corpus sync from KOSHA smart-search API
- Local normalization for guide/legal retrieval
- Best-effort attachment/PDF download pass from portal-linked records
- Direct KOSHA Guide API sync with file URL index and PDF download
- KOSHA Guide PDF text parsing (page/doc/chunk datasets)

## Layout

- `src/kosha_ingestion/sync_corpus.py`: category crawl + normalization
- `src/kosha_ingestion/download_assets.py`: attachment/PDF resolution and download
- `src/kosha_ingestion/sync_kosha_guide_api.py`: KOSHA Guide API index + direct PDF sync
- `src/kosha_ingestion/parse_kosha_guide_pdfs.py`: parse guide PDFs to normalized text files
- `src/kosha_ingestion/text_encoding.py`: robust JSON decoding + mojibake repair helpers
- `src/kosha_ingestion/validate_encoding.py`: snapshot encoding validator/repair tool
- `bin/sync_corpus.py`: local CLI entry
- `bin/download_assets.py`: local CLI entry
- `bin/sync_kosha_guide_api.py`: local CLI entry
- `bin/parse_kosha_guide_pdfs.py`: local CLI entry
- `bin/validate_encoding.py`: local CLI entry

## Run (from repo root)

```powershell
python scripts/sync_kosha_corpus.py --force
python scripts/sync_kosha_assets.py --max-items 300 --force
python scripts/sync_kosha_guide_api.py --download
python scripts/parse_kosha_guide_pdfs.py
```

## Run (inside this project)

```powershell
python tools/kosha-ingestion/bin/sync_corpus.py --force
python tools/kosha-ingestion/bin/download_assets.py --max-items 300 --force
python tools/kosha-ingestion/bin/sync_kosha_guide_api.py --download
python tools/kosha-ingestion/bin/parse_kosha_guide_pdfs.py
python tools/kosha-ingestion/bin/validate_encoding.py
python tools/kosha-ingestion/bin/validate_encoding.py --repair
```

## Notes

- Asset download is best-effort because portal attachment APIs are not fully documented.
- `assets_manifest.json` records unresolved items and download errors for audit/retry.
- `sync_kosha_guide_api.py` uses `callApiId=1050` and receives `fileDownloadUrl` directly from official Guide API.
- `parse_kosha_guide_pdfs.py` writes:
  - `datasets/kosha_guide/normalized/guide_pages.jsonl.gz`
  - `datasets/kosha_guide/normalized/guide_documents_text.json`
  - `datasets/kosha_guide/normalized/guide_chunks.jsonl.gz`
