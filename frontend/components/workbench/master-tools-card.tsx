"use client";

import { useEffect, useMemo, useRef, useState } from "react";

import { useUiLanguage } from "@/hooks/useUiLanguage";
import {
  calculateDiscipline,
  cancelAllCalculationJobs,
  createCalculationJob,
  downloadReportPackage,
  getAuditSummary,
  getCalculationJob,
  getPersistenceStats,
  listAuditLogs,
  listCalculationJobs,
  retryCalculationJob,
  runSensitivityAnalysis,
} from "@/lib/api";
import { ApiMode, CalculationResponse, Discipline, FormFieldConfig } from "@/lib/types";
import { useWorkbenchStore } from "@/store/workbench-store";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { usePagination } from "@/hooks/usePagination";
import { useLocalStorageState } from "@/hooks/useLocalStorageState";
import { PaginationControls } from "@/components/workbench/pagination-controls";
import { BackendOpsPanel } from "@/components/workbench/backend-ops-panel";
import { ExperienceModePanel, type ExperienceMode } from "@/components/workbench/experience-mode-panel";
import { ExpertQuickActions } from "@/components/workbench/expert-quick-actions";
import {
  buildBatchResultsCsv,
  buildBatchTemplateCsv,
  buildEvidencePackPayload,
  buildScenarioResultsCsv,
  buildSummaryClipboardText,
  bucketBatchRisk,
  filterBatchRows,
  filterScenarioRows,
  groupBatchErrors,
  sortBatchRows,
  sortScenarioRows,
  summarizeBatchRows,
  summarizeScenarioRows,
} from "@/components/workbench/master-tools-logic";
import type {
  BatchRow,
  BatchSortKey,
  MasterToolsFilter,
  ScenarioRow,
  ScenarioSortKey,
  SortDirection,
} from "@/components/workbench/master-tools-types";
import { OperationsOverviewPanel } from "@/components/workbench/operations-overview-panel";
import {
  buildScenarioFactors,
  download,
  parseCsv,
  resultRiskScore,
  runWithConcurrency,
  toPayload,
} from "@/components/workbench/master-tools-utils";

export function MasterToolsCard({
  discipline,
  fields,
  sampleInput,
  baseInput,
  activeResult,
}: {
  discipline: Discipline;
  fields: FormFieldConfig[];
  sampleInput: Record<string, unknown>;
  baseInput: Record<string, unknown>;
  activeResult: CalculationResponse | null;
}) {
  const { language } = useUiLanguage();
  const apiMode = useWorkbenchStore((state) => state.apiMode);
  const backendApiPrefix = useWorkbenchStore((state) => state.backendApiPrefix);
  const projectId = useWorkbenchStore((state) => state.activeProjectId);
  const assetId = useWorkbenchStore((state) => state.activeAssetId);
  const storagePrefix = `master-tools:${discipline}`;
  const [experienceMode, setExperienceMode] = useLocalStorageState<ExperienceMode>(`${storagePrefix}:experienceMode`, "beginner", {
    serialize: (value) => value,
    deserialize: (raw) => (raw === "expert" ? "expert" : "beginner"),
  });
  const [scenarioPageSize, setScenarioPageSize] = useLocalStorageState<number>(`${storagePrefix}:scenarioPageSize`, 8, {
    serialize: (value) => String(value),
    deserialize: (raw) => (Number.isFinite(Number(raw)) ? Number(raw) : 8),
  });
  const [batchPageSize, setBatchPageSize] = useLocalStorageState<number>(`${storagePrefix}:batchPageSize`, 8, {
    serialize: (value) => String(value),
    deserialize: (raw) => (Number.isFinite(Number(raw)) ? Number(raw) : 8),
  });

  const [scenarioField, setScenarioField] = useState<string>("");
  const [scenarioPct, setScenarioPct] = useState<number>(10);
  const [scenarioPoints, setScenarioPoints] = useLocalStorageState<number>(`${storagePrefix}:scenarioPoints`, 3, {
    serialize: (value) => String(value),
    deserialize: (raw) => (Number.isFinite(Number(raw)) ? Number(raw) : 3),
  });
  const [scenarioRunning, setScenarioRunning] = useState(false);
  const [scenarioRows, setScenarioRows] = useState<ScenarioRow[]>([]);
  const [scenarioProgress, setScenarioProgress] = useState({ done: 0, total: 0 });
  const scenarioAbortRef = useRef({ cancelled: false });
  const [scenarioFilter, setScenarioFilter] = useState<MasterToolsFilter>("all");
  const [scenarioSortKey, setScenarioSortKey] = useState<ScenarioSortKey>("risk");
  const [scenarioSortDir, setScenarioSortDir] = useState<SortDirection>("desc");
  const [selectedScenarioLabel, setSelectedScenarioLabel] = useState<string | null>(null);
  const [selectedScenarioLabels, setSelectedScenarioLabels] = useState<string[]>([]);

  const [batchCsv, setBatchCsv] = useLocalStorageState<string>(`${storagePrefix}:batchCsv`, "asset_id,project_id\nASSET-100,PROJECT-ALPHA", {
    serialize: (value) => value,
    deserialize: (raw) => raw,
  });
  const [batchMaxRows, setBatchMaxRows] = useLocalStorageState<number>(`${storagePrefix}:batchMaxRows`, 20, {
    serialize: (value) => String(value),
    deserialize: (raw) => (Number.isFinite(Number(raw)) ? Number(raw) : 20),
  });
  const [batchConcurrency, setBatchConcurrency] = useLocalStorageState<number>(`${storagePrefix}:batchConcurrency`, 4, {
    serialize: (value) => String(value),
    deserialize: (raw) => (Number.isFinite(Number(raw)) ? Number(raw) : 4),
  });
  const [batchRunning, setBatchRunning] = useState(false);
  const [batchRows, setBatchRows] = useState<BatchRow[]>([]);
  const [batchProgress, setBatchProgress] = useState({ done: 0, total: 0 });
  const batchAbortRef = useRef({ cancelled: false });
  const [batchFilter, setBatchFilter] = useState<MasterToolsFilter>("all");
  const [batchSortKey, setBatchSortKey] = useState<BatchSortKey>("risk");
  const [batchSortDir, setBatchSortDir] = useState<SortDirection>("desc");
  const [selectedBatchRowId, setSelectedBatchRowId] = useState<string | null>(null);
  const [selectedBatchRowIds, setSelectedBatchRowIds] = useState<string[]>([]);
  const [rerunKeys, setRerunKeys] = useState<string[]>([]);
  const [scenarioSearch, setScenarioSearch] = useState("");
  const [batchSearch, setBatchSearch] = useState("");
  const [copiedSummary, setCopiedSummary] = useState(false);
  const [riskMediumThreshold, setRiskMediumThreshold] = useLocalStorageState<number>(`${storagePrefix}:riskMediumThreshold`, 2, {
    serialize: (value) => String(value),
    deserialize: (raw) => (Number.isFinite(Number(raw)) ? Number(raw) : 2),
  });
  const [riskHighThreshold, setRiskHighThreshold] = useLocalStorageState<number>(`${storagePrefix}:riskHighThreshold`, 4, {
    serialize: (value) => String(value),
    deserialize: (raw) => (Number.isFinite(Number(raw)) ? Number(raw) : 4),
  });
  const [jobRunning, setJobRunning] = useState(false);
  const [jobId, setJobId] = useState("");
  const [jobStatus, setJobStatus] = useState("");
  const [jobResultPreview, setJobResultPreview] = useState<Record<string, unknown> | null>(null);
  const [sensitivityRunning, setSensitivityRunning] = useState(false);
  const [sensitivityRows, setSensitivityRows] = useState<Array<Record<string, unknown>>>([]);
  const [collabAuthor, setCollabAuthor] = useState("engineer");
  const [collabMessage, setCollabMessage] = useState("");
  const [collabLogs, setCollabLogs] = useState<string[]>([]);
  const [persistenceStats, setPersistenceStats] = useState<Record<string, unknown> | null>(null);
  const [reportBusy, setReportBusy] = useState(false);
  const [wsStreaming, setWsStreaming] = useState(false);
  const [wsMessages, setWsMessages] = useState<string[]>([]);
  const [recentJobs, setRecentJobs] = useState<Array<Record<string, unknown>>>([]);
  const [recentAudits, setRecentAudits] = useState<Array<Record<string, unknown>>>([]);
  const [auditSummary, setAuditSummary] = useState<Record<string, unknown> | null>(null);
  const [autoRefreshEnabled, setAutoRefreshEnabled] = useState(false);
  const runScenarioShortcutRef = useRef<() => void>(() => {});
  const runBatchShortcutRef = useRef<() => void>(() => {});
  const refreshJobsRef = useRef<() => void>(() => {});
  const refreshAuditsRef = useRef<() => void>(() => {});
  const refreshPersistenceRef = useRef<() => void>(() => {});
  const wsRef = useRef<WebSocket | null>(null);

  const copy = language === "ko"
    ? {
        title: "Master Tools",
        scenario: "Scenario Lab",
        scenarioHint: "선택 변수 ±변동 케이스를 병렬 실행해 결과를 비교합니다.",
        scenarioField: "변동 변수",
        scenarioPct: "변동률(%)",
        scenarioPoints: "시나리오 포인트",
        runScenario: "시나리오 실행",
        batch: "Batch Screening",
        batchHint: "CSV 입력을 다건 병렬 실행하고 위험 점수 순으로 정렬합니다.",
        runBatch: "배치 실행",
        maxRows: "최대 행 수",
        concurrency: "병렬 수",
        template: "CSV 템플릿",
        exportPack: "Evidence Pack 내보내기",
        exportHint: "활성 결과 + 시나리오 + 배치 결과를 Markdown/JSON으로 저장합니다.",
        running: "실행 중...",
        cancel: "중단",
        progress: "진행률",
        noRows: "아직 결과가 없습니다.",
        summary: "요약",
        filter: "필터",
        all: "전체",
        success: "성공",
        error: "오류",
        highRisk: "고위험",
        sort: "정렬",
        exportCsv: "필터 결과 CSV",
        status: "상태",
        risk: "리스크",
        confidence: "신뢰도",
        red: "Red",
        warn: "Warn",
        errorGroup: "오류 그룹",
        actions: "액션",
        rerun: "재실행",
        detail: "상세",
        close: "닫기",
        page: "페이지",
        prev: "이전",
        next: "다음",
        select: "선택",
        selectPage: "페이지 전체 선택",
        clearSelection: "선택 해제",
        rerunSelected: "선택 재실행",
        rerunFailed: "실패 재실행",
        clearResults: "결과 지우기",
        riskHeatmap: "리스크 히트맵",
        low: "저",
        medium: "중",
        high: "고",
        search: "검색",
        importCsv: "CSV 파일 불러오기",
        riskThresholds: "리스크 임계값(M/H)",
        copyMd: "결과 요약 복사",
        copied: "복사됨",
        backendOps: "Backend Ops",
        queueRun: "Job 큐 실행",
        queuePoll: "상태 갱신",
        sensitivityRun: "민감도 실행",
        collabLog: "협업 로그",
        addNote: "노트 추가",
        persistence: "영속 통계",
        packageZip: "ZIP 패키지 받기",
        streamStart: "WS 스트림 시작",
        streamStop: "WS 스트림 중지",
        jobsRefresh: "잡 목록 새로고침",
        auditRefresh: "감사로그 새로고침",
        retryLast: "최근 잡 재시도",
        cancelAll: "전체 취소",
        autoRefresh: "자동새로고침",
        autoOn: "켜짐",
        autoOff: "꺼짐",
      }
    : {
        title: "Master Tools",
        scenario: "Scenario Lab",
        scenarioHint: "Run ±change variants in parallel and compare outcomes.",
        scenarioField: "Variable",
        scenarioPct: "Change (%)",
        scenarioPoints: "Scenario points",
        runScenario: "Run Scenario",
        batch: "Batch Screening",
        batchHint: "Run CSV rows in parallel and rank by risk score.",
        runBatch: "Run Batch",
        maxRows: "Max rows",
        concurrency: "Concurrency",
        template: "CSV template",
        exportPack: "Export Evidence Pack",
        exportHint: "Export active + scenario + batch evidence in Markdown/JSON.",
        running: "Running...",
        cancel: "Cancel",
        progress: "Progress",
        noRows: "No results yet.",
        summary: "Summary",
        filter: "Filter",
        all: "All",
        success: "Success",
        error: "Error",
        highRisk: "High Risk",
        sort: "Sort",
        exportCsv: "Filtered CSV",
        status: "Status",
        risk: "Risk",
        confidence: "Confidence",
        red: "Red",
        warn: "Warn",
        errorGroup: "Error groups",
        actions: "Actions",
        rerun: "Rerun",
        detail: "Detail",
        close: "Close",
        page: "Page",
        prev: "Prev",
        next: "Next",
        select: "Select",
        selectPage: "Select Page",
        clearSelection: "Clear Selection",
        rerunSelected: "Rerun Selected",
        rerunFailed: "Rerun Failed",
        clearResults: "Clear Results",
        riskHeatmap: "Risk Heatmap",
        low: "Low",
        medium: "Medium",
        high: "High",
        search: "Search",
        importCsv: "Import CSV file",
        riskThresholds: "Risk thresholds (M/H)",
        copyMd: "Copy summary",
        copied: "Copied",
        backendOps: "Backend Ops",
        queueRun: "Run queued job",
        queuePoll: "Refresh status",
        sensitivityRun: "Run sensitivity",
        collabLog: "Collab log",
        addNote: "Add note",
        persistence: "Persistence",
        packageZip: "Download ZIP package",
        streamStart: "Start WS stream",
        streamStop: "Stop WS stream",
        jobsRefresh: "Refresh jobs",
        auditRefresh: "Refresh audit",
        retryLast: "Retry latest",
        cancelAll: "Cancel all",
        autoRefresh: "Auto refresh",
        autoOn: "ON",
        autoOff: "OFF",
      };

  const numericFields = useMemo(() => fields.filter((field) => field.type === "number"), [fields]);
  const apiOptions = useMemo(() => ({ apiMode, backendApiPrefix }), [apiMode, backendApiPrefix]);
  const backendEnabled = apiMode === "backend" && backendApiPrefix.trim().length > 0;

  const scenarioSummary = useMemo(() => summarizeScenarioRows(scenarioRows), [scenarioRows]);
  const filteredScenarioRows = useMemo(
    () => filterScenarioRows(scenarioRows, scenarioFilter, scenarioSearch, riskHighThreshold),
    [riskHighThreshold, scenarioFilter, scenarioRows, scenarioSearch],
  );
  const sortedFilteredScenarioRows = useMemo(
    () => sortScenarioRows(filteredScenarioRows, scenarioSortKey, scenarioSortDir),
    [filteredScenarioRows, scenarioSortDir, scenarioSortKey],
  );
  const scenarioPagination = usePagination(sortedFilteredScenarioRows, Math.max(4, Math.min(20, scenarioPageSize)));

  const batchSummary = useMemo(() => summarizeBatchRows(batchRows), [batchRows]);
  const filteredBatchRows = useMemo(
    () => filterBatchRows(batchRows, batchFilter, batchSearch, riskHighThreshold),
    [batchFilter, batchRows, batchSearch, riskHighThreshold],
  );
  const batchErrorGroups = useMemo(() => groupBatchErrors(batchRows), [batchRows]);
  const sortedFilteredBatchRows = useMemo(
    () => sortBatchRows(filteredBatchRows, batchSortKey, batchSortDir),
    [batchSortDir, batchSortKey, filteredBatchRows],
  );
  const batchPagination = usePagination(sortedFilteredBatchRows, Math.max(4, Math.min(20, batchPageSize)));
  const selectedScenario = useMemo(
    () => sortedFilteredScenarioRows.find((row) => row.label === selectedScenarioLabel) ?? null,
    [selectedScenarioLabel, sortedFilteredScenarioRows],
  );
  const selectedBatch = useMemo(
    () => sortedFilteredBatchRows.find((row) => row.rowId === selectedBatchRowId) ?? null,
    [selectedBatchRowId, sortedFilteredBatchRows],
  );
  const batchRiskBuckets = useMemo(
    () => bucketBatchRisk(batchRows, riskMediumThreshold, riskHighThreshold),
    [batchRows, riskHighThreshold, riskMediumThreshold],
  );
  const auditTotal = Number((auditSummary as { total?: number } | null)?.total ?? 0);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (!(event.ctrlKey || event.metaKey)) return;
      if (event.shiftKey && event.key === "Enter") {
        event.preventDefault();
        runScenarioShortcutRef.current();
        return;
      }
      if (!event.shiftKey && event.key === "Enter") {
        event.preventDefault();
        runBatchShortcutRef.current();
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  useEffect(() => {
    if (!backendEnabled) return;
    let mounted = true;
    (async () => {
      try {
        const stats = await getPersistenceStats(apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
        if (mounted) setPersistenceStats(stats);
      } catch {
        if (mounted) setPersistenceStats(null);
      }
      try {
        const jobs = await listCalculationJobs(apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
        const rows = Array.isArray(jobs.jobs) ? (jobs.jobs as Array<Record<string, unknown>>) : [];
        if (mounted) setRecentJobs(rows.slice(0, 8));
      } catch {
        if (mounted) setRecentJobs([]);
      }
      try {
        const audits = await listAuditLogs(apiOptions as { apiMode: ApiMode; backendApiPrefix?: string }, 20);
        const rows = Array.isArray(audits.logs) ? (audits.logs as Array<Record<string, unknown>>) : [];
        if (mounted) setRecentAudits(rows.slice(0, 8));
      } catch {
        if (mounted) setRecentAudits([]);
      }
      try {
        const summary = await getAuditSummary(apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
        if (mounted) setAuditSummary(summary);
      } catch {
        if (mounted) setAuditSummary(null);
      }
    })();
    return () => {
      mounted = false;
    };
  }, [apiOptions, backendEnabled, batchRows.length, scenarioRows.length]); // intentional lightweight refresh trigger

  useEffect(() => () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  useEffect(() => {
    if (!backendEnabled || !autoRefreshEnabled) return;
    const timer = window.setInterval(() => {
      refreshJobsRef.current();
      refreshAuditsRef.current();
      refreshPersistenceRef.current();
    }, 5000);
    return () => window.clearInterval(timer);
  }, [autoRefreshEnabled, backendEnabled]); // keep interval stable

  async function runScenarioLab() {
    if (!scenarioField) return;
    scenarioAbortRef.current.cancelled = false;
    setScenarioRunning(true);

    const base = Number(baseInput[scenarioField] ?? sampleInput[scenarioField] ?? 0);
    const factors = buildScenarioFactors(scenarioPoints, scenarioPct);
    setScenarioProgress({ done: 0, total: factors.length });

    const rows = await Promise.all(factors.map(async (factor) => {
      const next = Number.isFinite(base) ? Number((base * factor).toFixed(5)) : base;
      const payload = { ...sampleInput, ...baseInput, [scenarioField]: next };
      const label = `${scenarioField}=${next}`;

      if (scenarioAbortRef.current.cancelled) {
        setScenarioProgress((prev) => ({ ...prev, done: prev.done + 1 }));
        return { label, payload, result: null, error: "cancelled" } as ScenarioRow;
      }

      try {
        const result = await calculateDiscipline(discipline, payload, apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
        setScenarioProgress((prev) => ({ ...prev, done: prev.done + 1 }));
        return { label, payload, result } as ScenarioRow;
      } catch (error) {
        setScenarioProgress((prev) => ({ ...prev, done: prev.done + 1 }));
        return {
          label,
          payload,
          result: null,
          error: error instanceof Error ? error.message : "scenario failed",
        } as ScenarioRow;
      }
    }));

    setScenarioRows(rows);
    scenarioPagination.reset();
    setScenarioRunning(false);
  }

  async function runBatchScreening() {
    batchAbortRef.current.cancelled = false;
    setBatchRunning(true);

    const parsed = parseCsv(batchCsv).slice(0, Math.max(1, batchMaxRows));
    setBatchProgress({ done: 0, total: parsed.length });
    const rows = await runWithConcurrency(parsed, Math.max(1, Math.min(batchConcurrency, 10)), async (row, index) => {
      const rowId = row.asset_id || row.assetId || `row-${index + 1}`;
      if (batchAbortRef.current.cancelled) {
        setBatchProgress((prev) => ({ ...prev, done: prev.done + 1 }));
        return { rowId, payload: toPayload(row, fields, sampleInput), result: null, error: "cancelled" } as BatchRow;
      }

      const payload = toPayload(row, fields, sampleInput);
      try {
        const result = await calculateDiscipline(discipline, payload, apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
        setBatchProgress((prev) => ({ ...prev, done: prev.done + 1 }));
        return {
          rowId,
          payload,
          result,
        } as BatchRow;
      } catch (error) {
        setBatchProgress((prev) => ({ ...prev, done: prev.done + 1 }));
        return {
          rowId,
          payload,
          result: null,
          error: error instanceof Error ? error.message : "batch failed",
        } as BatchRow;
      }
    });

    const sorted = [...rows].sort((left, right) => {
      const leftScore = left.result ? resultRiskScore(left.result) : -1;
      const rightScore = right.result ? resultRiskScore(right.result) : -1;
      return rightScore - leftScore;
    });

    setBatchRows(sorted);
    batchPagination.reset();
    setBatchRunning(false);
  }

  function cancelScenarioRun() {
    scenarioAbortRef.current.cancelled = true;
  }

  function cancelBatchRun() {
    batchAbortRef.current.cancelled = true;
  }

  function markRerunStart(key: string) {
    setRerunKeys((prev) => (prev.includes(key) ? prev : [...prev, key]));
  }

  function markRerunEnd(key: string) {
    setRerunKeys((prev) => prev.filter((item) => item !== key));
  }

  async function rerunScenarioRow(label: string) {
    const target = scenarioRows.find((row) => row.label === label);
    if (!target?.payload) return;
    const key = `scenario:${label}`;
    markRerunStart(key);
    try {
      const result = await calculateDiscipline(discipline, target.payload, apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
      setScenarioRows((prev) => prev.map((row) => (
        row.label === label ? { ...row, result, error: undefined } : row
      )));
    } catch (error) {
      const message = error instanceof Error ? error.message : "rerun failed";
      setScenarioRows((prev) => prev.map((row) => (
        row.label === label ? { ...row, result: null, error: message } : row
      )));
    } finally {
      markRerunEnd(key);
    }
  }

  async function rerunBatchRow(rowId: string) {
    const target = batchRows.find((row) => row.rowId === rowId);
    if (!target?.payload) return;
    const key = `batch:${rowId}`;
    markRerunStart(key);
    try {
      const result = await calculateDiscipline(discipline, target.payload, apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
      setBatchRows((prev) => prev.map((row) => (
        row.rowId === rowId ? { ...row, result, error: undefined } : row
      )));
    } catch (error) {
      const message = error instanceof Error ? error.message : "rerun failed";
      setBatchRows((prev) => prev.map((row) => (
        row.rowId === rowId ? { ...row, result: null, error: message } : row
      )));
    } finally {
      markRerunEnd(key);
    }
  }

  async function rerunSelectedScenarioRows() {
    await Promise.all(selectedScenarioLabels.map(async (label) => rerunScenarioRow(label)));
  }

  async function rerunSelectedBatchRows() {
    await Promise.all(selectedBatchRowIds.map(async (rowId) => rerunBatchRow(rowId)));
  }

  async function rerunFailedScenarioRows() {
    const failedLabels = scenarioRows.filter((row) => Boolean(row.error)).map((row) => row.label);
    await Promise.all(failedLabels.map(async (label) => rerunScenarioRow(label)));
  }

  async function rerunFailedBatchRows() {
    const failedRowIds = batchRows.filter((row) => Boolean(row.error)).map((row) => row.rowId);
    await Promise.all(failedRowIds.map(async (rowId) => rerunBatchRow(rowId)));
  }

  function clearScenarioResults() {
    setScenarioRows([]);
    setScenarioProgress({ done: 0, total: 0 });
    setSelectedScenarioLabels([]);
    setSelectedScenarioLabel(null);
    scenarioPagination.reset();
  }

  function clearBatchResults() {
    setBatchRows([]);
    setBatchProgress({ done: 0, total: 0 });
    setSelectedBatchRowIds([]);
    setSelectedBatchRowId(null);
    batchPagination.reset();
  }

  async function runQueuedJob() {
    if (!backendEnabled) return;
    setJobRunning(true);
    try {
      const created = await createCalculationJob(discipline, { ...sampleInput, ...baseInput }, apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
      setJobId(created.job_id);
      setJobStatus(created.status);
      for (let index = 0; index < 80; index += 1) {
        const job = await getCalculationJob(created.job_id, apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
        const status = String(job.status ?? "");
        setJobStatus(status);
        if (status === "success" || status === "error" || status === "cancelled") {
          const result = (job.result as Record<string, unknown> | null) ?? null;
          setJobResultPreview(result);
          break;
        }
        await new Promise((resolve) => {
          window.setTimeout(resolve, 250);
        });
      }
    } catch (error) {
      setJobStatus(error instanceof Error ? error.message : "job failed");
    } finally {
      setJobRunning(false);
    }
  }

  async function refreshJobStatus() {
    if (!backendEnabled || !jobId) return;
    try {
      const job = await getCalculationJob(jobId, apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
      setJobStatus(String(job.status ?? ""));
      const result = (job.result as Record<string, unknown> | null) ?? null;
      setJobResultPreview(result);
    } catch (error) {
      setJobStatus(error instanceof Error ? error.message : "refresh failed");
    }
  }

  async function runSensitivity() {
    if (!backendEnabled || !scenarioField) return;
    setSensitivityRunning(true);
    try {
      const response = await runSensitivityAnalysis(
        discipline,
        {
          base_input: { ...sampleInput, ...baseInput },
          variable: scenarioField,
          delta_pct: scenarioPct,
          points: scenarioPoints,
        },
        apiOptions as { apiMode: ApiMode; backendApiPrefix?: string },
      );
      const rows = Array.isArray(response.rows) ? (response.rows as Array<Record<string, unknown>>) : [];
      setSensitivityRows(rows);
    } catch {
      setSensitivityRows([]);
    } finally {
      setSensitivityRunning(false);
    }
  }

  async function addCollabNote() {
    const trimmed = collabMessage.trim();
    if (!backendEnabled || !trimmed) return;
    try {
      const prefix = backendApiPrefix.replace(/\/+$/, "");
      const response = await fetch(
        `${prefix}/api/collab/${discipline}/${encodeURIComponent(projectId)}/${encodeURIComponent(assetId)}/comments`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ author: collabAuthor || "engineer", message: trimmed }),
        },
      );
      if (response.ok) {
        setCollabLogs((prev) => [`${new Date().toISOString()} | ${collabAuthor}: ${trimmed}`, ...prev].slice(0, 20));
        setCollabMessage("");
      }
    } catch {
      // noop
    }
  }

  async function refreshPersistenceStats() {
    if (!backendEnabled) return;
    try {
      const stats = await getPersistenceStats(apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
      setPersistenceStats(stats);
    } catch {
      setPersistenceStats(null);
    }
  }

  async function downloadBackendPackage() {
    if (!backendEnabled) return;
    setReportBusy(true);
    try {
      const blob = await downloadReportPackage(
        {
          discipline,
          project_id: projectId,
          asset_id: assetId,
          active_result: activeResult,
          scenario_results: scenarioRows.map((row) => ({
            label: row.label,
            status: row.result?.status ?? "error",
            error: row.error,
          })),
          batch_results: batchRows.map((row) => ({
            rowId: row.rowId,
            status: row.result?.status ?? "error",
            error: row.error,
          })),
        },
        apiOptions as { apiMode: ApiMode; backendApiPrefix?: string },
      );
      const url = window.URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `backend_report_${discipline}_${Date.now()}.zip`;
      document.body.append(anchor);
      anchor.click();
      anchor.remove();
      window.setTimeout(() => window.URL.revokeObjectURL(url), 1000);
    } catch {
      // noop
    } finally {
      setReportBusy(false);
    }
  }

  async function refreshRecentJobs() {
    if (!backendEnabled) return;
    try {
      const body = await listCalculationJobs(apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
      const rows = Array.isArray(body.jobs) ? (body.jobs as Array<Record<string, unknown>>) : [];
      setRecentJobs(rows.slice(0, 8));
    } catch {
      setRecentJobs([]);
    }
  }

  async function refreshRecentAudits() {
    if (!backendEnabled) return;
    try {
      const body = await listAuditLogs(apiOptions as { apiMode: ApiMode; backendApiPrefix?: string }, 20);
      const rows = Array.isArray(body.logs) ? (body.logs as Array<Record<string, unknown>>) : [];
      setRecentAudits(rows.slice(0, 8));
      const summary = await getAuditSummary(apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
      setAuditSummary(summary);
    } catch {
      setRecentAudits([]);
      setAuditSummary(null);
    }
  }

  async function retryLatestJob() {
    if (!backendEnabled || recentJobs.length === 0) return;
    const latestId = String(recentJobs[0]?.job_id ?? "");
    if (!latestId) return;
    try {
      const retried = await retryCalculationJob(latestId, apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
      const nextJobId = String(retried.job_id ?? "");
      if (nextJobId) setJobId(nextJobId);
      await refreshRecentJobs();
    } catch {
      // noop
    }
  }

  async function cancelAllJobs() {
    if (!backendEnabled) return;
    try {
      await cancelAllCalculationJobs(apiOptions as { apiMode: ApiMode; backendApiPrefix?: string });
      await refreshRecentJobs();
    } catch {
      // noop
    }
  }

  function stopJobStream() {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setWsStreaming(false);
  }

  function startJobStream() {
    if (!backendEnabled || !jobId || typeof window === "undefined") return;
    stopJobStream();
    const prefix = backendApiPrefix.replace(/\/+$/, "");
    const wsUrl = prefix.replace(/^http/i, "ws");
    const socket = new WebSocket(`${wsUrl}/ws/jobs/${jobId}`);
    wsRef.current = socket;
    setWsStreaming(true);

    socket.onmessage = (event) => {
      const line = `${new Date().toISOString()} | ${event.data}`;
      setWsMessages((prev) => [line, ...prev].slice(0, 20));
      try {
        const parsed = JSON.parse(event.data) as { status?: string; result?: Record<string, unknown> };
        if (parsed.status) setJobStatus(parsed.status);
        if (parsed.result && typeof parsed.result === "object") setJobResultPreview(parsed.result);
        if (parsed.status && ["success", "error", "cancelled", "not_found"].includes(parsed.status)) {
          stopJobStream();
        }
      } catch {
        // noop
      }
    };
    socket.onerror = () => {
      setWsMessages((prev) => [`${new Date().toISOString()} | websocket error`, ...prev].slice(0, 20));
      stopJobStream();
    };
    socket.onclose = () => {
      setWsStreaming(false);
    };
  }

  function exportEvidencePack() {
    if (!activeResult && scenarioRows.length === 0 && batchRows.length === 0) return;

    const { pack, markdown } = buildEvidencePackPayload({
      discipline,
      projectId,
      assetId,
      batchMaxRows,
      batchConcurrency,
      activeResult,
      scenarioRows,
      batchRows,
    });
    const stamp = Date.now();
    download(markdown, `evidence_pack_${discipline}_${stamp}.md`, "text/markdown;charset=utf-8");
    download(JSON.stringify(pack, null, 2), `evidence_pack_${discipline}_${stamp}.json`, "application/json;charset=utf-8");
  }

  async function copyCurrentSummary() {
    if (typeof navigator === "undefined" || !navigator.clipboard) return;
    const text = buildSummaryClipboardText({
      activeResult,
      scenarioSummary,
      batchSummary,
      discipline,
      projectId,
      assetId,
    });
    try {
      await navigator.clipboard.writeText(text);
      setCopiedSummary(true);
      window.setTimeout(() => setCopiedSummary(false), 1200);
    } catch {
      // noop
    }
  }

  function downloadTemplate() {
    download(buildBatchTemplateCsv(fields, sampleInput), `batch_template_${discipline}.csv`, "text/csv;charset=utf-8");
  }

  function exportFilteredScenarioCsv() {
    download(buildScenarioResultsCsv(sortedFilteredScenarioRows), `scenario_results_${discipline}_${Date.now()}.csv`, "text/csv;charset=utf-8");
  }

  function exportFilteredBatchCsv() {
    download(buildBatchResultsCsv(sortedFilteredBatchRows), `batch_results_${discipline}_${Date.now()}.csv`, "text/csv;charset=utf-8");
  }

  runScenarioShortcutRef.current = () => {
    if (!scenarioRunning && scenarioField) void runScenarioLab();
  };
  runBatchShortcutRef.current = () => {
    if (!batchRunning) void runBatchScreening();
  };
  refreshJobsRef.current = () => {
    void refreshRecentJobs();
  };
  refreshAuditsRef.current = () => {
    void refreshRecentAudits();
  };
  refreshPersistenceRef.current = () => {
    void refreshPersistenceStats();
  };

  function toggleScenarioSelection(label: string) {
    setSelectedScenarioLabels((prev) => (prev.includes(label) ? prev.filter((item) => item !== label) : [...prev, label]));
  }

  function toggleBatchSelection(rowId: string) {
    setSelectedBatchRowIds((prev) => (prev.includes(rowId) ? prev.filter((item) => item !== rowId) : [...prev, rowId]));
  }

  function selectAllScenarioOnPage() {
    const labels = scenarioPagination.paged.map((row) => row.label);
    setSelectedScenarioLabels((prev) => Array.from(new Set([...prev, ...labels])));
  }

  function selectAllBatchOnPage() {
    const ids = batchPagination.paged.map((row) => row.rowId);
    setSelectedBatchRowIds((prev) => Array.from(new Set([...prev, ...ids])));
  }

  function importBatchCsvFile(event: { target: { files?: FileList | null }; currentTarget: { value: string } }) {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      const text = typeof reader.result === "string" ? reader.result : "";
      if (text.trim().length > 0) setBatchCsv(text);
    };
    reader.readAsText(file, "utf-8");
    event.currentTarget.value = "";
  }

  function applyBeginnerPreset() {
    if (!scenarioField && numericFields.length > 0) {
      setScenarioField(numericFields[0].name);
    }
    setScenarioPct(10);
    setScenarioPoints(3);
    setBatchMaxRows(10);
    setBatchConcurrency(2);
    setScenarioPageSize(6);
    setBatchPageSize(6);
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>{copy.title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <ExperienceModePanel
          language={language}
          mode={experienceMode}
          onChangeMode={setExperienceMode}
          onApplyBeginnerPreset={applyBeginnerPreset}
        />

        {experienceMode === "expert" && (
          <ExpertQuickActions
            language={language}
            scenarioDisabled={scenarioRunning || !scenarioField}
            batchDisabled={batchRunning}
            onRunScenario={() => void runScenarioLab()}
            onRunBatch={() => void runBatchScreening()}
            onRefreshJobs={() => void refreshRecentJobs()}
            onCopySummary={() => void copyCurrentSummary()}
          />
        )}

        <OperationsOverviewPanel
          language={language}
          scenarioSuccess={scenarioSummary.success}
          scenarioFailed={scenarioSummary.failed}
          batchSuccess={batchSummary.success}
          batchFailed={batchSummary.failed}
          highRiskCount={batchRiskBuckets.success_high}
          recentJobCount={recentJobs.length}
          auditTotal={Number.isFinite(auditTotal) ? auditTotal : 0}
        />

        <section className="rounded-[6px] border border-border bg-muted/40 p-3">
          <p className="text-sm font-semibold text-foreground">{copy.scenario}</p>
          <p className="text-xs text-muted-foreground">{copy.scenarioHint}</p>
          <div className="mt-2 grid gap-2 md:grid-cols-[1fr_120px_120px_auto]">
            <Select value={scenarioField} onChange={(event) => setScenarioField(event.target.value)}>
              <option value="">{copy.scenarioField}</option>
              {numericFields.map((field) => (
                <option key={field.name} value={field.name}>{field.name}</option>
              ))}
            </Select>
            <Input type="number" min={1} max={50} value={scenarioPct} onChange={(event) => setScenarioPct(Number(event.target.value) || 10)} />
            <Input
              type="number"
              min={3}
              max={9}
              step={2}
              value={scenarioPoints}
              onChange={(event) => setScenarioPoints(Math.max(3, Math.min(9, Number(event.target.value) || 3)))}
              placeholder={copy.scenarioPoints}
            />
            <Button disabled={scenarioRunning || !scenarioField} onClick={runScenarioLab}>
              {scenarioRunning ? copy.running : copy.runScenario}
            </Button>
            <Button variant="outline" disabled={!scenarioRunning} onClick={cancelScenarioRun}>{copy.cancel}</Button>
          </div>
          <div className="mt-2 flex flex-wrap justify-end gap-2">
            <Input className="w-[170px]" placeholder={`${copy.search}...`} value={scenarioSearch} onChange={(event) => setScenarioSearch(event.target.value)} />
            <Input
              className="w-[120px]"
              type="number"
              min={4}
              max={20}
              value={scenarioPageSize}
              onChange={(event) => setScenarioPageSize(Math.max(4, Math.min(20, Number(event.target.value) || 8)))}
              placeholder={language === "ko" ? "행/페이지" : "Rows/page"}
            />
            <Select value={scenarioFilter} onChange={(event) => setScenarioFilter(event.target.value as "all" | "success" | "error" | "high-risk")} className="w-[130px]">
              <option value="all">{copy.filter}: {copy.all}</option>
              <option value="success">{copy.filter}: {copy.success}</option>
              <option value="error">{copy.filter}: {copy.error}</option>
              <option value="high-risk">{copy.filter}: {copy.highRisk}</option>
            </Select>
            <Select value={scenarioSortKey} onChange={(event) => setScenarioSortKey(event.target.value as "label" | "status" | "risk")} className="w-[120px]">
              <option value="risk">{copy.sort}: {copy.risk}</option>
              <option value="status">{copy.sort}: {copy.status}</option>
              <option value="label">{copy.sort}: ID</option>
            </Select>
            <Button variant="outline" onClick={() => setScenarioSortDir((prev) => (prev === "asc" ? "desc" : "asc"))}>
              {scenarioSortDir.toUpperCase()}
            </Button>
            <Button variant="outline" onClick={exportFilteredScenarioCsv}>{copy.exportCsv}</Button>
            <Button variant="outline" onClick={selectAllScenarioOnPage}>{copy.selectPage}</Button>
            <Button variant="outline" onClick={() => setSelectedScenarioLabels([])}>{copy.clearSelection}</Button>
            <Button variant="outline" disabled={selectedScenarioLabels.length === 0} onClick={() => void rerunSelectedScenarioRows()}>{copy.rerunSelected}</Button>
            <Button variant="outline" onClick={() => void rerunFailedScenarioRows()}>{copy.rerunFailed}</Button>
            <Button variant="outline" onClick={clearScenarioResults}>{copy.clearResults}</Button>
          </div>
          <p className="mt-1 text-[11px] text-muted-foreground">Ctrl/Cmd + Shift + Enter</p>
          <p className="mt-2 text-xs text-muted-foreground">
            {copy.summary}: success={scenarioSummary.success}, failed={scenarioSummary.failed}
          </p>
          <p className="mt-2 text-xs text-muted-foreground">{copy.progress}: {scenarioProgress.done}/{scenarioProgress.total}</p>
          <div className="mt-2 h-2 rounded bg-border/60">
            <div className="h-2 rounded bg-primary" style={{ width: `${scenarioProgress.total > 0 ? Math.round((scenarioProgress.done / scenarioProgress.total) * 100) : 0}%` }} />
          </div>
          {sortedFilteredScenarioRows.length === 0 && <p className="mt-2 text-xs text-muted-foreground">{copy.noRows}</p>}
          {sortedFilteredScenarioRows.length > 0 && (
            <TableContainer className="mt-2">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{copy.select}</TableHead>
                    <TableHead>ID</TableHead>
                    <TableHead>{copy.status}</TableHead>
                    <TableHead numeric>{copy.confidence}</TableHead>
                    <TableHead numeric>{copy.risk}</TableHead>
                    <TableHead numeric>{copy.red}</TableHead>
                    <TableHead numeric>{copy.warn}</TableHead>
                    <TableHead>Error</TableHead>
                    <TableHead>{copy.actions}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {scenarioPagination.paged.map((row) => (
                    <TableRow key={row.label}>
                      <TableCell>
                        <input type="checkbox" checked={selectedScenarioLabels.includes(row.label)} onChange={() => toggleScenarioSelection(row.label)} />
                      </TableCell>
                      <TableCell>{row.label}</TableCell>
                      <TableCell>{row.result?.status ?? "error"}</TableCell>
                      <TableCell numeric>{row.result?.verification.confidence ?? "-"}</TableCell>
                      <TableCell numeric>{row.result ? resultRiskScore(row.result) : 0}</TableCell>
                      <TableCell numeric>{row.result?.flags.red_flags.length ?? 0}</TableCell>
                      <TableCell numeric>{row.result?.flags.warnings.length ?? 0}</TableCell>
                      <TableCell className="text-xs text-muted-foreground">{row.error ?? "-"}</TableCell>
                      <TableCell>
                        <div className="flex gap-1">
                          <Button
                            variant="outline"
                            className="h-7 px-2 text-[11px]"
                            disabled={rerunKeys.includes(`scenario:${row.label}`) || !row.payload}
                            onClick={() => void rerunScenarioRow(row.label)}
                          >
                            {rerunKeys.includes(`scenario:${row.label}`) ? copy.running : copy.rerun}
                          </Button>
                          <Button
                            variant="outline"
                            className="h-7 px-2 text-[11px]"
                            onClick={() => setSelectedScenarioLabel((prev) => (prev === row.label ? null : row.label))}
                          >
                            {copy.detail}
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
          {sortedFilteredScenarioRows.length > 0 && (
            <PaginationControls
              page={scenarioPagination.page}
              totalPages={scenarioPagination.totalPages}
              prevLabel={copy.prev}
              nextLabel={copy.next}
              pageLabel={copy.page}
              onPrev={scenarioPagination.goPrev}
              onNext={scenarioPagination.goNext}
            />
          )}
          {selectedScenario && (
            <div className="mt-2 rounded-[6px] border border-border bg-background/60 p-2">
              <div className="mb-1 flex items-center justify-between">
                <p className="text-xs font-semibold text-foreground">{selectedScenario.label}</p>
                <Button className="h-7 px-2 text-[11px]" variant="outline" onClick={() => setSelectedScenarioLabel(null)}>{copy.close}</Button>
              </div>
              <pre className="max-h-40 overflow-auto text-[11px] text-muted-foreground">{JSON.stringify(selectedScenario.result?.results ?? selectedScenario.error ?? {}, null, 2)}</pre>
            </div>
          )}
        </section>

        <section className="rounded-[6px] border border-border bg-muted/40 p-3">
          <p className="text-sm font-semibold text-foreground">{copy.batch}</p>
          <p className="text-xs text-muted-foreground">{copy.batchHint}</p>
          <div className="mt-2 grid gap-2 md:grid-cols-3">
            <Input type="number" min={1} max={200} value={batchMaxRows} onChange={(event) => setBatchMaxRows(Number(event.target.value) || 20)} placeholder={copy.maxRows} />
            <Input type="number" min={1} max={10} value={batchConcurrency} onChange={(event) => setBatchConcurrency(Number(event.target.value) || 4)} placeholder={copy.concurrency} />
            <Button variant="outline" onClick={downloadTemplate}>{copy.template}</Button>
          </div>
          <div className="mt-2 grid gap-2 md:grid-cols-[220px_1fr_1fr]">
            <p className="text-xs text-muted-foreground">{copy.riskThresholds}</p>
            <Input type="number" min={1} max={20} value={riskMediumThreshold} onChange={(event) => setRiskMediumThreshold(Math.max(1, Number(event.target.value) || 1))} />
            <Input type="number" min={1} max={20} value={riskHighThreshold} onChange={(event) => setRiskHighThreshold(Math.max(1, Number(event.target.value) || 1))} />
          </div>
          <div className="mt-2 flex items-center gap-2">
            <Input className="w-[170px]" placeholder={`${copy.search}...`} value={batchSearch} onChange={(event) => setBatchSearch(event.target.value)} />
            <Input
              className="w-[120px]"
              type="number"
              min={4}
              max={20}
              value={batchPageSize}
              onChange={(event) => setBatchPageSize(Math.max(4, Math.min(20, Number(event.target.value) || 8)))}
              placeholder={language === "ko" ? "행/페이지" : "Rows/page"}
            />
            <label className="inline-flex h-9 cursor-pointer items-center rounded-[6px] border border-border px-2 text-xs">
              {copy.importCsv}
              <input type="file" accept=".csv,text/csv" className="hidden" onChange={importBatchCsvFile} />
            </label>
          </div>
          <textarea
            value={batchCsv}
            onChange={(event) => setBatchCsv(event.target.value)}
            className="mt-2 h-28 w-full rounded-[6px] border border-border bg-background px-2 py-1 text-xs"
          />
          <div className="mt-2 flex flex-wrap justify-end gap-2">
            <Select value={batchFilter} onChange={(event) => setBatchFilter(event.target.value as "all" | "success" | "error" | "high-risk")} className="w-[130px]">
              <option value="all">{copy.filter}: {copy.all}</option>
              <option value="success">{copy.filter}: {copy.success}</option>
              <option value="error">{copy.filter}: {copy.error}</option>
              <option value="high-risk">{copy.filter}: {copy.highRisk}</option>
            </Select>
            <Select value={batchSortKey} onChange={(event) => setBatchSortKey(event.target.value as "rowId" | "status" | "risk")} className="w-[120px]">
              <option value="risk">{copy.sort}: {copy.risk}</option>
              <option value="status">{copy.sort}: {copy.status}</option>
              <option value="rowId">{copy.sort}: ID</option>
            </Select>
            <Button variant="outline" onClick={() => setBatchSortDir((prev) => (prev === "asc" ? "desc" : "asc"))}>
              {batchSortDir.toUpperCase()}
            </Button>
            <Button variant="outline" onClick={exportFilteredBatchCsv}>{copy.exportCsv}</Button>
            <Button variant="outline" onClick={selectAllBatchOnPage}>{copy.selectPage}</Button>
            <Button variant="outline" onClick={() => setSelectedBatchRowIds([])}>{copy.clearSelection}</Button>
            <Button variant="outline" disabled={selectedBatchRowIds.length === 0} onClick={() => void rerunSelectedBatchRows()}>{copy.rerunSelected}</Button>
            <Button variant="outline" onClick={() => void rerunFailedBatchRows()}>{copy.rerunFailed}</Button>
            <Button variant="outline" onClick={clearBatchResults}>{copy.clearResults}</Button>
            <Button disabled={batchRunning} onClick={runBatchScreening}>
              {batchRunning ? copy.running : copy.runBatch}
            </Button>
            <Button variant="outline" disabled={!batchRunning} onClick={cancelBatchRun}>{copy.cancel}</Button>
          </div>
          <p className="mt-1 text-[11px] text-muted-foreground">Ctrl/Cmd + Enter</p>
          <p className="mt-2 text-xs text-muted-foreground">{copy.progress}: {batchProgress.done}/{batchProgress.total}</p>
          <div className="mt-2 h-2 rounded bg-border/60">
            <div className="h-2 rounded bg-primary" style={{ width: `${batchProgress.total > 0 ? Math.round((batchProgress.done / batchProgress.total) * 100) : 0}%` }} />
          </div>
          <p className="mt-2 text-xs text-muted-foreground">
            {copy.summary}: success={batchSummary.success}, failed={batchSummary.failed}, red={batchSummary.red}, warn={batchSummary.warn}
          </p>
          {batchErrorGroups.length > 0 && (
            <p className="mt-2 text-xs text-muted-foreground">
              {copy.errorGroup}: {batchErrorGroups.map(([message, count]) => `${count}x ${message}`).join(" | ")}
            </p>
          )}
          <div className="mt-2 grid grid-cols-2 gap-2 rounded-[6px] border border-border bg-background/40 p-2 text-xs">
            <p className="col-span-2 font-semibold text-foreground">{copy.riskHeatmap}</p>
            <p>{copy.low}: {batchRiskBuckets.success_low}</p>
            <p>{copy.medium}: {batchRiskBuckets.success_medium}</p>
            <p>{copy.high}: {batchRiskBuckets.success_high}</p>
            <p>Error: {batchRiskBuckets.error}</p>
          </div>
          {sortedFilteredBatchRows.length === 0 && <p className="mt-2 text-xs text-muted-foreground">{copy.noRows}</p>}
          {sortedFilteredBatchRows.length > 0 && (
            <TableContainer className="mt-2">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{copy.select}</TableHead>
                    <TableHead>ID</TableHead>
                    <TableHead>{copy.status}</TableHead>
                    <TableHead numeric>{copy.confidence}</TableHead>
                    <TableHead numeric>{copy.risk}</TableHead>
                    <TableHead numeric>{copy.red}</TableHead>
                    <TableHead numeric>{copy.warn}</TableHead>
                    <TableHead>Error</TableHead>
                    <TableHead>{copy.actions}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {batchPagination.paged.map((row) => (
                    <TableRow key={row.rowId}>
                      <TableCell>
                        <input type="checkbox" checked={selectedBatchRowIds.includes(row.rowId)} onChange={() => toggleBatchSelection(row.rowId)} />
                      </TableCell>
                      <TableCell>{row.rowId}</TableCell>
                      <TableCell>{row.result?.status ?? "error"}</TableCell>
                      <TableCell numeric>{row.result?.verification.confidence ?? "-"}</TableCell>
                      <TableCell numeric>{row.result ? resultRiskScore(row.result) : 0}</TableCell>
                      <TableCell numeric>{row.result?.flags.red_flags.length ?? 0}</TableCell>
                      <TableCell numeric>{row.result?.flags.warnings.length ?? 0}</TableCell>
                      <TableCell className="text-xs text-muted-foreground">{row.error ?? "-"}</TableCell>
                      <TableCell>
                        <div className="flex gap-1">
                          <Button
                            variant="outline"
                            className="h-7 px-2 text-[11px]"
                            disabled={rerunKeys.includes(`batch:${row.rowId}`) || !row.payload}
                            onClick={() => void rerunBatchRow(row.rowId)}
                          >
                            {rerunKeys.includes(`batch:${row.rowId}`) ? copy.running : copy.rerun}
                          </Button>
                          <Button
                            variant="outline"
                            className="h-7 px-2 text-[11px]"
                            onClick={() => setSelectedBatchRowId((prev) => (prev === row.rowId ? null : row.rowId))}
                          >
                            {copy.detail}
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
          {sortedFilteredBatchRows.length > 0 && (
            <PaginationControls
              page={batchPagination.page}
              totalPages={batchPagination.totalPages}
              prevLabel={copy.prev}
              nextLabel={copy.next}
              pageLabel={copy.page}
              onPrev={batchPagination.goPrev}
              onNext={batchPagination.goNext}
            />
          )}
          {selectedBatch && (
            <div className="mt-2 rounded-[6px] border border-border bg-background/60 p-2">
              <div className="mb-1 flex items-center justify-between">
                <p className="text-xs font-semibold text-foreground">{selectedBatch.rowId}</p>
                <Button className="h-7 px-2 text-[11px]" variant="outline" onClick={() => setSelectedBatchRowId(null)}>{copy.close}</Button>
              </div>
              <pre className="max-h-40 overflow-auto text-[11px] text-muted-foreground">{JSON.stringify(selectedBatch.result?.results ?? selectedBatch.error ?? {}, null, 2)}</pre>
            </div>
          )}
        </section>

        <BackendOpsPanel
          enabled={backendEnabled}
          copy={copy}
          jobRunning={jobRunning}
          jobId={jobId}
          jobStatus={jobStatus}
          sensitivityRunning={sensitivityRunning}
          scenarioField={scenarioField}
          reportBusy={reportBusy}
          wsStreaming={wsStreaming}
          persistenceStats={persistenceStats}
          jobResultPreview={jobResultPreview}
          sensitivityRows={sensitivityRows}
          collabAuthor={collabAuthor}
          collabMessage={collabMessage}
          collabLogs={collabLogs}
          wsMessages={wsMessages}
          recentJobs={recentJobs}
          recentAudits={recentAudits}
          auditSummary={auditSummary}
          autoRefreshEnabled={autoRefreshEnabled}
          onRunQueuedJob={() => void runQueuedJob()}
          onRefreshJobStatus={() => void refreshJobStatus()}
          onRunSensitivity={() => void runSensitivity()}
          onRefreshPersistence={() => void refreshPersistenceStats()}
          onDownloadPackage={() => void downloadBackendPackage()}
          onStartStream={startJobStream}
          onStopStream={stopJobStream}
          onRefreshJobs={() => void refreshRecentJobs()}
          onRefreshAudit={() => void refreshRecentAudits()}
          onRetryLatest={() => void retryLatestJob()}
          onCancelAll={() => void cancelAllJobs()}
          onToggleAutoRefresh={() => setAutoRefreshEnabled((prev) => !prev)}
          onChangeAuthor={setCollabAuthor}
          onChangeMessage={setCollabMessage}
          onAddNote={() => void addCollabNote()}
        />

        <section className="rounded-[6px] border border-border bg-muted/40 p-3">
          <p className="text-sm font-semibold text-foreground">{copy.exportPack}</p>
          <p className="text-xs text-muted-foreground">{copy.exportHint}</p>
          <div className="mt-2 flex justify-end gap-2">
            <Button variant="outline" onClick={() => void copyCurrentSummary()}>{copiedSummary ? copy.copied : copy.copyMd}</Button>
            <Button variant="outline" onClick={exportEvidencePack}>{copy.exportPack}</Button>
          </div>
        </section>
      </CardContent>
    </Card>
  );
}
