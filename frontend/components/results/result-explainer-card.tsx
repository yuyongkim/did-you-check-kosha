"use client";

import { useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { CalculationResponse } from "@/lib/types";

function topMetrics(result: CalculationResponse): string[] {
  return Object.entries(result.results)
    .slice(0, 3)
    .map(([key, value]) => `${key}: ${String(value)}`);
}

export function ResultExplainerCard({
  result,
  defaultSimple,
}: {
  result: CalculationResponse | null;
  defaultSimple?: boolean;
}) {
  const { language } = useUiLanguage();
  const [simpleMode, setSimpleMode] = useState(defaultSimple ?? true);

  const copy = language === "ko"
    ? {
        title: "결과 해석",
        noData: "계산 결과가 없습니다. 먼저 계산을 실행하세요.",
        simple: "쉬운 설명",
        expert: "엔지니어 설명",
        overall: "종합 판단",
      }
    : {
        title: "Result Interpretation",
        noData: "No result yet. Run a calculation first.",
        simple: "Simple",
        expert: "Engineer",
        overall: "Overall",
      };

  const summaryText = useMemo(() => {
    if (!result) return copy.noData;
    const metrics = topMetrics(result).join(" | ");
    const blocked = result.status === "blocked" || result.flags.red_flags.length > 0;

    if (simpleMode) {
      if (language === "ko") {
        return blocked
          ? `위험 신호가 감지되어 즉시 조치가 필요합니다. 핵심 수치: ${metrics}`
          : `현재 조건에서는 운전 가능성이 높습니다. 핵심 수치: ${metrics}`;
      }
      return blocked
        ? `Critical risk signals detected. Immediate action is recommended. Key values: ${metrics}`
        : `Current condition looks operable. Key values: ${metrics}`;
    }

    if (language === "ko") {
      return `상태=${result.status}, 신뢰도=${result.verification.confidence}, Red=${result.flags.red_flags.length}, Warn=${result.flags.warnings.length}. 핵심 수치: ${metrics}`;
    }
    return `Status=${result.status}, Confidence=${result.verification.confidence}, Red=${result.flags.red_flags.length}, Warn=${result.flags.warnings.length}. Key values: ${metrics}`;
  }, [copy.noData, language, result, simpleMode]);

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between gap-2">
        <CardTitle>{copy.title}</CardTitle>
        <div className="flex gap-1">
          <Button variant={simpleMode ? "default" : "outline"} className="h-8 px-2 text-xs" onClick={() => setSimpleMode(true)}>
            {copy.simple}
          </Button>
          <Button variant={simpleMode ? "outline" : "default"} className="h-8 px-2 text-xs" onClick={() => setSimpleMode(false)}>
            {copy.expert}
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-xs uppercase tracking-wide text-muted-foreground">{copy.overall}</p>
        <p className="mt-1 text-sm text-foreground">{summaryText}</p>
      </CardContent>
    </Card>
  );
}
