"use client";

import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { useUiLanguage } from "@/hooks/useUiLanguage";
import { CalculationResponse } from "@/lib/types";
import { inputValue, resultValue } from "@/components/visualization/utils";
import { VisualSectionCard } from "@/components/visualization/visual-section-card";
import { CHART_AXIS_LABEL_STYLE, CHART_AXIS_STROKE, CHART_TICK_STYLE, getChartTooltipProps } from "@/components/visualization/chart-theme";

type UiLanguage = "en" | "ko";

const CIVIL_COPY: Record<UiLanguage, {
  sectionContext: string;
  sectionProgress: string;
  sectionDamage: string;
  cover: string;
  carbonation: string;
  dcRatio: string;
  crackWidth: string;
  spallingArea: string;
  repairPriority: string;
  consequenceCategory: string;
  axisYears: string;
  axisDepth: string;
}> = {
  en: {
    sectionContext: "Concrete Section Context",
    sectionProgress: "Carbonation Progress",
    sectionDamage: "Damage Classification",
    cover: "Cover",
    carbonation: "Carbonation",
    dcRatio: "D/C Ratio",
    crackWidth: "Crack Width",
    spallingArea: "Spalling Area",
    repairPriority: "Repair Priority",
    consequenceCategory: "Consequence Category",
    axisYears: "Service time (years)",
    axisDepth: "Carbonation depth (mm)",
  },
  ko: {
    sectionContext: "콘크리트 단면 컨텍스트",
    sectionProgress: "탄산화 진행",
    sectionDamage: "손상 분류",
    cover: "피복두께",
    carbonation: "탄산화 깊이",
    dcRatio: "D/C 비율",
    crackWidth: "균열 폭",
    spallingArea: "박락 면적",
    repairPriority: "보수 우선순위",
    consequenceCategory: "결과 범주",
    axisYears: "사용 시간 (년)",
    axisDepth: "탄산화 깊이 (mm)",
  },
};

export function CivilVisuals({ result }: { result: CalculationResponse | null }) {
  const { language } = useUiLanguage();
  const copy = CIVIL_COPY[language];

  const serviceYears = inputValue(result, "service_years", 18);
  const cover = inputValue(result, "cover_thickness_mm", 40);
  const carbonationDepth = resultValue(result, "carbonation_depth_mm", 9.5);
  const yearsToCorrosion = resultValue(result, "years_to_corrosion_init", 34);
  const dcRatio = resultValue(result, "dc_ratio", 0.78);
  const crackWidth = resultValue(result, "crack_width_mm", 0.22);
  const spalling = resultValue(result, "spalling_area_percent", 5);
  const repairPriority = String(result?.results.repair_priority ?? "—");
  const consequenceCategory = String(result?.results.consequence_category ?? "—");
  const trend = [
    { year: 0, depth: 0 },
    { year: serviceYears * 0.4, depth: carbonationDepth * 0.55 },
    { year: serviceYears * 0.7, depth: carbonationDepth * 0.85 },
    { year: serviceYears, depth: carbonationDepth },
    { year: serviceYears + yearsToCorrosion, depth: cover },
  ];
  const tooltipProps = getChartTooltipProps();

  return (
    <div className="grid gap-3 lg:grid-cols-3">
      <VisualSectionCard title={copy.sectionContext}>
        <svg viewBox="0 0 280 210" className="h-[190px] w-full">
          <rect x="36" y="34" width="208" height="146" fill="none" stroke="hsl(var(--foreground))" strokeWidth="2" />
          <rect x="46" y="44" width="188" height="126" fill="none" stroke="hsl(var(--accent))" strokeDasharray="5 3" />
          <circle cx="74" cy="146" r="9" fill="hsl(var(--warning))" />
          <circle cx="126" cy="146" r="9" fill="hsl(var(--warning))" />
          <circle cx="178" cy="146" r="9" fill="hsl(var(--warning))" />
          <text x="12" y="22" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.cover}: {cover.toFixed(1)} mm</text>
          <text x="12" y="38" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.carbonation}: {carbonationDepth.toFixed(1)} mm</text>
        </svg>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionProgress}>
        <div className="h-[190px]">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={trend}>
              <XAxis
                dataKey="year"
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisYears, position: "insideBottom", offset: -4, ...CHART_AXIS_LABEL_STYLE }}
              />
              <YAxis
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisDepth, angle: -90, position: "insideLeft", ...CHART_AXIS_LABEL_STYLE }}
              />
              <Tooltip {...tooltipProps} />
              <Area type="monotone" dataKey="depth" stroke="hsl(var(--accent))" fill="hsl(var(--accent))" fillOpacity={0.28} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionDamage}>
        <div className="space-y-2 text-sm">
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.dcRatio}</p>
            <p className={dcRatio >= 1.2 ? "text-danger" : dcRatio >= 1.0 ? "text-warning" : "text-foreground"}>{dcRatio.toFixed(3)}</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.crackWidth}</p>
            <p className={crackWidth > 0.4 ? "text-danger" : "text-foreground"}>{crackWidth.toFixed(2)} mm</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.spallingArea}</p>
            <p className={spalling > 20 ? "text-danger" : "text-foreground"}>{spalling.toFixed(1)}%</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.repairPriority}</p>
            <p className={repairPriority.includes("IMMEDIATE") ? "text-danger" : repairPriority.includes("NEXT_SHUTDOWN") ? "text-warning" : "text-foreground"}>
              {repairPriority.replace(/_/g, " ")}
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.consequenceCategory}</p>
            <p className={consequenceCategory.includes("HIGH") ? "text-danger" : consequenceCategory.includes("MEDIUM") ? "text-warning" : "text-success"}>
              {consequenceCategory.replace(/_/g, " ")}
            </p>
          </div>
        </div>
      </VisualSectionCard>
    </div>
  );
}
