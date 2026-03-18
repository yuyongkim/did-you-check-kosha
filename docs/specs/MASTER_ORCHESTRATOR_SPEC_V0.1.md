# Master Orchestrator Specification

Status: Draft  
Version: v0.1  
Last Updated: 2026-02-26

## Context Summary
- The Orchestrator is the control-plane agent for EPC maintenance calculations.
- It converts user input into a disciplined workflow: classify -> retrieve standards -> calculate -> verify -> report.
- It must enforce safety-first, standards-first, and traceability-first behavior across all participating agents.

## Architecture Overview
- Primary responsibilities:
  - Route tasks to correct discipline specialists.
  - Enforce use of shared message schema and red-flag taxonomy.
  - Gate progression between workflow stages using verification outcomes.
- Operates with high reasoning effort and has authority to call all sub-agents.
- Maintains immutable run-level trace context (`correlation_id`, `trace_id`, `workflow_id`).

## Detailed Specifications

### 1) Scope
The Orchestrator governs all standard and emergency calculation workflows for:
- Piping and static equipment
- Rotating equipment
- Electrical and instrumentation
- Steel and civil

It does not perform heavy numerical calculations directly except tie-breaker-level sanity checks.

### 2) Inputs
- User request payload (engineering context and objectives).
- Structured input data (inspection records, process conditions, material specs).
- Optional prior run context for continuation or comparison.

### 3) Core Responsibilities
1. Input readiness and completeness scoring.
2. Discipline classification and multi-discipline dependency detection.
3. Standards applicability matrix generation.
4. Task decomposition and parallel dispatch.
5. Verification gate orchestration and escalation decisioning.
6. Final result assembly with confidence and audit trail.

### 4) Orchestration State Machine
- `received`
- `validated`
- `classified`
- `standards_identified`
- `spec_extracted`
- `calculation_in_progress`
- `verification_in_progress`
- `ready_for_report`
- `completed`
- `escalated`
- `failed`

State transitions are blocked when:
- a critical red flag exists,
- schema validation fails,
- K-consensus is not reached after tie-breaker,
- standards reference integrity fails.

### 5) Standard Workflow (Canonical)
1. `input_validation`
2. `discipline_classification`
3. `standards_identification`
4. `spec_extraction`
5. `parallel_calculation`
6. `cross_verification`
7. `final_validation`
8. `report_generation`

### 6) Emergency Workflow (Fast Track)
Used when critical conditions are detected (for example, very low remaining life or severe vibration breach).
- Restrict execution to impacted discipline(s).
- Force strict thresholds and conservative assumptions.
- Require mandatory escalation package in final output.

### 7) Decision Rules
- Default to conservative assumptions when uncertainty exists and log each assumption.
- Never infer missing mandatory safety data silently.
- Any standards ambiguity must produce explicit user-facing warning and verification hold.

### 8) Delegation Rules
- Spec retrieval only through `spec_explorer` interface.
- Heavy calculations only through specialist and/or `calculator_worker`.
- Verification authority centralized through `verification_agent` and verification gates.

### 9) Output Contract
The orchestrator must emit:
- Calculation summary by discipline.
- Standards references used per step.
- Verification status and confidence level.
- Red flags, warnings, and escalation actions.
- Full trace metadata.

### 10) Message Contract Dependency
All communication must conform to:
- `docs/specs/shared/MESSAGE_SCHEMA_AND_RED_FLAG_TAXONOMY_V0.1.md`

### 11) Human Escalation Triggers
- Critical red flag raised.
- No consensus after tie-breaker.
- Invalid standards reference in final output.
- Missing mandatory input fields after retry cycle.

## Verification Strategy
- Pre-dispatch checks: schema, units, and minimal context completeness.
- Mid-flow checks: stage-level red-flag scan after every major step.
- Pre-report checks: all required verification artifacts present.
- Post-run checks: traceability package integrity and reproducibility markers.

## Next Steps
1. Align agent-level contracts in Multi-Agent Configuration Spec.
2. Bind this state machine to workflow contracts in `src/workflows/` during implementation.
3. Add runbook examples for normal and emergency orchestration paths.
