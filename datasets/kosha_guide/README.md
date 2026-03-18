# KOSHA Guide API Snapshot

This folder stores direct KOSHA Guide API outputs (`getKoshaGuide`, `callApiId=1050`).

## Contents

- `guides.json`: Guide metadata index
- `files/`: Downloaded guide files (typically PDF)
- `normalized/guide_pages.jsonl.gz`: page-level extracted text
- `normalized/guide_documents_text.json`: document-level full text
- `normalized/guide_chunks.jsonl.gz`: retrieval chunks
- `normalized/manifest_text.json`: parse manifest
- `manifest.json`: Sync summary
- `downloads_manifest.json`: Per-file download status

## Generate

```powershell
python scripts/sync_kosha_guide_api.py --download
```

Index only (no files):

```powershell
python scripts/sync_kosha_guide_api.py
```

Parse downloaded PDFs into text datasets:

```powershell
python scripts/parse_kosha_guide_pdfs.py
```
