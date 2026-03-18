"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { ArrowDown, ArrowUp, ExternalLink } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { getGlossaryEntries, getTermDeepGuidance } from "@/lib/glossary";
import {
  exportPinsJson,
  loadGlossaryPins,
  movePinned,
  parseImportedPins,
  saveGlossaryPins,
  togglePinned,
} from "@/lib/glossary-pins";
import { GLOSSARY_DISCIPLINE_FILTERS, GlossaryDiscipline } from "@/lib/glossary-types";
import { getStandardDeepGuidance, getStandardGlossaryEntries } from "@/lib/standards";

function downloadText(text: string, filename: string): void {
  if (typeof window === "undefined") return;
  const blob = new Blob([text], { type: "application/json;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.style.display = "none";
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function messageTone(message: string): "normal" | "error" {
  return /failed|invalid|error/i.test(message) ? "error" : "normal";
}

type SortDirection = "asc" | "desc";

function compareText(a: string, b: string, direction: SortDirection): number {
  if (a === b) return 0;
  const value = a.localeCompare(b);
  return direction === "asc" ? value : -value;
}

function SortMarker({ active, direction }: { active: boolean; direction: SortDirection }) {
  if (!active) return null;
  return direction === "asc" ? <ArrowUp className="h-3 w-3" /> : <ArrowDown className="h-3 w-3" />;
}

function StandardGuidance({ code, compact = false }: { code: string; compact?: boolean }) {
  const guide = getStandardDeepGuidance(code);

  return (
    <details className="rounded-[6px] border border-border/70 bg-background/50 px-2 py-1 text-xs text-muted-foreground">
      <summary className="cursor-pointer text-primary">Field Guide</summary>
      <p className="mt-1">
        <span className="font-semibold text-foreground">Intent:</span> {guide.engineeringIntent}
      </p>
      {!compact && (
        <p className="mt-1">
          <span className="font-semibold text-foreground">Practical Use:</span> {guide.practicalUse}
        </p>
      )}
      <p className="mt-1">
        <span className="font-semibold text-foreground">Verify:</span> {guide.whatToVerify.join("; ")}
      </p>
      {!compact && (
        <p className="mt-1">
          <span className="font-semibold text-foreground">Common Misses:</span> {guide.commonMisses.join("; ")}
        </p>
      )}
    </details>
  );
}

function TermGuidance({ term, compact = false }: { term: string; compact?: boolean }) {
  const guide = getTermDeepGuidance(term);

  return (
    <details className="rounded-[6px] border border-border/70 bg-background/50 px-2 py-1 text-xs text-muted-foreground">
      <summary className="cursor-pointer text-primary">Field Guide</summary>
      <p className="mt-1">
        <span className="font-semibold text-foreground">Intent:</span> {guide.engineeringIntent}
      </p>
      {!compact && (
        <p className="mt-1">
          <span className="font-semibold text-foreground">Calculation:</span> {guide.calculationContext}
        </p>
      )}
      <p className="mt-1">
        <span className="font-semibold text-foreground">Input Checks:</span> {guide.inputChecks.join("; ")}
      </p>
      {!compact && (
        <p className="mt-1">
          <span className="font-semibold text-foreground">Common Misses:</span> {guide.commonMisses.join("; ")}
        </p>
      )}
      <p className="mt-1">
        <span className="font-semibold text-foreground">Related:</span> {guide.relatedStandards.join(", ")}
      </p>
    </details>
  );
}

export default function GlossaryPage() {
  const [query, setQuery] = useState("");
  const [discipline, setDiscipline] = useState<GlossaryDiscipline>("all");
  const [pins, setPins] = useState<{ standards: string[]; terms: string[] }>({ standards: [], terms: [] });
  const [ioMessage, setIoMessage] = useState<string>("");
  const [standardSortKey, setStandardSortKey] = useState<"code" | "label">("code");
  const [standardSortDirection, setStandardSortDirection] = useState<SortDirection>("asc");
  const [termSortKey, setTermSortKey] = useState<"key" | "label">("key");
  const [termSortDirection, setTermSortDirection] = useState<SortDirection>("asc");
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    setPins(loadGlossaryPins());
  }, []);

  useEffect(() => {
    saveGlossaryPins(pins);
  }, [pins]);

  const allEngineeringTerms = useMemo(() => getGlossaryEntries(discipline), [discipline]);
  const allStandardTerms = useMemo(() => getStandardGlossaryEntries(discipline), [discipline]);

  const normalized = query.trim().toLowerCase();
  const filteredEngineering = allEngineeringTerms.filter((item) => {
    if (!normalized) return true;
    return (
      item.label.toLowerCase().includes(normalized)
      || item.key.toLowerCase().includes(normalized)
      || item.description.toLowerCase().includes(normalized)
    );
  });

  const filteredStandards = allStandardTerms.filter((item) => {
    if (!normalized) return true;
    return (
      item.code.toLowerCase().includes(normalized)
      || item.label.toLowerCase().includes(normalized)
      || item.summary.toLowerCase().includes(normalized)
    );
  });

  const standardMap = useMemo(
    () => new Map(allStandardTerms.map((item) => [item.code, item])),
    [allStandardTerms],
  );
  const termMap = useMemo(
    () => new Map(allEngineeringTerms.map((item) => [item.key, item])),
    [allEngineeringTerms],
  );

  const pinnedStandards = pins.standards
    .map((code) => standardMap.get(code))
    .filter((item): item is NonNullable<typeof item> => Boolean(item));
  const pinnedEngineering = pins.terms
    .map((key) => termMap.get(key))
    .filter((item): item is NonNullable<typeof item> => Boolean(item));

  const topEngineering = filteredEngineering.slice(0, 10);
  const topStandards = filteredStandards.slice(0, 10);

  const sortedStandards = useMemo(
    () => [...filteredStandards].sort((a, b) => compareText(a[standardSortKey], b[standardSortKey], standardSortDirection)),
    [filteredStandards, standardSortDirection, standardSortKey],
  );

  const sortedTerms = useMemo(
    () => [...filteredEngineering].sort((a, b) => compareText(a[termSortKey], b[termSortKey], termSortDirection)),
    [filteredEngineering, termSortDirection, termSortKey],
  );

  const tone = messageTone(ioMessage);

  function onStandardSort(nextKey: "code" | "label") {
    if (standardSortKey === nextKey) {
      setStandardSortDirection((prev) => (prev === "asc" ? "desc" : "asc"));
      return;
    }
    setStandardSortKey(nextKey);
    setStandardSortDirection("asc");
  }

  function onTermSort(nextKey: "key" | "label") {
    if (termSortKey === nextKey) {
      setTermSortDirection((prev) => (prev === "asc" ? "desc" : "asc"));
      return;
    }
    setTermSortKey(nextKey);
    setTermSortDirection("asc");
  }

  function sortButtonClass(active: boolean) {
    return active
      ? "inline-flex items-center gap-1 text-primary"
      : "inline-flex items-center gap-1 text-muted-foreground";
  }

  return (
    <main className="flex-1 p-4">
      <section className="rounded-lg border border-border bg-card p-5">
        <p className="text-xs uppercase tracking-[0.25em] text-muted-foreground">Glossary</p>
        <h1 className="mt-2 text-3xl font-semibold text-foreground">Term and Standard Guide</h1>
        <p className="mt-2 max-w-4xl text-sm leading-6 text-muted-foreground">
          Browse quick definitions for engineering terms and standard code references used in this workbench.
          Filter by discipline and search by code/keyword. Entries are sorted by practical usage priority first.
        </p>
        <p className="mt-1 max-w-4xl text-xs text-muted-foreground">
          Original standards text is not embedded in-app due licensing. Use the official publisher link in each standard row.
        </p>

        <div className="mt-4 max-w-lg">
          <Input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="UG-27, t_min_mm, corrosion, API 570 ..."
          />
        </div>

        <div className="mt-4 flex flex-wrap gap-2">
          {GLOSSARY_DISCIPLINE_FILTERS.map((item) => (
            <Button
              key={item.value}
              type="button"
              variant={discipline === item.value ? "default" : "outline"}
              className="h-8 px-3 text-xs"
              onClick={() => setDiscipline(item.value)}
            >
              {item.label}
            </Button>
          ))}
        </div>

        <div className="mt-3 text-xs text-muted-foreground">
          {`Standards: ${filteredStandards.length}/${allStandardTerms.length} | Terms: ${filteredEngineering.length}/${allEngineeringTerms.length}`}
        </div>

        <div className="mt-4 flex flex-wrap gap-2">
          <Button
            type="button"
            variant="outline"
            className="h-8 px-3 text-xs"
            onClick={() => {
              downloadText(exportPinsJson(pins), `glossary_pins_${Date.now()}.json`);
              setIoMessage("Pins exported.");
            }}
          >
            Export Pins
          </Button>
          <Button
            type="button"
            variant="outline"
            className="h-8 px-3 text-xs"
            onClick={() => fileInputRef.current?.click()}
          >
            Import Pins
          </Button>
          <Button
            type="button"
            variant="outline"
            className="h-8 px-3 text-xs"
            onClick={() => {
              setPins({ standards: [], terms: [] });
              setIoMessage("Pins cleared.");
            }}
          >
            Clear Pins
          </Button>
          {ioMessage && (
            <p className={tone === "error" ? "self-center text-xs text-danger" : "self-center text-xs text-muted-foreground"}>
              {ioMessage}
            </p>
          )}
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept=".json,application/json"
          className="hidden"
          onChange={async (event) => {
            const file = event.target.files?.[0];
            if (!file) return;
            const text = await file.text();
            const imported = parseImportedPins(text);
            if (!imported) {
              setIoMessage("Import failed: invalid pin JSON format.");
            } else {
              setPins(imported);
              setIoMessage(`Imported pins: ${imported.standards.length} standards, ${imported.terms.length} terms.`);
            }
            event.target.value = "";
          }}
        />
      </section>

      <section className="mt-4 grid gap-4 xl:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Pinned Standards</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {pinnedStandards.length === 0 && (
              <p className="text-sm text-muted-foreground">No pinned standards.</p>
            )}
            {pinnedStandards.map((item, index) => (
              <div key={`pin-standard-${item.code}`} className="rounded-lg border border-border bg-background/70 p-3">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-xs uppercase tracking-wide text-accent">#{index + 1} {item.code}</p>
                  <div className="flex items-center gap-1">
                    <Button
                      type="button"
                      variant="outline"
                      className="h-7 px-2 text-xs"
                      disabled={index === 0}
                      onClick={() => setPins((prev) => ({ ...prev, standards: movePinned(prev.standards, item.code, "up") }))}
                    >
                      Up
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      className="h-7 px-2 text-xs"
                      disabled={index === pinnedStandards.length - 1}
                      onClick={() => setPins((prev) => ({ ...prev, standards: movePinned(prev.standards, item.code, "down") }))}
                    >
                      Down
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      className="h-7 px-2 text-xs"
                      onClick={() => setPins((prev) => ({ ...prev, standards: togglePinned(prev.standards, item.code) }))}
                    >
                      Unpin
                    </Button>
                  </div>
                </div>
                <p className="mt-1 text-sm font-semibold text-foreground">{item.label}</p>
                <p className="mt-1 text-sm text-muted-foreground">{item.summary}</p>
                <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                  <span>Source: {item.publisher}</span>
                  <a
                    href={item.officialUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 text-primary hover:underline"
                  >
                    Official Text
                    <ExternalLink className="h-3 w-3" />
                  </a>
                </div>
                <p className="mt-1 text-[11px] text-muted-foreground">{item.accessNote}</p>
                <div className="mt-2">
                  <StandardGuidance code={item.code} />
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Pinned Terms</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {pinnedEngineering.length === 0 && (
              <p className="text-sm text-muted-foreground">No pinned terms.</p>
            )}
            {pinnedEngineering.map((item, index) => (
              <div key={`pin-term-${item.key}`} className="rounded-lg border border-border bg-background/70 p-3">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-xs uppercase tracking-wide text-muted-foreground">#{index + 1} {item.key}</p>
                  <div className="flex items-center gap-1">
                    <Button
                      type="button"
                      variant="outline"
                      className="h-7 px-2 text-xs"
                      disabled={index === 0}
                      onClick={() => setPins((prev) => ({ ...prev, terms: movePinned(prev.terms, item.key, "up") }))}
                    >
                      Up
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      className="h-7 px-2 text-xs"
                      disabled={index === pinnedEngineering.length - 1}
                      onClick={() => setPins((prev) => ({ ...prev, terms: movePinned(prev.terms, item.key, "down") }))}
                    >
                      Down
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      className="h-7 px-2 text-xs"
                      onClick={() => setPins((prev) => ({ ...prev, terms: togglePinned(prev.terms, item.key) }))}
                    >
                      Unpin
                    </Button>
                  </div>
                </div>
                <p className="mt-1 text-sm font-semibold text-foreground">{item.label}</p>
                <p className="mt-1 text-sm text-muted-foreground">{item.description}</p>
                <div className="mt-2">
                  <TermGuidance term={item.key} />
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </section>

      <section className="mt-4 grid gap-4 xl:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Top 10 Key Standards</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {topStandards.length === 0 && (
              <p className="text-sm text-muted-foreground">No standard code match.</p>
            )}
            {topStandards.map((item, index) => (
              <div key={`${item.code}-${index}`} className="rounded-lg border border-border bg-background/70 p-3">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-xs uppercase tracking-wide text-accent">#{index + 1} {item.code}</p>
                  <Button
                    type="button"
                    variant="outline"
                    className="h-7 px-2 text-xs"
                    onClick={() => setPins((prev) => ({ ...prev, standards: togglePinned(prev.standards, item.code) }))}
                  >
                    {pins.standards.includes(item.code) ? "Pinned" : "Pin"}
                  </Button>
                </div>
                <p className="mt-1 text-sm font-semibold text-foreground">{item.label}</p>
                <p className="mt-1 text-sm text-muted-foreground">{item.summary}</p>
                <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                  <span>Source: {item.publisher}</span>
                  <a
                    href={item.officialUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 text-primary hover:underline"
                  >
                    Official Text
                    <ExternalLink className="h-3 w-3" />
                  </a>
                </div>
                <p className="mt-1 text-[11px] text-muted-foreground">{item.accessNote}</p>
                <div className="mt-2">
                  <StandardGuidance code={item.code} />
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Top 10 Key Terms</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {topEngineering.length === 0 && (
              <p className="text-sm text-muted-foreground">No term match.</p>
            )}
            {topEngineering.map((item, index) => (
              <div key={`${item.key}-${index}`} className="rounded-lg border border-border bg-background/70 p-3">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-xs uppercase tracking-wide text-muted-foreground">#{index + 1} {item.key}</p>
                  <Button
                    type="button"
                    variant="outline"
                    className="h-7 px-2 text-xs"
                    onClick={() => setPins((prev) => ({ ...prev, terms: togglePinned(prev.terms, item.key) }))}
                  >
                    {pins.terms.includes(item.key) ? "Pinned" : "Pin"}
                  </Button>
                </div>
                <p className="mt-1 text-sm font-semibold text-foreground">{item.label}</p>
                <p className="mt-1 text-sm text-muted-foreground">{item.description}</p>
                <div className="mt-2">
                  <TermGuidance term={item.key} />
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </section>

      <section className="mt-4 grid gap-4 xl:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Standards Code Quick Guide</CardTitle>
          </CardHeader>
          <CardContent>
            {filteredStandards.length === 0 && (
              <p className="text-sm text-muted-foreground">No standard code match.</p>
            )}
            {filteredStandards.length > 0 && (
              <TableContainer>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>
                        <button type="button" className={sortButtonClass(standardSortKey === "code")} onClick={() => onStandardSort("code")}>
                          Code
                          <SortMarker active={standardSortKey === "code"} direction={standardSortDirection} />
                        </button>
                      </TableHead>
                      <TableHead>
                        <button type="button" className={sortButtonClass(standardSortKey === "label")} onClick={() => onStandardSort("label")}>
                          Label
                          <SortMarker active={standardSortKey === "label"} direction={standardSortDirection} />
                        </button>
                      </TableHead>
                      <TableHead>Summary</TableHead>
                      <TableHead>Source</TableHead>
                      <TableHead>Original Text</TableHead>
                      <TableHead>Field Guide</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {sortedStandards.map((item) => (
                      <TableRow key={item.code}>
                        <TableCell className="font-data text-xs font-semibold uppercase text-primary">{item.code}</TableCell>
                        <TableCell className="font-semibold">{item.label}</TableCell>
                        <TableCell className="text-muted-foreground">{item.summary}</TableCell>
                        <TableCell className="text-xs text-muted-foreground">{item.publisher}</TableCell>
                        <TableCell className="text-xs text-muted-foreground">
                          <a
                            href={item.officialUrl}
                            target="_blank"
                            rel="noreferrer"
                            className="inline-flex items-center gap-1 text-primary hover:underline"
                          >
                            Open
                            <ExternalLink className="h-3 w-3" />
                          </a>
                          <p className="mt-1 text-[11px] text-muted-foreground">{item.accessNote}</p>
                        </TableCell>
                        <TableCell className="text-xs text-muted-foreground min-w-[260px]">
                          <StandardGuidance code={item.code} compact />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Engineering Terms</CardTitle>
          </CardHeader>
          <CardContent>
            {filteredEngineering.length === 0 && (
              <p className="text-sm text-muted-foreground">No term match.</p>
            )}
            {filteredEngineering.length > 0 && (
              <TableContainer>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>
                        <button type="button" className={sortButtonClass(termSortKey === "key")} onClick={() => onTermSort("key")}>
                          Key
                          <SortMarker active={termSortKey === "key"} direction={termSortDirection} />
                        </button>
                      </TableHead>
                      <TableHead>
                        <button type="button" className={sortButtonClass(termSortKey === "label")} onClick={() => onTermSort("label")}>
                          Label
                          <SortMarker active={termSortKey === "label"} direction={termSortDirection} />
                        </button>
                      </TableHead>
                      <TableHead>Description</TableHead>
                      <TableHead>Field Guide</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {sortedTerms.map((item) => (
                      <TableRow key={item.key}>
                        <TableCell className="font-data text-xs uppercase text-muted-foreground">{item.key}</TableCell>
                        <TableCell className="font-semibold">{item.label}</TableCell>
                        <TableCell className="text-muted-foreground">{item.description}</TableCell>
                        <TableCell className="text-xs text-muted-foreground min-w-[260px]">
                          <TermGuidance term={item.key} compact />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </CardContent>
        </Card>
      </section>
    </main>
  );
}
