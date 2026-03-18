#!/usr/bin/env python3
"""
Append a completion record to:
1) docs/revisions/CHANGELOG.md
2) docs/revisions/DELIVERY_LOG.md

Usage example:
  python scripts/log_completion.py ^
    --version v0.44 ^
    --title "Frontend form hardening wave" ^
    --scope "Completed 100-point hardening batch with validation rerun." ^
    --file frontend/components/forms/discipline-form.tsx ^
    --file docs/revisions/CHANGELOG.md ^
    --verify "npm --prefix frontend run typecheck" ^
    --verify "npm --prefix frontend run lint" ^
    --verify "npm --prefix frontend run test:unit" ^
    --verify "npm --prefix frontend run build" ^
    --result PASS
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import List


ROOT = Path(__file__).resolve().parents[1]
CHANGELOG_PATH = ROOT / "docs" / "revisions" / "CHANGELOG.md"
DELIVERY_LOG_PATH = ROOT / "docs" / "revisions" / "DELIVERY_LOG.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write completion history entries to changelog and delivery log.")
    parser.add_argument("--version", required=True, help="Version tag (example: v0.44)")
    parser.add_argument("--title", required=True, help="Short change title for changelog.")
    parser.add_argument("--scope", required=True, help="Scope summary.")
    parser.add_argument("--file", action="append", default=[], help="Impacted file/module path. Repeat for multiple.")
    parser.add_argument("--item", action="append", default=[], help="Changelog bullet item. Repeat for multiple.")
    parser.add_argument("--verify", action="append", default=[], help="Verification command. Repeat for multiple.")
    parser.add_argument("--result", default="PASS", help="Result status (default: PASS).")
    parser.add_argument("--risk", action="append", default=[], help="Risk/follow-up note. Repeat for multiple.")
    parser.add_argument("--date", default=str(date.today()), help="Date in YYYY-MM-DD (default: today).")
    parser.add_argument("--dry-run", action="store_true", help="Print generated sections without writing files.")
    return parser.parse_args()


def ensure_exists(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Required file is missing: {path}")


def build_changelog_section(entry_date: str, version: str, title: str, scope: str, items: List[str]) -> str:
    lines = [f"## {entry_date} - {version} - {title}"]
    if items:
        lines.extend([f"- {item}" for item in items])
    else:
        lines.append(f"- {scope}")
    return "\n".join(lines) + "\n\n"


def build_delivery_section(
    entry_date: str,
    version: str,
    scope: str,
    files: List[str],
    verify: List[str],
    result: str,
    risks: List[str],
) -> str:
    lines: List[str] = []
    lines.append(f"## {entry_date} - {version}")
    lines.append(f"- Date: {entry_date}")
    lines.append(f"- Version/Tag: {version}")
    lines.append(f"- Scope: {scope}")
    lines.append("- Files/Modules:")
    if files:
        lines.extend([f"  - `{item}`" for item in files])
    else:
        lines.append("  - N/A")
    lines.append("- Verification Commands:")
    if verify:
        lines.extend([f"  - `{cmd}`" for cmd in verify])
    else:
        lines.append("  - N/A")
    lines.append("- Result:")
    lines.append(f"  - {result}")
    lines.append("- Risks/Follow-ups:")
    if risks:
        lines.extend([f"  - {note}" for note in risks])
    else:
        lines.append("  - None")
    lines.append("")
    return "\n".join(lines)


def prepend_changelog(path: Path, section: str) -> None:
    content = path.read_text(encoding="utf-8")
    marker = "\n## "
    marker_index = content.find(marker)
    if marker_index == -1:
        # fallback: append to end if no section marker exists
        new_content = content.rstrip() + "\n\n" + section
        path.write_text(new_content, encoding="utf-8")
        return

    insert_at = marker_index + 1  # keep first newline before first "##"
    new_content = content[:insert_at] + section + content[insert_at:]
    path.write_text(new_content, encoding="utf-8")


def append_delivery(path: Path, section: str) -> None:
    content = path.read_text(encoding="utf-8")
    new_content = content.rstrip() + "\n\n" + section
    path.write_text(new_content, encoding="utf-8")


def main() -> int:
    args = parse_args()

    ensure_exists(CHANGELOG_PATH)
    ensure_exists(DELIVERY_LOG_PATH)

    changelog_section = build_changelog_section(
        entry_date=args.date,
        version=args.version,
        title=args.title,
        scope=args.scope,
        items=args.item,
    )
    delivery_section = build_delivery_section(
        entry_date=args.date,
        version=args.version,
        scope=args.scope,
        files=args.file,
        verify=args.verify,
        result=args.result,
        risks=args.risk,
    )

    if args.dry_run:
        print("=== CHANGELOG SECTION ===")
        print(changelog_section)
        print("=== DELIVERY SECTION ===")
        print(delivery_section)
        return 0

    prepend_changelog(CHANGELOG_PATH, changelog_section)
    append_delivery(DELIVERY_LOG_PATH, delivery_section)
    print("Completion history written:")
    print(f"- {CHANGELOG_PATH}")
    print(f"- {DELIVERY_LOG_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
