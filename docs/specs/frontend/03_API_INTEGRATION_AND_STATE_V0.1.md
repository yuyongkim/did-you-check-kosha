# Frontend API Integration and State Specification

Status: Draft
Version: v0.1
Last Updated: 2026-02-27

## 1) API Integration Strategy
Use a typed client layer under `lib/api.ts` with route-specific methods:
- `calculatePiping()`
- `calculateVessel()`
- `calculateRotating()`
- `calculateElectrical()`
- `calculateInstrumentation()`
- `calculateSteel()`
- `calculateCivil()`
- `calculateFiveDiscipline()`
- `calculateSevenDiscipline()`

## 2) Expected API Response Envelope
```json
{
  "status": "success|error|blocked",
  "discipline": "piping",
  "results": {},
  "details": {
    "calculation_summary": {},
    "layer_results": [],
    "calculation_steps": [],
    "flags": {"red_flags": [], "warnings": []},
    "recommendations": []
  }
}
```

## 3) State Model (Zustand)
- `activeDiscipline`
- `activeProjectId`
- `activeAssetId`
- `requestState` (idle/loading/success/error)
- `lastResultByDiscipline`
- `lastError`

## 4) Hooks
- `useCalculation(discipline)`
  - submit payload
  - map response to VM
  - expose loading/error/result
- `useVerification(result)`
  - derive layer status summary
  - derive blocking boolean
- `useStandardsReferences(result)`
  - aggregate and dedupe references from steps

## 5) Error Handling Policy
- Schema mismatch:
  - show contract error and request trace context
- Timeout/network failure:
  - allow retry with same payload
- Backend blocked status:
  - treat as successful response with safety-blocked UI state

## 6) Mapping Rules
- Always map `flags.red_flags` to top-level alert ribbon.
- Always render `layer_results` in right pane.
- If `calculation_steps` exists, render references list.
- If references are empty, show explicit warning badge.

## 7) Telemetry (Frontend)
- Track:
  - request duration
  - route + discipline usage
  - blocked result rate by discipline
  - validation-error rate
- Do not log raw sensitive project data in client telemetry.
