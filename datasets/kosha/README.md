# KOSHA Local Snapshot

## What This Folder Contains

This snapshot was generated from KOSHA smart-search API and stores:
- category-level raw records (`raw/category_*.jsonl.gz`)
- normalized guide/legal corpus (`normalized/*.json / *.jsonl.gz`)
- collection metadata (`manifest.json`)

## Current Snapshot Scope

- Categories collected: `1,2,3,4,5,6,7,8,9,11`
- Source API: `https://apis.data.go.kr/B552468/srch/smartSearch`
- Query mode: empty keyword (`searchValue=""`) with pagination

## Important: What Is NOT Included

- No binary PDF files are downloaded in this folder.
- This snapshot stores text fields and metadata from API responses.
- `filepath` values (when present) are portal detail links, not direct PDF URLs.

## Verified Current Status

- Total rows: `18,576`
- Rows with `filepath`: `6,405`
- Direct `.pdf` URLs in corpus: `0`
- `filepath` domain observed: `portal.kosha.or.kr`

## Regeneration

From repository root:

```powershell
python scripts/sync_kosha_corpus.py --categories 1,2,3,4,5,6,7,8,9,11 --force
```

Ingestion source project:
- `tools/kosha-ingestion/`

## If You Need Full PDF Archive

For Guide PDFs, use the dedicated KOSHA Guide API pipeline:

```powershell
python scripts/sync_kosha_guide_api.py --download
```

Guide API output location:
- `datasets/kosha_guide/guides.json`
- `datasets/kosha_guide/files/`
- `datasets/kosha_guide/manifest.json`

Notes:
- `datasets/kosha/` itself remains a smart-search text/metadata snapshot.
- Direct guide file URLs come from `koshaguide/getKoshaGuide` (`callApiId=1050`).

## Best-Effort Asset Pass

Attachment/PDF resolution pass is available:

```powershell
python scripts/sync_kosha_assets.py --max-items 300 --force
```

Results are stored in:
- `datasets/kosha/assets/`
- `datasets/kosha/assets_manifest.json`
