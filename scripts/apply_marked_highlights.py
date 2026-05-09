"""Regenerate PAPER_JLP_REVISED_v3_MARKED.docx with yellow/green highlights.

Pipeline:
1. Read the marked markdown source (`_archive/PAPER_JLP_REVISED_v3_MARKED.md`).
2. Build an ordered list of headings with their marker state ([NEW] / [REVISED] / unmarked-inherits).
3. Strip the `[NEW]`/`[REVISED]` heading prefixes and the
   `> **[NEW SECTION]**` / `> **[REVISED SECTION]**` blockquote markers (plus the
   `>` continuation line that immediately follows them) into a temporary clean .md.
4. Convert the clean .md to .docx via pandoc, with the resource path set to the
   `_archive/` directory so figures resolve.
5. Walk the resulting docx with python-docx; for each Heading paragraph, look up
   the corresponding marker state and apply highlight color (YELLOW for [NEW],
   BRIGHT_GREEN for [REVISED]); apply the same color to all subsequent body
   paragraphs and tables until the next heading.

Run from project root (the working directory is irrelevant — all paths absolute).
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from docx import Document
from docx.enum.text import WD_COLOR_INDEX

ROOT = Path(r"C:\Users\USER\Desktop\EPC engineering")
SUBMISSION_DIR = ROOT / "docs/publication/submissions/jlp_revision_2026-05-08"
ARCHIVE_DIR = SUBMISSION_DIR / "_archive"
SRC_MD = ARCHIVE_DIR / "PAPER_JLP_REVISED_v3_MARKED.md"
OUT_DOCX = SUBMISSION_DIR / "PAPER_JLP_REVISED_v3_MARKED.docx"

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
MARKER_PREFIX_RE = re.compile(r"^\[(NEW|REVISED)\]\s+")
SECTION_MARKER_LINE_RE = re.compile(
    r"^>\s*\*\*\[(NEW|REVISED) SECTION\]\*\*"
)
EMPTY_BLOCKQUOTE_RE = re.compile(r"^>\s*$")


def parse_markers(md_text: str):
    """Return list of (heading_level, clean_heading_text, marker) and clean md.

    marker is "NEW", "REVISED", or None (inherits from parent / unchanged).
    Resolution rule: a heading without an explicit marker INHERITS from the
    closest ancestor heading (lower level number) that has a marker. A top-level
    heading (h1/h2) with no marker is treated as unchanged (None).
    """
    headings: list[tuple[int, str, str | None]] = []  # resolved markers
    out_lines: list[str] = []
    src_lines = md_text.splitlines()
    i = 0
    # ancestor-stack of (level, resolved_marker)
    stack: list[tuple[int, str | None]] = []
    while i < len(src_lines):
        line = src_lines[i]
        m = HEADING_RE.match(line)
        if m:
            hashes, text = m.group(1), m.group(2).rstrip()
            level = len(hashes)
            mm = MARKER_PREFIX_RE.match(text)
            explicit_marker: str | None = None
            if mm:
                explicit_marker = mm.group(1)
                clean_text = text[mm.end():].rstrip()
            else:
                clean_text = text
            # Pop ancestors at >= current level
            while stack and stack[-1][0] >= level:
                stack.pop()
            inherited = stack[-1][1] if stack else None
            resolved = explicit_marker if explicit_marker else inherited
            stack.append((level, resolved))
            headings.append((level, clean_text, resolved))
            out_lines.append(f"{hashes} {clean_text}")
            i += 1
            # If next line is the blockquote section marker, drop it AND the
            # immediately-following empty `>` continuation line so the next
            # paragraph is plain text (not a blockquote).
            if i < len(src_lines) and SECTION_MARKER_LINE_RE.match(src_lines[i]):
                i += 1  # skip marker line
                if i < len(src_lines) and EMPTY_BLOCKQUOTE_RE.match(src_lines[i]):
                    i += 1  # skip the trailing `>` continuation
            continue
        out_lines.append(line)
        i += 1
    return headings, "\n".join(out_lines) + "\n"


def normalise_heading(text: str) -> str:
    """Normalise a heading for matching markdown -> docx (whitespace-only)."""
    return re.sub(r"\s+", " ", text).strip()


def apply_highlight_to_paragraph(para, color: WD_COLOR_INDEX) -> bool:
    """Apply highlight to every run in the paragraph. Returns True if any run."""
    if not para.runs:
        return False
    applied = False
    for run in para.runs:
        run.font.highlight_color = color
        applied = True
    return applied


def apply_highlight_to_table(table, color: WD_COLOR_INDEX) -> int:
    """Apply highlight to every run inside every cell. Returns # paragraphs touched."""
    n = 0
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                if apply_highlight_to_paragraph(para, color):
                    n += 1
    return n


def is_heading(para) -> bool:
    return para.style is not None and para.style.name.startswith("Heading")


def main() -> int:
    if not SRC_MD.exists():
        print(f"ERROR: source markdown not found: {SRC_MD}", file=sys.stderr)
        return 1
    print(f"[1/5] Reading {SRC_MD}")
    md = SRC_MD.read_text(encoding="utf-8")

    print("[2/5] Parsing markers and building clean markdown")
    headings, clean_md = parse_markers(md)
    new_count = sum(1 for _, _, m in headings if m == "NEW")
    rev_count = sum(1 for _, _, m in headings if m == "REVISED")
    none_count = sum(1 for _, _, m in headings if m is None)
    print(f"        headings: total={len(headings)} NEW={new_count} REVISED={rev_count} unmarked={none_count}")

    # Build heading->marker lookup (by normalised text). Heading text should be
    # unique within the document; if it isn't, fall back to ordered consumption.
    heading_queue = list(headings)  # consumed in order; safer than dict lookup

    with tempfile.TemporaryDirectory() as td:
        tmp_md = Path(td) / "clean.md"
        tmp_md.write_text(clean_md, encoding="utf-8")
        print(f"[3/5] Running pandoc → {OUT_DOCX}")
        # `--resource-path` so figures resolve from the archive directory.
        cmd = [
            "pandoc",
            str(tmp_md),
            "-o", str(OUT_DOCX),
            f"--resource-path={ARCHIVE_DIR}",
            "--from=gfm+pipe_tables",
            "--to=docx",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print("pandoc stderr:\n" + r.stderr, file=sys.stderr)
            return r.returncode

    print(f"[4/5] Walking docx and applying highlights")
    doc = Document(str(OUT_DOCX))

    body = doc.element.body
    # We iterate over the body's child block elements in order so paragraphs
    # and tables are visited in document order.
    from docx.oxml.ns import qn
    from docx.text.paragraph import Paragraph
    from docx.table import Table

    current_color: WD_COLOR_INDEX | None = None
    yellow_paras = 0
    green_paras = 0
    none_paras = 0
    skipped_headings: list[str] = []
    matched_headings: list[tuple[str, str | None]] = []

    # Build a mutable iterator over expected headings for ordered consumption
    expected_iter = iter(heading_queue)
    next_expected = next(expected_iter, None)

    for child in body.iterchildren():
        tag = child.tag
        if tag == qn("w:p"):
            para = Paragraph(child, doc)
            if is_heading(para):
                # Match against next expected heading by normalised text.
                ptext = normalise_heading(para.text)
                if next_expected is not None:
                    _, exp_text, exp_marker = next_expected
                    if normalise_heading(exp_text) == ptext:
                        if exp_marker == "NEW":
                            current_color = WD_COLOR_INDEX.YELLOW
                        elif exp_marker == "REVISED":
                            current_color = WD_COLOR_INDEX.BRIGHT_GREEN
                        else:
                            current_color = None
                        matched_headings.append((ptext, exp_marker))
                        next_expected = next(expected_iter, None)
                    else:
                        # Out-of-order; try to skip ahead to find a match.
                        # Look ahead a few entries.
                        found = False
                        lookahead: list = []
                        while next_expected is not None:
                            _, exp_text, exp_marker = next_expected
                            if normalise_heading(exp_text) == ptext:
                                found = True
                                if exp_marker == "NEW":
                                    current_color = WD_COLOR_INDEX.YELLOW
                                elif exp_marker == "REVISED":
                                    current_color = WD_COLOR_INDEX.BRIGHT_GREEN
                                else:
                                    current_color = None
                                matched_headings.append((ptext, exp_marker))
                                next_expected = next(expected_iter, None)
                                break
                            lookahead.append(next_expected)
                            next_expected = next(expected_iter, None)
                        if not found:
                            # Restore the queue (we exhausted it without match).
                            # Treat as unknown — keep current_color (inherit).
                            skipped_headings.append(ptext)
                            # Re-prepend the lookahead for next attempts.
                            expected_iter = iter(lookahead + ([next_expected] if next_expected else []))
                            next_expected = next(expected_iter, None)
                else:
                    skipped_headings.append(ptext)

                # Apply color to the heading paragraph itself.
                if current_color is not None:
                    apply_highlight_to_paragraph(para, current_color)
                    if current_color == WD_COLOR_INDEX.YELLOW:
                        yellow_paras += 1
                    else:
                        green_paras += 1
                else:
                    none_paras += 1
            else:
                # Body paragraph
                if current_color is not None and para.runs:
                    apply_highlight_to_paragraph(para, current_color)
                    if current_color == WD_COLOR_INDEX.YELLOW:
                        yellow_paras += 1
                    else:
                        green_paras += 1
                else:
                    none_paras += 1
        elif tag == qn("w:tbl"):
            table = Table(child, doc)
            if current_color is not None:
                n = apply_highlight_to_table(table, current_color)
                if current_color == WD_COLOR_INDEX.YELLOW:
                    yellow_paras += n
                else:
                    green_paras += n
            # else: unhighlighted table

    doc.save(str(OUT_DOCX))

    print(f"[5/5] Verification")
    size = OUT_DOCX.stat().st_size
    with zipfile.ZipFile(OUT_DOCX) as z:
        media = [n for n in z.namelist() if n.startswith("word/media/")]
    print(f"        file size: {size:,} bytes")
    print(f"        embedded media files: {len(media)} -> {media}")
    print(f"        paragraphs highlighted YELLOW : {yellow_paras}")
    print(f"        paragraphs highlighted GREEN  : {green_paras}")
    print(f"        paragraphs unhighlighted      : {none_paras}")
    print(f"        headings matched: {len(matched_headings)} / {len(heading_queue)}")
    if skipped_headings:
        print("        UNMATCHED docx headings (no marker assigned):")
        for h in skipped_headings:
            print(f"          - {h}")
    leftover = [h for h in [next_expected] if h is not None] + list(expected_iter)
    if leftover:
        print("        UNMATCHED markdown headings (never found in docx):")
        for lvl, txt, mk in leftover:
            print(f"          - h{lvl} [{mk}] {txt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
