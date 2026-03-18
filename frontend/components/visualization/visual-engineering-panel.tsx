"use client";

import { CalculationResponse, Discipline } from "@/lib/types";
import { CivilVisuals } from "@/components/visualization/civil-visuals";
import { ElectricalVisuals } from "@/components/visualization/electrical-visuals";
import { InstrumentationVisuals } from "@/components/visualization/instrumentation-visuals";
import { PipingVisuals } from "@/components/visualization/piping-visuals";
import { RotatingVisuals } from "@/components/visualization/rotating-visuals";
import { SteelVisuals } from "@/components/visualization/steel-visuals";
import { VesselVisuals } from "@/components/visualization/vessel-visuals";

export function VisualEngineeringPanel({
  discipline,
  result,
  previewInput,
}: {
  discipline: Discipline;
  result: CalculationResponse | null;
  previewInput?: Record<string, unknown>;
}) {
  if (discipline === "piping") return <PipingVisuals result={result} />;
  if (discipline === "vessel") return <VesselVisuals result={result} previewInput={previewInput} />;
  if (discipline === "rotating") return <RotatingVisuals result={result} />;
  if (discipline === "electrical") return <ElectricalVisuals result={result} />;
  if (discipline === "instrumentation") return <InstrumentationVisuals result={result} />;
  if (discipline === "steel") return <SteelVisuals result={result} />;
  return <CivilVisuals result={result} />;
}
