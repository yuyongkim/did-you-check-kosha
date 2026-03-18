"use client";

import { Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { useUiLanguage } from "@/hooks/useUiLanguage";
import { CalculationResponse } from "@/lib/types";
import { inputValue, resultValue } from "@/components/visualization/utils";
import { VisualSectionCard } from "@/components/visualization/visual-section-card";
import { CHART_AXIS_LABEL_STYLE, CHART_AXIS_STROKE, CHART_TICK_STYLE, getChartTooltipProps } from "@/components/visualization/chart-theme";
import { Badge } from "@/components/ui/badge";
import {
  getNdeGuide,
  historyData,
  mapFluidTypeLabel,
  mapTemperatureProfileLabel,
  MATERIAL_GROUP_LABEL,
  normalizeMaterialGroup,
  PIPING_COPY,
  processHint,
  recommendedNdeCadence,
  RiskBand,
} from "@/components/visualization/piping-visuals-content";

export function PipingVisuals({ result }: { result: CalculationResponse | null }) {
  const { language } = useUiLanguage();
  const uiLanguage = language === "ko" ? "ko" : "en";
  const copy = PIPING_COPY[uiLanguage];

  const od = inputValue(result, "od_mm", 168.3);
  const currentT = resultValue(result, "t_current_mm", 7.3);
  const minT = resultValue(result, "t_min_mm", 5.1);
  const remainingLife = resultValue(result, "remaining_life_years", 6.2);
  const corrosionRate = resultValue(
    result,
    "cr_selected_mm_per_year",
    resultValue(result, "corrosion_rate_selected_mm_per_year", 0.34),
  );
  const fluidType = String(result?.results.fluid_type ?? result?.details.input_data.fluid_type ?? "unknown");
  const material = String(result?.results.material ?? result?.details.input_data.material ?? "unknown");
  const rawMaterialGroup = String(result?.results.material_group ?? result?.details.input_data.material_group ?? "");
  const materialGroup = normalizeMaterialGroup(rawMaterialGroup || material);
  const materialGroupLabel = MATERIAL_GROUP_LABEL[uiLanguage][materialGroup];
  const materialDisplay = material === "unknown" ? copy.unknown : material;
  const temperatureProfile = String(result?.results.temperature_profile ?? result?.details.input_data.temperature_profile ?? "strict_process");
  const temperatureMode = String(result?.results.temperature_limit_mode ?? "within_conservative_limit");
  const tempSoft = resultValue(result, "temperature_soft_limit_c", 425);
  const tempHard = resultValue(result, "temperature_hard_limit_c", tempSoft);
  const hoopStress = resultValue(result, "hoop_stress_screening_mpa", 0);
  const hoopRatio = resultValue(result, "hoop_stress_ratio", 0);
  const hydrotestPressure = resultValue(result, "hydrotest_pressure_mpa", 0);
  const data = historyData(result, uiLanguage);

  const innerCurrent = Math.max(od - (2 * currentT), 1);
  const innerMin = Math.max(od - (2 * minT), 1);
  const svgCenterX = 150;
  const svgCenterY = 130;
  const rOuter = 92;
  const rCurrent = (innerCurrent / od) * rOuter;
  const rMin = (innerMin / od) * rOuter;

  const lossRatio = minT > 0 ? currentT / minT : 0;
  const corrosionSpread = Math.max(0.06, Math.min(0.45, corrosionRate * 0.14));
  const riskBand: RiskBand =
    remainingLife < 2 || lossRatio < 1.1 ? "critical" : remainingLife < 5 || lossRatio < 1.25 ? "warning" : "normal";

  const currentStroke =
    riskBand === "critical" ? "hsl(var(--danger))" : riskBand === "warning" ? "hsl(var(--warning))" : "hsl(var(--accent))";
  const tooltipProps = getChartTooltipProps();
  const ndeGuide = getNdeGuide(uiLanguage, materialGroup);
  const ndeCadence = recommendedNdeCadence(uiLanguage, riskBand, corrosionRate, temperatureMode);
  const ndeContextHint = processHint(uiLanguage, fluidType, materialGroup, temperatureMode);

  const points = [
    { angle: 270, label: "12h", thickness: currentT + corrosionSpread * 0.6 },
    { angle: 0, label: "3h", thickness: currentT - corrosionSpread * 1.3 },
    { angle: 90, label: "6h", thickness: currentT + corrosionSpread * 0.4 },
    { angle: 180, label: "9h", thickness: currentT - corrosionSpread * 0.9 },
  ].map((point) => ({ ...point, thickness: Math.max(point.thickness, 0.1) }));

  const avgPoint = points.reduce((sum, point) => sum + point.thickness, 0) / points.length;
  const utilizationPercent = Math.max(Math.min((minT / Math.max(currentT, 1e-6)) * 100, 180), 0);
  const utilizationColor =
    utilizationPercent >= 95 ? "text-danger" : utilizationPercent >= 80 ? "text-warning" : "text-success";

  const forecastYear = new Date().getFullYear() + Math.max(Math.ceil(remainingLife), 0);
  const historyLegend = data.map((row, index) => ({
    tag: `T${index + 1}`,
    label: row.name,
    thickness: row.thickness,
  }));
  const lifeMessage =
    riskBand === "critical"
      ? (uiLanguage === "ko"
        ? "임계 감육 추세입니다. 즉시 검사 및 보수 검토가 필요합니다."
        : "Critical thinning trend. Immediate inspection and repair review required.")
      : riskBand === "warning"
        ? (uiLanguage === "ko"
          ? "주의 추세입니다. 모니터링 주기를 단축하고 부식 메커니즘을 재확인하세요."
          : "Warning trend. Increase monitoring cadence and verify corrosion mechanism.")
        : (uiLanguage === "ko"
          ? "현재 스크리닝 가정에서는 두께 여유가 안정적입니다."
          : "Thickness margin is stable under current screening assumptions.");

  return (
    <div className="grid gap-3 lg:grid-cols-3">
      <VisualSectionCard title={copy.sectionCross}>
        <div className="flex h-[240px] items-center justify-center rounded-md border border-border bg-background/40">
          <svg viewBox="0 0 300 270" className="h-[240px] w-full max-w-[460px]">
            {/* Legend – top-left, clear of circle */}
            <rect x="6" y="4" width="10" height="10" rx="2" fill="none" stroke="hsl(var(--foreground))" strokeWidth="1.5" />
            <text x="20" y="13" fontSize="10" fill="hsl(var(--muted-foreground))">
              {copy.labelOd}: {od.toFixed(1)} mm
            </text>
            <rect x="6" y="20" width="10" height="10" rx="2" fill="none" stroke={currentStroke} strokeWidth="1.5" />
            <text x="20" y="29" fontSize="10" fill={currentStroke}>
              {copy.labelIdCurrent}: {innerCurrent.toFixed(1)} mm
            </text>
            <rect x="6" y="36" width="10" height="10" rx="2" fill="none" stroke="hsl(var(--danger))" strokeWidth="1.5" strokeDasharray="3 2" />
            <text x="20" y="45" fontSize="10" fill="hsl(var(--danger))">
              {copy.labelIdAtMin}: {innerMin.toFixed(1)} mm
            </text>

            {/* Cross-section circles */}
            <circle cx={svgCenterX} cy={svgCenterY} r={rOuter} fill="none" stroke="hsl(var(--foreground))" strokeWidth="2" />
            <circle cx={svgCenterX} cy={svgCenterY} r={rCurrent} fill="none" stroke={currentStroke} strokeWidth="9" />
            <circle cx={svgCenterX} cy={svgCenterY} r={rMin} fill="none" stroke="hsl(var(--danger))" strokeWidth="3" strokeDasharray="5 4" />

            {/* Center label */}
            <text x={svgCenterX} y={svgCenterY - 8} fontSize="11" fill="hsl(var(--foreground))" textAnchor="middle" fontWeight="600">
              t = {currentT.toFixed(2)} mm
            </text>
            <text x={svgCenterX} y={svgCenterY + 8} fontSize="10" fill="hsl(var(--danger))" textAnchor="middle">
              t_min = {minT.toFixed(2)} mm
            </text>

            {/* Clock position markers */}
            {points.map((point) => {
              const rad = (point.angle * Math.PI) / 180;
              const cx = svgCenterX + Math.cos(rad) * (rOuter + 14);
              const cy = svgCenterY + Math.sin(rad) * (rOuter + 14);
              const dotX = svgCenterX + Math.cos(rad) * (rOuter - 5);
              const dotY = svgCenterY + Math.sin(rad) * (rOuter - 5);
              return (
                <g key={point.label}>
                  <circle cx={dotX} cy={dotY} r="3.5" fill="hsl(var(--warning))" />
                  <text x={cx} y={cy + 4} fontSize="10" fill="hsl(var(--muted-foreground))" textAnchor="middle">
                    {point.label}
                  </text>
                </g>
              );
            })}
          </svg>
        </div>
        <div className="mt-2 grid grid-cols-2 gap-1 text-[11px]">
          <div className="rounded-md border border-border bg-background/50 px-2 py-1 text-muted-foreground">{copy.labelOd}: {od.toFixed(1)} mm</div>
          <div className="rounded-md border border-border bg-background/50 px-2 py-1" style={{ color: currentStroke }}>
            {copy.labelIdCurrent}: {innerCurrent.toFixed(1)} mm
          </div>
          <div className="rounded-md border border-border bg-background/50 px-2 py-1 text-muted-foreground">
            {copy.labelRl}: {remainingLife.toFixed(2)} {copy.yearUnit}
          </div>
          <div className="rounded-md border border-border bg-background/50 px-2 py-1" style={{ color: currentStroke }}>
            {copy.labelCurrentThickness}: {currentT.toFixed(2)} mm
          </div>
          <div className="rounded-md border border-border bg-background/50 px-2 py-1 text-muted-foreground">
            {copy.labelCr}: {corrosionRate.toFixed(3)} {copy.rateUnit}
          </div>
          <div className="col-span-2 rounded-md border border-border bg-background/50 px-2 py-1 text-danger">
            {copy.labelIdAtMin}: {innerMin.toFixed(1)} mm
          </div>
          <div className="col-span-2 rounded-md border border-border bg-background/50 px-2 py-1 text-danger">{copy.labelTminLimit}: {minT.toFixed(2)} mm</div>
          <div className="rounded-md border border-border bg-background/50 px-2 py-1" style={{ color: hoopRatio > 0.9 ? "hsl(var(--danger))" : hoopRatio > 0.7 ? "hsl(var(--warning))" : undefined }}>
            {copy.labelHoopStress}: {hoopStress.toFixed(2)} MPa
          </div>
          <div className="rounded-md border border-border bg-background/50 px-2 py-1" style={{ color: hoopRatio > 0.9 ? "hsl(var(--danger))" : hoopRatio > 0.7 ? "hsl(var(--warning))" : undefined }}>
            {copy.labelHoopRatio}: {(hoopRatio * 100).toFixed(1)}%
          </div>
          <div className="col-span-2 rounded-md border border-border bg-background/50 px-2 py-1 text-muted-foreground">
            {copy.labelHydrotest}: {hydrotestPressure.toFixed(2)} MPa
          </div>
        </div>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionTrend}>
        <div className="h-[220px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <XAxis
                dataKey="name"
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisInspection, position: "insideBottom", offset: -4, ...CHART_AXIS_LABEL_STYLE }}
              />
              <YAxis
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisThickness, angle: -90, position: "insideLeft", ...CHART_AXIS_LABEL_STYLE }}
              />
              <Tooltip {...tooltipProps} />
              <ReferenceLine y={minT} stroke="hsl(var(--danger))" strokeDasharray="4 4" />
              <Line dataKey="thickness" stroke={currentStroke} strokeWidth={3} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <p className="mt-2 text-[11px] text-muted-foreground">{copy.xAxisHint}</p>
        <div className="mt-2 space-y-1 text-[11px]">
          {historyLegend.map((row) => (
            <p key={`history-${row.tag}-${row.label}`} className="text-muted-foreground">
              <span className="font-semibold text-foreground">{row.tag}</span>
              {` = ${row.label}, ${row.thickness.toFixed(2)} mm`}
            </p>
          ))}
        </div>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionNde}>
        <div className="space-y-2 text-sm">
          {points.map((point) => (
            <div key={point.label} className="flex items-center justify-between rounded-md border border-border bg-background/50 px-2 py-1">
              <span className="text-muted-foreground">{point.label}</span>
              <span className={point.thickness <= minT ? "text-danger" : "text-foreground"}>{point.thickness.toFixed(2)} mm</span>
            </div>
          ))}
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.fluidContext}</p>
            <p className="text-foreground">{mapFluidTypeLabel(uiLanguage, fluidType, copy.unknown)}</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.tempEnvelope}</p>
            <p className={temperatureMode === "exceeded_hard_limit" ? "text-danger" : temperatureMode === "override_review_required" ? "text-warning" : "text-success"}>
              {mapTemperatureProfileLabel(uiLanguage, temperatureProfile)} | {tempSoft.toFixed(0)}&deg;C / {tempHard.toFixed(0)}&deg;C
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.gridAverage}</p>
            <p className={utilizationColor}>
              {uiLanguage === "ko" ? "평균" : "avg"} {avgPoint.toFixed(2)} mm | {utilizationPercent.toFixed(1)}%
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.forecast}</p>
            <p className={riskBand === "critical" ? "text-danger" : riskBand === "warning" ? "text-warning" : "text-success"}>
              {copy.limitYear(forecastYear)}
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.materialGroup}</p>
            <p className="font-data text-xs text-foreground">{materialDisplay} | {materialGroupLabel}</p>
            <p className="mt-1 text-xs text-muted-foreground">{ndeGuide.damageMode}</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.suggestedNdeCadence}</p>
            <p className={riskBand === "critical" ? "text-danger" : riskBand === "warning" ? "text-warning" : "text-success"}>{ndeCadence}</p>
            <p className="mt-1 text-xs text-muted-foreground">{ndeContextHint}</p>
          </div>
          <div className="space-y-1">
            {ndeGuide.methods.map((method) => (
              <div key={method.method} className="rounded-md border border-border bg-background/50 px-2 py-1">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-xs font-semibold text-foreground">{method.method}</p>
                  <Badge variant="neutral" className="font-data text-[10px]">
                    {method.scope}
                  </Badge>
                </div>
                <p className="text-[11px] text-muted-foreground">{method.rationale}</p>
              </div>
            ))}
          </div>
          <p className="text-[11px] text-muted-foreground">{ndeGuide.caution}</p>
          <p className="text-[11px] text-muted-foreground">{copy.ndeTerms}</p>
          <p className="pt-1 text-xs text-muted-foreground">{lifeMessage}</p>
        </div>
      </VisualSectionCard>
    </div>
  );
}
