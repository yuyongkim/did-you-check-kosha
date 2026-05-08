# KOSHA Missing Law-Article Bodies — Refetch Report

Total empty-content rows identified: **12** (of 3,102 in `law_articles.json`)

- KOSHA service key available: **True**
- Rows patched into `law_articles.utf8.json`: **0**

## Summary

- Refetched OK with new body: **0**
- Refetched but source is truly empty (incl. repealed `삭제` articles): **0**
- Refetch failed (network / auth blocker): **12**
- Rows whose title contains `삭제` (repealed): **4** — for these an empty body is the *correct* state, not corruption.

## Per-id outcome

| # | doc_id | title | repealed | route | OK | new len | blocker |
|---|--------|-------|---------:|-------|----|--------:|---------|
| 1 | `KOSHA04_002000004000001000000000336000` | 제336조 제336조 |  | law_go_kr | N | 0 | KOSHA API: doc_id not found in 0 returned items \| law.go.kr: law.go.kr returned SPA shell (no article body in HTML); nee |
| 2 | `KOSHA04_002000004000001000000000337000` | 제337조 제337조 |  | law_go_kr | N | 0 | KOSHA API: doc_id not found in 0 returned items \| law.go.kr: law.go.kr returned SPA shell (no article body in HTML); nee |
| 3 | `KOSHA04_003000009000002000000000610000` | 제610조 제610조 |  | law_go_kr | N | 0 | KOSHA API: doc_id not found in 0 returned items \| law.go.kr: law.go.kr returned SPA shell (no article body in HTML); nee |
| 4 | `KOSHA04_003000010000004000000000645201733000` | 제645조 삭제 제645조 삭제 | Y | law_go_kr | N | 0 | KOSHA API: doc_id not found in 0 returned items \| law.go.kr: law.go.kr returned SPA shell (no article body in HTML); nee |
| 5 | `KOSHA04_00300001300000000000000067120191223000` | 제671조 삭제 제671조 삭제 | Y | law_go_kr | N | 0 | KOSHA API: doc_id not found in 0 returned items \| law.go.kr: law.go.kr returned SPA shell (no article body in HTML); nee |
| 6 | `KOSHA05_건설업 산업안전보건관리비 계상 및 사용기준000000002000000000000000000000005000` | 건설업 산업안전보건관리비 계상 및 사용기준 제5조 계상방법 및 계상시기 등 |  | kosha_api | N | 0 | KOSHA API: doc_id not found in 0 returned items |
| 7 | `KOSHA05_건설업 산업안전보건관리비 계상 및 사용기준000000002000000000000000000000006000` | 건설업 산업안전보건관리비 계상 및 사용기준 제6조 수급인등의 의무 |  | kosha_api | N | 0 | KOSHA API: doc_id not found in 0 returned items |
| 8 | `KOSHA05_건설업 산업안전보건관리비 계상 및 사용기준000000003000000000000000000000011000` | 건설업 산업안전보건관리비 계상 및 사용기준 제11조 기술지도 횟수 등 |  | kosha_api | N | 0 | KOSHA API: doc_id not found in 0 returned items |
| 9 | `KOSHA05_제1차 금속산업 안전작업지침000000001000000000000000000000003000` | 제1차 금속산업 안전작업지침 제3조 적용범위 |  | kosha_api | N | 0 | KOSHA API: doc_id not found in 0 returned items |
| 10 | `KOSHA05_추락재해방지표준안전작업지침000000003000001000000000000000014000` | 추락재해방지표준안전작업지침 제14조 구조 |  | kosha_api | N | 0 | KOSHA API: doc_id not found in 0 returned items |
| 11 | `KOSHA11_00000000000000000000000000622011316` | 제6조의2 삭제 제6조의2 삭제 | Y | kosha_api | N | 0 | KOSHA API: doc_id not found in 0 returned items |
| 12 | `KOSHA11_000000000000000000000000132011316000` | 제13조 삭제 제13조 삭제 | Y | law_go_kr | N | 0 | KOSHA API: doc_id not found in 0 returned items \| law.go.kr: law.go.kr returned SPA shell (no article body in HTML); nee |

## Author follow-up required

The following ids could not be refetched. Inspect each `direct_url`
manually on https://www.law.go.kr to confirm whether the source is
truly empty (repealed) or the body needs to be backfilled.

