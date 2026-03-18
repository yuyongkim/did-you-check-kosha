"use client";

import { Button } from "@/components/ui/button";

export type ExperienceMode = "beginner" | "expert";

export function ExperienceModePanel({
  language,
  mode,
  onChangeMode,
  onApplyBeginnerPreset,
}: {
  language: "ko" | "en";
  mode: ExperienceMode;
  onChangeMode: (mode: ExperienceMode) => void;
  onApplyBeginnerPreset: () => void;
}) {
  const copy = language === "ko"
    ? {
        title: "사용자 모드",
        beginner: "초심자",
        expert: "전문가",
        beginnerHint: "권장값/가이드 중심으로 빠르게 첫 결과를 만들 수 있습니다.",
        expertHint: "단축키/병렬 실행 중심으로 고속 워크플로우를 사용합니다.",
        applyPreset: "초심자 권장값 적용",
        checklist: "초심자 체크리스트",
      }
    : {
        title: "Experience mode",
        beginner: "Beginner",
        expert: "Expert",
        beginnerHint: "Guided defaults and safer first-run workflow.",
        expertHint: "Shortcut-first, high-throughput workflow.",
        applyPreset: "Apply beginner defaults",
        checklist: "Beginner checklist",
      };

  return (
    <section className="rounded-[6px] border border-border bg-muted/40 p-3">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <p className="text-sm font-semibold text-foreground">{copy.title}</p>
        <div className="flex gap-2">
          <Button variant={mode === "beginner" ? "default" : "outline"} className="h-8 px-3 text-xs" onClick={() => onChangeMode("beginner")}>{copy.beginner}</Button>
          <Button variant={mode === "expert" ? "default" : "outline"} className="h-8 px-3 text-xs" onClick={() => onChangeMode("expert")}>{copy.expert}</Button>
        </div>
      </div>

      <p className="mt-2 text-xs text-muted-foreground">{mode === "beginner" ? copy.beginnerHint : copy.expertHint}</p>

      {mode === "beginner" && (
        <>
          <Button variant="outline" className="mt-2 h-8 text-xs" onClick={onApplyBeginnerPreset}>{copy.applyPreset}</Button>
          <div className="mt-2 rounded-[6px] border border-border bg-background/40 p-2 text-xs text-muted-foreground">
            <p className="font-semibold text-foreground">{copy.checklist}</p>
            <p className="mt-1">1) Scenario 변수 선택</p>
            <p>2) Run Scenario 실행</p>
            <p>3) Batch CSV 업로드 후 Run Batch</p>
            <p>4) Export Evidence Pack 저장</p>
          </div>
        </>
      )}
    </section>
  );
}
