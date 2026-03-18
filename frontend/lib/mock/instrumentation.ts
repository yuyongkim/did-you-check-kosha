import { DisciplineConfig } from "@/lib/types";
import { DisciplineOutcome, linearRegression, pfdToSil, round, toNumber } from "@/lib/mock/shared";

export const INSTRUMENTATION_STANDARD_REFS = [
  "IEC 61511",
  "ISA-TR84.00.02",
  "ISO GUM",
];

export const INSTRUMENTATION_DEFAULT_RESULTS: Record<string, unknown> = {
  pfdavg: 0.00044,
  sil_target: 2,
  sil_achieved: 3,
  predicted_drift_pct: 0.38,
  calibration_interval_optimal_days: 220,
  status: "ACCEPTABLE",
  proof_test_adequacy: "ADEQUATE",
  calibration_health: "HEALTHY",
};

const INSTRUMENTATION_SIL_TARGET_PFD_LIMIT: Record<number, number> = {
  1: 1e-2,
  2: 1e-3,
  3: 1e-4,
  4: 1e-5,
};

const INSTRUMENTATION_ARCHITECTURE_PFD_FACTOR: Record<string, number> = {
  "1oo1": 1.0,
  "1oo2": 0.45,
  "2oo2": 0.55,
  "2oo3": 0.3,
};

const INSTRUMENTATION_TYPE_DRIFT_FACTOR: Record<string, number> = {
  pressure_transmitter: 1.0,
  temperature_transmitter: 0.9,
  flow_meter: 1.15,
  level_transmitter: 1.05,
  control_valve_positioner: 1.2,
  analyzer: 1.25,
  vibration_probe: 1.1,
  pressure_switch: 0.95,
  thermocouple: 1.08,
  radar_level: 0.98,
  coriolis_meter: 1.04,
};

function silTargetLimit(target: number): number {
  return INSTRUMENTATION_SIL_TARGET_PFD_LIMIT[target] ?? 1e-1;
}

export const INSTRUMENTATION_CONFIG: DisciplineConfig = {
  discipline: "instrumentation",
  title: "Instrumentation and SIS",
  subtitle: "IEC 61511 and ISO GUM drift, SIL, and uncertainty validation",
  shortLabel: "INS",
  formFields: [
    {
      name: "instrument_type",
      label: "Instrument Type",
      type: "select",
      options: [
        { label: "Pressure Transmitter", value: "pressure_transmitter" },
        { label: "Temperature Transmitter", value: "temperature_transmitter" },
        { label: "Flow Meter", value: "flow_meter" },
        { label: "Level Transmitter", value: "level_transmitter" },
        { label: "Control Valve Positioner", value: "control_valve_positioner" },
        { label: "Analyzer", value: "analyzer" },
        { label: "Vibration Probe", value: "vibration_probe" },
        { label: "Pressure Switch", value: "pressure_switch" },
        { label: "Thermocouple", value: "thermocouple" },
        { label: "Radar Level", value: "radar_level" },
        { label: "Coriolis Meter", value: "coriolis_meter" },
      ],
    },
    {
      name: "voting_architecture",
      label: "SIF Architecture",
      type: "select",
      options: [
        { label: "1oo1", value: "1oo1" },
        { label: "1oo2", value: "1oo2" },
        { label: "2oo2", value: "2oo2" },
        { label: "2oo3", value: "2oo3" },
      ],
    },
    { name: "sil_target", label: "SIL Target", unit: "level", type: "number", min: 1, max: 4, step: 1 },
    { name: "failure_rate_per_hour", label: "Failure Rate", unit: "/h", type: "number", min: 0, max: 0.0001, step: 0.0000001 },
    { name: "proof_test_interval_hours", label: "Proof Test Interval", unit: "h", type: "number", min: 24, max: 30000, step: 1 },
    { name: "mttr_hours", label: "MTTR", unit: "h", type: "number", min: 0.1, max: 240, step: 0.1 },
    { name: "calibration_interval_days", label: "Current Calibration Interval", unit: "days", type: "number", min: 7, max: 3650, step: 1 },
    { name: "tolerance_pct", label: "Tolerance", unit: "%", type: "number", min: 0.1, max: 10, step: 0.1 },
    { name: "sensor_mtbf_years", label: "Sensor MTBF", unit: "years", type: "number", min: 0.5, max: 25, step: 0.1 },
    { name: "cv_required", label: "Required Cv", type: "number", min: 1, max: 500, step: 0.1 },
    { name: "cv_rated", label: "Rated Cv", type: "number", min: 1, max: 500, step: 0.1 },
  ],
  sampleInput: {
    instrument_type: "pressure_transmitter",
    voting_architecture: "1oo1",
    sil_target: 2,
    failure_rate_per_hour: 1.0e-7,
    proof_test_interval_hours: 8760,
    mttr_hours: 8,
    calibration_interval_days: 180,
    calibration_history: [
      { days_since_ref: 0, error_pct: 0.05 },
      { days_since_ref: 90, error_pct: 0.16 },
      { days_since_ref: 180, error_pct: 0.28 },
      { days_since_ref: 270, error_pct: 0.39 },
    ],
    tolerance_pct: 1,
    sensor_mtbf_years: 8,
    cv_required: 45,
    cv_rated: 80,
    uncertainty_components_pct: [0.2, 0.3, 0.1],
  },
  presets: [
    {
      id: "ins-pressure-normal",
      label: "PT Normal",
      description: "Pressure transmitter with stable drift and SIL margin.",
      values: {
        instrument_type: "pressure_transmitter",
        voting_architecture: "1oo1",
        sil_target: 2,
        calibration_interval_days: 180,
        tolerance_pct: 1,
      },
    },
    {
      id: "ins-sis-tight",
      label: "SIS Tight",
      description: "Tight safety target and shorter proof test interval.",
      values: {
        instrument_type: "pressure_switch",
        voting_architecture: "2oo3",
        sil_target: 3,
        failure_rate_per_hour: 2.2e-7,
        proof_test_interval_hours: 4380,
      },
    },
    {
      id: "ins-flow-drift",
      label: "Flow Drift",
      description: "Flow-meter drift-focused scenario for interval optimization.",
      values: {
        instrument_type: "flow_meter",
        calibration_interval_days: 270,
        tolerance_pct: 0.8,
        sensor_mtbf_years: 4.2,
      },
    },
    {
      id: "ins-valve-cv",
      label: "Valve Cv Margin",
      description: "Control valve sizing margin review case.",
      values: {
        instrument_type: "control_valve_positioner",
        cv_required: 78,
        cv_rated: 80,
      },
    },
  ],
  defaultChart: "trend",
  primaryMetrics: ["pfdavg", "sil_target", "sil_achieved", "predicted_drift_pct", "calibration_interval_optimal_days", "proof_test_adequacy", "calibration_health"],
};

export function buildInstrumentationOutcome(input: Record<string, unknown>): DisciplineOutcome {
  const instrumentType = String(input.instrument_type ?? "pressure_transmitter").toLowerCase();
  const architecture = String(input.voting_architecture ?? "1oo1").toLowerCase();
  const silTarget = toNumber(input.sil_target, 2);
  const failureRate = Math.max(toNumber(input.failure_rate_per_hour, 1.0e-7), 1.0e-12);
  const proofHours = Math.max(toNumber(input.proof_test_interval_hours, 8760), 1);
  const mttr = Math.max(toNumber(input.mttr_hours, 8), 0.1);
  const tolerance = toNumber(input.tolerance_pct, 1);
  const calIntervalDays = Math.max(toNumber(input.calibration_interval_days, 180), 1);
  const sensorMtbfYears = toNumber(input.sensor_mtbf_years, 8);
  const cvRequired = Math.max(toNumber(input.cv_required, 45), 1e-12);
  const cvRated = Math.max(toNumber(input.cv_rated, 80), 1e-12);
  const uncertaintyComponents = Array.isArray(input.uncertainty_components_pct)
    ? input.uncertainty_components_pct.map((value) => Math.abs(toNumber(value, 0)))
    : [0.2, 0.3, 0.1];
  const history = Array.isArray(input.calibration_history) ? input.calibration_history : [];

  const architectureFactor = INSTRUMENTATION_ARCHITECTURE_PFD_FACTOR[architecture] ?? 1.0;
  const instrumentDriftFactor = INSTRUMENTATION_TYPE_DRIFT_FACTOR[instrumentType] ?? 1.0;
  const pfdavg = round(((failureRate * (proofHours + mttr)) / 2) * architectureFactor, 6);
  const silAchieved = pfdToSil(pfdavg);
  const regressionData = history.map((row) => ({
    x: toNumber((row as { days_since_ref?: number }).days_since_ref, 0),
    y: toNumber((row as { error_pct?: number }).error_pct, 0),
  }));
  const { slope, intercept, r2 } = linearRegression(regressionData);
  const adjustedSlope = slope * instrumentDriftFactor;
  const predictedDriftRaw = Math.max((adjustedSlope * calIntervalDays) + intercept, 0);
  const predictedDrift = round(predictedDriftRaw, 3);

  let optimalInterval = 180;
  if (adjustedSlope > 0) {
    optimalInterval = (tolerance - intercept) / adjustedSlope;
  }
  if (!Number.isFinite(optimalInterval) || optimalInterval <= 0) {
    optimalInterval = calIntervalDays;
  }
  if (r2 <= 0.8) optimalInterval *= 0.8;
  optimalInterval = round(Math.max(30, Math.min(3650, optimalInterval)), 0);

  const combinedUncertainty = round(Math.sqrt(uncertaintyComponents.reduce((acc, value) => acc + (value ** 2), 0)), 3);
  const cvMarginRatio = round(cvRequired / cvRated, 3);

  const warnings: string[] = [];
  const redFlags: string[] = [];

  if (predictedDrift > tolerance) warnings.push("PHY.INSTRUMENT_DRIFT_ABOVE_TOLERANCE");
  if (r2 < 0.3) warnings.push("LOG.DRIFT_MODEL_LOW_CONFIDENCE");
  if (sensorMtbfYears < 5) warnings.push("PHY.SENSOR_MTBF_LOW");
  if (cvMarginRatio > 0.9) warnings.push("PHY.CONTROL_VALVE_CAPACITY_LOW");
  if (pfdavg > silTargetLimit(silTarget)) redFlags.push("STD.SIL_TARGET_NOT_MET");
  if (predictedDrift > (2 * tolerance)) redFlags.push("PHY.DRIFT_RATE_EXCEEDED");
  if (cvMarginRatio > 1.0) redFlags.push("PHY.CONTROL_VALVE_CAPACITY_INSUFFICIENT");

  return {
    finalResults: {
      instrument_type: instrumentType,
      voting_architecture: architecture,
      pfdavg,
      sil_target: silTarget,
      sil_achieved: silAchieved,
      drift_rate_pct_per_day: round(adjustedSlope, 6),
      drift_intercept_pct: round(intercept, 3),
      drift_r_squared: round(r2, 3),
      predicted_drift_pct: predictedDrift,
      calibration_interval_optimal_days: optimalInterval,
      calibration_interval_current_days: round(calIntervalDays, 0),
      combined_uncertainty_pct: combinedUncertainty,
      cv_required: round(cvRequired, 2),
      cv_rated: round(cvRated, 2),
      cv_margin_ratio: cvMarginRatio,
      inspection_interval_days: Math.min(optimalInterval, round(calIntervalDays, 0)),
      proof_test_adequacy: (() => {
        const limit = silTargetLimit(silTarget);
        const ratio = pfdavg / Math.max(limit, 1e-15);
        return ratio > 1 ? "INADEQUATE" : ratio > 0.7 ? "MARGINAL" : "ADEQUATE";
      })(),
      calibration_health: (() => {
        if (tolerance <= 0) return "UNKNOWN";
        const ratio = predictedDrift / tolerance;
        return ratio > 1 ? "EXCEEDED" : ratio > 0.7 ? "AT_RISK" : ratio > 0.5 ? "WATCH" : "HEALTHY";
      })(),
      status: redFlags.length ? "CRITICAL" : warnings.length ? "WARNING" : "ACCEPTABLE",
    },
    warnings,
    redFlags,
  };
}
