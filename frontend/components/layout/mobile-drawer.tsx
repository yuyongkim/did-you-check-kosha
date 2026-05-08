"use client";

import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { usePathname } from "next/navigation";
import { X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Sidebar } from "@/components/layout/sidebar";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { useWorkbenchStore } from "@/store/workbench-store";

interface MobileDrawerProps {
  open: boolean;
  onClose: () => void;
}

export function MobileDrawer({ open, onClose }: MobileDrawerProps) {
  const pathname = usePathname();
  const { language } = useUiLanguage();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  const projectId = useWorkbenchStore((state) => state.activeProjectId);
  const assetId = useWorkbenchStore((state) => state.activeAssetId);
  const setProject = useWorkbenchStore((state) => state.setProject);
  const setAsset = useWorkbenchStore((state) => state.setAsset);

  const labels = language === "ko"
    ? { project: "프로젝트", asset: "자산", close: "닫기", menu: "메뉴" }
    : { project: "Project", asset: "Asset", close: "Close", menu: "Menu" };

  useEffect(() => {
    if (!open) return;
    onClose();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname]);

  useEffect(() => {
    if (!open) return;
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = previous;
    };
  }, [open]);

  useEffect(() => {
    if (!open) return;
    function onKey(event: KeyboardEvent) {
      if (event.key === "Escape") onClose();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open || !mounted) return null;

  return createPortal(
    <div className="fixed inset-0 z-[80] lg:hidden" role="dialog" aria-modal="true" aria-label={labels.menu}>
      <div
        className="absolute inset-0 bg-background/70 backdrop-blur-[2px]"
        onClick={onClose}
      />
      <aside className="absolute inset-y-0 left-0 flex h-full w-[min(82vw,320px)] flex-col border-r border-border/80 bg-background shadow-panel">
        <div className="flex items-center justify-between border-b border-border/70 px-3 py-2">
          <p className="text-[11px] font-semibold uppercase tracking-[0.14em] text-muted-foreground">
            {labels.menu}
          </p>
          <Button
            variant="outline"
            className="h-8 px-2 text-xs"
            onClick={onClose}
            aria-label={labels.close}
            title={labels.close}
          >
            <X className="h-3.5 w-3.5" />
          </Button>
        </div>

        <div className="space-y-2 border-b border-border/70 px-3 py-3">
          <label className="block space-y-1">
            <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">
              {labels.project}
            </span>
            <Input
              value={projectId}
              onChange={(event) => setProject(event.target.value)}
              className="h-9 text-xs font-medium"
            />
          </label>
          <label className="block space-y-1">
            <span className="text-[10px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">
              {labels.asset}
            </span>
            <Input
              value={assetId}
              onChange={(event) => setAsset(event.target.value)}
              className="h-9 text-xs font-medium"
            />
          </label>
        </div>

        <div className="flex-1 overflow-y-auto">
          <Sidebar />
        </div>
      </aside>
    </div>,
    document.body,
  );
}
