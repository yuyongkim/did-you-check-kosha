"use client";

import { useMemo } from "react";
import { usePathname } from "next/navigation";

import { detectLanguage, localizeHref, stripLanguagePrefix, switchLanguagePath, UiLanguage } from "@/lib/i18n";

export function useUiLanguage() {
  const pathname = usePathname() ?? "/";

  return useMemo(() => {
    const language = detectLanguage(pathname);
    const basePath = stripLanguagePrefix(pathname);
    return {
      language,
      pathname,
      basePath,
      isKorean: language === "ko",
      localizedHref: (href: string) => localizeHref(href, language),
      switchPath: (target: UiLanguage) => switchLanguagePath(pathname, target),
    };
  }, [pathname]);
}

