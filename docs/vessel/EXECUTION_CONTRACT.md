# Vessel Execution Contract
Status: Draft

## Key Inputs
- `design_conditions`
- `geometry_context`
- `material_joint_data`
- `damage_observations`
- `inspection_history`

## Key Outputs
- `required_thickness`
- `remaining_life`
- `inspection_interval`
- `ffs_screening_summary`
- `repair_flags`

## Layer Checks
- Layer 1:
  - thickness math and unit consistency
- Layer 2:
  - code applicability and consensus
- Layer 3:
  - damage, pressure, and repair red-flag screening
- Layer 4:
  - reverse pressure-thickness and interval checks

## Core Red Flags
- Thickness below required minimum
- External-pressure screening failure
- Opening or nozzle reinforcement concern
- Missing damage mechanism basis
- Inspection interval unsupported by remaining life
