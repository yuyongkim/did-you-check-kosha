# Sample Engineering Report Submission (Civil)

Status: Draft  
Version: v0.1  
Last Updated: 2026-03-01

This sample is prepared from `docs/REPORT_SUBMISSION_TEMPLATE.md` for civil/concrete integrity screening.

## 0) Submission Metadata
- Report ID: `RPT-CIV-2026-03-001`
- Submission date: `2026-03-01`
- Project / Unit / Area: `EPC Demo / Pipe Support Foundation / Zone-C`
- Discipline(s): `civil`
- Prepared by: `Civil Integrity Team (Demo)`
- Reviewed by: `Senior Civil Engineer (Demo)`
- Approval status: `Review`

## 1) Executive Summary
- Objective:
  - Screen concrete flexural margin and durability progression indicators.
- Key conclusion:
  - Flexural D/C remains below unity in this sample.
  - No substantial-damage trigger is indicated.
  - Carbonation depth remains below cover thickness.
- Operational decision:
  - `continue`

## 2) Scope and Boundary
- Assets/tags covered:
  - `FDN-C-14`
- Time range of data:
  - current inspection campaign snapshot
- Data sources:
  - material and section input set
  - crack/spalling/settlement observations
  - carbonation parameter set
- Out of scope:
  - geotechnical deep-dive reassessment
  - full retrofit design package

## 3) Input Snapshot (Traceable)
- input payload path:
  - `outputs/sample/civil_input_2026-03-01.json`
- form preset / mode:
  - preset: `Beam Normal`
- backend or mock mode:
  - `mock`
- standards/profile options:
  - `ACI 318`, `ACI 562`

Key inputs:
- element_type: `beam`
- environment_exposure: `outdoor_urban`
- fc_mpa: `35`
- fy_mpa: `420`
- width_mm: `300`
- effective_depth_mm: `550`
- rebar_area_mm2: `2450`
- demand_moment_knm: `280`
- service_years: `18`
- cover_thickness_mm: `40`
- carbonation_coeff_mm_sqrt_year: `1.8`
- crack_width_mm: `0.22`
- spalling_area_percent: `5`
- foundation_settlement_mm: `8`

## 4) Calculation and Verification Summary
### 4.1 Key Metrics Table
| Metric | Value | Unit | Status | Note |
| --- | --- | --- | --- | --- |
| dc_ratio | 0.78 | - | pass | flexural demand below capacity |
| carbonation_depth | 9.5 | mm | pass | below cover thickness |
| years_to_corrosion_init | 34 | years | pass | positive durability horizon |
| substantial_damage | false | boolean | pass | no ACI 562 trigger |
| inspection_interval | 2.0 | years | pass | normal cycle |
| crack_width | 0.22 | mm | pass | below high-risk threshold |

### 4.2 Verification Layer Results
| Layer | Pass/Fail | Critical Issues | Warnings | Evidence |
| --- | --- | --- | --- | --- |
| L1 (Input/Schema) | Pass | 0 | 0 | payload schema validation |
| L2 (Physics/Calc) | Pass | 0 | 0 | D/C and durability checks |
| L3 (Standards) | Pass | 0 | 0 | ACI references mapped |
| L4 (Policy/Cross-check) | Pass | 0 | 0 | release policy screen |

### 4.3 Red Flag and Warning Disposition
- Red flags:
  - none.
- Warnings:
  - none in this sample case.

## 5) Standards and Formula Traceability
- Standard references:
  - ACI 318 flexural capacity context
  - ACI 562 substantial damage criteria
- Formula trace source:
  - UI `Calculation Trace` (civil run)
  - `docs/standards_index.md`

## 6) Engineering Interpretation and Action Plan
- Technical interpretation:
  - Structural and durability screens are currently acceptable in this sample.
  - Continue periodic monitoring to confirm no acceleration of damage indicators.
- Recommended actions:
  - Keep routine inspection interval.
  - Re-screen early if crack/spalling/settlement trend worsens.

## 7) Evidence Attachments
- `outputs/sample/civil_result_2026-03-01.json`
- `outputs/sample/civil_summary_2026-03-01.md`
- civil panel screenshots (damage cards + trend context)

## 8) Final Sign-Off
- Technical reviewer: `Pending`
- Operations reviewer: `Pending`
- QA/compliance reviewer: `Pending`
- Final decision: `Pending review completion`
