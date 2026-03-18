import { KoshaGuideReference, KoshaLawReference } from "@/lib/types";
import {
  LAW_CATEGORY_LABEL,
  LAW_PORTAL_LINK,
  PORTAL_SEARCH_LINK,
} from "@/lib/kosha/constants";
import { cleanText, safeScore } from "@/lib/kosha/helpers";
import { SmartSearchItem } from "@/lib/kosha/types";

const LAW_SEARCH_BASE_URL = "https://www.law.go.kr/lsSc.do";

function buildLawSearchUrl(query: string): string {
  const url = new URL(LAW_SEARCH_BASE_URL);
  url.searchParams.set("query", query);
  return url.toString();
}

function extractGuideCode(item: SmartSearchItem): string {
  const merged = `${cleanText(item.title)} ${cleanText(item.content)} ${cleanText(item.doc_id)}`;
  const codeMatch = merged.match(/\b([A-Z](?:-[A-Z])?-\d{1,3}-\d{4})\b/i);
  if (codeMatch) return codeMatch[1].toUpperCase();
  if (cleanText(item.doc_id)) return cleanText(item.doc_id);
  return "KOSHA GUIDE";
}

function extractArticle(item: SmartSearchItem): string {
  const merged = `${cleanText(item.title)} ${cleanText(item.content)}`;
  const koreanArticle = merged.match(/제\s*\d+\s*조/);
  if (koreanArticle) return koreanArticle[0].replace(/\s+/g, "");
  const englishArticle = merged.match(/article\s*\d+/i);
  if (englishArticle) return englishArticle[0].replace(/\s+/g, " ");
  return "article_review_required";
}

function normalizeDetailUrl(raw: unknown): string | undefined {
  const value = cleanText(raw);
  if (!value) return undefined;
  if (value.startsWith("http://") || value.startsWith("https://")) return value;
  if (value.startsWith("/")) return `https://smartsearch.kosha.or.kr${value}`;
  return undefined;
}

export function mapGuideItem(
  item: SmartSearchItem,
  source: KoshaGuideReference["source"],
): KoshaGuideReference {
  const title = cleanText(item.title) || "KOSHA GUIDE";
  const summary = cleanText(item.highlight_content || item.content).slice(0, 220);
  const id = cleanText(item.doc_id) || `${title}-${safeScore(item.score)}`;
  const externalLink = normalizeDetailUrl(item.filepath);

  return {
    id,
    code: extractGuideCode(item),
    title,
    summary,
    score: safeScore(item.score),
    pdf_url: externalLink ?? PORTAL_SEARCH_LINK,
    source,
  };
}

export function mapLawItem(
  item: SmartSearchItem,
  source: KoshaLawReference["source"],
): KoshaLawReference {
  const category = cleanText(item.category);
  const lawName = LAW_CATEGORY_LABEL[category] ?? "Occupational safety regulation";
  const title = cleanText(item.title) || "Legal article";
  const summary = cleanText(item.highlight_content || item.content).slice(0, 280);
  const sourceText = cleanText(item.content).slice(0, 8000);
  const article = extractArticle(item);
  const id = cleanText(item.doc_id) || `${lawName}-${article}-${title}`;
  const externalLink = normalizeDetailUrl(item.filepath);
  const lawSearchLink = buildLawSearchUrl(`${lawName} ${title}`.trim());

  return {
    id,
    law_name: lawName,
    article,
    title,
    summary,
    source_text: sourceText || undefined,
    score: safeScore(item.score),
    source_category: category || "0",
    detail_url: externalLink ?? lawSearchLink ?? LAW_PORTAL_LINK,
    source,
  };
}
