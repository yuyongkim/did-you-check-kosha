import { describe, expect, it } from "vitest";

import { buildRegulatoryCrosswalk } from "@/lib/kosha/crosswalk";
import { buildMockCalculationResponse } from "@/lib/mock-data";
import { KoshaGuideReference, KoshaLawReference } from "@/lib/types";

describe("kosha crosswalk module", () => {
  it("maps high-pressure gas topic with Korean law links", () => {
    const result = buildMockCalculationResponse("vessel", {});

    const guides: KoshaGuideReference[] = [
      {
        id: "g-hpg-1",
        code: "C-C-91-2026",
        title: "High pressure gas vessel inspection guidance",
        summary: "압력용기, 고압가스, 검사 주기",
        score: 0.91,
        pdf_url: "https://example.com/guide.pdf",
        source: "smartsearch_api",
      },
    ];

    const laws: KoshaLawReference[] = [
      {
        id: "l-hpg-1",
        law_name: "Safety and Health Standards Rules",
        article: "Article 261",
        title: "Pressure vessel safety valve",
        summary: "고압가스 용기 과압 보호 및 안전밸브 요구사항",
        score: 0.87,
        source_category: "4",
        detail_url: "https://example.com/law",
        source: "smartsearch_api",
      },
    ];

    const items = buildRegulatoryCrosswalk(
      "vessel",
      ["high pressure gas", "고압가스", "pressure vessel"],
      result,
      guides,
      laws,
    );

    const target = items.find((item) => item.id === "high-pressure-gas-vessel");
    expect(target).toBeDefined();
    expect(target?.confidence).not.toBe("low");
    expect(target?.links.some((link) => link.url.includes("law.go.kr"))).toBe(true);
    expect(target?.links.some((link) => link.label.includes("KGS"))).toBe(true);
  });

  it("returns fallback item when no rule is matched", () => {
    const result = buildMockCalculationResponse("electrical", {});

    const items = buildRegulatoryCrosswalk("electrical", ["relay", "arc flash"], result, [], []);
    expect(items.length).toBe(1);
    expect(items[0].id).toBe("fallback-regulatory-baseline");
    expect(items[0].links.some((link) => link.url.includes("law.go.kr"))).toBe(true);
  });
});
