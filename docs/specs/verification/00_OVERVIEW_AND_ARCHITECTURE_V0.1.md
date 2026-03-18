# Verification Architecture Overview

Status: Draft  
Version: v0.1  
Last Updated: 2026-02-26

## Mission
Design a validation system that assures calculation integrity for EPC maintenance workflows using a 4-layer defense model.

## Coverage
- Piping and static equipment (ASME B31.3, API 570, API 510)
- Rotating equipment (API 610, API 617, API 670)
- Electrical and instrumentation (IEEE 3000 series)
- Steel and civil (AISC 360, ACI 318)

## Top-Level Flow
1. Input normalization and schema validation.
2. MAKER-based decomposition and multi-agent consensus.
3. Standards and physical sanity verification.
4. Reverse and historical consistency verification.
5. Verified report generation with confidence and audit trail.

## Architectural Principles
- Standards-first: no unsupported formula or extrapolation without explicit exception handling.
- Fail-closed safety posture: stop automation when critical risk is detected.
- Full traceability: preserve inputs, assumptions, references, and intermediate values.
- Modular governance: separate verification concerns into independent specs.

## Required Outputs
- Validation result with severity classification.
- Confidence level and consensus metadata.
- Structured red-flag and warning list.
- Actionable escalation recommendation.
