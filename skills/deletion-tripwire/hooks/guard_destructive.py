#!/usr/bin/env python3
"""Deletion tripwire — PreToolUse hook for Claude Code.

Blocks destructive shell commands until the enumerate -> confirm -> ledger -> approve
protocol has been followed. Born from a public field disaster (a `Windows.old` cleanup
that followed junctions into live Documents/Pictures) and a local miniature (a "clean up
junk" pass that deleted a skill's only test evidence).

Contract: stdin JSON {tool_name, tool_input:{command}}; exit 0 allows, exit 2 + stderr
blocks (the stderr message is fed back to the model). Ledger dir as argv[1], default
~/.claude/deletion-ledger.
"""
import json
import os
import re
import sys
import time

APPROVAL_RE = re.compile(r"tripwire-approved:([A-Za-z0-9_\-]+)")
LEDGER_MAX_AGE_SECONDS = 15 * 60
# ponytail: tiny allowlist on purpose; expand deliberately, never generically
EPHEMERAL_TARGETS = ("node_modules", "__pycache__")

# One combined list applied to every shell: over-blocking across shells is harmless,
# under-blocking is the disaster. Each entry: (compiled regex, short reason).
# ponytail: pattern-based with named ceilings (see SKILL.md); grows with incidents.
PATTERNS = [
    # the flag must be a whitespace-preceded TOKEN, or a hyphenated filename ("my-report.txt",
    # "deletion-tripwire/") false-matches as a flag
    (re.compile(r"(?<![\w/-])rm\s[^;&|]*?(?<=\s)(-\w*[rR]\w*|--recursive)\b"), "recursive rm"),
    (re.compile(r"(?i)\b(remove-item|ri|rmdir|rd|del|erase)\b[^;|]*\s-r(e\w*)?\b"), "Remove-Item -Recurse"),
    (re.compile(r"(?i)\b(rd|rmdir|del)\b[^;|]*\s/s\b"), "cmd-style /s delete"),
    (re.compile(r"(?i)\brobocopy\b[^;|]*\s/(mir|purge)\b"), "robocopy /MIR|/PURGE (deletes at destination)"),
    (re.compile(r"\bgit\s+clean\b[^;&|]*-\w*[fdxX]"), "git clean"),
    (re.compile(r"\bgit\s+reset\s+--hard"), "git reset --hard"),
    (re.compile(r"\bfind\b[^;&|]*(\s-delete\b|\s-exec\s+rm\b)"), "find -delete/-exec rm"),
    (re.compile(r"shutil\.rmtree"), "shutil.rmtree"),
    (re.compile(r"\bdd\b[^;&|]*\bof=/dev/"), "dd onto a device"),
    (re.compile(r"\bmkfs(\.\w+)?\b"), "mkfs"),
    (re.compile(r"(?i)\b(format-volume\b|format\s+[a-z]:)"), "format a volume"),
]

# `rm -Recurse` in PowerShell is Remove-Item; the rm pattern above catches -R via -\w*[rR].
# The Remove-Item pattern deliberately skips bare `rm` (bash rm is handled by the first
# pattern; PS `rm -r`+ abbreviations reach Remove-Item via alias and match pattern 1 or 2).


def _matched(command):
    for regex, reason in PATTERNS:
        if regex.search(command):
            return reason
    return None


def _is_single_ephemeral_target(command):
    """Allow `rm -rf node_modules`-shaped commands: one simple statement, one target,
    and that target's last path component is on the ephemeral allowlist."""
    if re.search(r"[;&|]", command):
        return False
    tokens = command.split()
    # keep it simple: non-flag tokens after the command name are the targets
    targets = [t for t in tokens[1:] if not t.startswith("-")]
    if len(targets) != 1:
        return False
    last = re.split(r"[\\/]", targets[0].rstrip("\\/"))[-1]
    return last in EPHEMERAL_TARGETS


def _protocol_message(reason, ledger_dir):
    suggested_id = time.strftime("%Y%m%d-%H%M%S") + "-describe-target"
    return (
        f"TRIPWIRE: destructive command blocked ({reason}). A deletion's blast radius is "
        "everything REACHABLE from the target, not the folder named. Protocol before this may run:\n"
        "1. ENUMERATE, don't predict: dry-run the reachable set (count, total size, sample paths) "
        "and hunt links/junctions resolving OUTSIDE the target "
        "(PowerShell: Get-ChildItem <target> -Recurse -Force -Attributes ReparsePoint; "
        "bash: find <target> -type l). Anything escaping the target is a hard STOP to report.\n"
        "2. CONFIRM: show the user the manifest (and anything outside-target); get an explicit yes. "
        "If the user never asked for a deletion, stop and surface instead of proceeding.\n"
        f"3. LEDGER: write {os.path.join(ledger_dir, suggested_id + '.md')} BEFORE deleting - "
        "the user's verbatim ask, the command, the manifest summary, the confirmation.\n"
        f"4. RERUN the same command with trailing comment: # tripwire-approved:{suggested_id}\n"
        "Prefer recoverable deletion (Recycle Bin / move-aside) over permanent when practical."
    )


def decide(tool_name, command, ledger_dir, now=None):
    """Return ("allow"|"block", reason)."""
    reason = _matched(command)
    if reason is None:
        return ("allow", "no destructive pattern")
    if _is_single_ephemeral_target(command):
        return ("allow", "single ephemeral target")
    token = APPROVAL_RE.search(command)
    if token:
        entry = os.path.join(ledger_dir, token.group(1) + ".md")
        if not os.path.isfile(entry):
            return ("block", f"TRIPWIRE: approval token given but no ledger entry at {entry}. "
                             "Write the ledger entry first (step 3 of the protocol), then rerun.")
        age = (now or time.time()) - os.path.getmtime(entry)
        if age > LEDGER_MAX_AGE_SECONDS:
            return ("block", f"TRIPWIRE: ledger entry {entry} is stale ({int(age // 60)} min old; "
                             "limit 15). Re-verify the manifest with the user, refresh the entry, rerun.")
        return ("allow", "approved via ledger")
    return ("block", _protocol_message(reason, ledger_dir))


def main():
    ledger_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.expanduser("~"), ".claude", "deletion-ledger")
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # unparseable input: never brick the harness on a guard bug
    command = (data.get("tool_input") or {}).get("command", "")
    if not command:
        sys.exit(0)
    verdict, reason = decide(data.get("tool_name", ""), command, ledger_dir)
    if verdict == "block":
        print(reason, file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
