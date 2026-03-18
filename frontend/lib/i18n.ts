export type UiLanguage = "en" | "ko";

export function detectLanguage(pathname?: string): UiLanguage {
  if (!pathname) return "en";
  return pathname === "/ko" || pathname.startsWith("/ko/") ? "ko" : "en";
}

export function stripLanguagePrefix(pathname: string): string {
  if (pathname === "/ko") return "/";
  if (pathname.startsWith("/ko/")) {
    const stripped = pathname.slice(3);
    return stripped.startsWith("/") ? stripped : `/${stripped}`;
  }
  return pathname || "/";
}

export function localizeHref(href: string, language: UiLanguage): string {
  const normalized = href.startsWith("/") ? href : `/${href}`;
  if (language === "en") return normalized;
  if (normalized === "/") return "/ko";
  return `/ko${normalized}`;
}

export function switchLanguagePath(pathname: string, target: UiLanguage): string {
  const base = stripLanguagePrefix(pathname || "/");
  return localizeHref(base, target);
}

