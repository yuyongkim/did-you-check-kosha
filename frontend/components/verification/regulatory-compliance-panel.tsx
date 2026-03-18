"use client";

import { BookText, ExternalLink, Link2, Scale, ShieldCheck } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LawTextViewer } from "@/components/verification/law-text-viewer";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { CalculationResponse, RegulatoryStatus } from "@/lib/types";
import { regulatoryConfidenceLabel } from "@/lib/ui-labels";

function statusVariant(status: RegulatoryStatus): "ok" | "warning" | "blocked" | "neutral" {
  if (status === "pass") return "ok";
  if (status === "review") return "warning";
  if (status === "fail") return "blocked";
  return "neutral";
}

function statusLabel(status: RegulatoryStatus, language: "en" | "ko"): string {
  if (language === "ko") {
    if (status === "pass") return "통과";
    if (status === "review") return "검토";
    if (status === "fail") return "실패";
    return "미확인";
  }

  if (status === "pass") return "PASS";
  if (status === "review") return "REVIEW";
  if (status === "fail") return "FAIL";
  return "UNKNOWN";
}

export function RegulatoryCompliancePanel({ result }: { result: CalculationResponse | null }) {
  const { language } = useUiLanguage();
  const regulatory = result?.details.regulatory;
  const copy = language === "ko"
    ? {
        title: "KOSHA 규제 매핑",
        idle: "대기",
        empty: "계산 실행 후 KOSHA 지침/법령 매핑이 표시됩니다.",
        summary: "규제 매핑 요약",
        guides: "관련 기술지침",
        laws: "법적 근거",
        crosswalk: "ASME/API ↔ KR 교차 매핑",
        compliance: "준수 상태",
        legal: "법령",
        sourceLink: "원문 링크",
        legalText: "법령 원문",
        legalLink: "링크",
        globalRefs: "글로벌 표준",
        law: "법령",
        query: "검색어",
        updated: "업데이트",
        local: "로컬",
        koshaGuide: "KOSHA 지침",
      }
    : {
        title: "KOSHA Regulatory",
        idle: "IDLE",
        empty: "Run a calculation to populate KOSHA guide and legal mapping.",
        summary: "Regulatory mapping summary",
        guides: "Related Guides",
        laws: "Legal Basis",
        crosswalk: "ASME/API ↔ KR Crosswalk",
        compliance: "Compliance Status",
        legal: "Legal",
        sourceLink: "Open source link",
        legalText: "Open legal text",
        legalLink: "link",
        globalRefs: "Global refs",
        law: "Law",
        query: "query",
        updated: "updated",
        local: "LOCAL",
        koshaGuide: "KOSHA GUIDE",
      };

  return (
    <Card className="animate-fadeUp">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>{copy.title}</CardTitle>
        <Badge variant={regulatory ? statusVariant(regulatory.compliance.overall_status) : "neutral"}>
          {regulatory ? statusLabel(regulatory.compliance.overall_status, language) : copy.idle}
        </Badge>
      </CardHeader>
      <CardContent className="space-y-3">
        {!regulatory && (
          <p className="text-sm text-muted-foreground">{copy.empty}</p>
        )}

        {regulatory && (
          <>
            <div className="rounded-[6px] border border-border bg-muted px-2 py-1">
              <p className="text-xs text-muted-foreground">{copy.summary}</p>
              <p className="text-sm">{regulatory.compliance.summary}</p>
            </div>

            <div>
              <p className="mb-1 flex items-center gap-1 text-xs uppercase tracking-wide text-primary">
                <BookText className="h-3.5 w-3.5" /> {copy.guides}
              </p>
              <ul className="space-y-1">
                {regulatory.guides.map((guide) => (
                  <li key={guide.id} className="rounded-[6px] border border-border bg-card p-2">
                    <div className="flex items-center justify-between gap-2">
                      <p className="text-xs font-semibold text-foreground">{guide.code}</p>
                      <Badge variant={guide.source === "local_fallback" ? "warning" : "ok"}>
                        {guide.source === "local_fallback" ? copy.local : "API"}
                      </Badge>
                    </div>
                    <p className="mt-0.5 text-xs text-foreground/90">{guide.title}</p>
                    <p className="mt-0.5 text-xs text-muted-foreground">{guide.summary}</p>
                    {guide.pdf_url && (
                      <a
                        className="mt-1 inline-flex items-center gap-1 text-xs text-primary hover:underline"
                        href={guide.pdf_url}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        [{copy.sourceLink}] <ExternalLink className="h-3 w-3" />
                      </a>
                    )}
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <p className="mb-1 flex items-center gap-1 text-xs uppercase tracking-wide text-primary">
                <Scale className="h-3.5 w-3.5" /> {copy.laws}
              </p>
              <ul className="space-y-1">
                {regulatory.laws.map((law) => (
                  <li key={law.id} className="rounded-[6px] border border-border bg-card p-2">
                    <p className="text-xs font-semibold text-foreground">
                      {law.law_name} {law.article}
                    </p>
                    <p className="mt-0.5 text-xs text-foreground/90">{law.title}</p>
                    <p className="mt-0.5 text-xs text-muted-foreground">{law.summary}</p>
                    {law.source_text && (
                      <LawTextViewer text={law.source_text} language={language} />
                    )}
                    {law.detail_url && (
                      <a
                        className="mt-1 inline-flex items-center gap-1 text-xs text-primary hover:underline"
                        href={law.detail_url}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        [{copy.legalText} {copy.legalLink}] <ExternalLink className="h-3 w-3" />
                      </a>
                    )}
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <p className="mb-1 flex items-center gap-1 text-xs uppercase tracking-wide text-primary">
                <Link2 className="h-3.5 w-3.5" /> {copy.crosswalk}
              </p>
              <ul className="space-y-1">
                {(regulatory.crosswalk ?? []).map((item) => (
                  <li key={item.id} className="rounded-[6px] border border-border bg-card p-2">
                    <div className="flex items-center justify-between gap-2">
                      <p className="text-xs font-semibold text-foreground">{item.topic}</p>
                      <Badge
                        variant={
                          item.confidence === "high"
                            ? "ok"
                            : item.confidence === "medium"
                              ? "warning"
                              : "neutral"
                        }
                      >
                        {regulatoryConfidenceLabel(item.confidence, language)}
                      </Badge>
                    </div>
                    <p className="mt-0.5 text-xs text-muted-foreground">{item.korean_regulatory_summary}</p>
                    {item.global_references.length > 0 && (
                      <p className="mt-1 text-xs text-foreground/90">
                        {copy.globalRefs}: {item.global_references.join(" | ")}
                      </p>
                    )}
                    {item.matched_guides.length > 0 && (
                      <p className="mt-1 text-xs text-foreground/90">
                        KOSHA: {item.matched_guides.join(" | ")}
                      </p>
                    )}
                    {item.matched_laws.length > 0 && (
                      <p className="mt-1 text-xs text-foreground/90">
                        {copy.law}: {item.matched_laws.join(" | ")}
                      </p>
                    )}
                    {item.links.length > 0 && (
                      <div className="mt-1 flex flex-wrap gap-2">
                        {item.links.slice(0, 4).map((link) => (
                          <a
                            key={link.id}
                            className="inline-flex items-center gap-1 text-xs text-primary hover:underline"
                            href={link.url}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            [{link.label}] <ExternalLink className="h-3 w-3" />
                          </a>
                        ))}
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            </div>

            <div className="rounded-[6px] border border-border bg-card p-2">
              <p className="mb-1 flex items-center gap-1 text-xs uppercase tracking-wide text-primary">
                <ShieldCheck className="h-3.5 w-3.5" /> {copy.compliance}
              </p>
              <div className="flex flex-wrap gap-1">
                <Badge variant={statusVariant(regulatory.compliance.guide_status)}>
                  {copy.koshaGuide}: {statusLabel(regulatory.compliance.guide_status, language)}
                </Badge>
                <Badge variant={statusVariant(regulatory.compliance.legal_status)}>
                  {copy.legal}: {statusLabel(regulatory.compliance.legal_status, language)}
                </Badge>
              </div>
              {regulatory.compliance.notes.length > 0 && (
                <ul className="mt-2 space-y-1">
                  {regulatory.compliance.notes.map((note, index) => (
                    <li key={`${note}-${index}`} className="text-xs text-muted-foreground">
                      - {note}
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div className="rounded-[6px] border border-border bg-muted px-2 py-1">
              <p className="text-xs text-muted-foreground">
                {copy.query}: {regulatory.query_terms.join(", ")} | {copy.updated}:{" "}
                {new Date(regulatory.generated_at).toLocaleString(language === "ko" ? "ko-KR" : "en-US")}
              </p>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}
