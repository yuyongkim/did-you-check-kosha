"use client";

import { CheckCircle2, Circle, PlayCircle, ShieldCheck, Wrench } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { CalculationResponse, FormFieldConfig } from "@/lib/types";

function isFilled(value: unknown, field: FormFieldConfig): boolean {
  if (value === null || value === undefined) return false;
  if (field.type === "checkbox") return true;
  if (field.type === "number") return Number.isFinite(Number(value));
  return String(value).trim().length > 0;
}

function isVisible(field: FormFieldConfig, values: Record<string, unknown>): boolean {
  if (!field.showWhen) return true;
  const current = values[field.showWhen.field];
  if (Array.isArray(field.showWhen.equalsAny) && field.showWhen.equalsAny.length > 0) {
    return field.showWhen.equalsAny.some((expected) => String(expected) === String(current));
  }
  if (Object.prototype.hasOwnProperty.call(field.showWhen, "equals")) {
    return String(field.showWhen.equals) === String(current);
  }
  return true;
}

export function GuidedRunCard({
  fields,
  values,
  result,
}: {
  fields: FormFieldConfig[];
  values: Record<string, unknown>;
  result: CalculationResponse | null;
}) {
  const { language } = useUiLanguage();
  const copy = language === "ko"
    ? {
        title: "Guided Run (입문 모드)",
        subtitle: "아래 4단계를 순서대로 따라가면 결과 해석까지 가능합니다.",
        inputStep: "1) 입력 준비",
        inputHint: "필수 입력을 채우고 프리셋을 확인하세요.",
        runStep: "2) 계산 실행",
        runHint: "Run Calculation 버튼으로 첫 실행을 완료하세요.",
        verifyStep: "3) 검증 확인",
        verifyHint: "4계층 검증 패널에서 PASS/FAIL을 확인하세요.",
        actionStep: "4) 조치 결정",
        actionHint: "권고사항 카드에서 즉시/단기/정기 액션을 결정하세요.",
        done: "완료",
        pending: "대기",
        inputProgress: "입력 진행",
      }
    : {
        title: "Guided Run (Beginner)",
        subtitle: "Follow this 4-step flow to move from input to action.",
        inputStep: "1) Prepare inputs",
        inputHint: "Complete required fields and check presets.",
        runStep: "2) Run calculation",
        runHint: "Use Run Calculation for the first execution.",
        verifyStep: "3) Check verification",
        verifyHint: "Review PASS/FAIL across 4-layer verification.",
        actionStep: "4) Decide action",
        actionHint: "Pick immediate/short-term/planned actions from recommendations.",
        done: "Done",
        pending: "Pending",
        inputProgress: "Input progress",
      };

  const visibleFields = fields.filter((field) => isVisible(field, values));
  const filledCount = visibleFields.filter((field) => isFilled(values[field.name], field)).length;
  const completion = visibleFields.length === 0 ? 0 : Math.round((filledCount / visibleFields.length) * 100);

  const steps = [
    {
      key: "input",
      label: copy.inputStep,
      hint: copy.inputHint,
      done: completion >= 80,
      icon: PlayCircle,
    },
    {
      key: "run",
      label: copy.runStep,
      hint: copy.runHint,
      done: Boolean(result),
      icon: PlayCircle,
    },
    {
      key: "verify",
      label: copy.verifyStep,
      hint: copy.verifyHint,
      done: Boolean(result && result.verification.layers.every((layer) => layer.passed)),
      icon: ShieldCheck,
    },
    {
      key: "action",
      label: copy.actionStep,
      hint: copy.actionHint,
      done: Boolean(result && result.details.recommendations.length > 0),
      icon: Wrench,
    },
  ] as const;

  return (
    <Card>
      <CardHeader>
        <CardTitle>{copy.title}</CardTitle>
        <p className="text-xs text-muted-foreground">{copy.subtitle}</p>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="rounded-[6px] border border-border bg-muted px-2 py-1 text-xs text-muted-foreground">
          {copy.inputProgress}: {filledCount}/{visibleFields.length} ({completion}%)
        </div>
        {steps.map((step) => {
          const Icon = step.icon;
          return (
            <article key={step.key} className="rounded-[6px] border border-border bg-card px-2 py-2">
              <div className="flex items-center justify-between gap-2">
                <p className="flex items-center gap-1 text-sm font-medium text-foreground">
                  <Icon className="h-3.5 w-3.5 text-primary" />
                  {step.label}
                </p>
                <span className="inline-flex items-center gap-1 text-xs text-muted-foreground">
                  {step.done ? <CheckCircle2 className="h-3.5 w-3.5 text-success" /> : <Circle className="h-3.5 w-3.5" />}
                  {step.done ? copy.done : copy.pending}
                </span>
              </div>
              <p className="mt-1 text-xs text-muted-foreground">{step.hint}</p>
            </article>
          );
        })}
      </CardContent>
    </Card>
  );
}
