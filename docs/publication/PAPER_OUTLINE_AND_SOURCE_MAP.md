# Paper Outline And Source Map
Status: Draft

## Recommended Paper Structure
1. Introduction
2. Related Background And Problem Context
3. System Architecture
4. Regulatory Knowledge Layer And Local RAG Support
5. Discipline Modeling And Verification Design
6. Dataset And Evaluation Protocol
7. Experimental Results
8. Discussion
9. Limitations
10. Conclusion

## Section Mapping
| Section | Main Claim | Primary Source Files | Suggested Figures/Tables |
| --- | --- | --- | --- |
| Introduction | Multi-discipline maintenance screening is fragmented and needs unified, explainable verification | `docs/SYSTEM_OVERVIEW.md`, `docs/DISCIPLINE_EXPANSION_GUIDE.md`, `docs/standards_index.md` | Figure 1: problem framing diagram |
| Related Background And Problem Context | The contribution is a systems-and-verification framework rather than a single-discipline calculator | `docs/verification_layers.md`, `docs/golden_dataset_spec.md`, `COMPLETION_REPORT_20260314.md` | Table 1: contribution boundary |
| System Architecture | The platform integrates seven discipline services, orchestration, API execution, support agents, and report packaging | `docs/SYSTEM_OVERVIEW.md`, `src/api/server.py`, `src/orchestrator/seven_pipeline.py`, `src/agents/specialists/*.py`, `outputs/api_specification.md` | Figure 2: architecture block diagram |
| Regulatory Knowledge Layer And Local RAG Support | The platform also supports regulatory grounding through local KOSHA corpus sync, guide ingestion, local RAG retrieval, and optional local LLM generation | `README.md`, `docs/KOSHA_DATA_SYNC_GUIDE.md`, `outputs/api_specification.md` | Figure 3: regulatory knowledge flow; Table 2: KOSHA/RAG component map |
| Discipline Modeling And Verification Design | Each discipline follows a shared service pattern and a four-layer verification model | `docs/DISCIPLINE_EXPANSION_GUIDE.md`, `src/*/service.py`, `src/*/verification.py`, `docs/verification_layers.md` | Table 3: discipline expansion matrix; Figure 4: verification flow |
| Dataset And Evaluation Protocol | Synthetic golden datasets and scenario-set benchmarks provide reproducible evaluation | `docs/golden_dataset_spec.md`, `golden/*.json`, `datasets/golden_standards/*.json`, `scripts/generate_*_golden_dataset.py` | Table 4: dataset composition |
| Experimental Results | The framework achieves complete golden-dataset verification and differentiated pipeline blocking behavior | `outputs/verification_report_runtime.md`, `outputs/seven_pipeline_report.md`, `outputs/cross_discipline_report.md`, `outputs/cross_discipline_tuning_report.md`, `scripts/benchmark_*.py` | Figure 5: runtime results; Table 5: scenario-set results |
| Discussion | The system is strong in traceable screening, regulatory grounding, and reproducibility, but still screening-level in several outputs | `COMPLETION_REPORT_20260314.md`, `docs/DISCIPLINE_EXPANSION_GUIDE.md`, `README.md` | Table 6: strengths vs limitations |
| Limitations | Some outputs remain screening-level and real plant data validation is still needed | `COMPLETION_REPORT_20260314.md`, `docs/publication/VENUE_AND_STYLE_GUIDE.md` | None |
| Conclusion | A reusable engineering-AI and regulatory-grounded verification framework has been demonstrated and is ready for stronger external validation | `docs/SYSTEM_OVERVIEW.md`, `outputs/*.md`, `README.md` | None |

## Recommended Figure Plan
- Figure 1:
  - Fragmented single-discipline maintenance review vs unified seven-discipline workflow
- Figure 2:
  - System architecture showing orchestrator, seven discipline services, support agents, API layer, and report outputs
- Figure 3:
  - Regulatory knowledge flow showing KOSHA sync, guide parsing, local RAG retrieval, and optional local LLM answer generation
- Figure 4:
  - Four-layer verification pipeline with cross-discipline blocking gate
- Figure 5:
  - Benchmark result summary using completion and blocking ratios

## Recommended Table Plan
- Table 1:
  - Paper contribution statement
  - columns: problem, contribution, artifact evidence
- Table 2:
  - KOSHA/RAG component map and platform role
- Table 3:
  - Discipline expansion matrix from `docs/SYSTEM_OVERVIEW.md`
- Table 4:
  - Golden dataset counts and category ratios from `docs/golden_dataset_spec.md`
- Table 5:
  - Reported results from `outputs/verification_report_runtime.md`, `outputs/seven_pipeline_report.md`, and `outputs/cross_discipline_report.md`
- Table 6:
  - Known limitations and next-step extensions from `COMPLETION_REPORT_20260314.md`

## High-Value Code Files To Cite In The Method Section
- `src/api/server.py`
- `src/orchestrator/seven_pipeline.py`
- `src/cross_discipline/validator.py`
- `src/piping/service.py`
- `src/vessel/service.py`
- `src/rotating/service.py`
- `src/electrical/service.py`
- `src/instrumentation/service.py`
- `src/steel/service.py`
- `src/civil/service.py`

## High-Value Result Files To Quote In The Evaluation Section
- `README.md`
- `docs/KOSHA_DATA_SYNC_GUIDE.md`
- `outputs/api_specification.md`
- `outputs/verification_report_runtime.md`
- `outputs/seven_pipeline_report.md`
- `outputs/cross_discipline_report.md`
- `outputs/cross_discipline_tuning_report.md`

## Writing Cautions
- Do not claim full design automation for deliverables such as ISO or repair packages where the current implementation is still screening-level.
- Do not present synthetic golden datasets as a substitute for external industrial validation.
- Frame the contribution as a reproducible engineering verification framework with explainable screening outputs.
