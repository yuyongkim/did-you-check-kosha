import { buildResultMarkdown } from "@/lib/exporters";
import type { CalculationResponse, Discipline, FormFieldConfig } from "@/lib/types";
import { resultRiskScore } from "@/components/workbench/master-tools-utils";
import type {
  BatchRiskBuckets,
  BatchRow,
  BatchSortKey,
  BatchSummary,
  MasterToolsFilter,
  ScenarioRow,
  ScenarioSortKey,
  ScenarioSummary,
  SortDirection,
} from "@/components/workbench/master-tools-types";

export function summarizeScenarioRows(rows: ScenarioRow[]): ScenarioSummary {
  return {
    success: rows.filter((row) => row.result).length,
    failed: rows.filter((row) => row.error).length,
  };
}

export function filterScenarioRows(
  rows: ScenarioRow[],
  filter: MasterToolsFilter,
  search: string,
  riskHighThreshold: number,
): ScenarioRow[] {
  const keyword = search.trim().toLowerCase();
  return rows.filter((row) => {
    const passFilter = filter === "all"
      ? true
      : filter === "success"
          ? Boolean(row.result)
        : filter === "error"
          ? Boolean(row.error)
          : Boolean(row.result && resultRiskScore(row.result) >= riskHighThreshold);
    if (!passFilter) return false;
    if (!keyword) return true;
    return row.label.toLowerCase().includes(keyword) || String(row.error ?? "").toLowerCase().includes(keyword);
  });
}

export function sortScenarioRows(
  rows: ScenarioRow[],
  sortKey: ScenarioSortKey,
  sortDir: SortDirection,
): ScenarioRow[] {
  const sorted = [...rows];
  sorted.sort((left, right) => {
    if (sortKey === "label") return left.label.localeCompare(right.label);
    if (sortKey === "status") {
      const a = left.result?.status ?? "error";
      const b = right.result?.status ?? "error";
      return a.localeCompare(b);
    }
    const aRisk = left.result ? resultRiskScore(left.result) : -1;
    const bRisk = right.result ? resultRiskScore(right.result) : -1;
    return aRisk - bRisk;
  });
  return sortDir === "asc" ? sorted : sorted.reverse();
}

export function summarizeBatchRows(rows: BatchRow[]): BatchSummary {
  const successRows = rows.filter((row) => row.result);
  return {
    success: successRows.length,
    failed: rows.filter((row) => row.error).length,
    red: successRows.reduce((sum, row) => sum + (row.result?.flags.red_flags.length ?? 0), 0),
    warn: successRows.reduce((sum, row) => sum + (row.result?.flags.warnings.length ?? 0), 0),
  };
}

export function filterBatchRows(
  rows: BatchRow[],
  filter: MasterToolsFilter,
  search: string,
  riskHighThreshold: number,
): BatchRow[] {
  const keyword = search.trim().toLowerCase();
  return rows.filter((row) => {
    const passFilter = filter === "all"
      ? true
      : filter === "success"
          ? Boolean(row.result)
        : filter === "error"
          ? Boolean(row.error)
          : Boolean(row.result && resultRiskScore(row.result) >= riskHighThreshold);
    if (!passFilter) return false;
    if (!keyword) return true;
    return row.rowId.toLowerCase().includes(keyword) || String(row.error ?? "").toLowerCase().includes(keyword);
  });
}

export function sortBatchRows(
  rows: BatchRow[],
  sortKey: BatchSortKey,
  sortDir: SortDirection,
): BatchRow[] {
  const sorted = [...rows];
  sorted.sort((left, right) => {
    if (sortKey === "rowId") {
      return left.rowId.localeCompare(right.rowId);
    }
    if (sortKey === "status") {
      const a = left.result?.status ?? "error";
      const b = right.result?.status ?? "error";
      return a.localeCompare(b);
    }
    const leftRisk = left.result ? resultRiskScore(left.result) : -1;
    const rightRisk = right.result ? resultRiskScore(right.result) : -1;
    return leftRisk - rightRisk;
  });
  return sortDir === "asc" ? sorted : sorted.reverse();
}

export function groupBatchErrors(rows: BatchRow[]): Array<[string, number]> {
  const groups = new Map<string, number>();
  rows.forEach((row) => {
    if (!row.error) return;
    groups.set(row.error, (groups.get(row.error) ?? 0) + 1);
  });
  return Array.from(groups.entries()).sort((a, b) => b[1] - a[1]);
}

export function bucketBatchRisk(
  rows: BatchRow[],
  riskMediumThreshold: number,
  riskHighThreshold: number,
): BatchRiskBuckets {
  const buckets: BatchRiskBuckets = {
    success_low: 0,
    success_medium: 0,
    success_high: 0,
    error: 0,
  };

  rows.forEach((row) => {
    if (!row.result) {
      buckets.error += 1;
      return;
    }
    const score = resultRiskScore(row.result);
    if (score >= riskHighThreshold) buckets.success_high += 1;
    else if (score >= riskMediumThreshold) buckets.success_medium += 1;
    else buckets.success_low += 1;
  });

  return buckets;
}

function serializeScenarioRows(rows: ScenarioRow[]) {
  return rows.map((item) => ({
    label: item.label,
    status: item.result?.status ?? "error",
    confidence: item.result?.verification.confidence ?? "-",
    red: item.result?.flags.red_flags.length ?? 0,
    warn: item.result?.flags.warnings.length ?? 0,
    error: item.error,
  }));
}

function serializeBatchRows(rows: BatchRow[]) {
  return rows.map((item) => ({
    rowId: item.rowId,
    status: item.result?.status ?? "error",
    confidence: item.result?.verification.confidence ?? "-",
    red: item.result?.flags.red_flags.length ?? 0,
    warn: item.result?.flags.warnings.length ?? 0,
    error: item.error,
  }));
}

export function buildSummaryClipboardText({
  activeResult,
  scenarioSummary,
  batchSummary,
  discipline,
  projectId,
  assetId,
}: {
  activeResult: CalculationResponse | null;
  scenarioSummary: ScenarioSummary;
  batchSummary: BatchSummary;
  discipline: Discipline;
  projectId: string;
  assetId: string;
}): string {
  if (activeResult) {
    return buildResultMarkdown(activeResult, { discipline, projectId, assetId });
  }

  return [
    `Scenario: success=${scenarioSummary.success}, failed=${scenarioSummary.failed}`,
    `Batch: success=${batchSummary.success}, failed=${batchSummary.failed}, red=${batchSummary.red}, warn=${batchSummary.warn}`,
  ].join("\n");
}

export function buildEvidencePackPayload({
  discipline,
  projectId,
  assetId,
  batchMaxRows,
  batchConcurrency,
  activeResult,
  scenarioRows,
  batchRows,
}: {
  discipline: Discipline;
  projectId: string;
  assetId: string;
  batchMaxRows: number;
  batchConcurrency: number;
  activeResult: CalculationResponse | null;
  scenarioRows: ScenarioRow[];
  batchRows: BatchRow[];
}) {
  const scenarioPayload = serializeScenarioRows(scenarioRows);
  const batchPayload = serializeBatchRows(batchRows);
  const stampIso = new Date().toISOString();

  const pack = {
    exported_at: stampIso,
    context: { discipline, projectId, assetId, batch_max_rows: batchMaxRows, batch_concurrency: batchConcurrency },
    active_result: activeResult,
    scenario_results: scenarioPayload,
    batch_results: batchPayload,
    markdown_preview: activeResult ? buildResultMarkdown(activeResult, { discipline, projectId, assetId }) : "",
  };

  const markdown = [
    `# Evidence Pack (${discipline.toUpperCase()})`,
    "",
    `- Project: ${projectId}`,
    `- Asset: ${assetId}`,
    `- Exported: ${stampIso}`,
    `- Batch Config: max_rows=${batchMaxRows}, concurrency=${batchConcurrency}`,
    "",
    "## Active Result",
    activeResult ? buildResultMarkdown(activeResult, { discipline, projectId, assetId }) : "- none",
    "",
    "## Scenario Lab Summary",
    scenarioPayload.length === 0
      ? "- none"
      : scenarioPayload.map((row) => `- ${row.label}: ${row.status} | conf=${row.confidence} | red=${row.red} | warn=${row.warn}`).join("\n"),
    "",
    "## Batch Screening Summary",
    batchPayload.length === 0
      ? "- none"
      : batchPayload.map((row) => `- ${row.rowId}: ${row.status} | conf=${row.confidence} | red=${row.red} | warn=${row.warn}`).join("\n"),
    "",
    "## Link Index",
    "- /calculation-guide",
    "- /glossary",
    `- /${discipline}`,
    "",
  ].join("\n");

  return { pack, markdown };
}

function escapeCsvCell(value: string): string {
  return `"${value.replaceAll("\"", "\"\"")}"`;
}

export function buildScenarioResultsCsv(rows: ScenarioRow[]): string {
  const header = ["scenario_label", "status", "confidence", "risk_score", "red_flags", "warnings", "error"].join(",");
  const body = rows.map((row) => {
    const status = row.result?.status ?? "error";
    const confidence = row.result?.verification.confidence ?? "-";
    const risk = row.result ? String(resultRiskScore(row.result)) : "0";
    const red = row.result ? String(row.result.flags.red_flags.length) : "0";
    const warn = row.result ? String(row.result.flags.warnings.length) : "0";
    const error = row.error ?? "";
    return [row.label, status, confidence, risk, red, warn, error].map((value) => escapeCsvCell(String(value))).join(",");
  });
  return [header, ...body].join("\n");
}

export function buildBatchResultsCsv(rows: BatchRow[]): string {
  const header = ["row_id", "status", "confidence", "risk_score", "red_flags", "warnings", "error"].join(",");
  const body = rows.map((row) => {
    const status = row.result?.status ?? "error";
    const confidence = row.result?.verification.confidence ?? "-";
    const risk = row.result ? String(resultRiskScore(row.result)) : "0";
    const red = row.result ? String(row.result.flags.red_flags.length) : "0";
    const warn = row.result ? String(row.result.flags.warnings.length) : "0";
    const error = row.error ?? "";
    return [row.rowId, status, confidence, risk, red, warn, error].map((value) => escapeCsvCell(String(value))).join(",");
  });
  return [header, ...body].join("\n");
}

export function buildBatchTemplateCsv(
  fields: FormFieldConfig[],
  sampleInput: Record<string, unknown>,
): string {
  const headers = ["asset_id", "project_id", ...fields.map((field) => field.name)].join(",");
  const sample = ["ASSET-100", "PROJECT-ALPHA", ...fields.map((field) => String(sampleInput[field.name] ?? ""))].join(",");
  return `${headers}\n${sample}\n`;
}
