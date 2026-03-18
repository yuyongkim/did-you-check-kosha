#!/usr/bin/env python3
"""Validate and optionally repair text mojibake in KOSHA JSON snapshots."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Tuple

from kosha_ingestion.sync_corpus import REPO_ROOT
from kosha_ingestion.text_encoding import maybe_fix_mojibake_text


DEFAULT_TARGETS = [
  REPO_ROOT / "datasets" / "kosha" / "normalized" / "guide_documents.json",
  REPO_ROOT / "datasets" / "kosha" / "normalized" / "law_articles.json",
  REPO_ROOT / "datasets" / "kosha_guide" / "guides.json",
  REPO_ROOT / "datasets" / "kosha_guide" / "normalized" / "guide_documents_text.json",
]


@dataclass
class FileStats:
  path: Path
  strings_total: int = 0
  strings_changed: int = 0
  rows: int = 0
  repaired: bool = False


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
  parser = argparse.ArgumentParser(description="Validate/fix KOSHA snapshot text encoding.")
  parser.add_argument(
    "--paths",
    nargs="*",
    default=[str(path) for path in DEFAULT_TARGETS],
    help="JSON file paths to scan.",
  )
  parser.add_argument("--repair", action="store_true", help="Write repaired JSON when fixes are found.")
  return parser.parse_args(argv)


def iter_paths(raw_paths: Iterable[str]) -> List[Path]:
  out: List[Path] = []
  for value in raw_paths:
    path = Path(value).resolve()
    if path.exists() and path.suffix.lower() == ".json":
      out.append(path)
  return out


def walk_and_fix(value: Any, stats: FileStats) -> Any:
  if isinstance(value, dict):
    return {k: walk_and_fix(v, stats) for k, v in value.items()}
  if isinstance(value, list):
    return [walk_and_fix(item, stats) for item in value]
  if isinstance(value, str):
    stats.strings_total += 1
    fixed = maybe_fix_mojibake_text(value)
    if fixed != value:
      stats.strings_changed += 1
    return fixed
  return value


def load_json(path: Path) -> Any:
  return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: Any) -> None:
  path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def process_file(path: Path, repair: bool) -> FileStats:
  stats = FileStats(path=path)
  data = load_json(path)
  if isinstance(data, list):
    stats.rows = len(data)
  elif isinstance(data, dict):
    stats.rows = len(data)

  fixed = walk_and_fix(data, stats)
  if repair and stats.strings_changed > 0:
    save_json(path, fixed)
    stats.repaired = True
  return stats


def main(argv: List[str] | None = None) -> int:
  args = parse_args(argv)
  paths = iter_paths(args.paths)
  if not paths:
    raise RuntimeError("No valid JSON paths provided.")

  all_stats: List[FileStats] = [process_file(path, repair=args.repair) for path in paths]

  total_strings = sum(item.strings_total for item in all_stats)
  total_changed = sum(item.strings_changed for item in all_stats)
  total_repaired = sum(1 for item in all_stats if item.repaired)

  for item in all_stats:
    status = "repaired" if item.repaired else "checked"
    print(
      f"[{status}] {item.path} rows={item.rows} "
      f"strings={item.strings_total} changed={item.strings_changed}"
    )

  print("[summary]")
  print(f"- files: {len(all_stats)}")
  print(f"- strings_scanned: {total_strings}")
  print(f"- strings_changed: {total_changed}")
  print(f"- files_repaired: {total_repaired}")

  return 0


if __name__ == "__main__":
  raise SystemExit(main())
