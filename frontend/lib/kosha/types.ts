import { RegulatoryContext } from "@/lib/types";

export interface SmartSearchItem {
  category?: string;
  content?: string;
  doc_id?: string;
  score?: number;
  title?: string;
  highlight_content?: string;
  filepath?: string;
  keyword?: string;
}

export interface CacheEntry {
  expiresAt: number;
  value: RegulatoryContext;
}

export interface RuntimeConfig {
  enabled: boolean;
  serviceKey: string;
  smartSearchEndpoint: string;
  guideEndpoint: string;
  timeoutMs: number;
  cacheTtlMs: number;
}

export interface LawFallbackItem {
  lawName: string;
  article: string;
  title: string;
  summary: string;
}
