import { ReactNode } from "react";

import { cn } from "@/lib/utils";

interface ThreePaneLayoutProps {
  left: ReactNode;
  center: ReactNode;
  right: ReactNode;
  className?: string;
}

export function ThreePaneLayout({ left, center, right, className }: ThreePaneLayoutProps) {
  return (
    <section className={cn("grid gap-3 px-4 py-4 xl:grid-cols-[minmax(300px,25%)_minmax(0,50%)_minmax(300px,25%)]", className)}>
      <div className="order-1 flex min-h-[320px] flex-col gap-3">{left}</div>
      <div className="order-3 flex min-h-[320px] flex-col gap-3 xl:order-2">{center}</div>
      <div className="order-2 flex min-h-[320px] flex-col gap-3 xl:order-3 xl:sticky xl:top-[74px] xl:max-h-[calc(100vh-86px)] xl:overflow-y-auto">
        {right}
      </div>
    </section>
  );
}

