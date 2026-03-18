"use client";

import { useEffect, useMemo, useState } from "react";
import { BookOpenText, Download, Eye, Factory, FileDown, Info, MonitorCog, Moon, Settings, Sun, X } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { Select } from "@/components/ui/select";
import { ThemePalette, useThemePalette } from "@/hooks/useThemePalette";
import { ThemeMode, useThemeMode } from "@/hooks/useThemeMode";
import { buildResultMarkdown, exportResultJson, exportResultMarkdown } from "@/lib/exporters";
import { NAV_ITEMS } from "@/lib/navigation";
import { WorkbenchMode, useWorkbenchStore } from "@/store/workbench-store";

export function TopBar() {
  const router = useRouter();
  const [showSettings, setShowSettings] = useState(false);
  const [showReportPreview, setShowReportPreview] = useState(false);
  const { mode, resolvedMode, setMode, toggleMode } = useThemeMode();
  const { palette, setPalette } = useThemePalette();
  const { language, isKorean, basePath, localizedHref, switchPath } = useUiLanguage();

  const labels = useMemo(
    () =>
      language === "ko"
        ? {
            console: "엔지니어링 콘솔",
            project: "프로젝트",
            asset: "자산",
            apiMode: "API 모드",
            apiMock: "모의",
            apiBackend: "백엔드",
            exportJson: "JSON",
            exportMd: "보고서",
            preview: "미리보기",
            reportPreviewTitle: "보고서 미리보기",
            close: "닫기",
            reportPreviewEmpty: "계산 결과가 없어 미리보기를 표시할 수 없습니다.",
            settings: "설정",
            language: "언어",
            glossary: "용어집",
            calcGuide: "계산 안내",
            theme: "테마",
            themeLight: "라이트",
            themeDark: "다크",
            themeSystem: "시스템",
            colorTone: "색상 톤",
            colorToneCalm: "차분",
            colorToneVivid: "강조",
            workbenchMode: "워크벤치 모드",
            modeBeginner: "입문",
            modeStandard: "표준",
            modeMaster: "마스터",
            backendPrefix: "백엔드 API Prefix",
            mockDescription: "Mock = 로컬 샘플 계산 엔진(외부 복사 아님)",
            backendDescription: "백엔드 = 외부 API 연동",
            activeTheme: "현재",
            localRoute: "로컬 라우트",
            externalRoute: "외부 연동",
          }
        : {
            console: "Engineering Console",
            project: "Project",
            asset: "Asset",
            apiMode: "API Mode",
            apiMock: "Mock",
            apiBackend: "Backend",
            exportJson: "JSON",
            exportMd: "MD",
            preview: "Preview",
            reportPreviewTitle: "Report Preview",
            close: "Close",
            reportPreviewEmpty: "No calculation result to preview.",
            settings: "Settings",
            language: "Language",
            glossary: "Glossary",
            calcGuide: "Calculation Guide",
            theme: "Theme",
            themeLight: "Light",
            themeDark: "Dark",
            themeSystem: "System",
            colorTone: "Color Tone",
            colorToneCalm: "Calm",
            colorToneVivid: "Vivid",
            workbenchMode: "Workbench Mode",
            modeBeginner: "Beginner",
            modeStandard: "Standard",
            modeMaster: "Master",
            backendPrefix: "Backend API Prefix",
            mockDescription: "Mock = local simulated calculation engine (not copied)",
            backendDescription: "Backend = external API integration",
            activeTheme: "active",
            localRoute: "local route",
            externalRoute: "external",
          },
    [language],
  );
  const koLabelMap: Record<string, string> = {
    Piping: "배관",
    "Static Equipment": "정기기",
    Rotating: "회전기기",
    Electrical: "전기",
    Instrumentation: "계장",
    "Steel Structure": "철골구조",
    "Civil Concrete": "토목콘크리트",
  };

  const activeDiscipline = useWorkbenchStore((state) => state.activeDiscipline);
  const projectId = useWorkbenchStore((state) => state.activeProjectId);
  const assetId = useWorkbenchStore((state) => state.activeAssetId);
  const apiMode = useWorkbenchStore((state) => state.apiMode);
  const backendApiPrefix = useWorkbenchStore((state) => state.backendApiPrefix);
  const resultByDiscipline = useWorkbenchStore((state) => state.resultByDiscipline);
  const workbenchMode = useWorkbenchStore((state) => state.workbenchMode);

  const setProject = useWorkbenchStore((state) => state.setProject);
  const setAsset = useWorkbenchStore((state) => state.setAsset);
  const setApiMode = useWorkbenchStore((state) => state.setApiMode);
  const setBackendApiPrefix = useWorkbenchStore((state) => state.setBackendApiPrefix);
  const setWorkbenchMode = useWorkbenchStore((state) => state.setWorkbenchMode);

  const activeResult = resultByDiscipline[activeDiscipline];
  const apiBadge = apiMode === "mock" ? labels.apiMock : labels.apiBackend;
  const apiBadgeText = language === "ko" ? apiBadge : apiBadge.toUpperCase();
  const modeLabel = mode === "dark" ? labels.themeDark : mode === "light" ? labels.themeLight : labels.themeSystem;
  const resolvedModeLabel = resolvedMode === "dark" ? labels.themeDark : labels.themeLight;
  const paletteLabel = palette === "vivid" ? labels.colorToneVivid : labels.colorToneCalm;
  const reportPreview = useMemo(() => {
    if (!activeResult) return "";
    return buildResultMarkdown(activeResult, { projectId, assetId, discipline: activeDiscipline });
  }, [activeResult, activeDiscipline, assetId, projectId]);

  function openReportPreview(): void {
    setShowReportPreview(true);
  }

  function handleJsonExport(): void {
    if (!activeResult) {
      openReportPreview();
      return;
    }
    exportResultJson(activeResult, { projectId, assetId, discipline: activeDiscipline });
  }

  function handleMarkdownExport(): void {
    if (!activeResult) {
      openReportPreview();
      return;
    }
    exportResultMarkdown(activeResult, { projectId, assetId, discipline: activeDiscipline });
  }

  const selectedPath = useMemo(() => {
    const match = NAV_ITEMS.find((item) => item.href === basePath);
    return match?.href ?? "/piping";
  }, [basePath]);

  useEffect(() => {
    if (typeof document === "undefined") return;
    document.documentElement.lang = isKorean ? "ko" : "en";
  }, [isKorean]);

  return (
    <header className="fixed inset-x-0 top-0 z-40 border-b border-border/90 bg-background/95 backdrop-blur-sm">
      <div className="relative flex h-[60px] items-center gap-2 px-4">
        <Link href={localizedHref("/")} className="mr-1 flex min-w-0 items-center gap-2">
          <span className="inline-flex h-7 w-7 items-center justify-center rounded-[6px] border border-primary/35 bg-primary/10 text-primary">
            <Factory className="h-4 w-4" />
          </span>
          <div className="hidden min-w-0 sm:block">
            <p className="font-display truncate text-xs font-semibold uppercase tracking-[0.14em] text-secondary">EPC Maintenance AI</p>
            <p className="truncate text-[10px] font-medium uppercase tracking-[0.12em] text-muted-foreground">{labels.console}</p>
          </div>
        </Link>

        <span className="hidden h-6 w-px bg-border md:block" />

        <div className="hidden items-center gap-2 md:flex">
          <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">{labels.project}</span>
          <Input
            value={projectId}
            onChange={(event) => setProject(event.target.value)}
            className="h-8 w-[150px] text-xs font-medium"
          />
        </div>

        <div className="hidden items-center gap-2 lg:flex">
          <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">{labels.asset}</span>
          <Input
            value={assetId}
            onChange={(event) => setAsset(event.target.value)}
            className="h-8 w-[150px] text-xs font-medium"
          />
        </div>

        <div className="ml-auto flex items-center gap-2">
          <div className="w-[140px] md:w-[170px]">
            <Select
              value={selectedPath}
              onChange={(event) => router.push(localizedHref(event.target.value))}
              className="h-8 text-xs font-medium"
            >
              {NAV_ITEMS.map((item) => (
                <option key={item.href} value={item.href}>
                  [{item.tag}] {language === "ko" ? (koLabelMap[item.label] ?? item.label) : item.label}
                </option>
              ))}
            </Select>
          </div>
          <div className="hidden w-[110px] lg:block">
            <Select
              value={workbenchMode}
              onChange={(event) => setWorkbenchMode(event.target.value as WorkbenchMode)}
              className="h-8 text-xs"
              title={labels.workbenchMode}
            >
              <option value="beginner">{labels.modeBeginner}</option>
              <option value="standard">{labels.modeStandard}</option>
              <option value="master">{labels.modeMaster}</option>
            </Select>
          </div>
          <span title={apiMode === "mock" ? labels.mockDescription : labels.backendDescription}>
            <Badge variant={apiMode === "mock" ? "warning" : "ok"}>
              {apiBadgeText}
            </Badge>
          </span>
          <Button
            variant="outline"
            className="h-8 gap-1.5 px-2 text-xs"
            aria-label={labels.exportJson}
            title={labels.exportJson}
            onClick={handleJsonExport}
          >
            <Download className="h-3.5 w-3.5" />
            <span className="hidden xl:inline">{labels.exportJson}</span>
          </Button>
          <Button
            variant="outline"
            className="h-8 gap-1.5 px-2 text-xs"
            aria-label={labels.exportMd}
            title={labels.exportMd}
            onClick={handleMarkdownExport}
          >
            <FileDown className="h-3.5 w-3.5" />
            <span className="hidden xl:inline">{labels.exportMd}</span>
          </Button>
          <Button
            variant="outline"
            className="h-8 gap-1.5 px-2 text-xs"
            aria-label={labels.preview}
            title={labels.preview}
            onClick={openReportPreview}
          >
            <Eye className="h-3.5 w-3.5" />
            <span className="hidden xl:inline">{labels.preview}</span>
          </Button>
          <Button
            variant="outline"
            className="h-8 px-2 text-xs"
            title={labels.settings}
            onClick={() => setShowSettings((prev) => !prev)}
          >
            <Settings className="h-3.5 w-3.5" />
          </Button>
          <Button
            variant="outline"
            className="h-8 px-2 text-xs font-semibold"
            title={labels.language}
            onClick={() => router.push(switchPath(isKorean ? "en" : "ko"))}
          >
            {isKorean ? "EN" : "KO"}
          </Button>
          <Button
            variant="outline"
            className="h-8 px-2 text-xs"
            title={`${labels.theme}: ${modeLabel} (${resolvedModeLabel})`}
            onClick={toggleMode}
          >
            {resolvedMode === "dark" ? <Moon className="h-3.5 w-3.5" /> : <Sun className="h-3.5 w-3.5" />}
          </Button>
          <Link href={localizedHref("/glossary")}>
            <Button variant="outline" className="h-8 px-2 text-xs" title={labels.glossary}>
              <BookOpenText className="h-3.5 w-3.5" />
            </Button>
          </Link>
          <Link href={localizedHref("/calculation-guide")}>
            <Button variant="outline" className="h-8 px-2 text-xs" title={labels.calcGuide}>
              <Info className="h-3.5 w-3.5" />
            </Button>
          </Link>
        </div>

        {showSettings && (
          <section className="absolute right-4 top-[64px] z-50 grid w-[min(100vw-2rem,960px)] gap-3 rounded-[8px] border border-border/90 bg-card p-3 shadow-panel md:grid-cols-6">
            <label className="space-y-1">
              <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">{labels.apiMode}</span>
              <Select value={apiMode} onChange={(event) => setApiMode(event.target.value as "mock" | "backend")}>
                <option value="mock">{labels.apiMock} ({labels.localRoute})</option>
                <option value="backend">{labels.apiBackend} ({labels.externalRoute})</option>
              </Select>
            </label>

            <label className="space-y-1">
              <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">{labels.theme}</span>
              <Select value={mode} onChange={(event) => setMode(event.target.value as ThemeMode)}>
                <option value="light">{labels.themeLight}</option>
                <option value="dark">{labels.themeDark}</option>
                <option value="system">{labels.themeSystem}</option>
              </Select>
              <p className="flex items-center gap-1 text-[11px] text-muted-foreground">
                <MonitorCog className="h-3 w-3" />
                {labels.activeTheme}: {resolvedModeLabel}
              </p>
            </label>

            <label className="space-y-1">
              <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">{labels.colorTone}</span>
              <Select value={palette} onChange={(event) => setPalette(event.target.value as ThemePalette)}>
                <option value="calm">{labels.colorToneCalm}</option>
                <option value="vivid">{labels.colorToneVivid}</option>
              </Select>
              <p className="text-[11px] text-muted-foreground">
                {labels.activeTheme}: {paletteLabel}
              </p>
            </label>

            <label className="space-y-1">
              <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">{labels.workbenchMode}</span>
              <Select value={workbenchMode} onChange={(event) => setWorkbenchMode(event.target.value as WorkbenchMode)}>
                <option value="beginner">{labels.modeBeginner}</option>
                <option value="standard">{labels.modeStandard}</option>
                <option value="master">{labels.modeMaster}</option>
              </Select>
            </label>

            <label className="space-y-1 md:col-span-2">
              <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">{labels.backendPrefix}</span>
              <Input
                placeholder="http://localhost:8000"
                value={backendApiPrefix}
                disabled={apiMode !== "backend"}
                onChange={(event) => setBackendApiPrefix(event.target.value)}
              />
            </label>
          </section>
        )}
      </div>

      {showReportPreview && (
        <section
          className="fixed inset-0 z-[70] flex items-start justify-center bg-background/70 px-3 py-16 backdrop-blur-[2px]"
          onClick={() => setShowReportPreview(false)}
        >
          <article
            className="w-[min(1040px,96vw)] rounded-[10px] border border-border/90 bg-card shadow-panel"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="flex items-center justify-between border-b border-border/80 px-4 py-3">
              <p className="text-sm font-semibold text-secondary">{labels.reportPreviewTitle}</p>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  className="h-8 gap-1.5 px-2 text-xs"
                  disabled={!activeResult}
                  onClick={handleMarkdownExport}
                >
                  <FileDown className="h-3.5 w-3.5" />
                  {labels.exportMd}
                </Button>
                <Button variant="outline" className="h-8 px-2 text-xs" onClick={() => setShowReportPreview(false)}>
                  <X className="h-3.5 w-3.5" />
                  {labels.close}
                </Button>
              </div>
            </div>
            <div className="max-h-[72vh] overflow-auto p-4">
              {!activeResult && (
                <p className="text-sm text-muted-foreground">{labels.reportPreviewEmpty}</p>
              )}
              {activeResult && (
                <pre className="whitespace-pre-wrap rounded-[8px] border border-border bg-muted p-3 text-xs leading-5 text-foreground">
                  {reportPreview}
                </pre>
              )}
            </div>
          </article>
        </section>
      )}
    </header>
  );
}
