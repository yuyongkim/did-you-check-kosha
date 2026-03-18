import { describe, expect, it } from "vitest";

import { exportPinsJson, movePinned, parseImportedPins, togglePinned } from "@/lib/glossary-pins";

describe("glossary-pins helpers", () => {
  it("toggles values on/off", () => {
    const first = togglePinned(["A"], "B");
    expect(first).toEqual(["A", "B"]);

    const second = togglePinned(first, "A");
    expect(second).toEqual(["B"]);
  });

  it("moves pinned keys up/down safely", () => {
    const list = ["A", "B", "C"];
    expect(movePinned(list, "B", "up")).toEqual(["B", "A", "C"]);
    expect(movePinned(list, "B", "down")).toEqual(["A", "C", "B"]);
    expect(movePinned(list, "A", "up")).toEqual(["A", "B", "C"]);
    expect(movePinned(list, "C", "down")).toEqual(["A", "B", "C"]);
  });

  it("exports and imports normalized pins", () => {
    const raw = exportPinsJson({ standards: ["UG-27", "UG-27", "  API 570  "], terms: ["t_min_mm", "", "RL"] });
    const parsed = parseImportedPins(raw);

    expect(parsed).toEqual({
      standards: ["UG-27", "API 570"],
      terms: ["t_min_mm", "RL"],
    });
  });

  it("returns null for invalid payloads", () => {
    expect(parseImportedPins("not-json")).toBeNull();
    expect(parseImportedPins(JSON.stringify({ version: "v1" }))).toBeNull();
  });
});
