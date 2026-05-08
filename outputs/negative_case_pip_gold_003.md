# Negative-Case RAG Report: PIP-GOLD-003

- Dataset: `datasets/golden_standards/piping_golden_dataset_v1.json`
- Expected red flags (from dataset): []
- Expected warnings (from dataset): ['PHY.UNREALISTIC_REMAINING_LIFE']

## Headline

**WARNING** -- at least one query variant returned a *mandatory* (law_article) hit in its top-10. The negative-case argument in manuscript §6.7 is **weakened** and should be revisited.

Negative-case argument is WEAKENED if any_mandatory_hit_across_variants is True, because a mandatory law-article hit means the system would surface a regulatory flag for a benign case. False means no mandatory law-article hit appeared in either variant's top-10 -- consistent with the manuscript's negative-case claim.

## Variant: generic_piping_integrity

- Query: `piping life management corrosion inspection SA-312 TP316 general service NPS 4.0 weld erw 배관 잔여수명 부식 검사주기`
- Discipline filter: `piping`
- Rationale: Neutral query for a generic piping integrity assessment derived strictly from PIP-GOLD-003 inputs (material, NPS, weld_type, service_type='general'). No chloride or sour-service terms because the case sets neither.
- Hits: 10 (mandatory=0, guidance=10)
- Any mandatory in top-10: False
- First mandatory rank: None

| Rank | Class | reference_code | source_type | score | title |
|---:|---|---|---|---:|---|
| 1 | guidance | B-M-18-2026 | guide_chunk | 40.4282 | 배관 수명관리 기술지원규정 |
| 2 | guidance | B-M-18-2026 | guide_chunk | 32.1803 | 배관 수명관리 기술지원규정 |
| 3 | guidance | B-M-18-2026 | guide_chunk | 31.7710 | 배관 수명관리 기술지원규정 |
| 4 | guidance | C-C-41-2026 | guide_chunk | 31.1838 | 회분식 공정에 대한 위험과 운전분석(HAZOP) 기법에 관한 기술지원규정 |
| 5 | guidance | B-M-18-2026 | guide_chunk | 30.5047 | 배관 수명관리 기술지원규정 |
| 6 | guidance | B-M-18-2026 | guide_chunk | 30.5039 | 배관 수명관리 기술지원규정 |
| 7 | guidance | C-C-37-2026 | guide_chunk | 30.4188 | 연속공정의 위험과 운전분석(HAZOP) 기법에 관한 기술지원규정 |
| 8 | guidance | B-M-18-2026 | guide_chunk | 29.7034 | 배관 수명관리 기술지원규정 |
| 9 | guidance | C-C-75-2026 | guide_chunk | 28.7789 | 화학설비의 부식 위험성평가에 관한 기술지원규정 |
| 10 | guidance | C-C-64-2026 | guide_chunk | 27.5745 | 노후설비의 관리에 관한 기술지원규정 |

## Variant: mirrored_pip047_form_chloride_terms_removed

- Query: `corrosion prevention piping occupational safety statute Article 256 배관 부식 방지`
- Discipline filter: `<none>`
- Rationale: Same query shape as the PIP-GOLD-047 case in benchmark_rag_retrieval.py, with chloride/sour-service terms removed (PIP-GOLD-003 has has_chloride=False, has_sour=False). Tests whether the RAG layer would flag a non-corrosive case the same way.
- Hits: 10 (mandatory=1, guidance=9)
- Any mandatory in top-10: True
- First mandatory rank: 2

| Rank | Class | reference_code | source_type | score | title |
|---:|---|---|---|---:|---|
| 1 | guidance | B-M-18-2026 | guide_chunk | 57.3521 | 배관 수명관리 기술지원규정 |
| 2 | mandatory | KOSHA04_002000002000004000000000256000 | law_article | 40.7205 | 제256조 부식 방지 |
| 3 | guidance | C-C-20-2026 | guide_chunk | 32.1800 | 화학설비의 재질선정에 관한 기술지원규정 |
| 4 | guidance | B-M-18-2026 | guide_chunk | 28.2761 | 배관 수명관리 기술지원규정 |
| 5 | guidance | B-M-18-2026 | guide_chunk | 28.2111 | 배관 수명관리 기술지원규정 |
| 6 | guidance | B-M-18-2026 | guide_chunk | 25.2687 | 배관 수명관리 기술지원규정 |
| 7 | guidance | D-38-2012 | guide_chunk | 25.1622 | 진한황산 및 발연황산 저장탱크의 공정설계에 관한 기술지침 |
| 8 | guidance | B-M-20-2026 | guide_chunk | 21.8878 | 배관지지물 설치 및 유지에 관한 기술지원규정 |
| 9 | guidance | C-C-23-2026 | guide_chunk | 21.6712 | 위험기반검사(RBI) 기법에 의한 설비의 신뢰성 향상에 관한 기술지원규정 |
| 10 | guidance | P-32-2012 | guide_chunk | 20.3450 | 산소공급설비의 안전기술지침 |

