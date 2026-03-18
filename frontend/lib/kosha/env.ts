import {
  GUIDE_DEFAULT_ENDPOINT,
  SMART_SEARCH_DEFAULT_ENDPOINT,
} from "@/lib/kosha/constants";
import { RuntimeConfig } from "@/lib/kosha/types";

function parseServiceKey(raw: string): string {
  if (!raw.trim()) return "";
  try {
    return decodeURIComponent(raw);
  } catch {
    return raw;
  }
}

function resolveServiceKey(): string {
  const raw =
    process.env.KOSHA_API_KEY_ENCODING ??
    process.env.KOSHA_API_KEY_ENCODED ??
    process.env.KOSHA_SERVICE_KEY ??
    process.env.KOSHA_API_KEY ??
    process.env.KOSHA_API_KEY_DECODING ??
    process.env.KOSHA_API_KEY_DECODED ??
    "";
  return parseServiceKey(raw);
}

function resolveEnabledFlag(): boolean {
  const value = (process.env.KOSHA_REGULATORY_ENABLED ?? "true").trim().toLowerCase();
  return value !== "false" && value !== "0" && value !== "off";
}

function resolveTimeoutMs(): number {
  const parsed = Number(process.env.KOSHA_API_TIMEOUT_MS ?? 5500);
  if (!Number.isFinite(parsed) || parsed < 1000) return 5500;
  return parsed;
}

function resolveCacheTtlMs(): number {
  const parsed = Number(process.env.KOSHA_CACHE_TTL_MS ?? 300000);
  if (!Number.isFinite(parsed) || parsed < 10000) return 300000;
  return parsed;
}

export function getRuntimeConfig(): RuntimeConfig {
  return {
    enabled: resolveEnabledFlag(),
    serviceKey: resolveServiceKey(),
    smartSearchEndpoint: (process.env.KOSHA_SMART_SEARCH_API_ENDPOINT ?? SMART_SEARCH_DEFAULT_ENDPOINT).trim(),
    guideEndpoint: (process.env.KOSHA_GUIDE_API_ENDPOINT ?? GUIDE_DEFAULT_ENDPOINT).trim(),
    timeoutMs: resolveTimeoutMs(),
    cacheTtlMs: resolveCacheTtlMs(),
  };
}
