"use client";

import { Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { CalculationResponse, Discipline } from "@/lib/types";
import { CHART_AXIS_LABEL_STYLE, CHART_AXIS_STROKE, CHART_TICK_STYLE, getChartTooltipProps } from "@/components/visualization/chart-theme";

interface Point {
  name: string;
  value: number;
}

function toNumber(value: unknown, fallback = 0): number {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function buildSeries(result: CalculationResponse | null): Point[] {
  if (!result) return [{ name: "T-2", value: 80 }, { name: "T-1", value: 74 }, { name: "Now", value: 70 }];

  const input = result.details.input_data;
  const thicknessHistory = Array.isArray(input.thickness_history) ? input.thickness_history : [];
  if (thicknessHistory.length > 0) {
    return thicknessHistory.map((row, index) => ({
      name: `H${index + 1}`,
      value: toNumber((row as { thickness_mm?: number }).thickness_mm, 0),
    }));
  }

  const calibrationHistory = Array.isArray(input.calibration_history) ? input.calibration_history : [];
  if (calibrationHistory.length > 0) {
    return calibrationHistory.map((row, index) => ({
      name: `C${index + 1}`,
      value: toNumber((row as { error_pct?: number }).error_pct, 0),
    }));
  }

  const firstNumeric = Object.values(result.results).find((value) => Number.isFinite(Number(value)));
  const base = toNumber(firstNumeric, 50);
  return [
    { name: "T-2", value: base * 1.08 },
    { name: "T-1", value: base * 1.04 },
    { name: "Now", value: base },
  ];
}

function thresholdFor(discipline: Discipline, result: CalculationResponse | null, current: number): number {
  if (discipline === "piping") return toNumber(result?.results.t_min_mm, current * 0.9);
  if (discipline === "vessel") return toNumber(result?.results.t_required_shell_mm, current * 0.9);
  if (discipline === "steel" || discipline === "civil") return 1;
  if (discipline === "instrumentation") return 2;
  if (discipline === "electrical") return 8;
  return current * 0.85;
}

export function TimeSeriesThresholdCard({
  discipline,
  result,
}: {
  discipline: Discipline;
  result: CalculationResponse | null;
}) {
  const { language } = useUiLanguage();
  const copy = language === "ko"
    ? {
        title: "Time-Series + Threshold",
        xAxis: "시점",
        yAxis: "핵심 지표",
        threshold: "기준치",
        forecast: "다음 점검 예측",
      }
    : {
        title: "Time-Series + Threshold",
        xAxis: "Time",
        yAxis: "Key metric",
        threshold: "Threshold",
        forecast: "Next inspection forecast",
      };

  const data = buildSeries(result);
  const current = data[data.length - 1]?.value ?? 0;
  const threshold = thresholdFor(discipline, result, current);
  const slope = data.length >= 2 ? data[data.length - 1].value - data[data.length - 2].value : -1;
  const forecast = Math.max(0, current + slope);
  const chartData = [...data, { name: "Next", value: forecast }];

  return (
    <Card>
      <CardHeader>
        <CardTitle>{copy.title}</CardTitle>
      </CardHeader>
      <CardContent className="h-[240px]">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <XAxis
              dataKey="name"
              stroke={CHART_AXIS_STROKE}
              tick={CHART_TICK_STYLE}
              label={{ value: copy.xAxis, position: "insideBottom", offset: -4, ...CHART_AXIS_LABEL_STYLE }}
            />
            <YAxis
              stroke={CHART_AXIS_STROKE}
              tick={CHART_TICK_STYLE}
              label={{ value: copy.yAxis, angle: -90, position: "insideLeft", ...CHART_AXIS_LABEL_STYLE }}
            />
            <Tooltip {...getChartTooltipProps()} />
            <ReferenceLine y={threshold} stroke="hsl(var(--danger))" strokeDasharray="5 4" label={copy.threshold} />
            <Line type="monotone" dataKey="value" stroke="hsl(var(--primary))" strokeWidth={2} dot={{ r: 2 }} />
          </LineChart>
        </ResponsiveContainer>
        <p className="mt-2 text-xs text-muted-foreground">
          {copy.forecast}: {forecast.toFixed(2)} / {copy.threshold}: {threshold.toFixed(2)}
        </p>
      </CardContent>
    </Card>
  );
}
