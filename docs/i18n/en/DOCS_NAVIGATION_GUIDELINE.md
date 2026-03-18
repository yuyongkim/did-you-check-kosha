# Documentation Navigation Guideline

Status: Draft  
Version: v0.1  
Last Updated: 2026-03-01

## 1) Why This Document Exists
This guide tells you exactly:
- which docs to read first,
- which docs are required for each role/task,
- and which docs are required before report submission.

Use this as an operational map, not as a replacement for technical specs.

## 2) One-Minute Route Selection
Choose your route first:

1. `I need to understand what this system calculates`
  - Read: `docs/i18n/ko/README.md` (or `.en.md`)
  - Then: `docs/standards_index.md`, `docs/verification_layers.md`

2. `I need architecture/spec details before implementation`
  - Read: `docs/architecture_overview.md`
  - Then: `docs/specs/README.md`
  - Then: discipline/front-end/verification spec files

3. `I need to run QA/verification and approve release`
  - Read: `docs/specs/VERIFICATION_FRAMEWORK_SPEC_V0.1.md`
  - Then: `docs/golden_dataset_spec.md`
  - Then: `docs/plans/FRONTEND_RELEASE_CHECKLIST_V0.1.md`

4. `I need to submit a formal engineering report`
  - Read: `docs/i18n/ko/REPORT_SUBMISSION_TEMPLATE.md` (or `.en.md`)
  - Then: collect evidence listed in the template

## 3) Reading Order by Role
### 3.1 Process Engineer (Piping / Vessel / Rotating)
1. `docs/i18n/ko/README.md`
2. `docs/i18n/ko/standards_index.md`
3. `docs/i18n/ko/piping/NDE_RECOMMENDATIONS.md`
4. `docs/piping/USER_GUIDE.md`
5. relevant discipline specs under `docs/specs/`

### 3.2 Frontend Engineer
1. `docs/plans/PROJECT_PLAN_V0.1.md`
2. `docs/specs/frontend/README.md`
3. `docs/specs/frontend/00_OVERVIEW_AND_ARCHITECTURE_V0.1.md`
4. `docs/specs/frontend/02_COMPONENT_SYSTEM_V0.1.md`
5. `docs/plans/FRONTEND_RELEASE_CHECKLIST_V0.1.md`

### 3.3 Verification / QA Engineer
1. `docs/verification_layers.md`
2. `docs/specs/VERIFICATION_FRAMEWORK_SPEC_V0.1.md`
3. `docs/specs/verification/README.md`
4. `docs/golden_dataset_spec.md`
5. `docs/revisions/REVISION_POLICY.md`

### 3.4 Reviewer / Manager
1. `docs/i18n/ko/README.md` (or `.en.md`)
2. `docs/plans/PROJECT_PLAN_V0.1.md`
3. `docs/revisions/CHANGELOG.md`
4. `docs/revisions/DELIVERY_LOG.md`
5. latest submission package from `docs/REPORT_SUBMISSION_TEMPLATE.*`

## 4) Decision Gates and Required Docs
### Gate A: Start of a New Work Round
Required:
- `docs/plans/PROJECT_PLAN_V0.1.md`
- impacted spec docs under `docs/specs/`

### Gate B: Before Implementation Merge
Required:
- corresponding frontend/spec docs
- verification strategy docs
- release checklist entry

### Gate C: Before Report Submission
Required:
- completed report template
- verification evidence
- standards references
- changelog and delivery log updates

## 5) Common Mistakes to Avoid
- Reading only plan docs without spec docs.
- Using `*.ko.md` companion summary as sole technical source for edge cases.
- Submitting report without:
  - standards references,
  - red/warning flag disposition,
  - evidence commands/output paths.
- Forgetting `CHANGELOG` and `DELIVERY_LOG` updates.

## 6) Bilingual Policy
- Canonical baseline: source `*.md`.
- Language companions:
  - `*.en.md`: English companion.
  - `*.ko.md`: Korean companion.
- Full map:
  - `docs/BILINGUAL_INDEX.md`

## 7) Operational Checklist
Before you say "done", verify:
1. You read the docs route for your role.
2. You updated impacted specs/plans.
3. You prepared submission using `docs/REPORT_SUBMISSION_TEMPLATE.*`.
4. You updated:
   - `docs/revisions/CHANGELOG.md`
   - `docs/revisions/DELIVERY_LOG.md`
