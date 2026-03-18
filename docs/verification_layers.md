# Verification Layers (7-Discipline Common Policy)

## Layer 1: Input / Unit / Range Guard
- Validate required fields and data types.
- Validate unit contracts and internal normalization.
- Apply discipline-specific range checks.
- Missing critical fields -> blocking error.

## Layer 2: MAKER Consensus (K-Voting)
- Execute 3 independent solution paths.
- Numeric outputs must agree within 1% relative tolerance.
- If not, run tie-breaker and mark consensus quality.
- Unresolved divergence -> `LOG.NO_CONSENSUS_AFTER_TIEBREAKER`.

## Layer 3: Physics and Standards Compliance
- Enforce discipline-specific red flags.
- Block physically impossible states and standards scope violations.
- Require explicit standard references for every major calculation step.

## Layer 4: Reverse Verification
- Back-calculate key inputs from outputs.
- Deviation threshold:
  - warning at >2% for critical variables
  - escalate at >5%
- Reverse-check failures feed audit trail and confidence downgrade.

## Piping Discipline Addendum (ASME B31.3 / API 570)
- Layer 1 minimum checks
  - required: `material`, `design_pressure_mpa`, `design_temperature_c`, `thickness_history`
  - contract fields: `weld_type`, `service_type`, `corrosion_allowance_mm`, `chloride_ppm`, `has_internal_coating`
  - unit scope: MPa / C / mm only
- Layer 2 consensus focus
  - independent recomputation of `t_min`, `CR_long`, `CR_short`, `CR_selected`, `RL`
  - acceptance: relative deviation <= 1%
- Layer 3 red flags (blocking)
  - `current_thickness <= t_min`
  - design temperature above profile hard-limit envelope
  - hydrotest chloride above material-group limit
  - unrealistic corrosion regime (project policy threshold)
  - blocked banner displays top red-flag codes to identify immediate cause
  - non-blocking managed-envelope warning:
    - `STD.TEMPERATURE_OVERRIDE_REVIEW_REQUIRED` when temperature is above conservative limit but within selected managed profile hard-limit
- Layer 4 reverse checks
  - reverse initial thickness from selected corrosion rate and service years
  - reverse pressure consistency check from thickness result and stress factors
  - escalate when reverse deviation >5%

## Rotating Discipline Addendum (API 610/617/670 + Steam Turbine Context)
- Layer 1 minimum checks
  - required: `machine_type`, `vibration_mm_per_s`, `nozzle_load_ratio`, `bearing_temperature_c`, `speed_rpm`
  - when `machine_type=steam_turbine`:
    - required: `steam_pressure_bar`
    - plus at least one state anchor set:
      - (`steam_temperature_c` or `steam_quality_x`) OR
      - (`inlet_enthalpy_kj_per_kg` + `outlet_enthalpy_kj_per_kg`)
  - missing state anchors -> `STD.STEAM_TABLE_LOOKUP_REQUIRED`
- Layer 2 consensus focus
  - independent recomputation of vibration/nozzle/bearing HI path
  - for steam turbine, include `phase_change_risk_index` consensus
- Layer 3 red flags (blocking)
  - vibration limit exceeded
  - nozzle load exceeded
  - steam wetness erosion risk (`steam_quality_x` below threshold)
  - steam phase-change boundary risk (low superheat margin / high risk index)
- Layer 4 reverse checks
  - bearing-temperature reverse consistency (common rotating)
  - enthalpy drop reverse consistency (steam turbine only, when enthalpy pair provided)

## Static Equipment Addendum (ASME VIII / API 510)
- Layer 1 minimum checks
  - required core: `material`, `design_pressure_mpa`, `design_temperature_c`, `inside_radius_mm`, `t_current_mm`
  - geometry context (non-blocking warning if missing by type):
    - `shell_length_mm` for horizontal/hx context
    - `straight_shell_height_mm` for vertical/column context
    - `head_type`, `head_depth_mm`, `nozzle_od_mm`
  - optional screening inputs:
    - `external_pressure_mpa`
    - `reinforcement_pad_thickness_mm`, `reinforcement_pad_width_mm`
- Layer 2 consensus focus
  - independent recomputation of `t_required_shell`, `remaining_life`, `inspection_interval`
- Layer 3 red flags (blocking)
  - `current_thickness <= t_required_shell`
  - material temperature limit exceeded
  - external pressure screening utilization > 1.2 (`PHY.VESSEL_EXTERNAL_PRESSURE_RISK`)
  - nozzle reinforcement screening index < 0.8 (`PHY.VESSEL_NOZZLE_REINFORCEMENT_RISK`)
- Layer 3 warnings (non-blocking)
  - high L/D screening ratio
  - external pressure utilization review band (1.0-1.2)
  - nozzle reinforcement review band (index 0.8-1.0 / high opening ratio)
- Layer 4 reverse checks
  - reverse pressure consistency from thickness result
  - deviation escalation above project threshold

## Human Intervention Triggers
- Any critical red flag.
- Standards ambiguity not resolved by conservative rule.
- No consensus after tie-breaker.
- Reverse deviation above escalation threshold.

## Final Release Gate
Release allowed only when:
- no blocking flags,
- standards references complete,
- layer status meets policy,
- traceability package complete.
