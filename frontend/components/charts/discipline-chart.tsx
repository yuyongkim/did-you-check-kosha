"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  PolarAngleAxis,
  PolarGrid,
  RadialBar,
  RadialBarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { CalculationResponse, Discipline } from "@/lib/types";
import { CHART_AXIS_LABEL_STYLE, CHART_AXIS_STROKE, CHART_TICK_STYLE, getChartTooltipProps } from "@/components/visualization/chart-theme";

function toNumber(value: unknown, fallback = 0): number {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function getTrendData(result: CalculationResponse | null): Array<{ name: string; value: number }> {
  if (!result) {
    return [
      { name: "Y-10", value: 10 },
      { name: "Y-5", value: 8.4 },
      { name: "Now", value: 7.2 },
    ];
  }

  const input = result.details.input_data;
  const thicknessHistory = Array.isArray(input.thickness_history) ? input.thickness_history : [];
  if (thicknessHistory.length > 0) {
    return thicknessHistory.map((row, idx) => ({
      name: `T${idx + 1}`,
      value: toNumber((row as { thickness_mm?: number }).thickness_mm, 0),
    }));
  }

  const calibrationHistory = Array.isArray(input.calibration_history) ? input.calibration_history : [];
  if (calibrationHistory.length > 0) {
    return calibrationHistory.map((row, idx) => ({
      name: `P${idx + 1}`,
      value: toNumber((row as { error_pct?: number }).error_pct, 0),
    }));
  }

  return Object.entries(result.results)
    .slice(0, 4)
    .map(([key, value]) => ({ name: key.slice(0, 8), value: toNumber(value, 0) }));
}

function getSpectrumData(result: CalculationResponse | null): Array<{ name: string; value: number }> {
  const vibration = toNumber(result?.results.vibration_mm_per_s, 2.5);
  return [
    { name: "1X", value: vibration },
    { name: "2X", value: Math.max(vibration * 0.45, 0.05) },
    { name: "BPFO", value: Math.max(vibration * 0.33, 0.05) },
    { name: "BPFI", value: Math.max(vibration * 0.27, 0.05) },
  ];
}

function getGaugeValue(result: CalculationResponse | null): number {
  if (!result) return 0;
  if (typeof result.results.dc_ratio === "number") {
    return Math.min(Math.max(toNumber(result.results.dc_ratio) * 100, 0), 150);
  }
  if (typeof result.results.remaining_life_years === "number") {
    return Math.min(Math.max(toNumber(result.results.remaining_life_years) * 5, 0), 100);
  }
  return 45;
}

function getSeriesColor(discipline: Discipline): string {
  if (discipline === "piping") return "hsl(var(--chart-piping))";
  if (discipline === "vessel") return "hsl(var(--chart-vessel))";
  if (discipline === "rotating") return "hsl(var(--chart-rotating))";
  return "hsl(var(--primary))";
}

export function DisciplineChart({ discipline, result }: { discipline: Discipline; result: CalculationResponse | null }) {
  const { language } = useUiLanguage();
  const trendData = getTrendData(result);
  const spectrumData = getSpectrumData(result);
  const gaugeValue = getGaugeValue(result);
  const tooltipProps = getChartTooltipProps();
  const seriesColor = getSeriesColor(discipline);
  const copy = language === "ko"
    ? {
        axisPoint: "지점 / 시점",
        axisValue: "값",
        axisBand: "주파수 밴드 / 차수",
        axisAmplitude: "진폭 (mm/s)",
      }
    : {
        axisPoint: "Point / timestamp",
        axisValue: "Value",
        axisBand: "Frequency band / order",
        axisAmplitude: "Amplitude (mm/s)",
      };

  return (
    <Card className="animate-fadeUp">
      <CardHeader>
        <CardTitle>Engineering Visualization</CardTitle>
      </CardHeader>
      <CardContent className="h-[260px]">
        <ResponsiveContainer width="100%" height="100%">
          {discipline === "rotating" ? (
            <BarChart data={spectrumData}>
              <CartesianGrid strokeDasharray="2 4" stroke="hsl(var(--border))" />
              <XAxis
                dataKey="name"
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisBand, position: "insideBottom", offset: -4, ...CHART_AXIS_LABEL_STYLE }}
              />
              <YAxis
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisAmplitude, angle: -90, position: "insideLeft", ...CHART_AXIS_LABEL_STYLE }}
              />
              <Tooltip {...tooltipProps} />
              <Bar dataKey="value" fill={seriesColor} radius={[4, 4, 0, 0]} />
            </BarChart>
          ) : discipline === "steel" || discipline === "civil" ? (
            <RadialBarChart
              cx="50%"
              cy="50%"
              innerRadius="35%"
              outerRadius="85%"
              barSize={14}
              data={[{ name: "utilization", value: gaugeValue, fill: seriesColor }]}
            >
              <PolarGrid />
              <PolarAngleAxis type="number" domain={[0, 150]} tick={false} />
              <RadialBar background dataKey="value" />
            </RadialBarChart>
          ) : (
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="2 4" stroke="hsl(var(--border))" />
              <XAxis
                dataKey="name"
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisPoint, position: "insideBottom", offset: -4, ...CHART_AXIS_LABEL_STYLE }}
              />
              <YAxis
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisValue, angle: -90, position: "insideLeft", ...CHART_AXIS_LABEL_STYLE }}
              />
              <Tooltip {...tooltipProps} />
              <Line type="monotone" dataKey="value" stroke={seriesColor} strokeWidth={2} dot={{ r: 2 }} />
            </LineChart>
          )}
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
