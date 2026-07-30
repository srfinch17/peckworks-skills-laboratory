#!/usr/bin/env python3
"""PreCompact hook for the managing-assumption-debt skill.

Fires right before the session context is compacted/summarized - the exact
moment long-session lessons get lost (the EP-015 failure). It does NOT write
anything itself (authoring a good episode needs judgment); it raises a visible
nudge to run a capture pass before the detail is gone.

ponytail: PreCompact has NO model-context channel - `additionalContext` is only
valid for UserPromptSubmit / PostToolUse / PostToolBatch / Stop, so the original
version failed schema validation on every compact and never fired. `systemMessage`
is the only outlet, and it addresses the HUMAN, not the assistant. Upgrade path if
the reminder is not enough: write a pending-capture marker file here, and add a
UserPromptSubmit hook that injects the instruction and clears the marker.

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

    nudge = (
        "ASSUMPTION-DEBT CAPTURE: context is about to be compacted, so session detail will be lost. "
        "If a debt episode came due this session (a correction, a wrong assumption, a rule applied "
        "past its scope, a silent preference override, a provenance/competence or state drift, or a "
        "near-miss), ask for a capture pass now, BEFORE relying on the summary. "
        f"Logbook: {path}"
    )

    print(json.dumps({"systemMessage": nudge}))


if __name__ == "__main__":
    main()
