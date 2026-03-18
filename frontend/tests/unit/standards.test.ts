import { describe, expect, it } from "vitest";

import { getStandardDeepGuidance, getStandardGlossaryEntries } from "@/lib/standards";

describe("standard glossary metadata", () => {
  it("includes source and official link metadata for all entries", () => {
    const entries = getStandardGlossaryEntries("all");
    expect(entries.length).toBeGreaterThan(0);

    for (const item of entries) {
      expect(item.publisher.length).toBeGreaterThan(0);
      expect(item.officialUrl.startsWith("https://")).toBe(true);
      expect(item.accessNote.length).toBeGreaterThan(10);
    }
  });
});

describe("standard glossary field guide", () => {
  it("returns practical field guidance for all standard entries", () => {
    const entries = getStandardGlossaryEntries("all");
    for (const item of entries) {
      const guide = getStandardDeepGuidance(item.code);
      expect(guide.engineeringIntent.length).toBeGreaterThan(20);
      expect(guide.practicalUse.length).toBeGreaterThan(20);
      expect(guide.whatToVerify.length).toBeGreaterThanOrEqual(3);
      expect(guide.commonMisses.length).toBeGreaterThanOrEqual(2);
    }
  });
});
