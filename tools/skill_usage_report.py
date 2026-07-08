#!/usr/bin/env python3
"""skill_usage_report.py - sweep local Claude Code transcripts and report skill usage.

Counts Skill-tool invocations in ~/.claude/projects/**/*.jsonl (every session transcript
records each Skill call as a tool_use block). Produces a per-skill table: total invocations,
invocations in the last N days, last-used date, distinct projects; flags which skills live in
this lab and lists lab skills that were never invoked (retirement-review candidates).

Usage (from anywhere; run with `py` on Windows):
    py tools/skill_usage_report.py                # full report, 30-day recent window
    py tools/skill_usage_report.py --days 7       # change the recent window
    py tools/skill_usage_report.py --project job  # only projects whose dir name contains "job"
    py tools/skill_usage_report.py --csv out.csv  # also write the rows as CSV (UTF-8)

Notes / honest limits:
- Usage is a WEAK proxy for value. The value signal is the Provenance win log in each
  SKILL.md (see CONTRIBUTING.md, "Logging value"). This report exists to answer "does it
  fire at all / where / how often", and to surface never-fired lab skills.
- Only explicit Skill-tool calls are counted. Built-in CLI commands (/model, /help) and
  hook-injected content do not go through the Skill tool and are invisible here.
- ASCII-only output on purpose: the Windows console (cp1252) chokes on fancy glyphs.
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"
LAB_SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"

# cheap substring pre-filters so we json.loads only candidate lines (transcripts are big)
PREFILTERS = ('"name":"Skill"', '"name": "Skill"')


def short_project(dirname: str) -> str:
    """Turn the encoded project dir name into a short readable tail."""
    # dir names look like C--Users-x-Dropbox-Dev-repos-peckworks-clipmeta
    parts = dirname.strip("-").split("-")
    return "-".join(parts[-3:]) if len(parts) > 3 else dirname


def iter_skill_calls(project_filter: str | None):
    """Yield (skill_name, timestamp_or_None, project_dirname) for every Skill tool_use."""
    if not PROJECTS_DIR.is_dir():
        sys.exit(f"No transcripts dir at {PROJECTS_DIR}")
    for jsonl in PROJECTS_DIR.glob("*/*.jsonl"):
        project = jsonl.parent.name
        if project_filter and project_filter.lower() not in project.lower():
            continue
        try:
            with open(jsonl, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if not any(p in line for p in PREFILTERS):
                        continue
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    msg = rec.get("message") or {}
                    content = msg.get("content")
                    if not isinstance(content, list):
                        continue
                    ts = rec.get("timestamp")
                    for block in content:
                        if (
                            isinstance(block, dict)
                            and block.get("type") == "tool_use"
                            and block.get("name") == "Skill"
                        ):
                            skill = (block.get("input") or {}).get("skill")
                            if skill:
                                yield skill, ts, project
        except OSError:
            continue  # unreadable file; skip, never crash the sweep


def parse_ts(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--days", type=int, default=30, help="recent-window size (default 30)")
    ap.add_argument("--project", help="only project dirs whose name contains this substring")
    ap.add_argument("--csv", help="also write rows to this CSV path (UTF-8)")
    args = ap.parse_args()

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    lab_skills = (
        sorted(p.parent.name for p in LAB_SKILLS_DIR.glob("*/SKILL.md"))
        if LAB_SKILLS_DIR.is_dir()
        else []
    )

    total = defaultdict(int)
    recent = defaultdict(int)
    last_used = {}
    projects = defaultdict(set)
    files_hint = 0

    for skill, ts, project in iter_skill_calls(args.project):
        files_hint += 1
        total[skill] += 1
        projects[skill].add(project)
        dt = parse_ts(ts)
        if dt:
            if dt >= cutoff:
                recent[skill] += 1
            if skill not in last_used or dt > last_used[skill]:
                last_used[skill] = dt

    if not total:
        print("No Skill invocations found (check --project filter or transcripts dir).")
        return

    rows = []
    for skill in sorted(total, key=lambda s: (-total[s], s)):
        rows.append(
            {
                "skill": skill,
                "total": total[skill],
                f"last_{args.days}d": recent[skill],
                "last_used": last_used[skill].date().isoformat() if skill in last_used else "?",
                "projects": len(projects[skill]),
                "lab": "LAB" if skill.split(":")[-1] in lab_skills else "",
            }
        )

    w_skill = max(len(r["skill"]) for r in rows)
    hdr = f"{'SKILL':<{w_skill}}  TOTAL  {args.days}D  LAST-USED   PROJ  LAB"
    print(f"Skill usage report - {sum(total.values())} invocations across "
          f"{len(total)} skills (window: last {args.days} days)")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(
            f"{r['skill']:<{w_skill}}  {r['total']:>5}  {r[f'last_{args.days}d']:>3}  "
            f"{r['last_used']:>10}  {r['projects']:>4}  {r['lab']}"
        )

    fired = {r["skill"].split(":")[-1] for r in rows}
    never = [s for s in lab_skills if s not in fired]
    print()
    if never:
        print("Lab skills NEVER invoked (retirement-review candidates, or too new): "
              + ", ".join(never))
    else:
        print("Every lab skill has fired at least once.")
    print("Reminder: usage is not value - check each skill's Provenance win log "
          "(CONTRIBUTING.md, 'Logging value').")

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"CSV written: {args.csv}")


if __name__ == "__main__":
    main()
