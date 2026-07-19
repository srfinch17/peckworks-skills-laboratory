---
name: deletion-tripwire
description: Use when a TRIPWIRE block message appears after a destructive command, when wiring the deletion guard on a new machine, or before any bulk deletion or cleanup — "remove junk", "clean up", "delete old files", "wipe this folder", clearing an old installation, or any recursive/force delete — so the enumerate-confirm-ledger protocol runs before anything leaves existence.
---

# Deletion Tripwire

## Overview

A **mechanical** guard, not a persona: a PreToolUse hook that intercepts destructive shell
commands and refuses to run them until the enumerate → confirm → ledger → approve protocol has
been followed. It exists because the catastrophic-deletion class strikes during casual,
un-reviewed operations, when no review panel is in session — so the guard must fire EVERY time,
without anyone remembering to ask.

The two lessons it enforces, burned in by a public field disaster (an agent cleaned up
`Windows.old` after answering "safe" when asked directly; leftover junctions inside it pointed at
the user's LIVE Documents/Pictures; the deletion followed the links and emptied the real folders):

1. **The blast radius of a deletion is everything REACHABLE from the target** — links and
   junctions included — not the folder that was named.
2. **"Is it safe?" answered by prediction is the weapon.** Safety requires enumeration (a dry
   run that lists what will actually be touched), never reasoning about what should be there.

This is the deletion-direction sibling of the push/publish/send boundary: two irreversible
directions, leaving the machine (can't recall) and leaving existence (can't recover).

## The protocol (what the block message demands)

1. **ENUMERATE, don't predict.** Dry-run the reachable set: count, total size, sample paths.
   Hunt links/junctions resolving OUTSIDE the target
   (PowerShell: `Get-ChildItem <target> -Recurse -Force -Attributes ReparsePoint`;
   bash: `find <target> -type l`). Anything escaping the target is a hard stop to report.
2. **CONFIRM.** Show the user the manifest and anything outside-target; get an explicit yes.
   If the user never asked for a deletion, stop and surface instead of proceeding.
3. **LEDGER.** Write `<ledger>/<id>.md` BEFORE deleting: the user's verbatim ask, the command,
   the manifest summary, the confirmation. Evidence of what died, every time — experiment
   artifacts and receipts have been destroyed by innocent "clean up junk" passes before.
4. **RERUN** the same command with trailing comment `# tripwire-approved:<id>`. The hook allows
   it only while the ledger entry is fresh (15 minutes).

Prefer recoverable deletion (Recycle Bin / move-aside) over permanent when practical.

## Setup (per machine, like the assumption-debt hooks)

`install.sh` symlinks this skill but deliberately does not touch `settings.json`. Wire the hook
manually as a PreToolUse entry matching `Bash|PowerShell`:

```json
"PreToolUse": [{
  "matcher": "Bash|PowerShell",
  "hooks": [{ "type": "command",
    "command": "python \"<repo>/skills/deletion-tripwire/hooks/guard_destructive.py\" \"<ledger-dir>\"" }]
}]
```

Ledger default: `~/.claude/deletion-ledger/`. Self-check: `python hooks/test_guard.py`.

## What it blocks / what it lets through

| Blocked (any shell) | Allowed |
|---|---|
| `rm` with `-r`/`--recursive` (any flag combo) | single-file `rm` / `Remove-Item` |
| `Remove-Item -Recurse` (+ aliases/abbreviations) | non-delete commands with `-r` flags (`grep -r`) |
| `rd|rmdir|del /s` | `rm -rf node_modules` / `__pycache__` (single simple target) |
| `robocopy /MIR|/PURGE` | approved rerun with fresh ledger entry |
| `git clean -f*`, `git reset --hard` | |
| `find -delete` / `find -exec rm`, `shutil.rmtree` | |
| `dd of=/dev/*`, `mkfs`, `format X:` | |

## Common Mistakes

- **Self-serving the approval token without doing the protocol.** The token is not a bypass;
  writing the ledger entry REQUIRES the enumeration and the user's confirmation to already
  exist. Skipping to step 4 defeats the guard and re-arms the exact disaster it prevents.
- **Predicting instead of enumerating.** "That folder only contains X" is the sentence that
  destroyed a stranger's family photos. Run the dry-run; read the real list.
- **Growing the ephemeral allowlist casually.** Every generic name added (`build`, `dist`,
  `temp`) widens the silent path. Expand only deliberately, for names that are unambiguous.
- **Treating a quiet tripwire as a broken one.** It is pattern-based and stays silent on normal
  work by design (a guard that fires constantly gets tuned out). Known ceilings are named in
  the design spec; grow the pattern list with incidents, not speculation.
- **Weakening the matcher because prose tripped it.** The guard cannot tell running a
  destructive command from *talking about one* — a commit message or echo that mentions the
  patterns gets blocked (observed twice on day one, on this very skill's own commit messages).
  That over-blocking is deliberate: quote-stripping would open a `bash -c "<destructive>"`
  bypass. The durable workaround is to keep such prose OUT of the shell string — write commit
  messages to a file and use `git commit -F <file>`, print docs from files instead of echoes.

## Provenance

Born 2026-07-19, test-first (RED: 35-check assert suite watched failing on the missing module;
GREEN: all pass, including the end-to-end stdin/exit-code hook contract). Motivating cases:
(1) public r/ClaudeCode data-loss incident, 2026-07 — `Windows.old` cleanup followed junctions
into live Documents/Pictures after the agent answered "safe" from prediction; (2) same-day local
miniature in this lab — a routine "clean up any junk" pass deleted the artifacts that were a
skill's only test evidence ([[paladin-review-works]]). Design spec:
`docs/specs/2026-07-19-deletion-tripwire-design.md`. Field wins to be appended per the
Provenance win rule.
