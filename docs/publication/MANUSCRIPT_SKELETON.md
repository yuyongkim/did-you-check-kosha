# Manuscript Skeleton
Status: Draft

## Title
A Seven-Discipline EPC Maintenance Verification Framework with Layered Validation and Cross-Discipline Consistency Checks

## Abstract
Use the abstract draft from `docs/publication/TITLE_ABSTRACT_OPTIONS.md` and refine it for the target venue.

## Keywords
- EPC maintenance
- engineering AI
- multi-discipline verification
- explainable screening
- cross-discipline validation

## 1. Introduction
- Describe the fragmentation problem in maintenance screening across piping, vessel, rotating, electrical, instrumentation, steel, and civil domains.
- State that isolated calculators are not enough when engineering decisions propagate across domain boundaries.
- Introduce the repository contribution as a unified verification framework rather than a standalone predictive model.
- End the section with 3 to 4 explicit contributions.

## 2. Problem Context And Contribution Boundary
- Explain what the system does:
  - discipline calculation
  - layered verification
  - cross-discipline validation
  - API-based execution and report packaging
- Explain what the system does not yet do:
  - full design automation for every downstream deliverable
  - replacement of formal code sign-off or expert review

## 3. System Architecture
- Summarize orchestrator, discipline services, support agents, API layer, and runtime flow.
- Cite:
  - `docs/SYSTEM_OVERVIEW.md`
  - `src/api/server.py`
  - `src/orchestrator/seven_pipeline.py`
- Insert Figure 2 here.

## 4. Regulatory Knowledge Layer And Local RAG Support
- Explain that the platform is not only a calculation engine but also a regulatory-support environment.
- Describe:
  - local KOSHA corpus synchronization
  - KOSHA guide API sync and PDF parsing
  - local SQLite FTS retrieval
  - frontend regulatory-compliance and local-RAG panels
  - optional local-LLM generation on top of retrieved passages
- Cite:
  - `README.md`
  - `docs/KOSHA_DATA_SYNC_GUIDE.md`
  - `outputs/api_specification.md`

## 5. Discipline Modeling And Verification Framework
### 4.1 Shared Discipline Pattern
- Explain the common pattern:
  - models
  - calculations
  - verification
  - service

### 4.2 Four-Layer Verification
- Layer 1: input, unit, and range guard
- Layer 2: multi-path consensus
- Layer 3: physics and standards compliance
- Layer 4: reverse verification

### 4.3 Cross-Discipline Validator
- Explain why discipline-level correctness is not sufficient without inter-domain consistency checks.
- Cite:
  - `src/cross_discipline/validator.py`
  - `docs/verification_layers.md`

## 6. Discipline Expansion Scope
- Summarize the seven-discipline expansion map using:
  - `docs/SYSTEM_OVERVIEW.md`
  - `docs/DISCIPLINE_EXPANSION_GUIDE.md`
- Insert Table 2 here.

## 7. Dataset And Evaluation Protocol
- Describe the synthetic golden dataset specification:
  - case counts
  - standard, boundary, failure-mode ratios
  - required schema
  - tolerance policy
- Cite:
  - `docs/golden_dataset_spec.md`
  - `golden/*.json`
  - `datasets/golden_standards/*.json`

## 8. Experimental Results
### 7.1 Discipline-Level Runtime Verification
- Report the aggregated runtime verification results from:
  - `outputs/verification_report_runtime.md`

### 7.2 Seven-Discipline Pipeline Results
- Report scenario-set completion and blocking ratios from:
  - `outputs/seven_pipeline_report.md`

### 7.3 Cross-Discipline Blocking And Threshold Tuning
- Report tuned profile behavior from:
  - `outputs/cross_discipline_report.md`
  - `outputs/cross_discipline_tuning_report.md`

## 9. Discussion
- Explain why full pass on discipline golden datasets does not eliminate the need for cross-discipline blocking logic.
- Highlight explainability, regulatory grounding, and reproducibility strengths.
- Connect screening outputs to engineering review workflows.

## 10. Limitations
- Synthetic dataset dependence
- Screening-level outputs for some domain extensions
- Need for real site data and expert comparison
- Need for stronger external benchmarking
- Need for stronger evaluation of local RAG answer quality under real user queries

## 11. Conclusion
- Re-state the main contribution as an explainable, reproducible, multi-discipline engineering verification framework.
- State the next-step roadmap:
  - real-site validation
  - richer discipline inputs
  - stronger downstream deliverable generation
  - stronger local-RAG and local-LLM regulatory evaluation

## Appendices
- Appendix A:
  - discipline-specific outputs and red flags
- Appendix B:
  - benchmark scenario definitions
- Appendix C:
  - reproducibility notes and test commands
