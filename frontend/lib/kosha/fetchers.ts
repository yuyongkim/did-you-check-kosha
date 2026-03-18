import { GUIDE_CATEGORY } from "@/lib/kosha/constants";
import { cleanText, toArray } from "@/lib/kosha/helpers";
import { SmartSearchItem } from "@/lib/kosha/types";

function unwrapItems(payload: unknown): SmartSearchItem[] {
  const candidate = payload as {
    response?: {
      body?: {
        items?: { item?: SmartSearchItem | SmartSearchItem[] };
        total_media?:
          | { media?: SmartSearchItem | SmartSearchItem[] }
          | SmartSearchItem[]
          | SmartSearchItem;
      };
    };
  };

  const body = candidate?.response?.body;
  const items = toArray(body?.items?.item);
  const totalMediaRaw = body?.total_media;
  const media = Array.isArray(totalMediaRaw)
    ? totalMediaRaw
    : toArray(
        (totalMediaRaw as { media?: SmartSearchItem | SmartSearchItem[] } | undefined)?.media ??
          (totalMediaRaw as SmartSearchItem | undefined),
      );

  return [...items, ...media]
    .filter((item) => item && typeof item === "object")
    .filter((item) => cleanText(item.title || item.content).length > 0);
}

async function fetchJson(url: URL, timeoutMs: number): Promise<unknown> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url.toString(), {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      cache: "no-store",
      signal: controller.signal,
    });

    const text = await response.text();
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${text.slice(0, 160) || "empty response"}`);
    }

    try {
      return JSON.parse(text) as unknown;
    } catch {
      return {};
    }
  } finally {
    clearTimeout(timer);
  }
}

export async function fetchSmartSearch(
  endpoint: string,
  serviceKey: string,
  query: string,
  category: string,
  numRows: number,
  timeoutMs: number,
): Promise<SmartSearchItem[]> {
  const url = new URL(endpoint);
  url.searchParams.set("serviceKey", serviceKey);
  url.searchParams.set("pageNo", "1");
  url.searchParams.set("numOfRows", String(numRows));
  url.searchParams.set("searchValue", query);
  url.searchParams.set("category", category);

  const payload = await fetchJson(url, timeoutMs);
  return unwrapItems(payload);
}

export async function fetchGuideFromDedicatedEndpoint(
  endpoint: string,
  serviceKey: string,
  query: string,
  timeoutMs: number,
): Promise<SmartSearchItem[]> {
  const attempts: Array<Record<string, string>> = [
    { serviceKey, pageNo: "1", numOfRows: "8", searchValue: query, category: GUIDE_CATEGORY },
    { serviceKey, pageNo: "1", numOfRows: "8", searchValue: query },
    { serviceKey, pageNo: "1", numOfRows: "8", keyword: query, category: GUIDE_CATEGORY },
    { serviceKey, pageNo: "1", numOfRows: "8", keyword: query },
  ];

  for (const params of attempts) {
    const url = new URL(endpoint);
    for (const [key, value] of Object.entries(params)) {
      url.searchParams.set(key, value);
    }

    try {
      const payload = await fetchJson(url, timeoutMs);
      const items = unwrapItems(payload);
      if (items.length > 0) return items;
    } catch {
      // Keep trying parameter permutations.
    }
  }

  return [];
}
