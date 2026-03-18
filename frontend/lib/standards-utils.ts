import type { GlossaryDiscipline } from "@/lib/glossary-types";
import { PRIORITY_BY_DISCIPLINE } from "@/lib/standards-content";
import type { StandardGlossaryEntry } from "@/lib/standards-types";

function standardKey(entry: StandardGlossaryEntry): string {
  return entry.code.toUpperCase();
}

export function standardPriority(entry: StandardGlossaryEntry, discipline: GlossaryDiscipline): number {
  const key = standardKey(entry);
  if (discipline !== "all") {
    const scoped = PRIORITY_BY_DISCIPLINE[discipline][key];
    if (scoped !== undefined) return scoped;
  }
  const disciplineDefault = PRIORITY_BY_DISCIPLINE[entry.disciplines[0] ?? "common"]?.[key];
  if (disciplineDefault !== undefined) return disciplineDefault + 20;
  const global = PRIORITY_BY_DISCIPLINE.all[key];
  if (global !== undefined) return global + 50;
  return 1000;
}

export function formatStandardReference(reference: string): string {
  const raw = String(reference ?? "").trim();
  if (!raw) return raw;

  const normalized = raw.toUpperCase();

  if (normalized.includes("UG-27")) return `Internal pressure shell thickness (${raw})`;
  if (normalized.includes("UG-28")) return `External pressure buckling check (${raw})`;
  if (normalized.includes("UG-37")) return `Nozzle/opening reinforcement check (${raw})`;
  if (normalized.includes("TABLE A-1")) return `Allowable stress table lookup (${raw})`;
  if (normalized.includes("PARA 304.1.2")) return `Piping minimum thickness equation (${raw})`;
  if (normalized.includes("API 510")) return `Vessel in-service inspection basis (${raw})`;
  if (normalized.includes("API 570")) return `Piping life/inspection basis (${raw})`;
  if (normalized.includes("API 610")) return `Pump vibration/nozzle-load basis (${raw})`;
  if (normalized.includes("API 674")) return `Recip pump mechanical integrity basis (${raw})`;
  if (normalized.includes("API 617")) return `Compressor integrity basis (${raw})`;
  if (normalized.includes("API 618")) return `Recip compressor integrity basis (${raw})`;
  if (normalized.includes("API 619")) return `Rotary PD compressor integrity basis (${raw})`;
  if (normalized.includes("API 672")) return `Integrally geared compressor package basis (${raw})`;
  if (normalized.includes("API 611") || normalized.includes("API 612")) return `Steam turbine driver basis (${raw})`;
  if (normalized.includes("API 616")) return `Gas turbine driver basis (${raw})`;
  if (normalized.includes("API 670")) return `Machinery protection basis (${raw})`;
  if (normalized.includes("ISO 20816-3")) return `Vibration severity basis (${raw})`;

  return raw;
}
