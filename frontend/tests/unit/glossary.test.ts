import { describe, expect, it } from "vitest";

import { getGlossaryEntries, getTermDeepGuidance, getTermDefinition, getTermLabel } from "@/lib/glossary";

describe("glossary term helpers", () => {
  it("resolves known label and definition", () => {
    expect(getTermLabel("UG-27")).toContain("UG-27");
    expect(getTermDefinition("UG-27")).toContain("ASME");
  });

  it("returns inferred fallback for unknown keys", () => {
    expect(getTermLabel("unknown_metric_key")).toBe("Unknown Metric Key");
    expect(getTermDefinition("unknown_metric_key").length).toBeGreaterThan(10);
  });

  it("provides field guidance for all glossary terms", () => {
    const entries = getGlossaryEntries("all");
    expect(entries.length).toBeGreaterThan(0);

    for (const item of entries) {
      const guide = getTermDeepGuidance(item.key);
      expect(guide.engineeringIntent.length).toBeGreaterThan(15);
      expect(guide.calculationContext.length).toBeGreaterThan(15);
      expect(guide.inputChecks.length).toBeGreaterThanOrEqual(3);
      expect(guide.commonMisses.length).toBeGreaterThanOrEqual(2);
      expect(guide.relatedStandards.length).toBeGreaterThanOrEqual(1);
    }
  });
});
