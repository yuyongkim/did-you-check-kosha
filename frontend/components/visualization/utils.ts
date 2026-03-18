import { CalculationResponse } from "@/lib/types";

export function toNumber(value: unknown, fallback = 0): number {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

export function resultValue(result: CalculationResponse | null, key: string, fallback = 0): number {
  return toNumber(result?.results[key], fallback);
}

export function inputValue(result: CalculationResponse | null, key: string, fallback = 0): number {
  return toNumber(result?.details.input_data[key], fallback);
}

export function percent(value: number, base: number): number {
  if (base === 0) return 0;
  return (value / base) * 100;
}
