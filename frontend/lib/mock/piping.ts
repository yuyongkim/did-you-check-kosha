import { DisciplineOutcome, parseDate, round, toNumber, yearsBetween } from "@/lib/mock/shared";
import { PIPING_CONFIG } from "@/lib/mock/piping.config";
import {
  PIPING_ALLOWABLE_STRESS_TABLE_MPA,
  PIPING_DEFAULT_RESULTS,
  PIPING_HYDROTEST_CHLORIDE_LIMIT_PPM,
  PIPING_MATERIAL_GROUP,
  PIPING_NPS_TO_OD_MM,
  PIPING_SERVICE_CORROSION_FACTOR,
  PIPING_STANDARD_REFS,
  getPipingTemperatureWindowC,
  PIPING_WELD_EFFICIENCY,
  PIPING_Y_COEFFICIENT,
  PIPING_FLUID_CORROSION_FACTOR,
  PipingMaterialGroup,
} from "@/lib/mock/piping.constants";

export { PIPING_CONFIG, PIPING_DEFAULT_RESULTS, PIPING_STANDARD_REFS };

function getPipingMaterialGroup(material: string): PipingMaterialGroup {
  const mapped = PIPING_MATERIAL_GROUP[material];
  if (mapped) return mapped;

  const normalized = material.toUpperCase();
  if (normalized.includes("S31803") || normalized.includes("S32205") || normalized.includes("S32750")) {
    return "duplex_stainless";
  }
  if (normalized.includes("TP3")) return "stainless_steel";
  if (normalized.includes("P11") || normalized.includes("P22") || normalized.includes("P5") || normalized.includes("P9") || normalized.includes("P91")) {
    return "low_alloy_steel";
  }
  if (normalized.includes("N08825") || normalized.includes("N06625") || normalized.includes("N04400") || normalized.includes("ALLOY")) {
    return "nickel_alloy";
  }
  return "carbon_steel";
}

function resolvePipingOdMm(nps: number): number {
  if (Object.prototype.hasOwnProperty.call(PIPING_NPS_TO_OD_MM, nps)) {
    return PIPING_NPS_TO_OD_MM[nps];
  }

  const keys = Object.keys(PIPING_NPS_TO_OD_MM).map(Number).sort((a, b) => a - b);
  if (nps <= keys[0]) return PIPING_NPS_TO_OD_MM[keys[0]];
  if (nps >= keys[keys.length - 1]) return PIPING_NPS_TO_OD_MM[keys[keys.length - 1]];

  for (let idx = 1; idx < keys.length; idx += 1) {
    const lo = keys[idx - 1];
    const hi = keys[idx];
    if (nps <= hi) {
      const loValue = PIPING_NPS_TO_OD_MM[lo];
      const hiValue = PIPING_NPS_TO_OD_MM[hi];
      const ratio = (nps - lo) / (hi - lo);
      return loValue + (hiValue - loValue) * ratio;
    }
  }
  return 168.3;
}

function lookupPipingAllowableStressMpa(material: string, temperatureC: number): number {
  const table = PIPING_ALLOWABLE_STRESS_TABLE_MPA[material] ?? PIPING_ALLOWABLE_STRESS_TABLE_MPA["SA-106 Gr.B"];
  const points = Object.keys(table).map(Number).sort((a, b) => a - b);

  if (temperatureC <= points[0]) return table[points[0]];
  if (temperatureC >= points[points.length - 1]) return table[points[points.length - 1]];

  for (let idx = 1; idx < points.length; idx += 1) {
    const loTemp = points[idx - 1];
    const hiTemp = points[idx];
    if (temperatureC <= hiTemp) {
      const loStress = table[loTemp];
      const hiStress = table[hiTemp];
      const ratio = (temperatureC - loTemp) / (hiTemp - loTemp);
      return loStress + (hiStress - loStress) * ratio;
    }
  }

  return table[points[points.length - 1]];
}

export function buildPipingOutcome(input: Record<string, unknown>): DisciplineOutcome {
  const pressure = toNumber(input.design_pressure_mpa, 4.5);
  const temperature = toNumber(input.design_temperature_c, 250);
  const nps = toNumber(input.nps, 6);
  const material = String(input.material ?? "SA-106 Gr.B");
  const temperatureProfile = String(input.temperature_profile ?? "strict_process").toLowerCase();
  const weldType = String(input.weld_type ?? "seamless").toLowerCase();
  const serviceType = String(input.service_type ?? "general").toLowerCase();
  const fluidType = String(input.fluid_type ?? "hydrocarbon_dry").toLowerCase();
  const chloridePpm = input.chloride_ppm === undefined ? null : toNumber(input.chloride_ppm, 0);
  const hasInternalCoating = Boolean(input.has_internal_coating);
  const hasCaInput = input.corrosion_allowance_mm !== undefined && input.corrosion_allowance_mm !== null;
  const ca = toNumber(input.corrosion_allowance_mm ?? input.CA_mm, 1.5);
  const materialGroup = getPipingMaterialGroup(material);
  const { softLimitC, hardLimitC, profile } = getPipingTemperatureWindowC(materialGroup, temperatureProfile);
  const chlorideLimit = PIPING_HYDROTEST_CHLORIDE_LIMIT_PPM[materialGroup];
  const weldEfficiency = PIPING_WELD_EFFICIENCY[weldType] ?? 0.85;
  const yCoefficient = PIPING_Y_COEFFICIENT;
  const odMm = resolvePipingOdMm(nps);
  const allowableStressMpa = round(lookupPipingAllowableStressMpa(material, temperature), 2);
  const serviceFactor = PIPING_SERVICE_CORROSION_FACTOR[serviceType] ?? 1.0;
  const fluidFactor = PIPING_FLUID_CORROSION_FACTOR[fluidType] ?? 1.0;
  const coatingFactor = hasInternalCoating ? 0.85 : 1.0;
  const history = Array.isArray(input.thickness_history) ? input.thickness_history : [];

  const first = history[0] as { date?: string; thickness_mm?: number } | undefined;
  const prev = history[history.length - 2] as { date?: string; thickness_mm?: number } | undefined;
  const last = history[history.length - 1] as { date?: string; thickness_mm?: number } | undefined;

  const firstT = toNumber(first?.thickness_mm, 10.0);
  const prevT = toNumber(prev?.thickness_mm, 8.5);
  const currentT = toNumber(last?.thickness_mm, 7.2);

  const longYears = yearsBetween(parseDate(first?.date), parseDate(last?.date), 10);
  const shortYears = yearsBetween(parseDate(prev?.date), parseDate(last?.date), 5);

  const denominator = 2 * ((allowableStressMpa * weldEfficiency) + (pressure * yCoefficient));
  const tRequiredNoCa = denominator > 0 ? (pressure * odMm) / denominator : Number.POSITIVE_INFINITY;
  const tMin = round(tRequiredNoCa + ca, 2);

  const crLongRaw = ((firstT - currentT) / longYears) * serviceFactor * fluidFactor * coatingFactor;
  const crShortRaw = ((prevT - currentT) / shortYears) * serviceFactor * fluidFactor * coatingFactor;
  const crLong = round(crLongRaw, 3);
  const crShort = round(crShortRaw, 3);
  const crCandidate = Math.max(crLong, crShort);
  const crSelected = round(Math.max(crCandidate, 0.001), 3);
  const rl = round(Math.max((currentT - tMin) / crSelected, 0), 2);

  let inspectionInterval = Math.min(10, 0.5 * rl);
  if (crSelected > 2) inspectionInterval = Math.min(inspectionInterval, 1);
  else if (crSelected > 1) inspectionInterval = Math.min(inspectionInterval, 2);
  else if (crSelected > 0.5) inspectionInterval = Math.min(inspectionInterval, 3);
  inspectionInterval = rl < 1 ? 0.25 : round(Math.max(0.5, inspectionInterval), 2);

  const warnings: string[] = [];
  const redFlags: string[] = [];

  if (!hasCaInput) warnings.push("DATA.CORROSION_ALLOWANCE_DEFAULTED_1P5MM");
  if (!Object.prototype.hasOwnProperty.call(PIPING_NPS_TO_OD_MM, nps)) warnings.push("DATA.NPS_OD_INTERPOLATED");
  if (crCandidate < 0 && !hasInternalCoating) warnings.push("PHY.NEGATIVE_CORROSION_RATE_REVIEW");
  if (crSelected > 5) warnings.push("PHY.CORROSION_RATE_HIGH");
  if (rl > 50) warnings.push("PHY.REMAINING_LIFE_UNREALISTIC_HIGH");
  if (rl > 0 && rl < 2) warnings.push("PHY.REMAINING_LIFE_LOW_MONITORING_TIGHTEN");

  if (temperature > hardLimitC) {
    redFlags.push("PHY.TEMPERATURE_LIMIT_EXCEEDED");
  } else if (temperature > softLimitC) {
    warnings.push("STD.TEMPERATURE_OVERRIDE_REVIEW_REQUIRED");
  }
  if (chloridePpm !== null && chloridePpm > chlorideLimit) redFlags.push("STD.HYDROTEST_CHLORIDE_LIMIT_EXCEEDED");
  if (crSelected > 20) redFlags.push("PHY.CORROSION_RATE_UNREALISTIC");
  if (currentT <= tMin) redFlags.push("PHY.THICKNESS_BELOW_MINIMUM");
  if (rl < 1) redFlags.push("PHY.REMAINING_LIFE_CRITICAL");

  return {
    finalResults: {
      material,
      material_group: materialGroup,
      temperature_profile: profile,
      temperature_soft_limit_c: softLimitC,
      temperature_hard_limit_c: hardLimitC,
      temperature_limit_mode:
        temperature > hardLimitC
          ? "exceeded_hard_limit"
          : temperature > softLimitC
            ? "override_review_required"
            : "within_conservative_limit",
      allowable_stress_mpa: allowableStressMpa,
      weld_type: weldType,
      weld_efficiency: weldEfficiency,
      y_coefficient: yCoefficient,
      service_type: serviceType,
      fluid_type: fluidType,
      fluid_factor: fluidFactor,
      od_mm: round(odMm, 2),
      t_current_mm: round(currentT, 2),
      t_min_mm: tMin,
      cr_long_mm_per_year: crLong,
      cr_short_mm_per_year: crShort,
      cr_selected_mm_per_year: crSelected,
      remaining_life_years: rl,
      inspection_interval_years: inspectionInterval,
      chloride_ppm: chloridePpm,
      chloride_limit_ppm: chlorideLimit,
      hoop_stress_screening_mpa: round(currentT > 0 ? (pressure * odMm) / (2 * currentT) : 0, 4),
      hoop_stress_ratio: round(currentT > 0 && allowableStressMpa > 0 ? ((pressure * odMm) / (2 * currentT)) / allowableStressMpa : 0, 4),
      hydrotest_pressure_mpa: round(pressure * 1.5, 4),
      status: redFlags.length ? "CRITICAL" : warnings.length ? "WARNING" : "ACCEPTABLE",
    },
    warnings,
    redFlags,
  };
}
