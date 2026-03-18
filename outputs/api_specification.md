# API Specification (Design)

## Envelope
All APIs use common envelope fields:
- message_id
- message_type
- correlation_id
- trace_id
- from_agent
- to_agent
- timestamp_utc
- priority
- timeout_sec
- payload
- meta

## Endpoints (Logical)
1. `POST /api/calculate/piping`
2. `POST /api/calculate/vessel`
3. `POST /api/calculate/rotating`
4. `POST /api/calculate/electrical`
5. `POST /api/calculate/instrumentation`
6. `POST /api/calculate/steel`
7. `POST /api/calculate/civil`
8. `POST /api/calculate/five-discipline`
9. `POST /api/calculate/seven-discipline`
10. `POST /api/verify/cross-discipline`
11. `POST /api/spec/lookup`

## Response
- status
- results
- flags (red_flags, warnings)
- references
- verification_summary

## Error Contract
- error_code
- error_message
- retryable
- details
