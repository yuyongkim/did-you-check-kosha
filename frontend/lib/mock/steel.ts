import { DisciplineConfig } from "@/lib/types";
import { DisciplineOutcome, round, toNumber } from "@/lib/mock/shared";

export const STEEL_STANDARD_REFS = [
  "AISC 360 Chapter E",
  "AISC serviceability deflection guidance",
];

export const STEEL_DEFAULT_RESULTS: Record<string, unknown> = {
  dc_ratio: 0.82,
  corrosion_loss_percent: 8,
  deflection_ratio: 0.45,
  inspection_interval_years: 2,
  status: "ACCEPTABLE",
  reinforcement_need: "NO_ACTION",
  connection_status: "ACCEPTABLE",
};

const STEEL_GRADE_DEFAULT_FY: Record<string, number> = {
  a36: 250,
  a572_gr50: 345,
  a992: 345,
  a500_grb: 317,
  a500_grc: 345,
  a588: 345,
  a913_gr65: 450,
  api_2w_gr50: 345,
};

export const STEEL_CONFIG: DisciplineConfig = {
  discipline: "steel",
  title: "Steel Structure Integrity",
  subtitle: "AISC-based D/C, section-loss, and serviceability screening",
  shortLabel: "STL",
  formFields: [
    {
      name: "member_type",
      label: "Member Type",
      type: "select",
      options: [
        { label: "Column", value: "column" },
        { label: "Beam", value: "beam" },
        { label: "Brace", value: "brace" },
        { label: "Girder", value: "girder" },
        { label: "Truss Member", value: "truss_member" },
        { label: "Pipe Rack Leg", value: "pipe_rack_leg" },
        { label: "Portal Frame", value: "portal_frame" },
      ],
    },
    {
      name: "steel_grade",
      label: "Steel Grade",
      type: "select",
      options: [
        { label: "ASTM A36", value: "a36" },
        { label: "ASTM A572 Gr50", value: "a572_gr50" },
        { label: "ASTM A992", value: "a992" },
        { label: "ASTM A500 GrB", value: "a500_grb" },
        { label: "ASTM A500 GrC", value: "a500_grc" },
        { label: "ASTM A588", value: "a588" },
        { label: "ASTM A913 Gr65", value: "a913_gr65" },
        { label: "API 2W Gr50", value: "api_2w_gr50" },
      ],
    },
    { name: "section_label", label: "Section Label", type: "text" },
    { name: "length_m", label: "Member Length", unit: "m", type: "number", min: 0.5, max: 30, step: 0.1 },
    { name: "k_factor", label: "K Factor", type: "number", min: 0.5, max: 3, step: 0.01 },
    { name: "radius_of_gyration_mm", label: "Radius of Gyration r", unit: "mm", type: "number", min: 10, max: 300, step: 0.1 },
    { name: "yield_strength_mpa", label: "Fy", unit: "MPa", type: "number", min: 150, max: 700, step: 1 },
    { name: "gross_area_mm2", label: "Gross Area Ag", unit: "mm2", type: "number", min: 100, max: 100000, step: 1 },
    { name: "axial_demand_kn", label: "Axial Demand", unit: "kN", type: "number", min: 0, max: 5000, step: 1 },
    { name: "corrosion_loss_percent", label: "Corrosion Loss", unit: "%", type: "number", min: 0, max: 95, step: 0.1 },
    { name: "deflection_mm", label: "Deflection", unit: "mm", type: "number", min: 0, max: 500, step: 0.1 },
    { name: "span_mm", label: "Span", unit: "mm", type: "number", min: 100, max: 50000, step: 1 },
    {
      name: "connection_failure_detected",
      label: "Connection Failure",
      type: "checkbox",
      helper: "Mark if any bolt/weld connection failure is observed.",
    },
  ],
  sampleInput: {
    member_type: "column",
    steel_grade: "a572_gr50",
    section_label: "W310x60",
    length_m: 6.0,
    k_factor: 1.0,
    radius_of_gyration_mm: 90.0,
    yield_strength_mpa: 345.0,
    elasticity_mpa: 200000,
    gross_area_mm2: 7600,
    corrosion_loss_percent: 8,
    axial_demand_kn: 650,
    moment_demand_knm: 90,
    deflection_mm: 10,
    span_mm: 6000,
    connection_failure_detected: false,
  },
  presets: [
    {
      id: "stl-column-normal",
      label: "Column Normal",
      description: "Standard column case with moderate corrosion and low utilization.",
      values: {
        member_type: "column",
        steel_grade: "a572_gr50",
        axial_demand_kn: 650,
        corrosion_loss_percent: 8,
      },
    },
    {
      id: "stl-pipe-rack",
      label: "Pipe Rack",
      description: "Pipe-rack leg with higher demand and serviceability attention.",
      values: {
        member_type: "pipe_rack_leg",
        section_label: "W360x79",
        length_m: 8.5,
        axial_demand_kn: 1450,
        deflection_mm: 24,
        span_mm: 8500,
      },
    },
    {
      id: "stl-corrosion-critical",
      label: "Corrosion Critical",
      description: "High section-loss scenario for urgent structural review.",
      values: {
        member_type: "brace",
        corrosion_loss_percent: 52,
        axial_demand_kn: 980,
      },
    },
    {
      id: "stl-connection-fail",
      label: "Connection Fail",
      description: "Observed connection failure scenario.",
      values: {
        member_type: "portal_frame",
        connection_failure_detected: true,
        corrosion_loss_percent: 18,
      },
    },
  ],
  defaultChart: "gauge",
  primaryMetrics: ["dc_ratio", "lambda_c", "phi_pn_kn", "corrosion_loss_percent", "status", "reinforcement_need", "connection_status"],
};

export function buildSteelOutcome(input: Record<string, unknown>): DisciplineOutcome {
  const memberType = String(input.member_type ?? "column").toLowerCase();
  const steelGrade = String(input.steel_grade ?? "a572_gr50").toLowerCase();
  const sectionLabel = String(input.section_label ?? "W310x60");
  const lengthM = Math.max(toNumber(input.length_m, 6), 0.1);
  const kFactor = Math.max(toNumber(input.k_factor, 1), 0.1);
  const rgMm = Math.max(toNumber(input.radius_of_gyration_mm, 90), 0.1);
  const fyFromInput = toNumber(input.yield_strength_mpa, 0);
  const fy = Math.max(fyFromInput > 0 ? fyFromInput : (STEEL_GRADE_DEFAULT_FY[steelGrade] ?? 345), 1);
  const eModulus = Math.max(toNumber(input.elasticity_mpa, 200000), 1);
  const area = Math.max(toNumber(input.gross_area_mm2, 7600), 1);
  const corrosionLossPct = Math.max(toNumber(input.corrosion_loss_percent, 8), 0);
  const demand = Math.max(toNumber(input.axial_demand_kn, 650), 0);
  const deflection = Math.max(toNumber(input.deflection_mm, 10), 0);
  const span = Math.max(toNumber(input.span_mm, 6000), 1);

  const reducedArea = area * Math.max(0, 1 - (corrosionLossPct / 100));
  const klOverR = (kFactor * lengthM * 1000) / rgMm;
  const lambdaC = (klOverR / Math.PI) * Math.sqrt(fy / eModulus);
  const fcr = lambdaC <= 2.25 ? ((0.658 ** (lambdaC ** 2)) * fy) : ((0.877 / (lambdaC ** 2)) * fy);
  const phiPn = (0.9 * fcr * reducedArea) / 1000;
  const dcRatio = round(demand / Math.max(phiPn, 0.01), 3);
  const deflectionRatio = round((deflection / span) * 240, 3);

  const warnings: string[] = [];
  const redFlags: string[] = [];

  if (dcRatio >= 1.05 && dcRatio < 1.5) warnings.push("PHY.STEEL_MEMBER_OVERUTILIZED");
  if (deflectionRatio > 1.0) warnings.push("PHY.STEEL_DEFLECTION_LIMIT_EXCEEDED");
  if (corrosionLossPct >= 20 && corrosionLossPct < 50) warnings.push("PHY.STEEL_CORROSION_SECTION_LOSS_MODERATE");
  if (corrosionLossPct >= 50) redFlags.push("PHY.STEEL_CORROSION_SECTION_LOSS_HIGH");
  if (dcRatio >= 1.5) redFlags.push("PHY.STEEL_COLLAPSE_RISK_HIGH");
  if (Boolean(input.connection_failure_detected)) redFlags.push("PHY.STEEL_CONNECTION_FAILURE");

  let status = "ACCEPTABLE";
  if (dcRatio >= 1.5) status = "CRITICAL";
  else if (dcRatio >= 1.05) status = "OVERSTRESSED";
  else if (dcRatio >= 1.0) status = "MARGINAL";

  const inspectionInterval = status === "CRITICAL" ? 0.25 : status === "OVERSTRESSED" ? 0.5 : status === "MARGINAL" ? 1 : 2;

  return {
    finalResults: {
      member_type: memberType,
      steel_grade: steelGrade,
      section_label: sectionLabel,
      dc_ratio: dcRatio,
      lambda_c: round(lambdaC, 3),
      fcr_mpa: round(fcr, 2),
      phi_pn_kn: round(phiPn, 2),
      reduced_area_mm2: round(reducedArea, 1),
      corrosion_loss_percent: round(corrosionLossPct, 2),
      deflection_ratio: deflectionRatio,
      inspection_interval_years: redFlags.length ? 0.25 : inspectionInterval,
      reinforcement_need: dcRatio >= 1.5 || corrosionLossPct >= 50 ? "REPLACEMENT_RECOMMENDED"
        : dcRatio >= 1.05 || corrosionLossPct >= 30 ? "REINFORCEMENT_RECOMMENDED"
        : dcRatio >= 0.9 || corrosionLossPct >= 15 ? "MONITOR_AND_EVALUATE"
        : "NO_ACTION",
      connection_status: Boolean(input.connection_failure_detected) ? "FAILED_REPAIR_REQUIRED"
        : dcRatio >= 1.05 ? "REVIEW_CONNECTION_ADEQUACY"
        : "ACCEPTABLE",
      status: redFlags.length ? "CRITICAL" : warnings.length ? status : "ACCEPTABLE",
    },
    warnings,
    redFlags,
  };
}
