export interface GlossaryPins {
  standards: string[];
  terms: string[];
}

const STORAGE_KEY = "epc_glossary_pins_v1";
const EXPORT_VERSION = "v1";

const EMPTY_PINS: GlossaryPins = {
  standards: [],
  terms: [],
};

function sanitize(values: unknown): string[] {
  if (!Array.isArray(values)) return [];
  return Array.from(
    new Set(
      values
        .filter((value): value is string => typeof value === "string")
        .map((value) => value.trim())
        .filter(Boolean),
    ),
  );
}

function normalizePins(pins: Partial<GlossaryPins> | null | undefined): GlossaryPins {
  return {
    standards: sanitize(pins?.standards),
    terms: sanitize(pins?.terms),
  };
}

export function loadGlossaryPins(): GlossaryPins {
  if (typeof window === "undefined") return EMPTY_PINS;
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return EMPTY_PINS;
    const parsed = JSON.parse(raw) as Partial<GlossaryPins>;
    return normalizePins(parsed);
  } catch {
    return EMPTY_PINS;
  }
}

export function saveGlossaryPins(pins: GlossaryPins): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(pins));
}

export function togglePinned(list: string[], key: string): string[] {
  if (list.includes(key)) return list.filter((item) => item !== key);
  return [...list, key];
}

export function movePinned(list: string[], key: string, direction: "up" | "down"): string[] {
  const index = list.indexOf(key);
  if (index < 0) return list;
  const targetIndex = direction === "up" ? index - 1 : index + 1;
  if (targetIndex < 0 || targetIndex >= list.length) return list;
  const next = [...list];
  [next[index], next[targetIndex]] = [next[targetIndex], next[index]];
  return next;
}

export function exportPinsJson(pins: GlossaryPins): string {
  return JSON.stringify(
    {
      version: EXPORT_VERSION,
      exported_at: new Date().toISOString(),
      pins: normalizePins(pins),
    },
    null,
    2,
  );
}

export function parseImportedPins(raw: string): GlossaryPins | null {
  try {
    const parsed = JSON.parse(raw) as {
      version?: string;
      pins?: Partial<GlossaryPins>;
    };
    if (!parsed || typeof parsed !== "object") return null;
    if (!parsed.pins) return null;
    return normalizePins(parsed.pins);
  } catch {
    return null;
  }
}
