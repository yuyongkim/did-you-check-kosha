import { DisciplineConfig } from "@/lib/types";
import { DisciplineOutcome, lookupInterpolatedTableValue, round, toNumber } from "@/lib/mock/shared";

export const VESSEL_STANDARD_REFS = [
  "ASME VIII UG-27",
  "ASME VIII UG-28",
  "ASME VIII UG-37",
  "API 510 thickness reassessment",
];

export const VESSEL_DEFAULT_RESULTS: Record<string, unknown> = {
  t_required_shell_mm: 11.2,
  corrosion_rate_mm_per_year: 0.2,
  remaining_life_years: 8.7,
  inspection_interval_years: 4,
  diameter_mm: 1500,
  slenderness_ld_ratio: 2,
  estimated_internal_volume_m3: 13.8,
  external_pressure_utilization: 0.62,
  nozzle_reinforcement_index: 1.12,
  status: "ACCEPTABLE",
  ffs_screening_level: "LEVEL0_FIT_FOR_SERVICE",
  repair_scope_screening: "NO_REPAIR_ACTION",
};

const VESSEL_ALLOWABLE_STRESS_TABLE_MPA: Record<string, Record<number, number>> = {
  "SA-516-60": { 20: 131, 100: 124, 200: 117, 300: 110, 400: 103 },
  "SA-516-65": { 20: 135, 100: 128, 200: 121, 300: 114, 400: 107 },
  "SA-516-70": { 20: 138, 100: 131, 200: 124, 300: 117, 400: 110 },
  "SA-515-70": { 20: 131, 100: 124, 200: 117, 300: 110, 400: 103 },
  "SA-537 Cl1": { 20: 155, 100: 148, 200: 141, 300: 134, 400: 127 },
  "SA-387 Gr11 Cl2": { 20: 138, 100: 138, 200: 132, 300: 126, 400: 120, 500: 108, 550: 101 },
  "SA-387 Gr22 Cl2": { 20: 138, 100: 138, 200: 134, 300: 128, 400: 122, 500: 112, 550: 105 },
  "SA-387 Gr91 Cl2": { 20: 160, 100: 156, 200: 152, 300: 148, 400: 145, 500: 138, 550: 132, 600: 125 },
  "SA-240-304": { 20: 138, 100: 131, 200: 124, 300: 117, 400: 110, 500: 97 },
  "SA-240-304L": { 20: 132, 100: 125, 200: 118, 300: 111, 400: 104, 500: 90 },
  "SA-240-304H": { 20: 145, 100: 139, 200: 133, 300: 126, 400: 119, 500: 106, 550: 99 },
  "SA-240-316": { 20: 138, 100: 131, 200: 124, 300: 117, 400: 110, 500: 97 },
  "SA-240-316L": { 20: 132, 100: 125, 200: 118, 300: 111, 400: 104, 500: 90 },
  "SA-240-321": { 20: 138, 100: 131, 200: 125, 300: 119, 400: 113, 500: 97 },
  "SA-240-347": { 20: 138, 100: 131, 200: 126, 300: 120, 400: 114, 500: 99 },
  "SA-240-310S": { 20: 145, 100: 140, 200: 135, 300: 129, 400: 123, 500: 113, 550: 106 },
};

const VESSEL_MATERIAL_TEMP_LIMIT_C: Record<string, number> = {
  "SA-516-60": 425,
  "SA-516-65": 425,
  "SA-516-70": 425,
  "SA-515-70": 425,
  "SA-537 Cl1": 425,
  "SA-387 Gr11 Cl2": 593,
  "SA-387 Gr22 Cl2": 593,
  "SA-387 Gr91 Cl2": 650,
  "SA-240-304": 538,
  "SA-240-304L": 538,
  "SA-240-304H": 650,
  "SA-240-316": 538,
  "SA-240-316L": 538,
  "SA-240-321": 538,
  "SA-240-347": 538,
  "SA-240-310S": 650,
};

const VESSEL_VALID_JOINT_EFFICIENCY = [1.0, 0.95, 0.9, 0.85, 0.8, 0.7, 0.6];

function isVerticalType(vesselType: string): boolean {
  return ["vertical_vessel", "column_tower", "reactor"].includes(vesselType);
}

function defaultHeadDepthMm(headType: string, insideRadiusMm: number): number {
  if (headType === "flat") return 0;
  if (headType === "hemispherical") return insideRadiusMm;
  if (headType === "torispherical") return 0.36 * insideRadiusMm;
  return 0.5 * insideRadiusMm;
}

function headVolumeFactor(headType: string): number {
  if (headType === "flat") return 0;
  if (headType === "hemispherical") return 4 / 3;
  if (headType === "torispherical") return 0.5;
  return 2 / 3;
}

function externalPressureAllowableScreenMpa(shellThicknessMm: number, diameterMm: number, spanMm: number): number {
  if (shellThicknessMm <= 0 || diameterMm <= 0 || spanMm <= 0) return 0;
  const E = 200000;
  const nu = 0.3;
  const tOverD = shellThicknessMm / diameterMm;
  const ld = spanMm / diameterMm;
  const elastic = ((2 * E) / Math.sqrt(3 * (1 - nu ** 2))) * (tOverD ** 3);
  const slendernessFactor = Math.min(1, 4 / Math.max(ld, 1));
  return elastic * slendernessFactor * 0.5;
}

function nozzleReinforcementIndex(
  nozzleOdMm: number,
  shellThicknessMm: number,
  requiredShellThicknessMm: number,
  padThicknessMm: number,
  padWidthMm: number,
): number | null {
  if (nozzleOdMm <= 0 || shellThicknessMm <= 0 || requiredShellThicknessMm <= 0) return null;
  const requiredArea = nozzleOdMm * requiredShellThicknessMm;
  const shellExcess = Math.max(shellThicknessMm - requiredShellThicknessMm, 0);
  const availableShell = 2 * nozzleOdMm * shellExcess;
  const availablePad = Math.max(padThicknessMm, 0) * Math.max(padWidthMm, 0);
  if (requiredArea <= 0) return null;
  return (availableShell + availablePad) / requiredArea;
}

export const VESSEL_CONFIG: DisciplineConfig = {
  discipline: "vessel",
  title: "Static Equipment Integrity",
  subtitle: "ASME VIII and API 510 vessel thickness and remaining life checks",
  shortLabel: "VES",
  formFields: [
    {
      name: "material",
      label: "Material",
      type: "select",
      optionGroups: [
        {
          label: "Carbon / Carbon-Mn Steel",
          options: [
            { label: "SA-516-60", value: "SA-516-60" },
            { label: "SA-516-65", value: "SA-516-65" },
            { label: "SA-516-70", value: "SA-516-70" },
            { label: "SA-515-70", value: "SA-515-70" },
            { label: "SA-537 Cl1", value: "SA-537 Cl1" },
          ],
        },
        {
          label: "Low Alloy Steel",
          options: [
            { label: "SA-387 Gr11 Cl2", value: "SA-387 Gr11 Cl2" },
            { label: "SA-387 Gr22 Cl2", value: "SA-387 Gr22 Cl2" },
            { label: "SA-387 Gr91 Cl2", value: "SA-387 Gr91 Cl2" },
          ],
        },
        {
          label: "Stainless Steel",
          options: [
            { label: "SA-240-304", value: "SA-240-304" },
            { label: "SA-240-304L", value: "SA-240-304L" },
            { label: "SA-240-304H", value: "SA-240-304H" },
            { label: "SA-240-316", value: "SA-240-316" },
            { label: "SA-240-316L", value: "SA-240-316L" },
            { label: "SA-240-321", value: "SA-240-321" },
            { label: "SA-240-347", value: "SA-240-347" },
            { label: "SA-240-310S", value: "SA-240-310S" },
          ],
        },
      ],
    },
    {
      name: "vessel_type",
      label: "Vessel Type",
      type: "select",
      options: [
        { label: "Horizontal Drum", value: "horizontal_drum" },
        { label: "Vertical Vessel", value: "vertical_vessel" },
        { label: "Column / Tower", value: "column_tower" },
        { label: "Heat Exchanger Shell", value: "hx_shell" },
        { label: "Reactor", value: "reactor" },
      ],
    },
    { name: "design_pressure_mpa", label: "Design Pressure", unit: "MPa", type: "number", min: 0.1, max: 35, step: 0.1, placeholder: "2.0" },
    { name: "design_temperature_c", label: "Design Temperature", unit: "C", type: "number", min: -50, max: 650, step: 1, placeholder: "200" },
    { name: "inside_radius_mm", label: "Inside Radius", unit: "mm", type: "number", min: 100, max: 4000, step: 1, placeholder: "750" },
    {
      name: "shell_length_mm",
      label: "Shell Length",
      unit: "mm",
      type: "number",
      min: 500,
      max: 50000,
      step: 10,
      helper: "Horizontal/hx context: tangent-to-tangent shell length",
      showWhen: { field: "vessel_type", equalsAny: ["horizontal_drum", "hx_shell"] },
    },
    {
      name: "straight_shell_height_mm",
      label: "Straight Shell Height",
      unit: "mm",
      type: "number",
      min: 500,
      max: 80000,
      step: 10,
      helper: "Vertical/column context: straight shell height",
      showWhen: { field: "vessel_type", equalsAny: ["vertical_vessel", "column_tower", "reactor"] },
    },
    {
      name: "head_type",
      label: "Head Type",
      type: "select",
      options: [
        { label: "Ellipsoidal 2:1", value: "ellipsoidal_2_1" },
        { label: "Torispherical", value: "torispherical" },
        { label: "Hemispherical", value: "hemispherical" },
        { label: "Flat", value: "flat" },
      ],
    },
    { name: "head_depth_mm", label: "Head Depth", unit: "mm", type: "number", min: 0, max: 5000, step: 1, placeholder: "375" },
    { name: "nozzle_od_mm", label: "Nozzle OD", unit: "mm", type: "number", min: 25, max: 2000, step: 1, placeholder: "350" },
    { name: "external_pressure_mpa", label: "External Pressure", unit: "MPa", type: "number", min: 0, max: 5, step: 0.01, placeholder: "0.25" },
    { name: "reinforcement_pad_thickness_mm", label: "Reinf. Pad Thickness", unit: "mm", type: "number", min: 0, max: 80, step: 0.1, placeholder: "6" },
    { name: "reinforcement_pad_width_mm", label: "Reinf. Pad Width", unit: "mm", type: "number", min: 0, max: 2000, step: 1, placeholder: "180" },
    {
      name: "joint_efficiency",
      label: "Joint Efficiency (E)",
      type: "select",
      options: [
        { label: "Type 1 (1.00)", value: "1.0" },
        { label: "Type 1 alt (0.95)", value: "0.95" },
        { label: "Type 2 alt (0.90)", value: "0.9" },
        { label: "Type 2 (0.85)", value: "0.85" },
        { label: "Type 3 alt (0.80)", value: "0.8" },
        { label: "Type 3 (0.70)", value: "0.7" },
        { label: "Type 4 (0.60)", value: "0.6" },
      ],
    },
    { name: "t_current_mm", label: "Current Thickness", unit: "mm", type: "number", min: 1, max: 200, step: 0.1, placeholder: "18" },
    { name: "corrosion_allowance_mm", label: "Corrosion Allowance", unit: "mm", type: "number", min: 0, max: 20, step: 0.1, placeholder: "1.5" },
    { name: "assumed_corrosion_rate_mm_per_year", label: "Corrosion Rate", unit: "mm/yr", type: "number", min: 0.01, max: 10, step: 0.01, placeholder: "0.2" },
  ],
  sampleInput: {
    material: "SA-516-70",
    vessel_type: "horizontal_drum",
    design_pressure_mpa: 2.0,
    design_temperature_c: 200,
    inside_radius_mm: 750,
    shell_length_mm: 3000,
    straight_shell_height_mm: 6000,
    head_type: "ellipsoidal_2_1",
    head_depth_mm: 375,
    nozzle_od_mm: 350,
    external_pressure_mpa: 0.25,
    reinforcement_pad_thickness_mm: 6,
    reinforcement_pad_width_mm: 180,
    joint_efficiency: "0.85",
    t_current_mm: 18,
    corrosion_allowance_mm: 1.5,
    assumed_corrosion_rate_mm_per_year: 0.2,
  },
  presets: [
    {
      id: "ves-hdrum-standard",
      label: "Horizontal Drum",
      description: "Typical horizontal drum in moderate pressure and temperature.",
      values: {
        vessel_type: "horizontal_drum",
        head_type: "ellipsoidal_2_1",
        material: "SA-516-70",
        design_pressure_mpa: 2.0,
        design_temperature_c: 200,
      },
    },
    {
      id: "ves-column-high-temp",
      label: "Column High Temp",
      description: "Tall column with alloy steel and higher process temperature.",
      values: {
        vessel_type: "column_tower",
        material: "SA-387 Gr22 Cl2",
        design_pressure_mpa: 3.5,
        design_temperature_c: 480,
        straight_shell_height_mm: 16000,
        shell_length_mm: 4000,
      },
    },
    {
      id: "ves-vacuum-risk",
      label: "External Pressure",
      description: "Vacuum/external pressure screening-focused case.",
      values: {
        vessel_type: "vertical_vessel",
        external_pressure_mpa: 0.5,
        design_pressure_mpa: 1.1,
        design_temperature_c: 180,
        t_current_mm: 12,
      },
    },
    {
      id: "ves-nozzle-hotspot",
      label: "Nozzle Hotspot",
      description: "Nozzle opening and pad reinforcement screening case.",
      values: {
        vessel_type: "reactor",
        nozzle_od_mm: 600,
        reinforcement_pad_thickness_mm: 4,
        reinforcement_pad_width_mm: 80,
        t_current_mm: 14,
      },
    },
  ],
  defaultChart: "trend",
  primaryMetrics: [
    "allowable_stress_mpa",
    "joint_efficiency",
    "t_required_shell_mm",
    "remaining_life_years",
    "inspection_interval_years",
    "diameter_mm",
    "slenderness_ld_ratio",
    "external_pressure_utilization",
    "nozzle_reinforcement_index",
    "estimated_internal_volume_m3",
    "ffs_screening_level",
    "repair_scope_screening",
  ],
};

export function buildVesselOutcome(input: Record<string, unknown>): DisciplineOutcome {
  const material = String(input.material ?? "SA-516-70");
  const vesselType = String(input.vessel_type ?? "horizontal_drum");
  const pressure = toNumber(input.design_pressure_mpa, 2.0);
  const temperature = toNumber(input.design_temperature_c, 200);
  const radius = toNumber(input.inside_radius_mm, 750);
  const shellLength = toNumber(input.shell_length_mm, 3000);
  const shellHeight = toNumber(input.straight_shell_height_mm, 6000);
  const headType = String(input.head_type ?? "ellipsoidal_2_1");
  const efficiency = toNumber(input.joint_efficiency, 0.85);
  const currentT = toNumber(input.t_current_mm, 18);
  const corrosionRate = Math.max(toNumber(input.assumed_corrosion_rate_mm_per_year, 0.2), 0.001);
  const ca = toNumber(input.corrosion_allowance_mm, 1.5);
  const nozzleOd = toNumber(input.nozzle_od_mm, 350);
  const externalPressure = Math.max(toNumber(input.external_pressure_mpa, 0.25), 0);
  const padThickness = Math.max(toNumber(input.reinforcement_pad_thickness_mm, 6), 0);
  const padWidth = Math.max(toNumber(input.reinforcement_pad_width_mm, 180), 0);
  const diameter = radius * 2;
  const governingSpan = isVerticalType(vesselType) ? shellHeight : shellLength;
  const headDepth = toNumber(input.head_depth_mm, defaultHeadDepthMm(headType, radius));

  const allowableStress = round(lookupInterpolatedTableValue(VESSEL_ALLOWABLE_STRESS_TABLE_MPA, material, temperature, "SA-516-70"), 2);
  const tempLimit = VESSEL_MATERIAL_TEMP_LIMIT_C[material] ?? 425;
  const validJointEfficiency = VESSEL_VALID_JOINT_EFFICIENCY.includes(efficiency);
  const denominator = (allowableStress * efficiency) - (0.6 * pressure);
  const tReq = round(denominator > 0 ? ((pressure * radius) / denominator) + ca : Number.POSITIVE_INFINITY, 2);
  const rl = round(Math.max((currentT - tReq) / corrosionRate, 0), 2);
  const thicknessMargin = round(currentT - tReq, 2);
  const slenderness = round(governingSpan / Math.max(diameter, 1e-9), 3);
  const shellArea = round((Math.PI * diameter * governingSpan) / 1_000_000, 3);
  const bodyVolume = (Math.PI * (radius ** 2) * governingSpan) / 1_000_000_000;
  const headsVolume = (headVolumeFactor(headType) * Math.PI * (radius ** 3)) / 1_000_000_000;
  const estVolume = round(bodyVolume + headsVolume, 3);
  const externalAllowable = externalPressureAllowableScreenMpa(currentT, diameter, governingSpan);
  const externalUtilization = externalAllowable > 0 ? round(externalPressure / externalAllowable, 3) : null;
  const openingRatio = round(nozzleOd / Math.max(diameter, 1e-9), 3);
  const nozzleIndex = nozzleReinforcementIndex(nozzleOd, currentT, tReq, padThickness, padWidth);

  let inspectionInterval = Math.min(10, 0.5 * rl);
  if (corrosionRate > 1) inspectionInterval = Math.min(inspectionInterval, 1);
  inspectionInterval = rl < 2 ? Math.min(inspectionInterval, 0.5) : inspectionInterval;
  inspectionInterval = round(Math.max(0.25, inspectionInterval), 2);

  const warnings: string[] = [];
  const redFlags: string[] = [];

  if (!validJointEfficiency) warnings.push("STD.JOINT_EFFICIENCY_INVALID_REVIEW");
  if (pressure > 10) warnings.push("STD.HIGH_PRESSURE_REVIEW_REQUIRED");
  if (thicknessMargin < 0.5 && thicknessMargin >= 0) warnings.push("PHY.VESSEL_LOCAL_THINNING_SCREEN_RECOMMENDED");
  if (corrosionRate > 2) warnings.push("PHY.VESSEL_CORROSION_RATE_ELEVATED");
  if (slenderness > 8) warnings.push("PHY.VESSEL_HIGH_LD_RATIO");
  if (externalUtilization !== null && externalUtilization > 1 && externalUtilization <= 1.2) warnings.push("PHY.VESSEL_EXTERNAL_PRESSURE_REVIEW");
  if (nozzleIndex !== null && nozzleIndex < 1 && nozzleIndex >= 0.8) warnings.push("PHY.VESSEL_NOZZLE_REINFORCEMENT_REVIEW");
  if (openingRatio > 0.8) warnings.push("PHY.VESSEL_NOZZLE_REINFORCEMENT_REVIEW");
  if (temperature > tempLimit) redFlags.push("PHY.TEMPERATURE_LIMIT_EXCEEDED");
  if (currentT <= tReq) redFlags.push("PHY.VESSEL_THICKNESS_BELOW_REQUIRED");
  if (corrosionRate > 5) redFlags.push("PHY.VESSEL_CORROSION_RATE_CRITICAL");
  if (externalUtilization !== null && externalUtilization > 1.2) redFlags.push("PHY.VESSEL_EXTERNAL_PRESSURE_RISK");
  if (nozzleIndex !== null && nozzleIndex < 0.8) redFlags.push("PHY.VESSEL_NOZZLE_REINFORCEMENT_RISK");

  return {
    finalResults: {
      material,
      vessel_type: vesselType,
      head_type: headType,
      allowable_stress_mpa: allowableStress,
      joint_efficiency: round(efficiency, 2),
      t_required_shell_mm: tReq,
      thickness_margin_mm: thicknessMargin,
      corrosion_rate_mm_per_year: round(corrosionRate, 3),
      remaining_life_years: rl,
      inspection_interval_years: inspectionInterval,
      diameter_mm: round(diameter, 2),
      governing_span_mm: round(governingSpan, 2),
      head_depth_mm_used: round(headDepth, 2),
      nozzle_od_mm: round(nozzleOd, 2),
      nozzle_opening_ratio: openingRatio,
      external_pressure_mpa_input: externalPressure,
      external_pressure_allowable_screen_mpa: round(externalAllowable, 4),
      external_pressure_utilization: externalUtilization,
      reinforcement_pad_thickness_mm_used: round(padThickness, 2),
      reinforcement_pad_width_mm_used: round(padWidth, 2),
      nozzle_reinforcement_index: nozzleIndex === null ? null : round(nozzleIndex, 3),
      slenderness_ld_ratio: slenderness,
      shell_surface_area_m2: shellArea,
      estimated_internal_volume_m3: estVolume,
      ffs_screening_level: thicknessMargin < 0 ? "LEVEL3_DETAILED_ASSESSMENT_REQUIRED"
        : rl < 2 || thicknessMargin < 0.5 ? "LEVEL2_ENGINEERING_REVIEW"
        : corrosionRate > 0.5 || rl < 5 ? "LEVEL1_MONITOR_CLOSELY"
        : "LEVEL0_FIT_FOR_SERVICE",
      repair_scope_screening: thicknessMargin < 0 ? "REPAIR_OR_REPLACE"
        : (rl < 2 || thicknessMargin < 0.5) ? "EVALUATE_REPAIR_FEASIBILITY"
        : corrosionRate > 0.5 ? "CONSIDER_WELD_OVERLAY_OR_COATING"
        : "NO_REPAIR_ACTION",
      status: redFlags.length ? "CRITICAL" : warnings.length ? "WARNING" : "ACCEPTABLE",
    },
    warnings,
    redFlags,
  };
}
