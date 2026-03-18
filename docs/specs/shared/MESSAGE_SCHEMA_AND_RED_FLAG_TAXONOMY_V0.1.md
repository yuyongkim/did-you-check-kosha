# Message Schema and Red-Flag Taxonomy Specification

Status: Draft (Freeze Candidate)  
Version: v0.1  
Last Updated: 2026-02-26

## 1) Scope
- Define a single message envelope for all agent-to-agent communications.
- Define mandatory payload contracts for core workflow messages.
- Define a unified red-flag taxonomy with severity, trigger, and auto-action rules.

## 2) Message Envelope (Global Contract)

### Required Fields
```json
{
  "message_id": "uuid-v4",
  "message_type": "calculation_request",
  "correlation_id": "uuid-v4",
  "trace_id": "uuid-v4",
  "from_agent": "orchestrator",
  "to_agent": "piping_specialist",
  "timestamp_utc": "2026-02-26T09:30:00Z",
  "priority": "normal",
  "timeout_sec": 300,
  "payload": {},
  "meta": {
    "discipline": "piping",
    "workflow_id": "standard_calculation",
    "standards_context_version": "v0.1"
  }
}
```

### Field Rules
- `message_id`, `correlation_id`, `trace_id`: UUID only.
- `priority`: `low | normal | high | critical`.
- `timeout_sec`: integer, 1-1800.
- `timestamp_utc`: ISO 8601 UTC only.
- `payload`: must match schema by `message_type`.

## 3) Core Message Types

### `calculation_request`
Used by orchestrator to trigger discipline or worker calculation.
```json
{
  "calculation_type": "remaining_life",
  "input_data": {},
  "assumptions": [],
  "required_outputs": ["remaining_life", "inspection_interval"],
  "standards_context": [
    {"code": "ASME B31.3", "section": "Para 304.1.2"}
  ]
}
```

### `spec_lookup_request`
Used to query spec explorer for clauses/table values.
```json
{
  "query": "SA-106 Gr.B allowable stress at 300F",
  "filters": {
    "standard": "ASME B31.3",
    "section_or_table": "Table A-1",
    "material": "SA-106 Gr.B",
    "temperature_f": 300
  }
}
```

### `verification_request`
Used to trigger MAKER, reverse-check, or sanity checks.
```json
{
  "verification_type": "maker_voting",
  "inputs": {},
  "results": {},
  "tolerance": {"type": "relative", "value": 0.01},
  "criticality": "safety_critical"
}
```

### `calculation_result`
Used by specialists/workers for computed outputs.
```json
{
  "status": "success",
  "results": {},
  "calculation_steps": [],
  "references": [],
  "assumptions": [],
  "flags": {"red_flags": [], "warnings": []}
}
```

### `escalation_event`
Used when auto-run must stop or human review is required.
```json
{
  "reason_code": "STD.INVALID_REFERENCE",
  "severity": "critical",
  "summary": "Invalid standard section reference detected",
  "recommended_action": "human_review_required",
  "blocking": true
}
```

## 4) Error Response Contract
```json
{
  "status": "error",
  "error_code": "SCHEMA.MISSING_REQUIRED_FIELD",
  "error_message": "input_data.design_pressure is required",
  "retryable": false,
  "details": {},
  "flags": {"red_flags": [], "warnings": []}
}
```

## 5) Red-Flag Taxonomy (Unified)

### Severity Levels
- `critical`: immediate stop + escalation.
- `high`: block final release + mandatory re-verification.
- `medium`: warning + additional checks required.
- `low`: note only, does not block release.

### Category Map
- `PHY`: physical impossibility or implausibility.
- `STD`: standards reference or applicability violation.
- `UNIT`: unit mismatch or conversion inconsistency.
- `LOG`: logical inconsistency in decomposition flow.
- `DATA`: mandatory input missing/invalid.
- `FMT`: schema/format contract violations.
- `OPS`: timeout/retry/execution operation issues.

### Standard Red-Flag Codes
- `PHY.NEGATIVE_THICKNESS`
- `PHY.NEGATIVE_REMAINING_LIFE`
- `PHY.UNREALISTIC_CORROSION_RATE`
- `PHY.UNREALISTIC_REMAINING_LIFE`
- `PHY.ALLOWABLE_STRESS_EXCEEDED`
- `PHY.CURRENT_THICKNESS_BELOW_MINIMUM`
- `PHY.TEMPERATURE_LIMIT_EXCEEDED`
- `PHY.VIBRATION_LIMIT_EXCEEDED`
- `PHY.NOZZLE_LOAD_EXCEEDED`
- `PHY.BEARING_TEMPERATURE_HIGH`
- `PHY.TRANSFORMER_HEALTH_CRITICAL`
- `PHY.ARC_FLASH_ENERGY_EXCEEDED`
- `PHY.VOLTAGE_DROP_EXCEEDED`
- `PHY.BREAKER_INTERRUPT_RATING_EXCEEDED`
- `PHY.HARMONIC_DISTORTION_EXCEEDED`
- `PHY.SIL_TARGET_NOT_MET`
- `PHY.DRIFT_RATE_EXCEEDED`
- `PHY.SENSOR_MTBF_LOW`
- `PHY.CONTROL_VALVE_CAPACITY_LOW`
- `PHY.ELECTRICAL_TO_ROTATING_COUPLING_RISK`
- `PHY.INSTRUMENT_TO_PIPING_COUPLING_RISK`
- `PHY.ELECTRICAL_NOISE_TO_SIS_RISK`
- `PHY.STRUCTURAL_DC_CRITICAL`
- `PHY.STRUCTURAL_DC_OVERSTRESSED`
- `PHY.STEEL_CORROSION_SECTION_LOSS_HIGH`
- `PHY.STEEL_DEFLECTION_EXCEEDED`
- `PHY.CONNECTION_FAILURE_DETECTED`
- `PHY.CIVIL_FLEXURE_OVERSTRESS`
- `PHY.CIVIL_SUBSTANTIAL_DAMAGE`
- `PHY.CIVIL_CARBONATION_CORROSION_INITIATED`
- `PHY.CIVIL_CRACK_WIDTH_EXCEEDED`
- `PHY.CIVIL_SPALLING_SEVERE`
- `PHY.CIVIL_FOUNDATION_SETTLEMENT_HIGH`
- `PHY.STRUCTURE_TO_PIPING_OVERLOAD_RISK`
- `PHY.STRUCTURE_TO_PIPING_DEFLECTION_RISK`
- `PHY.FOUNDATION_TO_ROTATING_MISALIGNMENT_RISK`
- `PHY.FOUNDATION_CRACK_VIBRATION_COUPLING`
- `PHY.STRUCTURE_SUPPORT_ELECTRICAL_RISK`
- `PHY.STRUCTURE_TO_SIS_RELIABILITY_RISK`
- `STD.INVALID_REFERENCE`
- `STD.OUT_OF_SCOPE_APPLICATION`
- `STD.UNAPPROVED_MATERIAL`
- `STD.JOINT_EFFICIENCY_INVALID`
- `UNIT.MIXED_SYSTEM_DETECTED`
- `UNIT.CONVERSION_MISMATCH`
- `LOG.NO_CONSENSUS_AFTER_TIEBREAKER`
- `LOG.REVERSE_CHECK_DEVIATION`
- `LOG.DRIFT_MODEL_LOW_CONFIDENCE`
- `DATA.MISSING_MANDATORY_FIELD`
- `DATA.INVALID_THICKNESS_HISTORY`
- `FMT.SCHEMA_VALIDATION_FAILED`
- `OPS.TIMEOUT_EXCEEDED`

## 6) Red-Flag Auto-Action Matrix

| Severity | Blocking | Auto Action | Human Review |
|---|---|---|---|
| critical | true | terminate workflow | required |
| high | true | re-run with strict mode | required |
| medium | false | add extra verification step | optional |
| low | false | log and continue | no |

## 7) Escalation Rules
- Any `critical` flag: stop current workflow and publish `escalation_event`.
- Repeated `high` on same `correlation_id` (>=2): escalate.
- `LOG.NO_CONSENSUS_AFTER_TIEBREAKER`: mandatory SME review.
- `STD.INVALID_REFERENCE` in final result: hard fail regardless of numeric accuracy.

## 8) Traceability Rules
- Every message must preserve `correlation_id` and `trace_id`.
- Final report must include:
  - all references used
  - all assumptions introduced
  - full flag history with timestamps
  - escalation decisions and owners

## 9) Freeze Criteria for This Spec
- No ambiguous enum values remain.
- Red-flag codes cover all current critical scenarios.
- At least one end-to-end dry-run validates message compatibility across all 11 agents.
