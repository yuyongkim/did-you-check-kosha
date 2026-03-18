"use client";

import { Line, LineChart, ResponsiveContainer, Scatter, Tooltip, XAxis, YAxis } from "recharts";

import { useUiLanguage } from "@/hooks/useUiLanguage";
import { CalculationResponse } from "@/lib/types";
import { inputValue, resultValue } from "@/components/visualization/utils";
import { VisualSectionCard } from "@/components/visualization/visual-section-card";
import { CHART_AXIS_LABEL_STYLE, CHART_AXIS_STROKE, CHART_TICK_STYLE, getChartTooltipProps } from "@/components/visualization/chart-theme";

type UiLanguage = "en" | "ko";

interface VesselVisualCopy {
  sectionSchematic: string;
  sectionStress: string;
  sectionScreen: string;
  shellReq: string;
  current: string;
  shellMargin: string;
  slenderness: string;
  volume: string;
  externalUtil: string;
  nozzleIndex: string;
  opening: string;
  ffsLevel: string;
  repairScope: string;
  diameter: string;
  length: string;
  height: string;
  ld: string;
  axisTemperature: string;
  axisStress: string;
}

const VESSEL_COPY: Record<UiLanguage, VesselVisualCopy> = {
  en: {
    sectionSchematic: "Vessel Schematic (Concept)",
    sectionStress: "Allowable Stress vs Temperature",
    sectionScreen: "Thickness and Geometry Screens",
    shellReq: "Shell req",
    current: "Current",
    shellMargin: "Shell Margin",
    slenderness: "Slenderness (L/D)",
    volume: "Estimated Internal Volume",
    externalUtil: "External Pressure Utilization",
    nozzleIndex: "Nozzle Reinforcement Index",
    opening: "opening",
    ffsLevel: "FFS Screening Level",
    repairScope: "Repair Scope",
    diameter: "D",
    length: "L",
    height: "H",
    ld: "L/D",
    axisTemperature: "Temperature (C)",
    axisStress: "Allowable stress (MPa)",
  },
  ko: {
    sectionSchematic: "용기 스케매틱 (개념)",
    sectionStress: "허용응력 vs 온도",
    sectionScreen: "두께 및 형상 스크리닝",
    shellReq: "쉘 요구두께",
    current: "현재두께",
    shellMargin: "쉘 여유",
    slenderness: "세장비 (L/D)",
    volume: "추정 내부 체적",
    externalUtil: "외압 사용률",
    nozzleIndex: "노즐 보강 지수",
    opening: "개구비",
    ffsLevel: "FFS 스크리닝 등급",
    repairScope: "보수 범위",
    diameter: "D",
    length: "L",
    height: "H",
    ld: "L/D",
    axisTemperature: "온도 (C)",
    axisStress: "허용응력 (MPa)",
  },
};

function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

function toMaybeNumber(value: unknown): number | null {
  if (value === null || value === undefined) return null;
  const asNumber = Number(value);
  return Number.isFinite(asNumber) ? asNumber : null;
}

function readInputNumber(
  result: CalculationResponse | null,
  previewInput: Record<string, unknown> | undefined,
  key: string,
  fallback: number,
): number {
  const preview = toMaybeNumber(previewInput?.[key]);
  if (preview !== null) return preview;
  return inputValue(result, key, fallback);
}

function resolveVesselType(result: CalculationResponse | null, previewInput?: Record<string, unknown>): string {
  const fromPreview = String(previewInput?.vessel_type ?? "").trim();
  if (fromPreview) return fromPreview;
  return String(result?.details.input_data.vessel_type ?? result?.results.vessel_type ?? "horizontal_drum");
}

function resolveHeadType(result: CalculationResponse | null, previewInput?: Record<string, unknown>): string {
  const fromPreview = String(previewInput?.head_type ?? "").trim();
  if (fromPreview) return fromPreview;
  return String(result?.details.input_data.head_type ?? result?.results.head_type ?? "ellipsoidal_2_1");
}

function vesselLabel(language: UiLanguage, vesselType: string): string {
  if (language === "ko") {
    if (vesselType === "vertical_vessel") return "수직 용기";
    if (vesselType === "column_tower") return "컬럼 / 타워";
    if (vesselType === "hx_shell") return "열교환기 쉘";
    if (vesselType === "reactor") return "반응기";
    return "수평 드럼";
  }

  if (vesselType === "vertical_vessel") return "Vertical Vessel";
  if (vesselType === "column_tower") return "Column / Tower";
  if (vesselType === "hx_shell") return "Heat Exchanger Shell";
  if (vesselType === "reactor") return "Reactor";
  return "Horizontal Drum";
}

function headLabel(language: UiLanguage, headType: string): string {
  if (language === "ko") {
    if (headType === "torispherical") return "토리구형";
    if (headType === "hemispherical") return "반구형";
    if (headType === "flat") return "평판형";
    return "타원형 2:1";
  }

  if (headType === "torispherical") return "Torispherical";
  if (headType === "hemispherical") return "Hemispherical";
  if (headType === "flat") return "Flat";
  return "Ellipsoidal 2:1";
}

function isVerticalType(vesselType: string): boolean {
  return ["vertical_vessel", "column_tower", "reactor"].includes(vesselType);
}

function VesselSchematic({
  vesselType,
  requiredThickness,
  currentThickness,
  insideRadius,
  shellLength,
  shellHeight,
  headDepth,
  nozzleOd,
  copy,
}: {
  vesselType: string;
  requiredThickness: number;
  currentThickness: number;
  insideRadius: number;
  shellLength: number;
  shellHeight: number;
  headDepth: number;
  nozzleOd: number;
  copy: VesselVisualCopy;
}) {
  const diameter = Math.max(insideRadius * 2, 1);
  const span = isVerticalType(vesselType) ? shellHeight : shellLength;
  const ldRatio = span / diameter;
  const nozzleScale = clamp((nozzleOd / diameter) * 60, 10, 32);
  const headDepthRatio = clamp(headDepth / diameter, 0.02, 0.55);
  const headBulge = clamp(10 + headDepthRatio * 52, 12, 40);

  if (isVerticalType(vesselType)) {
    const bodyHeight = Math.round(clamp(74 + ldRatio * 7, 74, 145));
    return (
      <svg viewBox="0 0 280 210" className="h-[190px] w-full">
        <ellipse cx="140" cy={34} rx={52} ry={headBulge / 2} fill="none" stroke="hsl(var(--foreground))" strokeWidth="2" />
        <rect x="88" y="34" width="104" height={bodyHeight} fill="none" stroke="hsl(var(--accent))" strokeWidth="5" />
        <ellipse cx="140" cy={34 + bodyHeight} rx={52} ry={headBulge / 2} fill="none" stroke="hsl(var(--foreground))" strokeWidth="2" />
        <rect x={192 - nozzleScale / 2} y={66} width={nozzleScale} height={14} fill="none" stroke="hsl(var(--danger))" strokeWidth="2" />
        <text x="12" y="18" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.shellReq}: {requiredThickness.toFixed(2)} mm</text>
        <text x="12" y="34" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.current}: {currentThickness.toFixed(2)} mm</text>
        <text x="12" y="50" fontSize="11" fill="hsl(var(--muted-foreground))">
          {copy.diameter}={diameter.toFixed(0)} | {copy.height}={span.toFixed(0)} | {copy.ld}={ldRatio.toFixed(2)}
        </text>
      </svg>
    );
  }

  if (vesselType === "hx_shell") {
    const bodyWidth = Math.round(clamp(150 + ldRatio * 18, 160, 224));
    const x = Math.round((280 - bodyWidth) / 2);
    return (
      <svg viewBox="0 0 280 210" className="h-[190px] w-full">
        <ellipse cx="140" cy="78" rx={bodyWidth / 2} ry={headBulge / 2 + 10} fill="none" stroke="hsl(var(--foreground))" strokeWidth="2" />
        <rect x={x} y="78" width={bodyWidth} height="62" fill="none" stroke="hsl(var(--accent))" strokeWidth="5" />
        <ellipse cx="140" cy="140" rx={bodyWidth / 2} ry={headBulge / 2 + 10} fill="none" stroke="hsl(var(--foreground))" strokeWidth="2" />
        <line x1={x + 10} y1="93" x2={x + bodyWidth - 10} y2="93" stroke="hsl(var(--muted-foreground))" strokeWidth="1.5" />
        <line x1={x + 10} y1="106" x2={x + bodyWidth - 10} y2="106" stroke="hsl(var(--muted-foreground))" strokeWidth="1.5" />
        <line x1={x + 10} y1="119" x2={x + bodyWidth - 10} y2="119" stroke="hsl(var(--muted-foreground))" strokeWidth="1.5" />
        <rect x={x + bodyWidth - 20} y={86} width={nozzleScale} height={14} fill="none" stroke="hsl(var(--danger))" strokeWidth="2" />
        <text x="12" y="18" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.shellReq}: {requiredThickness.toFixed(2)} mm</text>
        <text x="12" y="34" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.current}: {currentThickness.toFixed(2)} mm</text>
        <text x="12" y="50" fontSize="11" fill="hsl(var(--muted-foreground))">
          {copy.diameter}={diameter.toFixed(0)} | {copy.length}={span.toFixed(0)} | {copy.ld}={ldRatio.toFixed(2)}
        </text>
      </svg>
    );
  }

  const bodyWidth = Math.round(clamp(150 + ldRatio * 18, 160, 224));
  const x = Math.round((280 - bodyWidth) / 2);
  return (
    <svg viewBox="0 0 280 210" className="h-[190px] w-full">
      <ellipse cx="140" cy="50" rx={bodyWidth / 2} ry={headBulge / 2 + 8} fill="none" stroke="hsl(var(--foreground))" strokeWidth="2" />
      <rect x={x} y="50" width={bodyWidth} height="108" fill="none" stroke="hsl(var(--accent))" strokeWidth="5" />
      <ellipse cx="140" cy="158" rx={bodyWidth / 2} ry={headBulge / 2 + 8} fill="none" stroke="hsl(var(--foreground))" strokeWidth="2" />
      <rect x={x + bodyWidth - 24} y="75" width={nozzleScale} height="20" fill="none" stroke="hsl(var(--danger))" strokeWidth="2" />
      <text x="12" y="20" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.shellReq}: {requiredThickness.toFixed(2)} mm</text>
      <text x="12" y="36" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.current}: {currentThickness.toFixed(2)} mm</text>
      <text x="12" y="52" fontSize="11" fill="hsl(var(--muted-foreground))">
        {copy.diameter}={diameter.toFixed(0)} | {copy.length}={span.toFixed(0)} | {copy.ld}={ldRatio.toFixed(2)}
      </text>
    </svg>
  );
}

export function VesselVisuals({
  result,
  previewInput,
}: {
  result: CalculationResponse | null;
  previewInput?: Record<string, unknown>;
}) {
  const { language } = useUiLanguage();
  const copy = VESSEL_COPY[language];

  const vesselType = resolveVesselType(result, previewInput);
  const headType = resolveHeadType(result, previewInput);
  const insideRadius = readInputNumber(result, previewInput, "inside_radius_mm", 750);
  const shellLength = readInputNumber(result, previewInput, "shell_length_mm", 3000);
  const shellHeight = readInputNumber(result, previewInput, "straight_shell_height_mm", 6000);
  const headDepth = readInputNumber(result, previewInput, "head_depth_mm", insideRadius * 0.5);
  const nozzleOd = readInputNumber(result, previewInput, "nozzle_od_mm", 350);

  const designTemp = readInputNumber(result, previewInput, "design_temperature_c", 200);
  const currentThickness = readInputNumber(result, previewInput, "t_current_mm", 18);
  const requiredThickness = resultValue(result, "t_required_shell_mm", 11.2);
  const margin = resultValue(result, "thickness_margin_mm", currentThickness - requiredThickness);
  const allowableStress = resultValue(result, "allowable_stress_mpa", 120);
  const extUtil = resultValue(result, "external_pressure_utilization", 0);
  const nozzleIndex = resultValue(result, "nozzle_reinforcement_index", 1.1);
  const openingRatio = resultValue(result, "nozzle_opening_ratio", nozzleOd / Math.max(insideRadius * 2, 1));
  const ffsLevel = String(result?.results.ffs_screening_level ?? "—");
  const repairScope = String(result?.results.repair_scope_screening ?? "—");

  const diameter = insideRadius * 2;
  const span = isVerticalType(vesselType) ? shellHeight : shellLength;
  const ldRatio = span / Math.max(diameter, 1);
  const volume = resultValue(result, "estimated_internal_volume_m3", (Math.PI * (insideRadius ** 2) * span) / 1_000_000_000);

  const vesselTypeText = vesselLabel(language, vesselType);
  const tooltipProps = getChartTooltipProps();

  const tempData = [
    { temp: 20, stress: 138 },
    { temp: 100, stress: 131 },
    { temp: 200, stress: 124 },
    { temp: 300, stress: 117 },
    { temp: 400, stress: 110 },
  ];

  return (
    <div className="grid gap-3 lg:grid-cols-3">
      <VisualSectionCard title={copy.sectionSchematic}>
        <p className="mb-1 text-[11px] uppercase tracking-wide text-accent">{vesselTypeText} | {headLabel(language, headType)}</p>
        <VesselSchematic
          vesselType={vesselType}
          requiredThickness={requiredThickness}
          currentThickness={currentThickness}
          insideRadius={insideRadius}
          shellLength={shellLength}
          shellHeight={shellHeight}
          headDepth={headDepth}
          nozzleOd={nozzleOd}
          copy={copy}
        />
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionStress}>
        <div className="h-[190px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={tempData}>
              <XAxis
                dataKey="temp"
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisTemperature, position: "insideBottom", offset: -4, ...CHART_AXIS_LABEL_STYLE }}
              />
              <YAxis
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisStress, angle: -90, position: "insideLeft", ...CHART_AXIS_LABEL_STYLE }}
              />
              <Tooltip {...tooltipProps} />
              <Line dataKey="stress" stroke="hsl(var(--accent))" strokeWidth={3} dot={{ r: 2 }} />
              <Scatter data={[{ temp: designTemp, stress: allowableStress }]} fill="hsl(var(--danger))" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionScreen}>
        <div className="space-y-2 text-sm">
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.shellMargin}</p>
            <p className={margin < 0.5 ? "text-warning" : "text-success"}>{margin.toFixed(2)} mm</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.slenderness}</p>
            <p className={ldRatio > 8 ? "text-warning" : "text-foreground"}>{ldRatio.toFixed(2)}</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.volume}</p>
            <p className="text-foreground">{volume.toFixed(2)} m3</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.externalUtil}</p>
            <p className={extUtil > 1 ? "text-warning" : "text-foreground"}>{extUtil.toFixed(2)}</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.nozzleIndex}</p>
            <p className={nozzleIndex < 1 ? "text-warning" : "text-foreground"}>
              {nozzleIndex.toFixed(2)} ({copy.opening} {openingRatio.toFixed(2)})
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.ffsLevel}</p>
            <p className={ffsLevel.includes("LEVEL3") ? "text-danger" : ffsLevel.includes("LEVEL2") ? "text-warning" : "text-success"}>
              {ffsLevel.replace(/_/g, " ")}
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.repairScope}</p>
            <p className={repairScope.includes("REPLACE") ? "text-danger" : repairScope.includes("EVALUATE") ? "text-warning" : "text-foreground"}>
              {repairScope.replace(/_/g, " ")}
            </p>
          </div>
        </div>
      </VisualSectionCard>
    </div>
  );
}
