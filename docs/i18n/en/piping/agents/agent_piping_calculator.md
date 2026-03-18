# Agent Spec: Piping Calculator

## Role
- Execute full ASME/API-based piping integrity calculations.

## Inputs
- Material, pressure, temperature, thickness history, CA, weld type, service context.

## Core Methods
- Minimum thickness (ASME B31.3)
- Corrosion rates and RL (API 570)
- Inspection interval policy (API 570)

## Verification Hooks
- Layer 2 consensus candidates
- Layer 3 red-flag checks
- Layer 4 reverse validation

## Output Contract
- `final_results`: t_min, corrosion rates, RL, inspection interval
- `flags`: red flags and warnings
- `calculation_steps`: references and formulas
