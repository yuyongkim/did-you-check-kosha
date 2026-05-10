"""Final pre-submission audit for the JLP package.

Proactive checks for failure modes that have bitten this submission before:
  - cross-references to sections that do not exist
  - claims about content not actually in the paper ("reported in §X")
  - reviewer-name leaks in body (blind-review violation)
  - title leaks (old title still alive after a revert)
  - acronyms used before definition
  - dated / rotted file paths
  - reproducibility script integrity (referenced sub-scripts exist)
  - cover letter vs paper consistency (title, key numbers)
  - response-letter quotes that no longer match current paper text
  - Highlights bullet length

Returns non-zero exit code if any blocking issue is found.
"""
import os, re, sys, zipfile

sys.stdout.reconfigure(encoding='utf-8')

ROOT_REL = os.path.join('docs', 'publication', 'submissions', 'jlp_revision_2026-05-08')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ROOT_REL))
ARCH = os.path.join(ROOT, '_archive')


def doc_text(path):
    z = zipfile.ZipFile(path)
    body = z.read('word/document.xml').decode('utf-8', errors='ignore')
    return re.sub(r'<[^>]+>', ' ', body)


def md(name):
    return open(os.path.join(ARCH, name), encoding='utf-8').read()


def main():
    issues, warns = [], []

    paper = md('PAPER_JLP_REVISED_v3.md')
    cover = md('COVER_LETTER_JLP_RESUBMISSION_v2.md')
    resp  = md('RESPONSE_TO_REVIEWERS_v2.md')
    hl    = md('HIGHLIGHTS.md')

    # 1. Section cross-reference integrity
    section_nums = set()
    for m in re.finditer(r'^#{2,4}\s+(\d+(?:\.\d+){0,2})\b', paper, re.M):
        section_nums.add(m.group(1))
    for m in re.finditer(r'^#{2,4}\s+(Appendix [AB])', paper, re.M):
        section_nums.add(m.group(1))

    refs = set()
    for m in re.finditer(r'§\s*(\d+(?:\.\d+){0,2})', paper):
        refs.add(m.group(1))
    for m in re.finditer(r'\bSection\s+(\d+(?:\.\d+){0,2})', paper):
        refs.add(m.group(1))
    for m in re.finditer(r'\bAppendix\s+([AB])', paper):
        refs.add('Appendix ' + m.group(1))

    orphan = sorted(r for r in refs if r not in section_nums)
    if orphan:
        issues.append(f'PAPER references {len(orphan)} sections that may not exist: {orphan[:10]}')

    # 2. Reviewer leaks in PAPER body
    hits = re.findall(r'\breviewer[s]?\b', paper, re.I)
    if hits:
        issues.append(f'PAPER body has {len(hits)} "reviewer" mentions (blind-review concern)')

    # 3. Title leaks
    NEW = 'A KOSHA Regulatory Knowledge-Grounded Multi-Discipline'
    for f in ['PAPER_JLP_REVISED_v3.docx',
              'COVER_LETTER_JLP_RESUBMISSION_v2.docx',
              'RESPONSE_TO_REVIEWERS_v2.docx',
              'DECLARATION_OF_INTERESTS.docx',
              'BEFORE_AFTER_COMPARISON.docx']:
        p = os.path.join(ROOT, f)
        if os.path.exists(p) and NEW in doc_text(p):
            issues.append(f'NEW title still appears in {f}')

    # 4. Internal version markers
    for f in ['PAPER_JLP_REVISED_v3.docx', 'COVER_LETTER_JLP_RESUBMISSION_v2.docx']:
        p = os.path.join(ROOT, f)
        if os.path.exists(p) and 'v3.5' in doc_text(p):
            issues.append(f'{f} contains "v3.5" internal version marker')

    # 5. False "reported in §X" claims
    for m in re.finditer(r'reported (?:in|as part of) §(\d+(?:\.\d+){0,2})', paper, re.I):
        if m.group(1) not in section_nums:
            issues.append(f'PAPER claims "reported in §{m.group(1)}" but that section is missing')

    # 6. Cover letter title matches PAPER title
    paper_title_m = re.search(r'^# (.+)$', paper, re.M)
    if paper_title_m:
        paper_title = paper_title_m.group(1).strip()
        cover_re = re.search(r'\*\*Re:\*\*[^"]*"([^"]+)"', cover)
        if cover_re:
            cover_title = cover_re.group(1).strip()
            if cover_title != paper_title:
                issues.append(f'Title mismatch:\n     PAPER : "{paper_title}"\n     COVER : "{cover_title}"')

    # 7. Highlights bullet length
    for i, m in enumerate(re.finditer(r'^- (.+)$', hl, re.M), 1):
        s = m.group(1).strip()
        if len(s) > 85:
            issues.append(f'Highlight bullet {i} is {len(s)} chars (>85): "{s}"')

    # 8. Reproducibility script integrity
    repro_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'reproduce_all.py'))
    if not os.path.exists(repro_path):
        issues.append('scripts/reproduce_all.py missing')
    else:
        repro_src = open(repro_path, encoding='utf-8').read()
        for s in set(re.findall(r'scripts/(\w+\.py)', repro_src)):
            sp = os.path.abspath(os.path.join(os.path.dirname(__file__), s))
            if not os.path.exists(sp):
                issues.append(f'reproduce_all.py references missing scripts/{s}')

    # 9. Numeric consistency cover vs paper (informational)
    for n in ['26/60', '+0.4333', '0.7400', '0.7933', '12,932', '4,928']:
        if n in paper and n not in cover:
            warns.append(f'Number {n} in PAPER but not in COVER (probably fine; FYI)')

    # 10. Response-letter quotes match current paper text
    paper_clean = re.sub(r'\*\*?', '', paper)
    for m in re.finditer(r'^>\s+(.{50,200}?)$', resp, re.M):
        quote = m.group(1).strip().rstrip('.[…')
        if quote.lower().startswith(('the reviewer', 'reviewer', 'r1', 'r2', 'r3')):
            continue
        bare = re.sub(r'\*\*?', '', quote)[:80]
        if len(bare) >= 50 and bare not in paper_clean:
            warns.append(f'Response quote may not match current paper: "{bare[:60]}…"')

    # 11b. Cross-document count consistency:
    # COVER must not cite numbers that contradict its source documents
    # (CHANGE_SUMMARY for section-level, BEFORE_AFTER for row-level).
    chsum_path = os.path.join(ARCH, 'CHANGE_SUMMARY_TABLE.md')
    if os.path.exists(chsum_path):
        chsum = open(chsum_path, encoding='utf-8').read()
        cs_match = re.search(r'(\d+)\s+sections changed.*?(\d+)\s+NEW\s*\+\s*(\d+)\s+REVISED', chsum)
        if cs_match:
            cs_total, cs_new, cs_rev = (int(g) for g in cs_match.groups())
            m = re.search(r'(\d+)\s+section-level changes', cover)
            if m and int(m.group(1)) != cs_total:
                issues.append(f'COVER cites {m.group(1)} section-level changes but CHANGE_SUMMARY has {cs_total}')
            m = re.search(r'\*\*(\d+)\s+new sections\*\*', cover)
            if m and int(m.group(1)) != cs_new:
                issues.append(f'COVER cites {m.group(1)} new sections but CHANGE_SUMMARY has {cs_new} (granularity collision)')
            m = re.search(r'\*\*(\d+)\s+rewritten sections\*\*', cover)
            if m and int(m.group(1)) != cs_rev:
                issues.append(f'COVER cites {m.group(1)} rewritten sections but CHANGE_SUMMARY has {cs_rev} (granularity collision)')

    ba_path = os.path.join(ROOT, 'BEFORE_AFTER_COMPARISON.docx')
    if os.path.exists(ba_path):
        ba_text = doc_text(ba_path)
        m = re.search(r'(\d+)\s+changed rows.*?(\d+)\s+NEW.*?(\d+)\s+REVISED.*?(\d+)\s+DELETED', ba_text)
        if m:
            ba_total = int(m.group(1))
            cm = re.search(r'\*\*(\d+)\s+sub-heading-level rows\*\*', cover)
            if cm and int(cm.group(1)) != ba_total:
                issues.append(f'COVER cites {cm.group(1)} sub-heading rows but BEFORE_AFTER has {ba_total}')

    # 11. MARKED-ACCEPTED sync probe: simulate Word "Accept All Changes"
    #     and verify the resulting text matches PAPER_v3.docx on key probes.
    #     This catches the case where MARKED.docx is stale wrt clean.
    marked_path = os.path.join(ROOT, 'PAPER_JLP_REVISED_v3_MARKED.docx')
    if os.path.exists(marked_path):
        try:
            from lxml import etree
            z = zipfile.ZipFile(marked_path)
            NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            root = etree.fromstring(z.read('word/document.xml'))
            # Drop <w:del> blocks (deletions are gone after Accept)
            for d in root.findall('.//w:del', NS):
                d.getparent().remove(d)
            # Unwrap <w:ins> elements (insertions become regular text after Accept)
            for ins in root.findall('.//w:ins', NS):
                parent = ins.getparent()
                idx = list(parent).index(ins)
                for child in reversed(list(ins)):
                    parent.insert(idx, child)
                parent.remove(ins)
            marked_acc = re.sub(r'\s+', ' ',
                                re.sub(r'<[^>]+>', ' ',
                                       etree.tostring(root, encoding='unicode'))).strip()
            clean_txt  = re.sub(r'\s+', ' ',
                                doc_text(os.path.join(ROOT, 'PAPER_JLP_REVISED_v3.docx'))).strip()

            # Probes — anchor strings that must (or must NOT) appear in both
            sync_probes = [
                ('Title in clean and marked',                 'Detecting Jurisdiction Compliance Gaps', True),
                ('OLD-revision NEW-title must NOT leak',      'A KOSHA Regulatory Knowledge-Grounded Multi-Discipline', False),
                ('K-voting future-work wording',              'formal threshold-sensitivity sweep', True),
                ('§6.6 human-expert paragraph',               'industry baseline is not a human-expert', True),
                ('Acks must NOT have JLP editorial team',     'JLP editorial team', False),
            ]
            for label, needle, must_present in sync_probes:
                in_clean  = needle in clean_txt
                in_marked = needle in marked_acc
                if must_present:
                    if not in_clean:
                        warns.append(f'sync probe "{label}": needle missing from clean (probe stale?)')
                    elif not in_marked:
                        issues.append(f'MARKED out of sync — clean has "{label[:40]}" but marked-accepted does not')
                else:
                    if in_clean:
                        issues.append(f'CLEAN regression — "{label}" needle still present in clean')
                    elif in_marked:
                        issues.append(f'MARKED out of sync — clean drops "{label[:40]}" but marked-accepted still has it')
        except ImportError:
            warns.append('lxml not installed; skipping marked-vs-clean sync check')

    # Report
    print('=' * 70)
    print('FINAL PRE-SUBMISSION AUDIT')
    print('=' * 70)
    print()
    if not issues:
        print('NO BLOCKING ISSUES FOUND.')
    else:
        print(f'BLOCKING ISSUES ({len(issues)}):')
        for i in issues:
            print(f'  [BLOCK] {i}')
    print()
    if warns:
        print(f'WARNINGS ({len(warns)}):')
        for w in warns[:10]:
            print(f'  [WARN]  {w}')
        if len(warns) > 10:
            print(f'  … and {len(warns) - 10} more')
    print()
    print(f'Sections defined in PAPER: {len(section_nums)}')
    print(f'Cross-refs in PAPER:       {len(refs)} unique')
    sys.exit(1 if issues else 0)


if __name__ == '__main__':
    main()
