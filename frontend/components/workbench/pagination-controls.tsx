"use client";

import { Button } from "@/components/ui/button";

export function PaginationControls({
  page,
  totalPages,
  prevLabel,
  nextLabel,
  pageLabel,
  onPrev,
  onNext,
}: {
  page: number;
  totalPages: number;
  prevLabel: string;
  nextLabel: string;
  pageLabel: string;
  onPrev: () => void;
  onNext: () => void;
}) {
  return (
    <div className="mt-2 flex items-center justify-between text-xs text-muted-foreground">
      <span>{pageLabel}: {Math.min(page, totalPages)}/{totalPages}</span>
      <div className="flex gap-2">
        <Button className="h-7 px-2 text-[11px]" variant="outline" disabled={page <= 1} onClick={onPrev}>{prevLabel}</Button>
        <Button className="h-7 px-2 text-[11px]" variant="outline" disabled={page >= totalPages} onClick={onNext}>{nextLabel}</Button>
      </div>
    </div>
  );
}
