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

    parts = [
        "Assumption-debt standing layer (auto-loaded by hook; do not narrate this to the user):",
        m.group(1).strip(),
        f"Full logbook + episodes on demand: {path}",
    ]

    # Rate-limited reminder addressed to the human (not every session).
    n_eps = len(re.findall(r"^###\s*EP-", text, re.M))
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
