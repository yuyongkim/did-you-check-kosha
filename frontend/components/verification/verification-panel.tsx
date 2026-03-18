"use client";

import { CheckCircle2, TriangleAlert, XCircle } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TermHelp } from "@/components/ui/term-help";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { CalculationResponse } from "@/lib/types";
import { verificationLayerName } from "@/lib/ui-labels";
import { useVerification } from "@/hooks/useVerification";

export function VerificationPanel({ result }: { result: CalculationResponse | null }) {
  const { language } = useUiLanguage();
  const { blocked, layerSummary } = useVerification(result);
  const copy = language === "ko"
    ? {
        title: "AI 검증",
        blocked: "차단",
        ready: "준비",
        empty: "아직 검증 실행이 없습니다.",
      }
    : {
        title: "AI Verification",
        blocked: "BLOCKED",
        ready: "READY",
        empty: "No verification run yet.",
      };

  return (
    <Card className="animate-fadeUp">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>{copy.title}</CardTitle>
        <Badge variant={blocked ? "blocked" : "ok"}>{blocked ? copy.blocked : copy.ready}</Badge>
      </CardHeader>
      <CardContent className="space-y-2">
        {layerSummary.length === 0 && <p className="text-sm text-muted-foreground">{copy.empty}</p>}
        {layerSummary.map((layer) => (
          <div key={layer.name} className="rounded-[6px] border border-border bg-card p-2">
            <div className="flex items-center justify-between gap-2">
              <p className="flex items-center gap-1 text-sm font-medium text-foreground">
                <span>{verificationLayerName(layer.name, language)}</span>
                <TermHelp term={layer.name} fallbackLabel={verificationLayerName(layer.name, language)} />
              </p>
              {layer.status === "pass" && <CheckCircle2 className="h-4 w-4 text-success" />}
              {layer.status === "warn" && <TriangleAlert className="h-4 w-4 text-warning" />}
              {layer.status === "fail" && <XCircle className="h-4 w-4 text-danger" />}
            </div>
            {layer.issues.length > 0 && (
              <ul className="mt-1 space-y-1">
                {layer.issues.map((issue) => (
                  <li key={issue.code} className="text-xs text-muted-foreground">
                    {issue.code}: {issue.message}
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

