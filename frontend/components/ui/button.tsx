import * as React from "react";

import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "danger" | "ghost";
}

const variantClass: Record<NonNullable<ButtonProps["variant"]>, string> = {
  default:
    "border border-primary bg-primary text-accent-foreground shadow-[inset_0_1px_0_rgba(255,255,255,0.18)] hover:bg-primary/85 active:scale-[0.97]",
  outline:
    "border border-border/80 bg-card/60 backdrop-blur-sm text-foreground hover:border-primary/50 hover:bg-primary/8 active:scale-[0.97]",
  danger:
    "border border-danger bg-danger text-white hover:bg-danger/85 active:scale-[0.97]",
  ghost:
    "border border-transparent bg-transparent text-foreground hover:bg-muted/70 active:scale-[0.97]",
};

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex h-9 items-center justify-center rounded-lg px-3 text-sm font-semibold tracking-[0.01em] transition-all duration-[180ms] ease-[cubic-bezier(0.2,0.8,0.2,1)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/50 focus-visible:ring-offset-1 disabled:pointer-events-none disabled:opacity-50",
          variantClass[variant],
          className,
        )}
        {...props}
      />
    );
  },
);
Button.displayName = "Button";
