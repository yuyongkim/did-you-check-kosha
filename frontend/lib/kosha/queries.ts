import { CalculationResponse, Discipline } from "@/lib/types";
import {
  BASE_TERMS,
  DISCIPLINE_LAW_SUFFIX,
  DYNAMIC_INPUT_FIELDS,
} from "@/lib/kosha/constants";
import { cleanText, uniqueBy } from "@/lib/kosha/helpers";

export function buildSearchTerms(
  discipline: Discipline,
  input: Record<string, unknown>,
  result: CalculationResponse,
): string[] {
  const base = BASE_TERMS[discipline] ?? [];
  const dynamic = DYNAMIC_INPUT_FIELDS
    .map((field) => cleanText(input[field]))
    .filter((value) => value.length > 0 && value.length <= 28);

  const riskHints: string[] = [];
  if (result.flags.red_flags.some((flag) => flag.includes("PRESSURE") || flag.includes("CAVITATION"))) {
    riskHints.push("safety valve", "pressure vessel");
  }
  if (result.flags.warnings.some((flag) => flag.includes("CORROSION"))) {
    riskHints.push("corrosion");
  }

  return uniqueBy(
    [...base, ...dynamic, ...riskHints]
      .map((token) => cleanText(token))
      .filter((token) => token.length > 0),
    (token) => token.toLowerCase(),
  ).slice(0, 6);
}

export function guideQueryFromTerms(terms: string[]): string {
  if (terms.length === 0) return "KOSHA GUIDE";
  if (terms.length === 1) return terms[0];
  return `${terms[0]} ${terms[1]}`;
}

export function lawQueryFromTerms(discipline: Discipline, terms: string[]): string {
  const base = terms.slice(0, 2).join(" ").trim();
  const suffix = DISCIPLINE_LAW_SUFFIX[discipline];
  return `${base} ${suffix}`.trim();
}
