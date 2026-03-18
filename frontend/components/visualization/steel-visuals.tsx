"use client";

import { RadialBar, RadialBarChart, ResponsiveContainer } from "recharts";

import { useUiLanguage } from "@/hooks/useUiLanguage";
import { CalculationResponse } from "@/lib/types";
import { clamp, inputValue, resultValue } from "@/components/visualization/utils";
import { VisualSectionCard } from "@/components/visualization/visual-section-card";

type UiLanguage = "en" | "ko";

const STEEL_COPY: Record<UiLanguage, {
  sectionMember: string;
  sectionGauge: string;
  sectionService: string;
  kl: string;
  corrosionLoss: string;
  dcRatio: string;
  deflection: string;
  sectionLoss: string;
  reinforcementNeed: string;
  connectionStatus: string;
}> = {
  en: {
    sectionMember: "Member Schematic",
    sectionGauge: "D/C Utilization Gauge",
    sectionService: "Serviceability Checks",
    kl: "KL",
    corrosionLoss: "Corrosion loss",
    dcRatio: "D/C Ratio",
    deflection: "Deflection vs L/240",
    sectionLoss: "Section Loss",
    reinforcementNeed: "Reinforcement Need",
    connectionStatus: "Connection Status",
  },
  ko: {
    sectionMember: "부재 스케매틱",
    sectionGauge: "D/C 사용률 게이지",
    sectionService: "사용성 검토",
    kl: "KL",
    corrosionLoss: "부식 손실",
    dcRatio: "D/C 비율",
    deflection: "처짐 vs L/240",
    sectionLoss: "단면 손실",
    reinforcementNeed: "보강 필요도",
    connectionStatus: "접합부 상태",
  },
};

export function SteelVisuals({ result }: { result: CalculationResponse | null }) {
  const { language } = useUiLanguage();
  const copy = STEEL_COPY[language];

  const dcRatio = resultValue(result, "dc_ratio", 0.82);
  const corrosionLoss = resultValue(result, "corrosion_loss_percent", 8);
  const deflectionRatio = resultValue(result, "deflection_ratio", 0.45);
  const length = inputValue(result, "length_m", 6);
  const utilization = clamp(dcRatio * 100, 0, 180);
  const reinforcementNeed = String(result?.results.reinforcement_need ?? "—");
  const connectionStatus = String(result?.results.connection_status ?? "—");

  return (
    <div className="grid gap-3 lg:grid-cols-3">
      <VisualSectionCard title={copy.sectionMember}>
        <svg viewBox="0 0 280 210" className="h-[190px] w-full">
          <rect x="122" y="24" width="36" height="150" fill="none" stroke="hsl(var(--accent))" strokeWidth="6" />
          <line x1="80" y1="179" x2="200" y2="179" stroke="hsl(var(--foreground))" strokeWidth="2" />
          <line x1="90" y1="35" x2="190" y2="35" stroke="hsl(var(--danger))" strokeDasharray="4 3" strokeWidth="2" />
          <text x="14" y="18" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.kl}: {length.toFixed(1)} m</text>
          <text x="14" y="34" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.corrosionLoss}: {corrosionLoss.toFixed(1)}%</text>
        </svg>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionGauge}>
        <div className="h-[190px]">
          <ResponsiveContainer width="100%" height="100%">
            <RadialBarChart
              cx="50%"
              cy="50%"
              innerRadius="38%"
              outerRadius="85%"
              barSize={18}
              data={[{ name: "D/C", value: utilization, fill: "hsl(var(--accent))" }]}
            >
              <RadialBar background dataKey="value" />
            </RadialBarChart>
          </ResponsiveContainer>
        </div>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionService}>
        <div className="space-y-2 text-sm">
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.dcRatio}</p>
            <p className={dcRatio >= 1.5 ? "text-danger" : dcRatio >= 1.05 ? "text-warning" : "text-success"}>
              {dcRatio.toFixed(3)}
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.deflection}</p>
            <p className={deflectionRatio > 1 ? "text-warning" : "text-foreground"}>{deflectionRatio.toFixed(3)}</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.sectionLoss}</p>
            <p className={corrosionLoss >= 50 ? "text-danger" : corrosionLoss >= 20 ? "text-warning" : "text-foreground"}>
              {corrosionLoss.toFixed(1)}%
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.reinforcementNeed}</p>
            <p className={reinforcementNeed.includes("REPLACEMENT") ? "text-danger" : reinforcementNeed.includes("REINFORCEMENT") ? "text-warning" : "text-success"}>
              {reinforcementNeed.replace(/_/g, " ")}
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.connectionStatus}</p>
            <p className={connectionStatus.includes("FAILED") ? "text-danger" : connectionStatus.includes("REVIEW") ? "text-warning" : "text-success"}>
              {connectionStatus.replace(/_/g, " ")}
            </p>
          </div>
        </div>
      </VisualSectionCard>
    </div>
  );
}
