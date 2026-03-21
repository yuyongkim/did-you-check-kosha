import { ReactNode } from "react";

import { cn } from "@/lib/utils";

const styleMap = {
  ok: "border-success/30 bg-success/10 text-success dark:border-success/40 dark:bg-success/15",
  warning: "border-warning/30 bg-warning/10 text-warning dark:border-warning/40 dark:bg-warning/15",
  blocked: "border-danger/30 bg-danger/10 text-danger dark:border-danger/40 dark:bg-danger/15",
  error: "border-danger/30 bg-danger/10 text-danger dark:border-danger/40 dark:bg-danger/15",
  neutral: "border-border/70 bg-muted/60 text-muted-foreground",
  primary: "border-primary/30 bg-primary/10 text-primary dark:border-primary/40 dark:bg-primary/15",
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
        "inline-flex items-center rounded-full border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.06em] transition-colors duration-150",
        styleMap[variant],
        className,
      )}
    >
      {children}
    </span>
  );
}
