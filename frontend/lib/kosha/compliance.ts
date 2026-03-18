import {
  CalculationResponse,
  Discipline,
  KoshaGuideReference,
  KoshaLawReference,
  RegulatoryComplianceSummary,
  RegulatoryStatus,
} from "@/lib/types";

function statusRank(status: RegulatoryStatus): number {
  if (status === "pass") return 3;
  if (status === "review") return 2;
  if (status === "unknown") return 1;
  return 0;
}

function aggregateOverallStatus(
  guideStatus: RegulatoryStatus,
  legalStatus: RegulatoryStatus,
): RegulatoryStatus {
  return statusRank(guideStatus) <= statusRank(legalStatus) ? guideStatus : legalStatus;
}

function hasPressureLawCoverage(laws: KoshaLawReference[]): boolean {
  return laws.some((law) =>
    /(261|제\s*261\s*조|safety valve|pressure vessel)/i.test(
      `${law.article} ${law.title} ${law.summary}`,
    ),
  );
}

export function buildComplianceSummary(
  discipline: Discipline,
  guides: KoshaGuideReference[],
  laws: KoshaLawReference[],
  result: CalculationResponse,
  trace: string[],
): RegulatoryComplianceSummary {
  const guideStatus: RegulatoryStatus = guides.length >= 2 ? "pass" : guides.length > 0 ? "review" : "fail";

  let legalStatus: RegulatoryStatus = laws.length > 0 ? "review" : "fail";
  if (discipline === "piping" || discipline === "vessel" || discipline === "rotating") {
    if (hasPressureLawCoverage(laws)) legalStatus = "pass";
  } else if (laws.length >= 1) {
    legalStatus = "pass";
  }

  const overallStatus = aggregateOverallStatus(guideStatus, legalStatus);

  const notes: string[] = [];
  if (guideStatus !== "pass") {
    notes.push("Guide auto-mapping count is low; manual review is recommended.");
  }
  if (legalStatus !== "pass") {
    notes.push("Legal mapping is reference-only; final compliance decision requires legal review.");
  }
  if (result.flags.red_flags.length > 0) {
    notes.push("Red flags are present; mitigation actions should be prioritized before closure.");
  }
  if (trace.some((line) => line.toLowerCase().includes("error"))) {
    notes.push("API error detected; local fallback references were used.");
  }
  if (notes.length === 0) {
    notes.push("Guide and legal mappings were resolved successfully.");
  }

  return {
    guide_status: guideStatus,
    legal_status: legalStatus,
    overall_status: overallStatus,
    summary: `Guide ${guideStatus.toUpperCase()} / Legal ${legalStatus.toUpperCase()} / Overall ${overallStatus.toUpperCase()}`,
    notes,
  };
}
