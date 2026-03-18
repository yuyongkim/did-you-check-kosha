import { NextRequest, NextResponse } from "next/server";

import { buildRegulatoryContext } from "@/lib/kosha-regulatory";
import { buildMockCalculationResponse, isDiscipline } from "@/lib/mock-data";

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

  const result = buildMockCalculationResponse(discipline, payload);
  result.details.regulatory = await buildRegulatoryContext(discipline, payload, result);
  return NextResponse.json(result);
}

