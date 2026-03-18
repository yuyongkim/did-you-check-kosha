import { z } from "zod";

import { FormFieldConfig } from "@/lib/types";

export function firstSelectValue(field: FormFieldConfig): string {
  const grouped = field.optionGroups?.flatMap((group) => group.options) ?? [];
  const flat = field.options ?? [];
  const all = grouped.length > 0 ? grouped : flat;
  return all[0]?.value ?? "";
}

export function fieldSchema(field: FormFieldConfig): z.ZodTypeAny {
  if (field.type === "number") {
    let schema = z.coerce.number({ invalid_type_error: `${field.label} must be a number.` });
    if (typeof field.min === "number") schema = schema.min(field.min, `${field.label} must be >= ${field.min}.`);
    if (typeof field.max === "number") schema = schema.max(field.max, `${field.label} must be <= ${field.max}.`);
    return schema;
  }
  if (field.type === "checkbox") return z.boolean();
  return z.string().min(1, `${field.label} is required.`);
}
