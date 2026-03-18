import { GlossaryDiscipline } from "@/lib/glossary-types";

const TERM_LABELS: Record<string, string> = {
  // Verification
  "Layer 1: Input Validation": "Layer 1 Input Validation",
  "Layer 2: MAKER Consensus": "Layer 2 MAKER Consensus",
  "Layer 3: Physics and Standards": "Layer 3 Physics and Standards",
  "Layer 4: Reverse Verification": "Layer 4 Reverse Verification",
  confidence: "Confidence",
  execution_time_sec: "Execution Time",
  references: "Standards References",
  status: "Status",
  "UG-27": "ASME VIII UG-27",
  "UG-28": "ASME VIII UG-28",
  "UG-37": "ASME VIII UG-37",
  "Para 304.1.2": "ASME B31.3 Para 304.1.2",
  "Table A-1": "ASME B31.3 Table A-1",

  // Piping
  material: "Material",
  temperature_profile: "Temperature Profile",
  design_pressure_mpa: "Design Pressure",
  design_temperature_c: "Design Temperature",
  nps: "NPS",
  weld_type: "Weld Type",
  service_type: "Service Type",
  fluid_type: "Fluid Type",
  corrosion_allowance_mm: "Corrosion Allowance",
  chloride_ppm: "Hydrotest Chloride",
  has_internal_coating: "Internal Coating",
  allowable_stress_mpa: "Allowable Stress",
  weld_efficiency: "Weld Efficiency",
  t_min_mm: "Minimum Required Thickness",
  t_current_mm: "Current Thickness",
  temperature_soft_limit_c: "Conservative Temperature Limit",
  temperature_hard_limit_c: "Managed Temperature Hard Limit",
  temperature_limit_mode: "Temperature Limit Mode",
  cr_selected_mm_per_year: "Selected Corrosion Rate",
  remaining_life_years: "Remaining Life",
  inspection_interval_years: "Inspection Interval",

  // Vessel
  vessel_type: "Vessel Type",
  inside_radius_mm: "Inside Radius",
  shell_length_mm: "Shell Length",
  straight_shell_height_mm: "Straight Shell Height",
  head_type: "Head Type",
  head_depth_mm: "Head Depth",
  nozzle_od_mm: "Nozzle OD",
  external_pressure_mpa: "External Pressure",
  reinforcement_pad_thickness_mm: "Reinforcement Pad Thickness",
  reinforcement_pad_width_mm: "Reinforcement Pad Width",
  joint_efficiency: "Joint Efficiency",
  assumed_corrosion_rate_mm_per_year: "Assumed Corrosion Rate",
  t_required_shell_mm: "Required Shell Thickness",
  diameter_mm: "Vessel Diameter",
  governing_span_mm: "Governing Span",
  head_depth_mm_used: "Head Depth Used",
  slenderness_ld_ratio: "L/D Ratio",
  shell_surface_area_m2: "Shell Surface Area",
  estimated_internal_volume_m3: "Estimated Internal Volume",
  span_source: "Span Source",
  external_pressure_mpa_input: "External Pressure Input",
  external_pressure_allowable_screen_mpa: "External Pressure Allowable (Screen)",
  external_pressure_utilization: "External Pressure Utilization",
  nozzle_opening_ratio: "Nozzle Opening Ratio",
  nozzle_reinforcement_index: "Nozzle Reinforcement Index",
  reinforcement_pad_thickness_mm_used: "Pad Thickness Used",
  reinforcement_pad_width_mm_used: "Pad Width Used",

  // Rotating
  machine_type: "Machine Type",
  driver_type: "Driver Type",
  service_criticality: "Service Criticality",
  stage_count: "Stage / Throw Count",
  train_arrangement: "Train Arrangement",
  casing_type: "Casing Type",
  bearing_type: "Bearing Type",
  seal_system: "Seal System",
  lube_system: "Lube System",
  vibration_mm_per_s: "Vibration",
  vibration_limit_mm_per_s: "Vibration Limit",
  adjusted_vibration_limit_mm_per_s: "Adjusted Vibration Limit",
  nozzle_load_ratio: "Nozzle Load Ratio",
  nozzle_load_limit_ratio: "Nozzle Load Limit",
  nozzle_load_limit_base_ratio: "Nozzle Load Base Limit",
  bearing_temperature_c: "Bearing Temperature",
  lube_oil_supply_temp_c: "Lube Oil Supply Temperature",
  coupling_misalignment_mils: "Coupling Misalignment",
  axial_displacement_um: "Axial Displacement",
  axial_displacement_limit_um: "Axial Displacement Limit",
  speed_rpm: "Speed",
  speed_low_limit_rpm: "Speed Low Limit",
  speed_high_limit_rpm: "Speed High Limit",
  phase_change_risk_index: "Phase Change Risk Index",
  steam_pressure_bar: "Steam Pressure",
  steam_temperature_c: "Steam Temperature",
  steam_quality_x: "Steam Quality (x)",
  inlet_enthalpy_kj_per_kg: "Inlet Enthalpy",
  outlet_enthalpy_kj_per_kg: "Outlet Enthalpy",
  suction_pressure_bar: "Suction Pressure",
  discharge_pressure_bar: "Discharge Pressure",
  pressure_ratio: "Pressure Ratio",
  surge_events_30d: "Surge Events (30d)",
  npsh_available_m: "NPSH Available",
  npsh_required_m: "NPSH Required",
  npsh_margin_m: "NPSH Margin",
  api670_coverage_pct: "API 670 Coverage",
  trip_tests_last_12m: "Trip Tests (12m)",
  expected_trip_tests_per_year: "Expected Trip Tests / Year",
  protection_bypass_active: "Protection Bypass Active",
  mechanical_integrity_index: "Mechanical Integrity Index",
  process_stability_index: "Process Stability Index",
  protection_readiness_index: "Protection Readiness Index",
  bearing_health_index: "Bearing Health Index",
  driver_factor: "Driver Factor",
  criticality_factor: "Criticality Factor",
  stage_vibration_factor: "Stage Vibration Factor",
  train_vibration_factor: "Train Vibration Factor",
  casing_vibration_factor: "Casing Vibration Factor",
  bearing_vibration_factor: "Bearing Vibration Factor",
  train_nozzle_factor: "Train Nozzle Factor",
  casing_nozzle_factor: "Casing Nozzle Factor",
  seal_process_factor: "Seal Process Factor",
  lube_process_factor: "Lube Process Factor",
  lube_temperature_factor: "Lube Temperature Factor",

  // Electrical
  equipment_type: "Equipment Type",
  system_voltage_kv: "System Voltage",
  bolted_fault_current_ka: "Bolted Fault Current",
  fault_current_ka: "Fault Current",
  clearing_time_sec: "Clearing Time",
  working_distance_mm: "Working Distance",
  breaker_interrupt_rating_ka: "Breaker Interrupt Rating",
  voltage_drop_percent: "Voltage Drop",
  thd_voltage_percent: "Voltage THD",
  motor_current_thd_percent: "Current THD",
  power_factor: "Power Factor",
  dga_score: "DGA Score",
  oil_quality_score: "Oil Quality Score",
  insulation_score: "Insulation Score",
  load_factor_score: "Load Score",
  transformer_health_index: "Transformer Health Index",
  arc_flash_energy_cal_cm2: "Arc Flash Energy",
  ppe_category: "PPE Category",

  // Instrumentation
  instrument_type: "Instrument Type",
  voting_architecture: "SIF Voting Architecture",
  sil_target: "SIL Target",
  sil_achieved: "SIL Achieved",
  failure_rate_per_hour: "Failure Rate",
  proof_test_interval_hours: "Proof Test Interval",
  mttr_hours: "MTTR",
  calibration_interval_days: "Current Calibration Interval",
  calibration_interval_optimal_days: "Optimal Calibration Interval",
  tolerance_pct: "Tolerance",
  sensor_mtbf_years: "Sensor MTBF",
  cv_required: "Required Cv",
  cv_rated: "Rated Cv",
  pfdavg: "PFDavg",
  predicted_drift_pct: "Predicted Drift",

  // Steel
  member_type: "Member Type",
  steel_grade: "Steel Grade",
  section_label: "Section Label",
  length_m: "Member Length",
  k_factor: "K Factor",
  radius_of_gyration_mm: "Radius of Gyration",
  yield_strength_mpa: "Yield Strength",
  gross_area_mm2: "Gross Area",
  axial_demand_kn: "Axial Demand",
  corrosion_loss_percent: "Corrosion Loss",
  deflection_mm: "Deflection",
  span_mm: "Span",
  connection_failure_detected: "Connection Failure",
  dc_ratio: "Demand / Capacity Ratio",
  lambda_c: "Non-dimensional Slenderness",
  phi_pn_kn: "Design Strength (phi*Pn)",

  // Civil
  element_type: "Element Type",
  environment_exposure: "Exposure Environment",
  fc_mpa: "Concrete Strength (f'c)",
  fy_mpa: "Rebar Yield Strength",
  width_mm: "Section Width",
  effective_depth_mm: "Effective Depth",
  rebar_area_mm2: "Rebar Area",
  demand_moment_knm: "Demand Moment",
  lateral_capacity_loss_percent: "Lateral Capacity Loss",
  affected_area_percent: "Affected Area",
  vertical_capacity_loss_percent: "Vertical Capacity Loss",
  carbonation_coeff_mm_sqrt_year: "Carbonation Coefficient",
  service_years: "Service Years",
  cover_thickness_mm: "Cover Thickness",
  crack_width_mm: "Crack Width",
  spalling_area_percent: "Spalling Area",
  foundation_settlement_mm: "Foundation Settlement",
  carbonation_depth_mm: "Carbonation Depth",
  years_to_corrosion_init: "Years to Corrosion Initiation",
  substantial_damage: "Substantial Damage",
};

const TERM_DEFINITIONS: Record<string, string> = {
  // Verification
  "Layer 1: Input Validation": "Checks required fields, data types, units, and range limits before calculation.",
  "Layer 2: MAKER Consensus": "Runs decomposed calculation logic and checks multi-agent agreement.",
  "Layer 3: Physics and Standards": "Applies physical sanity and standards guardrails to catch unsafe outputs.",
  "Layer 4: Reverse Verification": "Back-calculates key values to verify consistency with inputs and history.",
  confidence: "Overall confidence level after all verification layers.",
  execution_time_sec: "Elapsed calculation time for the current run.",
  references: "Count of standards/code references used in this result.",
  status: "Final release state: ACCEPTABLE, WARNING, or CRITICAL.",
  "UG-27": "ASME Section VIII Div.1 internal pressure shell-thickness rules for cylindrical shells.",
  "UG-28": "ASME Section VIII Div.1 external pressure/stability rules for shells under vacuum or external pressure.",
  "UG-37": "ASME Section VIII Div.1 opening reinforcement requirements for nozzle/shell intersections.",
  "Para 304.1.2": "ASME B31.3 pressure design equation for required piping wall thickness.",
  "Table A-1": "ASME B31.3 allowable stress table by material and temperature.",

  // Piping
  material: "Selected piping material grade used for allowable stress and limit checks.",
  temperature_profile: "Temperature envelope mode: strict conservative limit or managed high-temperature review mode.",
  design_pressure_mpa: "Design pressure used in thickness formula and integrity checks (MPa).",
  design_temperature_c: "Design temperature used for material applicability and allowable stress lookup (C).",
  nps: "Nominal Pipe Size used to resolve outside diameter.",
  weld_type: "Weld category that determines joint efficiency factor E.",
  service_type: "Service severity class used to adjust corrosion expectation.",
  fluid_type: "Fluid category used for corrosion severity weighting.",
  corrosion_allowance_mm: "Additional thickness margin reserved for expected corrosion (mm).",
  chloride_ppm: "Hydrotest water chloride content compared with material limits (ppm).",
  has_internal_coating: "Indicates internal coating/lining exists, reducing internal corrosion tendency.",
  allowable_stress_mpa: "Allowable stress from standards table at selected temperature and material (MPa).",
  weld_efficiency: "Joint efficiency factor E applied in required thickness equation.",
  t_min_mm: "Minimum required wall thickness including corrosion allowance (mm).",
  t_current_mm: "Latest measured wall thickness from inspection data (mm).",
  temperature_soft_limit_c: "Conservative temperature limit for selected material/profile (C).",
  temperature_hard_limit_c: "Maximum managed-operation temperature for selected material/profile (C).",
  temperature_limit_mode: "Indicates whether temperature is within conservative limit, managed override zone, or hard-limit exceedance.",
  cr_selected_mm_per_year: "Conservative corrosion rate selected from long/short-term evaluations (mm/yr).",
  remaining_life_years: "Estimated remaining life until current thickness reaches required minimum.",
  inspection_interval_years: "Recommended maximum interval before next integrity inspection.",

  // Vessel
  vessel_type: "Vessel geometry/use category for context and reporting.",
  inside_radius_mm: "Inside radius used in shell required thickness calculation (mm).",
  shell_length_mm: "Straight shell length (typically tangent-to-tangent) used for geometry screening (mm).",
  straight_shell_height_mm: "Vertical straight shell height used for L/D and volume context (mm).",
  head_type: "Head geometry class used for context and approximate volume/depth assumptions.",
  head_depth_mm: "Provided head depth. If missing, a geometry-based default may be used for context.",
  nozzle_od_mm: "Representative nozzle outside diameter used for local hotspot context (mm).",
  external_pressure_mpa: "Design/operating external pressure used for shell stability screening (MPa).",
  reinforcement_pad_thickness_mm: "Reinforcement pad thickness used in nozzle area-availability screen (mm).",
  reinforcement_pad_width_mm: "Reinforcement pad width used in nozzle area-availability screen (mm).",
  joint_efficiency: "ASME joint efficiency factor E based on weld and examination category.",
  assumed_corrosion_rate_mm_per_year: "Corrosion rate used for remaining life and interval estimation (mm/yr).",
  t_required_shell_mm: "Required shell thickness per governing pressure design equation (mm).",
  diameter_mm: "Calculated vessel diameter from inside radius (mm).",
  governing_span_mm: "Primary vessel span (length or height) used for geometry screening (mm).",
  head_depth_mm_used: "Head depth used in context calculations (input or default estimate).",
  slenderness_ld_ratio: "Length/diameter style ratio used for additional screening context.",
  shell_surface_area_m2: "Approximate cylindrical shell outside area for context (m2).",
  estimated_internal_volume_m3: "Approximate internal volume from shell plus head geometry (m3).",
  span_source: "Indicates whether span came from shell length, shell height, or default estimate.",
  external_pressure_mpa_input: "External pressure value used for UG-28 style screening logic (MPa).",
  external_pressure_allowable_screen_mpa: "Conservative screening-only allowable external pressure estimate (not final code check).",
  external_pressure_utilization: "Ratio of applied external pressure to screening allowable.",
  nozzle_opening_ratio: "Nozzle OD divided by vessel diameter; used for local opening severity screening.",
  nozzle_reinforcement_index: "Screening index of available reinforcement area over required area around opening.",
  reinforcement_pad_thickness_mm_used: "Pad thickness value used in nozzle reinforcement screen (mm).",
  reinforcement_pad_width_mm_used: "Pad width value used in nozzle reinforcement screen (mm).",

  // Rotating
  machine_type: "Rotating equipment class used for limit sets and logic branches.",
  driver_type: "Prime mover/driver architecture used to adjust dynamic limits and train risk.",
  service_criticality: "Criticality class that tightens limits and shortens inspection cadence.",
  stage_count: "Stage count (dynamic machines) or throw/cylinder count (reciprocating machines) used in combination scaling.",
  train_arrangement: "Mechanical train arrangement (e.g., overhung, between-bearing, integrally geared) used in combination logic.",
  casing_type: "Casing construction category used for vibration/nozzle allowance adjustment and compatibility checks.",
  bearing_type: "Bearing architecture used to tune vibration allowance and mismatch checks.",
  seal_system: "Seal philosophy used to adjust leakage/trip-process risk sensitivity.",
  lube_system: "Lubrication architecture used to tune thermal penalties and process-risk weighting.",
  vibration_mm_per_s: "Measured overall vibration velocity (mm/s).",
  vibration_limit_mm_per_s: "Reference vibration limit for the selected machine class (mm/s).",
  adjusted_vibration_limit_mm_per_s: "Vibration limit adjusted by driver type and service criticality factors (mm/s).",
  nozzle_load_ratio: "Applied nozzle load divided by allowable nozzle load.",
  nozzle_load_limit_ratio: "Screened nozzle-load ratio limit for selected machine class.",
  nozzle_load_limit_base_ratio: "Baseline nozzle-load ratio limit before train-arrangement adjustment.",
  bearing_temperature_c: "Bearing metal temperature used for health and alarm checks (C).",
  lube_oil_supply_temp_c: "Lube-oil supply temperature used for lubrication health screening (C).",
  coupling_misalignment_mils: "Coupling alignment error magnitude (mils).",
  axial_displacement_um: "Measured axial shaft displacement for compressor/turbine trains (um).",
  axial_displacement_limit_um: "Axial displacement warning limit for selected machine class (um).",
  speed_rpm: "Running shaft speed (revolutions per minute).",
  speed_low_limit_rpm: "Screened lower operating speed envelope bound (rpm).",
  speed_high_limit_rpm: "Screened upper operating speed envelope bound (rpm).",
  phase_change_risk_index: "Steam phase-change screening index derived from pressure/temperature/quality.",
  steam_pressure_bar: "Steam pressure used for saturation and superheat margin checks (bar).",
  steam_temperature_c: "Steam temperature used for phase-state screening (C).",
  steam_quality_x: "Dryness fraction x for wetness/erosion risk screening in steam turbines.",
  inlet_enthalpy_kj_per_kg: "Inlet steam enthalpy for turbine energy-drop consistency check (kJ/kg).",
  outlet_enthalpy_kj_per_kg: "Outlet steam enthalpy for turbine energy-drop consistency check (kJ/kg).",
  suction_pressure_bar: "Compressor train suction pressure used for pressure-ratio screening (bar).",
  discharge_pressure_bar: "Compressor train discharge pressure used for pressure-ratio screening (bar).",
  pressure_ratio: "Discharge-to-suction pressure ratio used for surge tendency checks.",
  surge_events_30d: "Count of anti-surge or surge-proximity events in the last 30 days.",
  npsh_available_m: "Available NPSH at pump suction condition (m).",
  npsh_required_m: "Required NPSH for selected pump operating point (m).",
  npsh_margin_m: "NPSH margin (available minus required) used for cavitation screening (m).",
  api670_coverage_pct: "Estimated percentage of required API 670 protection functions in service (%).",
  trip_tests_last_12m: "Executed protection trip tests in the last 12 months.",
  expected_trip_tests_per_year: "Required annual trip test count from selected criticality class.",
  protection_bypass_active: "Indicates whether key protection bypass is active.",
  mechanical_integrity_index: "0-10 index from vibration, load, temperature, displacement, and alignment penalties.",
  process_stability_index: "0-10 index from surge/pressure-ratio/NPSH/steam-state process risk penalties.",
  protection_readiness_index: "0-10 index from API 670 coverage, trip-test discipline, and bypass state.",
  bearing_health_index: "0-10 synthetic index from vibration, temperature, nozzle load, and phase risk.",
  driver_factor: "Multiplicative adjustment factor from selected driver type.",
  criticality_factor: "Multiplicative adjustment factor from selected service criticality.",
  stage_vibration_factor: "Multiplicative adjustment factor from stage/throw count complexity.",
  train_vibration_factor: "Multiplicative adjustment factor from selected train arrangement.",
  casing_vibration_factor: "Multiplicative adjustment factor from selected casing construction.",
  bearing_vibration_factor: "Multiplicative adjustment factor from selected bearing architecture.",
  train_nozzle_factor: "Multiplicative nozzle-load limit adjustment from train arrangement.",
  casing_nozzle_factor: "Multiplicative nozzle-load limit adjustment from casing construction.",
  seal_process_factor: "Multiplicative process-penalty factor from selected seal system.",
  lube_process_factor: "Multiplicative process-penalty factor from selected lube system.",
  lube_temperature_factor: "Multiplicative bearing/oil-temperature penalty factor from selected lube system.",

  // Electrical
  equipment_type: "Electrical asset category used for weighting and threshold logic.",
  system_voltage_kv: "Nominal operating voltage level (kV).",
  bolted_fault_current_ka: "Prospective bolted short-circuit current used in arc/interrupt checks (kA).",
  fault_current_ka: "Calculated/used fault current summary metric (kA).",
  clearing_time_sec: "Protection clearing time used in incident energy estimate (s).",
  working_distance_mm: "Distance from arc source to worker position for arc energy calculation (mm).",
  breaker_interrupt_rating_ka: "Breaker interrupting capacity compared to fault current (kA).",
  voltage_drop_percent: "Voltage drop at load point; compared with recommended limits.",
  thd_voltage_percent: "Voltage harmonic distortion level (THD-V).",
  motor_current_thd_percent: "Current harmonic distortion level (THD-I).",
  power_factor: "Power factor for utilization and power quality context.",
  dga_score: "Transformer dissolved gas analysis condition score (0-10).",
  oil_quality_score: "Insulating oil condition score (0-10).",
  insulation_score: "Insulation condition score (0-10).",
  load_factor_score: "Load stress/usage score (0-10).",
  transformer_health_index: "Weighted health index for transformer condition (0-10).",
  arc_flash_energy_cal_cm2: "Incident arc-flash energy at working distance (cal/cm2).",
  ppe_category: "Recommended PPE category derived from incident energy.",

  // Instrumentation
  instrument_type: "Instrument family used for drift and reliability biasing.",
  voting_architecture: "SIF voting architecture (e.g., 1oo1, 1oo2, 2oo3).",
  sil_target: "Required safety integrity level for the function.",
  sil_achieved: "Calculated SIL based on PFDavg result.",
  failure_rate_per_hour: "Dangerous failure rate used in PFDavg estimate (/h).",
  proof_test_interval_hours: "Proof-test interval used in demand-mode reliability model (hours).",
  mttr_hours: "Mean time to repair used in reliability model (hours).",
  calibration_interval_days: "Current calibration interval in operation (days).",
  calibration_interval_optimal_days: "Recommended calibration interval from drift trend and tolerance (days).",
  tolerance_pct: "Maximum allowable measurement error before calibration is required (%).",
  sensor_mtbf_years: "Mean time between failures for sensor reliability context (years).",
  cv_required: "Required valve flow coefficient for service conditions.",
  cv_rated: "Rated valve flow coefficient from datasheet.",
  pfdavg: "Average probability of failure on demand for SIS safety function.",
  predicted_drift_pct: "Predicted instrument error at current interval based on trend model (%).",

  // Steel
  member_type: "Structural member class for reporting and checks.",
  steel_grade: "Steel grade/class for strength context.",
  section_label: "Section designation used for traceability (e.g., W-shape label).",
  length_m: "Unsupported/effective member length used for buckling checks (m).",
  k_factor: "Effective length factor K for compression stability.",
  radius_of_gyration_mm: "Radius of gyration r used in slenderness calculation (mm).",
  yield_strength_mpa: "Steel yield strength Fy used in capacity calculation (MPa).",
  gross_area_mm2: "Gross cross-sectional area Ag (mm2).",
  axial_demand_kn: "Applied axial load demand (kN).",
  corrosion_loss_percent: "Estimated cross-section loss from corrosion (%).",
  deflection_mm: "Measured/estimated deflection at governing span location (mm).",
  span_mm: "Member span used to evaluate deflection serviceability ratio (mm).",
  connection_failure_detected: "Indicates observed weld/bolt connection failure evidence.",
  dc_ratio: "Demand-to-capacity ratio; values above 1 indicate overstress.",
  lambda_c: "Non-dimensional slenderness parameter for compression capacity.",
  phi_pn_kn: "Design compression strength (phi*Pn) in kN.",

  // Civil
  element_type: "Concrete element class for model context.",
  environment_exposure: "Exposure category used to adjust durability deterioration rate.",
  fc_mpa: "Specified concrete compressive strength f'c (MPa).",
  fy_mpa: "Reinforcing steel yield strength Fy (MPa).",
  width_mm: "Section width b used in flexural capacity calculation (mm).",
  effective_depth_mm: "Effective depth d used in flexural capacity calculation (mm).",
  rebar_area_mm2: "Tension reinforcement area As (mm2).",
  demand_moment_knm: "Applied flexural demand moment (kN*m).",
  lateral_capacity_loss_percent: "Estimated lateral system capacity loss (%).",
  affected_area_percent: "Damage-affected area ratio used in ACI 562 screening (%).",
  vertical_capacity_loss_percent: "Estimated vertical load capacity loss (%).",
  carbonation_coeff_mm_sqrt_year: "Carbonation coefficient k in depth model Xc = k*sqrt(t).",
  service_years: "Elapsed operating years used for durability prediction.",
  cover_thickness_mm: "Concrete cover to rebar used in corrosion initiation check (mm).",
  crack_width_mm: "Observed crack width used for durability/safety screening (mm).",
  spalling_area_percent: "Area ratio with concrete spalling (%).",
  foundation_settlement_mm: "Measured foundation settlement value (mm).",
  carbonation_depth_mm: "Predicted carbonation front depth at current age (mm).",
  years_to_corrosion_init: "Estimated years until carbonation reaches reinforcement depth.",
  substantial_damage: "ACI 562 substantial-damage condition indicator.",
};

function normalizeKey(value: string): string {
  return value
    .trim()
    .toLowerCase()
    .replace(/[\s\-:/()]+/g, "_")
    .replace(/_+/g, "_")
    .replace(/^_+|_+$/g, "");
}

function titleCaseFromKey(key: string): string {
  const normalized = key.replace(/[_\-/]+/g, " ").trim();
  if (!normalized) return "Term";
  return normalized
    .split(/\s+/)
    .map((token) => {
      if (token.length <= 3 && token === token.toUpperCase()) return token;
      const lower = token.toLowerCase();
      return `${lower.charAt(0).toUpperCase()}${lower.slice(1)}`;
    })
    .join(" ");
}

function inferDefinition(key: string): string {
  const normalized = normalizeKey(key);

  if (normalized.includes("layer_1")) return "Input schema and range validation layer.";
  if (normalized.includes("layer_2")) return "MAKER consensus verification layer.";
  if (normalized.includes("layer_3")) return "Physics and standards compliance guardrail layer.";
  if (normalized.includes("layer_4")) return "Reverse-calculation consistency verification layer.";
  if (normalized.endsWith("_mpa")) return "Engineering value reported in MPa.";
  if (normalized.endsWith("_bar")) return "Engineering value reported in bar.";
  if (normalized.endsWith("_kv")) return "Engineering value reported in kV.";
  if (normalized.endsWith("_ka")) return "Engineering value reported in kA.";
  if (normalized.endsWith("_mm")) return "Engineering value reported in mm.";
  if (normalized.endsWith("_rpm")) return "Engineering value reported in RPM.";
  if (normalized.endsWith("_years")) return "Engineering value reported in years.";
  if (normalized.endsWith("_hours")) return "Engineering value reported in hours.";
  if (normalized.endsWith("_days")) return "Engineering value reported in days.";
  if (normalized.endsWith("_percent") || normalized.endsWith("_pct")) return "Engineering percentage value used for integrity evaluation.";
  if (normalized.includes("ratio")) return "Engineering ratio used for limit comparison.";
  if (normalized.includes("temperature")) return "Temperature input used in standards applicability and risk checks.";
  if (normalized.includes("pressure")) return "Pressure input used in design and integrity checks.";
  if (normalized.includes("corrosion")) return "Corrosion-related input/output used for life and inspection decisions.";
  if (normalized.includes("vibration")) return "Vibration metric used for rotating equipment reliability checks.";
  if (normalized.includes("health_index")) return "Condition index where lower values indicate higher risk.";
  if (normalized.includes("status")) return "Final classification after calculation and verification.";

  return "Engineering term used in the calculation and verification workflow.";
}

const NORMALIZED_LABELS: Record<string, string> = {};
const NORMALIZED_DEFINITIONS: Record<string, string> = {};

for (const [key, value] of Object.entries(TERM_LABELS)) {
  NORMALIZED_LABELS[normalizeKey(key)] = value;
}

for (const [key, value] of Object.entries(TERM_DEFINITIONS)) {
  NORMALIZED_DEFINITIONS[normalizeKey(key)] = value;
}

export function getTermLabel(term: string, fallback?: string): string {
  if (!term) return fallback ?? "Term";
  return TERM_LABELS[term]
    ?? NORMALIZED_LABELS[normalizeKey(term)]
    ?? fallback
    ?? titleCaseFromKey(term);
}

export function getTermDefinition(term: string): string {
  if (!term) return "Engineering term used in the calculation and verification workflow.";
  return TERM_DEFINITIONS[term]
    ?? NORMALIZED_DEFINITIONS[normalizeKey(term)]
    ?? inferDefinition(term);
}

export function getGlossarySize(): number {
  return Object.keys(TERM_DEFINITIONS).length;
}

export interface GlossaryEntry {
  key: string;
  label: string;
  description: string;
  discipline: Exclude<GlossaryDiscipline, "all">;
}

export interface TermDeepGuidance {
  engineeringIntent: string;
  calculationContext: string;
  inputChecks: string[];
  commonMisses: string[];
  relatedStandards: string[];
}

function inferTermDiscipline(key: string): Exclude<GlossaryDiscipline, "all"> {
  const normalized = normalizeKey(key);

  const commonKeys = new Set([
    "layer_1_input_validation",
    "layer_2_maker_consensus",
    "layer_3_physics_and_standards",
    "layer_4_reverse_verification",
    "confidence",
    "execution_time_sec",
    "references",
    "status",
  ]);
  if (commonKeys.has(normalized) || normalized.startsWith("layer_")) return "common";

  if (
    normalized.includes("vessel")
    || normalized.includes("inside_radius")
    || normalized.includes("head_")
    || normalized.includes("nozzle_")
    || normalized.includes("external_pressure")
    || normalized.includes("reinforcement_pad")
    || normalized.includes("slenderness_ld")
    || normalized.includes("shell_surface")
  ) return "vessel";

  if (
    normalized.includes("nps")
    || normalized.includes("weld")
    || normalized.includes("service_type")
    || normalized.includes("fluid_type")
    || normalized.includes("chloride")
    || normalized.includes("temperature_profile")
    || normalized.includes("t_min")
    || normalized.includes("cr_selected")
  ) return "piping";

  if (
    normalized.includes("machine_type")
    || normalized.includes("driver_type")
    || normalized.includes("criticality")
    || normalized.includes("stage_count")
    || normalized.includes("train_arrangement")
    || normalized.includes("casing_type")
    || normalized.includes("lube_system")
    || normalized.includes("driver_factor")
    || normalized.includes("stage_vibration_factor")
    || normalized.includes("casing_vibration_factor")
    || normalized.includes("casing_nozzle_factor")
    || normalized.includes("lube_process_factor")
    || normalized.includes("lube_temperature_factor")
    || normalized.includes("api670")
    || normalized.includes("vibration")
    || normalized.includes("bearing")
    || normalized.includes("lube_oil")
    || normalized.includes("axial_displacement")
    || normalized.includes("misalignment")
    || normalized.includes("steam_")
    || normalized.includes("enthalpy")
    || normalized.includes("speed_rpm")
    || normalized.includes("phase_change")
    || normalized.includes("pressure_ratio")
    || normalized.includes("surge_")
    || normalized.includes("npsh_")
    || normalized.includes("protection_readiness")
    || normalized.includes("mechanical_integrity")
    || normalized.includes("process_stability")
  ) return "rotating";

  if (
    normalized.includes("fault_current")
    || normalized.includes("arc_flash")
    || normalized.includes("transformer")
    || normalized.includes("voltage")
    || normalized.includes("breaker")
    || normalized.includes("power_factor")
    || normalized.includes("thd_")
  ) return "electrical";

  if (
    normalized.includes("instrument")
    || normalized.includes("sil_")
    || normalized.includes("pfdavg")
    || normalized.includes("proof_test")
    || normalized.includes("calibration")
    || normalized.includes("drift")
    || normalized.includes("sensor_mtbf")
    || normalized.includes("cv_")
  ) return "instrumentation";

  if (
    normalized.includes("steel")
    || normalized.includes("member_type")
    || normalized.includes("section_label")
    || normalized.includes("yield_strength")
    || normalized.includes("axial_demand")
    || normalized.includes("phi_pn")
    || normalized.includes("lambda_c")
    || normalized.includes("dc_ratio")
  ) return "steel";

  if (
    normalized.includes("civil")
    || normalized.includes("concrete")
    || normalized.includes("carbonation")
    || normalized.includes("spalling")
    || normalized.includes("foundation")
    || normalized.includes("crack_width")
    || normalized.includes("fc_mpa")
    || normalized.includes("fy_mpa")
    || normalized.includes("rebar")
    || normalized.includes("substantial_damage")
  ) return "civil";

  return "common";
}

function buildPriorityMap(keys: string[]): Record<string, number> {
  return keys.reduce<Record<string, number>>((acc, key, index) => {
    acc[normalizeKey(key)] = index + 1;
    return acc;
  }, {});
}

const COMMON_PRIORITY = buildPriorityMap([
  "material",
  "design_pressure_mpa",
  "design_temperature_c",
  "t_current_mm",
  "t_min_mm",
  "remaining_life_years",
  "inspection_interval_years",
  "status",
  "confidence",
  "references",
]);

const DISCIPLINE_PRIORITY: Record<Exclude<GlossaryDiscipline, "all">, Record<string, number>> = {
  common: buildPriorityMap([
    "Layer 1: Input Validation",
    "Layer 2: MAKER Consensus",
    "Layer 3: Physics and Standards",
    "Layer 4: Reverse Verification",
    "confidence",
    "execution_time_sec",
    "status",
    "references",
  ]),
  piping: buildPriorityMap([
    "material",
    "design_pressure_mpa",
    "design_temperature_c",
    "nps",
    "weld_type",
    "service_type",
    "fluid_type",
    "corrosion_allowance_mm",
    "chloride_ppm",
    "allowable_stress_mpa",
    "weld_efficiency",
    "t_min_mm",
    "cr_selected_mm_per_year",
    "remaining_life_years",
    "inspection_interval_years",
    "temperature_profile",
  ]),
  vessel: buildPriorityMap([
    "material",
    "vessel_type",
    "design_pressure_mpa",
    "design_temperature_c",
    "inside_radius_mm",
    "shell_length_mm",
    "straight_shell_height_mm",
    "head_type",
    "head_depth_mm",
    "nozzle_od_mm",
    "joint_efficiency",
    "t_required_shell_mm",
    "remaining_life_years",
    "inspection_interval_years",
    "external_pressure_utilization",
    "nozzle_reinforcement_index",
    "slenderness_ld_ratio",
  ]),
  rotating: buildPriorityMap([
    "machine_type",
    "driver_type",
    "service_criticality",
    "stage_count",
    "train_arrangement",
    "casing_type",
    "bearing_type",
    "seal_system",
    "lube_system",
    "vibration_mm_per_s",
    "vibration_limit_mm_per_s",
    "adjusted_vibration_limit_mm_per_s",
    "nozzle_load_ratio",
    "nozzle_load_limit_ratio",
    "nozzle_load_limit_base_ratio",
    "bearing_temperature_c",
    "lube_oil_supply_temp_c",
    "coupling_misalignment_mils",
    "axial_displacement_um",
    "speed_rpm",
    "speed_low_limit_rpm",
    "speed_high_limit_rpm",
    "mechanical_integrity_index",
    "process_stability_index",
    "protection_readiness_index",
    "api670_coverage_pct",
    "trip_tests_last_12m",
    "protection_bypass_active",
    "bearing_health_index",
    "driver_factor",
    "criticality_factor",
    "stage_vibration_factor",
    "train_vibration_factor",
    "casing_vibration_factor",
    "bearing_vibration_factor",
    "train_nozzle_factor",
    "casing_nozzle_factor",
    "seal_process_factor",
    "lube_process_factor",
    "lube_temperature_factor",
    "pressure_ratio",
    "surge_events_30d",
    "npsh_margin_m",
    "phase_change_risk_index",
    "steam_pressure_bar",
    "steam_temperature_c",
    "steam_quality_x",
  ]),
  electrical: buildPriorityMap([
    "equipment_type",
    "system_voltage_kv",
    "fault_current_ka",
    "bolted_fault_current_ka",
    "clearing_time_sec",
    "working_distance_mm",
    "arc_flash_energy_cal_cm2",
    "breaker_interrupt_rating_ka",
    "voltage_drop_percent",
    "transformer_health_index",
    "ppe_category",
  ]),
  instrumentation: buildPriorityMap([
    "instrument_type",
    "sil_target",
    "sil_achieved",
    "pfdavg",
    "failure_rate_per_hour",
    "proof_test_interval_hours",
    "mttr_hours",
    "calibration_interval_days",
    "calibration_interval_optimal_days",
    "predicted_drift_pct",
    "sensor_mtbf_years",
  ]),
  steel: buildPriorityMap([
    "member_type",
    "steel_grade",
    "section_label",
    "length_m",
    "k_factor",
    "yield_strength_mpa",
    "axial_demand_kn",
    "dc_ratio",
    "phi_pn_kn",
    "lambda_c",
    "deflection_mm",
  ]),
  civil: buildPriorityMap([
    "element_type",
    "environment_exposure",
    "fc_mpa",
    "fy_mpa",
    "demand_moment_knm",
    "carbonation_depth_mm",
    "years_to_corrosion_init",
    "crack_width_mm",
    "spalling_area_percent",
    "foundation_settlement_mm",
    "substantial_damage",
  ]),
};

function glossaryPriority(entry: GlossaryEntry, activeDiscipline: GlossaryDiscipline): number {
  const normalized = normalizeKey(entry.key);
  const disciplineKey = entry.discipline;

  if (activeDiscipline !== "all") {
    const activePriority = DISCIPLINE_PRIORITY[activeDiscipline]?.[normalized];
    if (activePriority !== undefined) return activePriority;
  }

  const disciplinePriority = DISCIPLINE_PRIORITY[disciplineKey]?.[normalized];
  if (disciplinePriority !== undefined) return disciplinePriority + 40;

  const commonPriority = COMMON_PRIORITY[normalized];
  if (commonPriority !== undefined) return commonPriority + 80;

  return 1000;
}

export function getGlossaryEntries(discipline: GlossaryDiscipline = "all"): GlossaryEntry[] {
  const allEntries: GlossaryEntry[] = Object.entries(TERM_DEFINITIONS)
    .map(([key, description]) => ({
      key,
      label: getTermLabel(key),
      description,
      discipline: inferTermDiscipline(key),
    }));

  const scopedEntries = discipline === "all"
    ? allEntries
    : allEntries.filter((entry) => entry.discipline === discipline || entry.discipline === "common");

  scopedEntries.sort((a, b) => {
    const priorityDiff = glossaryPriority(a, discipline) - glossaryPriority(b, discipline);
    if (priorityDiff !== 0) return priorityDiff;
    return a.label.localeCompare(b.label);
  });

  return scopedEntries;
}

function guidanceForDiscipline(discipline: Exclude<GlossaryDiscipline, "all">): TermDeepGuidance {
  if (discipline === "piping") {
    return {
      engineeringIntent: "Control pressure boundary integrity and corrosion-driven life management.",
      calculationContext: "Used in minimum thickness, corrosion rate, remaining life, and inspection interval decisions.",
      inputChecks: [
        "Material/temperature basis and allowable stress source",
        "Measured thickness history quality and date spacing",
        "Corrosion allowance, service severity, and fluid category alignment",
      ],
      commonMisses: [
        "Mixing nominal vs measured thickness basis",
        "Using short-term outlier data as long-term corrosion trend",
      ],
      relatedStandards: ["ASME B31.3 Para 304.1.2", "ASME B31.3 Table A-1", "API 570 Section 7"],
    };
  }

  if (discipline === "vessel") {
    return {
      engineeringIntent: "Maintain vessel shell/opening integrity under internal and external pressure effects.",
      calculationContext: "Used in required thickness, external-pressure stability, and nozzle reinforcement screening.",
      inputChecks: [
        "Geometry basis: radius/span/head assumptions",
        "Joint efficiency and corrosion-rate assumptions",
        "Opening/nozzle and reinforcement dimensions at current condition",
      ],
      commonMisses: [
        "Treating external-pressure cases with internal-pressure-only logic",
        "Ignoring localized thinning near openings",
      ],
      relatedStandards: ["ASME VIII Div.1 UG-27", "ASME VIII Div.1 UG-28", "ASME VIII Div.1 UG-37", "API 510"],
    };
  }

  if (discipline === "rotating") {
    return {
      engineeringIntent: "Reduce rotating train trip/failure risk using machine-driver-criticality-aware thresholds.",
      calculationContext: "Used in vibration/nozzle/temperature screening, surge/NPSH risk, and protection readiness.",
      inputChecks: [
        "Machine type and driver topology consistency",
        "Speed envelope, vibration trend, and axial/alignment condition",
        "API 670 coverage, trip-test evidence, and bypass status",
      ],
      commonMisses: [
        "Applying one fixed vibration limit across all machine/driver combinations",
        "Ignoring repeated surge events as leading indicators",
      ],
      relatedStandards: ["API 610", "API 674", "API 617", "API 618", "API 619", "API 670", "ISO 20816-3"],
    };
  }

  if (discipline === "electrical") {
    return {
      engineeringIntent: "Prevent personnel and equipment risk from arc-flash and short-circuit mismatch.",
      calculationContext: "Used in incident-energy screening, interrupting-rating checks, and power-quality review.",
      inputChecks: [
        "Fault current and clearing time basis",
        "Working distance and equipment context",
        "Breaker rating and coordination study revision date",
      ],
      commonMisses: [
        "Using stale protection settings after relay or breaker change",
        "Treating voltage distortion symptoms without source checks",
      ],
      relatedStandards: ["IEEE 1584"],
    };
  }

  if (discipline === "instrumentation") {
    return {
      engineeringIntent: "Sustain functional safety performance and instrumentation reliability over lifecycle.",
      calculationContext: "Used in SIL/PFDavg checks, drift forecasting, and calibration interval optimization.",
      inputChecks: [
        "Failure-rate and test-coverage assumptions",
        "Proof-test interval and MTTR realism",
        "Drift trend data quality and tolerance definition",
      ],
      commonMisses: [
        "Declaring SIL compliance without current proof-test evidence",
        "Setting calibration interval by habit instead of trend data",
      ],
      relatedStandards: ["IEC 61511", "API 670"],
    };
  }

  if (discipline === "steel") {
    return {
      engineeringIntent: "Prevent overstress and instability in steel members and connections.",
      calculationContext: "Used in slenderness/capacity checks and demand-capacity screening.",
      inputChecks: [
        "Effective length and boundary condition assumptions",
        "Corrosion section-loss adjustment in area/capacity",
        "Demand combination consistency",
      ],
      commonMisses: [
        "Using original section properties after measurable corrosion loss",
        "Ignoring serviceability signals before strength exceedance",
      ],
      relatedStandards: ["AISC 360"],
    };
  }

  if (discipline === "civil") {
    return {
      engineeringIntent: "Control concrete member risk via capacity and durability progression checks.",
      calculationContext: "Used in flexural D/C, carbonation progression, and substantial-damage screening.",
      inputChecks: [
        "Material strengths and reinforcement quantities",
        "Demand moment and section geometry basis",
        "Durability indicators: crack, spall, cover, exposure",
      ],
      commonMisses: [
        "Treating durability degradation as cosmetic only",
        "Not linking deterioration rate to environment severity",
      ],
      relatedStandards: ["ACI 318 / ACI 562"],
    };
  }

  return {
    engineeringIntent: "Provide traceable engineering terminology for cross-discipline verification layers.",
    calculationContext: "Used in confidence, status, and cross-check communication across workbench outputs.",
    inputChecks: [
      "Definition consistency across views and reports",
      "Unit consistency and rounding policy",
      "Traceability to calculation and standard references",
    ],
    commonMisses: [
      "Ambiguous term naming between similar indicators",
      "Using convenience labels without definition alignment",
    ],
    relatedStandards: ["ASME B31.3 Table A-1", "API 670"],
  };
}

function keySpecificGuidance(normalizedKey: string): Partial<TermDeepGuidance> | null {
  if (normalizedKey === "remaining_life_years") {
    return {
      engineeringIntent: "Quantify time-to-limit to prioritize inspection and replacement.",
      calculationContext: "Derived from thickness margin divided by selected corrosion rate.",
      inputChecks: [
        "Current thickness measurement confidence",
        "Selected corrosion rate conservatism",
        "Minimum required thickness basis consistency",
      ],
      commonMisses: [
        "Using optimistic corrosion rate under uncertain data",
        "Ignoring minimum practical interval caps from site policy",
      ],
    };
  }

  if (normalizedKey === "inspection_interval_years") {
    return {
      engineeringIntent: "Set next inspection timing before risk escalation.",
      calculationContext: "Bounded by remaining life, code maxima, and active warning/red flags.",
      inputChecks: [
        "Interval cap source and discipline-specific rule",
        "Presence of blocking red flags or warnings",
        "Criticality and consequence classification",
      ],
      commonMisses: [
        "Applying one fixed interval across all assets",
        "Ignoring active warnings when scheduling interval",
      ],
    };
  }

  if (normalizedKey === "t_min_mm" || normalizedKey === "t_required_shell_mm") {
    return {
      engineeringIntent: "Define non-negotiable minimum section needed to satisfy pressure design basis.",
      calculationContext: "Governing thickness output used as release threshold against measured minimum.",
      inputChecks: [
        "Correct formula branch and coefficients",
        "Design pressure/temperature basis recency",
        "Corrosion allowance and efficiency factor use",
      ],
      commonMisses: [
        "Comparing with nominal instead of measured effective thickness",
        "Missing allowance terms in downstream comparison",
      ],
    };
  }

  if (normalizedKey === "external_pressure_utilization") {
    return {
      engineeringIntent: "Expose shell stability margin under external pressure demand.",
      calculationContext: "Ratio of applied external pressure to screened allowable.",
      inputChecks: [
        "Span/geometry assumptions for stability screening",
        "Actual thinned thickness in worst zone",
        "Boundary/support condition realism",
      ],
      commonMisses: [
        "Using internal-pressure margin as substitute for stability margin",
        "Ignoring vacuum/upset scenarios in demand basis",
      ],
    };
  }

  if (
    normalizedKey === "mechanical_integrity_index"
    || normalizedKey === "process_stability_index"
    || normalizedKey === "protection_readiness_index"
    || normalizedKey === "bearing_health_index"
  ) {
    return {
      engineeringIntent: "Condense multi-signal risk into an operationally actionable index.",
      calculationContext: "Penalty-based score from dynamic response, process stability, and protection-state inputs.",
      inputChecks: [
        "Input signal freshness and sensor validity",
        "Penalty weights aligned with current criticality class",
        "Consistency between index trend and raw indicators",
      ],
      commonMisses: [
        "Overriding index interpretation without checking raw evidence",
        "Treating one-time spike as permanent degradation",
      ],
    };
  }

  if (normalizedKey === "pressure_ratio" || normalizedKey === "surge_events_30d" || normalizedKey === "npsh_margin_m") {
    return {
      engineeringIntent: "Detect process-induced rotating risk before mechanical damage acceleration.",
      calculationContext: "Used in compressor surge tendency and pump cavitation screening branches.",
      inputChecks: [
        "Suction/discharge pressure validity and timestamp alignment",
        "Event logging completeness and threshold definition",
        "Operating mode consistency (startup, transient, steady)",
      ],
      commonMisses: [
        "Discarding near-surge repeats as nuisance alarms",
        "Ignoring low NPSH margin during high-demand periods",
      ],
    };
  }

  if (normalizedKey === "arc_flash_energy_cal_cm2" || normalizedKey === "breaker_interrupt_rating_ka") {
    return {
      engineeringIntent: "Keep personnel exposure and interrupting capability within safe design envelope.",
      calculationContext: "Incident energy and interrupt checks use fault current and clearing time as dominant drivers.",
      inputChecks: [
        "Protection clearing time from latest settings",
        "Fault-duty basis vs installed equipment data",
        "Working-distance and scenario assumptions",
      ],
      commonMisses: [
        "Using outdated coordination study values",
        "Accepting close margins without mitigation plan",
      ],
    };
  }

  if (normalizedKey === "pfdavg" || normalizedKey === "sil_target" || normalizedKey === "sil_achieved") {
    return {
      engineeringIntent: "Verify demanded risk reduction is demonstrably achieved by SIS design and operation.",
      calculationContext: "PFDavg-based SIL achievement depends on architecture, test interval, and repair assumptions.",
      inputChecks: [
        "Failure-rate and architecture factor basis",
        "Proof-test interval and coverage assumptions",
        "Observed maintenance/repair response vs model",
      ],
      commonMisses: [
        "Assuming SIL achieved with stale proof-test assumptions",
        "Ignoring bypass/override duration in practical risk",
      ],
    };
  }

  if (normalizedKey === "calibration_interval_optimal_days" || normalizedKey === "predicted_drift_pct") {
    return {
      engineeringIntent: "Balance measurement reliability against calibration workload through evidence-based interval setting.",
      calculationContext: "Derived from drift trend slope/intercept and tolerance crossing constraints.",
      inputChecks: [
        "Drift sample quantity and representativeness",
        "Tolerance definition and unit consistency",
        "Confidence bound treatment in interval recommendation",
      ],
      commonMisses: [
        "Extending interval beyond uncertainty-backed limit",
        "Ignoring process upsets that invalidate trend continuity",
      ],
    };
  }

  if (normalizedKey === "dc_ratio" || normalizedKey === "lambda_c") {
    return {
      engineeringIntent: "Detect strength/stability exceedance risk in structural members.",
      calculationContext: "Compares demand against design capacity after section and slenderness effects.",
      inputChecks: [
        "Demand load combination and directionality",
        "Capacity with corrosion-adjusted properties",
        "Buckling/slenderness assumptions",
      ],
      commonMisses: [
        "Checking only D/C without confirming capacity model assumptions",
        "Missing connection condition degradation impact",
      ],
    };
  }

  if (normalizedKey === "carbonation_depth_mm" || normalizedKey === "years_to_corrosion_init" || normalizedKey === "substantial_damage") {
    return {
      engineeringIntent: "Identify durability-to-capacity transition before abrupt reliability loss.",
      calculationContext: "Carbonation progression and damage criteria feed repair urgency prioritization.",
      inputChecks: [
        "Exposure class and deterioration coefficient validity",
        "Cover depth and crack/spall field measurements",
        "Consistency between durability indicators and structural demand",
      ],
      commonMisses: [
        "Treating corrosion-initiation prediction as exact timestamp",
        "Delaying intervention despite combined durability and capacity signals",
      ],
    };
  }

  if (normalizedKey === "confidence" || normalizedKey === "status") {
    return {
      engineeringIntent: "Provide clear release-state communication after multi-layer verification.",
      calculationContext: "Synthesized from layer outcomes, issue severity, and unresolved risk conditions.",
      inputChecks: [
        "Layer pass/fail traceability",
        "Warning/red-flag severity classification",
        "Consistency between displayed status and decision rules",
      ],
      commonMisses: [
        "Interpreting medium confidence as release approval by default",
        "Ignoring blocked logic when manual overrides occur",
      ],
    };
  }

  return null;
}

export function getTermDeepGuidance(term: string): TermDeepGuidance {
  const key = normalizeKey(term);
  const discipline = inferTermDiscipline(term);
  const base = guidanceForDiscipline(discipline);
  const specific = keySpecificGuidance(key);

  if (!specific) return base;

  return {
    engineeringIntent: specific.engineeringIntent ?? base.engineeringIntent,
    calculationContext: specific.calculationContext ?? base.calculationContext,
    inputChecks: specific.inputChecks ?? base.inputChecks,
    commonMisses: specific.commonMisses ?? base.commonMisses,
    relatedStandards: specific.relatedStandards ?? base.relatedStandards,
  };
}
