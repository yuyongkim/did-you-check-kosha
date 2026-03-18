import { DisciplineConfig } from "@/lib/types";
import { DisciplineOutcome, round, toNumber } from "@/lib/mock/shared";

export const ELECTRICAL_STANDARD_REFS = [
  "IEEE C57.104",
  "IEEE 1584-2018",
  "NFPA 70E",
];

export const ELECTRICAL_DEFAULT_RESULTS: Record<string, unknown> = {
  transformer_health_index: 7.8,
  arc_flash_energy_cal_cm2: 11.5,
  ppe_category: 2,
  voltage_drop_percent: 3.2,
  status: "ACCEPTABLE",
  breaker_coordination_margin: 1.25,
  load_utilization: "LIGHTLY_LOADED",
};

const ELECTRICAL_HI_WEIGHTS = {
  dga: 0.35,
  oil: 0.25,
  insulation: 0.2,
  load: 0.2,
} as const;

const ELECTRICAL_EQUIPMENT_ARC_FACTOR: Record<string, number> = {
  transformer: 1.0,
  switchgear: 1.15,
  mcc: 1.05,
  motor: 0.95,
  ups: 0.9,
  feeder_panel: 1.1,
  generator: 1.05,
  inverter: 1.12,
  cable_feeder: 1.02,
};

const ELECTRICAL_EQUIPMENT_HI_BIAS: Record<string, number> = {
  transformer: 0.0,
  switchgear: -0.2,
  mcc: -0.1,
  motor: 0.1,
  ups: 0.2,
  feeder_panel: -0.15,
  generator: -0.05,
  inverter: -0.15,
  cable_feeder: 0.05,
};

export const ELECTRICAL_CONFIG: DisciplineConfig = {
  discipline: "electrical",
  title: "Electrical Integrity",
  subtitle: "IEEE and NFPA checks for HI, arc-flash, short-circuit, and power quality",
  shortLabel: "ELE",
  formFields: [
    {
      name: "equipment_type",
      label: "Equipment Type",
      type: "select",
      options: [
        { label: "Transformer", value: "transformer" },
        { label: "Switchgear", value: "switchgear" },
        { label: "MCC", value: "mcc" },
        { label: "Motor", value: "motor" },
        { label: "UPS", value: "ups" },
        { label: "Feeder Panel", value: "feeder_panel" },
        { label: "Generator", value: "generator" },
        { label: "Inverter / VFD", value: "inverter" },
        { label: "Cable Feeder", value: "cable_feeder" },
      ],
    },
    { name: "system_voltage_kv", label: "System Voltage", unit: "kV", type: "number", min: 0.4, max: 33, step: 0.1, placeholder: "13.8" },
    { name: "bolted_fault_current_ka", label: "Fault Current", unit: "kA", type: "number", min: 1, max: 100, step: 0.1, placeholder: "22" },
    { name: "clearing_time_sec", label: "Clearing Time", unit: "s", type: "number", min: 0.01, max: 2, step: 0.01, placeholder: "0.2" },
    { name: "working_distance_mm", label: "Working Distance", unit: "mm", type: "number", min: 300, max: 1000, step: 1, placeholder: "455" },
    { name: "breaker_interrupt_rating_ka", label: "Breaker Rating", unit: "kA", type: "number", min: 1, max: 100, step: 0.1, placeholder: "31.5" },
    { name: "voltage_drop_percent", label: "Voltage Drop", unit: "%", type: "number", min: 0, max: 20, step: 0.1, placeholder: "3.2" },
    { name: "thd_voltage_percent", label: "Voltage THD", unit: "%", type: "number", min: 0, max: 20, step: 0.1, placeholder: "4.8" },
    { name: "motor_current_thd_percent", label: "Current THD", unit: "%", type: "number", min: 0, max: 30, step: 0.1, placeholder: "4.5" },
    { name: "power_factor", label: "Power Factor", type: "number", min: 0.1, max: 1, step: 0.01 },
    { name: "dga_score", label: "DGA Score", unit: "0-10", type: "number", min: 0, max: 10, step: 0.1 },
    { name: "oil_quality_score", label: "Oil Quality Score", unit: "0-10", type: "number", min: 0, max: 10, step: 0.1 },
    { name: "insulation_score", label: "Insulation Score", unit: "0-10", type: "number", min: 0, max: 10, step: 0.1 },
    { name: "load_factor_score", label: "Load Score", unit: "0-10", type: "number", min: 0, max: 10, step: 0.1 },
  ],
  sampleInput: {
    equipment_type: "transformer",
    system_voltage_kv: 13.8,
    bolted_fault_current_ka: 22,
    clearing_time_sec: 0.2,
    working_distance_mm: 455,
    breaker_interrupt_rating_ka: 31.5,
    voltage_drop_percent: 3.2,
    thd_voltage_percent: 4.8,
    dga_score: 8.2,
    oil_quality_score: 7.9,
    insulation_score: 8.3,
    load_factor_score: 7.5,
    motor_current_thd_percent: 4.5,
    power_factor: 0.91,
  },
  presets: [
    {
      id: "ele-transformer-normal",
      label: "Transformer Normal",
      description: "Healthy transformer under acceptable arc-flash and quality conditions.",
      values: {
        equipment_type: "transformer",
        system_voltage_kv: 13.8,
        bolted_fault_current_ka: 22,
        breaker_interrupt_rating_ka: 31.5,
        voltage_drop_percent: 3.2,
      },
    },
    {
      id: "ele-switchgear-high-arc",
      label: "Switchgear High Arc",
      description: "Higher arc-flash case for protective review and PPE check.",
      values: {
        equipment_type: "switchgear",
        bolted_fault_current_ka: 35,
        clearing_time_sec: 0.35,
        working_distance_mm: 400,
      },
    },
    {
      id: "ele-vfd-harmonics",
      label: "VFD Harmonics",
      description: "Inverter-related harmonic stress case.",
      values: {
        equipment_type: "inverter",
        thd_voltage_percent: 7.5,
        motor_current_thd_percent: 11.5,
        power_factor: 0.86,
      },
    },
    {
      id: "ele-breaker-mismatch",
      label: "Breaker Mismatch",
      description: "Fault current near/above breaker interrupting capacity.",
      values: {
        equipment_type: "feeder_panel",
        bolted_fault_current_ka: 42,
        breaker_interrupt_rating_ka: 36,
      },
    },
  ],
  defaultChart: "bar",
  primaryMetrics: ["transformer_health_index", "arc_flash_energy_cal_cm2", "ppe_category", "voltage_drop_percent", "fault_current_ka", "breaker_coordination_margin", "load_utilization"],
};

export function buildElectricalOutcome(input: Record<string, unknown>): DisciplineOutcome {
  const equipmentType = String(input.equipment_type ?? "transformer").toLowerCase();
  const systemVoltageKv = toNumber(input.system_voltage_kv, 13.8);
  const ifault = toNumber(input.bolted_fault_current_ka, 22);
  const clearTime = toNumber(input.clearing_time_sec, 0.2);
  const distance = Math.max(toNumber(input.working_distance_mm, 455), 100);
  const breaker = toNumber(input.breaker_interrupt_rating_ka, 31.5);
  const voltageDrop = toNumber(input.voltage_drop_percent, 3.2);
  const thd = toNumber(input.thd_voltage_percent, 4.8);
  const currentThd = toNumber(input.motor_current_thd_percent, thd);
  const powerFactor = toNumber(input.power_factor, 0.91);

  const dgaScore = toNumber(input.dga_score, 8.2);
  const oilScore = toNumber(input.oil_quality_score, 7.9);
  const insulationScore = toNumber(input.insulation_score, 8.3);
  const loadScore = toNumber(input.load_factor_score, 7.5);

  const equipmentArcFactor = ELECTRICAL_EQUIPMENT_ARC_FACTOR[equipmentType] ?? 1.0;
  const equipmentHiBias = ELECTRICAL_EQUIPMENT_HI_BIAS[equipmentType] ?? 0.0;
  const arcFlash = round(
    0.35 * ifault * (clearTime / 0.2) * Math.pow(610 / distance, 1.1) * (1 + (systemVoltageKv / 100)) * equipmentArcFactor,
    2,
  );
  const healthIndexRaw =
    (dgaScore * ELECTRICAL_HI_WEIGHTS.dga)
    + (oilScore * ELECTRICAL_HI_WEIGHTS.oil)
    + (insulationScore * ELECTRICAL_HI_WEIGHTS.insulation)
    + (loadScore * ELECTRICAL_HI_WEIGHTS.load)
    + equipmentHiBias;
  const healthIndex = round(Math.max(0, Math.min(10, healthIndexRaw)), 2);

  let ppe = 0;
  if (arcFlash > 1.2) ppe = 1;
  if (arcFlash > 4) ppe = 2;
  if (arcFlash > 8) ppe = 3;
  if (arcFlash > 25) ppe = 4;

  const warnings: string[] = [];
  const redFlags: string[] = [];

  if (healthIndex < 4) warnings.push("PHY.TRANSFORMER_HEALTH_DEGRADED");
  if (arcFlash > 25) warnings.push("PHY.ARC_FLASH_HIGH_ALERT");
  if (currentThd > 5) warnings.push("PHY.CURRENT_THD_ELEVATED");
  if (powerFactor < 0.85) warnings.push("PHY.POWER_FACTOR_LOW");
  if (voltageDrop > 5) redFlags.push("PHY.ELECTRICAL_VOLTAGE_DROP_HIGH");
  if (thd > 8) redFlags.push("PHY.ELECTRICAL_THD_HIGH");
  if (ifault > breaker) redFlags.push("PHY.BREAKER_INTERRUPT_RATING_EXCEEDED");
  if (arcFlash > 40) redFlags.push("PHY.ARC_FLASH_ENERGY_CRITICAL");
  if (healthIndex < 3) redFlags.push("PHY.TRANSFORMER_HEALTH_CRITICAL");

  let intervalYears = 2.0;
  if (healthIndex < 3 || arcFlash > 40) intervalYears = 0.25;
  else if (healthIndex < 5 || arcFlash > 25) intervalYears = 0.5;
  else if (healthIndex < 7) intervalYears = 1.0;

  return {
    finalResults: {
      equipment_type: equipmentType,
      system_voltage_kv: round(systemVoltageKv, 2),
      transformer_health_index: healthIndex,
      arc_flash_energy_cal_cm2: arcFlash,
      ppe_category: ppe,
      voltage_drop_percent: round(voltageDrop, 2),
      fault_current_ka: round(ifault, 2),
      breaker_interrupt_rating_ka: round(breaker, 2),
      thd_voltage_percent: round(thd, 2),
      motor_current_thd_percent: round(currentThd, 2),
      power_factor: round(powerFactor, 3),
      inspection_interval_years: intervalYears,
      breaker_coordination_margin: round(ifault > 0 ? breaker / ifault : 999, 3),
      load_utilization: loadScore < 3 ? "HEAVILY_LOADED" : loadScore < 5 ? "MODERATELY_LOADED" : "LIGHTLY_LOADED",
      status: redFlags.length ? "CRITICAL" : warnings.length ? "WARNING" : "ACCEPTABLE",
    },
    warnings,
    redFlags,
  };
}
