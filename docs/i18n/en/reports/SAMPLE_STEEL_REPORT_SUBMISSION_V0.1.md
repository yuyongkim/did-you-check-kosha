# Sample Engineering Report Submission (Steel)

Status: Draft  
Version: v0.1  
Last Updated: 2026-03-01

This sample is prepared from `docs/REPORT_SUBMISSION_TEMPLATE.md` for steel-structure screening.

## 0) Submission Metadata
- Report ID: `RPT-STL-2026-03-001`
- Submission date: `2026-03-01`
- Project / Unit / Area: `EPC Demo / Pipe Rack / Bay-3`
- Discipline(s): `steel`
- Prepared by: `Structural Integrity Team (Demo)`
- Reviewed by: `Lead Structural Engineer (Demo)`
- Approval status: `Review`

## 1) Executive Summary
- Objective:
  - Screen demand-capacity ratio, section-loss impact, and serviceability indicators.
- Key conclusion:
  - D/C ratio is below unity with acceptable margin.
  - Corrosion section loss remains moderate in this sample.
  - No critical structural red flag triggered.
- Operational decision:
  - `continue`

## 2) Scope and Boundary
- Assets/tags covered:
  - `PR-B3-COL-07`
- Time range of data:
  - latest inspection cycle snapshot
- Data sources:
  - member geometry and material grade
  - demand inputs from load combination output
  - corrosion and deflection field observations
- Out of scope:
  - full nonlinear frame analysis
  - connection redesign package

## 3) Input Snapshot (Traceable)
- input payload path:
  - `outputs/sample/steel_input_2026-03-01.json`
- form preset / mode:
  - preset: `Column Normal`
- backend or mock mode:
  - `mock`
- standards/profile options:
  - `AISC 360 Chapter E`, serviceability guidance

Key inputs:
- member_type: `column`
- steel_grade: `a572_gr50`
- section_label: `W310x60`
- length_m: `6.0`
- k_factor: `1.0`
- radius_of_gyration_mm: `90`
- gross_area_mm2: `7600`
- axial_demand_kn: `650`
- corrosion_loss_percent: `8`
- deflection_mm: `10`
- span_mm: `6000`

## 4) Calculation and Verification Summary
### 4.1 Key Metrics Table
| Metric | Value | Unit | Status | Note |
| --- | --- | --- | --- | --- |
| dc_ratio | 0.82 | - | pass | below unity |
| lambda_c | 0.72 | - | pass | stable compression regime |
| phi_pn | 790 | kN | pass | capacity above demand |
| corrosion_loss | 8.0 | % | pass | moderate section loss |
| deflection_ratio | 0.45 | - | pass | serviceability screen acceptable |
| inspection_interval | 2.0 | years | pass | normal cycle |

### 4.2 Verification Layer Results
| Layer | Pass/Fail | Critical Issues | Warnings | Evidence |
| --- | --- | --- | --- | --- |
| L1 (Input/Schema) | Pass | 0 | 0 | payload schema validation |
| L2 (Physics/Calc) | Pass | 0 | 0 | capacity/serviceability calc |
| L3 (Standards) | Pass | 0 | 0 | AISC references mapped |
| L4 (Policy/Cross-check) | Pass | 0 | 0 | release policy screen |

### 4.3 Red Flag and Warning Disposition
- Red flags:
  - none.
- Warnings:
  - none in this sample case.

## 5) Standards and Formula Traceability
- Standard references:
  - AISC 360 Chapter E
  - AISC serviceability deflection guidance
- Formula trace source:
  - UI `Calculation Trace` (steel run)
  - `docs/standards_index.md`

## 6) Engineering Interpretation and Action Plan
- Technical interpretation:
  - No over-utilization signal in this sample.
  - Corrosion and deflection indicators are currently manageable.
- Recommended actions:
  - Maintain current interval and continue corrosion trend tracking.
  - Re-screen if new load case or section-loss increase is observed.

## 7) Evidence Attachments
- `outputs/sample/steel_result_2026-03-01.json`
- `outputs/sample/steel_summary_2026-03-01.md`
- steel panel screenshots (member schematic + D/C cards)

## 8) Final Sign-Off
- Technical reviewer: `Pending`
- Operations reviewer: `Pending`
- QA/compliance reviewer: `Pending`
- Final decision: `Pending review completion`
