import { CalculationResponse, FormFieldConfig } from "@/lib/types";

export function parseCsvCells(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let inQuotes = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];

    if (inQuotes) {
      if (char === '"' && next === '"') {
        cell += '"';
        index += 1;
        continue;
      }
      if (char === '"') {
        inQuotes = false;
        continue;
      }
      cell += char;
      continue;
    }

    if (char === '"') {
      inQuotes = true;
      continue;
    }
    if (char === ",") {
      row.push(cell.trim());
      cell = "";
      continue;
    }
    if (char === "\n" || char === "\r") {
      if (char === "\r" && next === "\n") index += 1;
      row.push(cell.trim());
      cell = "";
      if (row.some((value) => value.length > 0)) rows.push(row);
      row = [];
      continue;
    }

    cell += char;
  }

  row.push(cell.trim());
  if (row.some((value) => value.length > 0)) rows.push(row);
  return rows;
}

export function parseCsv(text: string): Array<Record<string, string>> {
  const rows = parseCsvCells(text);
  if (rows.length < 2) return [];

  const headers = rows[0].map((value) => value.trim());
  return rows.slice(1).map((values) => {
    const mapped: Record<string, string> = {};
    headers.forEach((header, index) => {
      mapped[header] = values[index] ?? "";
    });
    return mapped;
  });
}

export function toPayload(row: Record<string, string>, fields: FormFieldConfig[], sampleInput: Record<string, unknown>): Record<string, unknown> {
  const payload: Record<string, unknown> = { ...sampleInput };
  fields.forEach((field) => {
    const raw = row[field.name];
    if (raw === undefined || raw === "") return;

    if (field.type === "number") {
      payload[field.name] = Number(raw);
      return;
    }
    if (field.type === "checkbox") {
      payload[field.name] = /^(true|1|yes|y)$/i.test(raw);
      return;
    }

    payload[field.name] = raw;
  });
  return payload;
}

export async function runWithConcurrency<T, R>(items: T[], concurrency: number, worker: (item: T, index: number) => Promise<R>): Promise<R[]> {
  const results = new Array<R>(items.length);
  let nextIndex = 0;

  async function runner() {
    while (true) {
      const currentIndex = nextIndex;
      nextIndex += 1;
      if (currentIndex >= items.length) return;
      results[currentIndex] = await worker(items[currentIndex], currentIndex);
    }
  }

  const runnerCount = Math.max(1, Math.min(concurrency, items.length));
  await Promise.all(Array.from({ length: runnerCount }, () => runner()));
  return results;
}

export function download(text: string, filename: string, mime = "text/plain;charset=utf-8") {
  if (typeof window === "undefined") return;
  const blob = new Blob([text], { type: mime });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export function resultRiskScore(result: CalculationResponse): number {
  return result.flags.red_flags.length * 3 + result.flags.warnings.length;
}

export function buildScenarioFactors(points: number, pct: number): number[] {
  const safePoints = Math.max(3, Math.min(9, points % 2 === 0 ? points + 1 : points));
  const half = Math.floor(safePoints / 2);
  const step = half === 0 ? 0 : pct / half;
  const factors: number[] = [];
  for (let index = -half; index <= half; index += 1) {
    const deltaPct = index * step;
    factors.push(1 + (deltaPct / 100));
  }
  return factors;
}
