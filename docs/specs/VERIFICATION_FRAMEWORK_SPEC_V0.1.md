# Verification Framework Specification

Status: Draft  
Version: v0.1  
Last Updated: 2026-02-26

## Context Summary
- This specification defines a defense-in-depth validation framework for EPC maintenance calculations across piping/static, rotating, electrical/instrumentation, and steel/civil domains.
- The framework target is high integrity under safety-first constraints: critical calculations within +/-1%, general calculations within +/-3%.
- Validation is modularized into dedicated documents to reduce coupling and support fast debugging.

## Architecture Overview
- 4-layer validation stack:
  - Layer 1: Syntax and format guard
  - Layer 2: MAKER decomposition and K-voting
  - Layer 3: Physics and standards compliance
  - Layer 4: Reverse and historical consistency checks
- Continuous quality loop:
  - Golden dataset benchmark (pre-deployment)
  - Runtime monitoring and alerting
  - Weekly and monthly quality governance

## Detailed Specifications

### 1) Module Bundle (Authoritative)
- `docs/specs/verification/README.md`
- `docs/specs/verification/00_OVERVIEW_AND_ARCHITECTURE_V0.1.md`
- `docs/specs/verification/01_FOUR_LAYER_VALIDATION_V0.1.md`
- `docs/specs/verification/02_MAKER_MULTI_AGENT_V0.1.md`
- `docs/specs/verification/03_GOLDEN_DATASET_V0.1.md`
- `docs/specs/verification/04_RUNTIME_MONITORING_QA_V0.1.md`
- `docs/specs/verification/05_ROADMAP_AND_OPERATIONS_V0.1.md`

### 2) Shared Contracts Dependency
- Message and flag contracts are mandatory dependencies:
  - `docs/specs/shared/MESSAGE_SCHEMA_AND_RED_FLAG_TAXONOMY_V0.1.md`

### 3) Runtime Verification Gates
- `Gate A: Input Integrity`
  - schema validation, unit normalization, range checks
- `Gate B: Consensus Integrity`
  - MAKER decomposition and K-voting pass
- `Gate C: Compliance Integrity`
  - standards reference and physical sanity checks pass
- `Gate D: Causality Integrity`
  - reverse verification and historical consistency pass

Final release is allowed only when all required gates pass.

### 4) Red-Flag Handling Policy
- `critical`: immediate termination + escalation event.
- `high`: block final release and force strict re-validation.
- `medium`: continue with warning and additional checks.
- `low`: log for trend monitoring.

### 5) Human-in-the-Loop Policy
Human review is mandatory when:
- tie-breaker still fails to produce consensus,
- standards references conflict,
- any critical red flag is present,
- historical deviation exceeds tolerance and impacts safety judgment.

### 6) Traceability Requirements
Every validated run must preserve:
- request and response message chain
- assumptions and conservative overrides
- all citations with section/table/page anchors
- red-flag timeline and escalation decisions

### 7) Acceptance and Release Criteria
- Pre-deployment:
  - overall benchmark pass >=99.0%
  - critical false-negative rate = 0
- Runtime compliance:
  - standards reference validation pass = 100%
  - physical sanity pass = 100%
- Dataset readiness:
  - minimum 50 validated cases per discipline before production release of that discipline

## Verification Strategy
- Pre-deployment benchmark runs are mandatory for each discipline release.
- Runtime gate outcomes are persisted for audit and drift analysis.
- Weekly quality review addresses recurring failures and threshold tuning.

## Next Steps
1. Freeze v0.1 gate definitions and escalation criteria.
2. Convert gate logic into implementation contracts under `src/verification/`.
3. Run pilot benchmark and publish discipline-wise gap report.
