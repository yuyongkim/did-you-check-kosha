"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { Discipline } from "@/lib/types";
import { useWorkbenchStore } from "@/store/workbench-store";

const NODE_LAYOUT: Array<{ discipline: Discipline; x: number; y: number; label: string }> = [
  { discipline: "piping", x: 70, y: 110, label: "PIP" },
  { discipline: "vessel", x: 160, y: 45, label: "VES" },
  { discipline: "rotating", x: 250, y: 110, label: "ROT" },
  { discipline: "electrical", x: 250, y: 210, label: "ELE" },
  { discipline: "instrumentation", x: 160, y: 270, label: "INS" },
  { discipline: "steel", x: 70, y: 210, label: "STL" },
  { discipline: "civil", x: 160, y: 160, label: "CIV" },
];

const LINKS: Array<[Discipline, Discipline]> = [
  ["piping", "vessel"],
  ["piping", "rotating"],
  ["rotating", "electrical"],
  ["instrumentation", "piping"],
  ["steel", "piping"],
  ["civil", "rotating"],
  ["steel", "electrical"],
];

export function CrossDisciplineImpactMapCard() {
  const { language } = useUiLanguage();
  const resultByDiscipline = useWorkbenchStore((state) => state.resultByDiscipline);

  const copy = language === "ko"
    ? {
        title: "Cross-Discipline Impact Map",
        subtitle: "공종 간 영향 관계와 현재 리스크 집중도를 표시합니다.",
        topRisks: "상위 리스크 공종",
      }
    : {
        title: "Cross-Discipline Impact Map",
        subtitle: "Visual relation map with current risk concentration.",
        topRisks: "Top risk disciplines",
      };

  const alertMap: Record<Discipline, number> = {
    piping: 0,
    vessel: 0,
    rotating: 0,
    electrical: 0,
    instrumentation: 0,
    steel: 0,
    civil: 0,
  };

  (Object.keys(alertMap) as Discipline[]).forEach((discipline) => {
    const result = resultByDiscipline[discipline];
    if (!result) return;
    alertMap[discipline] = result.flags.red_flags.length * 2 + result.flags.warnings.length;
  });

  const topRisks = (Object.entries(alertMap) as Array<[Discipline, number]>)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .filter(([, score]) => score > 0);

  function nodeColor(score: number): string {
    if (score >= 4) return "hsl(var(--danger))";
    if (score >= 1) return "hsl(var(--warning))";
    return "hsl(var(--success))";
  }

  function pos(discipline: Discipline) {
    return NODE_LAYOUT.find((item) => item.discipline === discipline)!;
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>{copy.title}</CardTitle>
        <p className="text-xs text-muted-foreground">{copy.subtitle}</p>
      </CardHeader>
      <CardContent>
        <div className="rounded-[8px] border border-border bg-background/40 p-2">
          <svg viewBox="0 0 320 320" className="h-[240px] w-full">
            {LINKS.map(([from, to]) => {
              const a = pos(from);
              const b = pos(to);
              return (
                <line
                  key={`${from}-${to}`}
                  x1={a.x}
                  y1={a.y}
                  x2={b.x}
                  y2={b.y}
                  stroke="hsl(var(--border))"
                  strokeWidth="1.5"
                />
              );
            })}

            {NODE_LAYOUT.map((node) => {
              const score = alertMap[node.discipline];
              return (
                <g key={node.discipline}>
                  <circle cx={node.x} cy={node.y} r="24" fill={nodeColor(score)} opacity="0.18" />
                  <circle cx={node.x} cy={node.y} r="16" fill={nodeColor(score)} />
                  <text x={node.x} y={node.y + 4} textAnchor="middle" fontSize="10" fill="white">
                    {node.label}
                  </text>
                </g>
              );
            })}
          </svg>
        </div>

        <div className="mt-2 rounded-[6px] border border-border bg-muted px-2 py-1 text-xs text-muted-foreground">
          {copy.topRisks}: {topRisks.length === 0 ? "-" : topRisks.map(([d, score]) => `${d}(${score})`).join(" | ")}
        </div>
      </CardContent>
    </Card>
  );
}
