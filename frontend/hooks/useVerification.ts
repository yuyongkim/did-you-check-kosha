"use client";

import { useMemo } from "react";

import { CalculationResponse } from "@/lib/types";

export function useVerification(result: CalculationResponse | null) {
  return useMemo(() => {
    if (!result) {
      return {
        blocked: false,
        layerSummary: [],
      };
    }

    const layers = result.details.layer_results.map((layer) => {
      const hasCriticalIssue = layer.issues.some((issue) => issue.severity === "critical" || issue.severity === "high");
      return {
        name: layer.layer,
        status: hasCriticalIssue ? "fail" : layer.passed ? "pass" : "warn",
        issues: layer.issues,
      };
    });

    return {
      blocked: result.flags.red_flags.length > 0 || result.status === "blocked",
      layerSummary: layers,
    };
  }, [result]);
}

