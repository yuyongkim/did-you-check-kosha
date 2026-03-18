"use client";

import { type ReactNode, useEffect, useState } from "react";
import { FileText, ShieldCheck, Target } from "lucide-react";

import { DisciplineForm } from "@/components/forms/discipline-form";
import { ThreePaneLayout } from "@/components/layout/three-pane-layout";
import { BlockedBanner } from "@/components/results/blocked-banner";
import { CalculationTraceCard } from "@/components/results/calculation-trace-card";
import { ResultSummaryCard } from "@/components/results/result-summary-card";
import { ResultExplainerCard } from "@/components/results/result-explainer-card";
import { RunHistoryPanel } from "@/components/results/run-history-panel";
import { VisualEngineeringPanel } from "@/components/visualization/visual-engineering-panel";
import { CrossDisciplineImpactMapCard } from "@/components/visualization/cross-discipline-impact-map-card";
import { TimeSeriesThresholdCard } from "@/components/visualization/time-series-threshold-card";
import { GuidedRunCard } from "@/components/workbench/guided-run-card";
import { MasterToolsCard } from "@/components/workbench/master-tools-card";
import { FlagsPanel } from "@/components/verification/flags-panel";
import { LocalRagPanel } from "@/components/verification/local-rag-panel";
import { RegulatoryCompliancePanel } from "@/components/verification/regulatory-compliance-panel";
import { StandardsReferencePanel } from "@/components/verification/standards-reference-panel";
import { VerificationPanel } from "@/components/verification/verification-panel";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useCalculation } from "@/hooks/useCalculation";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { Discipline, DisciplineConfig } from "@/lib/types";
import { recommendationPriorityLabel, recommendationTimelineLabel } from "@/lib/ui-labels";
import { useWorkbenchStore } from "@/store/workbench-store";

const HERO_NOTES: Record<string, { focus: string; checks: string; output: string }> = {
  piping: {
    focus: "Corrosion-driven remaining life and inspection interval",
    checks: "t_min, corrosion rate, RL, chloride and material-temperature limits",
    output: "Actionable inspection and replacement recommendations",
  },
  vessel: {
    focus: "Shell/head/nozzle thickness integrity",
    checks: "required thickness, margin, localized thinning indicators",
    output: "Integrity status with reinforcement guidance",
  },
  rotating: {
    focus: "Machine x driver x criticality integrity management",
    checks: "Adjusted vibration limit, API 670 readiness, surge/NPSH/steam-state risk",
    output: "Condition status with risk-ranked monitoring cadence",
  },
  electrical: {
    focus: "Power safety and reliability",
    checks: "HI, arc-flash, voltage drop, fault-current margins",
    output: "Safety-zone and mitigation actions",
  },
  instrumentation: {
    focus: "SIL integrity and drift behavior",
    checks: "PFDavg, drift trend, tolerance crossing risk",
    output: "Calibration and SIS action guidance",
  },
  steel: {
    focus: "D/C ratio and serviceability",
    checks: "utilization, section loss, deflection screening",
    output: "Structural action priority",
  },
  civil: {
    focus: "Concrete durability and damage class",
    checks: "carbonation, crack/spalling, D/C and settlement context",
    output: "Repair urgency and monitoring plan",
  },
};

const HERO_NOTES_KO: Record<string, { focus: string; checks: string; output: string }> = {
  piping: {
    focus: "부식 기반 잔여수명 및 검사주기 산정",
    checks: "t_min, 부식률, RL, 염소농도, 재질-온도 제한",
    output: "검사/교체 실행 권고안",
  },
  vessel: {
    focus: "쉘/헤드/노즐 두께 건전성",
    checks: "요구두께, 여유도, 국부 감육 지표",
    output: "건전성 상태 및 보강 권고",
  },
  rotating: {
    focus: "기계-구동기-중요도 기반 무결성 관리",
    checks: "보정 진동한계, API 670 적합성, 서지/NPSH/스팀상태 위험",
    output: "위험 순위 기반 모니터링 주기",
  },
  electrical: {
    focus: "전력 안전 및 신뢰성",
    checks: "HI, 아크플래시, 전압강하, 고장전류 여유",
    output: "안전 구역 및 저감 조치",
  },
  instrumentation: {
    focus: "SIL 무결성 및 드리프트 거동",
    checks: "PFDavg, 드리프트 추세, 허용편차 초과 위험",
    output: "교정/SIS 조치 가이드",
  },
  steel: {
    focus: "D/C 비율 및 사용성",
    checks: "사용률, 단면손실, 처짐 스크리닝",
    output: "구조 조치 우선순위",
  },
  civil: {
    focus: "콘크리트 내구성 및 손상 등급",
    checks: "탄산화, 균열/박락, D/C 및 침하 맥락",
    output: "보수 긴급도 및 모니터링 계획",
  },
};

const DISCIPLINE_TITLE_KO: Record<Discipline, { title: string; subtitle: string }> = {
  piping: {
    title: "배관 건전성",
    subtitle: "ASME B31.3 / API 570 기반 두께, 부식률, 잔여수명 검증",
  },
  vessel: {
    title: "정기기 건전성",
    subtitle: "쉘/헤드/노즐 두께 여유 및 감육 상태 검증",
  },
  rotating: {
    title: "회전기기 건전성",
    subtitle: "진동/보호계통/공정안정성 기반 상태 평가",
  },
  electrical: {
    title: "전기 건전성",
    subtitle: "전력안전, 아크플래시, 고장전류 여유 검증",
  },
  instrumentation: {
    title: "계장 건전성",
    subtitle: "SIL, 드리프트, 허용편차 기반 계장 신뢰성 검증",
  },
  steel: {
    title: "철골구조 건전성",
    subtitle: "D/C 비율, 단면손실, 처짐 기반 구조 상태 평가",
  },
  civil: {
    title: "토목콘크리트 건전성",
    subtitle: "내구성/손상등급/침하 맥락 기반 보수 우선순위 평가",
  },
};

const DISCIPLINE_CODE_LABEL_KO: Record<Discipline, string> = {
  piping: "배관",
  vessel: "정기기",
  rotating: "회전기기",
  electrical: "전기",
  instrumentation: "계장",
  steel: "철골",
  civil: "토목",
};

export function DisciplineWorkbench({ config }: { config: DisciplineConfig }) {
  const { requestState, error, result, runCalculation } = useCalculation(config.discipline);
  const { language } = useUiLanguage();
  const setActiveDiscipline = useWorkbenchStore((state) => state.setActiveDiscipline);
  const workbenchMode = useWorkbenchStore((state) => state.workbenchMode);
  const [previewInput, setPreviewInput] = useState<Record<string, unknown>>(config.sampleInput);

  const copy = language === "ko"
    ? {
        focus: "핵심 목적",
        checks: "주요 검증",
        output: "출력",
        inputSnapshot: "입력 스냅샷",
        recommendations: "권고사항",
        recommendationsEmpty: "실행 후 권고사항이 표시됩니다.",
        requestError: "요청 오류",
      }
    : {
        focus: "Focus",
        checks: "Core Checks",
        output: "Output",
        inputSnapshot: "Input Snapshot",
        recommendations: "Recommendations",
        recommendationsEmpty: "Recommendations appear after a run.",
        requestError: "Request Error",
      };

  const hero = language === "ko" ? HERO_NOTES_KO[config.discipline] : HERO_NOTES[config.discipline];
  const checkItems = hero.checks
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
  const heroCards: Array<{
    key: "focus" | "checks" | "output";
    label: string;
    icon: (props: { className?: string }) => ReactNode;
    accentClass: string;
    content: ReactNode;
  }> = [
    {
      key: "focus",
      label: copy.focus,
      icon: Target,
      accentClass: "from-primary/85 to-primary/30",
      content: <p className="text-sm font-medium leading-6 text-foreground md:text-[15px]">{hero.focus}</p>,
    },
    {
      key: "checks",
      label: copy.checks,
      icon: ShieldCheck,
      accentClass: "from-warning/85 to-warning/30",
      content: (
        <div className="flex flex-wrap gap-1.5">
          {checkItems.map((item) => (
            <span
              key={item}
              className="rounded-full border border-border/85 bg-muted/65 px-2 py-1 text-[11px] font-semibold leading-4 text-foreground md:text-xs"
            >
              {item}
            </span>
          ))}
        </div>
      ),
    },
    {
      key: "output",
      label: copy.output,
      icon: FileText,
      accentClass: "from-accent/85 to-accent/30",
      content: <p className="text-sm font-medium leading-6 text-foreground md:text-[15px]">{hero.output}</p>,
    },
  ];
  const title = language === "ko" ? DISCIPLINE_TITLE_KO[config.discipline].title : config.title;
  const subtitle = language === "ko" ? DISCIPLINE_TITLE_KO[config.discipline].subtitle : config.subtitle;
  const disciplineCodeText = language === "ko" ? DISCIPLINE_CODE_LABEL_KO[config.discipline] : config.discipline.toUpperCase();

  useEffect(() => {
    setActiveDiscipline(config.discipline);
  }, [config.discipline, setActiveDiscipline]);

  useEffect(() => {
    setPreviewInput(config.sampleInput);
  }, [config.sampleInput]);

  return (
    <main className="flex-1">
      <section className="border-b border-border/85 bg-card/65 px-4 py-3 backdrop-blur-[1px]">
        <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-muted-foreground">[{config.shortLabel}] {disciplineCodeText}</p>
        <h1 className="title-display mt-1 text-2xl font-semibold tracking-tight text-secondary">{title}</h1>
        <p className="text-sm text-muted-foreground">{subtitle}</p>
        <div className="mt-3 grid gap-2 md:grid-cols-3">
          {heroCards.map((card) => {
            const Icon = card.icon;
            return (
              <article
                key={card.key}
                className="group relative overflow-hidden rounded-xl border border-border/80 bg-gradient-to-br from-card via-card to-muted/30 p-4 shadow-sm transition-colors hover:border-primary/35"
              >
                <span className={`absolute inset-x-0 top-0 h-[3px] bg-gradient-to-r ${card.accentClass}`} />
                <div className="mb-2 flex items-center gap-2">
                  <span className="inline-flex h-7 w-7 items-center justify-center rounded-[6px] border border-border/85 bg-muted/50 text-primary">
                    <Icon className="h-3.5 w-3.5" />
                  </span>
                  <p className="text-xs font-semibold uppercase tracking-[0.12em] text-primary">{card.label}</p>
                </div>
                {card.content}
              </article>
            );
          })}
        </div>
      </section>

      <ThreePaneLayout
        left={(
          <>
            <DisciplineForm
              discipline={config.discipline}
              title={title}
              fields={config.formFields}
              sampleInput={config.sampleInput}
              presets={config.presets}
              onValuesChange={setPreviewInput}
              onSubmit={async (payload) => {
                setPreviewInput(payload);
                await runCalculation(payload);
              }}
              submitting={requestState === "loading"}
            />
            {workbenchMode === "beginner" && (
              <GuidedRunCard fields={config.formFields} values={previewInput} result={result} />
            )}
            <RunHistoryPanel discipline={config.discipline} />
            <Card>
              <CardHeader>
                <CardTitle>{copy.inputSnapshot}</CardTitle>
              </CardHeader>
              <CardContent>
                <pre className="max-h-[240px] overflow-auto rounded-[6px] border border-border bg-muted p-2 text-xs text-muted-foreground">
                  {JSON.stringify(previewInput, null, 2)}
                </pre>
              </CardContent>
            </Card>
          </>
        )}
        center={(
          <>
            <BlockedBanner result={result} />
            <ResultSummaryCard result={result} metricKeys={config.primaryMetrics} />
            <ResultExplainerCard result={result} defaultSimple={workbenchMode === "beginner"} />
            <VisualEngineeringPanel discipline={config.discipline} result={result} previewInput={previewInput} />
            <TimeSeriesThresholdCard discipline={config.discipline} result={result} />
            <CrossDisciplineImpactMapCard />
            <CalculationTraceCard result={result} />
            {workbenchMode === "master" && (
              <MasterToolsCard
                discipline={config.discipline}
                fields={config.formFields}
                sampleInput={config.sampleInput}
                baseInput={previewInput}
                activeResult={result}
              />
            )}
            <Card>
              <CardHeader>
                <CardTitle>{copy.recommendations}</CardTitle>
              </CardHeader>
              <CardContent>
                {!result && <p className="text-sm text-muted-foreground">{copy.recommendationsEmpty}</p>}
                {result && (
                  <ul className="space-y-2">
                    {result.details.recommendations.map((rec, idx) => (
                      <li key={`${rec.action}-${idx}`} className="rounded-[6px] border border-border bg-card p-3">
                        <p className="text-xs uppercase tracking-wide text-muted-foreground">
                          {recommendationPriorityLabel(rec.priority, language)} / {recommendationTimelineLabel(rec.timeline, language)}
                        </p>
                        <p className="mt-1 text-sm font-medium text-foreground">{rec.action}</p>
                        <p className="text-sm text-muted-foreground">{rec.description}</p>
                      </li>
                    ))}
                  </ul>
                )}
              </CardContent>
            </Card>
            {error && (
              <Card>
                <CardHeader>
                  <CardTitle>{copy.requestError}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-danger">{error}</p>
                </CardContent>
              </Card>
            )}
          </>
        )}
        right={(
          <>
            <VerificationPanel result={result} />
            <RegulatoryCompliancePanel result={result} />
            <LocalRagPanel discipline={config.discipline} result={result} />
            <StandardsReferencePanel result={result} />
            <FlagsPanel result={result} />
          </>
        )}
      />
    </main>
  );
}
