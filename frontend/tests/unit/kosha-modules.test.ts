import { describe, expect, it } from "vitest";

import { buildMockCalculationResponse } from "@/lib/mock-data";
import { buildComplianceSummary } from "@/lib/kosha/compliance";
import { buildSearchTerms, guideQueryFromTerms, lawQueryFromTerms } from "@/lib/kosha/queries";
import { KoshaGuideReference, KoshaLawReference } from "@/lib/types";

describe("kosha query modules", () => {
  it("builds search terms with dynamic input and risk hints", () => {
    const result = buildMockCalculationResponse("piping", {
      material: "SA-106 Gr.B",
      force_high_corrosion: true,
    });

    const terms = buildSearchTerms("piping", { material: "SA-106 Gr.B" }, result);

    expect(terms.length).toBeGreaterThan(0);
    expect(terms.join(" ")).toContain("SA-106 Gr.B");
    expect(terms.some((term) => term.toLowerCase().includes("corrosion"))).toBe(true);
  });

  it("creates guide and law query strings", () => {
    const terms = ["piping", "thickness", "corrosion"];

    expect(guideQueryFromTerms(terms)).toBe("piping thickness");
    expect(lawQueryFromTerms("piping", terms)).toContain("safety valve");
    expect(lawQueryFromTerms("electrical", terms)).toContain("electrical shock prevention");
  });
});

describe("kosha compliance module", () => {
  it("marks piping legal status as pass when pressure-law hit exists", () => {
    const result = buildMockCalculationResponse("piping", {});
    const guides: KoshaGuideReference[] = [
      {
        id: "g1",
        code: "D-10-2012",
        title: "Guide A",
        summary: "desc",
        score: 0.9,
        source: "smartsearch_api",
      },
      {
        id: "g2",
        code: "C-C-91-2026",
        title: "Guide B",
        summary: "desc",
        score: 0.8,
        source: "smartsearch_api",
      },
    ];
    const laws: KoshaLawReference[] = [
      {
        id: "l1",
        law_name: "Safety and Health Standards Rules",
        article: "Article 261",
        title: "Safety valve installation",
        summary: "Pressure vessel requires overpressure protection.",
        score: 0.88,
        source_category: "4",
        source: "smartsearch_api",
      },
    ];

    const summary = buildComplianceSummary("piping", guides, laws, result, []);
    expect(summary.guide_status).toBe("pass");
    expect(summary.legal_status).toBe("pass");
    expect(summary.overall_status).toBe("pass");
  });

  it("marks legal status as review when laws exist but no pressure-law hit", () => {
    const result = buildMockCalculationResponse("piping", {});
    const guides: KoshaGuideReference[] = [];
    const laws: KoshaLawReference[] = [
      {
        id: "l1",
        law_name: "Occupational Safety and Health Act",
        article: "Article 1",
        title: "General duty",
        summary: "General requirements",
        score: 0.52,
        source_category: "1",
        source: "smartsearch_api",
      },
    ];

    const summary = buildComplianceSummary("piping", guides, laws, result, []);
    expect(summary.guide_status).toBe("fail");
    expect(summary.legal_status).toBe("review");
    expect(summary.overall_status).toBe("fail");
  });
});
