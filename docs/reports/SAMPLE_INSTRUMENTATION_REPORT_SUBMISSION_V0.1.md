# Sample Engineering Report Submission (Instrumentation)

Status: Draft  
Version: v0.1  
Last Updated: 2026-03-01

This sample is prepared from `docs/REPORT_SUBMISSION_TEMPLATE.md` for instrumentation and SIS screening.

## 0) Submission Metadata
- Report ID: `RPT-INS-2026-03-001`
- Submission date: `2026-03-01`
- Project / Unit / Area: `EPC Demo / Reactor Train / SIS Loop B`
- Discipline(s): `instrumentation`
- Prepared by: `I&C Integrity Team (Demo)`
- Reviewed by: `Senior SIS Engineer (Demo)`
- Approval status: `Review`

## 1) Executive Summary
- Objective:
  - Validate SIL target margin, drift behavior, and calibration interval suitability.
- Key conclusion:
  - Achieved SIL is above target in this sample.
  - Predicted drift is below tolerance.
  - Calibration interval remains acceptable with trend tracking.
- Operational decision:
  - `continue`

## 2) Scope and Boundary
- Assets/tags covered:
  - `PT-4402`
  - associated SIF loop reference: `SIF-B-102`
- Time range of data:
  - calibration trend window (0 to 270 days)
- Data sources:
  - calibration history
  - reliability parameters (failure rate, proof interval, MTTR)
  - architecture target data
- Out of scope:
  - full SRS redesign
  - detailed field wiring diagnostics

## 3) Input Snapshot (Traceable)
- input payload path:
  - `outputs/sample/instrumentation_input_2026-03-01.json`
- form preset / mode:
  - preset: `PT Normal`
- backend or mock mode:
  - `mock`
- standards/profile options:
  - `IEC 61511`, `ISA-TR84.00.02`, `ISO GUM`

Key inputs:
- instrument_type: `pressure_transmitter`
- voting_architecture: `1oo1`
- sil_target: `2`
- failure_rate_per_hour: `1.0e-7`
- proof_test_interval_hours: `8760`
- mttr_hours: `8`
- calibration_interval_days: `180`
- tolerance_pct: `1.0`

## 4) Calculation and Verification Summary
### 4.1 Key Metrics Table
| Metric | Value | Unit | Status | Note |
| --- | --- | --- | --- | --- |
| pfdavg | 0.00044 | - | pass | below SIL-2 limit |
| sil_target | 2 | level | pass | target set |
| sil_achieved | 3 | level | pass | target met with margin |
| predicted_drift | 0.38 | % | pass | below tolerance |
| calibration_interval_optimal | 220 | days | pass | near current interval |
| combined_uncertainty | 0.37 | % | pass | within expected range |

### 4.2 Verification Layer Results
| Layer | Pass/Fail | Critical Issues | Warnings | Evidence |
| --- | --- | --- | --- | --- |
| L1 (Input/Schema) | Pass | 0 | 0 | payload schema validation |
| L2 (Physics/Calc) | Pass | 0 | 0 | pfd/drift interval calculations |
| L3 (Standards) | Pass | 0 | 0 | IEC/ISA references mapped |
| L4 (Policy/Cross-check) | Pass | 0 | 0 | release policy screen |

### 4.3 Red Flag and Warning Disposition
- Red flags:
  - none.
- Warnings:
  - none in this sample case.

## 5) Standards and Formula Traceability
- Standard references:
  - IEC 61511
  - ISA-TR84.00.02
  - ISO GUM
- Formula trace source:
  - UI `Calculation Trace` (instrumentation run)
  - `docs/standards_index.md`

## 6) Engineering Interpretation and Action Plan
- Technical interpretation:
  - SIL margin and drift trend support continued operation under current assumptions.
  - Continue trend-based calibration governance to keep early warning visibility.
- Recommended actions:
  - Maintain current interval while monitoring drift fit quality.
  - Re-evaluate immediately if drift slope or process disturbance changes.

## 7) Evidence Attachments
- `outputs/sample/instrumentation_result_2026-03-01.json`
- `outputs/sample/instrumentation_summary_2026-03-01.md`
- instrumentation panel screenshots (drift trend + SIL cards)

## 8) Final Sign-Off
- Technical reviewer: `Pending`
- Operations reviewer: `Pending`
- QA/compliance reviewer: `Pending`
- Final decision: `Pending review completion`
