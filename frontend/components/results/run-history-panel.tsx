"use client";

import { useMemo, useState } from "react";
import { ArrowDown, ArrowUp, Trash2 } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { Discipline, RunHistoryEntry } from "@/lib/types";
import { calculationStatusLabel, confidenceLabel } from "@/lib/ui-labels";
import { useWorkbenchStore } from "@/store/workbench-store";

type SortKey = "time" | "status" | "confidence" | "elapsedMs" | "redFlags" | "warnings";
type SortDirection = "asc" | "desc";

const STATUS_WEIGHT: Record<RunHistoryEntry["status"], number> = {
  blocked: 3,
  error: 2,
  success: 1,
};

const CONFIDENCE_WEIGHT: Record<RunHistoryEntry["confidence"], number> = {
  high: 3,
  medium: 2,
  low: 1,
};

function statusVariant(status: RunHistoryEntry["status"]): "ok" | "error" | "blocked" {
  if (status === "success") return "ok";
  if (status === "blocked") return "blocked";
  return "error";
}

function sortRows(rows: RunHistoryEntry[], key: SortKey, direction: SortDirection): RunHistoryEntry[] {
  const sorted = [...rows].sort((a, b) => {
    if (key === "time") {
      return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
    }
    if (key === "status") {
      return STATUS_WEIGHT[a.status] - STATUS_WEIGHT[b.status];
    }
    if (key === "confidence") {
      return CONFIDENCE_WEIGHT[a.confidence] - CONFIDENCE_WEIGHT[b.confidence];
    }
    if (key === "elapsedMs") {
      return a.elapsedMs - b.elapsedMs;
    }
    if (key === "redFlags") {
      return a.redFlagCount - b.redFlagCount;
    }
    return a.warningCount - b.warningCount;
  });

  return direction === "asc" ? sorted : sorted.reverse();
}

function SortMarker({ active, direction }: { active: boolean; direction: SortDirection }) {
  if (!active) return null;
  return direction === "asc" ? <ArrowUp className="h-3 w-3" /> : <ArrowDown className="h-3 w-3" />;
}

export function RunHistoryPanel({ discipline }: { discipline: Discipline }) {
  const { language } = useUiLanguage();
  const [sortKey, setSortKey] = useState<SortKey>("time");
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");
  const copy = language === "ko"
    ? {
        title: "최근 실행 이력",
        clear: "초기화",
        empty: "이 공종의 실행 이력이 없습니다.",
        time: "시간",
        status: "상태",
        projectAsset: "프로젝트 / 자산",
        headline: "요약",
        conf: "신뢰도",
        red: "레드",
        warn: "경고",
      }
    : {
        title: "Recent Runs",
        clear: "Clear",
        empty: "No run history yet for this discipline.",
        time: "Time",
        status: "Status",
        projectAsset: "Project / Asset",
        headline: "Headline",
        conf: "Conf.",
        red: "Red",
        warn: "Warn",
      };

  const history = useWorkbenchStore((state) =>
    state.runHistory.filter((entry) => entry.discipline === discipline).slice(0, 24),
  );
  const clearRunHistoryByDiscipline = useWorkbenchStore((state) => state.clearRunHistoryByDiscipline);

  const sortedHistory = useMemo(
    () => sortRows(history, sortKey, sortDirection),
    [history, sortDirection, sortKey],
  );

  function onSort(key: SortKey) {
    if (sortKey === key) {
      setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"));
      return;
    }
    setSortKey(key);
    setSortDirection(key === "time" ? "desc" : "asc");
  }

  function sortButtonClass(active: boolean) {
    return active
      ? "inline-flex items-center gap-1 text-primary"
      : "inline-flex items-center gap-1 text-muted-foreground";
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>{copy.title}</CardTitle>
        <Button variant="outline" onClick={() => clearRunHistoryByDiscipline(discipline)}>
          <Trash2 className="mr-2 h-4 w-4" />
          {copy.clear}
        </Button>
      </CardHeader>
      <CardContent>
        {history.length === 0 && <p className="text-sm text-muted-foreground">{copy.empty}</p>}
        {history.length > 0 && (
          <TableContainer>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>
                    <button type="button" className={sortButtonClass(sortKey === "time")} onClick={() => onSort("time")}>
                      {copy.time}
                      <SortMarker active={sortKey === "time"} direction={sortDirection} />
                    </button>
                  </TableHead>
                  <TableHead>
                    <button type="button" className={sortButtonClass(sortKey === "status")} onClick={() => onSort("status")}>
                      {copy.status}
                      <SortMarker active={sortKey === "status"} direction={sortDirection} />
                    </button>
                  </TableHead>
                  <TableHead>{copy.projectAsset}</TableHead>
                  <TableHead>{copy.headline}</TableHead>
                  <TableHead numeric>
                    <button type="button" className={sortButtonClass(sortKey === "confidence")} onClick={() => onSort("confidence")}>
                      {copy.conf}
                      <SortMarker active={sortKey === "confidence"} direction={sortDirection} />
                    </button>
                  </TableHead>
                  <TableHead numeric>
                    <button type="button" className={sortButtonClass(sortKey === "elapsedMs")} onClick={() => onSort("elapsedMs")}>
                      ms
                      <SortMarker active={sortKey === "elapsedMs"} direction={sortDirection} />
                    </button>
                  </TableHead>
                  <TableHead numeric>
                    <button type="button" className={sortButtonClass(sortKey === "redFlags")} onClick={() => onSort("redFlags")}>
                      {copy.red}
                      <SortMarker active={sortKey === "redFlags"} direction={sortDirection} />
                    </button>
                  </TableHead>
                  <TableHead numeric>
                    <button type="button" className={sortButtonClass(sortKey === "warnings")} onClick={() => onSort("warnings")}>
                      {copy.warn}
                      <SortMarker active={sortKey === "warnings"} direction={sortDirection} />
                    </button>
                  </TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {sortedHistory.map((entry) => (
                  <TableRow key={entry.id}>
                    <TableCell className="font-data text-xs text-muted-foreground">
                      {new Date(entry.timestamp).toLocaleString(language === "ko" ? "ko-KR" : "en-US")}
                    </TableCell>
                    <TableCell>
                      <Badge variant={statusVariant(entry.status)}>{calculationStatusLabel(entry.status, language)}</Badge>
                    </TableCell>
                    <TableCell className="text-xs text-muted-foreground">
                      {entry.projectId} / {entry.assetId}
                    </TableCell>
                    <TableCell>{entry.headline}</TableCell>
                    <TableCell numeric>
                      {confidenceLabel(entry.confidence, language)}
                    </TableCell>
                    <TableCell numeric>{entry.elapsedMs}</TableCell>
                    <TableCell numeric>{entry.redFlagCount}</TableCell>
                    <TableCell numeric>{entry.warningCount}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </CardContent>
    </Card>
  );
}
