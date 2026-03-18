"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { useUiLanguage } from "@/hooks/useUiLanguage";
import { formatStandardReference } from "@/lib/standards";
import { CalculationResponse } from "@/lib/types";

export function StandardsReferencePanel({ result }: { result: CalculationResponse | null }) {
  const { language } = useUiLanguage();
  const refs = result ? Array.from(new Set(result.references)) : [];
  const copy = language === "ko"
    ? {
        title: "표준 참조",
        empty: "계산 실행 후 참조 표준이 표시됩니다.",
        reference: "참조",
      }
    : {
        title: "Standards References",
        empty: "References appear after calculation.",
        reference: "Reference",
      };

  return (
    <Card className="animate-fadeUp">
      <CardHeader>
        <CardTitle>{copy.title}</CardTitle>
      </CardHeader>
      <CardContent>
        {refs.length === 0 && <p className="text-sm text-muted-foreground">{copy.empty}</p>}
        {refs.length > 0 && (
          <TableContainer>
            <Table className="min-w-0">
              <TableHeader>
                <TableRow>
                  <TableHead numeric>#</TableHead>
                  <TableHead>{copy.reference}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {refs.map((ref, index) => (
                  <TableRow key={ref}>
                    <TableCell numeric>{index + 1}</TableCell>
                    <TableCell>{formatStandardReference(ref)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </CardContent>
    </Card>
  );
}
