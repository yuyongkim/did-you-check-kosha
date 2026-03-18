"use client";

import { useEffect, useMemo, useRef } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { TermHelp } from "@/components/ui/term-help";
import { Discipline, DisciplinePreset, FormFieldConfig } from "@/lib/types";
import {
  FormUiLanguage,
  getDisciplineFormCopy,
  localizeFieldHelper,
  localizeFieldLabel,
  localizeOptionGroupLabel,
  localizeOptionLabel,
  localizePresetLabel,
  localizeUnit,
} from "@/components/forms/discipline-form-localization";
import { fieldSchema, firstSelectValue } from "@/components/forms/discipline-form-schema";

interface DisciplineFormProps {
  discipline?: Discipline;
  title: string;
  fields: FormFieldConfig[];
  sampleInput: Record<string, unknown>;
  presets?: DisciplinePreset[];
  onSubmit: (payload: Record<string, unknown>) => Promise<void>;
  onValuesChange?: (values: Record<string, unknown>) => void;
  submitting: boolean;
}

export function DisciplineForm({
  discipline,
  title,
  fields,
  sampleInput,
  presets,
  onSubmit,
  onValuesChange,
  submitting,
}: DisciplineFormProps) {
  const effectiveDiscipline = discipline ?? "piping";
  const showForceBlockedToggle = process.env.NEXT_PUBLIC_ENABLE_DEMO_BLOCKED === "true";
  const { language } = useUiLanguage();
  const formLanguage: FormUiLanguage = language === "ko" ? "ko" : "en";
  const copy = getDisciplineFormCopy(formLanguage);

  const schema = useMemo(() => {
    const shape: Record<string, z.ZodTypeAny> = {};
    for (const field of fields) {
      const base = fieldSchema(field);
      shape[field.name] = field.showWhen ? base.optional() : base;
    }
    shape.force_blocked = z.boolean().optional();
    return z.object(shape);
  }, [fields]);

  type FormValues = z.infer<typeof schema>;

  const defaultValues = useMemo(() => {
    const values: Record<string, unknown> = {};
    for (const field of fields) {
      if (field.type === "number") {
        values[field.name] = sampleInput[field.name] ?? field.min ?? 0;
      } else if (field.type === "checkbox") {
        values[field.name] = Boolean(sampleInput[field.name]);
      } else if (field.type === "select") {
        const sample = String(sampleInput[field.name] ?? "").trim();
        values[field.name] = sample || firstSelectValue(field);
      } else {
        values[field.name] = sampleInput[field.name] ?? "";
      }
    }
    values.force_blocked = false;
    return values as FormValues;
  }, [fields, sampleInput]);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
    setValue,
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues,
  });

  const watchedValues = watch() as Record<string, unknown>;
  const forceBlocked = Boolean(watch("force_blocked"));
  const lastEmittedRef = useRef<string>("");

  useEffect(() => {
    if (!onValuesChange) return;
    const mergedValues = {
      ...sampleInput,
      ...watchedValues,
    };
    const serialized = JSON.stringify(mergedValues);
    if (serialized === lastEmittedRef.current) return;
    lastEmittedRef.current = serialized;
    onValuesChange(mergedValues);
  }, [onValuesChange, sampleInput, watchedValues]);

  return (
    <Card className="animate-fadeUp">
      <CardHeader>
        <CardTitle>{title} {copy.input}</CardTitle>
      </CardHeader>
      <CardContent>
        {presets && presets.length > 0 && (
          <div className="mb-3 space-y-2 rounded-[6px] border border-border bg-muted p-2">
            <p className="text-xs uppercase tracking-wide text-muted-foreground">{copy.quickPresets}</p>
            <div className="flex flex-wrap gap-2">
              {presets.map((preset) => (
                <Button
                  key={preset.id}
                  type="button"
                  variant="outline"
                  className="h-8 px-2 text-xs"
                  disabled={submitting}
                  title={preset.description}
                  onClick={() => reset({ ...defaultValues, ...preset.values } as FormValues)}
                >
                  {localizePresetLabel(effectiveDiscipline, formLanguage, preset.id, preset.label)}
                </Button>
              ))}
            </div>
          </div>
        )}

        <form
          className="flex flex-col gap-3"
          onSubmit={handleSubmit(async (values) => {
            const payload: Record<string, unknown> = {
              ...sampleInput,
              ...values,
            };
            await onSubmit(payload);
          })}
        >
          {fields.map((field) => {
            if (field.showWhen) {
              const currentValue = watchedValues[field.showWhen.field];
              if (Array.isArray(field.showWhen.equalsAny) && field.showWhen.equalsAny.length > 0) {
                const visible = field.showWhen.equalsAny.some((expected) => String(currentValue ?? "") === String(expected));
                if (!visible) return null;
              } else if (Object.prototype.hasOwnProperty.call(field.showWhen, "equals")) {
                if (String(currentValue ?? "") !== String(field.showWhen.equals)) return null;
              }
            }

            const fieldId = `field-${field.name}`;
            const localizedLabel = localizeFieldLabel(effectiveDiscipline, formLanguage, field);
            const localizedHelper = localizeFieldHelper(effectiveDiscipline, formLanguage, field);
            const helperText = (() => {
              const parts: string[] = [];
              if (localizedHelper) parts.push(localizedHelper);
              if (field.type === "number" && (typeof field.min === "number" || typeof field.max === "number")) {
                const min = typeof field.min === "number" ? String(field.min) : "-inf";
                const max = typeof field.max === "number" ? String(field.max) : "inf";
                parts.push(`${copy.range}: ${min} ${copy.to} ${max}${field.unit ? ` ${localizeUnit(formLanguage, field.unit)}` : ""}`);
              }
              return parts.length ? parts.join(" | ") : undefined;
            })();
            const unitLabel = field.unit ? ` (${localizeUnit(formLanguage, field.unit)})` : "";

            return (
              <div key={field.name} className="space-y-1">
                <label htmlFor={fieldId} className="flex items-center gap-1 text-xs uppercase tracking-wide text-muted-foreground">
                  <span>{localizedLabel}{unitLabel}</span>
                  <span className="text-danger">*</span>
                  <TermHelp term={field.name} fallbackLabel={localizedLabel} fallbackDescription={helperText} />
                </label>
                {field.type === "select" ? (
                  <Select id={fieldId} {...register(field.name)}>
                    {field.optionGroups && field.optionGroups.length > 0
                      ? field.optionGroups.map((group) => (
                        <optgroup key={group.label} label={localizeOptionGroupLabel(formLanguage, group.label)}>
                          {group.options.map((option) => (
                            <option key={option.value} value={option.value}>
                              {localizeOptionLabel(effectiveDiscipline, formLanguage, field.name, option.value, option.label)}
                            </option>
                          ))}
                        </optgroup>
                      ))
                      : field.options?.map((option) => (
                        <option key={option.value} value={option.value}>
                          {localizeOptionLabel(effectiveDiscipline, formLanguage, field.name, option.value, option.label)}
                        </option>
                      ))}
                  </Select>
                ) : field.type === "checkbox" ? (
                  <label htmlFor={fieldId} className="flex items-center gap-2 rounded-[6px] border border-border bg-muted px-3 py-2">
                    <input id={fieldId} type="checkbox" {...register(field.name)} />
                    <span className="text-sm text-foreground">{localizedHelper ?? copy.toggleOption}</span>
                    <TermHelp term={field.name} fallbackLabel={localizedLabel} fallbackDescription={helperText} />
                  </label>
                ) : (
                  <Input
                    id={fieldId}
                    type={field.type}
                    min={field.min}
                    max={field.max}
                    step={field.step}
                    placeholder={field.placeholder}
                    {...register(field.name)}
                  />
                )}
                {errors[field.name] && (
                  <p className="text-xs text-danger">{String(errors[field.name]?.message ?? copy.invalidValue)}</p>
                )}
                {helperText && field.type !== "checkbox" && <p className="text-xs text-muted-foreground">{helperText}</p>}
              </div>
            );
          })}

          {showForceBlockedToggle && (
            <label className="mt-2 flex items-center gap-2 rounded-[6px] border border-border bg-muted px-3 py-2 text-sm">
              <input
                type="checkbox"
                checked={forceBlocked}
                onChange={(event) => setValue("force_blocked", event.target.checked as FormValues["force_blocked"])}
              />
              {copy.forceBlocked}
            </label>
          )}

          <div className="mt-2 grid grid-cols-2 gap-2">
            <Button type="button" variant="outline" onClick={() => reset(defaultValues)} disabled={submitting}>
              {copy.resetSample}
            </Button>
            <Button type="submit" disabled={submitting}>
              {submitting ? copy.calculating : copy.runCalculation}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
