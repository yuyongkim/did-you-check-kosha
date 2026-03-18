import { ShieldAlert } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { getFlagMessage } from "@/lib/flag-taxonomy";
import { CalculationResponse } from "@/lib/types";

export function BlockedBanner({ result }: { result: CalculationResponse | null }) {
  const { language } = useUiLanguage();
  const copy = language === "ko"
    ? {
        title: "차단 출력",
        body: "치명적 레드 플래그가 감지되었습니다. 사람 검토 없이 이 결과를 배포하지 마십시오.",
      }
    : {
        title: "Blocked Output",
        body: "Critical red flags were detected. Do not release this result without human review.",
      };

  if (!result || result.status !== "blocked") return null;
  const causes = result.flags.red_flags.slice(0, 3);

  return (
    <Card className="border-danger/50 bg-danger/10">
      <CardContent className="flex items-start gap-3 py-3">
        <ShieldAlert className="mt-0.5 h-5 w-5 text-danger" />
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-danger">{copy.title}</p>
          <p className="mt-1 text-sm text-foreground">{copy.body}</p>
          {causes.length > 0 && (
            <ul className="mt-2 space-y-1">
              {causes.map((cause) => (
                <li key={cause} className="rounded-[6px] border border-danger/30 bg-danger/10 px-2 py-1 text-xs text-danger">
                  <p className="font-semibold">{cause}</p>
                  <p className="text-[11px] text-foreground">{getFlagMessage(cause, language)}</p>
                </li>
              ))}
            </ul>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
