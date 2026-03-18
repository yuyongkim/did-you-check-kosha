export const CHART_AXIS_STROKE = "hsl(var(--border))";

export const CHART_TICK_STYLE = {
  fill: "hsl(var(--muted-foreground))",
  fontSize: 11,
  opacity: 1,
} as const;

export const CHART_AXIS_LABEL_STYLE = {
  fill: "hsl(var(--muted-foreground))",
  fontSize: 10,
  fontWeight: 600,
} as const;

export function getChartTooltipProps() {
  return {
    contentStyle: {
      background: "hsl(var(--card))",
      border: "1px solid hsl(var(--border))",
      borderRadius: "6px",
      color: "hsl(var(--foreground))",
      boxShadow: "none",
    },
    labelStyle: {
      color: "hsl(var(--foreground))",
      fontWeight: 600,
    },
    itemStyle: {
      color: "hsl(var(--foreground))",
      opacity: 1,
      fontWeight: 600,
    },
    cursor: {
      stroke: "hsl(var(--primary))",
      strokeOpacity: 0.24,
    },
    wrapperStyle: {
      outline: "none",
      zIndex: 30,
    },
  };
}
