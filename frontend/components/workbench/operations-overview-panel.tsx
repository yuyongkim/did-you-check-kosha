"use client";

export function OperationsOverviewPanel({
  language,
  scenarioSuccess,
  scenarioFailed,
  batchSuccess,
  batchFailed,
  highRiskCount,
  recentJobCount,
  auditTotal,
}: {
  language: "ko" | "en";
  scenarioSuccess: number;
  scenarioFailed: number;
  batchSuccess: number;
  batchFailed: number;
  highRiskCount: number;
  recentJobCount: number;
  auditTotal: number;
}) {
  const copy = language === "ko"
    ? {
        title: "운영 개요 시각화",
        scenario: "시나리오",
        batch: "배치",
        highRisk: "고위험",
        jobs: "최근 잡",
        audit: "감사 합계",
        success: "성공",
        failed: "실패",
      }
    : {
        title: "Operations overview",
        scenario: "Scenario",
        batch: "Batch",
        highRisk: "High risk",
        jobs: "Recent jobs",
        audit: "Audit total",
        success: "Success",
        failed: "Failed",
      };

  const scenarioTotal = Math.max(1, scenarioSuccess + scenarioFailed);
  const batchTotal = Math.max(1, batchSuccess + batchFailed);

  return (
    <section className="rounded-[6px] border border-border bg-muted/40 p-3">
      <p className="text-sm font-semibold text-foreground">{copy.title}</p>
      <div className="mt-2 grid gap-2 md:grid-cols-5">
        <MetricCard label={copy.scenario} value={`${scenarioSuccess + scenarioFailed}`} />
        <MetricCard label={copy.batch} value={`${batchSuccess + batchFailed}`} />
        <MetricCard label={copy.highRisk} value={`${highRiskCount}`} />
        <MetricCard label={copy.jobs} value={`${recentJobCount}`} />
        <MetricCard label={copy.audit} value={`${auditTotal}`} />
      </div>

      <div className="mt-3 grid gap-3 md:grid-cols-2">
        <div className="rounded-[6px] border border-border bg-background/50 p-2">
          <p className="text-xs font-semibold text-foreground">{copy.scenario}</p>
          <p className="mt-1 text-[11px] text-muted-foreground">{copy.success}: {scenarioSuccess} | {copy.failed}: {scenarioFailed}</p>
          <div className="mt-2 h-2 rounded bg-border/60">
            <div className="h-2 rounded bg-primary" style={{ width: `${Math.round((scenarioSuccess / scenarioTotal) * 100)}%` }} />
          </div>
        </div>

        <div className="rounded-[6px] border border-border bg-background/50 p-2">
          <p className="text-xs font-semibold text-foreground">{copy.batch}</p>
          <p className="mt-1 text-[11px] text-muted-foreground">{copy.success}: {batchSuccess} | {copy.failed}: {batchFailed}</p>
          <div className="mt-2 h-2 rounded bg-border/60">
            <div className="h-2 rounded bg-primary" style={{ width: `${Math.round((batchSuccess / batchTotal) * 100)}%` }} />
          </div>
        </div>
      </div>
    </section>
  );
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-[6px] border border-border bg-background/50 p-2">
      <p className="text-[11px] text-muted-foreground">{label}</p>
      <p className="text-sm font-semibold text-foreground">{value}</p>
    </div>
  );
}
