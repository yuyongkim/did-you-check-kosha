"use client";

import { useMemo, useState } from "react";
import { Bot, ExternalLink, FileText, Gavel, Loader2, Search } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { queryLocalKoshaRag } from "@/lib/rag/client";
import { KoshaRagHit, KoshaRagQueryResponse } from "@/lib/rag/types";
import { CalculationResponse, Discipline, RequestState } from "@/lib/types";

const DEFAULT_SUGGESTIONS_EN: Record<Discipline, string[]> = {
  piping: [
    "KOSHA piping minimum thickness criteria",
    "piping corrosion-based inspection interval",
    "pressure piping safety valve legal requirement",
  ],
  vessel: [
    "pressure vessel minimum thickness rule",
    "pressure vessel safety valve law article",
    "API 510 related KOSHA guidance",
  ],
  rotating: [
    "rotating equipment vibration acceptance criteria",
    "compressor surge protection guideline",
    "pump NPSH risk regulatory reference",
  ],
  electrical: [
    "arc flash protection requirement",
    "breaker rating and short-circuit check",
    "electrical safety management article",
  ],
  instrumentation: [
    "SIL and PFDavg requirement",
    "instrument drift calibration interval",
    "SIS compliance article",
  ],
  steel: [
    "steel structure D/C ratio requirement",
    "section loss acceptance limit",
    "repair and reinforcement guideline",
  ],
  civil: [
    "concrete durability repair prioritization",
    "crack and spalling severity criteria",
    "civil structure safety regulation reference",
  ],
};

const DEFAULT_SUGGESTIONS_KO: Record<Discipline, string[]> = {
  piping: [
    "배관 최소두께 KOSHA 지침",
    "배관 부식 기반 검사주기 기준",
    "압력배관 안전밸브 법령 근거",
  ],
  vessel: [
    "압력용기 최소두께 기준",
    "압력용기 안전밸브 법령 조항",
    "API 510 연계 KOSHA 지침",
  ],
  rotating: [
    "회전기기 진동 허용 기준",
    "압축기 서지 보호 가이드",
    "펌프 NPSH 리스크 규정",
  ],
  electrical: [
    "아크플래시 보호 요구사항",
    "차단기 정격과 단락전류 검토",
    "전기 안전관리 법령",
  ],
  instrumentation: [
    "SIL 및 PFDavg 요구사항",
    "계장 드리프트 교정 주기",
    "SIS 준수 조항",
  ],
  steel: [
    "철골 구조 D/C 비율 기준",
    "단면 손실 허용 한계",
    "보수 보강 가이드",
  ],
  civil: [
    "콘크리트 내구성 보수 우선순위",
    "균열 및 박락 심각도 기준",
    "토목 구조 안전 규정",
  ],
};

function buildSuggestions(
  discipline: Discipline,
  result: CalculationResponse | null,
  language: "en" | "ko",
): string[] {
  const defaults = language === "ko" ? DEFAULT_SUGGESTIONS_KO[discipline] : DEFAULT_SUGGESTIONS_EN[discipline];
  const regulatoryTerms = result?.details.regulatory?.query_terms ?? [];
  const termBased = (() => {
    if (regulatoryTerms.length === 0) return [];
    const base = regulatoryTerms.slice(0, 3).join(" ");
    if (language === "ko") {
      return [
        `${base} KOSHA 지침`,
        `${base} 법령 조항`,
      ];
    }
    return [
      `${base} KOSHA guide`,
      `${base} legal article`,
    ];
  })();

  return Array.from(
    new Set(
      [...termBased, ...defaults]
        .map((item) => item.trim())
        .filter(Boolean),
    ),
  ).slice(0, 4);
}

function hitBadge(hit: KoshaRagHit, language: "en" | "ko"): { text: string; variant: "ok" | "warning" | "neutral" } {
  if (hit.source_type === "law_article") return { text: language === "ko" ? "법령" : "LAW", variant: "warning" };
  if (hit.source_type === "guide_chunk") return { text: language === "ko" ? "지침" : "GUIDE", variant: "ok" };
  return { text: language === "ko" ? "기타" : String(hit.source_type).toUpperCase(), variant: "neutral" };
}

function stateBadge(state: RequestState, language: "en" | "ko"): { text: string; variant: "ok" | "warning" | "blocked" | "neutral" } {
  if (state === "loading") return { text: language === "ko" ? "조회중" : "RUNNING", variant: "warning" };
  if (state === "success") return { text: language === "ko" ? "준비" : "READY", variant: "ok" };
  if (state === "error") return { text: language === "ko" ? "오류" : "ERROR", variant: "blocked" };
  return { text: language === "ko" ? "대기" : "IDLE", variant: "neutral" };
}

export function LocalRagPanel({
  discipline,
  result,
}: {
  discipline: Discipline;
  result: CalculationResponse | null;
}) {
  const { language } = useUiLanguage();
  const [query, setQuery] = useState<string>("");
  const [requestState, setRequestState] = useState<RequestState>("idle");
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<KoshaRagQueryResponse | null>(null);
  const copy = language === "ko"
    ? {
        title: "로컬 KOSHA RAG",
        info: "로컬 `datasets/kosha_rag` 인덱스 기반으로 지침/법령 근거를 반환합니다.",
        placeholder: "예) 배관 최소두께 KOSHA 지침",
        enterQuery: "질문을 입력하세요.",
        noCalc: "계산 없이도 조회 가능하지만, 계산 후 검색어 품질이 더 좋아집니다.",
        answer: "답변",
        sourceLink: "원문 링크",
        noHits: "검색 결과가 없습니다. 키워드를 더 구체화해보세요.",
        score: "점수",
        noRef: "참조 없음",
      }
    : {
        title: "Local KOSHA RAG",
        info: "Uses local `datasets/kosha_rag` index to return grounded guide/law evidence.",
        placeholder: "ex) piping minimum thickness KOSHA guide",
        enterQuery: "Enter a query.",
        noCalc: "Query works without a calculation, but running one first improves keyword context.",
        answer: "Answer",
        sourceLink: "source link",
        noHits: "No hits found. Try narrower keywords.",
        score: "score",
        noRef: "NO-REF",
      };

  const suggestions = useMemo(
    () => buildSuggestions(discipline, result, language),
    [discipline, result, language],
  );
  const badge = stateBadge(requestState, language);

  const runQuery = async (nextQuery?: string) => {
    const normalized = (nextQuery ?? query).trim();
    if (!normalized) {
      setError(copy.enterQuery);
      setRequestState("error");
      return;
    }

    setQuery(normalized);
    setRequestState("loading");
    setError(null);

    try {
      const rag = await queryLocalKoshaRag({
        query: normalized,
        discipline,
        top_k: 6,
      });
      setResponse(rag);
      setRequestState("success");
    } catch (err) {
      const message = err instanceof Error ? err.message : (language === "ko" ? "RAG 조회 실패" : "RAG query failed");
      setError(message);
      setRequestState("error");
    }
  };

  const hits = response?.hits.slice(0, 4) ?? [];

  return (
    <Card className="animate-fadeUp">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="flex items-center gap-1.5">
          <Bot className="h-4 w-4 text-primary" />
          {copy.title}
        </CardTitle>
        <Badge variant={badge.variant}>{badge.text}</Badge>
      </CardHeader>
      <CardContent className="space-y-3">
        <p className="text-xs text-muted-foreground">
          {copy.info}
        </p>

        <div className="flex gap-2">
          <Input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder={copy.placeholder}
            className="h-8 text-xs"
          />
          <Button
            type="button"
            variant="outline"
            className="h-8 px-2"
            onClick={() => void runQuery()}
            disabled={requestState === "loading"}
          >
            {requestState === "loading" ? (
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
            ) : (
              <Search className="h-3.5 w-3.5" />
            )}
          </Button>
        </div>

        <div className="flex flex-wrap gap-1">
          {suggestions.map((item) => (
            <Button
              key={item}
              type="button"
              variant="outline"
              className="h-7 px-2 text-[11px]"
              onClick={() => void runQuery(item)}
              disabled={requestState === "loading"}
            >
              {item}
            </Button>
          ))}
        </div>

        {!result && (
          <p className="text-xs text-muted-foreground">
            {copy.noCalc}
          </p>
        )}

        {error && <p className="text-xs text-danger">{error}</p>}

        {response?.answer && (
          <div className="rounded-[6px] border border-border bg-muted p-2">
            <p className="mb-1 text-xs uppercase tracking-wide text-primary">{copy.answer}</p>
            <p className="whitespace-pre-wrap text-xs text-foreground">{response.answer}</p>
          </div>
        )}

        {hits.length > 0 && (
          <ul className="space-y-1">
            {hits.map((hit) => {
              const source = hitBadge(hit, language);
              return (
                <li key={hit.doc_id} className="rounded-[6px] border border-border bg-card p-2">
                  <div className="flex items-center justify-between gap-2">
                    <p className="line-clamp-1 text-xs font-semibold text-foreground">{hit.title}</p>
                    <Badge variant={source.variant}>{source.text}</Badge>
                  </div>
                  <p className="text-[11px] text-muted-foreground">
                    {hit.reference_code || copy.noRef} | {copy.score} {hit.score.toFixed(3)}
                  </p>
                  <p className="mt-1 line-clamp-3 text-xs text-foreground/90">{hit.snippet}</p>
                  {hit.url && (
                    <a
                      href={hit.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mt-1 inline-flex items-center gap-1 text-xs text-primary hover:underline"
                    >
                      {hit.source_type === "law_article" ? (
                        <Gavel className="h-3 w-3" />
                      ) : (
                        <FileText className="h-3 w-3" />
                      )}
                      {copy.sourceLink}
                      <ExternalLink className="h-3 w-3" />
                    </a>
                  )}
                </li>
              );
            })}
          </ul>
        )}

        {response && hits.length === 0 && (
          <p className="text-xs text-muted-foreground">
            {copy.noHits}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
