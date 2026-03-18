import { DisciplineConfig } from "@/lib/types";
import { DisciplineOutcome, round, toNumber } from "@/lib/mock/shared";

type MachineType =
  | "pump"
  | "recip_pump"
  | "compressor"
  | "centrifugal_compressor"
  | "axial_compressor"
  | "screw_compressor"
  | "recip_compressor"
  | "steam_turbine"
  | "gas_turbine"
  | "blower"
  | "fan"
  | "gearbox"
  | "expander";

type DriverType =
  | "electric_motor_fixed"
  | "electric_motor_vfd"
  | "steam_turbine_driver"
  | "gas_turbine_driver"
  | "recip_engine_driver"
  | "integral_prime_mover";

type ServiceCriticality = "normal" | "essential" | "high_critical" | "safety_critical";

type TrainArrangement = "overhung" | "between_bearing" | "integrally_geared" | "barrel" | "inline";

type BearingType = "rolling_element" | "journal_tilting_pad" | "sleeve" | "crosshead";

type SealSystem = "single_mech" | "dual_mech" | "dry_gas_seal" | "packing";

type CasingType = "horiz_split" | "vert_split" | "barrel" | "recip_frame" | "integral_gear_case";

type LubeSystem = "ring_oil" | "forced_lube" | "mist" | "none_process_fluid";

const MACHINE_TYPES = new Set<MachineType>([
  "pump",
  "recip_pump",
  "compressor",
  "centrifugal_compressor",
  "axial_compressor",
  "screw_compressor",
  "recip_compressor",
  "steam_turbine",
  "gas_turbine",
  "blower",
  "fan",
  "gearbox",
  "expander",
]);

const DRIVER_TYPES = new Set<DriverType>([
  "electric_motor_fixed",
  "electric_motor_vfd",
  "steam_turbine_driver",
  "gas_turbine_driver",
  "recip_engine_driver",
  "integral_prime_mover",
]);

const SERVICE_CRITICALITIES = new Set<ServiceCriticality>([
  "normal",
  "essential",
  "high_critical",
  "safety_critical",
]);

const TRAIN_ARRANGEMENTS = new Set<TrainArrangement>([
  "overhung",
  "between_bearing",
  "integrally_geared",
  "barrel",
  "inline",
]);

const BEARING_TYPES = new Set<BearingType>([
  "rolling_element",
  "journal_tilting_pad",
  "sleeve",
  "crosshead",
]);

const SEAL_SYSTEMS = new Set<SealSystem>([
  "single_mech",
  "dual_mech",
  "dry_gas_seal",
  "packing",
]);

const CASING_TYPES = new Set<CasingType>([
  "horiz_split",
  "vert_split",
  "barrel",
  "recip_frame",
  "integral_gear_case",
]);

const LUBE_SYSTEMS = new Set<LubeSystem>([
  "ring_oil",
  "forced_lube",
  "mist",
  "none_process_fluid",
]);

const AXIAL_MACHINES = new Set<MachineType>([
  "compressor",
  "centrifugal_compressor",
  "axial_compressor",
  "screw_compressor",
  "recip_compressor",
  "steam_turbine",
  "gas_turbine",
  "expander",
]);

const PRESSURE_RATIO_MACHINES = new Set<MachineType>([
  "compressor",
  "centrifugal_compressor",
  "axial_compressor",
  "screw_compressor",
  "recip_compressor",
  "expander",
]);

const PUMP_MACHINES = new Set<MachineType>([
  "pump",
  "recip_pump",
]);

const ROTODYNAMIC_COMPRESSORS = new Set<MachineType>([
  "compressor",
  "centrifugal_compressor",
  "axial_compressor",
]);

const POSITIVE_DISPLACEMENT_COMPRESSORS = new Set<MachineType>([
  "screw_compressor",
  "recip_compressor",
]);

export const ROTATING_STANDARD_REFS = [
  "API 610 centrifugal pump vibration/nozzle-load limits",
  "API 674 reciprocating positive-displacement pump context",
  "API 617 axial/centrifugal compressor integrity context",
  "API 618 reciprocating compressor mechanical integrity context",
  "API 619 rotary positive-displacement compressor context",
  "API 672 packaged/integrally geared compressor context",
  "API 611/API 612 steam turbine train context",
  "API 616 gas turbine train context",
  "API 670 machinery protection and trip logic",
  "ISO 20816-3 vibration severity guidance",
];

export const ROTATING_DEFAULT_RESULTS: Record<string, unknown> = {
  machine_type: "pump",
  driver_type: "electric_motor_fixed",
  service_criticality: "normal",
  stage_count: 1,
  train_arrangement: "overhung",
  casing_type: "horiz_split",
  bearing_type: "rolling_element",
  seal_system: "single_mech",
  lube_system: "ring_oil",
  vibration_mm_per_s: 2.5,
  vibration_limit_mm_per_s: 3.0,
  adjusted_vibration_limit_mm_per_s: 3.0,
  nozzle_load_ratio: 0.85,
  nozzle_load_limit_ratio: 1.0,
  bearing_temperature_c: 72,
  lube_oil_supply_temp_c: 56,
  speed_rpm: 1800,
  mechanical_integrity_index: 8.5,
  process_stability_index: 8.9,
  protection_readiness_index: 8.8,
  bearing_health_index: 8.1,
  inspection_interval_years: 2,
  status: "ACCEPTABLE",
  monitoring_escalation: "QUARTERLY_ROUTE",
  maintenance_urgency: "ROUTINE",
};

const ROTATING_VIBRATION_LIMIT_MM_PER_S: Record<MachineType, number> = {
  pump: 3.0,
  recip_pump: 5.4,
  compressor: 4.5,
  centrifugal_compressor: 4.5,
  axial_compressor: 4.0,
  screw_compressor: 5.1,
  recip_compressor: 6.0,
  steam_turbine: 4.0,
  gas_turbine: 4.5,
  blower: 4.8,
  fan: 5.0,
  gearbox: 3.5,
  expander: 4.2,
};

const ROTATING_NOZZLE_LOAD_LIMIT_RATIO: Record<MachineType, number> = {
  pump: 1.0,
  recip_pump: 0.95,
  compressor: 0.95,
  centrifugal_compressor: 0.95,
  axial_compressor: 0.9,
  screw_compressor: 0.92,
  recip_compressor: 0.9,
  steam_turbine: 0.95,
  gas_turbine: 0.95,
  blower: 1.0,
  fan: 1.05,
  gearbox: 1.0,
  expander: 0.95,
};

const ROTATING_SPEED_ENVELOPE_RPM: Record<MachineType, { low: number; high: number }> = {
  pump: { low: 600, high: 8000 },
  recip_pump: { low: 80, high: 900 },
  compressor: { low: 2000, high: 25000 },
  centrifugal_compressor: { low: 2000, high: 25000 },
  axial_compressor: { low: 3500, high: 22000 },
  screw_compressor: { low: 1200, high: 10000 },
  recip_compressor: { low: 250, high: 1800 },
  steam_turbine: { low: 3000, high: 18000 },
  gas_turbine: { low: 3000, high: 20000 },
  blower: { low: 800, high: 15000 },
  fan: { low: 300, high: 5000 },
  gearbox: { low: 300, high: 12000 },
  expander: { low: 1500, high: 18000 },
};

const ROTATING_AXIAL_DISPLACEMENT_LIMIT_UM: Record<MachineType, number> = {
  pump: 0,
  recip_pump: 0,
  compressor: 80,
  centrifugal_compressor: 80,
  axial_compressor: 70,
  screw_compressor: 60,
  recip_compressor: 110,
  steam_turbine: 75,
  gas_turbine: 80,
  blower: 0,
  fan: 0,
  gearbox: 0,
  expander: 70,
};

const DRIVER_VIBRATION_FACTOR: Record<DriverType, number> = {
  electric_motor_fixed: 1.0,
  electric_motor_vfd: 0.95,
  steam_turbine_driver: 0.93,
  gas_turbine_driver: 0.92,
  recip_engine_driver: 0.9,
  integral_prime_mover: 0.98,
};

const SERVICE_CRITICALITY_FACTOR: Record<ServiceCriticality, number> = {
  normal: 1.0,
  essential: 0.95,
  high_critical: 0.92,
  safety_critical: 0.88,
};

const TRAIN_VIBRATION_FACTOR: Record<TrainArrangement, number> = {
  overhung: 1.0,
  between_bearing: 0.96,
  integrally_geared: 0.94,
  barrel: 0.95,
  inline: 0.98,
};

const TRAIN_NOZZLE_FACTOR: Record<TrainArrangement, number> = {
  overhung: 1.0,
  between_bearing: 0.97,
  integrally_geared: 0.96,
  barrel: 0.95,
  inline: 0.98,
};

const BEARING_VIBRATION_FACTOR: Record<BearingType, number> = {
  rolling_element: 1.0,
  journal_tilting_pad: 0.95,
  sleeve: 0.97,
  crosshead: 1.04,
};

const SEAL_PROCESS_FACTOR: Record<SealSystem, number> = {
  single_mech: 1.0,
  dual_mech: 0.96,
  dry_gas_seal: 0.92,
  packing: 1.08,
};

const CASING_VIBRATION_FACTOR: Record<CasingType, number> = {
  horiz_split: 1.0,
  vert_split: 0.98,
  barrel: 0.96,
  recip_frame: 1.05,
  integral_gear_case: 0.95,
};

const CASING_NOZZLE_FACTOR: Record<CasingType, number> = {
  horiz_split: 1.0,
  vert_split: 0.98,
  barrel: 0.94,
  recip_frame: 0.96,
  integral_gear_case: 0.95,
};

const LUBE_PROCESS_FACTOR: Record<LubeSystem, number> = {
  ring_oil: 1.0,
  forced_lube: 0.95,
  mist: 1.06,
  none_process_fluid: 1.1,
};

const LUBE_TEMPERATURE_FACTOR: Record<LubeSystem, number> = {
  ring_oil: 1.0,
  forced_lube: 0.9,
  mist: 1.08,
  none_process_fluid: 1.12,
};

const EXPECTED_TRIP_TESTS_PER_YEAR: Record<ServiceCriticality, number> = {
  normal: 2,
  essential: 4,
  high_critical: 6,
  safety_critical: 8,
};

const PRESSURE_RATIO_WARNING_LIMIT: Record<MachineType, number> = {
  pump: Number.POSITIVE_INFINITY,
  recip_pump: Number.POSITIVE_INFINITY,
  compressor: 4.5,
  centrifugal_compressor: 4.5,
  axial_compressor: 3.8,
  screw_compressor: 6.0,
  recip_compressor: 6.0,
  steam_turbine: Number.POSITIVE_INFINITY,
  gas_turbine: Number.POSITIVE_INFINITY,
  blower: Number.POSITIVE_INFINITY,
  fan: Number.POSITIVE_INFINITY,
  gearbox: Number.POSITIVE_INFINITY,
  expander: 5.0,
};

const PRESSURE_RATIO_CRITICAL_LIMIT: Record<MachineType, number> = {
  pump: Number.POSITIVE_INFINITY,
  recip_pump: Number.POSITIVE_INFINITY,
  compressor: 6.0,
  centrifugal_compressor: 6.0,
  axial_compressor: 5.0,
  screw_compressor: 8.0,
  recip_compressor: 8.0,
  steam_turbine: Number.POSITIVE_INFINITY,
  gas_turbine: Number.POSITIVE_INFINITY,
  blower: Number.POSITIVE_INFINITY,
  fan: Number.POSITIVE_INFINITY,
  gearbox: Number.POSITIVE_INFINITY,
  expander: 6.5,
};

const STEAM_SATURATION_POINTS_BAR_C: Array<[number, number]> = [
  [1.0, 99.6],
  [5.0, 151.8],
  [10.0, 179.9],
  [20.0, 212.4],
  [40.0, 250.4],
  [60.0, 275.6],
  [80.0, 295.0],
  [100.0, 311.0],
  [160.0, 345.0],
  [220.0, 374.0],
];

function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

function pickMachineType(raw: unknown): MachineType {
  const candidate = String(raw ?? "").toLowerCase() as MachineType;
  return MACHINE_TYPES.has(candidate) ? candidate : "pump";
}

function pickDriverType(raw: unknown, machineType: MachineType): DriverType {
  const candidate = String(raw ?? "").toLowerCase() as DriverType;
  if (DRIVER_TYPES.has(candidate)) return candidate;
  if (machineType === "steam_turbine" || machineType === "gas_turbine") return "integral_prime_mover";
  return "electric_motor_fixed";
}

function pickServiceCriticality(raw: unknown): ServiceCriticality {
  const candidate = String(raw ?? "").toLowerCase() as ServiceCriticality;
  return SERVICE_CRITICALITIES.has(candidate) ? candidate : "normal";
}

function pickTrainArrangement(raw: unknown, machineType: MachineType): TrainArrangement {
  const candidate = String(raw ?? "").toLowerCase() as TrainArrangement;
  if (TRAIN_ARRANGEMENTS.has(candidate)) return candidate;
  if (machineType === "recip_compressor" || machineType === "recip_pump") return "inline";
  if (machineType === "screw_compressor") return "integrally_geared";
  return "overhung";
}

function pickBearingType(raw: unknown, machineType: MachineType): BearingType {
  const candidate = String(raw ?? "").toLowerCase() as BearingType;
  if (BEARING_TYPES.has(candidate)) return candidate;
  if (machineType === "recip_compressor" || machineType === "recip_pump") return "crosshead";
  if (machineType === "axial_compressor" || machineType === "steam_turbine" || machineType === "gas_turbine") {
    return "journal_tilting_pad";
  }
  return "rolling_element";
}

function pickSealSystem(raw: unknown, machineType: MachineType): SealSystem {
  const candidate = String(raw ?? "").toLowerCase() as SealSystem;
  if (SEAL_SYSTEMS.has(candidate)) return candidate;
  if (
    machineType === "compressor"
    || machineType === "centrifugal_compressor"
    || machineType === "axial_compressor"
    || machineType === "screw_compressor"
  ) {
    return "dry_gas_seal";
  }
  if (machineType === "recip_compressor" || machineType === "recip_pump") return "packing";
  return "single_mech";
}

function pickCasingType(raw: unknown, machineType: MachineType): CasingType {
  const candidate = String(raw ?? "").toLowerCase() as CasingType;
  if (CASING_TYPES.has(candidate)) return candidate;
  if (machineType === "recip_compressor" || machineType === "recip_pump") return "recip_frame";
  if (machineType === "screw_compressor") return "integral_gear_case";
  if (machineType === "axial_compressor") return "barrel";
  return "horiz_split";
}

function pickLubeSystem(raw: unknown, machineType: MachineType): LubeSystem {
  const candidate = String(raw ?? "").toLowerCase() as LubeSystem;
  if (LUBE_SYSTEMS.has(candidate)) return candidate;
  if (machineType === "gearbox") return "forced_lube";
  if (machineType === "recip_compressor" || machineType === "recip_pump") return "mist";
  return "ring_oil";
}

function pickStageCount(raw: unknown, machineType: MachineType): number {
  const fallback = machineType === "axial_compressor" ? 8 : machineType === "recip_compressor" ? 4 : 1;
  return clamp(Math.round(toNumber(raw, fallback)), 1, 20);
}

function stageVibrationFactor(machineType: MachineType, stageCount: number): number {
  const normalizedStage = Math.max(stageCount - 1, 0);

  if (ROTODYNAMIC_COMPRESSORS.has(machineType) || machineType === "expander") {
    return round(clamp(1.0 - (normalizedStage * 0.012), 0.84, 1.03), 3);
  }

  if (machineType === "screw_compressor" || machineType === "recip_compressor") {
    return round(clamp(1.0 - (normalizedStage * 0.008), 0.88, 1.02), 3);
  }

  if (PUMP_MACHINES.has(machineType)) {
    return round(clamp(1.0 - (normalizedStage * 0.015), 0.86, 1.02), 3);
  }

  return round(clamp(1.0 - (normalizedStage * 0.006), 0.9, 1.02), 3);
}

function saturationTempFromPressureBar(pressureBar: number): number {
  if (pressureBar <= STEAM_SATURATION_POINTS_BAR_C[0][0]) return STEAM_SATURATION_POINTS_BAR_C[0][1];
  if (pressureBar >= STEAM_SATURATION_POINTS_BAR_C[STEAM_SATURATION_POINTS_BAR_C.length - 1][0]) {
    return STEAM_SATURATION_POINTS_BAR_C[STEAM_SATURATION_POINTS_BAR_C.length - 1][1];
  }

  for (let i = 0; i < STEAM_SATURATION_POINTS_BAR_C.length - 1; i += 1) {
    const [p0, t0] = STEAM_SATURATION_POINTS_BAR_C[i];
    const [p1, t1] = STEAM_SATURATION_POINTS_BAR_C[i + 1];
    if (pressureBar >= p0 && pressureBar <= p1) {
      const ratio = (pressureBar - p0) / (p1 - p0);
      return t0 + ratio * (t1 - t0);
    }
  }

  return STEAM_SATURATION_POINTS_BAR_C[0][1];
}

function steamPhaseChangeRisk(
  pressureBar: number,
  temperatureC: number,
  quality: number,
): { risk: number; superheatMarginC: number; saturationTempC: number } {
  const satTemp = saturationTempFromPressureBar(pressureBar);
  const margin = temperatureC - satTemp;

  let risk = 0;
  if (quality < 0.85) risk += 8;
  else if (quality < 0.9) risk += 5;
  else if (quality < 0.95) risk += 2;

  if (margin < 3) risk += 4;
  else if (margin < 8) risk += 2;

  return {
    risk: Math.min(10, risk),
    superheatMarginC: margin,
    saturationTempC: satTemp,
  };
}

function pressureRatio(machineType: MachineType, suctionBar: number, dischargeBar: number): number {
  if (!PRESSURE_RATIO_MACHINES.has(machineType)) return 1;
  return dischargeBar / Math.max(suctionBar, 0.1);
}

const AXIAL_BRANCH_MACHINES: MachineType[] = [
  "compressor",
  "centrifugal_compressor",
  "axial_compressor",
  "screw_compressor",
  "recip_compressor",
  "steam_turbine",
  "gas_turbine",
  "expander",
];

const COMPRESSOR_BRANCH_MACHINES: MachineType[] = [
  "compressor",
  "centrifugal_compressor",
  "axial_compressor",
  "screw_compressor",
  "recip_compressor",
  "expander",
];

const PUMP_BRANCH_MACHINES: MachineType[] = [
  "pump",
  "recip_pump",
];

export const ROTATING_CONFIG: DisciplineConfig = {
  discipline: "rotating",
  title: "Rotating Reliability",
  subtitle: "Machine x driver x criticality matrix with API/ISO-based risk screening",
  shortLabel: "ROT",
  formFields: [
    {
      name: "machine_type",
      label: "Machine Type",
      type: "select",
      optionGroups: [
        {
          label: "Rotodynamic",
          options: [
            { label: "Centrifugal Pump", value: "pump" },
            { label: "Centrifugal Compressor", value: "centrifugal_compressor" },
            { label: "Axial Compressor", value: "axial_compressor" },
            { label: "Blower", value: "blower" },
            { label: "Fan", value: "fan" },
            { label: "Expander", value: "expander" },
          ],
        },
        {
          label: "Positive Displacement",
          options: [
            { label: "Reciprocating Pump", value: "recip_pump" },
            { label: "Screw Compressor (Rotary PD)", value: "screw_compressor" },
            { label: "Recip Compressor", value: "recip_compressor" },
          ],
        },
        {
          label: "Turbomachinery / Driver",
          options: [
            { label: "Steam Turbine", value: "steam_turbine" },
            { label: "Gas Turbine", value: "gas_turbine" },
            { label: "Compressor (Generic Legacy)", value: "compressor" },
          ],
        },
        {
          label: "Drive Train",
          options: [
            { label: "Gearbox", value: "gearbox" },
          ],
        },
      ],
    },
    {
      name: "driver_type",
      label: "Driver Type",
      type: "select",
      options: [
        { label: "Electric Motor (Fixed Speed)", value: "electric_motor_fixed" },
        { label: "Electric Motor (VFD)", value: "electric_motor_vfd" },
        { label: "Steam Turbine Driver", value: "steam_turbine_driver" },
        { label: "Gas Turbine Driver", value: "gas_turbine_driver" },
        { label: "Recip Engine Driver", value: "recip_engine_driver" },
        { label: "Integral Prime Mover", value: "integral_prime_mover" },
      ],
      helper: "Compressor and pump trains should match actual driver architecture.",
    },
    {
      name: "service_criticality",
      label: "Service Criticality",
      type: "select",
      options: [
        { label: "Normal", value: "normal" },
        { label: "Essential", value: "essential" },
        { label: "High Critical", value: "high_critical" },
        { label: "Safety Critical", value: "safety_critical" },
      ],
    },
    {
      name: "stage_count",
      label: "Stage / Throw Count",
      type: "number",
      min: 1,
      max: 20,
      step: 1,
      placeholder: "1",
      helper: "Number of stages (centrifugal/axial) or throws/cylinders (reciprocating family).",
    },
    {
      name: "train_arrangement",
      label: "Train Arrangement",
      type: "select",
      options: [
        { label: "Overhung", value: "overhung" },
        { label: "Between Bearing", value: "between_bearing" },
        { label: "Integrally Geared", value: "integrally_geared" },
        { label: "Barrel", value: "barrel" },
        { label: "Inline", value: "inline" },
      ],
      helper: "Mechanical train layout used for combination screening.",
    },
    {
      name: "casing_type",
      label: "Casing Type",
      type: "select",
      options: [
        { label: "Horizontal Split", value: "horiz_split" },
        { label: "Vertical Split", value: "vert_split" },
        { label: "Barrel", value: "barrel" },
        { label: "Reciprocating Frame", value: "recip_frame" },
        { label: "Integral Gear Casing", value: "integral_gear_case" },
      ],
      helper: "Casing construction used for integrity and nozzle-load adjustment.",
    },
    {
      name: "bearing_type",
      label: "Bearing Type",
      type: "select",
      options: [
        { label: "Rolling Element", value: "rolling_element" },
        { label: "Journal (Tilting Pad)", value: "journal_tilting_pad" },
        { label: "Sleeve", value: "sleeve" },
        { label: "Crosshead", value: "crosshead" },
      ],
      helper: "Bearing architecture affects baseline vibration and maintenance sensitivity.",
    },
    {
      name: "seal_system",
      label: "Seal System",
      type: "select",
      options: [
        { label: "Single Mechanical", value: "single_mech" },
        { label: "Dual Mechanical", value: "dual_mech" },
        { label: "Dry Gas Seal", value: "dry_gas_seal" },
        { label: "Packing", value: "packing" },
      ],
      helper: "Seal philosophy shifts process leakage/trip risk profile.",
    },
    {
      name: "lube_system",
      label: "Lube System",
      type: "select",
      options: [
        { label: "Ring Oil", value: "ring_oil" },
        { label: "Forced Lube", value: "forced_lube" },
        { label: "Mist", value: "mist" },
        { label: "None / Process Fluid", value: "none_process_fluid" },
      ],
      helper: "Lubrication strategy affects thermal margin and process-risk weighting.",
    },
    { name: "vibration_mm_per_s", label: "Vibration", unit: "mm/s", type: "number", min: 0, max: 20, step: 0.1, placeholder: "2.5" },
    { name: "nozzle_load_ratio", label: "Nozzle Load Ratio", type: "number", min: 0, max: 2, step: 0.01 },
    { name: "bearing_temperature_c", label: "Bearing Temperature", unit: "C", type: "number", min: 0, max: 140, step: 1, placeholder: "72" },
    { name: "lube_oil_supply_temp_c", label: "Lube Oil Supply Temp", unit: "C", type: "number", min: 10, max: 130, step: 1, placeholder: "56" },
    { name: "coupling_misalignment_mils", label: "Coupling Misalignment", unit: "mils", type: "number", min: 0, max: 20, step: 0.1, placeholder: "1.8" },
    {
      name: "axial_displacement_um",
      label: "Axial Displacement",
      unit: "um",
      type: "number",
      min: 0,
      max: 300,
      step: 1,
      helper: "Compressor/turbine/expander trains only",
      showWhen: { field: "machine_type", equalsAny: AXIAL_BRANCH_MACHINES },
    },
    { name: "speed_rpm", label: "Speed", unit: "rpm", type: "number", min: 50, max: 30000, step: 10, placeholder: "1800" },
    {
      name: "suction_pressure_bar",
      label: "Suction Pressure",
      unit: "bar",
      type: "number",
      min: 0.1,
      max: 300,
      step: 0.1,
      helper: "Compressor/expander train check",
      showWhen: { field: "machine_type", equalsAny: COMPRESSOR_BRANCH_MACHINES },
    },
    {
      name: "discharge_pressure_bar",
      label: "Discharge Pressure",
      unit: "bar",
      type: "number",
      min: 0.2,
      max: 400,
      step: 0.1,
      helper: "Compressor/expander train check",
      showWhen: { field: "machine_type", equalsAny: COMPRESSOR_BRANCH_MACHINES },
    },
    {
      name: "surge_events_30d",
      label: "Surge Events (30d)",
      type: "number",
      min: 0,
      max: 30,
      step: 1,
      helper: "Compressor anti-surge stability indicator",
      showWhen: { field: "machine_type", equalsAny: COMPRESSOR_BRANCH_MACHINES },
    },
    {
      name: "npsh_available_m",
      label: "NPSH Available",
      unit: "m",
      type: "number",
      min: 0,
      max: 50,
      step: 0.1,
      helper: "Pump and reciprocating-pump suction margin check",
      showWhen: { field: "machine_type", equalsAny: PUMP_BRANCH_MACHINES },
    },
    {
      name: "npsh_required_m",
      label: "NPSH Required",
      unit: "m",
      type: "number",
      min: 0,
      max: 50,
      step: 0.1,
      helper: "Pump and reciprocating-pump suction margin check",
      showWhen: { field: "machine_type", equalsAny: PUMP_BRANCH_MACHINES },
    },
    { name: "api670_coverage_pct", label: "API 670 Coverage", unit: "%", type: "number", min: 0, max: 100, step: 1, placeholder: "95" },
    { name: "trip_tests_last_12m", label: "Trip Tests (12m)", type: "number", min: 0, max: 24, step: 1, placeholder: "4" },
    { name: "protection_bypass_active", label: "Protection Bypass Active", type: "checkbox", helper: "Enable only if key protection bypass is currently active." },
    {
      name: "steam_pressure_bar",
      label: "Steam Pressure",
      unit: "bar",
      type: "number",
      min: 0.1,
      max: 250,
      step: 0.1,
      helper: "Steam turbine mode",
      showWhen: { field: "machine_type", equals: "steam_turbine" },
    },
    {
      name: "steam_temperature_c",
      label: "Steam Temperature",
      unit: "C",
      type: "number",
      min: 10,
      max: 650,
      step: 1,
      helper: "Steam turbine mode",
      showWhen: { field: "machine_type", equals: "steam_turbine" },
    },
    {
      name: "steam_quality_x",
      label: "Steam Quality x (0-1)",
      type: "number",
      min: 0,
      max: 1,
      step: 0.01,
      helper: "Dryness fraction for erosion/phase-change screening",
      showWhen: { field: "machine_type", equals: "steam_turbine" },
    },
    {
      name: "inlet_enthalpy_kj_per_kg",
      label: "Inlet Enthalpy",
      unit: "kJ/kg",
      type: "number",
      min: 1000,
      max: 4000,
      step: 1,
      showWhen: { field: "machine_type", equals: "steam_turbine" },
    },
    {
      name: "outlet_enthalpy_kj_per_kg",
      label: "Outlet Enthalpy",
      unit: "kJ/kg",
      type: "number",
      min: 500,
      max: 4000,
      step: 1,
      showWhen: { field: "machine_type", equals: "steam_turbine" },
    },
  ],
  sampleInput: {
    machine_type: "pump",
    driver_type: "electric_motor_fixed",
    service_criticality: "normal",
    stage_count: 1,
    train_arrangement: "overhung",
    casing_type: "horiz_split",
    bearing_type: "rolling_element",
    seal_system: "single_mech",
    lube_system: "ring_oil",
    vibration_mm_per_s: 2.5,
    nozzle_load_ratio: 0.85,
    bearing_temperature_c: 72,
    lube_oil_supply_temp_c: 56,
    coupling_misalignment_mils: 1.8,
    axial_displacement_um: 60,
    speed_rpm: 1800,
    suction_pressure_bar: 3.2,
    discharge_pressure_bar: 12.8,
    surge_events_30d: 0,
    npsh_available_m: 5.6,
    npsh_required_m: 3.8,
    api670_coverage_pct: 96,
    trip_tests_last_12m: 4,
    protection_bypass_active: false,
    steam_pressure_bar: 80,
    steam_temperature_c: 510,
    steam_quality_x: 0.97,
    inlet_enthalpy_kj_per_kg: 3350,
    outlet_enthalpy_kj_per_kg: 2900,
  },
  presets: [
    {
      id: "rot-pump-normal",
      label: "Pump Normal",
      description: "Centrifugal pump in healthy operating region with stable protection coverage.",
      values: {
        machine_type: "pump",
        driver_type: "electric_motor_fixed",
        service_criticality: "normal",
        stage_count: 1,
        train_arrangement: "overhung",
        casing_type: "horiz_split",
        bearing_type: "rolling_element",
        seal_system: "single_mech",
        lube_system: "ring_oil",
        vibration_mm_per_s: 2.4,
        nozzle_load_ratio: 0.84,
        bearing_temperature_c: 71,
        lube_oil_supply_temp_c: 56,
        speed_rpm: 1780,
        npsh_available_m: 5.8,
        npsh_required_m: 3.9,
        api670_coverage_pct: 96,
        trip_tests_last_12m: 4,
        protection_bypass_active: false,
      },
    },
    {
      id: "rot-pump-cavitation",
      label: "Pump Cavitation Risk",
      description: "Low NPSH margin and elevated vibration scenario.",
      values: {
        machine_type: "pump",
        driver_type: "electric_motor_vfd",
        service_criticality: "essential",
        stage_count: 1,
        train_arrangement: "overhung",
        casing_type: "horiz_split",
        bearing_type: "rolling_element",
        seal_system: "single_mech",
        lube_system: "ring_oil",
        vibration_mm_per_s: 4.3,
        nozzle_load_ratio: 1.08,
        bearing_temperature_c: 83,
        lube_oil_supply_temp_c: 74,
        speed_rpm: 3200,
        npsh_available_m: 2.9,
        npsh_required_m: 3.4,
        api670_coverage_pct: 88,
        trip_tests_last_12m: 2,
        protection_bypass_active: false,
      },
    },
    {
      id: "rot-compressor-vfd-alert",
      label: "Centrifugal Compressor VFD Alert",
      description: "VFD-driven centrifugal compressor with surge events and marginal protection.",
      values: {
        machine_type: "centrifugal_compressor",
        driver_type: "electric_motor_vfd",
        service_criticality: "high_critical",
        stage_count: 5,
        train_arrangement: "between_bearing",
        casing_type: "vert_split",
        bearing_type: "journal_tilting_pad",
        seal_system: "dry_gas_seal",
        lube_system: "forced_lube",
        vibration_mm_per_s: 5.4,
        nozzle_load_ratio: 1.02,
        bearing_temperature_c: 89,
        lube_oil_supply_temp_c: 78,
        coupling_misalignment_mils: 3.6,
        axial_displacement_um: 95,
        speed_rpm: 10600,
        suction_pressure_bar: 2.8,
        discharge_pressure_bar: 17.2,
        surge_events_30d: 3,
        api670_coverage_pct: 84,
        trip_tests_last_12m: 2,
        protection_bypass_active: false,
      },
    },
    {
      id: "rot-compressor-steam-driver",
      label: "Axial Compressor Steam Driver",
      description: "Steam-driven axial compressor train with elevated pressure ratio and protection bypass.",
      values: {
        machine_type: "axial_compressor",
        driver_type: "steam_turbine_driver",
        service_criticality: "safety_critical",
        stage_count: 10,
        train_arrangement: "integrally_geared",
        casing_type: "barrel",
        bearing_type: "journal_tilting_pad",
        seal_system: "dry_gas_seal",
        lube_system: "forced_lube",
        vibration_mm_per_s: 6.1,
        nozzle_load_ratio: 1.15,
        bearing_temperature_c: 97,
        lube_oil_supply_temp_c: 86,
        coupling_misalignment_mils: 5.2,
        axial_displacement_um: 118,
        speed_rpm: 12400,
        suction_pressure_bar: 2.1,
        discharge_pressure_bar: 19.5,
        surge_events_30d: 6,
        api670_coverage_pct: 72,
        trip_tests_last_12m: 1,
        protection_bypass_active: true,
      },
    },
    {
      id: "rot-recip-pump-suction-risk",
      label: "Recip Pump Suction Risk",
      description: "Reciprocating pump with low suction margin and high pulsation-linked vibration.",
      values: {
        machine_type: "recip_pump",
        driver_type: "recip_engine_driver",
        service_criticality: "essential",
        stage_count: 3,
        train_arrangement: "inline",
        casing_type: "recip_frame",
        bearing_type: "crosshead",
        seal_system: "packing",
        lube_system: "mist",
        vibration_mm_per_s: 5.9,
        nozzle_load_ratio: 1.03,
        bearing_temperature_c: 88,
        lube_oil_supply_temp_c: 76,
        coupling_misalignment_mils: 4.2,
        speed_rpm: 420,
        npsh_available_m: 2.2,
        npsh_required_m: 2.9,
        api670_coverage_pct: 86,
        trip_tests_last_12m: 2,
        protection_bypass_active: false,
      },
    },
    {
      id: "rot-screw-compressor-pd",
      label: "Screw Compressor PD",
      description: "Rotary PD compressor case with thermal rise, overload ratio, and repeat surge-like events.",
      values: {
        machine_type: "screw_compressor",
        driver_type: "electric_motor_fixed",
        service_criticality: "essential",
        stage_count: 2,
        train_arrangement: "integrally_geared",
        casing_type: "integral_gear_case",
        bearing_type: "sleeve",
        seal_system: "dual_mech",
        lube_system: "forced_lube",
        vibration_mm_per_s: 5.7,
        nozzle_load_ratio: 1.06,
        bearing_temperature_c: 94,
        lube_oil_supply_temp_c: 88,
        coupling_misalignment_mils: 4.9,
        axial_displacement_um: 68,
        speed_rpm: 5200,
        suction_pressure_bar: 1.7,
        discharge_pressure_bar: 12.6,
        surge_events_30d: 5,
        api670_coverage_pct: 81,
        trip_tests_last_12m: 2,
        protection_bypass_active: false,
      },
    },
    {
      id: "rot-steam-turbine-phase",
      label: "Steam Turbine Wetness",
      description: "Steam turbine mode with low quality and low superheat margin.",
      values: {
        machine_type: "steam_turbine",
        driver_type: "integral_prime_mover",
        service_criticality: "high_critical",
        stage_count: 5,
        train_arrangement: "between_bearing",
        casing_type: "barrel",
        bearing_type: "journal_tilting_pad",
        seal_system: "packing",
        lube_system: "forced_lube",
        vibration_mm_per_s: 4.1,
        nozzle_load_ratio: 0.92,
        bearing_temperature_c: 82,
        lube_oil_supply_temp_c: 68,
        coupling_misalignment_mils: 2.5,
        axial_displacement_um: 78,
        speed_rpm: 7200,
        api670_coverage_pct: 91,
        trip_tests_last_12m: 5,
        protection_bypass_active: false,
        steam_pressure_bar: 82,
        steam_temperature_c: 300,
        steam_quality_x: 0.89,
        inlet_enthalpy_kj_per_kg: 3290,
        outlet_enthalpy_kj_per_kg: 3160,
      },
    },
    {
      id: "rot-recip-mech",
      label: "Recip Mechanical Risk",
      description: "Recip train with vibration/misalignment growth and axial displacement excursion.",
      values: {
        machine_type: "recip_compressor",
        driver_type: "recip_engine_driver",
        service_criticality: "essential",
        stage_count: 4,
        train_arrangement: "inline",
        casing_type: "recip_frame",
        bearing_type: "crosshead",
        seal_system: "packing",
        lube_system: "mist",
        vibration_mm_per_s: 7.1,
        nozzle_load_ratio: 1.18,
        bearing_temperature_c: 92,
        lube_oil_supply_temp_c: 81,
        coupling_misalignment_mils: 6.7,
        axial_displacement_um: 136,
        speed_rpm: 1050,
        suction_pressure_bar: 1.4,
        discharge_pressure_bar: 13.2,
        surge_events_30d: 4,
        api670_coverage_pct: 79,
        trip_tests_last_12m: 2,
        protection_bypass_active: false,
      },
    },
  ],
  defaultChart: "spectrum",
  primaryMetrics: [
    "vibration_mm_per_s",
    "adjusted_vibration_limit_mm_per_s",
    "mechanical_integrity_index",
    "process_stability_index",
    "protection_readiness_index",
    "inspection_interval_years",
    "monitoring_escalation",
    "maintenance_urgency",
  ],
};

export function buildRotatingOutcome(input: Record<string, unknown>): DisciplineOutcome {
  const machineType = pickMachineType(input.machine_type);
  const driverType = pickDriverType(input.driver_type, machineType);
  const serviceCriticality = pickServiceCriticality(input.service_criticality);
  const stageCount = pickStageCount(input.stage_count, machineType);
  const trainArrangement = pickTrainArrangement(input.train_arrangement, machineType);
  const casingType = pickCasingType(input.casing_type, machineType);
  const bearingType = pickBearingType(input.bearing_type, machineType);
  const sealSystem = pickSealSystem(input.seal_system, machineType);
  const lubeSystem = pickLubeSystem(input.lube_system, machineType);

  const vibration = toNumber(input.vibration_mm_per_s, 2.5);
  const nozzleRatio = toNumber(input.nozzle_load_ratio, 0.85);
  const bearingTemp = toNumber(input.bearing_temperature_c, 72);
  const oilTemp = toNumber(input.lube_oil_supply_temp_c, 56);
  const misalignment = toNumber(input.coupling_misalignment_mils, 1.8);
  const speedRpm = toNumber(input.speed_rpm, 1800);
  const axialDisp = toNumber(input.axial_displacement_um, 60);

  const vibrationLimitBase = ROTATING_VIBRATION_LIMIT_MM_PER_S[machineType];
  const nozzleLimitBase = ROTATING_NOZZLE_LOAD_LIMIT_RATIO[machineType];
  const axialLimit = ROTATING_AXIAL_DISPLACEMENT_LIMIT_UM[machineType];
  const driverFactor = DRIVER_VIBRATION_FACTOR[driverType];
  const criticalityFactor = SERVICE_CRITICALITY_FACTOR[serviceCriticality];
  const trainVibrationFactor = TRAIN_VIBRATION_FACTOR[trainArrangement];
  const casingVibrationFactor = CASING_VIBRATION_FACTOR[casingType];
  const bearingVibrationFactor = BEARING_VIBRATION_FACTOR[bearingType];
  const stageFactor = stageVibrationFactor(machineType, stageCount);
  const trainNozzleFactor = TRAIN_NOZZLE_FACTOR[trainArrangement];
  const casingNozzleFactor = CASING_NOZZLE_FACTOR[casingType];
  const sealProcessFactor = SEAL_PROCESS_FACTOR[sealSystem];
  const lubeProcessFactor = LUBE_PROCESS_FACTOR[lubeSystem];
  const lubeTempFactor = LUBE_TEMPERATURE_FACTOR[lubeSystem];
  const adjustedVibrationLimit = round(
    vibrationLimitBase
      * driverFactor
      * criticalityFactor
      * trainVibrationFactor
      * casingVibrationFactor
      * bearingVibrationFactor
      * stageFactor,
    2,
  );
  const adjustedNozzleLimit = round(nozzleLimitBase * trainNozzleFactor * casingNozzleFactor, 2);

  const speedEnvelope = ROTATING_SPEED_ENVELOPE_RPM[machineType];
  const speedLow = speedEnvelope.low;
  const speedHigh = speedEnvelope.high;

  const suctionPressureBar = toNumber(input.suction_pressure_bar, 3.0);
  const dischargePressureBar = toNumber(input.discharge_pressure_bar, 12.0);
  const computedPressureRatio = round(pressureRatio(machineType, suctionPressureBar, dischargePressureBar), 2);
  const surgeEvents30d = Math.max(0, toNumber(input.surge_events_30d, 0));
  const npshAvailable = toNumber(input.npsh_available_m, 5.6);
  const npshRequired = toNumber(input.npsh_required_m, 3.8);
  const npshMargin = round(npshAvailable - npshRequired, 2);

  const api670Coverage = clamp(toNumber(input.api670_coverage_pct, 95), 0, 100);
  const tripTests = Math.max(0, toNumber(input.trip_tests_last_12m, 4));
  const expectedTripTests = EXPECTED_TRIP_TESTS_PER_YEAR[serviceCriticality];
  const protectionBypassActive = Boolean(input.protection_bypass_active);

  const warnings: string[] = [];
  const redFlags: string[] = [];

  if (machineType === "steam_turbine" || machineType === "gas_turbine") {
    if (driverType !== "integral_prime_mover") warnings.push("LOG.DRIVER_MACHINE_MISMATCH");
  } else if (driverType === "integral_prime_mover") {
    warnings.push("LOG.DRIVER_MACHINE_MISMATCH");
  }

  const isRecipMachine = machineType === "recip_compressor" || machineType === "recip_pump";
  const canBeIntegrallyGeared = ROTODYNAMIC_COMPRESSORS.has(machineType) || machineType === "screw_compressor" || machineType === "expander";
  if (trainArrangement === "integrally_geared" && !canBeIntegrallyGeared) {
    warnings.push("LOG.TRAIN_ARRANGEMENT_MACHINE_MISMATCH");
  }
  if (isRecipMachine && bearingType !== "crosshead") warnings.push("LOG.BEARING_MACHINE_MISMATCH");
  if (!isRecipMachine && bearingType === "crosshead") warnings.push("LOG.BEARING_MACHINE_MISMATCH");
  if ((machineType === "pump" || machineType === "recip_pump") && sealSystem === "dry_gas_seal") {
    warnings.push("LOG.SEAL_MACHINE_MISMATCH");
  }
  if (ROTODYNAMIC_COMPRESSORS.has(machineType) && sealSystem === "packing") {
    warnings.push("LOG.SEAL_MACHINE_MISMATCH");
  }
  if (
    (
      machineType === "steam_turbine"
      || machineType === "gas_turbine"
      || machineType === "gearbox"
      || ROTODYNAMIC_COMPRESSORS.has(machineType)
      || machineType === "screw_compressor"
      || machineType === "expander"
    )
    && lubeSystem === "none_process_fluid"
  ) {
    warnings.push("LOG.LUBE_MACHINE_MISMATCH");
  }
  if (isRecipMachine && casingType !== "recip_frame") warnings.push("LOG.CASING_MACHINE_MISMATCH");
  if (!isRecipMachine && casingType === "recip_frame") warnings.push("LOG.CASING_MACHINE_MISMATCH");
  if (machineType === "screw_compressor" && casingType !== "integral_gear_case" && casingType !== "vert_split") {
    warnings.push("LOG.CASING_MACHINE_MISMATCH");
  }

  if (machineType === "axial_compressor" && stageCount < 5) warnings.push("LOG.STAGE_COUNT_MACHINE_MISMATCH");
  if (machineType === "centrifugal_compressor" && stageCount < 2) warnings.push("LOG.STAGE_COUNT_MACHINE_MISMATCH");
  if ((machineType === "pump" || machineType === "recip_pump") && stageCount > 4) warnings.push("LOG.STAGE_COUNT_MACHINE_MISMATCH");
  if (machineType === "screw_compressor" && stageCount > 4) warnings.push("LOG.STAGE_COUNT_MACHINE_MISMATCH");
  if (machineType === "recip_compressor" && stageCount > 8) warnings.push("LOG.STAGE_COUNT_MACHINE_MISMATCH");

  if (speedRpm < speedLow || speedRpm > speedHigh) warnings.push("STD.ROTATING_SPEED_OUT_OF_SCOPE_REVIEW");
  if (speedRpm < speedLow * 0.8 || speedRpm > speedHigh * 1.2) redFlags.push("PHY.ROTATING_SPEED_CRITICAL_OUT_OF_SCOPE");

  if (vibration > adjustedVibrationLimit) warnings.push("PHY.ROTATING_VIBRATION_ABOVE_LIMIT");
  if (vibration > adjustedVibrationLimit * 1.25) redFlags.push("PHY.ROTATING_VIBRATION_CRITICAL");

  if (nozzleRatio > adjustedNozzleLimit) warnings.push("PHY.ROTATING_NOZZLE_LOAD_NEAR_LIMIT");
  if (nozzleRatio > adjustedNozzleLimit * 1.2) redFlags.push("PHY.ROTATING_NOZZLE_LOAD_EXCEEDED");

  if (bearingTemp >= 85) warnings.push("PHY.BEARING_TEMPERATURE_HIGH");
  if (bearingTemp >= 100) redFlags.push("PHY.BEARING_TEMPERATURE_CRITICAL");

  if (oilTemp >= 75) warnings.push("PHY.LUBE_OIL_TEMPERATURE_HIGH");
  if (oilTemp >= 90) redFlags.push("PHY.LUBE_OIL_TEMPERATURE_CRITICAL");

  if (misalignment >= 3) warnings.push("PHY.ROTATING_COUPLING_MISALIGNMENT_HIGH");
  if (misalignment >= 6) redFlags.push("PHY.ROTATING_COUPLING_MISALIGNMENT_CRITICAL");

  if (AXIAL_MACHINES.has(machineType)) {
    if (axialDisp > axialLimit) warnings.push("PHY.ROTATING_AXIAL_DISPLACEMENT_HIGH");
    if (axialDisp > axialLimit * 1.25) redFlags.push("PHY.ROTATING_AXIAL_DISPLACEMENT_CRITICAL");
  }

  if (PRESSURE_RATIO_MACHINES.has(machineType)) {
    if (computedPressureRatio < 1) warnings.push("LOG.ROTATING_PRESSURE_RATIO_INCONSISTENT");
    if (computedPressureRatio > PRESSURE_RATIO_WARNING_LIMIT[machineType]) warnings.push("PHY.ROTATING_SURGE_RISK");
    if (computedPressureRatio > PRESSURE_RATIO_CRITICAL_LIMIT[machineType]) redFlags.push("PHY.ROTATING_SURGE_CRITICAL");

    if (surgeEvents30d >= 1) warnings.push("PHY.ROTATING_SURGE_RISK");
    if (surgeEvents30d >= (POSITIVE_DISPLACEMENT_COMPRESSORS.has(machineType) ? 5 : 4)) {
      redFlags.push("PHY.ROTATING_SURGE_CRITICAL");
    }
  }

  if (PUMP_MACHINES.has(machineType)) {
    if (npshMargin < 1.0) warnings.push("PHY.PUMP_NPSH_MARGIN_LOW");
    if (npshMargin < 0) redFlags.push("PHY.PUMP_CAVITATION_RISK");
    if (machineType === "recip_pump" && npshMargin < 0.5) warnings.push("PHY.RECIP_PUMP_SUCTION_PULSATION_RISK");
  }

  if (api670Coverage < 90) warnings.push("STD.API670_PROTECTION_GAP");
  if (api670Coverage < 75) redFlags.push("STD.API670_PROTECTION_UNACCEPTABLE");

  if (tripTests < expectedTripTests) warnings.push("STD.API670_TRIP_TEST_OVERDUE");
  if (protectionBypassActive) redFlags.push("STD.API670_BYPASS_ACTIVE");

  let phaseRisk = 0;
  let steamSuperheatMarginC = 0;
  let steamSaturationTempC = 0;
  let steamQuality = 1;
  let steamPressureBar = 0;
  let steamTemperatureC = 0;
  let steamSpecificEnergyDrop = 0;

  if (machineType === "steam_turbine") {
    steamPressureBar = toNumber(input.steam_pressure_bar, 80);
    steamTemperatureC = toNumber(input.steam_temperature_c, 295);
    steamQuality = clamp(toNumber(input.steam_quality_x, 0.98), 0, 1);

    const steamState = steamPhaseChangeRisk(steamPressureBar, steamTemperatureC, steamQuality);
    phaseRisk = steamState.risk;
    steamSuperheatMarginC = steamState.superheatMarginC;
    steamSaturationTempC = steamState.saturationTempC;

    const inletH = toNumber(input.inlet_enthalpy_kj_per_kg, 3350);
    const outletH = toNumber(input.outlet_enthalpy_kj_per_kg, 2850);
    steamSpecificEnergyDrop = round(inletH - outletH, 1);

    if (steamQuality < 0.92) warnings.push("PHY.STEAM_WETNESS_EROSION_RISK");
    if (steamQuality < 0.88) redFlags.push("PHY.STEAM_WETNESS_EROSION_RISK");
    if (phaseRisk >= 7) redFlags.push("PHY.STEAM_PHASE_CHANGE_RISK");
    if (steamSpecificEnergyDrop <= 0) warnings.push("LOG.STEAM_STATE_INCONSISTENT");
  }

  const vibrationPenalty = Math.max(vibration - adjustedVibrationLimit, 0) * 1.8;
  const nozzlePenalty = Math.max(nozzleRatio - adjustedNozzleLimit, 0) * 4.0;
  const bearingPenalty = Math.max(bearingTemp - 75, 0) * 0.12 * lubeTempFactor;
  const oilPenalty = Math.max(oilTemp - 60, 0) * 0.08 * lubeTempFactor;
  const misalignmentPenalty = Math.max(misalignment - 2.5, 0) * 0.7;
  const axialPenalty = AXIAL_MACHINES.has(machineType) ? Math.max(axialDisp - axialLimit, 0) * 0.03 : 0;
  const phasePenalty = phaseRisk * 0.35;
  const stageComplexityPenalty = Math.max(stageCount - 1, 0) * 0.08;

  let processPenalty = 0;
  if (PRESSURE_RATIO_MACHINES.has(machineType)) {
    const ratioPenaltyStart = Math.max(PRESSURE_RATIO_WARNING_LIMIT[machineType] - 0.3, 1.5);
    const surgeEventPenaltyFactor = POSITIVE_DISPLACEMENT_COMPRESSORS.has(machineType)
      ? 0.95
      : ROTODYNAMIC_COMPRESSORS.has(machineType)
        ? 0.8
        : 0.75;
    processPenalty += Math.max(computedPressureRatio - ratioPenaltyStart, 0) * 0.6;
    processPenalty += surgeEvents30d * surgeEventPenaltyFactor;
  }
  if (PUMP_MACHINES.has(machineType)) {
    processPenalty += Math.max(1 - npshMargin, 0) * 1.8;
    if (machineType === "recip_pump") processPenalty += Math.max(0.7 - npshMargin, 0) * 1.2;
  }
  processPenalty += phaseRisk * 0.2;
  processPenalty += stageComplexityPenalty;
  processPenalty *= sealProcessFactor * lubeProcessFactor;

  const mechanicalIntegrity = round(
    clamp(
      10 - (vibrationPenalty + nozzlePenalty + bearingPenalty + oilPenalty + misalignmentPenalty + axialPenalty + phasePenalty + stageComplexityPenalty),
      0,
      10,
    ),
    2,
  );
  const processStability = round(clamp(10 - processPenalty, 0, 10), 2);
  const bearingHealth = round(clamp(10 - (vibrationPenalty + bearingPenalty + oilPenalty + (axialPenalty * 0.5)), 0, 10), 2);

  const coveragePenalty = Math.max(92 - api670Coverage, 0) * 0.07;
  const testPenalty = Math.max(expectedTripTests - tripTests, 0) * 0.9;
  const bypassPenalty = protectionBypassActive ? 3 : 0;
  const protectionReadiness = round(clamp(10 - (coveragePenalty + testPenalty + bypassPenalty), 0, 10), 2);

  let intervalYears = 2.0;
  if (serviceCriticality === "high_critical") intervalYears = 1.5;
  if (serviceCriticality === "safety_critical") intervalYears = 1.0;
  if (mechanicalIntegrity < 4 || processStability < 4 || protectionReadiness < 5) intervalYears = 0.5;
  else if (mechanicalIntegrity < 6 || processStability < 6 || protectionReadiness < 7) intervalYears = 1.0;
  if (warnings.length > 0) intervalYears = Math.min(intervalYears, 1.0);
  if (redFlags.length > 0) intervalYears = 0.25;

  const finalResults: Record<string, unknown> = {
    machine_type: machineType,
    driver_type: driverType,
    service_criticality: serviceCriticality,
    stage_count: stageCount,
    train_arrangement: trainArrangement,
    casing_type: casingType,
    bearing_type: bearingType,
    seal_system: sealSystem,
    lube_system: lubeSystem,
    vibration_mm_per_s: round(vibration, 2),
    vibration_limit_mm_per_s: vibrationLimitBase,
    adjusted_vibration_limit_mm_per_s: adjustedVibrationLimit,
    nozzle_load_ratio: round(nozzleRatio, 2),
    nozzle_load_limit_ratio: adjustedNozzleLimit,
    nozzle_load_limit_base_ratio: round(nozzleLimitBase, 2),
    bearing_temperature_c: round(bearingTemp, 1),
    lube_oil_supply_temp_c: round(oilTemp, 1),
    coupling_misalignment_mils: round(misalignment, 2),
    speed_rpm: round(speedRpm, 0),
    speed_low_limit_rpm: speedLow,
    speed_high_limit_rpm: speedHigh,
    axial_displacement_um: round(axialDisp, 1),
    axial_displacement_limit_um: axialLimit,
    suction_pressure_bar: round(suctionPressureBar, 2),
    discharge_pressure_bar: round(dischargePressureBar, 2),
    pressure_ratio: computedPressureRatio,
    surge_events_30d: round(surgeEvents30d, 0),
    npsh_available_m: round(npshAvailable, 2),
    npsh_required_m: round(npshRequired, 2),
    npsh_margin_m: npshMargin,
    api670_coverage_pct: round(api670Coverage, 1),
    trip_tests_last_12m: round(tripTests, 0),
    expected_trip_tests_per_year: expectedTripTests,
    protection_bypass_active: protectionBypassActive,
    driver_factor: round(driverFactor, 3),
    criticality_factor: round(criticalityFactor, 3),
    stage_vibration_factor: round(stageFactor, 3),
    train_vibration_factor: round(trainVibrationFactor, 3),
    casing_vibration_factor: round(casingVibrationFactor, 3),
    bearing_vibration_factor: round(bearingVibrationFactor, 3),
    train_nozzle_factor: round(trainNozzleFactor, 3),
    casing_nozzle_factor: round(casingNozzleFactor, 3),
    seal_process_factor: round(sealProcessFactor, 3),
    lube_process_factor: round(lubeProcessFactor, 3),
    lube_temperature_factor: round(lubeTempFactor, 3),
    mechanical_integrity_index: mechanicalIntegrity,
    process_stability_index: processStability,
    protection_readiness_index: protectionReadiness,
    bearing_health_index: bearingHealth,
    phase_change_risk_index: round(phaseRisk, 2),
    inspection_interval_years: round(intervalYears, 2),
    monitoring_escalation: bearingHealth < 3 ? "CONTINUOUS_ONLINE"
      : bearingHealth < 5 ? "WEEKLY_ROUTE"
      : bearingHealth < 7 ? "MONTHLY_ROUTE"
      : "QUARTERLY_ROUTE",
    maintenance_urgency: bearingHealth < 3 ? "IMMEDIATE_SHUTDOWN_REVIEW"
      : bearingHealth < 5 ? "NEXT_AVAILABLE_WINDOW"
      : bearingHealth < 7 ? "PLANNED_TURNAROUND"
      : "ROUTINE",
    status: redFlags.length > 0 ? "CRITICAL" : warnings.length > 0 ? "WARNING" : "ACCEPTABLE",
  };

  if (machineType === "steam_turbine") {
    finalResults.steam_pressure_bar = round(steamPressureBar, 2);
    finalResults.steam_temperature_c = round(steamTemperatureC, 1);
    finalResults.steam_quality_x = round(steamQuality, 3);
    finalResults.steam_saturation_temp_c = round(steamSaturationTempC, 1);
    finalResults.steam_superheat_margin_c = round(steamSuperheatMarginC, 1);
    finalResults.steam_specific_energy_drop_kj_per_kg = steamSpecificEnergyDrop;
  }

  return {
    finalResults,
    warnings: Array.from(new Set(warnings)),
    redFlags: Array.from(new Set(redFlags)),
  };
}
