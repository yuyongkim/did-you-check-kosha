import {
  CalculationResponse,
  Discipline,
  KoshaGuideReference,
  KoshaLawReference,
  RegulatoryCrosswalkItem,
  RegulatoryLink,
} from "@/lib/types";
import {
  KGS_PORTAL_LINK,
  KOSHA_PORTAL_LINK,
  PORTAL_SEARCH_LINK,
} from "@/lib/kosha/constants";
import { cleanText, uniqueBy } from "@/lib/kosha/helpers";

interface CrosswalkRule {
  id: string;
  topic: string;
  discipline: Discipline | "common";
  trigger_terms: string[];
  trigger_refs: string[];
  kosha_keywords: string[];
  legal_keywords: string[];
  korean_regulatory_summary: string;
  static_links: RegulatoryLink[];
}

const LAW_SEARCH_BASE_URL = "https://www.law.go.kr/lsSc.do";

function buildLawSearchUrl(query: string): string {
  const url = new URL(LAW_SEARCH_BASE_URL);
  url.searchParams.set("query", query);
  return url.toString();
}

const CROSSWALK_RULES: CrosswalkRule[] = [
  {
    id: "pressure-boundary-thickness",
    topic: "Pressure Boundary / Thickness / Remaining Life",
    discipline: "common",
    trigger_terms: [
      "pressure",
      "thickness",
      "corrosion",
      "remaining life",
      "배관",
      "압력용기",
      "두께",
      "부식",
      "잔여수명",
    ],
    trigger_refs: ["ASME B31.3", "ASME VIII", "API 570", "API 510"],
    kosha_keywords: ["배관", "압력용기", "두께", "부식", "검사주기"],
    legal_keywords: ["산업안전보건기준", "압력용기", "안전밸브"],
    korean_regulatory_summary:
      "압력경계(배관/용기) 계산 결과는 KOSHA 기술지침과 산업안전보건기준 조항(압력설비, 안전밸브) 근거를 함께 확인해야 합니다.",
    static_links: [
      {
        id: "law-pressure-vessel-search",
        label: "법령검색: 압력용기/안전밸브",
        url: buildLawSearchUrl("산업안전보건기준 압력용기 안전밸브"),
        type: "law_search",
      },
      {
        id: "asme-catalog",
        label: "ASME Codes Catalog",
        url: "https://www.asme.org/codes-standards",
        type: "standard_catalog",
      },
      {
        id: "api-catalog",
        label: "API Standards Catalog",
        url: "https://www.api.org/products-and-services/standards/digital-catalog",
        type: "standard_catalog",
      },
    ],
  },
  {
    id: "overpressure-relief",
    topic: "Overpressure / Relief Protection",
    discipline: "common",
    trigger_terms: [
      "safety valve",
      "relief",
      "overpressure",
      "psv",
      "안전밸브",
      "과압",
      "압력방출",
    ],
    trigger_refs: ["ASME VIII", "API 510", "API 520", "API 521", "API 570"],
    kosha_keywords: ["안전밸브", "과압보호", "압력방출장치", "정기검사"],
    legal_keywords: ["산업안전보건기준", "안전밸브", "압력설비"],
    korean_regulatory_summary:
      "과압 보호는 설계/운전/검사 단계에서 법적 의무 항목입니다. 안전밸브 설치와 기능 검증 주기를 계산 결과와 함께 제시해야 합니다.",
    static_links: [
      {
        id: "law-relief-search",
        label: "법령검색: 과압/안전밸브",
        url: buildLawSearchUrl("산업안전보건기준 안전밸브 과압"),
        type: "law_search",
      },
      {
        id: "kosha-portal",
        label: "KOSHA Portal",
        url: KOSHA_PORTAL_LINK,
        type: "regulator_portal",
      },
    ],
  },
  {
    id: "high-pressure-gas-vessel",
    topic: "High Pressure Gas / Cylinder / Storage",
    discipline: "common",
    trigger_terms: [
      "high pressure gas",
      "gas cylinder",
      "storage vessel",
      "고압가스",
      "용기",
      "저장탱크",
      "압력용기",
    ],
    trigger_refs: ["ASME VIII", "API 510", "API 570"],
    kosha_keywords: ["고압가스", "압력용기", "저장탱크", "정기검사"],
    legal_keywords: ["고압가스 안전관리법", "압력용기", "검사"],
    korean_regulatory_summary:
      "고압가스 설비는 산업안전보건 체계와 별도로 고압가스 안전관리법 체계 검토가 필요합니다. 설계 계산 결과와 법령 근거를 1:1로 연결해 관리하세요.",
    static_links: [
      {
        id: "law-high-gas-search",
        label: "법령검색: 고압가스 안전관리법",
        url: buildLawSearchUrl("고압가스 안전관리법 압력용기"),
        type: "law_search",
      },
      {
        id: "kgs-portal",
        label: "KGS Portal",
        url: KGS_PORTAL_LINK,
        type: "regulator_portal",
      },
    ],
  },
  {
    id: "rotating-equipment-integrity",
    topic: "Rotating Equipment (Pump/Compressor) Integrity",
    discipline: "rotating",
    trigger_terms: [
      "compressor",
      "pump",
      "vibration",
      "trip",
      "reciprocating",
      "centrifugal",
      "회전기기",
      "압축기",
      "펌프",
      "진동",
    ],
    trigger_refs: ["API 610", "API 617", "API 618", "API 619", "API 670", "API 674"],
    kosha_keywords: ["회전기기", "압축기", "펌프", "진동", "보호계전"],
    legal_keywords: ["산업안전보건법", "기계기구", "유해위험방지계획"],
    korean_regulatory_summary:
      "회전기기 무결성은 API 설계기준(API 610/617/618/674)과 보호시스템(API 670) 기준을 따르되, 국내 법령 문서와 연계하여 감사 근거를 함께 관리해야 합니다.",
    static_links: [
      {
        id: "law-rotating-search",
        label: "법령검색: 압축기/펌프",
        url: buildLawSearchUrl("산업안전보건법 기계기구 압축기 펌프"),
        type: "law_search",
      },
      {
        id: "api-rotating-catalog",
        label: "API Rotating Standards",
        url: "https://www.api.org/products-and-services/standards/digital-catalog",
        type: "standard_catalog",
      },
    ],
  },
];

function normalize(value: string): string {
  return cleanText(value).toLowerCase();
}

function includesAnyKeyword(haystack: string, keywords: string[]): boolean {
  const normalized = normalize(haystack);
  return keywords.some((keyword) => normalized.includes(normalize(keyword)));
}

function matchesByTerms(terms: string[], keywords: string[]): boolean {
  return terms.some((term) => includesAnyKeyword(term, keywords));
}

function matchesByReferences(references: string[], triggerRefs: string[]): boolean {
  return references.some((reference) => includesAnyKeyword(reference, triggerRefs));
}

function candidateGuides(guides: KoshaGuideReference[], rule: CrosswalkRule): KoshaGuideReference[] {
  const keywords = [...rule.kosha_keywords, ...rule.trigger_terms];
  return guides.filter((guide) =>
    includesAnyKeyword(`${guide.code} ${guide.title} ${guide.summary}`, keywords),
  );
}

function candidateLaws(laws: KoshaLawReference[], rule: CrosswalkRule): KoshaLawReference[] {
  const keywords = [...rule.legal_keywords, ...rule.trigger_terms];
  return laws.filter((law) =>
    includesAnyKeyword(`${law.law_name} ${law.article} ${law.title} ${law.summary}`, keywords),
  );
}

function buildGuideLinks(guides: KoshaGuideReference[]): RegulatoryLink[] {
  return guides
    .filter((guide) => !!guide.pdf_url)
    .map((guide) => ({
      id: `guide-${guide.id}`,
      label: `${guide.code} source`,
      url: guide.pdf_url as string,
      type: "kosha_search" as const,
    }));
}

function buildLawLinks(laws: KoshaLawReference[]): RegulatoryLink[] {
  return laws
    .filter((law) => !!law.detail_url)
    .map((law) => ({
      id: `law-${law.id}`,
      label: `${law.law_name} ${law.article}`,
      url: law.detail_url as string,
      type: "law_search" as const,
    }));
}

function confidenceFromMatches(guideCount: number, lawCount: number): "high" | "medium" | "low" {
  if (guideCount > 0 && lawCount > 0) return "high";
  if (guideCount > 0 || lawCount > 0) return "medium";
  return "low";
}

function crosswalkLinks(
  staticLinks: RegulatoryLink[],
  matchedGuides: KoshaGuideReference[],
  matchedLaws: KoshaLawReference[],
): RegulatoryLink[] {
  const all = [...staticLinks, ...buildGuideLinks(matchedGuides), ...buildLawLinks(matchedLaws)];
  return uniqueBy(
    all.filter((item) => cleanText(item.url).length > 0),
    (item) => item.url,
  );
}

function referencesForRule(result: CalculationResponse, rule: CrosswalkRule): string[] {
  const refs = result.references.filter((reference) => includesAnyKeyword(reference, rule.trigger_refs));
  if (refs.length > 0) return refs.slice(0, 4);
  return result.references.slice(0, 3);
}

function fallbackCrosswalk(
  discipline: Discipline,
  result: CalculationResponse,
): RegulatoryCrosswalkItem[] {
  return [
    {
      id: "fallback-regulatory-baseline",
      topic: "Korean Regulatory Baseline",
      discipline,
      confidence: "low",
      global_references: result.references.slice(0, 3),
      korean_regulatory_summary:
        "자동 교차매핑 룰 매칭이 부족합니다. 아래 링크로 법령/가이드 원문을 확인하고 프로젝트 기준서에 연결하세요.",
      kosha_keywords: ["KOSHA GUIDE", "산업안전보건기준", "법령 검색"],
      matched_guides: [],
      matched_laws: [],
      links: [
        {
          id: "fallback-law",
          label: "법령 통합검색",
          url: buildLawSearchUrl("산업안전보건법 산업안전보건기준"),
          type: "law_search",
        },
        {
          id: "fallback-kosha-api",
          label: "KOSHA API Portal",
          url: PORTAL_SEARCH_LINK,
          type: "regulator_portal",
        },
        {
          id: "fallback-kosha",
          label: "KOSHA Home",
          url: KOSHA_PORTAL_LINK,
          type: "regulator_portal",
        },
      ],
    },
  ];
}

export function buildRegulatoryCrosswalk(
  discipline: Discipline,
  queryTerms: string[],
  result: CalculationResponse,
  guides: KoshaGuideReference[],
  laws: KoshaLawReference[],
): RegulatoryCrosswalkItem[] {
  const matches = CROSSWALK_RULES
    .filter((rule) => rule.discipline === "common" || rule.discipline === discipline)
    .filter((rule) => {
      const termMatch = matchesByTerms(queryTerms, rule.trigger_terms);
      const refMatch = matchesByReferences(result.references, rule.trigger_refs);
      return termMatch || refMatch;
    })
    .map((rule) => {
      const matchedGuides = candidateGuides(guides, rule).slice(0, 3);
      const matchedLaws = candidateLaws(laws, rule).slice(0, 3);
      return {
        id: rule.id,
        topic: rule.topic,
        discipline: rule.discipline,
        confidence: confidenceFromMatches(matchedGuides.length, matchedLaws.length),
        global_references: referencesForRule(result, rule),
        korean_regulatory_summary: rule.korean_regulatory_summary,
        kosha_keywords: rule.kosha_keywords,
        matched_guides: matchedGuides.map((guide) => `${guide.code}: ${guide.title}`),
        matched_laws: matchedLaws.map((law) => `${law.law_name} ${law.article}: ${law.title}`),
        links: crosswalkLinks(rule.static_links, matchedGuides, matchedLaws),
      } satisfies RegulatoryCrosswalkItem;
    });

  const ranked = matches
    .sort((a, b) => {
      const score = { high: 3, medium: 2, low: 1 };
      return score[b.confidence] - score[a.confidence];
    })
    .slice(0, 4);

  if (ranked.length === 0) return fallbackCrosswalk(discipline, result);
  return ranked;
}
