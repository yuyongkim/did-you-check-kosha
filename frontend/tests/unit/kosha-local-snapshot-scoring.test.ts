import { describe, expect, it } from "vitest";

import {
  buildSnippetByTokens,
  normalizeForSearch,
  prepareSearchTokens,
  scoreNormalizedTextByTokens,
} from "@/lib/kosha/local-snapshot-scoring";

describe("kosha local snapshot scoring", () => {
  it("normalizes and de-duplicates search tokens", () => {
    const tokens = prepareSearchTokens(["  High Pressure  ", "high pressure", "고압가스", "", "  "]);
    expect(tokens).toEqual(["high pressure", "고압가스"]);
  });

  it("scores normalized text by token hits and occurrences", () => {
    const tokens = prepareSearchTokens(["pressure", "gas"]);
    const text = normalizeForSearch("pressure vessel gas pressure");
    const score = scoreNormalizedTextByTokens(text, tokens);
    expect(score).toBeGreaterThan(2);
  });

  it("builds focused snippet around matched token", () => {
    const text = "prefix ".repeat(40) + "high pressure gas safety valve" + " suffix".repeat(40);
    const snippet = buildSnippetByTokens(text, ["high pressure gas"], 80);
    expect(snippet.toLowerCase()).toContain("high pressure gas");
    expect(snippet.length).toBeLessThanOrEqual(86);
  });
});

