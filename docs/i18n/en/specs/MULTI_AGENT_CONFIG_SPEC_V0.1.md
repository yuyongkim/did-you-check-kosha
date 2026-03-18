# Multi-Agent Configuration Specification

Status: Draft  
Version: v0.1  
Last Updated: 2026-02-26

## Context Summary
- This document defines configuration-level contracts for the 11-agent EPC maintenance system.
- It is a design specification for `config.toml` structure and field semantics, not a final runtime file.
- Message and escalation behavior must be consistent with the shared contract specification.

## Architecture Overview
- Agent topology:
  - 1 orchestrator
  - 1 spec explorer
  - 7 discipline specialists
  - 1 calculator worker
  - 1 verification agent
- Execution pattern:
  - orchestrator-led, specialist-parallel, verification-gated
- Core constraints:
  - explicit standards traceability
  - conservative safety behavior
  - deterministic escalation policy

## Detailed Specifications

### 1) Global Settings Model
Required top-level sections:
- `[system]`
- `[models]`
- `[timeouts]`
- `[verification]`
- `[logging]`
- `[security]`

#### 1.1 Required Fields
- `[system]`
  - `max_threads` (int)
  - `max_depth` (int)
  - `default_workflow` (string)
  - `default_model` (string)
- `[timeouts]`
  - `default_agent_timeout_sec` (int)
  - `spec_lookup_timeout_sec` (int)
  - `verification_timeout_sec` (int)
- `[verification]`
  - `golden_dataset_path` (string)
  - `maker_voting_threshold` (int)
  - `red_flag_auto_escalation` (bool)
  - `critical_fail_closed` (bool)
- `[logging]`
  - `level` (enum)
  - `audit_trail_enabled` (bool)
  - `trace_retention_days` (int)

### 2) Agent Definitions
Every agent entry must define:
- `description`
- `persona_file`
- `model`
- `reasoning_effort`
- `tools_allowed`
- `dependencies`
- `max_tokens`
- `temperature`
- `timeout_sec`
- `retry_policy`

#### 2.1 Orchestrator
- Role: workflow planning, routing, stage gating, escalation.
- Required privilege: call all agents.
- Required mode: high reasoning effort.

#### 2.2 Spec Explorer
- Role: standards retrieval (section, table, formula, conditions).
- Required capability: table-aware lookup and filter-based extraction.
- Must return structured citation payload.

#### 2.3 Discipline Specialists (7)
- `piping_specialist`
  - Focus: ASME B31.3, API 570, API 510
  - Key outputs: t_min, CR, RL, inspection interval
- `static_equipment_specialist`
  - Focus: ASME VIII, API 510
  - Key outputs: required thickness, MAWP-related checks, integrity status
- `rotating_specialist`
  - Focus: API 610/617/670
  - Key outputs: vibration assessment, nozzle load status, bearing condition
- `electrical_specialist`
  - Focus: IEEE 3000 series
  - Key outputs: health index, protection margin, risk class
- `instrumentation_specialist`
  - Focus: calibration interval and drift governance
  - Key outputs: drift trend, interval recommendation, confidence
- `steel_specialist`
  - Focus: AISC 360
  - Key outputs: D/C ratio, fatigue margin
- `civil_specialist`
  - Focus: ACI 318/562
  - Key outputs: concrete integrity score, repair priority

#### 2.4 Support Agents
- `calculator_worker`
  - Role: deterministic numeric execution
  - Reasoning effort: low
- `verification_agent`
  - Role: MAKER voting, reverse checks, sanity checks
  - Reasoning effort: high

### 3) Workflow Definitions
Required workflow groups:
- `standard_calculation`
- `emergency_assessment`
- `revalidation_only`

#### 3.1 Standard Workflow Contract
Required steps:
1. input validation
2. discipline classification
3. standards identification
4. spec extraction
5. parallel calculation
6. cross-verification
7. final validation
8. report generation

#### 3.2 Emergency Workflow Contract
- `fast_track = true`
- `skip_parallel = conditional`
- `escalation_required = true`
- `strict_threshold_profile = safety_critical`

### 4) Dependency Model
- Specialists depend on `spec_explorer`, `calculator_worker`, `verification_agent`.
- Orchestrator depends on all sub-agents.
- Verification agent may call calculator worker for reverse checks.

### 5) Message Communication Contract
All runtime messages must use shared envelope and payload conventions defined in:
- `docs/specs/shared/MESSAGE_SCHEMA_AND_RED_FLAG_TAXONOMY_V0.1.md`

Minimum required message types:
- `calculation_request`
- `spec_lookup_request`
- `verification_request`
- `calculation_result`
- `escalation_event`

### 6) Error Handling and Escalation Rules
- Retries:
  - transient operational errors only
  - no retry for schema or standards-integrity critical errors
- Escalation:
  - immediate for critical red flags
  - required when consensus fails after tie-breaker
- Release blocking:
  - any unresolved `critical` or `high` flag blocks final report release

### 7) Configuration Validation Rules
- Agent names must be unique.
- Undefined dependencies are invalid.
- Timeout ranges must be within global bounds.
- Every workflow step must map to at least one callable agent.

### 8) Observability Requirements
- Each agent invocation must log:
  - start/end time
  - input hash
  - output hash
  - reference set
  - flags and escalation status

### 9) Security and Governance Requirements
- Standards source versions must be pinned.
- All output must preserve audit trace identifiers.
- Configuration changes require changelog update and compatibility note.

## Verification Strategy
- Pre-run config lint checks.
- Dry-run simulation with representative multi-discipline request.
- Verification that emergency path can bypass non-critical steps safely.
- Contract-level schema validation for all message types.

## Next Steps
1. Draft implementation-facing config schema in `src/shared/schemas/config.schema.json`.
2. Build config validator utility and test fixtures.
3. Execute one end-to-end dry run with mock agents and audit the trace chain.
