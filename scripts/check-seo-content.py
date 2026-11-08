#!/usr/bin/env python3
"""Check that the SEO summary edits retain original evidence and useful content.

Run against the pre-audit main (default origin/main), or pass an explicit base ref.
Only three generic experiment preambles are replaced. The comparison's existing
verdict gains a research qualification. Original tables, examples, test evidence,
corrections and other paragraphs must remain, even when blocks are reordered.
"""
import collections
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = sys.argv[1] if len(sys.argv) > 1 else 'origin/main'
REPLACED_PREAMBLES = {
    'ai-lead-follow-up-test': '<strong>What this test shows you.</strong>',
    'ai-readiness-checklist-test': '<strong>What this test shows you.</strong>',
    'ai-vs-rules-appointment-payment-reminders': '<strong>What you get from this.</strong>',
}
QUALIFICATION = 'These are researched editorial picks, not side-by-side test results. '
BLOCKS = re.compile(r'<(p|li|h2|h3|pre|table|details)\b[^>]*>.*?</\1>', re.S)

def body(html):
    match = re.search(r'<article class="article-body[^>]*>(.*?)</article>', html, re.S)
    if not match:
        raise AssertionError('Missing article body')
    return match[1]

def blocks(html, slug):
    out = []
    for match in BLOCKS.finditer(body(html).replace(QUALIFICATION, '')):
        block = match[0]
        if slug in REPLACED_PREAMBLES and block.startswith('<p>' + REPLACED_PREAMBLES[slug]):
            continue
        out.append(re.sub(r'\s+', ' ', block).strip())
    return collections.Counter(out)

count = 0
for path in sorted((ROOT / 'blog').glob('*/index.html')):
    rel = path.relative_to(ROOT).as_posix()
    old = subprocess.check_output(['git', 'show', f'{BASE}:{rel}'], cwd=ROOT, text=True)
    new = path.read_text()
    missing = blocks(old, path.parent.name) - blocks(new, path.parent.name)
    if missing:
        raise AssertionError(f'{rel}: original content changed or missing: {list(missing)[:2]}')
    count += 1

method = (ROOT / 'how-we-test/index.html').read_text()
for slug in ('can-ai-enter-invoices-spreadsheet-test', 'ai-lead-follow-up-test',
             'ai-readiness-checklist-test', 'ai-vs-rules-appointment-payment-reminders'):
    assert f'/blog/{slug}/' in method, slug
    assert 'href="/how-we-test/"' in (ROOT / 'blog' / slug / 'index.html').read_text(), slug
print(f'PASS: original content and evidence retained across {count} articles; four methodology links verified.')
