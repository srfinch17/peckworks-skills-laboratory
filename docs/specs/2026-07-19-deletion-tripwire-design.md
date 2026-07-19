# Deletion Tripwire Design Spec

**Date:** 2026-07-19
**Status:** Approved (option "Tripwire hook first"), building test-first

## Problem

Review personas (nemesis, paladin) only protect when a review is convened. The catastrophic
deletion class strikes during casual, un-reviewed operations — field case (public, 2026-07,
r/ClaudeCode "data loss" thread): an agent ran a cleanup of `Windows.old` after confirming
"safe" when asked directly; the folder contained junctions (folder-links) pointing at the
user's LIVE Documents/Pictures; the deletion tool followed the links (the one flag that
prevents it was missing) and emptied the real folders. Total loss + public humiliation.
Same-shape local miniature (2026-07-19, this lab): "clean up any junk" deleted the artifacts
that were a skill's only test evidence.

Two burned-in lessons:
1. **The blast radius of a deletion is everything REACHABLE from the target** (links/junctions),
   not the folder named.
2. **"Is it safe?" answered by prediction is the weapon.** Safety requires enumeration (a dry
   run), never reasoning.

A persona cannot fix this (no court in session at the moment of deletion). Only machinery that
fires EVERY time can: a PreToolUse hook. This is the deletion-direction sibling of the
assumption-debt skill's envisioned push/publish/send boundary guard — two irreversible
directions: leaving the machine (can't recall) and leaving existence (can't recover).

## Design

`skills/deletion-tripwire/`:
- `SKILL.md` — the protocol documentation + provenance.
- `hooks/guard_destructive.py` — the PreToolUse hook (generic; ledger path as argv[1]).
- `hooks/test_guard.py` — assert-based self-check (no framework), run directly.

**Hook contract (Claude Code PreToolUse):** stdin JSON `{tool_name, tool_input:{command}}`;
exit 0 = allow; exit 2 + stderr message = block (message is fed back to the model).

**Decision logic:**
1. One combined destructive-pattern list applied to BOTH shells (over-blocking across shells is
   harmless; under-blocking is the disaster): recursive/force `rm`, `Remove-Item -Recurse`
   (and aliases/abbreviations), cmd-style `rd|rmdir|del /s`, `robocopy /MIR|/PURGE`,
   `git clean -f*`, `git reset --hard`, `find ... -delete|-exec rm`, `shutil.rmtree`,
   `dd of=`, `mkfs`, `format X:`.
2. No match → allow (exit 0). The tripwire must stay quiet on normal work or it gets tuned out
   (the paladin's false-alarm lesson, applied to machinery).
3. Match + single simple ephemeral target (`node_modules`, `__pycache__`) → allow.
   (ponytail: tiny allowlist; expand deliberately, never generically.)
4. Match + `tripwire-approved:<id>` token → allow ONLY if `<ledger>/<id>.md` exists and is
   fresh (<15 min); else block naming the reason.
5. Match otherwise → block with the protocol message:
   - **ENUMERATE, don't predict:** dry-run the reachable set (count, size, sample paths) and
     hunt links/junctions resolving OUTSIDE the target (PowerShell
     `Get-ChildItem -Recurse -Force -Attributes ReparsePoint`; bash `find <t> -type l`).
   - **CONFIRM:** show the user the manifest + anything outside-target; explicit yes required.
     If the user never asked for a deletion, stop and surface instead.
   - **LEDGER:** write `<ledger>/<id>.md` — user's verbatim ask, command, manifest summary,
     confirmation — BEFORE deleting. (Evidence of what died, every time.)
   - **RERUN** with trailing `# tripwire-approved:<id>`.
   - Prefer recoverable deletion (Recycle Bin / move-aside) over permanent when practical.

**Ledger default:** `~/.claude/deletion-ledger/` (overridable via argv[1]).

**Wiring (manual, per machine, like the assumption-debt hooks):** a PreToolUse entry in
`~/.claude/settings.json` matching `Bash|PowerShell`. install.sh does not touch settings.json.

## Known ceilings (named, not hidden)

- **Prose-vs-command over-blocking (observed day one, twice):** text that merely *mentions*
  the patterns (a commit message naming the blocked command families) trips the matcher when it
  rides inside the shell string. Deliberately accepted: stripping quoted spans before matching
  would open a `bash -c "<destructive>"` bypass. Workaround (documented in SKILL.md): keep such
  prose out of the command string — `git commit -F <message-file>` instead of `-m "..."`.

- Pattern-based: a novel destructive command not in the list passes. The list grows with
  incidents; the ledger records what did run.
- The approval token could be self-served by a model that skips the protocol; the threat model
  is misjudgment ("safe" by prediction), not malice — forcing the stop+enumerate loop is the value.
- `Remove-Item -Force` on a directory without `-Recurse`, `git checkout --`, `Clear-Content`
  are not matched (noise/benefit trade); named here for deliberate future expansion.

## Test plan (RED first)

Assert-based `test_guard.py` covering: block on each pattern family; allow on normal commands
(incl. `grep -r`, `git status`); ephemeral allowlist single-target only; token+fresh-ledger
allows; token with missing/stale ledger blocks; one subprocess test of the real stdin/exit-code
contract.
