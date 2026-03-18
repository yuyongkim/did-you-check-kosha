import { ApiMode, CalculationResponse, Discipline } from "@/lib/types";

interface CalculateOptions {
  apiMode: ApiMode;
  backendApiPrefix?: string;
}

function normalizePrefix(prefix: string): string {
  const trimmed = prefix.trim();
  if (!trimmed) return "";
  return trimmed.endsWith("/") ? trimmed.slice(0, -1) : trimmed;
}

function resolveEndpoint(discipline: Discipline, options: CalculateOptions): string {
  if (options.apiMode === "backend") {
    const prefix = normalizePrefix(options.backendApiPrefix ?? "");
    if (!prefix) {
      throw new Error("Backend API mode is enabled, but API prefix is empty.");
    }
    return `${prefix}/api/calculate/${discipline}`;
  }

  return `/api/calculate/${discipline}`;
}

export async function calculateDiscipline(
  discipline: Discipline,
  payload: Record<string, unknown>,
  options: CalculateOptions,
): Promise<CalculationResponse> {
  const endpoint = resolveEndpoint(discipline, options);
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let detail = `Calculation request failed: ${response.status}`;
    try {
      const body = (await response.json()) as { error?: string; detail?: string };
      if (body.error) detail = body.error;
      if (body.detail) detail = body.detail;
    } catch {
      // no-op
    }
    throw new Error(detail);
  }

  const calculation = (await response.json()) as CalculationResponse;

  if (calculation?.details && !calculation.details.regulatory) {
    try {
      const regulatoryResponse = await fetch(`/api/regulatory/${discipline}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          input: payload,
          calculation_response: calculation,
        }),
      });

      if (regulatoryResponse.ok) {
        const regulatoryBody = (await regulatoryResponse.json()) as {
          regulatory?: CalculationResponse["details"]["regulatory"];
        };
        if (regulatoryBody?.regulatory) {
          calculation.details.regulatory = regulatoryBody.regulatory;
        }
      }
    } catch {
      // Regulatory context is additive. Calculation response is returned even if enrichment fails.
    }
  }

  return calculation;
}

function resolveBackendPrefix(options: CalculateOptions): string {
  const prefix = normalizePrefix(options.backendApiPrefix ?? "");
  if (!prefix) {
    throw new Error("Backend API prefix is required.");
  }
  return prefix;
}

export async function createCalculationJob(
  discipline: Discipline,
  payload: Record<string, unknown>,
  options: CalculateOptions,
): Promise<{ job_id: string; status: string }> {
  const prefix = resolveBackendPrefix(options);
  const response = await fetch(`${prefix}/api/jobs/${discipline}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error(`Job create failed: ${response.status}`);
  return response.json() as Promise<{ job_id: string; status: string }>;
}

export async function getCalculationJob(
  jobId: string,
  options: CalculateOptions,
): Promise<Record<string, unknown>> {
  const prefix = resolveBackendPrefix(options);
  const response = await fetch(`${prefix}/api/jobs/${jobId}`);
  if (!response.ok) throw new Error(`Job fetch failed: ${response.status}`);
  return response.json() as Promise<Record<string, unknown>>;
}

export async function retryCalculationJob(jobId: string, options: CalculateOptions): Promise<Record<string, unknown>> {
  const prefix = resolveBackendPrefix(options);
  const response = await fetch(`${prefix}/api/jobs/${jobId}/retry`, { method: "POST" });
  if (!response.ok) throw new Error(`Job retry failed: ${response.status}`);
  return response.json() as Promise<Record<string, unknown>>;
}

export async function cancelAllCalculationJobs(options: CalculateOptions): Promise<Record<string, unknown>> {
  const prefix = resolveBackendPrefix(options);
  const response = await fetch(`${prefix}/api/jobs/cancel-all`, { method: "POST" });
  if (!response.ok) throw new Error(`Cancel-all failed: ${response.status}`);
  return response.json() as Promise<Record<string, unknown>>;
}

export async function listCalculationJobs(
  options: CalculateOptions,
  status?: string,
): Promise<Record<string, unknown>> {
  const prefix = resolveBackendPrefix(options);
  const query = status ? `?status=${encodeURIComponent(status)}` : "";
  const response = await fetch(`${prefix}/api/jobs${query}`);
  if (!response.ok) throw new Error(`List jobs failed: ${response.status}`);
  return response.json() as Promise<Record<string, unknown>>;
}

export async function listAuditLogs(
  options: CalculateOptions,
  limit = 50,
): Promise<Record<string, unknown>> {
  const prefix = resolveBackendPrefix(options);
  const response = await fetch(`${prefix}/api/audit/logs?limit=${Math.max(1, Math.min(limit, 2000))}`);
  if (!response.ok) throw new Error(`Audit logs failed: ${response.status}`);
  return response.json() as Promise<Record<string, unknown>>;
}

export async function getAuditSummary(options: CalculateOptions): Promise<Record<string, unknown>> {
  const prefix = resolveBackendPrefix(options);
  const response = await fetch(`${prefix}/api/audit/summary`);
  if (!response.ok) throw new Error(`Audit summary failed: ${response.status}`);
  return response.json() as Promise<Record<string, unknown>>;
}

export async function runSensitivityAnalysis(
  discipline: Discipline,
  body: Record<string, unknown>,
  options: CalculateOptions,
): Promise<Record<string, unknown>> {
  const prefix = resolveBackendPrefix(options);
  const response = await fetch(`${prefix}/api/analysis/sensitivity/${discipline}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) throw new Error(`Sensitivity analysis failed: ${response.status}`);
  return response.json() as Promise<Record<string, unknown>>;
}

export async function getPersistenceStats(options: CalculateOptions): Promise<Record<string, unknown>> {
  const prefix = resolveBackendPrefix(options);
  const response = await fetch(`${prefix}/api/perf/persistence-stats`);
  if (!response.ok) throw new Error(`Persistence stats failed: ${response.status}`);
  return response.json() as Promise<Record<string, unknown>>;
}

export async function downloadReportPackage(
  body: Record<string, unknown>,
  options: CalculateOptions,
): Promise<Blob> {
  const prefix = resolveBackendPrefix(options);
  const response = await fetch(`${prefix}/api/report/package`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) throw new Error(`Report package failed: ${response.status}`);
  return response.blob();
}
