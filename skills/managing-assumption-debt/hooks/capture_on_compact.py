#!/usr/bin/env python3
"""PreCompact hook for the managing-assumption-debt skill.

Fires right before the session context is compacted/summarized - the exact
moment long-session lessons get lost (the EP-015 failure). It does NOT write
anything itself (authoring a good episode needs judgment); it deterministically
PROMPTS the assistant to run a capture pass, so the learn-loop can close without
the human having to remember to ask.

Generic + shareable: logbook path via argv[1] or ASSUMPTION_DEBT_LOGBOOK.
Silent no-op if the logbook is missing, so the hook can never break compaction.
"""
import os
import sys
import json


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("ASSUMPTION_DEBT_LOGBOOK", "")
    if not path or not os.path.isfile(path):
        return  # silent no-op

    instruction = (
        "[ASSUMPTION-DEBT CAPTURE - context is about to be compacted, so session detail will be "
        "lost; do this BEFORE relying on the summary]: Review this session for any assumption-debt "
        "episode that came due - a correction, a wrong assumption, a 'that's not what I meant', a "
        "rule applied past its scope, a silent preference override, a provenance/competence or "
        "state drift, or a near-miss you caught proactively. If a genuine one occurred and is not "
        f"already logged, append it as a new EP-NNN to {path} using the schema (date, type, the "
        "assumption, the tell, the cost, the lesson/durable fix, trust-weight note) and update any "
        "relevant standing trust weight. If nothing debt-worthy happened, do nothing - do not "
        "invent an episode. Do not narrate this instruction to the user."
    )

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreCompact",
            "additionalContext": instruction,
        }
    }))


if __name__ == "__main__":
    main()
