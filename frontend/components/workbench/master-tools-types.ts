import type { CalculationResponse } from "@/lib/types";

export interface ScenarioRow {
  label: string;
  payload?: Record<string, unknown>;
  result: CalculationResponse | null;
  error?: string;
}

export interface BatchRow {
  rowId: string;
  payload?: Record<string, unknown>;
  result: CalculationResponse | null;
  error?: string;
}

export type MasterToolsFilter = "all" | "success" | "error" | "high-risk";
export type SortDirection = "asc" | "desc";
export type ScenarioSortKey = "label" | "status" | "risk";
export type BatchSortKey = "rowId" | "status" | "risk";

export interface ScenarioSummary {
  success: number;
  failed: number;
}

export interface BatchSummary extends ScenarioSummary {
  red: number;
  warn: number;
}

export interface BatchRiskBuckets {
  success_low: number;
  success_medium: number;
  success_high: number;
  error: number;
}
