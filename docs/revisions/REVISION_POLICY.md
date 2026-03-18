# Revision Policy

Status: Draft  
Version: v0.1  
Last Updated: 2026-02-27

## Scope
This policy applies to all documents in `docs/` and to architecture-impacting code changes.

## Revision Levels
- `major`:
  - Changes architecture, safety rules, verification gates, or core workflows.
  - Requires explicit approval before implementation.
- `minor`:
  - Adds or refines sections without changing core decisions.
- `patch`:
  - Editorial fixes, typo corrections, formatting only.

## Change Workflow
1. Open or update relevant spec/plan doc in `docs/specs/` or `docs/plans/`.
2. Add an entry to `docs/revisions/CHANGELOG.md`.
3. Add a completion record entry to `docs/revisions/DELIVERY_LOG.md` when work is finished.
4. If architecture changed, include:
   - reason for change
   - impacted modules
   - migration or compatibility note
5. Move document status (`Draft` -> `Review` -> `Approved`) when validated.

Recommended command (single-step logging to both files):
- `python scripts/log_completion.py --version <tag> --title "<title>" --scope "<scope>"`

## Naming Conventions
- Plan documents: `PROJECT_PLAN_VX.Y.md`
- Spec documents: `<DOMAIN>_SPEC_VX.Y.md`
- Optional dated supplements: `YYYY-MM-DD_<topic>.md`

## Traceability Requirements
Each major decision should include:
- Decision statement
- Alternatives considered
- Risk impact
- Verification impact

## Mandatory Final MD Record (Required)
When a task/round is marked complete, the following Markdown records are mandatory:
1. `docs/revisions/CHANGELOG.md`:
   - version/date
   - what changed
   - impacted files/modules
2. `docs/revisions/DELIVERY_LOG.md`:
   - completion timestamp
   - scope summary
   - verification commands and pass/fail
   - open risks/next actions

No completion is considered valid unless both records are updated.
