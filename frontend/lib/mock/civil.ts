import { DisciplineConfig } from "@/lib/types";
import { DisciplineOutcome, round, toNumber } from "@/lib/mock/shared";

export const CIVIL_STANDARD_REFS = [
  "ACI 318 flexural strength",
  "ACI 562 substantial damage criteria",
];

export const CIVIL_DEFAULT_RESULTS: Record<string, unknown> = {
  dc_ratio: 0.78,
  carbonation_depth_mm: 9.5,
  substantial_damage: false,
  years_to_corrosion_init: 34,
  inspection_interval_years: 2,
  status: "ACCEPTABLE",
  repair_priority: "PRIORITY_4_ROUTINE_MAINTENANCE",
  consequence_category: "LOW_CONSEQUENCE",
};

const CIVIL_ENVIRONMENT_FACTOR: Record<string, number> = {
  indoor_dry: 0.8,
  outdoor_urban: 1.0,
  coastal_marine: 1.25,
  industrial_chemical: 1.2,
  splash_zone: 1.35,
  buried_soil: 1.1,
  desert_hot: 1.05,
  freeze_thaw: 1.18,
  acidic_soil: 1.3,
  offshore: 1.4,
};

export const CIVIL_CONFIG: DisciplineConfig = {
  discipline: "civil",
  title: "Civil and Concrete Integrity",
  subtitle: "ACI-based damage classification, carbonation, and durability checks",
  shortLabel: "CIV",
  formFields: [
    {
      name: "element_type",
      label: "Element Type",
      type: "select",
      options: [
        { label: "Beam", value: "beam" },
        { label: "Column", value: "column" },
        { label: "Slab", value: "slab" },
        { label: "Foundation", value: "foundation" },
        { label: "Retaining Wall", value: "retaining_wall" },
        { label: "Pedestal", value: "pedestal" },
        { label: "Pile Cap", value: "pile_cap" },
        { label: "Mat Foundation", value: "mat_foundation" },
      ],
    },
    {
      name: "environment_exposure",
      label: "Exposure Environment",
      type: "select",
      options: [
        { label: "Indoor Dry", value: "indoor_dry" },
        { label: "Outdoor Urban", value: "outdoor_urban" },
        { label: "Coastal Marine", value: "coastal_marine" },
        { label: "Industrial Chemical", value: "industrial_chemical" },
        { label: "Splash Zone", value: "splash_zone" },
        { label: "Buried Soil", value: "buried_soil" },
        { label: "Desert Hot", value: "desert_hot" },
        { label: "Freeze-Thaw", value: "freeze_thaw" },
        { label: "Acidic Soil", value: "acidic_soil" },
        { label: "Offshore Marine", value: "offshore" },
      ],
    },
    { name: "fc_mpa", label: "f'c", unit: "MPa", type: "number", min: 15, max: 80, step: 0.1 },
    { name: "fy_mpa", label: "Rebar Fy", unit: "MPa", type: "number", min: 250, max: 700, step: 1 },
    { name: "width_mm", label: "Section Width b", unit: "mm", type: "number", min: 100, max: 3000, step: 1 },
    { name: "effective_depth_mm", label: "Effective Depth d", unit: "mm", type: "number", min: 100, max: 3000, step: 1 },
    { name: "rebar_area_mm2", label: "Rebar Area As", unit: "mm2", type: "number", min: 100, max: 100000, step: 1 },
    { name: "demand_moment_knm", label: "Demand Moment", unit: "kN*m", type: "number", min: 0, max: 2000, step: 1 },
    { name: "lateral_capacity_loss_percent", label: "Lateral Capacity Loss", unit: "%", type: "number", min: 0, max: 100, step: 0.1 },
    { name: "affected_area_percent", label: "Affected Area", unit: "%", type: "number", min: 0, max: 100, step: 0.1 },
    { name: "vertical_capacity_loss_percent", label: "Vertical Capacity Loss", unit: "%", type: "number", min: 0, max: 100, step: 0.1 },
    { name: "carbonation_coeff_mm_sqrt_year", label: "Carbonation k", unit: "mm/sqrt(year)", type: "number", min: 0.1, max: 10, step: 0.1 },
    { name: "service_years", label: "Service Years", unit: "years", type: "number", min: 0, max: 120, step: 1 },
    { name: "cover_thickness_mm", label: "Cover Thickness", unit: "mm", type: "number", min: 15, max: 120, step: 1 },
    { name: "crack_width_mm", label: "Crack Width", unit: "mm", type: "number", min: 0, max: 5, step: 0.01 },
    { name: "spalling_area_percent", label: "Spalling Area", unit: "%", type: "number", min: 0, max: 100, step: 0.1 },
    { name: "foundation_settlement_mm", label: "Foundation Settlement", unit: "mm", type: "number", min: 0, max: 200, step: 0.1 },
  ],
  sampleInput: {
    element_type: "beam",
    environment_exposure: "outdoor_urban",
    fc_mpa: 35,
    fy_mpa: 420,
    width_mm: 300,
    effective_depth_mm: 550,
    rebar_area_mm2: 2450,
    demand_moment_knm: 280,
    lateral_capacity_loss_percent: 8,
    affected_area_percent: 12,
    vertical_capacity_loss_percent: 6,
    carbonation_coeff_mm_sqrt_year: 1.8,
    service_years: 18,
    cover_thickness_mm: 40,
    crack_width_mm: 0.22,
    spalling_area_percent: 5,
    foundation_settlement_mm: 8,
  },
  presets: [
    {
      id: "civ-beam-normal",
      label: "Beam Normal",
      description: "Nominal RC beam durability case under urban exposure.",
      values: {
        element_type: "beam",
        environment_exposure: "outdoor_urban",
        demand_moment_knm: 280,
        crack_width_mm: 0.22,
      },
    },
    {
      id: "civ-marine-durability",
      label: "Marine Durability",
      description: "Coastal/offshore durability stress case with faster carbonation.",
      values: {
        element_type: "column",
        environment_exposure: "offshore",
        service_years: 28,
        cover_thickness_mm: 35,
        carbonation_coeff_mm_sqrt_year: 2.5,
      },
    },
    {
      id: "civ-substantial-damage",
      label: "Substantial Damage",
      description: "ACI 562 substantial damage threshold scenario.",
      values: {
        element_type: "foundation",
        lateral_capacity_loss_percent: 35,
        affected_area_percent: 40,
        vertical_capacity_loss_percent: 24,
      },
    },
    {
      id: "civ-settlement-alert",
      label: "Settlement Alert",
      description: "Foundation settlement-driven risk review case.",
      values: {
        element_type: "mat_foundation",
        foundation_settlement_mm: 32,
        crack_width_mm: 0.48,
        spalling_area_percent: 22,
      },
    },
  ],
  defaultChart: "gauge",
  primaryMetrics: ["dc_ratio", "substantial_damage", "carbonation_depth_mm", "years_to_corrosion_init", "status", "repair_priority", "consequence_category"],
};

export function buildCivilOutcome(input: Record<string, unknown>): DisciplineOutcome {
  const elementType = String(input.element_type ?? "beam").toLowerCase();
  const exposure = String(input.environment_exposure ?? "outdoor_urban").toLowerCase();
  const fc = Math.max(toNumber(input.fc_mpa, 35), 1);
  const fy = Math.max(toNumber(input.fy_mpa, 420), 1);
  const b = Math.max(toNumber(input.width_mm, 300), 1);
  const d = Math.max(toNumber(input.effective_depth_mm, 550), 1);
  const as = Math.max(toNumber(input.rebar_area_mm2, 2450), 1);
  const demandMoment = Math.max(toNumber(input.demand_moment_knm, 280), 0);
  const a = (as * fy) / Math.max(0.85 * fc * b, 0.01);
  const mn = (as * fy * (d - (a / 2))) / 1_000_000;
  const phiMn = 0.9 * mn;
  const dcRatio = round(demandMoment / Math.max(phiMn, 0.01), 3);

  const serviceYears = Math.max(toNumber(input.service_years, 18), 0);
  const exposureFactor = CIVIL_ENVIRONMENT_FACTOR[exposure] ?? 1.0;
  const carbCoeff = Math.max(toNumber(input.carbonation_coeff_mm_sqrt_year, 1.8), 0.01) * exposureFactor;
  const cover = Math.max(toNumber(input.cover_thickness_mm, 40), 1);
  const carbonationDepth = round(carbCoeff * Math.sqrt(serviceYears), 2);
  const corrosionInitiated = carbonationDepth >= cover;
  const yearsToCorrosion = corrosionInitiated ? 0 : round(((cover - carbonationDepth) / carbCoeff) ** 2, 1);

  const lateralLoss = toNumber(input.lateral_capacity_loss_percent, 8);
  const affectedArea = toNumber(input.affected_area_percent, 12);
  const verticalLoss = toNumber(input.vertical_capacity_loss_percent, 6);
  const substantialDamage = lateralLoss >= 33 || (affectedArea >= 30 && verticalLoss >= 20);
  const damageMode = lateralLoss >= 33
    ? "type1_lateral"
    : substantialDamage ? "type2_vertical" : "none";

  const warnings: string[] = [];
  const redFlags: string[] = [];

  const crackWidth = toNumber(input.crack_width_mm, 0.22);
  const spallingArea = toNumber(input.spalling_area_percent, 5);
  const settlement = toNumber(input.foundation_settlement_mm, 8);

  if (dcRatio >= 1.0 && dcRatio < 1.2) warnings.push("PHY.CIVIL_MEMBER_OVERUTILIZED");
  if (dcRatio >= 1.2) redFlags.push("PHY.CIVIL_FLEXURE_OVERSTRESS");
  if (crackWidth > 0.4) redFlags.push("PHY.CIVIL_CRACK_WIDTH_HIGH");
  if (spallingArea > 20) redFlags.push("PHY.CIVIL_SPALLING_AREA_HIGH");
  if (substantialDamage) redFlags.push("PHY.CIVIL_SUBSTANTIAL_DAMAGE");
  if (carbonationDepth >= cover) redFlags.push("PHY.CIVIL_REBAR_CORROSION_INITIATED");
  if (settlement > 15 && settlement <= 25) warnings.push("PHY.CIVIL_FOUNDATION_SETTLEMENT_ELEVATED");
  if (settlement > 25) redFlags.push("PHY.CIVIL_FOUNDATION_SETTLEMENT_HIGH");

  let status = "ACCEPTABLE";
  if (substantialDamage || corrosionInitiated || dcRatio >= 1.2) status = "CRITICAL";
  else if (dcRatio >= 1.0 || crackWidth > 0.4 || spallingArea > 20) status = "WARNING";

  return {
    finalResults: {
      element_type: elementType,
      environment_exposure: exposure,
      exposure_factor: round(exposureFactor, 2),
      phi_mn_knm: round(phiMn, 2),
      dc_ratio: dcRatio,
      carbonation_depth_mm: carbonationDepth,
      substantial_damage: substantialDamage,
      damage_mode: damageMode,
      corrosion_initiated: corrosionInitiated,
      years_to_corrosion_init: yearsToCorrosion,
      crack_width_mm: round(crackWidth, 2),
      spalling_area_percent: round(spallingArea, 2),
      foundation_settlement_mm: round(settlement, 2),
      inspection_interval_years: redFlags.length ? 0.25 : warnings.length ? 1 : 2,
      repair_priority: (() => {
        const s = redFlags.length ? "CRITICAL" : warnings.length ? status : "ACCEPTABLE";
        if (s === "CRITICAL") return "PRIORITY_1_IMMEDIATE";
        const urgentCount = [crackWidth > 0.4, spallingArea > 20, settlement > 25, dcRatio >= 1.0].filter(Boolean).length;
        if (urgentCount >= 2) return "PRIORITY_2_NEXT_SHUTDOWN";
        if (urgentCount >= 1) return "PRIORITY_3_PLANNED_REPAIR";
        return "PRIORITY_4_ROUTINE_MAINTENANCE";
      })(),
      consequence_category: (() => {
        const criticalElements = ["foundation", "pile_cap", "mat_foundation", "column"];
        const isCritical = criticalElements.includes(elementType);
        if (substantialDamage && isCritical) return "HIGH_CONSEQUENCE";
        if (substantialDamage || (isCritical && settlement > 25)) return "MEDIUM_CONSEQUENCE";
        return "LOW_CONSEQUENCE";
      })(),
      status: redFlags.length ? "CRITICAL" : warnings.length ? status : "ACCEPTABLE",
    },
    warnings,
    redFlags,
  };
}
