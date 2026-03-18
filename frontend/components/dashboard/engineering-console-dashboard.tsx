"use client";

import Link from "next/link";
import { AlertTriangle, ArrowRight, BookText, CheckCircle2, Clock3, Factory, Gavel, Layers3, ShieldCheck } from "lucide-react";

import { DisciplineOverviewCard } from "@/components/dashboard/discipline-overview-card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { NAV_ITEMS } from "@/lib/navigation";
import { Discipline, KoshaGuideReference, KoshaLawReference } from "@/lib/types";
import {
  calculationStatusLabel,
  confidenceLabel,
  disciplineLabel,
  healthLabel,
  verificationLayerName,
  verificationLayerStatusLabel,
} from "@/lib/ui-labels";
import { cn } from "@/lib/utils";
import { useWorkbenchStore } from "@/store/workbench-store";

type DisciplineHealth = "idle" | "safe" | "warning" | "critical";

interface DisciplineSnapshot {
  discipline: Discipline;
  href: string;
  code: string;
  title: string;
  health: DisciplineHealth;
  alerts: number;
  activeProjects: number;
  lastRunLabel: string;
  headline: string;
}

function toDayKey(date: Date): string {
  const year = String(date.getFullYear());
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function formatRelativeTime(timestamp: string | undefined, language: "en" | "ko"): string {
  if (!timestamp) return "-";
  const target = new Date(timestamp).getTime();
  if (Number.isNaN(target)) return "-";

  const minutes = Math.max(0, Math.floor((Date.now() - target) / 60000));
  if (minutes < 1) return language === "ko" ? "방금 전" : "just now";
  if (minutes < 60) return language === "ko" ? `${minutes}분 전` : `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return language === "ko" ? `${hours}시간 전` : `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return language === "ko" ? `${days}일 전` : `${days}d ago`;
}

function healthFrom(status?: "success" | "error" | "blocked", alerts = 0): DisciplineHealth {
  if (!status) return "idle";
  if (status === "blocked" || status === "error") return "critical";
  if (alerts > 0) return "warning";
  return "safe";
}

function layerState(passed: boolean, issueCount: number): "pass" | "warn" | "fail" {
  if (!passed) return "fail";
  if (issueCount > 0) return "warn";
  return "pass";
}

function statusBadgeVariant(state: "pass" | "warn" | "fail"): "ok" | "warning" | "blocked" {
  if (state === "pass") return "ok";
  if (state === "warn") return "warning";
  return "blocked";
}

function sourceVariant(source: "koshaguide_api" | "smartsearch_api" | "local_fallback"): "ok" | "warning" | "neutral" {
  if (source === "local_fallback") return "warning";
  return "ok";
}

function lawSourceVariant(source: "smartsearch_api" | "local_fallback"): "ok" | "warning" {
  if (source === "local_fallback") return "warning";
  return "ok";
}

export function EngineeringConsoleDashboard() {
  const { language, localizedHref } = useUiLanguage();
  const resultByDiscipline = useWorkbenchStore((state) => state.resultByDiscipline);
  const runHistory = useWorkbenchStore((state) => state.runHistory);
  const setWorkbenchMode = useWorkbenchStore((state) => state.setWorkbenchMode);

  const copy = language === "ko"
    ? {
        operationView: "운영 화면",
        navigator: "공종 네비게이터",
        navigatorDesc: "워크벤치별 상태/알림/최근 실행 정보를 표시합니다.",
        alerts: "알림",
        lastRun: "최근 실행",
        console: "엔지니어링 콘솔",
        title: "산업 설비 무결성 대시보드",
        subtitle: "ASME/API 계산 + KOSHA 지침/법령 매핑을 한 화면에서 제공합니다.",
        verification4: "4계층 검증",
        koshaMapped: "KOSHA 매핑 완료",
        koshaPending: "KOSHA 대기",
        activeAlerts: "활성 알림",
        noAlerts: "활성 알림 없음",
        activeAssets: "운영 자산",
        todayRuns: "오늘 실행",
        compliance: "준수율",
        avgResponse: "평균 응답",
        aiVerification: "AI 검증 상태",
        noRunYet: "아직 실행 이력이 없습니다. 공종 하나를 실행해 패널을 채우세요.",
        issuesDetected: "건의 이슈 감지",
        koshaGuides: "KOSHA 지침",
        noGuides: "매핑된 지침이 없습니다.",
        legalCompliance: "법령 준수",
        noLegal: "매핑된 법령이 없습니다.",
        latestExecution: "최신 실행",
        noExecution: "실행 이력이 없습니다.",
        discipline: "공종",
        projectAsset: "프로젝트/자산",
        headline: "요약",
        sourceLink: "원문 링크",
        legalText: "법령 원문",
        local: "로컬",
        operatingPrinciple: "운영 원칙: 고밀도 정보, 명시적 상태, 감사 가능한 근거.",
        trafficRule: "의사결정은 신호등 규칙(safe / warning / critical)으로 통일.",
        activeAlertCount: "활성 알림 수",
        openPiping: "배관 워크벤치 열기",
        openGlossary: "용어집 열기",
        whatCalculate: "무엇을 계산하나",
        runNew: "새 스크리닝 실행",
        roleStart: "역할별 시작",
        starter: "입문",
        practitioner: "실무",
        master: "마스터",
        noCalcRun: "아직 계산 실행이 없습니다.",
      }
    : {
        operationView: "Operation View",
        navigator: "Discipline Navigator",
        navigatorDesc: "Status + alerts + last execution snapshot per workbench.",
        alerts: "Alerts",
        lastRun: "Last Run",
        console: "Engineering Console",
        title: "Industrial Integrity Dashboard",
        subtitle: "ASME/API calculation engine with KOSHA guide and legal mapping for audit-ready output.",
        verification4: "4-Layer Verification",
        koshaMapped: "KOSHA Mapped",
        koshaPending: "KOSHA Pending",
        activeAlerts: "Active Alerts",
        noAlerts: "No Active Alerts",
        activeAssets: "Active Assets",
        todayRuns: "Today Runs",
        compliance: "Compliance",
        avgResponse: "Avg Response",
        aiVerification: "AI Verification Status",
        noRunYet: "No run yet. Execute one discipline to populate this panel.",
        issuesDetected: "issue(s) detected",
        koshaGuides: "KOSHA Guides",
        noGuides: "No mapped guides yet.",
        legalCompliance: "Legal Compliance",
        noLegal: "No legal mapping yet.",
        latestExecution: "Latest Execution",
        noExecution: "No execution history yet.",
        discipline: "Discipline",
        projectAsset: "Project/Asset",
        headline: "Headline",
        sourceLink: "source link",
        legalText: "legal text",
        local: "LOCAL",
        operatingPrinciple: "Operating principle: dense data, explicit status, audit-ready evidence.",
        trafficRule: "Use traffic-light semantics for release decisions (safe / warning / critical).",
        activeAlertCount: "Active alert count",
        openPiping: "Open Piping Workbench",
        openGlossary: "Open Glossary",
        whatCalculate: "What This Calculates",
        runNew: "Run New Screening",
        roleStart: "Start by Role",
        starter: "Beginner",
        practitioner: "Practitioner",
        master: "Master",
        noCalcRun: "No calculation run yet.",
      };

  const koLabelMap: Record<string, string> = {
    Piping: "배관",
    "Static Equipment": "정기기",
    Rotating: "회전기기",
    Electrical: "전기",
    Instrumentation: "계장",
    "Steel Structure": "철골구조",
    "Civil Concrete": "토목콘크리트",
  };

  const runByDiscipline = Object.fromEntries(
    NAV_ITEMS.map((item) => [
      item.discipline,
      runHistory.find((entry) => entry.discipline === item.discipline),
    ]),
  ) as Record<Discipline, (typeof runHistory)[number] | undefined>;

  const snapshots: DisciplineSnapshot[] = NAV_ITEMS.map((item) => {
    const result = resultByDiscipline[item.discipline];
    const alerts = (result?.flags.red_flags.length ?? 0) + (result?.flags.warnings.length ?? 0);
    const lastRun = runByDiscipline[item.discipline];
    const health = healthFrom(result?.status, alerts);
    const projectCount = new Set(
      runHistory.filter((entry) => entry.discipline === item.discipline).map((entry) => entry.projectId),
    ).size;

    return {
      discipline: item.discipline,
      href: localizedHref(item.href),
      code: item.tag,
      title: language === "ko" ? (koLabelMap[item.label] ?? item.label) : item.label,
      health,
      alerts,
      activeProjects: projectCount,
      lastRunLabel: formatRelativeTime(lastRun?.timestamp, language),
      headline: lastRun?.headline ?? copy.noCalcRun,
    };
  });

  const latestRun = runHistory[0];
  const latestResult = latestRun ? resultByDiscipline[latestRun.discipline] : undefined;
  const latestRegulatory = latestResult?.details.regulatory;
  const today = toDayKey(new Date());
  const todaysRuns = runHistory.filter((entry) => toDayKey(new Date(entry.timestamp)) === today).length;
  const avgResponseMs =
    runHistory.length > 0
      ? Math.round(runHistory.reduce((sum, entry) => sum + entry.elapsedMs, 0) / runHistory.length)
      : 0;

  const totalAlerts = snapshots.reduce((sum, item) => sum + item.alerts, 0);
  const activeProjects = new Set(runHistory.map((entry) => `${entry.projectId}:${entry.assetId}`)).size;

  const complianceStatuses = Object.values(resultByDiscipline)
    .map((result) => result?.details.regulatory?.compliance.overall_status)
    .filter((status): status is "pass" | "review" | "fail" | "unknown" => Boolean(status));
  const passCount = complianceStatuses.filter((status) => status === "pass").length;
  const complianceRate =
    complianceStatuses.length > 0 ? Math.round((passCount / complianceStatuses.length) * 1000) / 10 : null;

  const guideRows: KoshaGuideReference[] = latestRegulatory?.guides.slice(0, 3) ?? [];
  const lawRows: KoshaLawReference[] = latestRegulatory?.laws.slice(0, 3) ?? [];

  return (
    <main className="flex-1 p-4">
      <section className="grid gap-3 xl:grid-cols-[260px_minmax(0,1fr)_320px]">
        <aside className="space-y-3">
          <div className="rounded-[8px] border border-border/90 bg-card p-3 shadow-panel">
            <p className="text-[10px] font-semibold uppercase tracking-[0.14em] text-muted-foreground">{copy.operationView}</p>
            <p className="mt-1 text-sm font-semibold text-secondary">{copy.navigator}</p>
            <p className="mt-1 text-xs text-muted-foreground">{copy.navigatorDesc}</p>
            <div className="mt-2 space-y-1">
              <p className="text-[10px] uppercase tracking-[0.12em] text-muted-foreground">{copy.roleStart}</p>
              <div className="flex gap-1">
                <Button className="h-7 px-2 text-[11px]" variant="outline" onClick={() => setWorkbenchMode("beginner")}>{copy.starter}</Button>
                <Button className="h-7 px-2 text-[11px]" variant="outline" onClick={() => setWorkbenchMode("standard")}>{copy.practitioner}</Button>
                <Button className="h-7 px-2 text-[11px]" variant="outline" onClick={() => setWorkbenchMode("master")}>{copy.master}</Button>
              </div>
            </div>
          </div>

          <nav className="space-y-2">
            {snapshots.map((item) => (
              <Link
                key={item.discipline}
                href={item.href}
                className="block rounded-[8px] border border-border/85 bg-card p-3 shadow-panel transition-colors hover:border-primary/50"
              >
                <div className="flex items-center justify-between gap-2">
                  <div className="flex min-w-0 items-center gap-2">
                    <span className="font-data inline-flex h-6 w-8 items-center justify-center rounded-[6px] border border-border bg-muted text-[10px] font-semibold text-secondary">
                      {item.code}
                    </span>
                    <p className="truncate text-sm font-medium text-foreground">{item.title}</p>
                  </div>
                  <Badge
                    variant={
                      item.health === "safe"
                        ? "ok"
                        : item.health === "warning"
                          ? "warning"
                          : item.health === "critical"
                            ? "blocked"
                            : "neutral"
                    }
                  >
                    {healthLabel(item.health, language)}
                  </Badge>
                </div>
                <div className="mt-2 grid grid-cols-2 gap-1 text-xs text-muted-foreground">
                  <span>{copy.alerts}</span>
                  <span className="font-data text-right text-foreground">{item.alerts}</span>
                  <span>{copy.lastRun}</span>
                  <span className="font-data text-right text-foreground">{item.lastRunLabel}</span>
                </div>
              </Link>
            ))}
          </nav>
        </aside>

        <section className="space-y-3">
          <div className="rounded-[8px] border border-border/90 bg-card p-4 shadow-panel">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="text-[10px] font-semibold uppercase tracking-[0.14em] text-muted-foreground">{copy.console}</p>
                <h1 className="mt-1 text-xl font-semibold tracking-tight text-secondary">{copy.title}</h1>
                <p className="mt-1 text-xs text-muted-foreground">
                  {copy.subtitle}
                </p>
              </div>
              <div className="flex flex-col items-end gap-1">
                <div className="flex flex-wrap justify-end gap-1">
                  <Badge variant="ok">{copy.verification4}</Badge>
                  <Badge variant={latestRegulatory ? "ok" : "neutral"}>
                    {latestRegulatory ? copy.koshaMapped : copy.koshaPending}
                  </Badge>
                  <Badge variant={totalAlerts > 0 ? "warning" : "ok"}>
                    {totalAlerts > 0 ? `${totalAlerts} ${copy.activeAlerts}` : copy.noAlerts}
                  </Badge>
                </div>
                <div className="flex flex-wrap justify-end gap-1">
                  <Link
                    href={localizedHref("/piping")}
                    className="inline-flex items-center gap-1 rounded-[6px] border border-primary/45 bg-primary/10 px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.08em] text-primary transition-colors hover:bg-primary hover:text-accent-foreground"
                  >
                    {copy.openPiping}
                    <ArrowRight className="h-3 w-3" />
                  </Link>
                  <Link
                    href={localizedHref("/calculation-guide")}
                    className="inline-flex items-center gap-1 rounded-[6px] border border-border/85 bg-card px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.08em] text-foreground transition-colors hover:border-primary/45 hover:bg-primary/10"
                  >
                    {copy.whatCalculate}
                    <ArrowRight className="h-3 w-3 text-primary" />
                  </Link>
                </div>
              </div>
            </div>

            <div className="mt-3 grid gap-2 md:grid-cols-4">
              <div className="rounded-[8px] border border-border/80 bg-muted/45 px-3 py-2">
                <p className="text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">{copy.activeAssets}</p>
                <p className="font-data mt-1 text-lg font-semibold text-secondary">{activeProjects}</p>
              </div>
              <div className="rounded-[8px] border border-border/80 bg-muted/45 px-3 py-2">
                <p className="text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">{copy.todayRuns}</p>
                <p className="font-data mt-1 text-lg font-semibold text-secondary">{todaysRuns}</p>
              </div>
              <div className="rounded-[8px] border border-border/80 bg-muted/45 px-3 py-2">
                <p className="text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">{copy.compliance}</p>
                <p className="font-data mt-1 text-lg font-semibold text-secondary">
                  {complianceRate === null ? "-" : `${complianceRate}%`}
                </p>
              </div>
              <div className="rounded-[8px] border border-border/80 bg-muted/45 px-3 py-2">
                <p className="text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">{copy.avgResponse}</p>
                <p className="font-data mt-1 text-lg font-semibold text-secondary">{avgResponseMs > 0 ? `${avgResponseMs} ms` : "-"}</p>
              </div>
            </div>
          </div>

          <div className="grid gap-3 md:grid-cols-2">
            {snapshots.map((item) => (
              <DisciplineOverviewCard
                key={item.discipline}
                href={item.href}
                code={item.code}
                title={item.title}
                status={item.health}
                activeProjects={item.activeProjects}
                alerts={item.alerts}
                lastRunLabel={item.lastRunLabel}
                headline={item.headline}
                language={language}
              />
            ))}
          </div>
        </section>

        <aside className="space-y-3 xl:sticky xl:top-[74px] xl:max-h-[calc(100vh-86px)] xl:overflow-y-auto">
          <div className="rounded-[8px] border border-border/90 bg-card p-3 shadow-panel">
            <p className="mb-2 inline-flex items-center gap-1 text-[10px] font-semibold uppercase tracking-[0.12em] text-primary">
              <Layers3 className="h-3.5 w-3.5" />
              {copy.aiVerification}
            </p>
            {!latestResult && <p className="text-xs text-muted-foreground">{copy.noRunYet}</p>}
            {latestResult && (
              <div className="space-y-2">
                {latestResult.verification.layers.map((layer) => {
                  const state = layerState(layer.passed, layer.issues.length);
                  return (
                    <div key={layer.layer} className="rounded-[6px] border border-border/80 bg-muted/45 p-2">
                      <div className="flex items-center justify-between gap-2">
                        <p className="truncate text-xs font-medium text-foreground">{verificationLayerName(layer.layer, language)}</p>
                        <Badge variant={statusBadgeVariant(state)}>{verificationLayerStatusLabel(state, language)}</Badge>
                      </div>
                      {layer.issues.length > 0 && (
                        <p className="mt-1 text-[11px] text-muted-foreground">{layer.issues.length} {copy.issuesDetected}</p>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <div className="rounded-[8px] border border-border/90 bg-card p-3 shadow-panel">
            <p className="mb-2 inline-flex items-center gap-1 text-[10px] font-semibold uppercase tracking-[0.12em] text-primary">
              <BookText className="h-3.5 w-3.5" />
              {copy.koshaGuides}
            </p>
            {guideRows.length === 0 && <p className="text-xs text-muted-foreground">{copy.noGuides}</p>}
            {guideRows.length > 0 && (
              <ul className="space-y-2">
                {guideRows.map((guide) => (
                  <li key={guide.id} className="rounded-[6px] border border-border/80 bg-muted/45 p-2">
                    <div className="flex items-center justify-between gap-2">
                      <p className="font-data text-xs font-semibold text-foreground">{guide.code}</p>
                      <Badge variant={sourceVariant(guide.source)}>
                        {guide.source === "local_fallback" ? copy.local : "API"}
                      </Badge>
                    </div>
                    <p className="mt-0.5 text-xs text-foreground">{guide.title}</p>
                    <p className="mt-1 line-clamp-2 text-[11px] text-muted-foreground">{guide.summary}</p>
                    {guide.pdf_url && (
                      <a
                        href={guide.pdf_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="mt-1 inline-flex items-center gap-1 text-xs font-semibold text-primary hover:underline"
                      >
                        {copy.sourceLink}
                        <ArrowRight className="h-3 w-3" />
                      </a>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="rounded-[8px] border border-border/90 bg-card p-3 shadow-panel">
            <p className="mb-2 inline-flex items-center gap-1 text-[10px] font-semibold uppercase tracking-[0.12em] text-primary">
              <Gavel className="h-3.5 w-3.5" />
              {copy.legalCompliance}
            </p>
            {lawRows.length === 0 && <p className="text-xs text-muted-foreground">{copy.noLegal}</p>}
            {lawRows.length > 0 && (
              <ul className="space-y-2">
                {lawRows.map((law) => (
                  <li key={law.id} className="rounded-[6px] border border-border/80 bg-muted/45 p-2">
                    <div className="flex items-center justify-between gap-2">
                      <p className="truncate text-xs font-semibold text-foreground">
                        {law.law_name} {law.article}
                      </p>
                      <Badge variant={lawSourceVariant(law.source)}>
                        {law.source === "local_fallback" ? copy.local : "API"}
                      </Badge>
                    </div>
                    <p className="mt-0.5 text-xs text-foreground">{law.title}</p>
                    <p className="mt-1 line-clamp-2 text-[11px] text-muted-foreground">{law.summary}</p>
                    {law.detail_url && (
                      <a
                        href={law.detail_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="mt-1 inline-flex items-center gap-1 text-xs font-semibold text-primary hover:underline"
                      >
                        {copy.legalText}
                        <ArrowRight className="h-3 w-3" />
                      </a>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="rounded-[8px] border border-border/90 bg-card p-3 shadow-panel">
            <p className="mb-2 inline-flex items-center gap-1 text-[10px] font-semibold uppercase tracking-[0.12em] text-primary">
              <Clock3 className="h-3.5 w-3.5" />
              {copy.latestExecution}
            </p>
            {!latestRun && <p className="text-xs text-muted-foreground">{copy.noExecution}</p>}
            {latestRun && (
              <div className="space-y-1 text-xs">
                <p className="text-muted-foreground">
                  {copy.discipline}: <span className="font-data text-foreground">{disciplineLabel(latestRun.discipline, language)}</span>
                </p>
                <p className="text-muted-foreground">
                  {copy.projectAsset}:{" "}
                  <span className="font-data text-foreground">{latestRun.projectId} / {latestRun.assetId}</span>
                </p>
                <p className="line-clamp-2 text-muted-foreground">{copy.headline}: {latestRun.headline}</p>
                <div className="flex flex-wrap gap-1 pt-1">
                  <Badge variant={latestRun.status === "success" ? "ok" : latestRun.status === "blocked" ? "blocked" : "error"}>
                    {calculationStatusLabel(latestRun.status, language)}
                  </Badge>
                  <Badge variant={latestRun.confidence === "high" ? "ok" : latestRun.confidence === "medium" ? "warning" : "blocked"}>
                    {confidenceLabel(latestRun.confidence, language)}
                  </Badge>
                </div>
              </div>
            )}
          </div>
        </aside>
      </section>

      <section className="mt-3 grid gap-2 rounded-[8px] border border-border/85 bg-card px-3 py-2 shadow-panel md:grid-cols-3">
        <div className="inline-flex items-center gap-2 text-xs text-muted-foreground">
          <Factory className="h-4 w-4 text-primary" />
          <span>
            {copy.operatingPrinciple}
          </span>
        </div>
        <div className="inline-flex items-center gap-2 text-xs text-muted-foreground">
          <ShieldCheck className="h-4 w-4 text-success" />
          <span>
            {copy.trafficRule}
          </span>
        </div>
        <div className="inline-flex items-center gap-2 text-xs text-muted-foreground">
          <AlertTriangle className={cn("h-4 w-4", totalAlerts > 0 ? "text-warning" : "text-muted-foreground")} />
          <span>
            {copy.activeAlertCount}: <span className="font-data text-foreground">{totalAlerts}</span>
          </span>
        </div>
      </section>

      <div className="mt-3 flex flex-wrap gap-2">
        <Link
          href={localizedHref("/piping")}
          className="inline-flex items-center gap-1 rounded-[6px] border border-primary/40 bg-primary/10 px-3 py-1.5 text-xs font-semibold uppercase tracking-[0.08em] text-primary transition-colors hover:bg-primary hover:text-accent-foreground"
        >
          {copy.openPiping}
          <ArrowRight className="h-3.5 w-3.5" />
        </Link>
        <Link
          href={localizedHref("/glossary")}
          className="inline-flex items-center gap-1 rounded-[6px] border border-border/90 bg-card px-3 py-1.5 text-xs font-semibold uppercase tracking-[0.08em] text-foreground transition-colors hover:border-primary/45 hover:bg-primary/10"
        >
          {copy.openGlossary}
          <ArrowRight className="h-3.5 w-3.5 text-primary" />
        </Link>
        <Link
          href={localizedHref("/calculation-guide")}
          className="inline-flex items-center gap-1 rounded-[6px] border border-border/90 bg-card px-3 py-1.5 text-xs font-semibold uppercase tracking-[0.08em] text-foreground transition-colors hover:border-primary/45 hover:bg-primary/10"
        >
          {copy.whatCalculate}
          <ArrowRight className="h-3.5 w-3.5 text-primary" />
        </Link>
        <Link
          href={localizedHref("/piping")}
          className="inline-flex items-center gap-1 rounded-[6px] border border-border/90 bg-card px-3 py-1.5 text-xs font-semibold uppercase tracking-[0.08em] text-foreground transition-colors hover:border-primary/45 hover:bg-primary/10"
        >
          <CheckCircle2 className="h-3.5 w-3.5 text-success" />
          {copy.runNew}
        </Link>
      </div>
    </main>
  );
}
