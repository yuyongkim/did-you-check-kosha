import { CalculationResponse, Discipline, DisciplineConfig } from "@/lib/types";
import { DisciplineOutcome, round } from "@/lib/mock/shared";
import {
  PIPING_CONFIG,
  PIPING_DEFAULT_RESULTS,
  PIPING_STANDARD_REFS,
  buildPipingOutcome,
} from "@/lib/mock/piping";
import {
  VESSEL_CONFIG,
  VESSEL_DEFAULT_RESULTS,
  VESSEL_STANDARD_REFS,
  buildVesselOutcome,
} from "@/lib/mock/vessel";
import {
  ROTATING_CONFIG,
  ROTATING_DEFAULT_RESULTS,
  ROTATING_STANDARD_REFS,
  buildRotatingOutcome,
} from "@/lib/mock/rotating";
import {
  ELECTRICAL_CONFIG,
  ELECTRICAL_DEFAULT_RESULTS,
  ELECTRICAL_STANDARD_REFS,
  buildElectricalOutcome,
} from "@/lib/mock/electrical";
import {
  INSTRUMENTATION_CONFIG,
  INSTRUMENTATION_DEFAULT_RESULTS,
  INSTRUMENTATION_STANDARD_REFS,
  buildInstrumentationOutcome,
} from "@/lib/mock/instrumentation";
import {
  STEEL_CONFIG,
  STEEL_DEFAULT_RESULTS,
  STEEL_STANDARD_REFS,
  buildSteelOutcome,
} from "@/lib/mock/steel";
import {
  CIVIL_CONFIG,
  CIVIL_DEFAULT_RESULTS,
  CIVIL_STANDARD_REFS,
  buildCivilOutcome,
} from "@/lib/mock/civil";
import { buildCalculationStepTemplates } from "@/lib/mock/step-templates";

const DEFAULT_RESULTS: Record<Discipline, Record<string, unknown>> = {
  piping: PIPING_DEFAULT_RESULTS,
  vessel: VESSEL_DEFAULT_RESULTS,
  rotating: ROTATING_DEFAULT_RESULTS,
  electrical: ELECTRICAL_DEFAULT_RESULTS,
  instrumentation: INSTRUMENTATION_DEFAULT_RESULTS,
  steel: STEEL_DEFAULT_RESULTS,
  civil: CIVIL_DEFAULT_RESULTS,
};

const STANDARD_REFS: Record<Discipline, string[]> = {
  piping: PIPING_STANDARD_REFS,
  vessel: VESSEL_STANDARD_REFS,
  rotating: ROTATING_STANDARD_REFS,
  electrical: ELECTRICAL_STANDARD_REFS,
  instrumentation: INSTRUMENTATION_STANDARD_REFS,
  steel: STEEL_STANDARD_REFS,
  civil: CIVIL_STANDARD_REFS,
};

export const DISCIPLINE_CONFIGS: Record<Discipline, DisciplineConfig> = {
  piping: PIPING_CONFIG,
  vessel: VESSEL_CONFIG,
  rotating: ROTATING_CONFIG,
  electrical: ELECTRICAL_CONFIG,
  instrumentation: INSTRUMENTATION_CONFIG,
  steel: STEEL_CONFIG,
  civil: CIVIL_CONFIG,
};

const OUTCOME_BUILDERS: Record<Discipline, (input: Record<string, unknown>) => DisciplineOutcome> = {
  piping: buildPipingOutcome,
  vessel: buildVesselOutcome,
  rotating: buildRotatingOutcome,
  electrical: buildElectricalOutcome,
  instrumentation: buildInstrumentationOutcome,
  steel: buildSteelOutcome,
  civil: buildCivilOutcome,
};

function buildOutcome(discipline: Discipline, input: Record<string, unknown>): DisciplineOutcome {
  const builder = OUTCOME_BUILDERS[discipline];
  if (!builder) return { finalResults: DEFAULT_RESULTS[discipline], warnings: [], redFlags: [] };
  return builder(input);
}

export function isDiscipline(value: string): value is Discipline {
  return Object.prototype.hasOwnProperty.call(DISCIPLINE_CONFIGS, value);
}

export function getDisciplineConfig(discipline: Discipline): DisciplineConfig {
  return DISCIPLINE_CONFIGS[discipline];
}

export function buildMockCalculationResponse(discipline: Discipline, input: Record<string, unknown>): CalculationResponse {
  const outcome = buildOutcome(discipline, input);
  const redFlags = [...outcome.redFlags];
  const warnings = [...outcome.warnings];
  const forceBlocked = Boolean(input.force_blocked);

  if (forceBlocked) redFlags.push("LOG.NO_CONSENSUS_AFTER_TIEBREAKER");

  const blocked = redFlags.length > 0;
  const confidence = blocked ? "low" : warnings.length > 0 ? "medium" : "high";
  const status: CalculationResponse["status"] = blocked ? "blocked" : "success";
  const executionTime = round(0.2 + Math.random() * 0.7, 3);

  const layer1Issues =
    status === "blocked" && forceBlocked
      ? [{ code: "LOG.NO_CONSENSUS_AFTER_TIEBREAKER", severity: "high" as const, message: "Consensus did not converge in allotted retries" }]
      : [];
  const layer3Issues = [
    ...redFlags.map((code) => ({
      code,
      severity: "high" as const,
      message: "Critical safety condition detected. Release blocked.",
    })),
    ...warnings.map((code) => ({
      code,
      severity: "medium" as const,
      message: "Conservative warning triggered. Review recommended.",
    })),
  ];

  const layerResults = [
    { layer: "Layer 1: Input Validation", passed: layer1Issues.length === 0, issues: layer1Issues, details: { normalized_units: true } },
    {
      layer: "Layer 2: MAKER Consensus",
      passed: !forceBlocked,
      issues: forceBlocked
        ? [{ code: "LOG.NO_CONSENSUS_AFTER_TIEBREAKER", severity: "high" as const, message: "Consensus below threshold" }]
        : [],
      details: { agreement: forceBlocked ? "1/3" : "3/3", deviation_percent: forceBlocked ? 2.8 : 0.6 },
    },
    {
      layer: "Layer 3: Physics and Standards",
      passed: layer3Issues.length === 0,
      issues: layer3Issues,
      details: { guardrails_checked: true },
    },
    {
      layer: "Layer 4: Reverse Verification",
      passed: true,
      issues: [],
      details: { reverse_deviation_percent: round(Math.max(0.5, Math.random() * 2.4), 2) },
    },
  ];

  const stepTemplates = buildCalculationStepTemplates(discipline, STANDARD_REFS[discipline]);
  const calculationSteps = stepTemplates.map((step, index) => ({
    step_number: index + 1,
    description: step.description,
    formula_used: step.formula_used,
    standard_reference: step.standard_reference,
    result: { evidence: "validated" },
  }));

  const recommendations = blocked
    ? [
        {
          priority: "high" as const,
          action: "escalate_human_review",
          timeline: "immediate" as const,
          description: "Blocking red flag detected. Human review required before release.",
        },
      ]
    : [
        {
          priority: warnings.length > 0 ? ("medium" as const) : ("low" as const),
          action: warnings.length > 0 ? "increase_monitoring" : "continue_monitoring",
          timeline: warnings.length > 0 ? ("1month" as const) : ("nextyear" as const),
          description:
            warnings.length > 0
              ? "Warnings detected. Tighten inspection and monitoring cadence."
              : "No blocking issue detected. Continue normal monitoring.",
        },
      ];

  return {
    status,
    discipline,
    results: outcome.finalResults,
    details: {
      calculation_summary: {
        discipline,
        calculation_type: `${discipline}_integrity`,
        standards_applied: STANDARD_REFS[discipline],
        confidence,
        execution_time_sec: executionTime,
      },
      input_data: input,
      calculation_steps: calculationSteps,
      layer_results: layerResults,
      final_results: outcome.finalResults,
      recommendations,
      flags: {
        red_flags: redFlags,
        warnings,
      },
    },
    references: STANDARD_REFS[discipline],
    verification: {
      layers: layerResults,
      confidence,
    },
    flags: {
      red_flags: redFlags,
      warnings,
    },
  };
}
