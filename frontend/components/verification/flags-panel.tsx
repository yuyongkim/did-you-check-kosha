"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { getFlagMessage } from "@/lib/flag-taxonomy";
import { CalculationResponse } from "@/lib/types";

export function FlagsPanel({ result }: { result: CalculationResponse | null }) {
  const { language } = useUiLanguage();
  const reds = result?.flags.red_flags ?? [];
  const warns = result?.flags.warnings ?? [];
  const copy = language === "ko"
    ? {
        title: "플래그",
        red: "레드 플래그",
        warnings: "경고",
        none: "없음",
      }
    : {
        title: "Flags",
        red: "Red Flags",
        warnings: "Warnings",
        none: "None",
      };

  return (
    <Card className="animate-fadeUp">
      <CardHeader>
        <CardTitle>{copy.title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div>
          <p className="mb-1 text-xs uppercase tracking-wide text-danger">{copy.red}</p>
          {reds.length === 0 ? (
            <p className="text-sm text-muted-foreground">{copy.none}</p>
          ) : (
            <ul className="space-y-1">
              {reds.map((flag) => (
                <li key={flag} className="rounded-[6px] border border-danger/30 bg-danger/10 px-2 py-1">
                  <p className="text-sm font-semibold text-danger">{flag}</p>
                  <p className="text-xs text-foreground">{getFlagMessage(flag, language)}</p>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div>
          <p className="mb-1 text-xs uppercase tracking-wide text-warning">{copy.warnings}</p>
          {warns.length === 0 ? (
            <p className="text-sm text-muted-foreground">{copy.none}</p>
          ) : (
            <ul className="space-y-1">
              {warns.map((flag) => (
                <li key={flag} className="rounded-[6px] border border-warning/30 bg-warning/10 px-2 py-1">
                  <p className="text-sm font-semibold text-warning">{flag}</p>
                  <p className="text-xs text-foreground">{getFlagMessage(flag, language)}</p>
                </li>
              ))}
            </ul>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

