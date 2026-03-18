import { Discipline } from "@/lib/types";

interface StepTemplate {
  description: string;
  formula: string;
}

const STEP_TEMPLATES: Record<Discipline, StepTemplate[]> = {
  piping: [
    {
      description: "Required thickness without corrosion allowance",
      formula: "t_req = (P * D) / (2 * (S * E + P * Y))",
    },
    {
      description: "Minimum required thickness with corrosion allowance",
      formula: "t_min = t_req + CA",
    },
    {
      description: "Long-term corrosion rate",
      formula: "CR_long = (t_first - t_current) / years_long * F_service * F_fluid * F_coating",
    },
    {
      description: "Short-term corrosion rate and conservative selection",
      formula: "CR_selected = max(CR_long, CR_short)",
    },
    {
      description: "Remaining life and inspection interval",
      formula: "RL = (t_current - t_min) / CR_selected; interval = min(code_limit, 0.5 * RL)",
    },
  ],
  vessel: [
    {
      description: "Allowable stress lookup at design temperature",
      formula: "S = lookup(material, T)",
    },
    {
      description: "Required shell thickness",
      formula: "t_required = (P * R) / (S * E - 0.6 * P) + CA",
    },
    {
      description: "Thickness margin and remaining life",
      formula: "margin = t_current - t_required; RL = margin / CR",
    },
  ],
  rotating: [
    {
      description: "Adjusted vibration limit by machine + driver + criticality + train/bearing combination",
      formula: "adjusted_vibration_limit_mm_per_s = vibration_limit_mm_per_s * driver_factor * criticality_factor * stage_vibration_factor * train_vibration_factor * casing_vibration_factor * bearing_vibration_factor",
    },
    {
      description: "Mechanical integrity index scoring",
      formula: "mechanical_integrity_index = 10 - penalty(vibration_mm_per_s, nozzle_load_ratio, bearing_temperature_c, lube_oil_supply_temp_c, axial_displacement_um, coupling_misalignment_mils)",
    },
    {
      description: "Protection readiness index (API 670 coverage and trip discipline)",
      formula: "protection_readiness_index = 10 - penalty(api670_coverage_pct, trip_tests_last_12m, protection_bypass_active)",
    },
    {
      description: "Process stability risk (compressor/pump/steam branches)",
      formula: "process_stability_index = 10 - (risk(pressure_ratio, surge_events_30d, npsh_margin_m, steam_quality_x, phase_change_risk_index) * seal_process_factor * lube_process_factor)",
    },
    {
      description: "Inspection interval rule",
      formula: "inspection_interval_years = rule(mechanical_integrity_index, process_stability_index, protection_readiness_index, service_criticality, flags)",
    },
  ],
  electrical: [
    {
      description: "Arc flash incident energy screening",
      formula: "E_arc = K * I_fault * (t_clear/0.2) * (610/d)^x",
    },
    {
      description: "Transformer health index",
      formula: "HI = sum(weight_i * score_i)",
    },
    {
      description: "Protection margin checks",
      formula: "pass if I_fault <= breaker_rating and THD/voltage-drop within limits",
    },
  ],
  instrumentation: [
    {
      description: "PFDavg calculation",
      formula: "PFDavg = ((lambda * (TI + MTTR)) / 2) * architecture_factor",
    },
    {
      description: "Drift trend fit",
      formula: "drift(t) = slope * t + intercept",
    },
    {
      description: "Optimal calibration interval",
      formula: "T_opt = (tolerance - intercept) / slope (with confidence adjustment)",
    },
  ],
  steel: [
    {
      description: "Slenderness and compression stress",
      formula: "lambda_c = (K*L/(r*pi))*sqrt(Fy/E), Fcr = code(lambda_c)",
    },
    {
      description: "Design strength",
      formula: "phiPn = 0.9 * Fcr * A_reduced",
    },
    {
      description: "Demand-capacity check",
      formula: "D/C = P_u / phiPn",
    },
  ],
  civil: [
    {
      description: "Flexural design strength",
      formula: "a = As*Fy/(0.85*f'c*b), phiMn = 0.9*As*Fy*(d-a/2)",
    },
    {
      description: "Demand-capacity check",
      formula: "D/C = M_u / phiMn",
    },
    {
      description: "Carbonation and corrosion-initiation screening",
      formula: "Xc = k*sqrt(t), corrosion_init if Xc >= cover",
    },
  ],
};

export function buildCalculationStepTemplates(
  discipline: Discipline,
  references: string[],
): Array<{ description: string; formula_used: string; standard_reference: string }> {
  const templates = STEP_TEMPLATES[discipline] ?? [];
  if (templates.length === 0) {
    return references.map((reference) => ({
      description: "Standards-backed calculation step",
      formula_used: "[TODO: backend formula log]",
      standard_reference: reference,
    }));
  }

  return templates.map((template, index) => ({
    description: template.description,
    formula_used: template.formula,
    standard_reference: references[index] ?? references[references.length - 1] ?? "N/A",
  }));
}
