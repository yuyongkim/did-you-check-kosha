import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";

import { NextRequest, NextResponse } from "next/server";

import { KoshaRagQueryResponse } from "@/lib/rag/types";
import { Discipline } from "@/lib/types";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const DEFAULT_TOP_K = 6;
const MAX_TOP_K = 20;
const DEFAULT_MAX_CONTEXT = 5;
const DEFAULT_TIMEOUT_MS = 20000;
const LAW_SEARCH_BASE_URL = "https://www.law.go.kr/lsSc.do";

interface QueryBody {
  query?: unknown;
  discipline?: unknown;
  top_k?: unknown;
  topK?: unknown;
  generate?: unknown;
  model?: unknown;
  max_context?: unknown;
  maxContext?: unknown;
}

interface CommandResult {
  code: number | null;
  stdout: string;
  stderr: string;
  timedOut: boolean;
  commandError: string | null;
}

function parsePositiveInt(value: unknown, fallback: number): number {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) return fallback;
  return Math.max(1, Math.floor(parsed));
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

function toBoolean(value: unknown, fallback: boolean): boolean {
  if (typeof value === "boolean") return value;
  if (typeof value !== "string") return fallback;
  const normalized = value.trim().toLowerCase();
  if (["1", "true", "yes", "on"].includes(normalized)) return true;
  if (["0", "false", "no", "off"].includes(normalized)) return false;
  return fallback;
}

function normalizeDiscipline(value: unknown): Discipline | undefined {
  if (typeof value !== "string") return undefined;
  const normalized = value.trim().toLowerCase();
  if (
    normalized === "piping" ||
    normalized === "vessel" ||
    normalized === "rotating" ||
    normalized === "electrical" ||
    normalized === "instrumentation" ||
    normalized === "steel" ||
    normalized === "civil"
  ) {
    return normalized;
  }
  return undefined;
}

function resolveRepoRoot(): string {
  const cwd = process.cwd();
  const parent = path.resolve(cwd, "..");
  const scriptInCwd = path.resolve(cwd, "scripts", "kosha_rag_local.py");
  const scriptInParent = path.resolve(parent, "scripts", "kosha_rag_local.py");
  if (existsSync(scriptInCwd)) return cwd;
  if (existsSync(scriptInParent)) return parent;
  return cwd;
}

function resolveScriptPath(repoRoot: string): string {
  const configured = process.env.KOSHA_RAG_SCRIPT?.trim();
  if (configured) {
    if (path.isAbsolute(configured)) return configured;
    return path.resolve(repoRoot, configured);
  }
  return path.resolve(repoRoot, "scripts", "kosha_rag_local.py");
}

function resolveIndexPath(repoRoot: string): string {
  const configured = process.env.KOSHA_RAG_INDEX_PATH?.trim();
  if (configured) {
    if (path.isAbsolute(configured)) return configured;
    return path.resolve(repoRoot, configured);
  }
  return path.resolve(repoRoot, "datasets", "kosha_rag", "kosha_local_rag.sqlite3");
}

function parseJsonPayload(stdout: string): unknown {
  const trimmed = stdout.trim();
  if (!trimmed) {
    throw new Error("RAG command returned empty output.");
  }

  try {
    return JSON.parse(trimmed) as unknown;
  } catch {
    const lines = trimmed.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
    for (let idx = lines.length - 1; idx >= 0; idx -= 1) {
      try {
        return JSON.parse(lines[idx]) as unknown;
      } catch {
        // keep scanning tail lines
      }
    }
  }

  throw new Error("Failed to parse JSON payload from RAG command output.");
}

function isRagResponse(payload: unknown): payload is KoshaRagQueryResponse {
  if (!payload || typeof payload !== "object") return false;
  const candidate = payload as Partial<KoshaRagQueryResponse>;
  return (
    typeof candidate.query === "string" &&
    typeof candidate.top_k === "number" &&
    Array.isArray(candidate.hits)
  );
}

function looksLikeHttpUrl(value: string): boolean {
  const lowered = value.trim().toLowerCase();
  return lowered.startsWith("http://") || lowered.startsWith("https://");
}

function normalizeGuideNo(value: string): string {
  return value.trim().toUpperCase();
}

function extractGuideNoFromString(value: string): string | null {
  const normalized = normalizeGuideNo(value);
  const direct = normalized.match(/\b([A-Z](?:-[A-Z])?-\d{1,3}-\d{4})\b/);
  if (direct?.[1]) return direct[1];

  const fileBase = path.basename(normalized);
  const prefix = fileBase.split("__")[0];
  const prefixed = prefix.match(/^([A-Z](?:-[A-Z])?-\d{1,3}-\d{4})$/);
  if (prefixed?.[1]) return prefixed[1];

  return null;
}

function normalizeHitUrl(
  rawUrl: string | null | undefined,
  referenceCode: string,
): string | null {
  if (!rawUrl) return null;
  const trimmed = String(rawUrl).trim();
  if (!trimmed) return null;
  if (looksLikeHttpUrl(trimmed)) return trimmed;
  if (trimmed.startsWith("/api/")) return trimmed;

  // Local dataset file path -> app route proxy
  const normalizedPath = trimmed.replace(/\\/g, "/").toLowerCase();
  if (normalizedPath.includes("/datasets/kosha_guide/files/")) {
    const guideNo =
      extractGuideNoFromString(trimmed) || extractGuideNoFromString(referenceCode);
    if (guideNo) {
      return `/api/kosha/guide-file/${encodeURIComponent(guideNo)}`;
    }
  }

  return null;
}

function sanitizeRagResponse(payload: KoshaRagQueryResponse): KoshaRagQueryResponse {
  return {
    ...payload,
    hits: payload.hits.map((hit) => ({
      ...hit,
      url:
        normalizeHitUrl(hit.url, hit.reference_code) ??
        (hit.source_type === "law_article"
          ? `${LAW_SEARCH_BASE_URL}?query=${encodeURIComponent(hit.title || hit.reference_code || "산업안전보건법")}`
          : null),
    })),
  };
}

function runCommand(
  command: string,
  args: string[],
  cwd: string,
  timeoutMs: number,
): Promise<CommandResult> {
  return new Promise((resolve) => {
    const child = spawn(command, args, {
      cwd,
      windowsHide: true,
      env: {
        ...process.env,
        PYTHONUTF8: process.env.PYTHONUTF8 ?? "1",
        PYTHONIOENCODING: process.env.PYTHONIOENCODING ?? "utf-8",
      },
    });

    let stdout = "";
    let stderr = "";
    let timedOut = false;
    let commandError: string | null = null;

    const timer = setTimeout(() => {
      timedOut = true;
      child.kill();
    }, timeoutMs);

    child.stdout.on("data", (chunk: Buffer | string) => {
      stdout += chunk.toString();
    });
    child.stderr.on("data", (chunk: Buffer | string) => {
      stderr += chunk.toString();
    });
    child.on("error", (error) => {
      commandError = error.message;
    });
    child.on("close", (code) => {
      clearTimeout(timer);
      resolve({
        code,
        stdout,
        stderr,
        timedOut,
        commandError,
      });
    });
  });
}

function buildPythonCandidates(): string[] {
  const configured = process.env.KOSHA_RAG_PYTHON_BIN?.trim();
  const base = configured ? [configured] : ["python", "py"];
  return Array.from(new Set(base.filter(Boolean)));
}

function commandArgs(pythonBin: string, scriptPath: string, scriptArgs: string[]): string[] {
  if (path.basename(pythonBin).toLowerCase() === "py") {
    return ["-3", "-X", "utf8", scriptPath, ...scriptArgs];
  }
  return ["-X", "utf8", scriptPath, ...scriptArgs];
}

export async function POST(request: NextRequest) {
  const enabled = toBoolean(process.env.KOSHA_LOCAL_RAG_ENABLED ?? "true", true);
  if (!enabled) {
    return NextResponse.json(
      { error: "Local RAG is disabled (KOSHA_LOCAL_RAG_ENABLED=false)." },
      { status: 503 },
    );
  }

  let body: QueryBody = {};
  try {
    body = (await request.json()) as QueryBody;
  } catch {
    body = {};
  }

  const query = String(body.query ?? "").trim();
  if (!query) {
    return NextResponse.json({ error: "query is required." }, { status: 400 });
  }
  if (query.length > 400) {
    return NextResponse.json({ error: "query is too long (max 400 chars)." }, { status: 400 });
  }

  const discipline = normalizeDiscipline(body.discipline);
  const topK = clamp(
    parsePositiveInt(body.top_k ?? body.topK ?? process.env.KOSHA_RAG_DEFAULT_TOP_K, DEFAULT_TOP_K),
    1,
    MAX_TOP_K,
  );
  const generate = toBoolean(body.generate, toBoolean(process.env.KOSHA_RAG_GENERATE ?? "false", false));
  const model = String(body.model ?? process.env.KOSHA_RAG_MODEL ?? "qwen2.5:7b-instruct").trim();
  const maxContext = clamp(
    parsePositiveInt(
      body.max_context ?? body.maxContext ?? process.env.KOSHA_RAG_MAX_CONTEXT,
      DEFAULT_MAX_CONTEXT,
    ),
    1,
    MAX_TOP_K,
  );
  const timeoutMs = parsePositiveInt(process.env.KOSHA_RAG_QUERY_TIMEOUT_MS, DEFAULT_TIMEOUT_MS);

  const repoRoot = resolveRepoRoot();
  const scriptPath = resolveScriptPath(repoRoot);
  const indexPath = resolveIndexPath(repoRoot);

  if (!existsSync(scriptPath)) {
    return NextResponse.json(
      { error: `RAG script not found: ${scriptPath}` },
      { status: 500 },
    );
  }
  if (!existsSync(indexPath)) {
    return NextResponse.json(
      {
        error: "RAG index not found. Build it first with `python scripts/kosha_rag_local.py build --rebuild`.",
      },
      { status: 500 },
    );
  }

  const baseArgs = [
    "query",
    query,
    "--index-path",
    indexPath,
    "--top-k",
    String(topK),
    "--json-output",
  ];
  if (discipline) {
    baseArgs.push("--discipline", discipline);
  }
  if (generate) {
    baseArgs.push("--generate", "--model", model, "--max-context", String(maxContext));
  }

  const pythonCandidates = buildPythonCandidates();
  const errors: string[] = [];

  for (const candidate of pythonCandidates) {
    const result = await runCommand(
      candidate,
      commandArgs(candidate, scriptPath, baseArgs),
      repoRoot,
      timeoutMs,
    );

    if (result.timedOut) {
      return NextResponse.json(
        { error: `RAG query timeout after ${timeoutMs}ms.` },
        { status: 504 },
      );
    }

    if (result.code !== 0) {
      const detail = [result.commandError, result.stderr.trim()]
        .filter(Boolean)
        .join(" | ");
      errors.push(`${candidate}: ${detail || `exit code ${result.code ?? "unknown"}`}`);
      continue;
    }

    try {
      const payload = parseJsonPayload(result.stdout);
      if (!isRagResponse(payload)) {
        return NextResponse.json(
          { error: "RAG response shape is invalid." },
          { status: 500 },
        );
      }
      return NextResponse.json(sanitizeRagResponse(payload));
    } catch (error) {
      return NextResponse.json(
        {
          error: error instanceof Error ? error.message : "Failed to parse RAG response.",
          detail: result.stdout.slice(0, 500),
        },
        { status: 500 },
      );
    }
  }

  return NextResponse.json(
    {
      error: "Failed to run local RAG command.",
      detail: errors.join(" || ").slice(0, 1200),
    },
    { status: 500 },
  );
}
