import {
  CalculationResponse,
  Discipline,
  KoshaGuideReference,
  KoshaLawReference,
  RegulatoryContext,
} from "@/lib/types";
import {
  FALLBACK_LAWS,
  GUIDE_CATEGORY,
  LAW_CATEGORIES,
  PORTAL_SEARCH_LINK,
} from "@/lib/kosha/constants";
import { buildComplianceSummary } from "@/lib/kosha/compliance";
import { buildRegulatoryCrosswalk } from "@/lib/kosha/crosswalk";
import { getRuntimeConfig } from "@/lib/kosha/env";
import {
  fetchGuideFromDedicatedEndpoint,
  fetchSmartSearch,
} from "@/lib/kosha/fetchers";
import { cleanText, uniqueBy } from "@/lib/kosha/helpers";
import { searchLocalRegulatorySnapshot } from "@/lib/kosha/local-snapshot";
import { mapGuideItem, mapLawItem } from "@/lib/kosha/mappers";
import {
  buildSearchTerms,
  guideQueryFromTerms,
  lawQueryFromTerms,
} from "@/lib/kosha/queries";
import { CacheEntry } from "@/lib/kosha/types";

const regulatoryCache = new Map<string, CacheEntry>();
const LAW_SEARCH_BASE_URL = "https://www.law.go.kr/lsSc.do";

function buildLawSearchUrl(query: string): string {
  const url = new URL(LAW_SEARCH_BASE_URL);
  url.searchParams.set("query", query);
  return url.toString();
}

function fallbackGuides(result: CalculationResponse): KoshaGuideReference[] {
  return result.references.slice(0, 3).map((reference, index) => ({
    id: `local-guide-${index + 1}`,
    code: reference,
    title: reference,
    summary: "Local fallback mapping from standards references. Enable API for detailed KOSHA guide records.",
    score: 0,
    pdf_url: PORTAL_SEARCH_LINK,
    source: "local_fallback",
  }));
}

function fallbackLaws(discipline: Discipline): KoshaLawReference[] {
  return (FALLBACK_LAWS[discipline] ?? []).map((law, index) => ({
    id: `local-law-${discipline}-${index + 1}`,
    law_name: law.lawName,
    article: law.article,
    title: law.title,
    summary: law.summary,
    score: 0,
    source_category: "local",
    detail_url: buildLawSearchUrl(`${law.lawName} ${law.title}`),
    source: "local_fallback",
  }));
}

function buildCacheKey(discipline: Discipline, terms: string[]): string {
  return `${discipline}:${terms.join("|").toLowerCase()}`;
}

export async function buildRegulatoryContext(
  discipline: Discipline,
  input: Record<string, unknown>,
  result: CalculationResponse,
): Promise<RegulatoryContext> {
  const terms = buildSearchTerms(discipline, input, result);
  const cacheKey = buildCacheKey(discipline, terms);
  const now = Date.now();
  const cached = regulatoryCache.get(cacheKey);
  if (cached && cached.expiresAt > now) return cached.value;

  const config = getRuntimeConfig();
  const trace: string[] = [];

  let guideHealth: RegulatoryContext["source_health"]["guide_api"] = "disabled";
  let lawHealth: RegulatoryContext["source_health"]["law_api"] = "disabled";
  let guides: KoshaGuideReference[] = [];
  let laws: KoshaLawReference[] = [];

  const guideQuery = guideQueryFromTerms(terms);
  const lawQuery = lawQueryFromTerms(discipline, terms);
  trace.push(`guide_query=${guideQuery}`);
  trace.push(`law_query=${lawQuery}`);

  if (!config.enabled) {
    trace.push("regulatory integration disabled by KOSHA_REGULATORY_ENABLED");
  } else if (!config.serviceKey) {
    guideHealth = "fallback";
    lawHealth = "fallback";
    trace.push("regulatory integration fallback: empty service key");
  } else {
    const guidePromise = (async () => {
      try {
        const dedicatedItems = await fetchGuideFromDedicatedEndpoint(
          config.guideEndpoint,
          config.serviceKey,
          guideQuery,
          config.timeoutMs,
        );
        if (dedicatedItems.length > 0) {
          guideHealth = "ok";
          return dedicatedItems.map((item) => mapGuideItem(item, "koshaguide_api"));
        }

        const smartGuideItems = await fetchSmartSearch(
          config.smartSearchEndpoint,
          config.serviceKey,
          guideQuery,
          GUIDE_CATEGORY,
          8,
          config.timeoutMs,
        );
        if (smartGuideItems.length > 0) {
          guideHealth = "ok";
          return smartGuideItems.map((item) => mapGuideItem(item, "smartsearch_api"));
        }

        guideHealth = "fallback";
        trace.push("guide_api empty result, fallback engaged");
        return [];
      } catch (error) {
        guideHealth = "error";
        trace.push(`guide_api error: ${error instanceof Error ? error.message : "unknown error"}`);
        return [];
      }
    })();

    const lawPromise = (async () => {
      try {
        const mixedItems = await fetchSmartSearch(
          config.smartSearchEndpoint,
          config.serviceKey,
          lawQuery,
          "0",
          16,
          config.timeoutMs,
        );
        const lawItems = mixedItems.filter((item) => LAW_CATEGORIES.has(cleanText(item.category)));
        if (lawItems.length > 0) {
          lawHealth = "ok";
          return lawItems.map((item) => mapLawItem(item, "smartsearch_api"));
        }

        lawHealth = "fallback";
        trace.push("law_api empty result, fallback engaged");
        return [];
      } catch (error) {
        lawHealth = "error";
        trace.push(`law_api error: ${error instanceof Error ? error.message : "unknown error"}`);
        return [];
      }
    })();

    const [guideList, lawList] = await Promise.all([guidePromise, lawPromise]);
    guides = guideList;
    laws = lawList;
  }

  const localSnapshot = searchLocalRegulatorySnapshot(discipline, terms, {
    guideLimit: 12,
    lawLimit: 18,
  });
  trace.push(...localSnapshot.trace);

  if (guides.length < 3 && localSnapshot.guides.length > 0) {
    guides = uniqueBy(
      [...guides, ...localSnapshot.guides],
      (item) => `${item.code}:${item.title}`,
    );
    trace.push("guides_enriched_by_local_snapshot=true");
  }
  if (laws.length < 4 && localSnapshot.laws.length > 0) {
    laws = uniqueBy(
      [...laws, ...localSnapshot.laws],
      (item) => `${item.law_name}:${item.article}:${item.title}`,
    );
    trace.push("laws_enriched_by_local_snapshot=true");
  }

  if (guides.length === 0) guides = fallbackGuides(result);
  if (laws.length === 0) laws = fallbackLaws(discipline);

  guides = uniqueBy(guides, (item) => `${item.code}:${item.title}`)
    .sort((a, b) => b.score - a.score)
    .slice(0, 3);
  laws = uniqueBy(laws, (item) => `${item.law_name}:${item.article}:${item.title}`)
    .sort((a, b) => b.score - a.score)
    .slice(0, 4);

  const crosswalk = buildRegulatoryCrosswalk(discipline, terms, result, guides, laws);
  const compliance = buildComplianceSummary(discipline, guides, laws, result, trace);

  const value: RegulatoryContext = {
    guides,
    laws,
    crosswalk,
    compliance,
    query_terms: terms,
    generated_at: new Date().toISOString(),
    source_health: {
      guide_api: guideHealth,
      law_api: lawHealth,
    },
    trace,
  };

  regulatoryCache.set(cacheKey, {
    expiresAt: now + config.cacheTtlMs,
    value,
  });

  return value;
}
