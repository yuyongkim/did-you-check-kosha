import { FormFieldOptionGroup } from "@/lib/types";

export const PIPING_STANDARD_REFS = [
  "ASME B31.3 Para 304.1.2",
  "ASME B31.3 Table A-1",
  "ASME B31.3 weld joint efficiency guidance",
  "ASME B31.1/API 579 managed high-temperature review context",
  "API 570 Section 7.5",
  "API 570 hydrotest water quality guidance",
];

export const PIPING_DEFAULT_RESULTS: Record<string, unknown> = {
  t_min_mm: 5.1,
  cr_long_mm_per_year: 0.24,
  cr_short_mm_per_year: 0.31,
  cr_selected_mm_per_year: 0.31,
  remaining_life_years: 6.8,
  inspection_interval_years: 3,
  status: "ACCEPTABLE",
  hoop_stress_screening_mpa: 51.89,
  hoop_stress_ratio: 0.376,
  hydrotest_pressure_mpa: 6.75,
};

export type PipingMaterialGroup =
  | "carbon_steel"
  | "low_alloy_steel"
  | "stainless_steel"
  | "duplex_stainless"
  | "nickel_alloy";

export type PipingTemperatureProfile = "strict_process" | "high_temp_managed" | "legacy_power_steam";

const CS_MATERIALS = [
  "SA-106 Gr.B",
  "A106 Gr.B",
  "SA-53 Gr.B",
  "SA-333 Gr.6",
  "A105",
  "A234 WPB",
  "API 5L Gr.B",
] as const;

const LOW_ALLOY_MATERIALS = [
  "SA-335 P11",
  "SA-335 P22",
  "SA-335 P5",
  "SA-335 P9",
  "SA-335 P91",
] as const;

const SUS_MATERIALS = [
  "SA-312 TP304",
  "SA-312 TP304L",
  "SA-312 TP316",
  "SA-312 TP316L",
  "SA-312 TP321",
  "SA-312 TP347",
] as const;

const DUPLEX_MATERIALS = [
  "SA-790 S31803",
  "SA-790 S32205",
  "SA-790 S32750",
] as const;

const NICKEL_MATERIALS = [
  "Alloy 825 (N08825)",
  "Alloy 625 (N06625)",
  "Monel 400 (N04400)",
] as const;

export const PIPING_MATERIAL_OPTION_GROUPS: FormFieldOptionGroup[] = [
  {
    label: "Carbon Steel (CS)",
    options: CS_MATERIALS.map((material) => ({ label: material, value: material })),
  },
  {
    label: "Low Alloy Steel",
    options: LOW_ALLOY_MATERIALS.map((material) => ({ label: material, value: material })),
  },
  {
    label: "Stainless Steel (SUS)",
    options: SUS_MATERIALS.map((material) => ({ label: material, value: material })),
  },
  {
    label: "Duplex Stainless",
    options: DUPLEX_MATERIALS.map((material) => ({ label: material, value: material })),
  },
  {
    label: "Nickel Alloy",
    options: NICKEL_MATERIALS.map((material) => ({ label: material, value: material })),
  },
];

const STRESS_PROFILES_MPA: Record<string, Record<number, number>> = {
  cs_main: { 20: 138, 100: 138, 200: 124, 250: 110, 300: 103, 350: 97, 400: 90 },
  cs_secondary: { 20: 131, 100: 131, 200: 117, 250: 103, 300: 97, 350: 90, 400: 83 },
  low_alloy_p11: { 20: 138, 100: 138, 200: 132, 250: 127, 300: 123, 350: 118, 400: 114, 500: 103, 550: 96 },
  low_alloy_p22: { 20: 138, 100: 138, 200: 134, 250: 130, 300: 126, 350: 122, 400: 118, 500: 108, 550: 101 },
  low_alloy_p5: { 20: 138, 100: 138, 200: 133, 250: 128, 300: 124, 350: 120, 400: 116, 500: 106, 550: 98 },
  low_alloy_p9: { 20: 138, 100: 138, 200: 134, 250: 130, 300: 126, 350: 122, 400: 119, 500: 112, 550: 105 },
  low_alloy_p91: { 20: 170, 100: 167, 200: 160, 250: 156, 300: 152, 350: 148, 400: 145, 500: 136, 550: 128, 600: 121 },
  ss_304: { 20: 138, 100: 131, 200: 124, 250: 117, 300: 110, 350: 103, 400: 97, 500: 83, 550: 76 },
  ss_316: { 20: 138, 100: 131, 200: 124, 250: 117, 300: 110, 350: 103, 400: 97, 500: 83, 550: 76 },
  ss_321: { 20: 138, 100: 131, 200: 125, 250: 119, 300: 113, 350: 107, 400: 101, 500: 90, 550: 83 },
  ss_347: { 20: 138, 100: 131, 200: 126, 250: 120, 300: 114, 350: 108, 400: 102, 500: 92, 550: 85 },
  duplex_2205: { 20: 170, 100: 166, 200: 160, 250: 154, 300: 148, 350: 142, 400: 136, 450: 130 },
  duplex_2507: { 20: 190, 100: 186, 200: 178, 250: 171, 300: 165, 350: 159, 400: 152, 450: 145 },
  ni_825: { 20: 155, 100: 150, 200: 145, 250: 141, 300: 137, 350: 133, 400: 129, 500: 118, 550: 110 },
  ni_625: { 20: 170, 100: 165, 200: 160, 250: 156, 300: 152, 350: 148, 400: 145, 500: 136, 550: 128, 600: 120 },
  ni_monel_400: { 20: 145, 100: 140, 200: 134, 250: 130, 300: 126, 350: 121, 400: 116, 500: 106, 550: 98 },
};

const MATERIAL_TO_STRESS_PROFILE: Record<string, keyof typeof STRESS_PROFILES_MPA> = {
  "SA-106 Gr.B": "cs_main",
  "A106 Gr.B": "cs_main",
  "SA-53 Gr.B": "cs_secondary",
  "SA-333 Gr.6": "cs_main",
  A105: "cs_main",
  "A234 WPB": "cs_secondary",
  "API 5L Gr.B": "cs_main",
  "SA-335 P11": "low_alloy_p11",
  "SA-335 P22": "low_alloy_p22",
  "SA-335 P5": "low_alloy_p5",
  "SA-335 P9": "low_alloy_p9",
  "SA-335 P91": "low_alloy_p91",
  "SA-312 TP304": "ss_304",
  "SA-312 TP304L": "ss_304",
  "SA-312 TP316": "ss_316",
  "SA-312 TP316L": "ss_316",
  "SA-312 TP321": "ss_321",
  "SA-312 TP347": "ss_347",
  "SA-790 S31803": "duplex_2205",
  "SA-790 S32205": "duplex_2205",
  "SA-790 S32750": "duplex_2507",
  "Alloy 825 (N08825)": "ni_825",
  "Alloy 625 (N06625)": "ni_625",
  "Monel 400 (N04400)": "ni_monel_400",
};

function buildTableByMaterial(): Record<string, Record<number, number>> {
  const table: Record<string, Record<number, number>> = {};
  for (const [material, profile] of Object.entries(MATERIAL_TO_STRESS_PROFILE)) {
    table[material] = { ...STRESS_PROFILES_MPA[profile] };
  }
  return table;
}

function assignGroup<T extends readonly string[]>(
  acc: Record<string, PipingMaterialGroup>,
  materials: T,
  group: PipingMaterialGroup,
) {
  materials.forEach((material) => {
    acc[material] = group;
  });
}

function buildMaterialGroupMap(): Record<string, PipingMaterialGroup> {
  const map: Record<string, PipingMaterialGroup> = {};
  assignGroup(map, CS_MATERIALS, "carbon_steel");
  assignGroup(map, LOW_ALLOY_MATERIALS, "low_alloy_steel");
  assignGroup(map, SUS_MATERIALS, "stainless_steel");
  assignGroup(map, DUPLEX_MATERIALS, "duplex_stainless");
  assignGroup(map, NICKEL_MATERIALS, "nickel_alloy");
  return map;
}

const MATERIAL_GROUP_TEMP_LIMIT_C: Record<PipingMaterialGroup, number> = {
  carbon_steel: 425,
  low_alloy_steel: 593,
  stainless_steel: 538,
  duplex_stainless: 315,
  nickel_alloy: 650,
};

const PIPING_PROFILE_LIMITS_C: Record<PipingTemperatureProfile, Record<PipingMaterialGroup, { soft: number; hard: number }>> = {
  strict_process: {
    carbon_steel: { soft: 425, hard: 425 },
    low_alloy_steel: { soft: 593, hard: 593 },
    stainless_steel: { soft: 538, hard: 538 },
    duplex_stainless: { soft: 315, hard: 315 },
    nickel_alloy: { soft: 650, hard: 650 },
  },
  high_temp_managed: {
    carbon_steel: { soft: 425, hard: 500 },
    low_alloy_steel: { soft: 593, hard: 620 },
    stainless_steel: { soft: 538, hard: 600 },
    duplex_stainless: { soft: 315, hard: 350 },
    nickel_alloy: { soft: 650, hard: 700 },
  },
  legacy_power_steam: {
    carbon_steel: { soft: 425, hard: 540 },
    low_alloy_steel: { soft: 593, hard: 650 },
    stainless_steel: { soft: 538, hard: 620 },
    duplex_stainless: { soft: 315, hard: 360 },
    nickel_alloy: { soft: 650, hard: 720 },
  },
};

export const PIPING_ALLOWABLE_STRESS_TABLE_MPA = buildTableByMaterial();
export const PIPING_MATERIAL_GROUP = buildMaterialGroupMap();
export const PIPING_MATERIAL_TEMP_LIMIT_C: Record<string, number> = Object.fromEntries(
  Object.entries(PIPING_MATERIAL_GROUP).map(([material, group]) => [material, MATERIAL_GROUP_TEMP_LIMIT_C[group]]),
);

export const PIPING_TEMPERATURE_PROFILE_OPTIONS = [
  { label: "Strict Process (Conservative)", value: "strict_process" },
  { label: "High Temp Managed (Review Required)", value: "high_temp_managed" },
  { label: "Legacy Power/Steam Managed", value: "legacy_power_steam" },
];

export function getPipingTemperatureWindowC(
  materialGroup: PipingMaterialGroup,
  rawProfile: string,
): { softLimitC: number; hardLimitC: number; profile: PipingTemperatureProfile } {
  const profile = (Object.prototype.hasOwnProperty.call(PIPING_PROFILE_LIMITS_C, rawProfile)
    ? rawProfile
    : "strict_process") as PipingTemperatureProfile;
  const limits = PIPING_PROFILE_LIMITS_C[profile][materialGroup];
  return {
    softLimitC: limits.soft,
    hardLimitC: limits.hard,
    profile,
  };
}

export const PIPING_WELD_EFFICIENCY: Record<string, number> = {
  seamless: 1.0,
  erw: 0.85,
  smaw: 0.85,
  spot_rt: 0.85,
  no_rt: 0.8,
};

export const PIPING_NPS_TO_OD_MM: Record<number, number> = {
  1: 33.4,
  2: 60.3,
  3: 88.9,
  4: 114.3,
  6: 168.3,
  8: 219.1,
  10: 273.1,
  12: 323.9,
  14: 355.6,
  16: 406.4,
  18: 457.2,
  20: 508.0,
  24: 609.6,
  30: 762.0,
  36: 914.4,
  42: 1066.8,
  48: 1219.2,
};

export const PIPING_HYDROTEST_CHLORIDE_LIMIT_PPM: Record<PipingMaterialGroup, number> = {
  carbon_steel: 250,
  low_alloy_steel: 250,
  stainless_steel: 30,
  duplex_stainless: 30,
  nickel_alloy: 50,
};

export const PIPING_SERVICE_CORROSION_FACTOR: Record<string, number> = {
  general: 1.0,
  sour: 1.35,
  chloride: 1.2,
  high_temp: 1.25,
};

export const PIPING_FLUID_OPTIONS = [
  { label: "Dry Hydrocarbon", value: "hydrocarbon_dry" },
  { label: "Wet Hydrocarbon", value: "hydrocarbon_wet" },
  { label: "Steam / Condensate", value: "steam_condensate" },
  { label: "Superheated Steam", value: "steam_superheated" },
  { label: "Wet Steam", value: "steam_wet" },
  { label: "Amine Service", value: "amine" },
  { label: "H2S Sour Service", value: "h2s_sour" },
  { label: "Chloride Aqueous", value: "chloride_aqueous" },
  { label: "Caustic Service", value: "caustic" },
  { label: "Seawater", value: "seawater" },
  { label: "Oxygen-rich Service", value: "oxygen_rich" },
];

export const PIPING_FLUID_CORROSION_FACTOR: Record<string, number> = {
  hydrocarbon_dry: 0.95,
  hydrocarbon_wet: 1.1,
  steam_condensate: 1.15,
  steam_superheated: 1.05,
  steam_wet: 1.25,
  amine: 1.25,
  h2s_sour: 1.35,
  chloride_aqueous: 1.4,
  caustic: 1.2,
  seawater: 1.45,
  oxygen_rich: 1.1,
};

export const PIPING_Y_COEFFICIENT = 0.4;
