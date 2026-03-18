"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export interface BackendOpsCopy {
  backendOps: string;
  running: string;
  queueRun: string;
  queuePoll: string;
  sensitivityRun: string;
  persistence: string;
  packageZip: string;
  streamStart: string;
  streamStop: string;
  jobsRefresh: string;
  auditRefresh: string;
  retryLast: string;
  cancelAll: string;
  addNote: string;
  collabLog: string;
  autoRefresh: string;
  autoOn: string;
  autoOff: string;
}

export function BackendOpsPanel({
  enabled,
  copy,
  jobRunning,
  jobId,
  jobStatus,
  sensitivityRunning,
  scenarioField,
  reportBusy,
  wsStreaming,
  persistenceStats,
  jobResultPreview,
  sensitivityRows,
  collabAuthor,
  collabMessage,
  collabLogs,
  wsMessages,
  recentJobs,
  recentAudits,
  auditSummary,
  autoRefreshEnabled,
  onRunQueuedJob,
  onRefreshJobStatus,
  onRunSensitivity,
  onRefreshPersistence,
  onDownloadPackage,
  onStartStream,
  onStopStream,
  onRefreshJobs,
  onRefreshAudit,
  onRetryLatest,
  onCancelAll,
  onToggleAutoRefresh,
  onChangeAuthor,
  onChangeMessage,
  onAddNote,
}: {
  enabled: boolean;
  copy: BackendOpsCopy;
  jobRunning: boolean;
  jobId: string;
  jobStatus: string;
  sensitivityRunning: boolean;
  scenarioField: string;
  reportBusy: boolean;
  wsStreaming: boolean;
  persistenceStats: Record<string, unknown> | null;
  jobResultPreview: Record<string, unknown> | null;
  sensitivityRows: Array<Record<string, unknown>>;
  collabAuthor: string;
  collabMessage: string;
  collabLogs: string[];
  wsMessages: string[];
  recentJobs: Array<Record<string, unknown>>;
  recentAudits: Array<Record<string, unknown>>;
  auditSummary: Record<string, unknown> | null;
  autoRefreshEnabled: boolean;
  onRunQueuedJob: () => void;
  onRefreshJobStatus: () => void;
  onRunSensitivity: () => void;
  onRefreshPersistence: () => void;
  onDownloadPackage: () => void;
  onStartStream: () => void;
  onStopStream: () => void;
  onRefreshJobs: () => void;
  onRefreshAudit: () => void;
  onRetryLatest: () => void;
  onCancelAll: () => void;
  onToggleAutoRefresh: () => void;
  onChangeAuthor: (value: string) => void;
  onChangeMessage: (value: string) => void;
  onAddNote: () => void;
}) {
  return (
    <section className="rounded-[6px] border border-border bg-muted/40 p-3">
      <p className="text-sm font-semibold text-foreground">{copy.backendOps}</p>
      {!enabled && <p className="text-xs text-muted-foreground">Enable backend mode to use queue/collab/sensitivity APIs.</p>}
      {enabled && (
        <>
          <div className="mt-2 flex flex-wrap gap-2">
            <Button variant="outline" disabled={jobRunning} onClick={onRunQueuedJob}>{jobRunning ? copy.running : copy.queueRun}</Button>
            <Button variant="outline" disabled={!jobId} onClick={onRefreshJobStatus}>{copy.queuePoll}</Button>
            <Button variant="outline" disabled={sensitivityRunning || !scenarioField} onClick={onRunSensitivity}>{sensitivityRunning ? copy.running : copy.sensitivityRun}</Button>
            <Button variant="outline" onClick={onRefreshPersistence}>{copy.persistence}</Button>
            <Button variant="outline" disabled={reportBusy} onClick={onDownloadPackage}>{reportBusy ? copy.running : copy.packageZip}</Button>
            <Button variant="outline" disabled={!jobId || wsStreaming} onClick={onStartStream}>{copy.streamStart}</Button>
            <Button variant="outline" disabled={!wsStreaming} onClick={onStopStream}>{copy.streamStop}</Button>
            <Button variant="outline" onClick={onRefreshJobs}>{copy.jobsRefresh}</Button>
            <Button variant="outline" onClick={onRefreshAudit}>{copy.auditRefresh}</Button>
            <Button variant="outline" onClick={onRetryLatest}>{copy.retryLast}</Button>
            <Button variant="outline" onClick={onCancelAll}>{copy.cancelAll}</Button>
            <Button variant="outline" onClick={onToggleAutoRefresh}>
              {copy.autoRefresh}: {autoRefreshEnabled ? copy.autoOn : copy.autoOff}
            </Button>
          </div>
          <p className="mt-2 text-xs text-muted-foreground">job_id={jobId || "-"} | status={jobStatus || "-"}</p>
          {persistenceStats && <p className="mt-1 text-xs text-muted-foreground">{copy.persistence}: {JSON.stringify(persistenceStats)}</p>}

          {jobResultPreview && (
            <pre className="mt-2 max-h-28 overflow-auto rounded-[6px] border border-border bg-background/60 p-2 text-[11px] text-muted-foreground">
              {JSON.stringify(jobResultPreview, null, 2)}
            </pre>
          )}
          {sensitivityRows.length > 0 && (
            <pre className="mt-2 max-h-28 overflow-auto rounded-[6px] border border-border bg-background/60 p-2 text-[11px] text-muted-foreground">
              {JSON.stringify(sensitivityRows.slice(0, 6), null, 2)}
            </pre>
          )}

          <div className="mt-2 grid gap-2 md:grid-cols-[120px_1fr_auto]">
            <Input value={collabAuthor} onChange={(event) => onChangeAuthor(event.target.value)} />
            <Input value={collabMessage} onChange={(event) => onChangeMessage(event.target.value)} />
            <Button variant="outline" onClick={onAddNote}>{copy.addNote}</Button>
          </div>

          {collabLogs.length > 0 && (
            <div className="mt-2 rounded-[6px] border border-border bg-background/40 p-2">
              <p className="text-xs font-semibold text-foreground">{copy.collabLog}</p>
              {collabLogs.slice(0, 5).map((line) => (
                <p key={line} className="mt-1 text-[11px] text-muted-foreground">{line}</p>
              ))}
            </div>
          )}
          {wsMessages.length > 0 && (
            <div className="mt-2 rounded-[6px] border border-border bg-background/40 p-2">
              <p className="text-xs font-semibold text-foreground">WS</p>
              {wsMessages.slice(0, 5).map((line) => (
                <p key={line} className="mt-1 text-[11px] text-muted-foreground">{line}</p>
              ))}
            </div>
          )}
          {recentJobs.length > 0 && (
            <div className="mt-2 rounded-[6px] border border-border bg-background/40 p-2">
              <p className="text-xs font-semibold text-foreground">Jobs</p>
              {recentJobs.slice(0, 5).map((row, index) => (
                <p key={`${row.job_id ?? "job"}-${index}`} className="mt-1 text-[11px] text-muted-foreground">
                  {String(row.job_id ?? "-")} | {String(row.status ?? "-")}
                </p>
              ))}
            </div>
          )}
          {recentAudits.length > 0 && (
            <div className="mt-2 rounded-[6px] border border-border bg-background/40 p-2">
              <p className="text-xs font-semibold text-foreground">Audit</p>
              {recentAudits.slice(0, 5).map((row, index) => (
                <p key={`${row.id ?? "audit"}-${index}`} className="mt-1 text-[11px] text-muted-foreground">
                  {String(row.event_type ?? "-")} | {String(row.timestamp ?? "-")}
                </p>
              ))}
            </div>
          )}
          {auditSummary && (
            <div className="mt-2 rounded-[6px] border border-border bg-background/40 p-2">
              <p className="text-xs font-semibold text-foreground">Audit Summary</p>
              <p className="mt-1 text-[11px] text-muted-foreground">total={String(auditSummary.total ?? 0)}</p>
              {(Array.isArray(auditSummary.by_event_type) ? auditSummary.by_event_type : []).slice(0, 5).map((row, index) => (
                <p key={`summary-${index}`} className="mt-1 text-[11px] text-muted-foreground">
                  {String((row as Record<string, unknown>).event_type ?? "-")} | {String((row as Record<string, unknown>).count ?? 0)}
                </p>
              ))}
            </div>
          )}
        </>
      )}
    </section>
  );
}
