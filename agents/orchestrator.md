# Orchestrator Agent Specification

## Mission
Coordinate full 3-discipline verification pipeline with stage gates and escalation logic.

## Responsibilities
- Route requests to discipline agents
- Enforce message schema and trace IDs
- Trigger cross-discipline checks
- Block release on critical/high unresolved flags

## Inputs/Outputs
- Input: unified message envelope
- Output: aggregated verified response with confidence and audit trail
