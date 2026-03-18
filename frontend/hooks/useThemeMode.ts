"use client";

import { useEffect, useState } from "react";

export type ThemeMode = "light" | "dark" | "system";

const STORAGE_KEY = "epc-theme-mode";
const DEFAULT_MODE: ThemeMode = "light";

function getSystemTheme(): "light" | "dark" {
  if (typeof window === "undefined") return "light";
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function resolveTheme(mode: ThemeMode): "light" | "dark" {
  return mode === "system" ? getSystemTheme() : mode;
}

function applyTheme(mode: ThemeMode): "light" | "dark" {
  if (typeof document === "undefined") return "light";
  const resolved = resolveTheme(mode);
  const root = document.documentElement;
  root.classList.toggle("dark", resolved === "dark");
  root.style.colorScheme = resolved;
  return resolved;
}

export function useThemeMode() {
  const [mode, setMode] = useState<ThemeMode>(DEFAULT_MODE);
  const [resolvedMode, setResolvedMode] = useState<"light" | "dark">("light");

  useEffect(() => {
    if (typeof window === "undefined") return;
    const saved = window.localStorage.getItem(STORAGE_KEY);
    if (saved === "light" || saved === "dark") {
      setMode(saved);
      return;
    }
    if (saved === "system") {
      // Avoid unexpected background flips by migrating legacy "system" default to light.
      setMode(DEFAULT_MODE);
      window.localStorage.setItem(STORAGE_KEY, DEFAULT_MODE);
    }
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const resolved = applyTheme(mode);
    setResolvedMode(resolved);
    window.localStorage.setItem(STORAGE_KEY, mode);

    if (mode !== "system") return;

    const media = window.matchMedia("(prefers-color-scheme: dark)");
    const onChange = () => setResolvedMode(applyTheme("system"));
    media.addEventListener("change", onChange);
    return () => media.removeEventListener("change", onChange);
  }, [mode]);

  function toggleMode() {
    setMode((prev) => {
      if (prev === "system") return resolvedMode === "dark" ? "light" : "dark";
      return prev === "dark" ? "light" : "dark";
    });
  }

  return { mode, resolvedMode, setMode, toggleMode };
}
