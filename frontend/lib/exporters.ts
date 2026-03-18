import { CalculationResponse, Discipline } from "@/lib/types";
import { formatStandardReference } from "@/lib/standards";

interface ExportContext {
  projectId: string;
  assetId: string;
  discipline: Discipline;
}

function sanitizeFilePart(value: string): string {
  const normalized = value.trim().replace(/\s+/g, "_");
  const safe = normalized.replace(/[^a-zA-Z0-9._-]/g, "_").replace(/_+/g, "_");
  const trimmed = safe.replace(/^_+|_+$/g, "");
  return trimmed || "NA";
}

function downloadText(text: string, filename: string, mimeType: string): void {
  if (typeof window === "undefined") return;
  if (typeof document === "undefined") return;
  if (!document.body) return;

  const blob = new Blob([text], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.rel = "noopener";
  anchor.style.display = "none";
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export function exportResultJson(result: CalculationResponse, context: ExportContext): void {
  const payload = {
    exported_at: new Date().toISOString(),
    context,
    result,
  };
  const filename = `${sanitizeFilePart(context.projectId)}_${sanitizeFilePart(context.assetId)}_${sanitizeFilePart(context.discipline)}_${Date.now()}.json`;
  downloadText(JSON.stringify(payload, null, 2), filename, "application/json;charset=utf-8");
}

function metricLines(result: CalculationResponse): string {
  return Object.entries(result.results)
    .map(([key, value]) => `- ${key}: ${String(value)}`)
    .join("\n");
}

function referenceLines(result: CalculationResponse): string {
  return result.references.map((ref) => `- ${formatStandardReference(ref)}`).join("\n");
}

function flagLines(values: string[]): string {
  if (values.length === 0) return "- none";
  return values.map((v) => `- ${v}`).join("\n");
}

export function buildResultMarkdown(result: CalculationResponse, context: ExportContext): string {
  return [
    `# ${context.discipline.toUpperCase()} Verification Report`,
    "",
    `- Project: ${context.projectId}`,
    `- Asset: ${context.assetId}`,
    `- Exported At: ${new Date().toISOString()}`,
    `- Status: ${result.status.toUpperCase()}`,
    `- Confidence: ${result.verification.confidence.toUpperCase()}`,
    "",
    "## Summary Metrics",
    metricLines(result),
    "",
    "## Standards References",
    referenceLines(result),
    "",
    "## Verification Layers",
    ...result.verification.layers.map((layer) => `- ${layer.layer}: ${layer.passed ? "PASS" : "FAIL"} (${layer.issues.length} issues)`),
    "",
    "## Red Flags",
    flagLines(result.flags.red_flags),
    "",
    "## Warnings",
    flagLines(result.flags.warnings),
    "",
  ].join("\n");
}

export function exportResultMarkdown(result: CalculationResponse, context: ExportContext): void {
  const markdown = buildResultMarkdown(result, context);
  const filename = `${sanitizeFilePart(context.projectId)}_${sanitizeFilePart(context.assetId)}_${sanitizeFilePart(context.discipline)}_${Date.now()}.md`;
  downloadText(markdown, filename, "text/markdown;charset=utf-8");
}
