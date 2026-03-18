# Sample Engineering Report Submission (Electrical)

Status: Draft  
Version: v0.1  
Last Updated: 2026-03-01

This sample is prepared from `docs/REPORT_SUBMISSION_TEMPLATE.md` for electrical integrity screening.

## 0) Submission Metadata
- Report ID: `RPT-ELE-2026-03-001`
- Submission date: `2026-03-01`
- Project / Unit / Area: `EPC Demo / Substation S-13.8kV / Switch Room`
- Discipline(s): `electrical`
- Prepared by: `Electrical Reliability Team (Demo)`
- Reviewed by: `Lead Electrical Engineer (Demo)`
- Approval status: `Review`

## 1) Executive Summary
- Objective:
  - Screen transformer health, arc-flash exposure, fault-current margin, and power quality.
- Key conclusion:
  - Health index remains in acceptable range.
  - Fault current is below breaker interrupting rating.
  - Arc-flash energy indicates controlled work planning and PPE management are required.
- Operational decision:
  - `continue_with_tightened_monitoring`

## 2) Scope and Boundary
- Assets/tags covered:
  - `TR-13A`
  - `SWGR-13.8-01`
- Time range of data:
  - current quarter condition snapshot
- Data sources:
  - electrical short-circuit data
  - breaker rating and protection settings
  - oil/DGA/insulation condition scores
- Out of scope:
  - full protection coordination study update
  - detailed harmonic source tracing

## 3) Input Snapshot (Traceable)
- input payload path:
  - `outputs/sample/electrical_input_2026-03-01.json`
- form preset / mode:
  - preset: `Transformer Normal`
- backend or mock mode:
  - `mock`
- standards/profile options:
  - `IEEE C57.104`, `IEEE 1584-2018`, `NFPA 70E`

Key inputs:
- equipment_type: `transformer`
- system_voltage_kv: `13.8`
- bolted_fault_current_ka: `22`
- clearing_time_sec: `0.2`
- working_distance_mm: `455`
- breaker_interrupt_rating_ka: `31.5`
- voltage_drop_percent: `3.2`
- thd_voltage_percent: `4.8`
- dga_score: `8.2`
- oil_quality_score: `7.9`
- insulation_score: `8.3`
- load_factor_score: `7.5`

## 4) Calculation and Verification Summary
### 4.1 Key Metrics Table
| Metric | Value | Unit | Status | Note |
| --- | --- | --- | --- | --- |
| transformer_health_index | 7.8 | /10 | pass | healthy range |
| arc_flash_energy | 11.5 | cal/cm2 | monitor | controlled-work/PPE management needed |
| ppe_category | 3 | category | monitor | per screen result |
| fault_current | 22.0 | kA | pass | below breaker rating |
| breaker_interrupt_rating | 31.5 | kA | pass | margin available |
| voltage_drop | 3.2 | % | pass | below high-alert threshold |
| inspection_interval | 2.0 | years | pass | base cycle |

### 4.2 Verification Layer Results
| Layer | Pass/Fail | Critical Issues | Warnings | Evidence |
| --- | --- | --- | --- | --- |
| L1 (Input/Schema) | Pass | 0 | 0 | payload schema validation |
| L2 (Physics/Calc) | Pass | 0 | 0 | HI/arc/fault computations |
| L3 (Standards) | Pass | 0 | 0 | IEEE/NFPA references mapped |
| L4 (Policy/Cross-check) | Pass | 0 | 0 | release policy screen |

### 4.3 Red Flag and Warning Disposition
- Red flags:
  - none.
- Warnings:
  - none in this sample case.

## 5) Standards and Formula Traceability
- Standard references:
  - IEEE C57.104
  - IEEE 1584-2018
  - NFPA 70E
- Formula trace source:
  - UI `Calculation Trace` (electrical run)
  - `docs/standards_index.md`

## 6) Engineering Interpretation and Action Plan
- Technical interpretation:
  - No immediate interrupting-capacity mismatch is indicated.
  - Arc-flash level is not critical in this sample but remains operationally significant.
- Recommended actions:
  - Maintain current interval and PPE/job-planning controls.
  - Keep harmonics and condition scores trended in routine review.

## 7) Evidence Attachments
- `outputs/sample/electrical_result_2026-03-01.json`
- `outputs/sample/electrical_summary_2026-03-01.md`
- electrical panel screenshots (arc/HI cards + quality chart)

## 8) Final Sign-Off
- Technical reviewer: `Pending`
- Operations reviewer: `Pending`
- QA/compliance reviewer: `Pending`
- Final decision: `Pending review completion`
