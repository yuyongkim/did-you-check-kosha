# MAKER Multi-Agent Verification Spec

Status: Draft  
Version: v0.1  
Last Updated: 2026-02-26

## Scope
Defines decomposition, independent execution, and K-voting consensus for runtime validation.

## Decomposition Pattern
- Split each calculation into minimal verifiable steps:
  - Input normalization
  - Standard/section lookup
  - Coefficient lookup
  - Core formula execution
  - Post-check and recommendation

## Agent Roles
- Agent A: Primary path using full context.
- Agent B: Alternative reasoning path with prompt variation.
- Agent C: Minimal-context numeric validator.
- Tie-breaker Agent: invoked only when K-threshold is not met.

## K-Voting Rules
- Default configuration: N=3, K=2.
- Numeric agreement uses tolerance bands.
- Categorical agreement uses exact match or controlled ontology mapping.

## Consensus Quality Metrics
- Agreement ratio per step.
- Coefficient of variation for numeric outputs.
- Method diversity score (to avoid same-path bias).
- Confidence class: HIGH, MEDIUM, LOW.

## Escalation Triggers
- No K-consensus after tie-breaker.
- Conflicting standard references.
- Any critical safety red flag.

## Logging Contract
Each step log must include:
- step_id, run_id, timestamp
- agent_id and method label
- input snapshot hash
- output value with unit
- standard reference and confidence
