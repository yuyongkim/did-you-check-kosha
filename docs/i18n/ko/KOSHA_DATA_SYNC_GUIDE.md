# KOSHA 데이터 동기화 가이드 (KO)

## 목적

규제 매핑에 사용하는 KOSHA 데이터를 실시간 조회만 의존하지 않고, 로컬 스냅샷으로 보관/검증할 수 있도록 전체 데이터를 수집합니다.

## 스크립트

`scripts/sync_kosha_corpus.py`

구현 프로젝트:
- `tools/kosha-ingestion/`

## 기본 수집 범위

- 카테고리: `1,2,3,4,5,7,8,9,11`
- 의미:
  - `7`: KOSHA GUIDE
  - `1,2,3,4,5,8,9,11`: 법령/시행령/규칙/고시/중처법 등 관련 카테고리

## 실행 방법

```powershell
python scripts/sync_kosha_corpus.py --force
```

옵션 예시:

```powershell
python scripts/sync_kosha_corpus.py --categories 1,2,3,4,5,6,7,8,9,11 --num-rows 200 --force
```

`6` 카테고리는 콘텐츠/아카이브성 자료가 매우 많으므로, 필요할 때만 포함하는 것을 권장합니다.

## 인증키 로딩 우선순위

1. `--service-key`
2. 환경변수:
   - `KOSHA_API_KEY_ENCODING`
   - `KOSHA_API_KEY_ENCODED`
   - `KOSHA_SERVICE_KEY`
   - `KOSHA_API_KEY`
   - `KOSHA_API_KEY_DECODING`
   - `KOSHA_API_KEY_DECODED`
3. `frontend/.env.local` (동일 키명)

## 생성 파일

- 카테고리별 Raw:
  - `datasets/kosha/raw/category_<n>.jsonl.gz`
- 정규화 데이터:
  - `datasets/kosha/normalized/guide_documents.json`
  - `datasets/kosha/normalized/law_articles.json`
  - `datasets/kosha/normalized/guide_sections.jsonl.gz`
  - `datasets/kosha/normalized/retrieval_corpus.jsonl.gz`
- 수집 메타:
  - `datasets/kosha/manifest.json`

## 최신 스냅샷 결과 (2026-03-01 KST 생성)

- 전체 행 수: `12,171`
- GUIDE 섹션 행 수: `9,069`
- GUIDE 문서(그룹화): `1,327`
- 법령 조항: `3,102`

## 참고

- 현재는 배치 스냅샷 방식이며 자동 스케줄러는 포함하지 않았습니다.
- 데이터 최신성 정책이 필요하면 주기 실행(CI/cron)으로 확장하면 됩니다.
- 법령 해석/최종 준수 판정은 반드시 전문가 검토를 포함해야 합니다.

## 첨부/PDF 다운로드 패스 (Best Effort)

```powershell
python scripts/sync_kosha_assets.py --max-items 300 --force
```

생성 결과:
- `datasets/kosha/assets/`
- `datasets/kosha/assets_manifest.json`

## KOSHA Guide API 직접 PDF 동기화 (권장)

`koshaguide/getKoshaGuide` API는 `fileDownloadUrl`을 직접 반환합니다.

```powershell
python scripts/sync_kosha_guide_api.py --download
```

생성 결과:
- `datasets/kosha_guide/guides.json`
- `datasets/kosha_guide/files/`
- `datasets/kosha_guide/manifest.json`
- `datasets/kosha_guide/downloads_manifest.json`

## Guide PDF 텍스트 파싱 데이터셋 생성

```powershell
python scripts/parse_kosha_guide_pdfs.py
```

생성 결과:
- `datasets/kosha_guide/normalized/guide_pages.jsonl.gz`
- `datasets/kosha_guide/normalized/guide_documents_text.json`
- `datasets/kosha_guide/normalized/guide_chunks.jsonl.gz`
- `datasets/kosha_guide/normalized/manifest_text.json`
