import * as React from "react";

import { cn } from "@/lib/utils";

export const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={cn(
          "h-9 w-full rounded-[6px] border border-border/90 bg-background px-3 text-sm text-foreground shadow-[inset_0_1px_0_rgba(255,255,255,0.15)] outline-none transition placeholder:text-muted-foreground/85 focus:border-primary/60 focus:ring-2 focus:ring-primary/20",
          className,
        )}
        {...props}
      />
    );
  },
);
Input.displayName = "Input";

