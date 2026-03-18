import fs from "node:fs";
import path from "node:path";

import { Discipline, KoshaGuideReference, KoshaLawReference } from "@/lib/types";
import {
  LAW_CATEGORY_LABEL,
  PORTAL_SEARCH_LINK,
} from "@/lib/kosha/constants";
import { cleanText, safeScore, uniqueBy } from "@/lib/kosha/helpers";
import {
  buildSnippetByTokens,
  normalizeForSearch,
  prepareSearchTokens,
  scoreNormalizedTextByTokens,
} from "@/lib/kosha/local-snapshot-scoring";

const LAW_SEARCH_BASE_URL = "https://www.law.go.kr/lsSc.do";
const DEFAULT_GUIDE_LIMIT = 12;
const DEFAULT_LAW_LIMIT = 18;

interface GuideTextRow {
  guide_no?: string;
  title?: string;
  text?: string;
  source_file?: string;
  ofanc_ymd?: string;
}

interface GuideMetaRow {
  techGdlnNo?: string;
  techGdlnNm?: string;
  fileDownloadUrl?: string;
}

interface LawArticleRow {
  id?: string;
  category?: string;
  title?: string;
  content?: string;
  keyword?: string;
  score?: number;
}

interface GuideSnapshotItem {
  guideNo: string;
  title: string;
  text: string;
  searchHead: string;
  searchBody: string;
}

interface LawSnapshotItem {
  id: string;
  category: string;
  title: string;
  content: string;
  keyword: string;
  sourceScore: number;
  searchHead: string;
  searchBody: string;
}

interface SnapshotState {
  repoRoot: string;
  guideItems: GuideSnapshotItem[];
  lawItems: LawSnapshotItem[];
  guideDownloadByNo: Map<string, string>;
  localGuideNos: Set<string>;
}

interface SearchResult {
  guides: KoshaGuideReference[];
  laws: KoshaLawReference[];
  trace: string[];
}

let snapshotCache: SnapshotState | null = null;

function resolveRepoRoot(): string {
  const cwd = process.cwd();
  const parent = path.resolve(cwd, "..");
  const cwdCandidate = path.resolve(cwd, "datasets");
  const parentCandidate = path.resolve(parent, "datasets");
  if (fs.existsSync(cwdCandidate)) return cwd;
  if (fs.existsSync(parentCandidate)) return parent;
  return cwd;
}

function readJsonFile<T>(filePath: string): T {
  const raw = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(raw) as T;
}

function normalizeGuideNo(raw: unknown): string {
  return cleanText(raw).toUpperCase();
}

function extractGuideNoFromFilename(filename: string): string | null {
  const parts = filename.split("__");
  if (parts.length < 2) return null;
  const guideNo = normalizeGuideNo(parts[0]);
  return guideNo || null;
}

function collectLocalGuideNos(filesDir: string): Set<string> {
  if (!fs.existsSync(filesDir)) return new Set<string>();
  const entries = fs.readdirSync(filesDir, { withFileTypes: true });
  const nos = entries
    .filter((entry) => entry.isFile() && entry.name.toLowerCase().endsWith(".pdf"))
    .map((entry) => extractGuideNoFromFilename(entry.name))
    .filter((item): item is string => !!item);
  return new Set(nos);
}

function loadSnapshotState(): SnapshotState {
  if (snapshotCache) return snapshotCache;

  const repoRoot = resolveRepoRoot();
  const guideTextPath = path.resolve(repoRoot, "datasets", "kosha_guide", "normalized", "guide_documents_text.json");
  const lawArticlesPath = path.resolve(repoRoot, "datasets", "kosha", "normalized", "law_articles.json");
  const guidesMetaPath = path.resolve(repoRoot, "datasets", "kosha_guide", "guides.json");
  const guideFilesDir = path.resolve(repoRoot, "datasets", "kosha_guide", "files");

  const guideRows = fs.existsSync(guideTextPath)
    ? readJsonFile<GuideTextRow[]>(guideTextPath)
    : [];
  const lawRows = fs.existsSync(lawArticlesPath)
    ? readJsonFile<LawArticleRow[]>(lawArticlesPath)
    : [];
  const guideMetaRows = fs.existsSync(guidesMetaPath)
    ? readJsonFile<GuideMetaRow[]>(guidesMetaPath)
    : [];

  const guideDownloadByNo = new Map<string, string>();
  for (const row of guideMetaRows) {
    const guideNo = normalizeGuideNo(row.techGdlnNo);
    const url = cleanText(row.fileDownloadUrl);
    if (guideNo && url) {
      guideDownloadByNo.set(guideNo, url);
    }
  }

  const guideItems = (Array.isArray(guideRows) ? guideRows : [])
    .map((row) => {
      const guideNo = normalizeGuideNo(row.guide_no);
      const title = cleanText(row.title);
      const text = cleanText(row.text);
      return {
        guideNo,
        title,
        text,
        searchHead: normalizeForSearch(`${guideNo} ${title}`),
        searchBody: normalizeForSearch(text),
      } satisfies GuideSnapshotItem;
    })
    .filter((item) => item.guideNo.length > 0);

  const lawItems = (Array.isArray(lawRows) ? lawRows : [])
    .map((row) => {
      const id = cleanText(row.id);
      const category = cleanText(row.category);
      const title = cleanText(row.title);
      const content = cleanText(row.content);
      const keyword = cleanText(row.keyword);
      const sourceScore = safeScore(row.score);
      return {
        id,
        category,
        title,
        content,
        keyword,
        sourceScore,
        searchHead: normalizeForSearch(`${title} ${keyword}`),
        searchBody: normalizeForSearch(content),
      } satisfies LawSnapshotItem;
    })
    .filter((item) => item.title.length > 0 || item.content.length > 0);

  snapshotCache = {
    repoRoot,
    guideItems,
    lawItems,
    guideDownloadByNo,
    localGuideNos: collectLocalGuideNos(guideFilesDir),
  };
  return snapshotCache;
}

function buildLawSearchUrl(query: string): string {
  const url = new URL(LAW_SEARCH_BASE_URL);
  url.searchParams.set("query", query);
  return url.toString();
}

function parseArticle(title: string): string {
  const cleaned = cleanText(title);
  const korean = cleaned.match(/제\s*\d+\s*조/);
  if (korean) return korean[0].replace(/\s+/g, "");
  const english = cleaned.match(/article\s*\d+/i);
  if (english) return english[0].replace(/\s+/g, " ");
  return "article_review_required";
}

function disciplineHints(discipline: Discipline): string[] {
  if (discipline === "piping") {
    return ["배관", "부식", "두께", "안전밸브", "압력용기"];
  }
  if (discipline === "vessel") {
    return ["압력용기", "두께", "검사", "안전밸브"];
  }
  if (discipline === "rotating") {
    return ["회전기기", "압축기", "펌프", "진동", "보호계전"];
  }
  if (discipline === "electrical") {
    return ["전기", "아크플래시", "차단기", "감전"];
  }
  if (discipline === "instrumentation") {
    return ["계장", "SIS", "기능안전", "교정"];
  }
  if (discipline === "steel") {
    return ["강구조", "부식", "좌굴", "용접"];
  }
  return ["토목", "콘크리트", "균열", "열화"];
}

function localGuideUrl(state: SnapshotState, guideNo: string): string | undefined {
  if (state.localGuideNos.has(guideNo)) {
    return `/api/kosha/guide-file/${encodeURIComponent(guideNo)}`;
  }
  const fromMeta = state.guideDownloadByNo.get(guideNo);
  if (fromMeta) return fromMeta;
  return undefined;
}

export function searchLocalRegulatorySnapshot(
  discipline: Discipline,
  terms: string[],
  options?: { guideLimit?: number; lawLimit?: number },
): SearchResult {
  const state = loadSnapshotState();
  const guideLimit = Math.max(1, options?.guideLimit ?? DEFAULT_GUIDE_LIMIT);
  const lawLimit = Math.max(1, options?.lawLimit ?? DEFAULT_LAW_LIMIT);
  const queryTerms = uniqueBy(
    [...terms, ...disciplineHints(discipline)].map((term) => cleanText(term)).filter(Boolean),
    (term) => term.toLowerCase(),
  );
  const searchTokens = prepareSearchTokens(queryTerms);
  const trace: string[] = [];
  trace.push(`local_snapshot_tokens=${searchTokens.length}`);
  trace.push(`local_snapshot_guide_rows=${state.guideItems.length}`);
  trace.push(`local_snapshot_law_rows=${state.lawItems.length}`);

  const scoredGuides = state.guideItems
    .map((item) => {
      const weighted = scoreNormalizedTextByTokens(item.searchHead, searchTokens) * 1.6
        + scoreNormalizedTextByTokens(item.searchBody, searchTokens);
      return { ...item, weighted };
    })
    .filter((item) => item.weighted > 0)
    .sort((a, b) => b.weighted - a.weighted)
    .slice(0, guideLimit);

  const guides = scoredGuides.map((item, index) => {
    const pdfUrl = localGuideUrl(state, item.guideNo);
    return {
      id: `local-guide-${item.guideNo}-${index + 1}`,
      code: item.guideNo,
      title: item.title || item.guideNo,
      summary: buildSnippetByTokens(item.text, searchTokens, 220),
      score: Math.round(item.weighted * 100) / 100,
      pdf_url: pdfUrl ?? PORTAL_SEARCH_LINK,
      source: "local_fallback" as const,
    } satisfies KoshaGuideReference;
  });
  trace.push(`local_snapshot_guides=${guides.length}`);

  const scoredLaws = state.lawItems
    .map((item) => {
      const weighted = scoreNormalizedTextByTokens(item.searchHead, searchTokens) * 1.8
        + scoreNormalizedTextByTokens(item.searchBody, searchTokens);
      return { ...item, weighted };
    })
    .filter((item) => item.weighted > 0)
    .sort((a, b) => b.weighted - a.weighted)
    .slice(0, lawLimit);

  const laws = scoredLaws.map((item, index) => {
    const lawName = LAW_CATEGORY_LABEL[item.category] ?? "Occupational safety regulation";
    const article = parseArticle(item.title);
    const lawQuery = `${lawName} ${item.title}`.trim();

    return {
      id: item.id || `local-law-${index + 1}`,
      law_name: lawName,
      article,
      title: item.title || "Legal article",
      summary: buildSnippetByTokens(item.content, searchTokens, 280),
      source_text: item.content.slice(0, 8000) || undefined,
      score: Math.max(item.sourceScore, Math.round(item.weighted * 100) / 100),
      source_category: item.category || "0",
      detail_url: buildLawSearchUrl(lawQuery),
      source: "local_fallback" as const,
    } satisfies KoshaLawReference;
  });
  trace.push(`local_snapshot_laws=${laws.length}`);

  return { guides, laws, trace };
}
