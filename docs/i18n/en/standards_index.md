# Standards Index (Discipline Map)

## Piping
- Scope
  - Process piping integrity screening: `t_min`, corrosion rate, remaining life, inspection interval.
- Material coverage (current runtime/frontend baseline)
  - Carbon steel (CS): `SA-106 Gr.B`, `A106 Gr.B`, `SA-53 Gr.B`, `SA-333 Gr.6`, `A105`, `A234 WPB`, `API 5L Gr.B`
  - Low alloy steel: `SA-335 P11`, `SA-335 P22`, `SA-335 P5`, `SA-335 P9`, `SA-335 P91`
  - Stainless steel (SUS): `SA-312 TP304`, `SA-312 TP304L`, `SA-312 TP316`, `SA-312 TP316L`, `SA-312 TP321`, `SA-312 TP347`
  - Duplex stainless: `SA-790 S31803`, `SA-790 S32205`, `SA-790 S32750`
  - Nickel alloy: `Alloy 825 (N08825)`, `Alloy 625 (N06625)`, `Monel 400 (N04400)`
- ASME B31.3
  - Minimum thickness formula: Para 304.1.2 (Eq. 3a context)
  - Allowable stress table: Table A-1 (temperature-dependent lookup/interpolation)
  - Weld efficiency and Y-coefficient: code-defined clauses
- API 570
  - Corrosion rate and remaining life methodology
  - Inspection interval governance (Section 7 context)
  - Hydrotest water quality guidance (chloride limit checks in workflow)
- Process-fluid context (engineering screening profile)
  - `fluid_type` factorized screening is supported in runtime/frontend:
    - hydrocarbon dry/wet, steam-condensate, amine, H2S sour, chloride aqueous, caustic, seawater, oxygen-rich
  - Used for conservative corrosion-severity weighting in internal calculation policy.
- Runtime guardrails
  - Material temperature envelope checks (material/profile-dependent limits)
  - Temperature profile modes:
    - `strict_process`: conservative limit only (exceedance blocks)
    - `high_temp_managed`: conservative-limit exceedance is warning, hard-limit exceedance blocks
    - `legacy_power_steam`: wider managed envelope with mandatory review warning
  - Hydrotest chloride screening:
    - carbon steel / low alloy baseline: `<= 250 ppm`
    - stainless / duplex baseline: `<= 30 ppm`
    - nickel alloy baseline: `<= 50 ppm`
- API 510 (interface relevance)
  - Boundary checks for pressure equipment interface

## Static Equipment (Vessel)
- Material/type coverage (current runtime/frontend baseline)
  - Carbon/carbon-manganese: `SA-516-60/65/70`, `SA-515-70`, `SA-537 Cl1`
  - Low alloy: `SA-387 Gr11 Cl2`, `SA-387 Gr22 Cl2`
  - Stainless: `SA-240-304/304L/316/316L/321/347`
  - Vessel categories: horizontal drum, vertical vessel, column/tower, exchanger shell, reactor
- Geometry context coverage (screening-level)
  - Inputs now include shell length, straight shell height, head type/depth, and nozzle OD.
  - Current UG-27 runtime core still uses `P, R, S, E, CA` for required shell thickness.
  - Dimension set is used for context metrics (`L/D`, estimated volume, shell area) and non-blocking review warnings.
- ASME Section VIII Div.1
  - Cylindrical shell thickness (UG-27)
  - External pressure screening context (UG-28)
  - Nozzle reinforcement screening context (UG-37)
  - Head forms and required thickness checks
  - Joint efficiency classification (Type 1, Type 2, etc.)
- API 510
  - In-service inspection and interval logic
- API 579-1/ASME FFS-1
  - Local thin area / local metal loss screening logic (Level 1 context)

## Rotating Equipment
- Machine-type coverage (current runtime/frontend baseline)
  - `pump`, `compressor`, `steam_turbine`, `gas_turbine`, `blower`, `fan`, `gearbox`
- API 610
  - Pump vibration/nozzle load acceptance boundaries
- API 617
  - Compressor acceptance and mechanical integrity checks
- API 670
  - Machinery protection and vibration monitoring framework
- Steam turbine deepening track (template split from generic rotating)
  - API 611/API 612 context for steam turbine reliability checks
  - IAPWS IF97 context for steam-property lookup and phase-state screening
  - dedicated steam state inputs:
    - `steam_pressure_bar`, `steam_temperature_c`, `steam_quality_x`
    - optional enthalpy pair: `inlet_enthalpy_kj_per_kg`, `outlet_enthalpy_kj_per_kg`
  - dedicated guardrails:
    - wetness/erosion risk flag when dryness fraction is low
    - phase-change boundary risk near saturation margin
    - steam-table lookup required when state anchors are missing

## Electrical
- Equipment-type coverage (current runtime/frontend baseline)
  - `transformer`, `switchgear`, `mcc`, `motor`, `ups`, `feeder_panel`
- IEEE C57.104
  - Transformer health index input dimensions
- IEEE 1584-2018
  - Arc-flash incident energy framework
- IEEE 3000 series
  - Voltage drop, fault current, and power-quality checks
- NFPA 70E
  - Electrical safety categories and work controls

## Instrumentation
- Device/architecture coverage (current runtime/frontend baseline)
  - Instrument types: pressure/temperature/flow/level transmitters, valve positioner, analyzer, vibration probe
  - SIF architectures: `1oo1`, `1oo2`, `2oo2`, `2oo3`
- IEC 61511
  - SIL target validation and PFDavg criteria
- ISA-TR84.00.02
  - SIS lifecycle and reliability context
- ISA 5.1
  - Instrument identification and tagging conventions
- ISO GUM
  - Measurement uncertainty model

## Steel Structure
- Member/type coverage (current runtime/frontend baseline)
  - `column`, `beam`, `brace`, `girder`, `truss_member`, `pipe_rack_leg`, `portal_frame`
  - Steel grade tags supported in frontend workflow: `A36`, `A572 Gr50`, `A992`, `A500 GrB`, `A500 GrC`
- AISC 360
  - Compression strength (lambda_c, Fcr, phiPn)
  - Demand/Capacity screening
  - Serviceability deflection checks

## Civil/Concrete
- Element/exposure coverage (current runtime/frontend baseline)
  - Elements: `beam`, `column`, `slab`, `foundation`, `retaining_wall`, `pedestal`, `pile_cap`, `mat_foundation`
  - Exposure classes: `indoor_dry`, `outdoor_urban`, `coastal_marine`, `industrial_chemical`, `splash_zone`, `buried_soil`
- ACI 318
  - Flexural capacity framework
- ACI 562
  - Substantial damage classification criteria
- Carbonation and durability references
  - Cover-depth and crack/spalling screening context

## Cross-Cutting
- All formula/limit values must be pinned to active standard editions before production use.
- Where edition-dependent values are uncertain, output must include explicit verification note.
