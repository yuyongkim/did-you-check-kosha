import fs from "node:fs";
import path from "node:path";

import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

function resolveRepoRoot(): string {
  const cwd = process.cwd();
  const parent = path.resolve(cwd, "..");
  const cwdCandidate = path.resolve(cwd, "datasets", "kosha_guide", "files");
  const parentCandidate = path.resolve(parent, "datasets", "kosha_guide", "files");
  if (fs.existsSync(cwdCandidate)) return cwd;
  if (fs.existsSync(parentCandidate)) return parent;
  return cwd;
}

function isSafeGuideNo(guideNo: string): boolean {
  return /^[A-Za-z0-9-]{3,40}$/.test(guideNo);
}

function findGuideFile(filesDir: string, guideNo: string): string | null {
  if (!fs.existsSync(filesDir)) return null;
  const prefix = `${guideNo.toLowerCase()}__`;
  const files = fs.readdirSync(filesDir, { withFileTypes: true });
  const target = files.find((entry) => {
    if (!entry.isFile()) return false;
    const lower = entry.name.toLowerCase();
    return lower.endsWith(".pdf") && lower.startsWith(prefix);
  });
  if (!target) return null;
  return path.resolve(filesDir, target.name);
}

export async function GET(
  _request: Request,
  context: { params: { guideNo: string } },
) {
  const guideNoRaw = String(context.params.guideNo ?? "");
  const guideNo = decodeURIComponent(guideNoRaw).trim().toUpperCase();
  if (!isSafeGuideNo(guideNo)) {
    return NextResponse.json({ error: "Invalid guide number." }, { status: 400 });
  }

  const repoRoot = resolveRepoRoot();
  const filesDir = path.resolve(repoRoot, "datasets", "kosha_guide", "files");
  const guideFile = findGuideFile(filesDir, guideNo);
  if (!guideFile || !fs.existsSync(guideFile)) {
    return NextResponse.json(
      { error: `Guide PDF not found for ${guideNo}.` },
      { status: 404 },
    );
  }

  const stat = fs.statSync(guideFile);
  const data = fs.readFileSync(guideFile);

  return new NextResponse(data, {
    headers: {
      "Content-Type": "application/pdf",
      "Content-Length": String(stat.size),
      "Content-Disposition": `inline; filename="${guideNo}.pdf"`,
      "Cache-Control": "public, max-age=300",
    },
  });
}
