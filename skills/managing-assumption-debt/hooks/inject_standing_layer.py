#!/usr/bin/env python3
"""SessionStart hook for the managing-assumption-debt skill.

Deterministically re-injects the logbook's compact "Standing trust weights"
section into every session (defeating cross-session context loss), and on a
rate-limited cadence asks the assistant to remind the human that the system
exists and how it learns.

Generic + shareable: the logbook path is argv[1] (or the ASSUMPTION_DEBT_LOGBOOK
env var). No personal data lives in this file. It is a silent no-op if the
logbook is missing, so the hook can never break a session.

Wire it as a SessionStart hook, e.g.:
  python "<...>/inject_standing_layer.py" "<...>/assumption_debt_log.md"
"""
import os
import re
import sys
import json
import datetime

REMINDER_EVERY_DAYS = 7

EP_HEAD = re.compile(r"^###\s*EP-(\d+)\b", re.M)
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def audit(text: str):
    """Episode count, next free id, and any structural drift.

    The logbook once split into two independently-numbered append regions under a
    single "newest first" heading: ten ids collided and the most recent episode sat
    last in the file, so session-start reads of the top silently missed three weeks.
    Nothing was watching, so the drift read as fine. Publishing the next free id is
    what prevents a recurrence - the collisions happened because that number was not
    knowable at a glance from either end of an 900-line file.
    """
    heads = list(EP_HEAD.finditer(text))
    ids, dates = [], []
    for i, h in enumerate(heads):
        stop = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        ids.append(int(h.group(1)))
        d = ISO_DATE.search(text, h.end(), min(stop, h.end() + 400))
        dates.append(d.group(0) if d else None)

    warns = []
    dup = sorted({n for n in ids if ids.count(n) > 1})
    if dup:
        warns.append("duplicate ids " + ", ".join(f"EP-{n:03d}" for n in dup))
    seen = [d for d in dates if d]
    if seen != sorted(seen, reverse=True):
        warns.append("episodes are not newest-first, so a recent one is buried mid-file")
    # Undated episodes are a known cosmetic gap in the early entries, not corruption.
    # Kept out of warns deliberately: a condition that fires every session forever is
    # how a guard trains you to ignore it.
    undated = sum(1 for d in dates if not d)
    return len(ids), (max(ids) + 1 if ids else 1), warns, undated


def emit(context: str) -> None:
    # Documented SessionStart contract for adding context to the session.
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }))


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("ASSUMPTION_DEBT_LOGBOOK", "")
    if not path or not os.path.isfile(path):
        return  # silent no-op; never break a session

    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return

    # The compact, always-relevant layer only (NOT the full episodes, which load
    # on demand via the existing memory trigger - avoids double-loading).
    m = re.search(r"(^##+\s*Standing trust weights.*?)(?=^##\s|\Z)", text, re.S | re.M)
    if not m:
        return

    n_eps, next_id, warns, undated = audit(text)
    gap = f" ({undated} early entries carry no date line.)" if undated else ""

    parts = [
        "Assumption-debt standing layer (auto-loaded by hook; do not narrate this to the user):",
        m.group(1).strip(),
        f"Full logbook + episodes on demand: {path}",
        f"Logbook: {n_eps} episodes, newest first. A new episode takes id EP-{next_id:03d} and goes "
        "at the TOP of the Episodes section. Do not infer the next id by reading either end of the "
        "file; use the number given here." + gap,
    ]

    if warns:
        parts.append(
            "[LOGBOOK INTEGRITY WARNING - the logbook has structurally drifted; relay this to the "
            "user rather than silently working around it]: " + "; ".join(warns) + "."
        )

    # Rate-limited reminder addressed to the human (not every session).
    state = os.path.join(os.path.dirname(path), ".assumption_debt_reminder_state")
    today = datetime.date.today()
    due = True
    try:
        with open(state) as f:
            due = (today - datetime.date.fromisoformat(f.read().strip())).days >= REMINDER_EVERY_DAYS
    except (OSError, ValueError):
        due = True

    if due:
        parts.append(
            "[REMINDER DUE - relay to the user in one short, friendly line at the top of your "
            f"first reply]: The assumption-debt logbook is active ({n_eps} episodes). It does not "
            "learn on its own - ask me to \"log the lessons\" at the end of any session where "
            "something went sideways and I'll append an episode. Say \"assumption check\" anytime "
            "to consult it."
        )
        try:
            with open(state, "w") as f:
                f.write(today.isoformat())
        except OSError:
            pass

    emit("\n\n".join(parts))


if __name__ == "__main__":
    main()
