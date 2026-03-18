"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { TermHelp } from "@/components/ui/term-help";
import { getTermLabel } from "@/lib/glossary";
import { CalculationResponse } from "@/lib/types";
import { calculationStatusLabel, confidenceLabel, disciplineLabel } from "@/lib/ui-labels";

function statusVariant(status: CalculationResponse["status"]) {
  if (status === "blocked") return "blocked" as const;
  if (status === "error") return "error" as const;
  return "ok" as const;
}

const METRIC_LABEL_KO: Record<string, string> = {
  t_min_mm: "최소 요구두께",
  cr_selected_mm_per_year: "선정 부식률",
  remaining_life_years: "잔여수명",
  inspection_interval_years: "검사 주기",
  t_required_shell_mm: "쉘 요구두께",
  external_pressure_utilization: "외압 사용률",
  nozzle_reinforcement_index: "노즐 보강 지수",
  adjusted_vibration_limit_mm_per_s: "보정 진동한계",
  mechanical_integrity_index: "기계 무결성 지수",
  process_stability_index: "공정 안정성 지수",
  protection_readiness_index: "보호 준비도 지수",
  arc_flash_energy_cal_cm2: "아크플래시 에너지",
  fault_current_ka: "고장전류",
  breaker_interrupt_rating_ka: "차단기 정격",
  voltage_drop_percent: "전압강하",
  pfdavg: "평균 수요고장확률",
  sil_achieved: "달성 SIL",
  predicted_drift_pct: "예측 드리프트",
  calibration_interval_optimal_days: "최적 교정 주기",
  dc_ratio: "수요/용량 비",
  lambda_c: "무차원 세장비",
  phi_pn_kn: "설계 강도(phi*Pn)",
  deflection_mm: "처짐",
  carbonation_depth_mm: "탄산화 깊이",
  years_to_corrosion_init: "부식개시까지 기간",
  substantial_damage: "중대 손상 여부",
  hoop_stress_screening_mpa: "후프응력 스크리닝",
  hoop_stress_ratio: "후프응력 사용률",
  hydrotest_pressure_mpa: "수압시험 압력",
  ffs_screening_level: "FFS 스크리닝 등급",
  repair_scope_screening: "보수 범위 스크리닝",
  monitoring_escalation: "모니터링 단계",
  maintenance_urgency: "정비 긴급도",
  breaker_coordination_margin: "차단기 협조 여유",
  load_utilization: "부하 사용률",
  proof_test_adequacy: "증명시험 적정성",
  calibration_health: "교정 건전성",
  reinforcement_need: "보강 필요도",
  connection_status: "접합부 상태",
  repair_priority: "보수 우선순위",
  consequence_category: "결과 범주",
};

function metricLabel(language: "en" | "ko", key: string): string {
  if (language === "ko" && METRIC_LABEL_KO[key]) return METRIC_LABEL_KO[key];
  return getTermLabel(key);
}

const ENUM_BADGE_VARIANT: Record<string, "ok" | "warning" | "blocked" | "neutral"> = {
  // FFS / repair
  LEVEL0_FIT_FOR_SERVICE: "ok",
  LEVEL1_MONITOR_CLOSELY: "warning",
  LEVEL2_ENGINEERING_REVIEW: "warning",
  LEVEL3_DETAILED_ASSESSMENT_REQUIRED: "blocked",
  NO_REPAIR_ACTION: "ok",
  CONSIDER_WELD_OVERLAY_OR_COATING: "neutral",
  EVALUATE_REPAIR_FEASIBILITY: "warning",
  REPAIR_OR_REPLACE: "blocked",
  // monitoring / urgency
  QUARTERLY_ROUTE: "ok",
  MONTHLY_ROUTE: "ok",
  WEEKLY_ROUTE: "warning",
  CONTINUOUS_ONLINE: "blocked",
  ROUTINE: "ok",
  PLANNED_TURNAROUND: "ok",
  NEXT_AVAILABLE_WINDOW: "warning",
  IMMEDIATE_SHUTDOWN_REVIEW: "blocked",
  // electrical
  LIGHTLY_LOADED: "ok",
  MODERATELY_LOADED: "neutral",
  HEAVILY_LOADED: "blocked",
  // instrumentation
  ADEQUATE: "ok",
  MARGINAL: "warning",
  INADEQUATE: "blocked",
  HEALTHY: "ok",
  WATCH: "neutral",
  AT_RISK: "warning",
  EXCEEDED: "blocked",
  // steel
  NO_ACTION: "ok",
  MONITOR_AND_EVALUATE: "neutral",
  REINFORCEMENT_RECOMMENDED: "warning",
  REPLACEMENT_RECOMMENDED: "blocked",
  ACCEPTABLE: "ok",
  REVIEW_CONNECTION_ADEQUACY: "warning",
  FAILED_REPAIR_REQUIRED: "blocked",
  // civil
  PRIORITY_4_ROUTINE_MAINTENANCE: "ok",
  PRIORITY_3_PLANNED_REPAIR: "neutral",
  PRIORITY_2_NEXT_SHUTDOWN: "warning",
  PRIORITY_1_IMMEDIATE: "blocked",
  LOW_CONSEQUENCE: "ok",
  MEDIUM_CONSEQUENCE: "warning",
  HIGH_CONSEQUENCE: "blocked",
};

function isEnumMetric(key: string): boolean {
  return [
    "ffs_screening_level", "repair_scope_screening",
    "monitoring_escalation", "maintenance_urgency",
    "load_utilization", "proof_test_adequacy", "calibration_health",
    "reinforcement_need", "connection_status",
    "repair_priority", "consequence_category",
  ].includes(key);
}

export function ResultSummaryCard({
  result,
  metricKeys,
}: {
  result: CalculationResponse | null;
  metricKeys: string[];
}) {
  const { language } = useUiLanguage();
  const copy = language === "ko"
    ? {
        title: "계산 요약",
        idle: "대기",
        empty: "계산 실행 후 요약 지표가 표시됩니다.",
        confidence: "신뢰도",
        execution: "실행시간",
        references: "참조 수",
        discipline: "공종",
        calcType: "계산 타입",
      }
    : {
        title: "Calculation Summary",
        idle: "IDLE",
        empty: "Run a calculation to see summary metrics.",
        confidence: "confidence",
        execution: "execution",
        references: "references",
        discipline: "discipline",
        calcType: "calculation type",
      };

  return (
    <Card className="animate-fadeUp">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>{copy.title}</CardTitle>
        <Badge variant={result ? statusVariant(result.status) : "neutral"}>
          {result ? calculationStatusLabel(result.status, language) : copy.idle}
        </Badge>
      </CardHeader>
      <CardContent>
        {!result && <p className="text-sm text-muted-foreground">{copy.empty}</p>}
        {result && (
          <>
            <div className="mb-3 grid gap-2 rounded-[6px] border border-border bg-muted p-3 text-xs text-muted-foreground sm:grid-cols-3">
              <p className="flex items-center gap-1">
                {copy.confidence}
                <TermHelp term="confidence" />
                <span className="font-data font-semibold text-foreground">
                  {confidenceLabel(result.verification.confidence, language)}
                </span>
              </p>
              <p className="flex items-center gap-1">
                {copy.execution}
                <TermHelp term="execution_time_sec" />
                <span className="font-data font-semibold text-foreground">{result.details.calculation_summary.execution_time_sec}s</span>
              </p>
              <p className="flex items-center gap-1">
                {copy.references}
                <TermHelp term="references" />
                <span className="font-data font-semibold text-foreground">{result.references.length}</span>
              </p>
            </div>
            <div className="grid gap-2 sm:grid-cols-2">
              {metricKeys.map((key) => {
                const raw = result.results[key];
                const isEnum = isEnumMetric(key);
                const strVal = String(raw ?? "-");
                const badgeVariant = isEnum ? (ENUM_BADGE_VARIANT[strVal] ?? "neutral") : undefined;
                const displayLabel = strVal.replace(/_/g, " ");
                const isHoopRatio = key === "hoop_stress_ratio";
                return (
                  <div key={key} className="rounded-[6px] border border-border bg-card p-3">
                    <p className="flex items-center gap-1 text-xs uppercase tracking-wide text-muted-foreground">
                      <span>{metricLabel(language, key)}</span>
                      <TermHelp term={key} fallbackLabel={metricLabel(language, key)} />
                    </p>
                    {isEnum ? (
                      <Badge variant={badgeVariant} className="mt-1 text-[11px]">{displayLabel}</Badge>
                    ) : (
                      <p className="font-data mt-1 text-lg font-semibold text-foreground">
                        {isHoopRatio && typeof raw === "number" ? `${(raw * 100).toFixed(1)}%` : strVal}
                        {key === "hoop_stress_screening_mpa" && raw != null ? " MPa" : ""}
                        {key === "hydrotest_pressure_mpa" && raw != null ? " MPa" : ""}
                        {key === "breaker_coordination_margin" && raw != null ? "x" : ""}
                      </p>
                    )}
                  </div>
                );
              })}
            </div>
            <div className="mt-3 text-xs text-muted-foreground">
              {copy.discipline}: {disciplineLabel(result.discipline, language)} | {copy.calcType}: {result.details.calculation_summary.calculation_type}
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}

