"use client";

import { Bar, BarChart, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { useUiLanguage } from "@/hooks/useUiLanguage";
import { CalculationResponse } from "@/lib/types";
import { resultValue } from "@/components/visualization/utils";
import { VisualSectionCard } from "@/components/visualization/visual-section-card";
import { CHART_AXIS_LABEL_STYLE, CHART_AXIS_STROKE, CHART_TICK_STYLE, getChartTooltipProps } from "@/components/visualization/chart-theme";

type UiLanguage = "en" | "ko";

const ELECTRICAL_COPY: Record<UiLanguage, {
  sectionSingleLine: string;
  sectionBreakdown: string;
  sectionSafety: string;
  transformer: string;
  switchgear: string;
  motor: string;
  arc: string;
  healthIndex: string;
  arcFlash: string;
  voltageDrop: string;
  thd: string;
  arcZone: string;
  noWork: string;
  highPpe: string;
  controlled: string;
  transformerHi: string;
  powerQuality: string;
  breakerMargin: string;
  loadUtil: string;
  axisMetric: string;
  axisValue: string;
}> = {
  en: {
    sectionSingleLine: "Single-Line Context (Concept)",
    sectionBreakdown: "Electrical Integrity Breakdown",
    sectionSafety: "Safety Zones",
    transformer: "Transformer",
    switchgear: "Switchgear",
    motor: "Motor",
    arc: "Arc",
    healthIndex: "Health Index",
    arcFlash: "Arc Flash",
    voltageDrop: "Voltage Drop",
    thd: "THD",
    arcZone: "Arc Flash Zone",
    noWork: "No work zone",
    highPpe: "High PPE zone",
    controlled: "Controlled zone",
    transformerHi: "Transformer HI",
    powerQuality: "Power Quality",
    breakerMargin: "Breaker Coordination Margin",
    loadUtil: "Load Utilization",
    axisMetric: "Metric",
    axisValue: "Value (mixed units)",
  },
  ko: {
    sectionSingleLine: "단선도 컨텍스트 (개념)",
    sectionBreakdown: "전기 무결성 분해",
    sectionSafety: "안전 구역",
    transformer: "변압기",
    switchgear: "스위치기어",
    motor: "모터",
    arc: "아크",
    healthIndex: "건전성 지수",
    arcFlash: "아크플래시",
    voltageDrop: "전압강하",
    thd: "THD",
    arcZone: "아크플래시 구역",
    noWork: "작업 금지 구역",
    highPpe: "고등급 PPE 구역",
    controlled: "통제 작업 구역",
    transformerHi: "변압기 HI",
    powerQuality: "전력품질",
    breakerMargin: "차단기 협조 여유",
    loadUtil: "부하 사용률",
    axisMetric: "지표",
    axisValue: "값 (혼합 단위)",
  },
};

export function ElectricalVisuals({ result }: { result: CalculationResponse | null }) {
  const { language } = useUiLanguage();
  const copy = ELECTRICAL_COPY[language];

  const arc = resultValue(result, "arc_flash_energy_cal_cm2", 11.5);
  const hi = resultValue(result, "transformer_health_index", 7.8);
  const voltageDrop = resultValue(result, "voltage_drop_percent", 3.2);
  const thd = resultValue(result, "thd_voltage_percent", 4.8);
  const breakerMargin = Number(result?.results.breaker_coordination_margin ?? 0);
  const loadUtil = String(result?.results.load_utilization ?? "—");
  const breakdown = [
    { key: copy.healthIndex, value: hi, color: "hsl(var(--success))" },
    { key: copy.arcFlash, value: arc, color: "hsl(var(--warning))" },
    { key: copy.voltageDrop, value: voltageDrop, color: "hsl(var(--accent))" },
    { key: copy.thd, value: thd, color: "hsl(var(--danger))" },
  ];
  const tooltipProps = getChartTooltipProps();

  return (
    <div className="grid gap-3 lg:grid-cols-3">
      <VisualSectionCard title={copy.sectionSingleLine}>
        <svg viewBox="0 0 290 210" className="h-[190px] w-full">
          <rect x="12" y="80" width="60" height="50" fill="none" stroke="hsl(var(--foreground))" />
          <rect x="112" y="80" width="70" height="50" fill="none" stroke="hsl(var(--accent))" />
          <rect x="218" y="80" width="60" height="50" fill="none" stroke="hsl(var(--foreground))" />
          <line x1="72" y1="105" x2="112" y2="105" stroke="hsl(var(--muted-foreground))" strokeWidth="2" />
          <line x1="182" y1="105" x2="218" y2="105" stroke="hsl(var(--muted-foreground))" strokeWidth="2" />
          <text x="18" y="74" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.transformer}</text>
          <text x="118" y="74" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.switchgear}</text>
          <text x="232" y="74" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.motor}</text>
          <text x="96" y="158" fontSize="11" fill="hsl(var(--danger))">{copy.arc}: {arc.toFixed(1)} cal/cm2</text>
        </svg>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionBreakdown}>
        <div className="h-[190px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={breakdown}>
              <XAxis
                dataKey="key"
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisMetric, position: "insideBottom", offset: -4, ...CHART_AXIS_LABEL_STYLE }}
              />
              <YAxis
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisValue, angle: -90, position: "insideLeft", ...CHART_AXIS_LABEL_STYLE }}
              />
              <Tooltip {...tooltipProps} />
              <Bar dataKey="value">
                {breakdown.map((entry) => <Cell key={entry.key} fill={entry.color} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionSafety}>
        <div className="space-y-2 text-sm">
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.arcZone}</p>
            <p className={arc > 40 ? "text-danger" : arc > 25 ? "text-warning" : "text-success"}>
              {arc > 40 ? copy.noWork : arc > 25 ? copy.highPpe : copy.controlled}
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.transformerHi}</p>
            <p className={hi < 3 ? "text-danger" : hi < 5 ? "text-warning" : "text-foreground"}>{hi.toFixed(2)} / 10</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.powerQuality}</p>
            <p className={thd > 8 ? "text-danger" : "text-foreground"}>THD {thd.toFixed(1)}% | Vdrop {voltageDrop.toFixed(1)}%</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.breakerMargin}</p>
            <p className={breakerMargin < 1 ? "text-danger" : breakerMargin < 1.25 ? "text-warning" : "text-success"}>
              {breakerMargin.toFixed(2)}x
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.loadUtil}</p>
            <p className={loadUtil.includes("HEAVILY") ? "text-danger" : loadUtil.includes("MODERATELY") ? "text-warning" : "text-foreground"}>
              {loadUtil.replace(/_/g, " ")}
            </p>
          </div>
        </div>
      </VisualSectionCard>
    </div>
  );
}
