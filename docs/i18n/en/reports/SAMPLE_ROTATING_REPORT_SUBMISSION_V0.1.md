# Sample Engineering Report Submission (Rotating)

Status: Draft  
Version: v0.1  
Last Updated: 2026-03-01

This sample is prepared from `docs/REPORT_SUBMISSION_TEMPLATE.md` for rotating-equipment reliability screening.

## 0) Submission Metadata
- Report ID: `RPT-ROT-2026-03-001`
- Submission date: `2026-03-01`
- Project / Unit / Area: `EPC Demo / Utilities / Pump House`
- Discipline(s): `rotating`
- Prepared by: `Rotating Reliability Team (Demo)`
- Reviewed by: `Principal Rotating Engineer (Demo)`
- Approval status: `Review`

## 1) Executive Summary
- Objective:
  - Assess vibration, process stability, and protection readiness for a pump train.
- Key conclusion:
  - Vibration and nozzle-load are below adjusted limits.
  - API 670 readiness and trip-test evidence are adequate for this sample case.
  - No unresolved critical red flag.
- Operational decision:
  - `continue`

## 2) Scope and Boundary
- Assets/tags covered:
  - `P-3301A`
- Time range of data:
  - current condition snapshot with latest monthly review
- Data sources:
  - condition monitoring trend
  - operating pressure/speed values
  - protection coverage and trip-test records
- Out of scope:
  - rotor dynamic simulation
  - full root-cause analysis of historical events

## 3) Input Snapshot (Traceable)
- input payload path:
  - `outputs/sample/rotating_input_2026-03-01.json`
- form preset / mode:
  - preset: `Pump Normal`
- backend or mock mode:
  - `mock`
- standards/profile options:
  - `API 610`, `API 670`, `ISO 20816-3`

Key inputs:
- machine_type: `pump`
- driver_type: `electric_motor_fixed`
- service_criticality: `normal`
- vibration_mm_per_s: `2.5`
- nozzle_load_ratio: `0.85`
- bearing_temperature_c: `72`
- lube_oil_supply_temp_c: `56`
- speed_rpm: `1800`
- npsh_available_m: `5.6`
- npsh_required_m: `3.8`
- api670_coverage_pct: `96`
- trip_tests_last_12m: `4`
- protection_bypass_active: `false`

## 4) Calculation and Verification Summary
### 4.1 Key Metrics Table
| Metric | Value | Unit | Status | Note |
| --- | --- | --- | --- | --- |
| vibration | 2.50 | mm/s | pass | below adjusted limit |
| adjusted_vibration_limit | 3.00 | mm/s | pass | machine/driver/criticality adjusted |
| nozzle_load_ratio | 0.85 | - | pass | below limit ratio 1.0 |
| mechanical_integrity_index | 8.5 | /10 | pass | healthy zone |
| process_stability_index | 8.9 | /10 | pass | stable process behavior |
| protection_readiness_index | 8.8 | /10 | pass | sufficient protection readiness |
| inspection_interval | 2.0 | years | pass | normal cycle |

### 4.2 Verification Layer Results
| Layer | Pass/Fail | Critical Issues | Warnings | Evidence |
| --- | --- | --- | --- | --- |
| L1 (Input/Schema) | Pass | 0 | 0 | payload schema validation |
| L2 (Physics/Calc) | Pass | 0 | 0 | index/limit calculations |
| L3 (Standards) | Pass | 0 | 0 | API/ISO references mapped |
| L4 (Policy/Cross-check) | Pass | 0 | 0 | release policy screen |

### 4.3 Red Flag and Warning Disposition
- Red flags:
  - none.
- Warnings:
  - none in this sample case.

## 5) Standards and Formula Traceability
- Standard references:
  - API 610
  - API 670
  - ISO 20816-3
- Formula trace source:
  - UI `Calculation Trace` (rotating run)
  - `docs/standards_index.md`

## 6) Engineering Interpretation and Action Plan
- Technical interpretation:
  - Current condition is inside screening acceptance for mechanical/process/protection dimensions.
  - NPSH margin is positive; no immediate cavitation screen alert in this sample.
- Recommended actions:
  - Maintain normal monitoring cadence.
  - Keep trip-test evidence and protection bypass controls up to date.

## 7) Evidence Attachments
- `outputs/sample/rotating_result_2026-03-01.json`
- `outputs/sample/rotating_summary_2026-03-01.md`
- rotating panel screenshots (spectrum + matrix + risk panel)

## 8) Final Sign-Off
- Technical reviewer: `Pending`
- Operations reviewer: `Pending`
- QA/compliance reviewer: `Pending`
- Final decision: `Pending review completion`
