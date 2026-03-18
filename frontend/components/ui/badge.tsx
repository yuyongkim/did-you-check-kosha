import { ReactNode } from "react";

import { cn } from "@/lib/utils";

const styleMap = {
  ok: "border-success/35 bg-success/12 text-success",
  warning: "border-warning/35 bg-warning/15 text-warning",
  blocked: "border-danger/35 bg-danger/12 text-danger",
  error: "border-danger/35 bg-danger/12 text-danger",
  neutral: "border-border/90 bg-muted/70 text-muted-foreground",
};

export function Badge({
  className,
  variant = "neutral",
  children,
}: {
  className?: string;
  variant?: keyof typeof styleMap;
  children: ReactNode;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-[6px] border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.08em]",
        styleMap[variant],
        className,
      )}
    >
      {children}
    </span>
  );
}

