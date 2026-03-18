"use client";

import Link from "next/link";
import { ArrowRight, CircleAlert, Clock3, ShieldCheck } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

type DisciplineStatus = "idle" | "safe" | "warning" | "critical";

interface DisciplineOverviewCardProps {
  href: string;
  code: string;
  title: string;
  language: "en" | "ko";
  status: DisciplineStatus;
  activeProjects: number;
  alerts: number;
  lastRunLabel: string;
  headline: string;
}

const statusToken: Record<
  DisciplineStatus,
  {
    badge: "neutral" | "ok" | "warning" | "blocked";
    border: string;
    panel: string;
    label: string;
  }
> = {
  idle: {
    badge: "neutral",
    border: "border-border",
    panel: "bg-muted/45",
    label: "IDLE",
  },
  safe: {
    badge: "ok",
    border: "border-success/40",
    panel: "bg-success/10",
    label: "SAFE",
  },
  warning: {
    badge: "warning",
    border: "border-warning/40",
    panel: "bg-warning/10",
    label: "WARNING",
  },
  critical: {
    badge: "blocked",
    border: "border-danger/40",
    panel: "bg-danger/10",
    label: "CRITICAL",
  },
};

export function DisciplineOverviewCard({
  href,
  code,
  title,
  language,
  status,
  activeProjects,
  alerts,
  lastRunLabel,
  headline,
}: DisciplineOverviewCardProps) {
  const token = statusToken[status];
  const copy = language === "ko"
    ? {
        activeProjects: "운영 프로젝트",
        alerts: "알림",
        lastRun: "최근 실행",
        openWorkbench: "워크벤치 열기",
      }
    : {
        activeProjects: "Active Projects",
        alerts: "Alerts",
        lastRun: "Last Run",
        openWorkbench: "Open Workbench",
      };
  const statusLabel = language === "ko"
    ? (
        {
          IDLE: "대기",
          SAFE: "정상",
          WARNING: "주의",
          CRITICAL: "위험",
        } as const
      )[token.label]
    : token.label;

  return (
    <Link
      href={href}
      className={cn(
        "group rounded-[8px] border border-border/85 bg-card p-4 shadow-panel transition-colors hover:border-primary/55",
        token.border,
      )}
    >
      <div className="flex items-center justify-between gap-2">
        <div className="min-w-0">
          <p className="font-data text-[11px] font-semibold uppercase tracking-[0.1em] text-muted-foreground">{code}</p>
          <h3 className="truncate text-sm font-semibold text-secondary">{title}</h3>
        </div>
        <Badge variant={token.badge}>{statusLabel}</Badge>
      </div>

      <div className={cn("mt-3 rounded-[6px] border border-border/75 px-3 py-2", token.panel)}>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <p className="text-muted-foreground">{copy.activeProjects}</p>
          <p className="font-data text-right font-semibold text-foreground">{activeProjects}</p>
          <p className="inline-flex items-center gap-1 text-muted-foreground">
            <CircleAlert className="h-3 w-3" />
            {copy.alerts}
          </p>
          <p className="font-data text-right font-semibold text-foreground">{alerts}</p>
        </div>
      </div>

      <div className="mt-3 space-y-1 text-xs">
        <p className="inline-flex items-center gap-1 text-muted-foreground">
          <Clock3 className="h-3 w-3" />
          {copy.lastRun}: <span className="font-data text-foreground">{lastRunLabel}</span>
        </p>
        <p className="line-clamp-2 text-muted-foreground">{headline}</p>
      </div>

      <div className="mt-3 flex items-center justify-between border-t border-border/70 pt-2 text-xs font-semibold uppercase tracking-[0.08em] text-primary">
        <span className="inline-flex items-center gap-1">
          <ShieldCheck className="h-3.5 w-3.5" />
          {copy.openWorkbench}
        </span>
        <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
      </div>
    </Link>
  );
}
