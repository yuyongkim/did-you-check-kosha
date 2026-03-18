export interface DisciplineOutcome {
  finalResults: Record<string, unknown>;
  warnings: string[];
  redFlags: string[];
}

export function toNumber(value: unknown, fallback: number): number {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) return fallback;
  return parsed;
}

export function round(value: number, digits = 2): number {
  const p = 10 ** digits;
  return Math.round(value * p) / p;
}

export function parseDate(raw: unknown): Date | null {
  if (typeof raw !== "string") return null;
  const parsed = new Date(raw);
  if (Number.isNaN(parsed.getTime())) return null;
  return parsed;
}

export function yearsBetween(a: Date | null, b: Date | null, fallback: number): number {
  if (!a || !b) return fallback;
  const diffMs = Math.abs(b.getTime() - a.getTime());
  const years = diffMs / (1000 * 60 * 60 * 24 * 365.25);
  return years > 0 ? years : fallback;
}

export function pfdToSil(pfd: number): number {
  if (pfd < 1e-4) return 4;
  if (pfd < 1e-3) return 3;
  if (pfd < 1e-2) return 2;
  if (pfd < 1e-1) return 1;
  return 0;
}

export function lookupInterpolatedTableValue(
  table: Record<string, Record<number, number>>,
  key: string,
  x: number,
  fallbackKey: string,
): number {
  const selectedTable = table[key] ?? table[fallbackKey];
  const points = Object.keys(selectedTable).map(Number).sort((a, b) => a - b);

  if (x <= points[0]) return selectedTable[points[0]];
  if (x >= points[points.length - 1]) return selectedTable[points[points.length - 1]];

  for (let idx = 1; idx < points.length; idx += 1) {
    const lo = points[idx - 1];
    const hi = points[idx];
    if (x <= hi) {
      const loVal = selectedTable[lo];
      const hiVal = selectedTable[hi];
      const ratio = (x - lo) / (hi - lo);
      return loVal + (hiVal - loVal) * ratio;
    }
  }

  return selectedTable[points[points.length - 1]];
}

export function linearRegression(
  samples: Array<{ x: number; y: number }>,
): { slope: number; intercept: number; r2: number } {
  if (samples.length < 2) return { slope: 0, intercept: 0, r2: 0 };

  const n = samples.length;
  const sumX = samples.reduce((acc, sample) => acc + sample.x, 0);
  const sumY = samples.reduce((acc, sample) => acc + sample.y, 0);
  const sumXY = samples.reduce((acc, sample) => acc + (sample.x * sample.y), 0);
  const sumXX = samples.reduce((acc, sample) => acc + (sample.x * sample.x), 0);
  const meanY = sumY / n;
  const denominator = (n * sumXX) - (sumX * sumX);
  const slope = denominator === 0 ? 0 : ((n * sumXY) - (sumX * sumY)) / denominator;
  const intercept = (sumY - (slope * sumX)) / n;

  const ssTot = samples.reduce((acc, sample) => acc + ((sample.y - meanY) ** 2), 0);
  const ssRes = samples.reduce((acc, sample) => {
    const pred = (slope * sample.x) + intercept;
    return acc + ((sample.y - pred) ** 2);
  }, 0);
  const r2 = ssTot === 0 ? 1 : Math.max(0, 1 - (ssRes / ssTot));

  return { slope, intercept, r2 };
}
