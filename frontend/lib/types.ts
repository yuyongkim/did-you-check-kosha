export type Discipline =
  | "piping"
  | "vessel"
  | "rotating"
  | "electrical"
  | "instrumentation"
  | "steel"
  | "civil";

export type RequestState = "idle" | "loading" | "success" | "error";
export type ApiMode = "mock" | "backend";

export type Severity = "critical" | "high" | "medium" | "low";

export interface VerificationIssue {
  code: string;
  severity: Severity;
  message: string;
  standard_reference?: string;
  auto_action?: string;
}

export interface VerificationLayerResult {
  layer: string;
  passed: boolean;
  issues: VerificationIssue[];
  details: Record<string, unknown>;
}

export interface CalculationStep {
  step_number: number;
  description: string;
  formula_used: string;
  standard_reference: string;
  result: Record<string, unknown>;
}

export interface Recommendation {
  priority: "high" | "medium" | "low";
  action: string;
  timeline: "immediate" | "1month" | "6months" | "nextyear";
  description: string;
}

export type RegulatoryStatus = "pass" | "review" | "fail" | "unknown";

export interface KoshaGuideReference {
  id: string;
  code: string;
  title: string;
  summary: string;
  score: number;
  pdf_url?: string;
  source: "koshaguide_api" | "smartsearch_api" | "local_fallback";
}

export interface KoshaLawReference {
  id: string;
  law_name: string;
  article: string;
  title: string;
  summary: string;
  source_text?: string;
  score: number;
  source_category: string;
  detail_url?: string;
  source: "smartsearch_api" | "local_fallback";
}

export interface RegulatoryComplianceSummary {
  guide_status: RegulatoryStatus;
  legal_status: RegulatoryStatus;
  overall_status: RegulatoryStatus;
  summary: string;
  notes: string[];
}

export interface RegulatoryLink {
  id: string;
  label: string;
  url: string;
  type: "law_search" | "kosha_search" | "standard_catalog" | "regulator_portal";
}

export interface RegulatoryCrosswalkItem {
  id: string;
  topic: string;
  discipline: Discipline | "common";
  confidence: "high" | "medium" | "low";
  global_references: string[];
  korean_regulatory_summary: string;
  kosha_keywords: string[];
  matched_guides: string[];
  matched_laws: string[];
  links: RegulatoryLink[];
}

export interface RegulatoryContext {
  guides: KoshaGuideReference[];
  laws: KoshaLawReference[];
  crosswalk: RegulatoryCrosswalkItem[];
  compliance: RegulatoryComplianceSummary;
  query_terms: string[];
  generated_at: string;
  source_health: {
    guide_api: "ok" | "fallback" | "disabled" | "error";
    law_api: "ok" | "fallback" | "disabled" | "error";
  };
  trace: string[];
}

export interface CalculationDetails {
  calculation_summary: {
    discipline: Discipline;
    calculation_type: string;
    standards_applied: string[];
    confidence: "high" | "medium" | "low";
    execution_time_sec: number;
  };
  input_data: Record<string, unknown>;
  calculation_steps: CalculationStep[];
  layer_results: VerificationLayerResult[];
  final_results: Record<string, unknown>;
  recommendations: Recommendation[];
  regulatory?: RegulatoryContext;
  flags: {
    red_flags: string[];
    warnings: string[];
  };
}

export interface CalculationResponse {
  status: "success" | "error" | "blocked";
  discipline: Discipline;
  results: Record<string, unknown>;
  details: CalculationDetails;
  references: string[];
  verification: {
    layers: VerificationLayerResult[];
    confidence: "high" | "medium" | "low";
  };
  flags: {
    red_flags: string[];
    warnings: string[];
  };
}

export interface FormFieldOption {
  label: string;
  value: string;
}

export interface FormFieldOptionGroup {
  label: string;
  options: FormFieldOption[];
}

export interface FormFieldVisibilityCondition {
  field: string;
  equals?: string | number | boolean;
  equalsAny?: Array<string | number | boolean>;
}

export interface FormFieldConfig {
  name: string;
  label: string;
  type: "number" | "text" | "select" | "checkbox";
  unit?: string;
  placeholder?: string;
  min?: number;
  max?: number;
  step?: number;
  options?: FormFieldOption[];
  optionGroups?: FormFieldOptionGroup[];
  helper?: string;
  showWhen?: FormFieldVisibilityCondition;
}

export interface DisciplinePreset {
  id: string;
  label: string;
  description: string;
  values: Record<string, unknown>;
}

export interface DisciplineConfig {
  discipline: Discipline;
  title: string;
  subtitle: string;
  shortLabel: string;
  formFields: FormFieldConfig[];
  sampleInput: Record<string, unknown>;
  presets?: DisciplinePreset[];
  defaultChart: "trend" | "spectrum" | "gauge" | "bar";
  primaryMetrics: string[];
}

export interface RunHistoryEntry {
  id: string;
  timestamp: string;
  discipline: Discipline;
  projectId: string;
  assetId: string;
  status: CalculationResponse["status"];
  confidence: CalculationResponse["verification"]["confidence"];
  elapsedMs: number;
  redFlagCount: number;
  warningCount: number;
  headline: string;
}

