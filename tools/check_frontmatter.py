#!/usr/bin/env python3
"""Fail on SKILL.md frontmatter that Claude Code will silently misread.

Why: on 2026-09-30 four skills in this lab had not been triggering for weeks. Each had a
plain (unquoted) `description:` containing a colon-space, which is invalid YAML. The loader
does not error; it drops the description and shows the skill's title instead, so the agent
never sees the triggering conditions. Nothing said so. This check says so.

Rules (no third-party YAML library needed):
  1. A plain-scalar description must not contain ': ' or ' #'. Fix: write it as a folded
     block (`description: >-` then indented lines), which allows anything.
  2. The description must start with "Use " (the repo convention: triggering conditions only).
Usage:  python tools/check_frontmatter.py            (exit 1 on any failure)
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
failures = 0

for path in sorted(glob.glob(os.path.join(ROOT, 'skills', '*', 'SKILL.md'))):
    name = os.path.basename(os.path.dirname(path))
    text = open(path, encoding='utf-8-sig').read().replace('\r\n', '\n')
    lines = text.split('\n')
    if lines[0] != '---' or '---' not in lines[1:]:
        print(f'FAIL {name}: no frontmatter block'); failures += 1; continue
    end = lines.index('---', 1)
    fm = lines[1:end]
    idx = next((i for i, l in enumerate(fm) if l.startswith('description:')), None)
    if idx is None:
        print(f'FAIL {name}: no description'); failures += 1; continue
    head = fm[idx][len('description:'):].strip()
    if head.startswith(('>', '|')):
        body = []
        for l in fm[idx + 1:]:
            if l.startswith(' ') or l == '':
                body.append(l.strip())
            else:
                break
        desc = ' '.join(b for b in body if b)
    elif head[:1] in ('"', "'"):
        desc = head.strip(head[0])
    else:
        desc = head
        if ': ' in desc or ' #' in desc:
            print(f'FAIL {name}: plain-scalar description contains ": " or " #" (invalid YAML; the '
                  f'loader drops it). Rewrite as a folded block: description: >-')
            failures += 1
    if not desc.startswith('Use '):
        print(f'FAIL {name}: description must start with "Use ..." (got: {desc[:60]!r})')
        failures += 1

print('ok: all SKILL.md frontmatter passes' if not failures else f'{failures} failure(s)')
sys.exit(1 if failures else 0)
