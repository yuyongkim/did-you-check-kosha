import { ReactNode } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function VisualSectionCard({ title, children }: { title: string; children: ReactNode }) {
  return (
    <Card className="animate-fadeUp">
      <CardHeader className="py-2">
        <CardTitle className="text-xs">{title}</CardTitle>
      </CardHeader>
      <CardContent className="py-2">{children}</CardContent>
    </Card>
  );
}
