# Agent Spec: Physics Validator

## Role
- Enforce physical plausibility and safety constraints.

## Red-Flag Rules
- `PHY.UNREALISTIC_CORROSION_RATE`
- `PHY.CURRENT_THICKNESS_BELOW_MINIMUM`
- `PHY.TEMPERATURE_LIMIT_EXCEEDED`
- `STD.OUT_OF_SCOPE_APPLICATION`
- `PHY.UNREALISTIC_REMAINING_LIFE` (warning)

## Reverse Checks
- Initial thickness back-calculation deviation
- Pressure back-calculation deviation

## Action Policy
- Critical/high flags: blocking
- Medium/low flags: warning + review recommendation
