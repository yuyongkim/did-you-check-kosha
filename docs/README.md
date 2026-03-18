# Documentation Hub

This repository follows a docs-first workflow.

## Start Here (Fast Path)
If you are not sure what to read first, use this order:
1. `docs/i18n/ko/README.md` or `docs/i18n/en/README.md` (user-level overview)
2. `docs/SYSTEM_OVERVIEW.md` (system scope, document model, reading routes)
3. `docs/i18n/ko/REPORT_SUBMISSION_TEMPLATE.md` or `docs/i18n/en/REPORT_SUBMISSION_TEMPLATE.md` (how to submit engineering report output)

## Bilingual Guides (EN/KR)
- User guide (English): `docs/i18n/en/README.md`
- 사용자 가이드 (한국어): `docs/i18n/ko/README.md`
- System overview: `docs/SYSTEM_OVERVIEW.md`
- Report submission template (English): `docs/i18n/en/REPORT_SUBMISSION_TEMPLATE.md`
- 보고서 제출 템플릿 (한국어): `docs/i18n/ko/REPORT_SUBMISSION_TEMPLATE.md`
- Piping NDE recommendations (English): `docs/i18n/en/piping/NDE_RECOMMENDATIONS.md`
- 배관 NDE 추천 (한국어): `docs/i18n/ko/piping/NDE_RECOMMENDATIONS.md`
- Sample piping submission (English): `docs/i18n/en/reports/SAMPLE_PIPING_REPORT_SUBMISSION_V0.1.md`
- 샘플 배관 제출본 (한국어): `docs/i18n/ko/reports/SAMPLE_PIPING_REPORT_SUBMISSION_V0.1.md`
- All-discipline sample pack (English): `docs/i18n/en/reports/README.md`
- 전 공종 샘플 팩 (한국어): `docs/i18n/ko/reports/README.md`
- Full mapping index (all docs): `docs/BILINGUAL_INDEX.md`

Note:
- Language docs are separated under:
  - `docs/i18n/en/`
  - `docs/i18n/ko/`
- Canonical technical baseline remains the source `*.md` unless explicitly superseded.

## Purpose
- Freeze architecture and validation requirements before implementation.
- Keep all requirement changes traceable with explicit revision history.
- Prevent oversized, hard-to-debug code by enforcing modular design boundaries.
- Provide repeatable engineering reporting format for internal/external review.

## Structure and What It Is For
- `docs/SYSTEM_OVERVIEW.md`: consolidated system overview and compact document model
  - includes the unified discipline expansion framework and matrix
- `docs/DISCIPLINE_EXPANSION_GUIDE.md`: detailed explanation of each discipline's basis, decisions, outputs, downstream use, and validation focus
- `docs/plans/`: project plans, execution roadmaps, release checklists
- `docs/specs/`: detailed architecture/specification baselines by subsystem
- `docs/revisions/`: changelog, delivery log, revision policy
- `docs/glossary/`: standards terms and engineering vocabulary references
- `docs/publication/`: paper planning package, title/abstract options, outline, style guide, and manuscript skeleton
- `docs/piping/`: piping-specific architecture, factor/deliverable baseline, user guide, reports, agent notes
- `docs/vessel/`: vessel-specific documentation baseline
- `docs/rotating/`: rotating-specific documentation baseline
- `docs/electrical/`: electrical-specific documentation baseline
- `docs/instrumentation/`: instrumentation-specific documentation baseline
- `docs/steel/`: steel-specific documentation baseline
- `docs/civil/`: civil-specific documentation baseline
- `docs/prompts/`: implementation prompts for generation and execution consistency

## Reading Order by Goal
### A) Process Engineer (PIP / VES / ROT first)
1. `docs/i18n/ko/README.md`
2. `docs/i18n/ko/standards_index.md`
3. `docs/i18n/ko/piping/NDE_RECOMMENDATIONS.md`
4. `docs/SYSTEM_OVERVIEW.md`
5. `docs/DISCIPLINE_EXPANSION_GUIDE.md`
6. discipline docs under `docs/piping/`, `docs/vessel/`, `docs/rotating/` and relevant `docs/specs/*`

### B) Frontend / Product Work
1. `docs/plans/PROJECT_PLAN_V0.1.md`
2. `docs/specs/frontend/README.md`
3. `docs/specs/frontend/00_OVERVIEW_AND_ARCHITECTURE_V0.1.md`
4. `docs/plans/FRONTEND_RELEASE_CHECKLIST_V0.1.md`

### C) Verification / QA / Compliance
1. `docs/verification_layers.md`
2. `docs/specs/VERIFICATION_FRAMEWORK_SPEC_V0.1.md`
3. `docs/specs/verification/README.md`
4. `docs/golden_dataset_spec.md`

### D) Report Submission
1. `docs/i18n/ko/REPORT_SUBMISSION_TEMPLATE.md` or `docs/i18n/en/REPORT_SUBMISSION_TEMPLATE.md`
2. attach run evidence and references listed in the template
3. record completion in revisions docs

### E) Paper Preparation
1. `docs/publication/README.md`
2. `docs/publication/TITLE_ABSTRACT_OPTIONS.md`
3. `docs/publication/PAPER_OUTLINE_AND_SOURCE_MAP.md`
4. `docs/publication/VENUE_AND_STYLE_GUIDE.md`
5. `docs/publication/MANUSCRIPT_SKELETON.md`

## Required Practice
1. Any requirement or architecture change must update:
   - `docs/revisions/CHANGELOG.md`
   - `docs/revisions/DELIVERY_LOG.md` (when the task/round is completed)
   - impacted spec document(s) in `docs/specs/`
2. Keep one topic per document where possible.
3. Use version labels in major docs, for example:
   - `PROJECT_PLAN_V0.1.md`
4. Mark status in each major doc header:
   - `Draft`, `Review`, `Approved`, `Superseded`

## Implementation Guardrail
- Do not start production coding until architecture and verification docs are approved.
- When implementation starts, keep modules separated by page/topic/domain to reduce debugging complexity.

## Completion Guardrail (Mandatory)
- At the end of every completed work round, update both:
  - `docs/revisions/CHANGELOG.md`
  - `docs/revisions/DELIVERY_LOG.md`
- A task is not considered complete unless both Markdown records are updated.
- Use one-step logger to reduce misses:
  - `python scripts/log_completion.py --version <tag> --title "<title>" --scope "<scope>"`
