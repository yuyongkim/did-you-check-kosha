import { cleanText, uniqueBy } from "@/lib/kosha/helpers";

export function normalizeForSearch(value: string): string {
  return cleanText(value).toLowerCase();
}

export function prepareSearchTokens(terms: string[]): string[] {
  return uniqueBy(
    terms
      .map((term) => normalizeForSearch(term))
      .filter((term) => term.length > 0),
    (term) => term,
  );
}

export function scoreNormalizedTextByTokens(normalizedText: string, tokens: string[]): number {
  if (!normalizedText) return 0;

  let score = 0;
  for (const token of tokens) {
    if (!token || !normalizedText.includes(token)) continue;
    score += 1;
    const occurrences = normalizedText.split(token).length - 1;
    score += Math.min(occurrences, 4) * 0.25;
  }
  return score;
}

export function buildSnippetByTokens(text: string, tokens: string[], maxLen = 240): string {
  const compact = cleanText(text);
  if (!compact) return "";
  if (compact.length <= maxLen) return compact;

  const lowered = compact.toLowerCase();
  let index = -1;
  for (const token of tokens) {
    if (!token) continue;
    const pos = lowered.indexOf(token);
    if (pos >= 0) {
      index = pos;
      break;
    }
  }

  if (index < 0) return `${compact.slice(0, maxLen).trim()}...`;

  const start = Math.max(0, index - Math.floor(maxLen / 3));
  const end = Math.min(compact.length, start + maxLen);
  const prefix = start > 0 ? "..." : "";
  const suffix = end < compact.length ? "..." : "";
  return `${prefix}${compact.slice(start, end).trim()}${suffix}`;
}

