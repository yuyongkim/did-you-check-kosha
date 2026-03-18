# Delivery Log

This log is mandatory for final completion history management.

## Entry Template
- Date:
- Version/Tag:
- Scope:
- Files/Modules:
- Verification Commands:
- Result:
- Risks/Follow-ups:

---

## 2026-03-01 - v0.49
- Date: 2026-03-01
- Version/Tag: v0.49
- Scope: Added all-discipline sample submission report package (EN/KO) under `docs/reports` and linked it from docs hub.
- Files/Modules:
  - `docs/reports/README.md`
  - `docs/i18n/en/reports/README.md`
  - `docs/i18n/ko/reports/README.md`
  - `docs/reports/SAMPLE_VESSEL_REPORT_SUBMISSION_V0.1.md`
  - `docs/i18n/en/reports/SAMPLE_VESSEL_REPORT_SUBMISSION_V0.1.md`
  - `docs/i18n/ko/reports/SAMPLE_VESSEL_REPORT_SUBMISSION_V0.1.md`
  - `docs/reports/SAMPLE_ROTATING_REPORT_SUBMISSION_V0.1.md`
  - `docs/i18n/en/reports/SAMPLE_ROTATING_REPORT_SUBMISSION_V0.1.md`
  - `docs/i18n/ko/reports/SAMPLE_ROTATING_REPORT_SUBMISSION_V0.1.md`
  - `docs/reports/SAMPLE_ELECTRICAL_REPORT_SUBMISSION_V0.1.md`
  - `docs/i18n/en/reports/SAMPLE_ELECTRICAL_REPORT_SUBMISSION_V0.1.md`
  - `docs/i18n/ko/reports/SAMPLE_ELECTRICAL_REPORT_SUBMISSION_V0.1.md`
  - `docs/reports/SAMPLE_INSTRUMENTATION_REPORT_SUBMISSION_V0.1.md`
  - `docs/i18n/en/reports/SAMPLE_INSTRUMENTATION_REPORT_SUBMISSION_V0.1.md`
  - `docs/i18n/ko/reports/SAMPLE_INSTRUMENTATION_REPORT_SUBMISSION_V0.1.md`
  - `docs/reports/SAMPLE_STEEL_REPORT_SUBMISSION_V0.1.md`
  - `docs/i18n/en/reports/SAMPLE_STEEL_REPORT_SUBMISSION_V0.1.md`
  - `docs/i18n/ko/reports/SAMPLE_STEEL_REPORT_SUBMISSION_V0.1.md`
  - `docs/reports/SAMPLE_CIVIL_REPORT_SUBMISSION_V0.1.md`
  - `docs/i18n/en/reports/SAMPLE_CIVIL_REPORT_SUBMISSION_V0.1.md`
  - `docs/i18n/ko/reports/SAMPLE_CIVIL_REPORT_SUBMISSION_V0.1.md`
  - `docs/README.md`
  - `docs/i18n/en/README.md`
  - `docs/i18n/ko/README.md`
  - `docs/BILINGUAL_INDEX.md`
  - `docs/i18n/en/BILINGUAL_INDEX.md`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - bilingual index regeneration script run after report creation
  - companion coverage check result: `MISSING=0`
- Result:
  - PASS
- Risks/Follow-ups:
  - Sample values are demonstration-grade; real submissions must replace all numeric values with run-trace evidence and project-approved assumptions.

## 2026-03-01 - v0.48
- Date: 2026-03-01
- Version/Tag: v0.48
- Scope: Added a fully filled piping sample report submission package (EN/KO) and linked it from docs hub/user guides.
- Files/Modules:
  - `docs/reports/SAMPLE_PIPING_REPORT_SUBMISSION_V0.1.md`
  - `docs/i18n/en/reports/SAMPLE_PIPING_REPORT_SUBMISSION_V0.1.md`
  - `docs/i18n/ko/reports/SAMPLE_PIPING_REPORT_SUBMISSION_V0.1.md`
  - `docs/README.md`
  - `docs/i18n/en/README.md`
  - `docs/i18n/ko/README.md`
  - `docs/BILINGUAL_INDEX.md`
  - `docs/i18n/en/BILINGUAL_INDEX.md`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - Bilingual index regeneration script run after file creation
  - companion coverage check maintained (`MISSING=0`)
- Result:
  - PASS
- Risks/Follow-ups:
  - Current sample is piping-focused; vessel and rotating sample submissions can be added next.

## 2026-03-01 - v0.47
- Date: 2026-03-01
- Version/Tag: v0.47
- Scope: Expanded docs hub guidance and added report-submission documentation pack (EN/KO), then regenerated bilingual index.
- Files/Modules:
  - `docs/README.md`
  - `docs/i18n/en/README.md`
  - `docs/i18n/ko/README.md`
  - `docs/DOCS_NAVIGATION_GUIDELINE.md`
  - `docs/i18n/en/DOCS_NAVIGATION_GUIDELINE.md`
  - `docs/i18n/ko/DOCS_NAVIGATION_GUIDELINE.md`
  - `docs/REPORT_SUBMISSION_TEMPLATE.md`
  - `docs/i18n/en/REPORT_SUBMISSION_TEMPLATE.md`
  - `docs/i18n/ko/REPORT_SUBMISSION_TEMPLATE.md`
  - `docs/BILINGUAL_INDEX.md`
  - `docs/i18n/en/BILINGUAL_INDEX.md`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - index regeneration script run (table refreshed with new docs)
  - coverage check: `MISSING=0` for canonical docs EN/KO companions
- Result:
  - PASS
- Risks/Follow-ups:
  - Report template is generic by design; discipline-specific report annex templates can be added in next round (piping/vessel/rotating first).

## 2026-03-01 - v0.46
- Date: 2026-03-01
- Version/Tag: v0.46
- Scope: Rolled out full EN/KO companion coverage for all canonical docs files and added bilingual index.
- Files/Modules:
  - `docs/BILINGUAL_INDEX.md`
  - `docs/i18n/en/BILINGUAL_INDEX.md`
  - `docs/i18n/ko/BILINGUAL_INDEX.md`
  - `docs/README.md`
  - `docs/i18n/en/README.md`
  - `docs/i18n/ko/README.md`
  - `docs/**/**/*.en.md` (new companion files)
  - `docs/**/**/*.ko.md` (new companion files)
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - coverage check: `BASE_DOCS=47, MISSING_COUNT=0` (all canonical docs have EN/KO companions)
  - index generation: `docs/BILINGUAL_INDEX.md` regenerated after rollout
- Result:
  - PASS
- Risks/Follow-ups:
  - Many KO companions are operational summary style with section-map linkage; deep line-by-line translation can be iteratively upgraded for high-priority specs.

## 2026-03-01 - v0.45
- Date: 2026-03-01
- Version/Tag: v0.45
- Scope: Added bilingual docs (EN/KR) and piping material-based NDE guide; linked from docs hub and aligned with frontend piping panel.
- Files/Modules:
  - `docs/README.md`
  - `docs/i18n/en/README.md`
  - `docs/i18n/ko/README.md`
  - `docs/i18n/en/piping/NDE_RECOMMENDATIONS.md`
  - `docs/i18n/ko/piping/NDE_RECOMMENDATIONS.md`
  - `docs/revisions/CHANGELOG.md`
  - `frontend/components/visualization/piping-visuals.tsx`
- Verification Commands:
  - `npm --prefix frontend run lint`
  - `npm --prefix frontend run typecheck`
- Result:
  - PASS
- Risks/Follow-ups:
  - Per-discipline deep bilingual guides are still partial; expand vessel/rotating/electrical/instrumentation/steel/civil guides in next round.

## 2026-02-27 - Bootstrap Entry
- Date: 2026-02-27
- Version/Tag: policy-bootstrap
- Scope: Established mandatory final Markdown completion logging policy.
- Files/Modules:
  - `docs/revisions/REVISION_POLICY.md`
  - `docs/revisions/DELIVERY_LOG.md`
  - `docs/README.md`
  - `docs/plans/PROJECT_PLAN_V0.1.md`
  - `docs/plans/FRONTEND_RELEASE_CHECKLIST_V0.1.md`
- Verification Commands:
  - N/A (documentation-only policy update)
- Result:
  - PASS
- Risks/Follow-ups:
  - All future completed rounds must append entries here and in changelog.

## 2026-02-28 - v0.44
- Date: 2026-02-28
- Version/Tag: v0.44
- Scope: Added one-step completion logger for changelog and delivery log; updated policy/docs to mandate use.
- Files/Modules:
  - `scripts/log_completion.py`
  - `docs/revisions/REVISION_POLICY.md`
  - `docs/README.md`
  - `README.md`
- Verification Commands:
  - `python scripts/log_completion.py --dry-run --version test --title test --scope test`
- Result:
  - PASS
- Risks/Follow-ups:
  - Continue using this command at every completed round.
