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

## 2026-03-15 - v0.63
- Date: 2026-03-15
- Version/Tag: v0.63
- Scope: Expanded the RAG ablation source pack so it includes the real local RAG implementation and backend service layers required for experiment design.
- Files/Modules:
  - `exports/rag_ablation_source_pack_v2_20260315_002600/`
  - `exports/rag_ablation_source_pack_v2_20260315_002600.zip`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - pack creation and file-count check
  - zip archive existence and size review
- Result:
  - PASS
- Risks/Follow-ups:
  - The pack is much more useful for analysis, but if the reviewer wants full runnable execution, additional transitive modules outside the current curated set may still be required.

## 2026-03-15 - v0.62
- Date: 2026-03-15
- Version/Tag: v0.62
- Scope: Exported the actual source-code pack needed for RAG ablation review, including core scripts, validator, benchmark files, verification modules, and supporting context files.
- Files/Modules:
  - `exports/rag_ablation_source_pack_20260315_002310/`
  - `exports/rag_ablation_source_pack_20260315_002310.zip`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - source-pack file-list review
  - zip archive existence and size review
- Result:
  - PASS
- Risks/Follow-ups:
  - This pack is curated for the ablation handoff and does not include every transitive dependency; if the reviewer wants full runnable context, a larger code bundle may still be needed.

## 2026-03-15 - v0.61
- Date: 2026-03-15
- Version/Tag: v0.61
- Scope: Created a single Markdown brief for the RAG ablation code-upload order and packaged it as a shareable zip file.
- Files/Modules:
  - `docs/publication/RAG_ABLATION_UPLOAD_BRIEF.md`
  - `exports/rag_ablation_upload_brief_20260315.zip`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - file existence review for the brief document
  - zip archive existence review
- Result:
  - PASS
- Risks/Follow-ups:
  - The zip currently contains only the summary brief, not the referenced source files themselves.

## 2026-03-14 - v0.60
- Date: 2026-03-14
- Version/Tag: v0.60
- Scope: Verified that non-piping disciplines are backed by real executable Python services and corrected the frontend default so configured environments prefer the real backend instead of mock mode.
- Files/Modules:
  - `frontend/store/workbench-store.ts`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - `python -m unittest tests.test_vessel_service tests.test_rotating_service tests.test_electrical_service tests.test_instrumentation_service tests.test_steel_service tests.test_civil_service`
  - FastAPI `TestClient` POST checks for `/api/calculate/{discipline}` on vessel, rotating, electrical, instrumentation, steel, and civil
  - `cmd /c npm --prefix frontend run typecheck`
- Result:
  - PASS
- Risks/Follow-ups:
  - Regulatory/RAG enrichment for all disciplines is still primarily handled in the Next/frontend layer rather than inside each Python service module.

## 2026-03-14 - v0.59
- Date: 2026-03-14
- Version/Tag: v0.59
- Scope: Corrected the publication materials so they explicitly describe the local RAG, KOSHA guide verification, and optional local LLM layer, and rebuilt the curated paper-topic Markdown bundle accordingly.
- Files/Modules:
  - `docs/SYSTEM_OVERVIEW.md`
  - `docs/publication/README.md`
  - `docs/publication/TITLE_ABSTRACT_OPTIONS.md`
  - `docs/publication/PAPER_OUTLINE_AND_SOURCE_MAP.md`
  - `docs/publication/VENUE_AND_STYLE_GUIDE.md`
  - `docs/publication/MANUSCRIPT_SKELETON.md`
  - `exports/paper_topics_md_bundle_20260314_234100/`
  - `exports/paper_topics_md_bundle_20260314_234100.zip`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - spot review of updated publication markdowns
  - curated bundle rebuild and file-count check
- Result:
  - PASS
- Risks/Follow-ups:
  - The manuscript package now mentions the regulatory/RAG layer, but a submission-quality paper will still need clearer experimental evidence specifically on retrieval quality and local-LLM answer quality.

## 2026-03-14 - v0.58
- Date: 2026-03-14
- Version/Tag: v0.58
- Scope: Exported only the Markdown files directly related to the three paper-topic planning tracks and their supporting evidence.
- Files/Modules:
  - `exports/paper_topics_md_bundle_20260314_233056/`
  - `exports/paper_topics_md_bundle_20260314_233056.zip`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - curated bundle file-list review
  - zip file existence and size check
- Result:
  - PASS
- Risks/Follow-ups:
  - This is a curated paper-writing subset; additional code, JSON, or figure assets may still be needed for an actual submission package.

## 2026-03-14 - v0.57
- Date: 2026-03-14
- Version/Tag: v0.57
- Scope: Exported all repository Markdown files into one collected folder and packaged them as a zip archive.
- Files/Modules:
  - `exports/markdown_bundle_20260314_232814/`
  - `exports/markdown_bundle_20260314_232814.zip`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - recursive markdown copy count check
  - zip file existence and size check
- Result:
  - PASS
- Risks/Follow-ups:
  - The export includes all Markdown files under the repository, including historical and i18n content; a curated subset export can be created separately if needed.

## 2026-03-14 - v0.56
- Date: 2026-03-14
- Version/Tag: v0.56
- Scope: Added a publication-planning document package so the repository can be used directly for paper drafting and submission preparation.
- Files/Modules:
  - `docs/publication/README.md`
  - `docs/publication/TITLE_ABSTRACT_OPTIONS.md`
  - `docs/publication/PAPER_OUTLINE_AND_SOURCE_MAP.md`
  - `docs/publication/VENUE_AND_STYLE_GUIDE.md`
  - `docs/publication/MANUSCRIPT_SKELETON.md`
  - `docs/README.md`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - spot review of publication package documents
  - docs hub route review for paper-preparation links
- Result:
  - PASS
- Risks/Follow-ups:
  - The package is sufficient for drafting, but an actual submission will still need venue-specific formatting and literature review polishing.

## 2026-03-14 - v0.55
- Date: 2026-03-14
- Version/Tag: v0.55
- Scope: Added a separate integrated detailed guide so the discipline expansion matrix remains a summary while the actual intent is explained in readable form.
- Files/Modules:
  - `docs/DISCIPLINE_EXPANSION_GUIDE.md`
  - `docs/SYSTEM_OVERVIEW.md`
  - `docs/README.md`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - spot review of `docs/DISCIPLINE_EXPANSION_GUIDE.md`
  - reading-order review in `docs/SYSTEM_OVERVIEW.md` and `docs/README.md`
- Result:
  - PASS
- Risks/Follow-ups:
  - The detailed guide is integrated and readable, but discipline-specific compact docs should still be aligned to the same wording over time.

## 2026-03-14 - v0.54
- Date: 2026-03-14
- Version/Tag: v0.54
- Scope: Consolidated the previously discussed discipline-by-discipline expansion approach into one shared framework inside the system overview.
- Files/Modules:
  - `docs/SYSTEM_OVERVIEW.md`
  - `docs/README.md`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - spot review of `docs/SYSTEM_OVERVIEW.md`
  - docs hub link/path review in `docs/README.md`
- Result:
  - PASS
- Risks/Follow-ups:
  - Per-discipline detailed docs still need migration to the compact model, but the expansion logic now has a single canonical source.

## 2026-03-14 - v0.53
- Date: 2026-03-14
- Version/Tag: v0.53
- Scope: Reduced documentation clutter by consolidating root overview guidance and compacting the vessel discipline docs into a 4-file structure.
- Files/Modules:
  - `docs/SYSTEM_OVERVIEW.md`
  - `docs/architecture_overview.md`
  - `docs/DISCIPLINE_DOCUMENT_MAP.md`
  - `docs/DOCS_NAVIGATION_GUIDELINE.md`
  - `docs/README.md`
  - `outputs/user_guide.md`
  - `docs/vessel/README.md`
  - `docs/vessel/ENGINEERING_MODEL.md`
  - `docs/vessel/EXECUTION_CONTRACT.md`
  - `docs/vessel/INTERFACES_AND_VALIDATION.md`
  - `docs/vessel/ARCHITECTURE.md` (removed)
  - `docs/vessel/FACTOR_TAXONOMY.md` (removed)
  - `docs/vessel/DELIVERABLES.md` (removed)
  - `docs/vessel/INPUT_OUTPUT_SCHEMA.md` (removed)
  - `docs/vessel/VERIFICATION_RULES.md` (removed)
  - `docs/vessel/CROSS_DISCIPLINE_INTERFACES.md` (removed)
  - `docs/vessel/GOLDEN_CASES.md` (removed)
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - root/vessel file presence review
  - reference search for removed vessel split files
- Result:
  - PASS
- Risks/Follow-ups:
  - Other disciplines still use the older split-file baseline and can be migrated incrementally using the same compact model.

## 2026-03-14 - v0.52
- Date: 2026-03-14
- Version/Tag: v0.52
- Scope: Expanded piping docs toward construction-facing ISO decision logic and established a standardized document skeleton for all seven engineering disciplines.
- Files/Modules:
  - `docs/architecture_overview.md`
  - `agents/piping_agent.md`
  - `docs/DISCIPLINE_DOCUMENT_MAP.md`
  - `docs/README.md`
  - `docs/piping/*.md` (new baseline files)
  - `docs/vessel/*.md`
  - `docs/rotating/*.md`
  - `docs/electrical/*.md`
  - `docs/instrumentation/*.md`
  - `docs/steel/*.md`
  - `docs/civil/*.md`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - directory and file presence review under `docs/`
  - spot inspection of representative discipline files
- Result:
  - PASS
- Risks/Follow-ups:
  - The new discipline documents are skeleton baselines; detailed numeric schemas, examples, and EN/KO companion files still need a follow-up round.

## 2026-03-03 - v0.51
- Date: 2026-03-03
- Version/Tag: v0.51
- Scope: Improved regulatory panel local-snapshot scoring path for implementation quality (response-path optimization + minimal modular split).
- Files/Modules:
  - `frontend/lib/kosha/local-snapshot-scoring.ts`
  - `frontend/lib/kosha/local-snapshot.ts`
  - `frontend/tests/unit/kosha-local-snapshot-scoring.test.ts`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - `cmd /c npm --prefix frontend run test:unit`
  - `cmd /c npm --prefix frontend run typecheck`
  - `python scripts/run_quality_gate.py --profile implementation`
- Result:
  - PASS
- Risks/Follow-ups:
  - Local snapshot still reads full JSON snapshots into memory; next iteration can add manifest-hash based lightweight index prebuild for larger corpus growth.

## 2026-03-03 - v0.50
- Date: 2026-03-03
- Version/Tag: v0.50
- Scope: Switched to implementation-first completion flow, added executable implementation gate profile, and fixed backend/frontend E2E reliability blockers.
- Files/Modules:
  - `scripts/run_quality_gate.py`
  - `scripts/smoke_backend_api.py`
  - `frontend/playwright.config.ts`
  - `frontend/tests/e2e/backend-mode-seven.spec.ts`
  - `frontend/tests/e2e/workbench-smoke.spec.ts`
  - `frontend/lib/kosha/crosswalk.ts`
  - `docs/plans/IMPLEMENTATION_COMPLETION_CHECKLIST_V0.1.md`
  - `docs/plans/PROJECT_MODULARIZATION_MASTER_PLAN_V0.1.md`
  - `docs/revisions/CHANGELOG.md`
- Verification Commands:
  - `python scripts/run_quality_gate.py --profile fast`
  - `python scripts/run_quality_gate.py --profile implementation`
- Result:
  - PASS
- Risks/Follow-ups:
  - `run_quality_gate.py` output on PowerShell still emits `python : ...` NativeCommandError decoration even when command returns success; output formatting cleanup can be handled in next maintenance pass.

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
