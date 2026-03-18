"use client";

import { useEffect, useState } from "react";

export type ThemePalette = "calm" | "vivid";

const STORAGE_KEY = "epc-theme-palette";
const DEFAULT_PALETTE: ThemePalette = "calm";

function applyPalette(palette: ThemePalette): void {
  if (typeof document === "undefined") return;
  const root = document.documentElement;
  root.classList.remove("theme-calm", "theme-vivid");
  root.classList.add(`theme-${palette}`);
}

export function useThemePalette() {
  const [palette, setPalette] = useState<ThemePalette>(DEFAULT_PALETTE);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const saved = window.localStorage.getItem(STORAGE_KEY);
    if (saved === "calm" || saved === "vivid") {
      setPalette(saved);
      return;
    }
    setPalette(DEFAULT_PALETTE);
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") return;
    applyPalette(palette);
    window.localStorage.setItem(STORAGE_KEY, palette);
  }, [palette]);

  return { palette, setPalette };
}

