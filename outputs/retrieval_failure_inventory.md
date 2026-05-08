# KOSHA RAG Retrieval Failure Inventory (Enhanced FTS, K=5 threshold)

- Dataset: `datasets/kosha_rag/rag_eval_queries.json`
- Total queries: 50
- Failure rule: `failure := first_relevant_rank > 5 OR no relevant hit in top-10`
- Failure count: 7
- Failure rate: 0.1400

## Diagnosis Summary

| Diagnosis | Count |
|---|---:|
| paraphrase_too_loose | 6 |
| regulatory_class_mismatch | 1 |

## Failure Details

### C-C-23 RBI | paraphrase_too_loose

- Query: `C-C-23 RBI guideline`
- Discipline filter: `None`
- Expected ref codes: ['C-C-23-2026']
- Actual first relevant rank: not in top-10
- Top-3 hits:
  1. ref=`C-C-58-2026` title=`최악 및 대안의 사고 시나리오 선정에 관한 기술지원규정`

### B-M-18 piping life | paraphrase_too_loose

- Query: `배관 잔여수명 관리`
- Discipline filter: `piping`
- Expected ref codes: ['B-M-18-2026']
- Actual first relevant rank: not in top-10
- Top-3 hits:
  1. ref=`G-82-2018` title=`실험실 안전보건에 관한 기술지침`
  2. ref=`A-R-1-2026` title=`자율안전보건관리체계 구축 및 운영에 관한 기술지원규정`
  3. ref=`B-M-37-2026` title=`회전기계 등의 끼임·절단재해 예방을 위한 기술지원규정`

### B-M-18 piping life | regulatory_class_mismatch

- Query: `pipe life management regulation`
- Discipline filter: `piping`
- Expected ref codes: ['B-M-18-2026']
- Actual first relevant rank: not in top-10
- Top-3 hits:
  1. ref=`C-C-15-2026` title=`배관재질 선정에 관한 기술지원규정`
  2. ref=`P-158-2017` title=`장거리 이송배관 안전관리에 관한 기술지침`
  3. ref=`C-C-79-2026` title=`화학설비의 부식 관리문서 개발에 관한 기술지원규정`

### C-C-75 corrosion risk | paraphrase_too_loose

- Query: `CCD corrosion risk assessment`
- Discipline filter: `piping`
- Expected ref codes: ['C-C-75-2026']
- Actual first relevant rank: not in top-10
- Top-3 hits:
  1. ref=`C-C-79-2026` title=`화학설비의 부식 관리문서 개발에 관한 기술지원규정`

### Article 256 corrosion prevention | paraphrase_too_loose

- Query: `산업안전보건기준에 관한 규칙 제256조`
- Discipline filter: `None`
- Expected ref codes: []
- Expected title substrings: ['제256조 부식 방지']
- Actual first relevant rank: not in top-10
- Top-3 hits:
  1. ref=`B-M-18-2026` title=`배관 수명관리 기술지원규정`

### Article 256 corrosion prevention | paraphrase_too_loose

- Query: `rules on occupational safety and health standards article 256`
- Discipline filter: `None`
- Expected ref codes: []
- Expected title substrings: ['제256조 부식 방지']
- Actual first relevant rank: not in top-10
- Top-3 hits:
  1. ref=`A-43-2018` title=`바륨에 대한 작업환경측정,분석 기술지침`
  2. ref=`A-46-2021` title=`요오드에 대한 작업환경측정,분석 기술지침`
  3. ref=`A-47-2018` title=`텅스텐에 대한 작업환경측정,분석 기술지침`

### Article 256 corrosion prevention | paraphrase_too_loose

- Query: `부식 방지 법령 제256조`
- Discipline filter: `None`
- Expected ref codes: []
- Expected title substrings: ['제256조 부식 방지']
- Actual first relevant rank: not in top-10
- Top-3 hits:
  1. ref=`D-38-2012` title=`진한황산 및 발연황산 저장탱크의 공정설계에 관한 기술지침`

