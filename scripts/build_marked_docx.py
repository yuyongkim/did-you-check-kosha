"""Build PAPER_JLP_REVISED_v3_MARKED.docx via python-docx text diff.

Approach:
  - Read original .docx paragraphs (text)
  - Walk revised .docx paragraphs (preserves figures, tables, headings, styles)
  - For each revised paragraph, find best original match by SequenceMatcher ratio
  - Matched (>= 0.40): clear runs and replace with word-level diff runs
      insertion = green underline, deletion = red strikethrough
  - Unmatched: whole paragraph green underline
  - Append "Deleted from original" block at end with strikethrough of all
    original paragraphs that were never matched
"""
import os, sys, difflib, time
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document
from docx.shared import RGBColor

ROOT = os.path.join(os.path.dirname(__file__), '..',
                    'docs', 'publication', 'submissions')
ROOT = os.path.abspath(ROOT)

ORIG_DOCX = os.path.join(ROOT, 'jlp_initial_2026-03-31',  'MANUSCRIPT (1).docx')
REV_DOCX  = os.path.join(ROOT, 'jlp_revision_2026-05-08', 'PAPER_JLP_REVISED_v3.docx')
OUT_DOCX  = os.path.join(ROOT, 'jlp_revision_2026-05-08', 'PAPER_JLP_REVISED_v3_MARKED.docx')

INS = (0, 112, 0)   # green
DEL = (192, 0, 0)   # red

def best_match(text, candidates, used, threshold=0.40):
    if len(text) < 20:
        return -1, 0.0
    best_idx, best_ratio = -1, 0.0
    for i, c in enumerate(candidates):
        if i in used or not c:
            continue
        if abs(len(c) - len(text)) > max(len(text), len(c)) * 1.5:
            continue
        r = difflib.SequenceMatcher(None, text.lower(), c.lower()).quick_ratio()
        if r > best_ratio:
            best_idx, best_ratio = i, r
    if best_ratio < threshold or best_idx == -1:
        return -1, best_ratio
    real = difflib.SequenceMatcher(None,
                                   candidates[best_idx].lower(),
                                   text.lower()).ratio()
    return (best_idx, real) if real >= threshold else (-1, real)

def clear_runs(para):
    p = para._element
    for child in list(p):
        if child.tag.endswith('}pPr'):
            continue
        p.remove(child)

def add_run(para, text, *, color=None, strike=False, underline=False, bold=False):
    if not text:
        return
    run = para.add_run(text)
    if color:
        run.font.color.rgb = RGBColor(*color)
    if strike:
        run.font.strike = True
    if underline:
        run.font.underline = True
    if bold:
        run.font.bold = True

def diff_into_para(para, orig_text, new_text):
    a = orig_text.split()
    b = new_text.split()
    sm = difflib.SequenceMatcher(None, a, b)
    clear_runs(para)
    parts = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            parts.append(('eq', ' '.join(b[j1:j2])))
        elif op == 'insert':
            parts.append(('ins', ' '.join(b[j1:j2])))
        elif op == 'delete':
            parts.append(('del', ' '.join(a[i1:i2])))
        elif op == 'replace':
            parts.append(('del', ' '.join(a[i1:i2])))
            parts.append(('ins', ' '.join(b[j1:j2])))
    for k, (kind, txt) in enumerate(parts):
        prefix = '' if k == 0 else ' '
        if kind == 'eq':
            add_run(para, prefix + txt)
        elif kind == 'ins':
            add_run(para, prefix + txt, color=INS, underline=True)
        elif kind == 'del':
            add_run(para, prefix + txt, color=DEL, strike=True)

def main():
    t0 = time.time()
    orig_doc = Document(ORIG_DOCX)
    orig_paras = [p.text.strip() for p in orig_doc.paragraphs if p.text.strip()]
    for t in orig_doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if p.text.strip():
                        orig_paras.append(p.text.strip())
    print(f'Original: {len(orig_paras)} non-empty paragraphs (incl. table cells)')

    rev_doc = Document(REV_DOCX)
    rev_count = sum(1 for p in rev_doc.paragraphs if p.text.strip())
    print(f'Revised:  {rev_count} non-empty body paragraphs (excl. tables)')

    used = set()
    n_eq = n_partial = n_new = 0
    for para in rev_doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        style_name = (para.style.name or '').lower() if para.style else ''
        if 'heading' in style_name or 'title' in style_name:
            continue
        idx, ratio = best_match(text, orig_paras, used)
        if idx >= 0 and ratio >= 0.95:
            used.add(idx)
            n_eq += 1
            continue
        if idx >= 0:
            used.add(idx)
            diff_into_para(para, orig_paras[idx], text)
            n_partial += 1
        else:
            clear_runs(para)
            add_run(para, text, color=INS, underline=True)
            n_new += 1

    deleted = [(i, p) for i, p in enumerate(orig_paras) if i not in used]
    if deleted:
        rev_doc.add_page_break()
        h = rev_doc.add_paragraph()
        add_run(h, 'Deleted content from original manuscript', bold=True, color=DEL)
        for _, p in deleted:
            para = rev_doc.add_paragraph()
            add_run(para, p, color=DEL, strike=True)

    if os.path.exists(OUT_DOCX):
        os.remove(OUT_DOCX)
    rev_doc.save(OUT_DOCX)
    size = os.path.getsize(OUT_DOCX)
    print(f'\n  Saved: {size:,} B in {time.time() - t0:.1f}s')
    print(f'  Paragraphs: equal={n_eq}  partial-diff={n_partial}  fully-new={n_new}')
    print(f'  Original paragraphs marked deleted: {len(deleted)} of {len(orig_paras)}')

    import zipfile
    z = zipfile.ZipFile(OUT_DOCX)
    media = [n for n in z.namelist() if 'media' in n and n.endswith('.png')]
    body = z.read('word/document.xml').decode('utf-8', errors='ignore')
    print(f'  PNGs preserved:    {len(media)}')
    print(f'  Strikethrough runs: {body.count("<w:strike")}')
    print(f'  Color runs:         {body.count("<w:color")}')
    print(f'  Underline runs:     {body.count("<w:u ")}')

if __name__ == '__main__':
    main()
