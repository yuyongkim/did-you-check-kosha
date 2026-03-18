"use client";

import { Button } from "@/components/ui/button";

export function ExpertQuickActions({
  language,
  onRunScenario,
  onRunBatch,
  onRefreshJobs,
  onCopySummary,
  scenarioDisabled,
  batchDisabled,
}: {
  language: "ko" | "en";
  onRunScenario: () => void;
  onRunBatch: () => void;
  onRefreshJobs: () => void;
  onCopySummary: () => void;
  scenarioDisabled: boolean;
  batchDisabled: boolean;
}) {
  const copy = language === "ko"
    ? {
        title: "전문가 빠른 액션",
        runScenario: "시나리오 실행",
        runBatch: "배치 실행",
        refreshJobs: "잡 갱신",
        copySummary: "요약 복사",
        shortcut: "단축키: Ctrl/Cmd+Shift+Enter(시나리오), Ctrl/Cmd+Enter(배치)",
      }
    : {
        title: "Expert quick actions",
        runScenario: "Run scenario",
        runBatch: "Run batch",
        refreshJobs: "Refresh jobs",
        copySummary: "Copy summary",
        shortcut: "Shortcut: Ctrl/Cmd+Shift+Enter (scenario), Ctrl/Cmd+Enter (batch)",
      };

  return (
    <section className="rounded-[6px] border border-border bg-muted/40 p-3">
      <p className="text-sm font-semibold text-foreground">{copy.title}</p>
      <div className="mt-2 flex flex-wrap gap-2">
        <Button className="h-8 px-3 text-xs" disabled={scenarioDisabled} onClick={onRunScenario}>{copy.runScenario}</Button>
        <Button className="h-8 px-3 text-xs" disabled={batchDisabled} onClick={onRunBatch}>{copy.runBatch}</Button>
        <Button variant="outline" className="h-8 px-3 text-xs" onClick={onRefreshJobs}>{copy.refreshJobs}</Button>
        <Button variant="outline" className="h-8 px-3 text-xs" onClick={onCopySummary}>{copy.copySummary}</Button>
      </div>
      <p className="mt-2 text-[11px] text-muted-foreground">{copy.shortcut}</p>
    </section>
  );
}
