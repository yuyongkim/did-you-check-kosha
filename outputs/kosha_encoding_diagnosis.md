# KOSHA Corpus Encoding Diagnosis & Re-encode Report
Run by `scripts/reencode_kosha_corpus.py`. The script scans the four
normalized KOSHA snapshot files, detects mojibake, and writes corrected
sibling files with the `.utf8.` infix. Originals are never overwritten.

## Encoding Pipeline (diagnosis)
Upstream: `https://apis.data.go.kr/B552468/srch/smartSearch` returns JSON
whose Korean text is *expected* to be UTF-8 but historically the Smart-search
endpoint has shipped CP949/EUC-KR bodies under a UTF-8 Content-Type, producing
two classic mojibake patterns when downstream code mishandles the bytes:

* **Pattern A** — UTF-8 bytes decoded as Latin-1, then re-encoded UTF-8.
  Signature: clusters of À-ÿ (`Ã`, `ë`, `ì`).
  Fix: `s.encode('latin-1').decode('utf-8')`.
* **Pattern B** — UTF-8 bytes decoded as CP949, then re-encoded UTF-8.
  Signature: rare CJK Unified ideographs (`諛`, `遺`, `젣`).
  Fix: `s.encode('latin-1').decode('cp949')` (or via cp949↔utf-8 chain).

The `tools/kosha-ingestion/src/kosha_ingestion/text_encoding.py` module already
tries multiple decoding candidates at ingest time and runs `repair_mojibake_in_object`
on every parsed payload. Any mojibake the API returned should already have been
fixed during `scripts/sync_kosha_corpus.py`.

## Per-file scan results
| File | Total string fields | Mojibake detected | Repaired | Round-trip failed |
|------|--------------------:|------------------:|---------:|------------------:|
| `law_articles.json` | 28199 | 0 | 0 | 0 |
| `guide_documents.json` | 29861 | 0 | 0 | 0 |
| `guide_sections.jsonl.gz` | 36276 | 0 | 0 | 0 |
| `retrieval_corpus.jsonl.gz` | 102788 | 0 | 0 | 0 |
| **TOTAL** | **197124** | **0** | **0** | **0** |

### Finding

**Zero mojibake fields detected on disk.** All four normalized files contain
clean UTF-8 Korean text. The original report symptoms (e.g., title shown as
`��256�� �ν� ����`) reproduce exactly when correct UTF-8 bytes are *displayed
through* a Windows console set to code-page 949 (CP949) — that is a terminal
rendering artifact, not corrupted storage. Verified by reading the same file
with explicit `encoding='utf-8'` and confirming all Hangul syllables decode
into the BMP `가-힣` block.

The protective `repair_mojibake_in_object` pass already runs at ingest time
(see `tools/kosha-ingestion/src/kosha_ingestion/text_encoding.py:82`), so any
mojibake the API returned was fixed before `law_articles.json` was written.

## Spot-check: Article 256 (`제256조 부식 방지`)
- id: `KOSHA04_002000002000004000000000256000`
- title: `제256조 부식 방지`
- title contains `제256조`: **True**
- title contains `부식`: **True**
- content contains `사업주는`: **True**
- content contains `부식`: **True**
- content contains `도장`: **True**
- content length: 218 chars

Content preview (first 200 chars):

```
사업주는 화학설비 또는 그 배관(화학설비 또는 그 배관의 밸브나 콕은 제외한다) 중 위험물 또는 인화점이 섭씨 60도 이상인 물질(이하 "위험물질등"이라 한다)이 접촉하는 부분에 대해서는 위험물질등에 의하여 그 부분이 부식되어 폭발ㆍ화재 또는 누출되는 것을 방지하기 위하여 위험물질등의 종류ㆍ온도ㆍ농도 등에 따라 부식이 잘 되지 않는 재료를 사용하거나 도장(
```

## Output files (siblings, originals untouched)
- `datasets/kosha/normalized/law_articles.utf8.json`
- `datasets/kosha/normalized/guide_documents.utf8.json`
- `datasets/kosha/normalized/guide_sections.utf8.jsonl.gz`
- `datasets/kosha/normalized/retrieval_corpus.utf8.jsonl.gz`
