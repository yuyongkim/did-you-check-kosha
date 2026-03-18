"use client";

import { Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { useUiLanguage } from "@/hooks/useUiLanguage";
import { CalculationResponse } from "@/lib/types";
import { resultValue, toNumber } from "@/components/visualization/utils";
import { VisualSectionCard } from "@/components/visualization/visual-section-card";
import { CHART_AXIS_LABEL_STYLE, CHART_AXIS_STROKE, CHART_TICK_STYLE, getChartTooltipProps } from "@/components/visualization/chart-theme";

type UiLanguage = "en" | "ko";

const INST_COPY: Record<UiLanguage, {
  sectionDrift: string;
  sectionSil: string;
  sectionCalGuide: string;
  sil34: string;
  sil2: string;
  sil1: string;
  target: string;
  achieved: string;
  predictedDrift: string;
  silCompliance: string;
  belowTarget: string;
  onTarget: string;
  note: string;
  proofTestAdequacy: string;
  calibrationHealth: string;
  axisElapsed: string;
  axisError: string;
}> = {
  en: {
    sectionDrift: "Drift Trend & Tolerance",
    sectionSil: "SIL Achievement Band",
    sectionCalGuide: "Calibration Decision Guide",
    sil34: "SIL 3-4 band",
    sil2: "SIL 2 band",
    sil1: "SIL 1 band",
    target: "target",
    achieved: "achieved",
    predictedDrift: "Predicted Drift",
    silCompliance: "SIL Compliance",
    belowTarget: "Below target",
    onTarget: "On target",
    note: "Regression confidence and tolerance crossing are tracked for interval optimization.",
    proofTestAdequacy: "Proof Test Adequacy",
    calibrationHealth: "Calibration Health",
    axisElapsed: "Elapsed time (days)",
    axisError: "Drift error (%)",
  },
  ko: {
    sectionDrift: "드리프트 추세 및 허용편차",
    sectionSil: "SIL 달성 밴드",
    sectionCalGuide: "교정 의사결정 가이드",
    sil34: "SIL 3-4 구간",
    sil2: "SIL 2 구간",
    sil1: "SIL 1 구간",
    target: "목표",
    achieved: "달성",
    predictedDrift: "예측 드리프트",
    silCompliance: "SIL 적합성",
    belowTarget: "목표 미달",
    onTarget: "목표 충족",
    note: "회귀 신뢰도와 허용편차 교차 시점을 추적해 교정 주기 최적화를 지원합니다.",
    proofTestAdequacy: "증명시험 적정성",
    calibrationHealth: "교정 건전성",
    axisElapsed: "경과 시간 (일)",
    axisError: "드리프트 오차 (%)",
  },
};

function driftSeries(result: CalculationResponse | null): Array<{ days: number; error: number }> {
  const rows = Array.isArray(result?.details.input_data.calibration_history)
    ? result.details.input_data.calibration_history
    : [];
  if (!rows.length) {
    return [
      { days: 0, error: 0.05 },
      { days: 90, error: 0.16 },
      { days: 180, error: 0.28 },
      { days: 270, error: 0.39 },
    ];
  }
  return rows.map((row) => ({
    days: toNumber((row as { days_since_ref?: number }).days_since_ref, 0),
    error: toNumber((row as { error_pct?: number }).error_pct, 0),
  }));
}

export function InstrumentationVisuals({ result }: { result: CalculationResponse | null }) {
  const { language } = useUiLanguage();
  const copy = INST_COPY[language];

  const tolerance = toNumber(result?.details.input_data.tolerance_pct, 1.0);
  const pfd = resultValue(result, "pfdavg", 0.00044);
  const silTarget = resultValue(result, "sil_target", 2);
  const silAchieved = resultValue(result, "sil_achieved", 3);
  const driftPred = resultValue(result, "predicted_drift_pct", 0.38);
  const series = driftSeries(result);
  const proofAdequacy = String(result?.results.proof_test_adequacy ?? "—");
  const calHealth = String(result?.results.calibration_health ?? "—");
  const tooltipProps = getChartTooltipProps();

  return (
    <div className="grid gap-3 lg:grid-cols-3">
      <VisualSectionCard title={copy.sectionDrift}>
        <div className="h-[190px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={series}>
              <XAxis
                dataKey="days"
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisElapsed, position: "insideBottom", offset: -4, ...CHART_AXIS_LABEL_STYLE }}
              />
              <YAxis
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisError, angle: -90, position: "insideLeft", ...CHART_AXIS_LABEL_STYLE }}
              />
              <Tooltip {...tooltipProps} />
              <ReferenceLine y={tolerance} stroke="hsl(var(--danger))" strokeDasharray="4 4" />
              <Line dataKey="error" stroke="hsl(var(--accent))" strokeWidth={3} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionSil}>
        <svg viewBox="0 0 280 210" className="h-[190px] w-full">
          <rect x="25" y="24" width="230" height="30" fill="hsl(var(--success))" opacity="0.35" />
          <rect x="25" y="56" width="230" height="30" fill="hsl(var(--warning))" opacity="0.35" />
          <rect x="25" y="88" width="230" height="30" fill="hsl(var(--danger))" opacity="0.35" />
          <text x="32" y="43" fontSize="11" fill="hsl(var(--foreground))">{copy.sil34}</text>
          <text x="32" y="75" fontSize="11" fill="hsl(var(--foreground))">{copy.sil2}</text>
          <text x="32" y="107" fontSize="11" fill="hsl(var(--foreground))">{copy.sil1}</text>
          <circle cx={55 + (silAchieved * 45)} cy="150" r="8" fill="hsl(var(--accent))" />
          <text x="25" y="175" fontSize="11" fill="hsl(var(--muted-foreground))">
            {copy.target}: SIL {silTarget.toFixed(0)} | {copy.achieved}: SIL {silAchieved.toFixed(0)} | PFDavg: {pfd.toExponential(2)}
          </text>
        </svg>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionCalGuide}>
        <div className="space-y-2 text-sm">
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.predictedDrift}</p>
            <p className={driftPred > tolerance ? "text-warning" : "text-success"}>{driftPred.toFixed(3)}%</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.silCompliance}</p>
            <p className={silAchieved < silTarget ? "text-danger" : "text-foreground"}>
              {silAchieved < silTarget ? copy.belowTarget : copy.onTarget}
            </p>
          </div>
          <p className="text-xs text-muted-foreground">{copy.note}</p>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.proofTestAdequacy}</p>
            <p className={proofAdequacy === "INADEQUATE" ? "text-danger" : proofAdequacy === "MARGINAL" ? "text-warning" : "text-success"}>
              {proofAdequacy.replace(/_/g, " ")}
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.calibrationHealth}</p>
            <p className={calHealth === "EXCEEDED" ? "text-danger" : calHealth === "AT_RISK" ? "text-warning" : "text-success"}>
              {calHealth.replace(/_/g, " ")}
            </p>
          </div>
        </div>
      </VisualSectionCard>
    </div>
  );
}
