import { ReactNode } from "react";

import { Sidebar } from "@/components/layout/sidebar";
import { TopBar } from "@/components/layout/top-bar";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <TopBar />
      <div className="grid min-h-screen grid-cols-1 pt-[60px] lg:grid-cols-[252px_minmax(0,1fr)]">
        <div className="hidden lg:block">
          <Sidebar />
        </div>
        <div className="flex min-h-[calc(100vh-60px)] min-w-0 flex-col border-l border-border/60">
          {children}
        </div>
      </div>
    </div>
  );
}

