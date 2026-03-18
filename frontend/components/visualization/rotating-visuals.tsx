"use client";

import { Bar, BarChart, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { useUiLanguage } from "@/hooks/useUiLanguage";
import { CalculationResponse } from "@/lib/types";
import { resultValue } from "@/components/visualization/utils";
import { VisualSectionCard } from "@/components/visualization/visual-section-card";
import { CHART_AXIS_LABEL_STYLE, CHART_AXIS_STROKE, CHART_TICK_STYLE, getChartTooltipProps } from "@/components/visualization/chart-theme";
import {
  ARRANGEMENT_LABEL,
  BEARING_LABEL,
  CASING_LABEL,
  CRITICALITY_LABEL,
  LUBE_LABEL,
  ROTATING_COPY,
  SEAL_LABEL,
} from "@/components/visualization/rotating-visuals-content";
import {
  driverLabel,
  enumLabel,
  indexVariant,
  machineLabel,
  processMode,
  spectrumData,
} from "@/components/visualization/rotating-visuals-utils";
import { Badge } from "@/components/ui/badge";

export function RotatingVisuals({ result }: { result: CalculationResponse | null }) {
  const { language } = useUiLanguage();
  const copy = ROTATING_COPY[language];

  const vibration = resultValue(result, "vibration_mm_per_s", 2.5);
  const baseLimit = resultValue(result, "vibration_limit_mm_per_s", 3.0);
  const adjustedLimit = resultValue(result, "adjusted_vibration_limit_mm_per_s", baseLimit);
  const nozzleRatio = resultValue(result, "nozzle_load_ratio", 0.85);
  const nozzleLimit = resultValue(result, "nozzle_load_limit_ratio", 1);
  const bearingTemp = resultValue(result, "bearing_temperature_c", 72);
  const oilTemp = resultValue(result, "lube_oil_supply_temp_c", 56);
  const speedRpm = resultValue(result, "speed_rpm", 1800);
  const speedLow = resultValue(result, "speed_low_limit_rpm", 600);
  const speedHigh = resultValue(result, "speed_high_limit_rpm", 8000);
  const mechIndex = resultValue(result, "mechanical_integrity_index", 8.5);
  const processIndex = resultValue(result, "process_stability_index", 8.9);
  const protectionIndex = resultValue(result, "protection_readiness_index", 8.8);
  const api670Coverage = resultValue(result, "api670_coverage_pct", 95);
  const tripTests = resultValue(result, "trip_tests_last_12m", 4);
  const expectedTests = resultValue(result, "expected_trip_tests_per_year", 4);

  const machineType = String(result?.results.machine_type ?? "pump");
  const driverType = String(result?.results.driver_type ?? "electric_motor_fixed");
  const criticality = String(result?.results.service_criticality ?? "normal");
  const stageCount = resultValue(result, "stage_count", 1);
  const trainArrangement = String(result?.results.train_arrangement ?? "overhung");
  const casingType = String(result?.results.casing_type ?? "horiz_split");
  const bearingType = String(result?.results.bearing_type ?? "rolling_element");
  const sealSystem = String(result?.results.seal_system ?? "single_mech");
  const lubeSystem = String(result?.results.lube_system ?? "ring_oil");
  const protectionBypass = Boolean(result?.results.protection_bypass_active);
  const monitoringEscalation = String(result?.results.monitoring_escalation ?? "—");
  const maintenanceUrgency = String(result?.results.maintenance_urgency ?? "—");

  const steamQuality = resultValue(result, "steam_quality_x", 1);
  const steamPressure = resultValue(result, "steam_pressure_bar", 0);
  const steamTemp = resultValue(result, "steam_temperature_c", 0);
  const steamSuperheatMargin = resultValue(result, "steam_superheat_margin_c", 0);
  const phaseRisk = resultValue(result, "phase_change_risk_index", 0);

  const suctionPressure = resultValue(result, "suction_pressure_bar", 0);
  const dischargePressure = resultValue(result, "discharge_pressure_bar", 0);
  const pressureRatio = resultValue(result, "pressure_ratio", 1);
  const surgeEvents = resultValue(result, "surge_events_30d", 0);

  const npshAvailable = resultValue(result, "npsh_available_m", 0);
  const npshRequired = resultValue(result, "npsh_required_m", 0);
  const npshMargin = resultValue(result, "npsh_margin_m", 0);

  const axialDisp = resultValue(result, "axial_displacement_um", 0);
  const axialLimit = resultValue(result, "axial_displacement_limit_um", 0);
  const misalignment = resultValue(result, "coupling_misalignment_mils", 0);

  const mode = processMode(machineType);
  const machineName = machineLabel(language, machineType);
  const driverName = driverLabel(language, driverType);
  const criticalityLabel = enumLabel(language, criticality, CRITICALITY_LABEL);
  const arrangementLabel = enumLabel(language, trainArrangement, ARRANGEMENT_LABEL);
  const casingLabel = enumLabel(language, casingType, CASING_LABEL);
  const bearingLabel = enumLabel(language, bearingType, BEARING_LABEL);
  const sealLabel = enumLabel(language, sealSystem, SEAL_LABEL);
  const lubeLabel = enumLabel(language, lubeSystem, LUBE_LABEL);
  const data = spectrumData(language, vibration);
  const tooltipProps = getChartTooltipProps();

  return (
    <div className="grid gap-3 xl:grid-cols-2 2xl:grid-cols-4">
      <VisualSectionCard title={copy.sectionTrain}>
        <div className="rounded-md border border-border bg-muted/35 p-2">
          <svg viewBox="0 0 520 170" className="h-[170px] w-full">
            <rect x="10" y="48" width="150" height="74" rx="8" fill="hsl(var(--card))" stroke="hsl(var(--border))" />
            <rect x="185" y="65" width="50" height="40" rx="6" fill="hsl(var(--muted))" stroke="hsl(var(--border))" />
            <rect x="260" y="38" width="180" height="94" rx="8" fill="hsl(var(--card))" stroke="hsl(var(--border))" />
            <line x1="160" y1="85" x2="185" y2="85" stroke="hsl(var(--secondary))" strokeWidth="4" />
            <line x1="235" y1="85" x2="260" y2="85" stroke="hsl(var(--secondary))" strokeWidth="4" />
            <line x1="36" y1="85" x2="430" y2="85" stroke="hsl(var(--primary))" strokeWidth="2" strokeDasharray="6 4" />
            <circle cx="305" cy="85" r="8" fill="hsl(var(--accent))" />
            <circle cx="392" cy="85" r="8" fill="hsl(var(--accent))" />
            <text x="85" y="93" textAnchor="middle" fontSize="11" fill="hsl(var(--muted-foreground))">{driverName}</text>
            <text x="210" y="89" textAnchor="middle" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.coupling}</text>
            <text x="350" y="93" textAnchor="middle" fontSize="11" fill="hsl(var(--muted-foreground))">{machineName}</text>
            <text x="12" y="18" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.arrangement}: {arrangementLabel} | {copy.stage}: {stageCount.toFixed(0)}</text>
            <text x="12" y="34" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.bearing}: {bearingLabel} | {copy.seal}: {sealLabel}</text>
            <text x="12" y="156" fontSize="11" fill="hsl(var(--muted-foreground))">{copy.casing}: {casingLabel} | {copy.lube}: {lubeLabel}</text>
          </svg>
        </div>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionSpectrum}>
        <div className="h-[210px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 8, right: 8, left: 4, bottom: 30 }}>
              <XAxis
                dataKey="band"
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                interval={0}
                minTickGap={0}
                label={{ value: copy.axisBand, position: "insideBottom", offset: -2, ...CHART_AXIS_LABEL_STYLE }}
              />
              <YAxis
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisAmplitude, angle: -90, position: "insideLeft", ...CHART_AXIS_LABEL_STYLE }}
              />
              <Tooltip {...tooltipProps} />
              <ReferenceLine y={baseLimit} stroke="hsl(var(--warning))" strokeDasharray="3 3" />
              <ReferenceLine y={adjustedLimit} stroke="hsl(var(--danger))" strokeDasharray="4 4" />
              <Bar dataKey="amp" fill="hsl(var(--accent))" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionFaultTimeline}>
        <div className="h-[210px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 8, right: 8, left: 4, bottom: 30 }}>
              <XAxis
                dataKey="band"
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                interval={0}
                minTickGap={0}
                label={{ value: copy.axisBand, position: "insideBottom", offset: -2, ...CHART_AXIS_LABEL_STYLE }}
              />
              <YAxis
                stroke={CHART_AXIS_STROKE}
                tick={CHART_TICK_STYLE}
                label={{ value: copy.axisAmplitude, angle: -90, position: "insideLeft", ...CHART_AXIS_LABEL_STYLE }}
              />
              <Tooltip {...tooltipProps} />
              <ReferenceLine y={adjustedLimit} stroke="hsl(var(--danger))" strokeDasharray="4 4" />
              <Line dataKey="amp" stroke="hsl(var(--warning))" strokeWidth={2.2} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionDriver}>
        <div className="space-y-2 text-sm">
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.machineDriverCrit}</p>
            <p className="font-data text-xs">{machineName} | {driverName} | {criticalityLabel}</p>
            <p className="font-data text-xs text-muted-foreground">{copy.stage} {stageCount.toFixed(0)} | {arrangementLabel} | {casingLabel}</p>
            <p className="font-data text-xs text-muted-foreground">{bearingLabel} | {sealLabel} | {lubeLabel}</p>
          </div>
          <div className="grid grid-cols-3 gap-2">
            <div className="rounded-md border border-border px-2 py-1">
              <p className="text-muted-foreground">{copy.mechanical}</p>
              <Badge variant={indexVariant(mechIndex)}>{mechIndex.toFixed(1)}</Badge>
            </div>
            <div className="rounded-md border border-border px-2 py-1">
              <p className="text-muted-foreground">{copy.process}</p>
              <Badge variant={indexVariant(processIndex)}>{processIndex.toFixed(1)}</Badge>
            </div>
            <div className="rounded-md border border-border px-2 py-1">
              <p className="text-muted-foreground">{copy.protection}</p>
              <Badge variant={indexVariant(protectionIndex)}>{protectionIndex.toFixed(1)}</Badge>
            </div>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.api670}</p>
            <p className={api670Coverage < 90 || tripTests < expectedTests ? "text-warning" : "text-success"}>
              {api670Coverage.toFixed(1)}% / {tripTests.toFixed(0)} ({copy.required} {expectedTests.toFixed(0)})
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.bearingOilAlign}</p>
            <p>{bearingTemp.toFixed(1)} &deg;C | {oilTemp.toFixed(1)} &deg;C | {misalignment.toFixed(1)} mils</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.speedEnvelope}</p>
            <p className={speedRpm < speedLow || speedRpm > speedHigh ? "text-warning" : "text-success"}>
              {speedRpm.toFixed(0)} rpm ({copy.limit} {speedLow.toFixed(0)}-{speedHigh.toFixed(0)})
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.protectionBypass}</p>
            <p className={protectionBypass ? "text-danger" : "text-success"}>{protectionBypass ? copy.active : copy.normal}</p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.monitoringEscalation}</p>
            <p className={monitoringEscalation.includes("CONTINUOUS") ? "text-danger" : monitoringEscalation.includes("WEEKLY") ? "text-warning" : "text-success"}>
              {monitoringEscalation.replace(/_/g, " ")}
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.maintenanceUrgency}</p>
            <p className={maintenanceUrgency.includes("IMMEDIATE") ? "text-danger" : maintenanceUrgency.includes("NEXT") ? "text-warning" : "text-success"}>
              {maintenanceUrgency.replace(/_/g, " ")}
            </p>
          </div>
        </div>
      </VisualSectionCard>

      <VisualSectionCard title={copy.sectionProcessRisk}>
        <div className="space-y-2 text-sm">
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.vibrationLimits}</p>
            <p className={vibration > adjustedLimit ? "text-warning" : "text-success"}>
              {vibration.toFixed(2)} ({copy.adjusted} {adjustedLimit.toFixed(2)}, {copy.base} {baseLimit.toFixed(2)})
            </p>
          </div>
          <div className="rounded-md border border-border px-2 py-1">
            <p className="text-muted-foreground">{copy.nozzleLoadRatio}</p>
            <p className={nozzleRatio > nozzleLimit ? "text-warning" : "text-success"}>
              {nozzleRatio.toFixed(2)} / {nozzleLimit.toFixed(2)}
            </p>
          </div>

          {mode === "steam" && (
            <>
              <div className="rounded-md border border-border px-2 py-1">
                <p className="text-muted-foreground">{copy.steamState}</p>
                <p>{steamPressure.toFixed(1)} bar / {steamTemp.toFixed(1)} &deg;C / x={steamQuality.toFixed(3)}</p>
              </div>
              <div className="rounded-md border border-border px-2 py-1">
                <p className="text-muted-foreground">{copy.phaseRiskSuperheat}</p>
                <p className={phaseRisk >= 7 || steamSuperheatMargin < 5 ? "text-danger" : "text-success"}>
                  {phaseRisk.toFixed(1)} /10 | {steamSuperheatMargin.toFixed(1)} C
                </p>
              </div>
            </>
          )}

          {mode === "compressor" && (
            <>
              <div className="rounded-md border border-border px-2 py-1">
                <p className="text-muted-foreground">{copy.suctionDischarge}</p>
                <p>{suctionPressure.toFixed(1)} bar / {dischargePressure.toFixed(1)} bar</p>
              </div>
              <div className="rounded-md border border-border px-2 py-1">
                <p className="text-muted-foreground">{copy.pressureRatioSurge}</p>
                <p className={pressureRatio > 4.5 || surgeEvents >= 1 ? "text-warning" : "text-success"}>
                  {pressureRatio.toFixed(2)} | {surgeEvents.toFixed(0)} {copy.in30d}
                </p>
              </div>
            </>
          )}

          {mode === "pump" && (
            <div className="rounded-md border border-border px-2 py-1">
              <p className="text-muted-foreground">{copy.npsh}</p>
              <p className={npshMargin < 1 ? "text-warning" : "text-success"}>
                {npshAvailable.toFixed(2)} / {npshRequired.toFixed(2)} / {npshMargin.toFixed(2)} m
              </p>
            </div>
          )}

          {(mode === "steam" || mode === "compressor") && axialLimit > 0 && (
            <div className="rounded-md border border-border px-2 py-1">
              <p className="text-muted-foreground">{copy.axialDisplacement}</p>
              <p className={axialDisp > axialLimit ? "text-warning" : "text-success"}>
                {axialDisp.toFixed(1)} / {axialLimit.toFixed(1)} um
              </p>
            </div>
          )}
        </div>
      </VisualSectionCard>
    </div>
  );
}
