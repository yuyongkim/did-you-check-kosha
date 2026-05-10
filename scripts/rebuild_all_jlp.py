"""One-shot rebuild of every artifact in the JLP revision submission folder.

Run this script after editing any of the source markdown files in
docs/publication/submissions/jlp_revision_2026-05-08/_archive/ — it
regenerates every downstream docx so they cannot drift apart.

Order:
  1. Pandoc: clean docx files from md sources (PAPER, COVER, RESPONSE,
     RESPONSE_KO, DOI, HIGHLIGHTS)
  2. build_marked_docx.py: native track-changes MARKED.docx from the
     fresh PAPER_v3.docx vs initial MANUSCRIPT (1).docx
  3. build_before_after_table.py: landscape side-by-side comparison
     against the fresh PAPER_v3.docx
  4. build_change_table.py: per-section change summary
  5. audit_submission.py: 10+1 pre-submission checks
"""
import os, sys, subprocess

sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ROOT = os.path.join(REPO, 'docs', 'publication', 'submissions', 'jlp_revision_2026-05-08')
ARCH = os.path.join(ROOT, '_archive')

PANDOC_PAIRS = [
    ('PAPER_JLP_REVISED_v3.md',           'PAPER_JLP_REVISED_v3.docx'),
    ('COVER_LETTER_JLP_RESUBMISSION_v2.md', 'COVER_LETTER_JLP_RESUBMISSION_v2.docx'),
    ('RESPONSE_TO_REVIEWERS_v2.md',       'RESPONSE_TO_REVIEWERS_v2.docx'),
    ('RESPONSE_TO_REVIEWERS_KO_v2.md',    'RESPONSE_TO_REVIEWERS_KO_v2.docx'),
    ('DECLARATION_OF_INTERESTS.md',       'DECLARATION_OF_INTERESTS.docx'),
    ('HIGHLIGHTS.md',                     'HIGHLIGHTS.docx'),
]


def kill_word_locks():
    """Kill any open Word instance and remove ~$*.docx lock files."""
    if sys.platform != 'win32':
        return
    subprocess.run(['powershell', '-Command',
                    "Get-Process WINWORD -ErrorAction SilentlyContinue | "
                    "Stop-Process -Force -ErrorAction SilentlyContinue"],
                   capture_output=True)
    for f in os.listdir(ROOT):
        if f.startswith('~$') and f.endswith('.docx'):
            try:
                os.remove(os.path.join(ROOT, f))
            except OSError:
                pass


def step(label, fn):
    print(f'\n[{label}]')
    return fn()


def pandoc_pass():
    for src, dst in PANDOC_PAIRS:
        src_path = os.path.join(ARCH, src)
        dst_path = os.path.join(ROOT, dst)
        if not os.path.exists(src_path):
            print(f'  SKIP {src} (source missing)')
            continue
        # Remove old output if present (Word lock recovery)
        if os.path.exists(dst_path):
            try:
                os.remove(dst_path)
            except OSError as e:
                print(f'  ERROR cannot remove {dst}: {e}')
                continue
        cmd = ['pandoc', src_path, '-o', dst_path, '--resource-path', ARCH]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f'  FAIL {src} -> {dst}: {r.stderr.strip()[:200]}')
            sys.exit(1)
        size = os.path.getsize(dst_path)
        print(f'  OK   {src} -> {dst} ({size:,} B)')


def run(script):
    r = subprocess.run([sys.executable, os.path.join(REPO, 'scripts', script)],
                       capture_output=True, text=True, encoding='utf-8',
                       errors='replace')
    if r.stdout:
        print(r.stdout.rstrip())
    if r.stderr:
        print(r.stderr.rstrip())
    if r.returncode != 0 and script != 'audit_submission.py':
        # audit may exit 1 deliberately when blocking issues found
        sys.exit(1)
    return r.returncode


def main():
    print('=' * 70)
    print('JLP revision: one-shot rebuild')
    print('=' * 70)
    step('1/5 Clearing Word locks',  kill_word_locks)
    step('2/5 Pandoc md -> docx',    pandoc_pass)
    step('3/5 build_marked_docx.py', lambda: run('build_marked_docx.py'))
    step('4/5 build_before_after_table.py', lambda: run('build_before_after_table.py'))
    step('5/5 build_change_table.py',       lambda: run('build_change_table.py'))
    print('\n' + '=' * 70)
    print('AUDIT')
    print('=' * 70)
    code = run('audit_submission.py')
    if code == 0:
        print('\nALL GREEN — submission package ready.')
    else:
        print(f'\nAUDIT failed with exit {code}; fix blocking issues above.')
    sys.exit(code)


if __name__ == '__main__':
    main()
