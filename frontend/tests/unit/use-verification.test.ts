import { renderHook } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { useVerification } from "@/hooks/useVerification";
import { CalculationResponse } from "@/lib/types";

const baseResult: CalculationResponse = {
  status: "success",
  discipline: "piping",
  results: {
    t_min_mm: 5.2,
    remaining_life_years: 7.1,
  },
  references: ["ASME B31.3 Table A-1"],
  verification: {
    confidence: "high",
    layers: [
      {
        layer: "Layer 1",
        passed: true,
        issues: [],
        details: {},
      },
    ],
  },
  flags: {
    red_flags: [],
    warnings: [],
  },
  details: {
    calculation_summary: {
      discipline: "piping",
      calculation_type: "remaining_life",
      standards_applied: ["ASME B31.3"],
      confidence: "high",
      execution_time_sec: 0.42,
    },
    input_data: {},
    calculation_steps: [],
    layer_results: [
      {
        layer: "Layer 1",
        passed: true,
        issues: [],
        details: {},
      },
      {
        layer: "Layer 2",
        passed: false,
        issues: [
          {
            code: "PHY.WARNING_CASE",
            severity: "medium",
            message: "warning",
          },
        ],
        details: {},
      },
      {
        layer: "Layer 3",
        passed: false,
        issues: [
          {
            code: "PHY.CRITICAL_CASE",
            severity: "high",
            message: "critical",
          },
        ],
        details: {},
      },
    ],
    final_results: {},
    recommendations: [],
    flags: {
      red_flags: [],
      warnings: [],
    },
  },
};

describe("useVerification", () => {
  it("returns empty summary for null result", () => {
    const { result } = renderHook(() => useVerification(null));
    expect(result.current.blocked).toBe(false);
    expect(result.current.layerSummary).toEqual([]);
  });

  it("maps layer statuses with fail/warn logic", () => {
    const { result } = renderHook(() => useVerification(baseResult));
    expect(result.current.blocked).toBe(false);
    expect(result.current.layerSummary[0].status).toBe("pass");
    expect(result.current.layerSummary[1].status).toBe("warn");
    expect(result.current.layerSummary[2].status).toBe("fail");
  });

  it("marks blocked when red flag exists", () => {
    const blockedResult: CalculationResponse = {
      ...baseResult,
      status: "blocked",
      flags: {
        red_flags: ["PHY.THICKNESS_BELOW_MINIMUM"],
        warnings: [],
      },
    };
    const { result } = renderHook(() => useVerification(blockedResult));
    expect(result.current.blocked).toBe(true);
  });
});
