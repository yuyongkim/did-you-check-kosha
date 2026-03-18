"use client";

import Link from "next/link";
import { ArrowRight, BookOpenText, Info } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { NAV_ITEMS } from "@/lib/navigation";
import { calculationStatusLabel } from "@/lib/ui-labels";
import { useWorkbenchStore } from "@/store/workbench-store";
import { cn } from "@/lib/utils";

function statusBadgeVariant(status: "success" | "error" | "blocked" | undefined): "ok" | "error" | "blocked" | "neutral" {
  if (!status) return "neutral";
  if (status === "success") return "ok";
  if (status === "blocked") return "blocked";
  return "error";
}

export function Sidebar() {
  const { language, basePath, localizedHref } = useUiLanguage();
  const results = useWorkbenchStore((state) => state.resultByDiscipline);

  const koLabelMap: Record<string, string> = {
    Piping: "배관",
    "Static Equipment": "정기기",
    Rotating: "회전기기",
    Electrical: "전기",
    Instrumentation: "계장",
    "Steel Structure": "철골구조",
    "Civil Concrete": "토목콘크리트",
  };

  const copy = language === "ko"
    ? {
        navigation: "내비게이션",
        workbench: "EPC 워크벤치",
        helper: "공종을 선택해 계산 및 검증 화면을 엽니다.",
        idle: "대기",
        glossary: "용어집 / 코드 가이드",
        calcGuide: "무엇을 계산하나",
      }
    : {
        navigation: "Navigation",
        workbench: "EPC Workbench",
        helper: "Open a discipline to run checks and verify standards.",
        idle: "IDLE",
        glossary: "Glossary / Code Guide",
        calcGuide: "What This Calculates",
      };

  return (
    <aside className="sticky top-[60px] flex h-[calc(100vh-60px)] w-full flex-col gap-3 border-r border-border/80 bg-muted/35 p-3">
      <div className="rounded-[8px] border border-border/90 bg-card p-3 shadow-panel">
        <p className="text-[10px] font-semibold uppercase tracking-[0.14em] text-muted-foreground">{copy.navigation}</p>
        <p className="mt-1 text-sm font-semibold text-secondary">{copy.workbench}</p>
        <p className="mt-1 text-[11px] text-muted-foreground">{copy.helper}</p>
      </div>

      <nav className="flex flex-1 flex-col gap-2 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const active = basePath === item.href;
          const status = results[item.discipline]?.status;
          return (
            <Link
              key={item.href}
              href={localizedHref(item.href)}
              className={cn(
                "group cursor-pointer rounded-[8px] border px-3 py-2 text-sm font-medium transition-colors",
                active
                  ? "border-primary/90 bg-primary text-accent-foreground shadow-[inset_3px_0_0_0_rgba(255,255,255,0.4)]"
                  : "border-border/80 bg-card/90 text-foreground hover:border-primary/45 hover:bg-primary/10",
              )}
            >
              <div className="flex items-center justify-between gap-2">
                <div className="flex min-w-0 items-center gap-2">
                  <span
                    className={cn(
                      "inline-flex h-6 w-6 items-center justify-center rounded-[6px] border text-[10px] font-bold tracking-wide",
                      active ? "border-white/30 bg-white/15 text-white" : "border-border bg-muted text-secondary",
                    )}
                  >
                    {item.tag}
                  </span>
                  <span className="truncate">{language === "ko" ? (koLabelMap[item.label] ?? item.label) : item.label}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Badge variant={statusBadgeVariant(status)}>
                    {status ? calculationStatusLabel(status, language) : copy.idle}
                  </Badge>
                  <ArrowRight className={cn("h-3.5 w-3.5 transition-opacity", active ? "opacity-100" : "opacity-40 group-hover:opacity-100")} />
                </div>
              </div>
            </Link>
          );
        })}
      </nav>
      <div className="space-y-2">
        <Link
          href={localizedHref("/glossary")}
          className="inline-flex w-full items-center justify-between rounded-[8px] border border-border/90 bg-card px-3 py-2 text-sm font-medium text-foreground transition-colors hover:border-primary/60 hover:bg-primary/10"
        >
          <span className="inline-flex items-center gap-2">
            <BookOpenText className="h-4 w-4 text-primary" />
            {copy.glossary}
          </span>
          <ArrowRight className="h-3.5 w-3.5" />
        </Link>
        <Link
          href={localizedHref("/calculation-guide")}
          className="inline-flex w-full items-center justify-between rounded-[8px] border border-primary/45 bg-primary/10 px-3 py-2 text-sm font-semibold text-primary transition-colors hover:bg-primary hover:text-accent-foreground"
        >
          <span className="inline-flex items-center gap-2">
            <Info className="h-4 w-4" />
            {copy.calcGuide}
          </span>
          <ArrowRight className="h-3.5 w-3.5" />
        </Link>
      </div>
    </aside>
  );
}
