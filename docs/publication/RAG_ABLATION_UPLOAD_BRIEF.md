# RAG Ablation Upload Brief
Status: Draft
Date: 2026-03-15

## Purpose
- Provide one copy-ready brief for sharing the correct code upload order for the RAG ablation and KOSHA-grounding analysis.
- Keep the upload sequence, rationale, exact paths, and handoff message in one file.

## Recommended Upload Order
1. `scripts/kosha_rag_local.py`
2. `src/cross_discipline/validator.py`
3. benchmark scripts
4. verification code
5. supporting Markdown references

## Exact File Paths
### Priority 1: RAG Pipeline Core
- `scripts/kosha_rag_local.py`

### Priority 2: Cross-Discipline Blocking Logic
- `src/cross_discipline/validator.py`

### Priority 3: Benchmark Scripts
- `scripts/benchmark_cross_discipline.py`
- `scripts/benchmark_seven_pipeline.py`
- `scripts/benchmark_all_runtime.py`
- `scripts/benchmark_piping_system.py`

### Priority 4: Verification Code
- Shared verification:
  - `src/shared/verification.py`
- Discipline verification:
  - `src/piping/verification.py`
  - `src/vessel/verification.py`
  - `src/rotating/verification.py`
  - `src/electrical/verification.py`
  - `src/instrumentation/verification.py`
  - `src/steel/verification.py`
  - `src/civil/verification.py`

### Priority 5: Supporting Markdown References
- `README.md`
- `docs/KOSHA_DATA_SYNC_GUIDE.md`
- `outputs/api_specification.md`

## Why This Order Is Correct
- `kosha_rag_local.py` comes first because the paper's Experiment A depends on understanding the local retrieval pipeline before anything else.
- `validator.py` comes second because the paper also depends on understanding where blocking logic is applied once the retrieved evidence is present.
- The benchmark scripts come next because they show how to turn the pipeline and blocking logic into measurable experiments.
- The verification files come after that because they explain how domain-level checks are structured once the evaluation harness is understood.
- The Markdown references are supporting context, not the first technical dependency.

## What The Receiver Should Check First
### In `scripts/kosha_rag_local.py`
- retrieval flow
- context assembly
- generation path
- where RAG can be turned on or off
- how KOSHA guide content is indexed

### In `src/cross_discipline/validator.py`
- blocking criteria
- red-flag thresholds
- cross-discipline coupling logic
- where retrieved or derived evidence affects pass or block outcomes

### In `scripts/benchmark_*.py`
- how evaluation scenarios are defined
- whether RAG on/off can be toggled cleanly
- what outputs can be converted into tables for the paper

### In `src/*/verification.py`
- how discipline-level checks are normalized
- which parts are shared versus discipline-specific
- how verification evidence is surfaced into final outputs

## Expected Experiment Outputs
- Ablation test harness for `RAG on` vs `RAG off`
- KOSHA citation accuracy checker
- result tables for paper Table 4 and Table 5
- clearer mapping from retrieval evidence to blocking behavior

## Copy-Ready Handoff Message
```text
우선 분석용 1차 파일은 아래 순서로 보겠습니다.

1) scripts/kosha_rag_local.py
2) src/cross_discipline/validator.py
3) scripts/benchmark_cross_discipline.py
4) scripts/benchmark_seven_pipeline.py
5) scripts/benchmark_all_runtime.py
6) src/shared/verification.py
7) src/<discipline>/verification.py 들

보조 자료:
- README.md
- docs/KOSHA_DATA_SYNC_GUIDE.md
- outputs/api_specification.md

이 순서로 보면 먼저 RAG pipeline 구조와 KOSHA grounding 방식을 파악하고,
그 다음 blocking logic과 benchmark harness를 연결해서
Experiment A (RAG on/off ablation) 설계를 바로 할 수 있습니다.
```

## Short Version
If only one file can be sent first, send:
- `scripts/kosha_rag_local.py`

If only three files can be sent first, send:
- `scripts/kosha_rag_local.py`
- `src/cross_discipline/validator.py`
- `scripts/benchmark_cross_discipline.py`
