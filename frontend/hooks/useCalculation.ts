"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import { calculateDiscipline } from "@/lib/api";
import { CalculationResponse, Discipline, RequestState, RunHistoryEntry } from "@/lib/types";
import { useWorkbenchStore } from "@/store/workbench-store";

function makeHeadline(response: CalculationResponse): string {
  const keys = Object.keys(response.results).slice(0, 2);
  if (keys.length === 0) return "No summary values";
  return keys
    .map((key) => `${key}: ${String(response.results[key])}`)
    .join(" | ");
}

export function useCalculation(discipline: Discipline) {
  const apiMode = useWorkbenchStore((state) => state.apiMode);
  const backendApiPrefix = useWorkbenchStore((state) => state.backendApiPrefix);
  const projectId = useWorkbenchStore((state) => state.activeProjectId);
  const assetId = useWorkbenchStore((state) => state.activeAssetId);
  const setStoreResult = useWorkbenchStore((state) => state.setResult);
  const appendRunHistory = useWorkbenchStore((state) => state.appendRunHistory);
  const storedResult = useWorkbenchStore((state) => state.resultByDiscipline[discipline] ?? null);

  const [requestState, setRequestState] = useState<RequestState>("idle");
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<CalculationResponse | null>(storedResult);

  useEffect(() => {
    setResult(storedResult);
  }, [storedResult]);

  const apiOptions = useMemo(
    () => ({
      apiMode,
      backendApiPrefix,
    }),
    [apiMode, backendApiPrefix],
  );

  const runCalculation = useCallback(
    async (input: Record<string, unknown>) => {
      const startedAt = performance.now();
      setRequestState("loading");
      setError(null);

      try {
        const response = await calculateDiscipline(discipline, input, apiOptions);
        const elapsedMs = Math.max(1, Math.round(performance.now() - startedAt));

        setResult(response);
        setStoreResult(discipline, response);
        setRequestState("success");

        const historyEntry: RunHistoryEntry = {
          id: `${discipline}-${Date.now()}`,
          timestamp: new Date().toISOString(),
          discipline,
          projectId,
          assetId,
          status: response.status,
          confidence: response.verification.confidence,
          elapsedMs,
          redFlagCount: response.flags.red_flags.length,
          warningCount: response.flags.warnings.length,
          headline: makeHeadline(response),
        };
        appendRunHistory(historyEntry);
        return response;
      } catch (err) {
        const message = err instanceof Error ? err.message : "Unexpected request error";
        setError(message);
        setRequestState("error");
        return null;
      }
    },
    [appendRunHistory, apiOptions, assetId, discipline, projectId, setStoreResult],
  );

  return {
    requestState,
    error,
    result,
    runCalculation,
  };
}
