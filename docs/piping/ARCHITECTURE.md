# Piping System Architecture

## Scope
This architecture covers piping maintenance calculations and verification for ASME B31.3 and API 570/510 aligned workflows.

## Core Calculation Coverage
- Minimum required thickness:
  - `t_min = (P*D)/(2*(S*E + P*Y)) + CA`
  - Reference: ASME B31.3 Para 304.1.2
- Allowable stress lookup and interpolation:
  - Reference: ASME B31.3 Table A-1 (edition verification required)
- Corrosion rate (long-term / short-term selection):
  - Reference: API 570 corrosion assessment method
- Remaining life:
  - `RL = (t_current - t_min)/CR_selected`
- Inspection interval policy:
  - Reference: API 570 Section 7
- Hydrotest chloride checks:
  - Carbon steel <= 250 ppm, stainless <= 30 ppm

## 4-Layer Verification
1. Layer 1 Input Guard:
   - Required field and schema checks
   - Unit/range checks
   - Material support checks
2. Layer 2 MAKER Consensus:
   - 3 independent calculation paths
   - 1% relative tolerance threshold
   - Tie-breaker median logic
3. Layer 3 Physics/Standards Compliance:
   - Red-flag triggers for unsafe or out-of-scope conditions
4. Layer 4 Reverse Validation:
   - Back-calculate initial thickness and design pressure
   - 5% deviation warning threshold

## Runtime Architecture
- Orchestrator receives message envelope and dispatches to runtime agent.
- Piping specialist agent invokes `PipingVerificationService`.
- Service emits structured outputs:
  - `calculation_summary`
  - `layer_results`
  - `final_results`
  - `flags`
  - `recommendations`

## Data and Artifacts
- Golden dataset:
  - `datasets/golden_standards/piping_golden_dataset_v1.json`
- Verification report:
  - `docs/piping/VERIFICATION_REPORT.json`
  - `docs/piping/VERIFICATION_REPORT.md`

## Production Constraints
- Standards references in code and output are mandatory.
- Critical red flags are fail-closed (release blocked).
- Edition-specific values must be re-validated before production signoff.
