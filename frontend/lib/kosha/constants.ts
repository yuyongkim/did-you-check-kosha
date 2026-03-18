import { Discipline } from "@/lib/types";

import { LawFallbackItem } from "@/lib/kosha/types";

export const SMART_SEARCH_DEFAULT_ENDPOINT = "https://apis.data.go.kr/B552468/srch/smartSearch";
export const GUIDE_DEFAULT_ENDPOINT = "https://apis.data.go.kr/B552468/koshaguide";
export const PORTAL_SEARCH_LINK = "https://www.data.go.kr/data/15123696/openapi.do";
export const KOSHA_PORTAL_LINK = "https://www.kosha.or.kr/kosha/index.do";
export const LAW_PORTAL_LINK = "https://www.law.go.kr/LSW/main.html";
export const KGS_PORTAL_LINK = "https://www.kgs.or.kr/";

export const LAW_CATEGORIES = new Set(["1", "2", "3", "4", "5", "8", "9", "11"]);
export const GUIDE_CATEGORY = "7";

export const LAW_CATEGORY_LABEL: Record<string, string> = {
  "1": "산업안전보건법",
  "2": "산업안전보건법 시행령",
  "3": "산업안전보건법 시행규칙",
  "4": "산업안전보건기준에 관한 규칙",
  "5": "고시/예규/훈령/지침",
  "8": "중대재해 처벌 등에 관한 법률",
  "9": "중대재해 처벌 등에 관한 법률 시행령",
  "11": "유해·위험작업 관련 규정",
};

export const BASE_TERMS: Record<Discipline, string[]> = {
  piping: ["piping", "corrosion", "thickness", "safety valve", "pressure vessel"],
  vessel: ["pressure vessel", "thickness", "inspection", "safety valve", "corrosion"],
  rotating: ["compressor", "pump", "rotating equipment", "bearing", "safety valve"],
  electrical: ["electrical equipment", "arc flash", "protection relay", "circuit breaker"],
  instrumentation: ["SIS", "instrument", "calibration", "functional safety"],
  steel: ["steel structure", "welding", "buckling", "fatigue"],
  civil: ["concrete", "crack", "repair", "structural safety"],
};

export const DYNAMIC_INPUT_FIELDS = [
  "material",
  "fluid_type",
  "service_type",
  "machine_type",
  "equipment_type",
  "instrument_type",
  "member_type",
  "element_type",
] as const;

export const DISCIPLINE_LAW_SUFFIX: Record<Discipline, string> = {
  piping: "safety valve pressure vessel",
  vessel: "safety valve pressure vessel",
  rotating: "safety valve pressure vessel",
  electrical: "electrical shock prevention",
  instrumentation: "functional safety",
  steel: "structural safety",
  civil: "construction safety",
};

export const FALLBACK_LAWS: Record<Discipline, LawFallbackItem[]> = {
  piping: [
    {
      lawName: "Safety and Health Standards Rules",
      article: "Article 261",
      title: "Safety valve and overpressure protection",
      summary: "Pressure systems shall include overpressure protection and periodic verification.",
    },
  ],
  vessel: [
    {
      lawName: "Safety and Health Standards Rules",
      article: "Article 261",
      title: "Pressure vessel overpressure prevention",
      summary: "Pressure vessels require suitable relief and monitoring controls.",
    },
  ],
  rotating: [
    {
      lawName: "Safety and Health Standards Rules",
      article: "Article 261",
      title: "Rotating equipment pressure protection",
      summary: "Compressors and pumps in pressurized service need adequate pressure safeguards.",
    },
  ],
  electrical: [
    {
      lawName: "Occupational Safety and Health Act",
      article: "Electrical Safety Clause",
      title: "Electric shock and arc hazard prevention",
      summary: "Electrical work must apply isolation, grounding, and protective devices.",
    },
  ],
  instrumentation: [
    {
      lawName: "Occupational Safety and Health Act",
      article: "General Safety Clause",
      title: "Control and protection system integrity",
      summary: "Critical control loops and protective instrumentation must be maintained and verified.",
    },
  ],
  steel: [
    {
      lawName: "Safety and Health Standards Rules",
      article: "Structure Safety Clause",
      title: "Structural collapse prevention",
      summary: "Steel structures shall satisfy inspection, maintenance, and reinforcement requirements.",
    },
  ],
  civil: [
    {
      lawName: "Occupational Safety and Health Act",
      article: "Construction Safety Clause",
      title: "Civil and construction structure safety",
      summary: "Civil structures require periodic risk evaluation and mitigation controls.",
    },
  ],
};
