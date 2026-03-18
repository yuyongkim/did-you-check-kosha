"use client";

import { useEffect, useRef, useState } from "react";
import { HelpCircle } from "lucide-react";

import { getTermDefinition, getTermLabel } from "@/lib/glossary";
import { cn } from "@/lib/utils";

interface TermHelpProps {
  term: string;
  fallbackLabel?: string;
  fallbackDescription?: string;
  className?: string;
}

export function TermHelp({
  term,
  fallbackLabel,
  fallbackDescription,
  className,
}: TermHelpProps) {
  const label = getTermLabel(term, fallbackLabel);
  const description = getTermDefinition(term) || fallbackDescription || "Engineering term used in the calculation and verification workflow.";
  const tooltip = `${label}: ${description}`;
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLSpanElement | null>(null);

  useEffect(() => {
    function onPointerDown(event: PointerEvent) {
      if (!rootRef.current) return;
      if (!rootRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    }
    window.addEventListener("pointerdown", onPointerDown);
    return () => window.removeEventListener("pointerdown", onPointerDown);
  }, []);

  return (
    <span
      ref={rootRef}
      className={cn("relative inline-flex align-middle", className)}
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
    >
      <button
        type="button"
        className="inline-flex cursor-help text-muted-foreground hover:text-primary focus:outline-none focus-visible:ring-2 focus-visible:ring-primary"
        aria-label={tooltip}
        aria-expanded={open}
        title={tooltip}
        onClick={() => setOpen((prev) => !prev)}
      >
        <HelpCircle className="h-3.5 w-3.5" />
      </button>
      <span
        role="tooltip"
        className={cn(
          "pointer-events-none absolute left-1/2 top-full z-50 mt-2 w-72 -translate-x-1/2 rounded-[6px] border border-border bg-card px-3 py-2 text-left",
          open ? "block" : "hidden",
        )}
      >
        <span className="block text-[10px] uppercase tracking-wider text-primary">{label}</span>
        <span className="mt-1 block text-xs leading-snug text-foreground">{description}</span>
      </span>
    </span>
  );
}
