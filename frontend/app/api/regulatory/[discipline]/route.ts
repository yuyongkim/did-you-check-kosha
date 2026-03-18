import { NextRequest, NextResponse } from "next/server";

import { buildRegulatoryContext } from "@/lib/kosha-regulatory";
import { isDiscipline } from "@/lib/mock-data";
import { CalculationResponse } from "@/lib/types";

function hasCalculationShape(value: unknown): value is CalculationResponse {
  if (!value || typeof value !== "object") return false;
  const candidate = value as Partial<CalculationResponse>;
  return typeof candidate.discipline === "string" && !!candidate.details && !!candidate.flags;
}

export async function POST(
  request: NextRequest,
  context: { params: { discipline: string } },
) {
  const { discipline } = context.params;

  if (!isDiscipline(discipline)) {
    return NextResponse.json(
      { error: `Unsupported discipline: ${discipline}` },
      { status: 400 },
    );
  }

  let payload: Record<string, unknown> = {};
  try {
    payload = (await request.json()) as Record<string, unknown>;
  } catch {
    payload = {};
  }

  const input = (payload.input ?? {}) as Record<string, unknown>;
  const calculation = payload.calculation_response;

  if (!hasCalculationShape(calculation)) {
    return NextResponse.json(
      { error: "calculation_response payload is missing or invalid." },
      { status: 400 },
    );
  }

  const regulatory = await buildRegulatoryContext(discipline, input, calculation);
  return NextResponse.json({ regulatory });
}
