# Engineering Report Submission Template

Status: Draft  
Version: v0.1  
Last Updated: 2026-03-01

## 0) Submission Metadata
- Report ID:
- Submission date:
- Project / Unit / Area:
- Discipline(s):
- Prepared by:
- Reviewed by:
- Approval status: `Draft` / `Review` / `Approved`

## 1) Executive Summary
- Objective of this report:
- Key conclusion (1-3 lines):
- Operational decision:
  - `continue`
  - `continue_with_tightened_monitoring`
  - `repair_or_replace_review_required`
  - `blocked_pending_action`

## 2) Scope and Boundary
- Assets/tags covered:
- Time range of data:
- Data sources:
  - design basis
  - inspection history
  - operation condition snapshots
- Out of scope:

## 3) Input Snapshot (Traceable)
Attach or reference:
- input payload file path:
- form preset / mode:
- backend or mock mode:
- standards/profile options selected:

Minimum required fields by discipline should be explicitly listed here.

## 4) Calculation and Verification Summary
### 4.1 Key Metrics Table
| Metric | Value | Unit | Status | Note |
| --- | --- | --- | --- | --- |
| t_min |  | mm |  |  |
| t_current |  | mm |  |  |
| corrosion_rate_selected |  | mm/y |  |  |
| remaining_life |  | years |  |  |
| inspection_interval |  | years |  |  |

Add discipline-specific metrics as needed.

### 4.2 Verification Layer Results
| Layer | Pass/Fail | Critical Issues | Warnings | Evidence |
| --- | --- | --- | --- | --- |
| L1 |  |  |  |  |
| L2 |  |  |  |  |
| L3 |  |  |  |  |
| L4 |  |  |  |  |

### 4.3 Red Flag and Warning Disposition
List each flag and how it was handled:
- Red flags:
  - code:
  - disposition:
  - owner:
  - due date:
- Warnings:
  - code:
  - disposition:
  - owner:
  - due date:

## 5) Standards and Formula Traceability
Reference exact documents and clauses:
- Standard references:
  - ASME/API/IEC/IEEE clause:
  - internal procedure:
- Formula trace source:
  - UI trace section or file path:
- Assumptions and conservative defaults used:

## 6) Engineering Interpretation and Action Plan
### 6.1 Technical Interpretation
- What the numbers mean physically:
- Degradation mechanism hypothesis:
- Confidence and uncertainty:

### 6.2 Recommended Actions
| Priority | Action | Timeline | Owner | Completion Criteria |
| --- | --- | --- | --- | --- |
| High |  |  |  |  |
| Medium |  |  |  |  |
| Low |  |  |  |  |

### 6.3 NDE / Inspection Plan (if applicable)
- Recommended NDE methods:
- Locations/CML/critical zones:
- Proposed inspection cadence:
- Blocking criteria for operation:

## 7) Evidence Attachments
Required attachments:
- exported JSON result
- exported Markdown summary
- screenshots/charts used in interpretation
- command log (how results were generated)
- revision evidence:
  - `docs/revisions/CHANGELOG.md` entry
  - `docs/revisions/DELIVERY_LOG.md` entry

Attachment checklist:
- [ ] JSON attached
- [ ] Markdown attached
- [ ] Flag disposition included
- [ ] Standards references included
- [ ] Action owner/timeline assigned
- [ ] Revision logs updated

## 8) Final Sign-Off
- Technical reviewer:
- Operations reviewer:
- QA/compliance reviewer:
- Final decision:
- Conditional constraints before operation:

## 9) Quick Fill Example (Piping)
- Decision: `continue_with_tightened_monitoring`
- Basis:
  - `t_current` is above `t_min`, but corrosion trend is not flat.
  - no unresolved critical red flag.
  - warning flags are assigned with due dates.
- Action:
  - UT mapping at elbows/reducers in next shutdown window.
  - repeat thickness grid within 3-6 months.
