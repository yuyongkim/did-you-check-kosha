# Sample Engineering Report Submission (Vessel)

Status: Draft  
Version: v0.1  
Last Updated: 2026-03-01

This sample is prepared from `docs/REPORT_SUBMISSION_TEMPLATE.md` for static equipment integrity screening.

## 0) Submission Metadata
- Report ID: `RPT-VES-2026-03-001`
- Submission date: `2026-03-01`
- Project / Unit / Area: `EPC Demo / HCU / Separator Area`
- Discipline(s): `vessel`
- Prepared by: `Static Equipment Team (Demo)`
- Reviewed by: `Lead Mechanical Engineer (Demo)`
- Approval status: `Review`

## 1) Executive Summary
- Objective:
  - Screen shell thickness integrity, external pressure margin, and nozzle reinforcement adequacy.
- Key conclusion:
  - Required shell thickness is below current thickness with positive margin.
  - No critical blocking red flag in this sample run.
  - Continue operation with routine monitoring and next-cycle nozzle area confirmation.
- Operational decision:
  - `continue`

## 2) Scope and Boundary
- Assets/tags covered:
  - `V-2045`
- Time range of data:
  - Current inspection cycle snapshot (2026-Q1)
- Data sources:
  - design pressure-temperature basis
  - in-service thickness reading
  - geometry/nozzle/pad dimensions
- Out of scope:
  - fatigue/fracture mechanics level assessment
  - full external pressure chart method validation package

## 3) Input Snapshot (Traceable)
- input payload path:
  - `outputs/sample/vessel_input_2026-03-01.json`
- form preset / mode:
  - preset: `Horizontal Drum`
- backend or mock mode:
  - `mock`
- standards/profile options:
  - `ASME VIII UG-27`, `UG-28`, `UG-37`, `API 510`

Key inputs:
- material: `SA-516-70`
- vessel_type: `horizontal_drum`
- design_pressure_mpa: `2.0`
- design_temperature_c: `200`
- inside_radius_mm: `750`
- shell_length_mm: `3000`
- head_type: `ellipsoidal_2_1`
- nozzle_od_mm: `350`
- external_pressure_mpa: `0.25`
- joint_efficiency: `0.85`
- t_current_mm: `18`
- corrosion_allowance_mm: `1.5`
- assumed_corrosion_rate_mm_per_year: `0.2`

## 4) Calculation and Verification Summary
### 4.1 Key Metrics Table
| Metric | Value | Unit | Status | Note |
| --- | --- | --- | --- | --- |
| t_required_shell | 11.20 | mm | pass | UG-27 context |
| thickness_margin | 6.80 | mm | pass | current minus required |
| remaining_life | 8.70 | years | pass | positive margin |
| inspection_interval | 4.00 | years | pass | routine cycle |
| external_pressure_utilization | 0.62 | - | pass | below screening threshold |
| nozzle_reinforcement_index | 1.12 | - | pass | above 1.0 screening target |
| slenderness_ld_ratio | 2.00 | - | pass | no high L/D concern |

### 4.2 Verification Layer Results
| Layer | Pass/Fail | Critical Issues | Warnings | Evidence |
| --- | --- | --- | --- | --- |
| L1 (Input/Schema) | Pass | 0 | 0 | payload schema validation |
| L2 (Physics/Calc) | Pass | 0 | 0 | thickness and RL checks |
| L3 (Standards) | Pass | 0 | 0 | UG/API clause mapping |
| L4 (Policy/Cross-check) | Pass | 0 | 0 | release policy screen |

### 4.3 Red Flag and Warning Disposition
- Red flags:
  - none.
- Warnings:
  - none in this sample case.

## 5) Standards and Formula Traceability
- Standard references:
  - ASME VIII UG-27
  - ASME VIII UG-28
  - ASME VIII UG-37
  - API 510
- Formula trace source:
  - UI `Calculation Trace` (vessel run)
  - `docs/standards_index.md`

## 6) Engineering Interpretation and Action Plan
- Technical interpretation:
  - Shell thickness margin is adequate under the current assumptions.
  - External pressure utilization and nozzle index are both within screening acceptance.
- Recommended actions:
  - Confirm nozzle-area local readings in next outage UT campaign.
  - Keep standard interval and monitor corrosion trend continuity.

## 7) Evidence Attachments
- `outputs/sample/vessel_result_2026-03-01.json`
- `outputs/sample/vessel_summary_2026-03-01.md`
- vessel panel screenshots (schematic + stress trend + margin cards)

## 8) Final Sign-Off
- Technical reviewer: `Pending`
- Operations reviewer: `Pending`
- QA/compliance reviewer: `Pending`
- Final decision: `Pending review completion`
