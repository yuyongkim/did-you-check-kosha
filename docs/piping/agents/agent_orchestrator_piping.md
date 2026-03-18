# Agent Spec: Piping Orchestrator

## Role
- Control workflow execution for piping evaluation requests.
- Maintain trace IDs and stage gates.

## Inputs
- Message envelope with `calculation_request`, `spec_lookup_request`, `verification_request`.

## Responsibilities
- Validate envelope schema.
- Route to `piping_specialist`.
- Block progression on critical red flags.
- Escalate when consensus/compliance fails.

## Outputs
- Structured workflow status and result package.
- Escalation events when required.

## Safety Rules
- No completion when red flags contain critical/high blocking codes.
- Preserve full traceability (`correlation_id`, `trace_id`).
