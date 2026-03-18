#!/usr/bin/env python3
"""Parse KOSHA Guide PDFs into normalized text datasets."""

from __future__ import annotations

import argparse
import bisect
import gzip
import json
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[4]


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
  parser = argparse.ArgumentParser(description="Parse KOSHA Guide PDFs into page/doc/chunk text datasets.")
  parser.add_argument(
    "--files-dir",
    default=str(REPO_ROOT / "datasets" / "kosha_guide" / "files"),
    help="Directory containing guide PDF files.",
  )
  parser.add_argument(
    "--guides-json",
    default=str(REPO_ROOT / "datasets" / "kosha_guide" / "guides.json"),
    help="Guide metadata json path.",
  )
  parser.add_argument(
    "--out-dir",
    default=str(REPO_ROOT / "datasets" / "kosha_guide" / "normalized"),
    help="Output directory for parsed text datasets.",
  )
  parser.add_argument("--max-files", type=int, default=0, help="Optional max number of files to parse (0 = all).")
  parser.add_argument("--chunk-size", type=int, default=1200, help="Chunk size for retrieval records.")
  parser.add_argument("--chunk-overlap", type=int, default=200, help="Chunk overlap for retrieval records.")
  parser.add_argument("--progress-every", type=int, default=50, help="Progress print interval.")
  return parser.parse_args(argv)


def normalize_text(value: Any) -> str:
  text = str(value or "")
  text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\u00a0", " ")
  text = "\n".join(line.rstrip() for line in text.split("\n"))
  text = re.sub(r"[ \t]+", " ", text)
  text = re.sub(r"\n{3,}", "\n\n", text)
  return text.strip()


def write_json(path: Path, payload: Any) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_jsonl_gz(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  with gzip.open(path, mode="wt", encoding="utf-8") as stream:
    for row in rows:
      stream.write(json.dumps(row, ensure_ascii=False))
      stream.write("\n")


def load_guide_map(path: Path) -> Dict[str, Dict[str, Any]]:
  rows = json.loads(path.read_text(encoding="utf-8"))
  mapping: Dict[str, Dict[str, Any]] = {}
  if isinstance(rows, list):
    for row in rows:
      if not isinstance(row, dict):
        continue
      key = str(row.get("techGdlnNo") or "").strip()
      if key:
        mapping[key] = row
  return mapping


def extract_guide_no_from_filename(path: Path) -> str:
  # Expected filename: "<techGdlnNo>__<title>.pdf"
  stem = path.stem
  if "__" in stem:
    return stem.split("__", 1)[0].strip()
  return ""


def extract_pages_text(path: Path) -> Tuple[List[str], str]:
  # Primary: PyMuPDF (fitz). Fallback: PyPDF2.
  try:
    import fitz  # type: ignore

    pages: List[str] = []
    with fitz.open(path) as doc:
      for page in doc:
        pages.append(normalize_text(page.get_text("text")))
    return pages, "fitz"
  except Exception:
    pass

  try:
    from PyPDF2 import PdfReader  # type: ignore

    reader = PdfReader(str(path))
    pages = [normalize_text(page.extract_text() or "") for page in reader.pages]
    return pages, "pypdf2"
  except Exception as exc:
    raise RuntimeError(f"pdf_parse_failed: {exc}") from exc


def iter_pdf_files(files_dir: Path, max_files: int) -> List[Path]:
  files = sorted(path for path in files_dir.glob("*.pdf") if path.is_file())
  if max_files > 0:
    return files[:max_files]
  return files


def chunk_text(text: str, size: int, overlap: int) -> List[Tuple[int, int, str]]:
  if not text:
    return []
  if size <= 0:
    raise ValueError("chunk size must be > 0")
  if overlap < 0:
    raise ValueError("chunk overlap must be >= 0")
  step = max(1, size - overlap)

  chunks: List[Tuple[int, int, str]] = []
  start = 0
  total = len(text)
  while start < total:
    end = min(total, start + size)
    body = text[start:end].strip()
    if body:
      chunks.append((start, end, body))
    if end >= total:
      break
    start += step
  return chunks


def page_for_offset(offsets: List[int], offset: int) -> int:
  # offsets: cumulative end offsets by page (len == page_count)
  return bisect.bisect_left(offsets, max(0, offset)) + 1


@dataclass
class ParseResult:
  file: str
  guide_no: str
  title: str
  parser_engine: str
  page_count: int
  char_count: int
  status: str
  message: str


def main(argv: List[str] | None = None) -> int:
  args = parse_args(argv)
  started = time.perf_counter()

  files_dir = Path(args.files_dir).resolve()
  guides_json = Path(args.guides_json).resolve()
  out_dir = Path(args.out_dir).resolve()
  out_dir.mkdir(parents=True, exist_ok=True)

  if not files_dir.exists():
    raise RuntimeError(f"files dir not found: {files_dir}")
  if not guides_json.exists():
    raise RuntimeError(f"guides json not found: {guides_json}")

  guide_map = load_guide_map(guides_json)
  pdf_files = iter_pdf_files(files_dir=files_dir, max_files=args.max_files)

  page_rows: List[Dict[str, Any]] = []
  doc_rows: List[Dict[str, Any]] = []
  chunk_rows: List[Dict[str, Any]] = []
  parse_log: List[Dict[str, Any]] = []

  parsed_ok = 0
  parsed_error = 0
  missing_meta = 0
  total_pages = 0
  total_chars = 0

  for index, pdf_path in enumerate(pdf_files, start=1):
    guide_no = extract_guide_no_from_filename(pdf_path)
    meta = guide_map.get(guide_no, {})
    title = normalize_text(meta.get("techGdlnNm")) or pdf_path.stem
    ofanc = normalize_text(meta.get("techGdlnOfancYmd"))

    if not meta:
      missing_meta += 1

    try:
      pages, parser_engine = extract_pages_text(pdf_path)
      page_count = len(pages)
      nonempty_pages = [page for page in pages if page]
      doc_text = normalize_text("\n\n".join(nonempty_pages))
      char_count = len(doc_text)

      cumulative_offsets: List[int] = []
      acc = 0
      for page in pages:
        acc += len(page)
        cumulative_offsets.append(acc)

      for page_no, page_text in enumerate(pages, start=1):
        page_rows.append(
          {
            "guide_no": guide_no or None,
            "title": title,
            "ofanc_ymd": ofanc or None,
            "source_file": str(pdf_path),
            "page_no": page_no,
            "char_count": len(page_text),
            "text": page_text,
          }
        )

      chunks = chunk_text(doc_text, size=args.chunk_size, overlap=args.chunk_overlap)
      for chunk_idx, (start_pos, end_pos, body) in enumerate(chunks, start=1):
        start_page = page_for_offset(cumulative_offsets, start_pos) if cumulative_offsets else 1
        end_page = page_for_offset(cumulative_offsets, max(0, end_pos - 1)) if cumulative_offsets else 1
        chunk_rows.append(
          {
            "chunk_id": f"{guide_no or pdf_path.stem}#{chunk_idx}",
            "guide_no": guide_no or None,
            "title": title,
            "ofanc_ymd": ofanc or None,
            "source_file": str(pdf_path),
            "chunk_index": chunk_idx,
            "page_start": start_page,
            "page_end": end_page,
            "char_start": start_pos,
            "char_end": end_pos,
            "text": body,
          }
        )

      doc_rows.append(
        {
          "guide_no": guide_no or None,
          "title": title,
          "ofanc_ymd": ofanc or None,
          "source_file": str(pdf_path),
          "parser_engine": parser_engine,
          "page_count": page_count,
          "char_count": char_count,
          "text": doc_text,
        }
      )

      parsed_ok += 1
      total_pages += page_count
      total_chars += char_count
      parse_log.append(
        ParseResult(
          file=str(pdf_path),
          guide_no=guide_no,
          title=title,
          parser_engine=parser_engine,
          page_count=page_count,
          char_count=char_count,
          status="ok",
          message="",
        ).__dict__
      )
    except Exception as exc:  # noqa: BLE001
      parsed_error += 1
      parse_log.append(
        ParseResult(
          file=str(pdf_path),
          guide_no=guide_no,
          title=title,
          parser_engine="",
          page_count=0,
          char_count=0,
          status="error",
          message=str(exc),
        ).__dict__
      )

    if args.progress_every > 0 and index % args.progress_every == 0:
      print(
        f"[PROGRESS] files={index}/{len(pdf_files)} ok={parsed_ok} error={parsed_error} "
        f"pages={total_pages} chunks={len(chunk_rows)}"
      )

  page_path = out_dir / "guide_pages.jsonl.gz"
  docs_path = out_dir / "guide_documents_text.json"
  chunks_path = out_dir / "guide_chunks.jsonl.gz"
  log_path = out_dir / "parse_log.json"
  manifest_path = out_dir / "manifest_text.json"

  write_jsonl_gz(page_path, page_rows)
  write_json(docs_path, doc_rows)
  write_jsonl_gz(chunks_path, chunk_rows)
  write_json(log_path, parse_log)

  duration = round(time.perf_counter() - started, 3)
  manifest = {
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "duration_sec": duration,
    "inputs": {
      "files_dir": str(files_dir),
      "guides_json": str(guides_json),
      "max_files": args.max_files,
      "chunk_size": args.chunk_size,
      "chunk_overlap": args.chunk_overlap,
    },
    "totals": {
      "pdf_files_seen": len(pdf_files),
      "parsed_ok": parsed_ok,
      "parsed_error": parsed_error,
      "missing_meta": missing_meta,
      "page_rows": len(page_rows),
      "doc_rows": len(doc_rows),
      "chunk_rows": len(chunk_rows),
      "total_pages": total_pages,
      "total_chars": total_chars,
    },
    "outputs": {
      "guide_pages": str(page_path),
      "guide_documents_text": str(docs_path),
      "guide_chunks": str(chunks_path),
      "parse_log": str(log_path),
    },
  }
  write_json(manifest_path, manifest)

  print("[DONE] KOSHA guide PDF parsing finished")
  print(f"- pdf_files_seen: {len(pdf_files)}")
  print(f"- parsed_ok: {parsed_ok}")
  print(f"- parsed_error: {parsed_error}")
  print(f"- page_rows: {len(page_rows)}")
  print(f"- doc_rows: {len(doc_rows)}")
  print(f"- chunk_rows: {len(chunk_rows)}")
  print(f"- manifest: {manifest_path}")
  return 0


if __name__ == "__main__":
  try:
    raise SystemExit(main())
  except Exception as exc:  # noqa: BLE001
    print(f"[FAIL] {exc}", file=sys.stderr)
    raise SystemExit(1)
