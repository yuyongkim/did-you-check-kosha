# Sample Engineering Report Submission (Piping)

Status: Draft  
Version: v0.1  
Last Updated: 2026-03-01

This is a sample-filled document based on `docs/REPORT_SUBMISSION_TEMPLATE.md`.
Use it as a reference format, then replace all values with your real project case.

## 0) Submission Metadata
- Report ID: `RPT-PIP-2026-03-001`
- Submission date: `2026-03-01`
- Project / Unit / Area: `EPC Demo / CDU-2 / Pipe Rack A`
- Discipline(s): `piping`
- Prepared by: `Process Integrity Team (Demo)`
- Reviewed by: `Senior Mechanical Engineer (Demo)`
- Approval status: `Review`

## 1) Executive Summary
- Objective of this report:
  - Evaluate piping wall-thickness integrity and define short-term inspection action.
- Key conclusion:
  - Current thickness remains above minimum required thickness.
  - No unresolved critical red flag was identified in this screening run.
  - Corrosion trend exists; monitoring density should be increased at hotspots.
- Operational decision:
  - `continue_with_tightened_monitoring`

## 2) Scope and Boundary
- Assets/tags covered:
  - `10"-P-2045-CS-001`
  - `6"-P-2045-CS-009`
- Time range of data:
  - 2015-01-01 to 2025-01-01
- Data sources:
  - design basis sheet (pressure/temperature/material)
  - UT thickness history from periodic inspection records
  - operating fluid classification from process data
- Out of scope:
  - branch connection stress analysis
  - full API 579 level assessment
  - insulation-off CUI campaign result integration

## 3) Input Snapshot (Traceable)
Attach or reference:
- input payload file path:
  - `frontend` run payload export (example): `outputs/sample/piping_input_2026-03-01.json`
- form preset / mode:
  - preset: `General CS`
- backend or mock mode:
  - `mock`
- standards/profile options selected:
  - `ASME B31.3 Para 304.1.2`, `Table A-1`, `API 570 Section 7`
  - temperature profile: `strict_process`

Key input snapshot:
- material: `SA-106 Gr.B`
- nps: `6`
- design_pressure_mpa: `4.5`
- design_temperature_c: `250`
- weld_type: `seamless`
- service_type: `general`
- fluid_type: `hydrocarbon_dry`
- chloride_ppm: `120`
- thickness_history:
  - 2015-01-01: 10.00 mm
  - 2020-01-01: 8.60 mm
  - 2025-01-01: 7.30 mm

## 4) Calculation and Verification Summary
### 4.1 Key Metrics Table
| Metric | Value | Unit | Status | Note |
| --- | --- | --- | --- | --- |
| t_min | 5.10 | mm | pass | minimum required thickness threshold |
| t_current | 7.30 | mm | pass | current measured thickness |
| corrosion_rate_selected | 0.340 | mm/y | monitor | active thinning trend |
| remaining_life | 6.20 | years | monitor | still positive margin |
| inspection_interval | 3.00 | years | tighten | hotspot-focused campaign recommended |
| allowable_stress | 110.0 | MPa | pass | table-based lookup at design temperature |
| temperature_limit_mode | within_conservative_limit | - | pass | no temperature over-limit trigger |

### 4.2 Verification Layer Results
| Layer | Pass/Fail | Critical Issues | Warnings | Evidence |
| --- | --- | --- | --- | --- |
| L1 (Input/Schema) | Pass | 0 | 0 | payload schema validation log |
| L2 (Physics/Calc) | Pass | 0 | 1 | trace and trend consistency review |
| L3 (Standards) | Pass | 0 | 0 | clause-reference checks |
| L4 (Cross-check/Policy) | Pass | 0 | 0 | release rule screen |

### 4.3 Red Flag and Warning Disposition
- Red flags:
  - none in this sample case.
- Warnings:
  - code: `DATA.CORROSION_ALLOWANCE_DEFAULTED_1P5MM`
  - disposition: accepted for screening run; set explicit CA in next formal run
  - owner: piping integrity engineer
  - due date: 2026-03-15

## 5) Standards and Formula Traceability
Standard references:
- ASME B31.3 Para 304.1.2 (minimum thickness context)
- ASME B31.3 Table A-1 (allowable stress)
- API 570 Section 7 (inspection interval and corrosion-rate context)

Formula trace source:
- UI `Calculation Trace` panel for piping run
- supporting docs:
  - `docs/standards_index.md`
  - `docs/specs/shared/MESSAGE_SCHEMA_AND_RED_FLAG_TAXONOMY_V0.1.md`

Assumptions and conservative defaults:
- corrosion allowance default handling used in this sample
- strict temperature profile applied
- trend interpreted as screening-level, not fitness-for-service replacement

## 6) Engineering Interpretation and Action Plan
### 6.1 Technical Interpretation
- Current thickness margin exists (`t_current > t_min`), so immediate replacement is not indicated by this screening.
- Corrosion progression is present and not flat; localized thinning risk remains at elbows/reducers and low points.
- Confidence:
  - medium-high for screening decision
  - lower for local-damage distribution without expanded UT map coverage

### 6.2 Recommended Actions
| Priority | Action | Timeline | Owner | Completion Criteria |
| --- | --- | --- | --- | --- |
| High | Execute UT CML recheck at top-risk locations | within 1 month | Piping Integrity | updated thickness records uploaded |
| Medium | Perform targeted PAUT/UT mapping at elbows/reducers | within 3 months | NDE Team | hotspot map and anomaly disposition issued |
| Low | Normalize corrosion allowance entry in input governance | within 1 month | Data Steward | form/payload includes explicit CA value |

### 6.3 NDE / Inspection Plan
- Recommended NDE methods:
  - UT Thickness (CML grid)
  - PAUT / UT mapping (targeted)
  - MT at selected weld toe areas (as needed)
- Locations/CML/critical zones:
  - downstream of control valve
  - elbow intrados/extrados
  - low-point drain vicinity
  - dead-leg branch
- Proposed inspection cadence:
  - targeted follow-up in 3-6 months
  - base interval maintained with hotspot campaign overlay
- Blocking criteria for operation:
  - any point thickness at or below `t_min`
  - new critical flag (`PHY.THICKNESS_BELOW_MINIMUM`, `PHY.REMAINING_LIFE_CRITICAL`, etc.)

## 7) Evidence Attachments
Required attachments:
- exported JSON result:
  - `outputs/sample/piping_result_2026-03-01.json`
- exported Markdown summary:
  - `outputs/sample/piping_summary_2026-03-01.md`
- screenshots/charts:
  - pipe cross-section
  - trend chart with `t_min` line
  - NDE recommendation panel snapshot
- command log:
  - `npm --prefix frontend run dev`
  - run from UI: piping preset `General CS`
- revision evidence:
  - `docs/revisions/CHANGELOG.md` entry
  - `docs/revisions/DELIVERY_LOG.md` entry

Attachment checklist:
- [x] JSON attached
- [x] Markdown attached
- [x] Flag disposition included
- [x] Standards references included
- [x] Action owner/timeline assigned
- [x] Revision logs updated

## 8) Final Sign-Off
- Technical reviewer: `Pending`
- Operations reviewer: `Pending`
- QA/compliance reviewer: `Pending`
- Final decision: `Pending review completion`
- Conditional constraints before operation:
  - complete hotspot UT mapping campaign
  - close warning action item for explicit CA input

