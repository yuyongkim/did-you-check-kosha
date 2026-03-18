import * as React from "react";

import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "danger";
}

const variantClass: Record<NonNullable<ButtonProps["variant"]>, string> = {
  default:
    "border border-primary bg-primary text-accent-foreground shadow-[inset_0_1px_0_rgba(255,255,255,0.2)] hover:bg-primary/90",
  outline:
    "border border-border/90 bg-background text-foreground hover:border-primary/45 hover:bg-muted",
  danger: "border border-danger bg-danger text-white hover:bg-danger/90",
};

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex h-9 items-center justify-center rounded-[6px] px-3 text-sm font-semibold tracking-[0.01em] transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/45 disabled:cursor-not-allowed disabled:opacity-60",
          variantClass[variant],
          className,
        )}
        {...props}
      />
    );
  },
);
Button.displayName = "Button";

