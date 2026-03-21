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
    <aside className="sticky top-[60px] flex h-[calc(100vh-60px)] w-full flex-col gap-3 border-r border-border/60 bg-muted/25 p-3 backdrop-blur-sm">
      {/* Header card with glass effect */}
      <div className="rounded-2xl border border-border/60 bg-card/70 p-4 shadow-panel backdrop-blur-sm">
        <p className="section-kicker">{copy.navigation}</p>
        <p className="mt-1.5 text-sm font-semibold text-secondary">{copy.workbench}</p>
        <p className="mt-1 text-[11px] leading-relaxed text-muted-foreground">{copy.helper}</p>
      </div>

      {/* Nav items */}
      <nav className="flex flex-1 flex-col gap-1.5 overflow-y-auto scrollbar-thin pr-0.5">
        {NAV_ITEMS.map((item) => {
          const active = basePath === item.href;
          const status = results[item.discipline]?.status;
          return (
            <Link
              key={item.href}
              href={localizedHref(item.href)}
              className={cn(
                "group relative flex cursor-pointer items-center justify-between gap-2 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-[180ms] ease-[cubic-bezier(0.2,0.8,0.2,1)]",
                active
                  ? "border border-primary/80 bg-primary text-accent-foreground shadow-[0_2px_12px_hsl(var(--primary)/0.25)]"
                  : "border border-transparent text-foreground hover:border-border/60 hover:bg-card/70 hover:shadow-panel",
              )}
            >
              <div className="flex min-w-0 items-center gap-2.5">
                <span
                  className={cn(
                    "inline-flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg text-[10px] font-bold tracking-wide transition-colors duration-150",
                    active
                      ? "bg-white/20 text-white"
                      : "bg-muted/80 text-secondary group-hover:bg-primary/10 group-hover:text-primary",
                  )}
                >
                  {item.tag}
                </span>
                <span className="truncate">{language === "ko" ? (koLabelMap[item.label] ?? item.label) : item.label}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Badge variant={statusBadgeVariant(status)}>
                  {status ? calculationStatusLabel(status, language) : copy.idle}
                </Badge>
                <ArrowRight
                  className={cn(
                    "h-3.5 w-3.5 transition-all duration-150",
                    active
                      ? "translate-x-0 opacity-100"
                      : "-translate-x-1 opacity-0 group-hover:translate-x-0 group-hover:opacity-60",
                  )}
                />
              </div>
            </Link>
          );
        })}
      </nav>

      {/* Bottom action links */}
      <div className="space-y-1.5">
        <Link
          href={localizedHref("/glossary")}
          className="group inline-flex w-full items-center justify-between rounded-xl border border-border/60 bg-card/60 px-3 py-2.5 text-sm font-medium text-foreground backdrop-blur-sm transition-all duration-[180ms] ease-[cubic-bezier(0.2,0.8,0.2,1)] hover:border-primary/40 hover:bg-card/80 hover:shadow-panel"
        >
          <span className="inline-flex items-center gap-2.5">
            <BookOpenText className="h-4 w-4 text-primary transition-transform duration-150 group-hover:scale-110" />
            {copy.glossary}
          </span>
          <ArrowRight className="h-3.5 w-3.5 opacity-40 transition-all duration-150 group-hover:translate-x-0.5 group-hover:opacity-80" />
        </Link>
        <Link
          href={localizedHref("/calculation-guide")}
          className="group inline-flex w-full items-center justify-between rounded-xl border border-primary/30 bg-primary/8 px-3 py-2.5 text-sm font-semibold text-primary transition-all duration-[180ms] ease-[cubic-bezier(0.2,0.8,0.2,1)] hover:bg-primary hover:text-accent-foreground hover:shadow-[0_2px_12px_hsl(var(--primary)/0.2)]"
        >
          <span className="inline-flex items-center gap-2.5">
            <Info className="h-4 w-4 transition-transform duration-150 group-hover:scale-110" />
            {copy.calcGuide}
          </span>
          <ArrowRight className="h-3.5 w-3.5 opacity-60 transition-all duration-150 group-hover:translate-x-0.5 group-hover:opacity-100" />
        </Link>
      </div>
    </aside>
  );
}
