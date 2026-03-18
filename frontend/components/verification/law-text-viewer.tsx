"use client";

import { useMemo, useState } from "react";

import { Button } from "@/components/ui/button";

interface LawTextViewerProps {
  text: string;
  language: "en" | "ko";
}

const MIN_FONT_PX = 11;
const MAX_FONT_PX = 18;
const DEFAULT_FONT_PX = 13;

export function LawTextViewer({ text, language }: LawTextViewerProps) {
  const [open, setOpen] = useState(false);
  const [fontPx, setFontPx] = useState(DEFAULT_FONT_PX);

  const copy = useMemo(
    () => (language === "ko"
      ? {
          open: "원문 보기",
          close: "원문 닫기",
          zoomOut: "축소",
          zoomIn: "확대",
          reset: "기본",
          body: "법령 원문",
          font: "글자",
        }
      : {
          open: "View original",
          close: "Hide original",
          zoomOut: "Zoom out",
          zoomIn: "Zoom in",
          reset: "Reset",
          body: "Original text",
          font: "Font",
        }),
    [language],
  );

  const normalized = text.trim();
  if (!normalized) return null;

  return (
    <div className="mt-2 space-y-1">
      <div className="flex flex-wrap items-center gap-1">
        <Button
          type="button"
          variant="outline"
          className="h-7 px-2 text-[11px]"
          onClick={() => setOpen((prev) => !prev)}
        >
          {open ? copy.close : copy.open}
        </Button>
        <Button
          type="button"
          variant="outline"
          className="h-7 px-2 text-[11px]"
          onClick={() => setFontPx((prev) => Math.max(MIN_FONT_PX, prev - 1))}
          disabled={!open || fontPx <= MIN_FONT_PX}
        >
          {copy.zoomOut}
        </Button>
        <Button
          type="button"
          variant="outline"
          className="h-7 px-2 text-[11px]"
          onClick={() => setFontPx((prev) => Math.min(MAX_FONT_PX, prev + 1))}
          disabled={!open || fontPx >= MAX_FONT_PX}
        >
          {copy.zoomIn}
        </Button>
        <Button
          type="button"
          variant="outline"
          className="h-7 px-2 text-[11px]"
          onClick={() => setFontPx(DEFAULT_FONT_PX)}
          disabled={!open || fontPx === DEFAULT_FONT_PX}
        >
          {copy.reset}
        </Button>
        <span className="text-[11px] text-muted-foreground">{copy.font} {fontPx}px</span>
      </div>

      {open && (
        <div className="rounded-[6px] border border-border bg-muted p-2">
          <p className="mb-1 text-[11px] uppercase tracking-wide text-primary">{copy.body}</p>
          <div
            className="max-h-60 overflow-auto whitespace-pre-wrap text-foreground"
            style={{ fontSize: `${fontPx}px`, lineHeight: 1.55 }}
          >
            {normalized}
          </div>
        </div>
      )}
    </div>
  );
}
