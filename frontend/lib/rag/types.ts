import { Discipline } from "@/lib/types";

export type KoshaRagSourceType = "guide_chunk" | "law_article" | string;

export interface KoshaRagHit {
  doc_id: string;
  source_type: KoshaRagSourceType;
  title: string;
  reference_code: string;
  score: number;
  snippet: string;
  url: string | null;
}

export interface KoshaRagQueryResponse {
  query: string;
  top_k: number;
  discipline: Discipline | "common" | string | null;
  hits: KoshaRagHit[];
  answer: string | null;
}

export interface KoshaRagQueryRequest {
  query: string;
  discipline?: Discipline;
  top_k?: number;
  generate?: boolean;
  model?: string;
  max_context?: number;
}
