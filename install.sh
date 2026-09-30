#!/usr/bin/env bash
#
# install.sh: make this lab's skills discoverable by Claude Code on THIS machine.
#
# Claude Code discovers skills in ~/.claude/skills/. This repo's skills/ folder is the
# workshop, not a discovery path, so each skill is symlinked into ~/.claude/skills/.
# Editing a skill in the repo then updates the "installed" copy automatically: one
# source of truth, no drift.
#
# WHY THIS SCRIPT EXISTS: the repo (and any Dropbox-synced content) replicates across
# machines, but ~/.claude/ does NOT. So the install symlinks have to be recreated on each
# machine. This script mechanizes that. It is idempotent; safe to run as often as you like.
#
# Usage:   bash install.sh
#
# On Windows (Git Bash), creating a real symlink needs Developer Mode or an elevated shell;
# MSYS=winsymlinks:nativestrict below forces a real symlink attempt and makes ln fail loudly
# instead of silently copying. When that fails, make_link falls back to a DIRECTORY JUNCTION
# (mklink /J), which needs no privilege at all. Git Bash reports a junction as a symlink
# (test -L and readlink both work), so the rest of this script cannot tell the two apart, and
# Claude Code follows either. Learned 2026-09-30: a machine with Developer Mode off had ZERO
# lab skills installed and nobody noticed until a skill failed to trigger.
# On macOS/Linux the env var is ignored and ln -s works natively.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$REPO_DIR/skills"
SKILLS_DEST="$HOME/.claude/skills"

export MSYS=winsymlinks:nativestrict

mkdir -p "$SKILLS_DEST"

# make_link TARGET LINK: a real symlink where the OS allows one, else (Windows) a junction.
make_link() {
  local target="$1" link="$2"
  if ln -s "$target" "$link" 2>/dev/null; then
    return 0
  fi
  if command -v cygpath >/dev/null 2>&1; then
    local wt wl
    wt="$(cygpath -w "$target")"
    wl="$(cygpath -w "$link")"
    # Separate arguments, not one quoted string: Git Bash backslash-escapes embedded quotes
    # on the Windows command line and cmd.exe cannot read that. MSYS_NO_PATHCONV keeps /c
    # and /J from being rewritten as paths.
    if MSYS_NO_PATHCONV=1 cmd /c mklink /J "$wl" "$wt" >/dev/null 2>&1; then
      return 0
    fi
  fi
  echo "  FAILED   $(basename "$link"): could not create a symlink or a junction" >&2
  return 1
}

echo "Installing skills from: $SKILLS_SRC"
echo "                   into: $SKILLS_DEST"
echo

linked=0 skipped=0 fixed=0
shadowed=()   # lab skills masked by a real (non-symlink) dir in ~/.claude/skills

for skill_path in "$SKILLS_SRC"/*/; do
  # Only treat a folder as a skill if it actually has a SKILL.md.
  [ -f "${skill_path}SKILL.md" ] || continue

  name="$(basename "$skill_path")"
  target="${skill_path%/}"          # repo-side skill dir (no trailing slash)
  link="$SKILLS_DEST/$name"         # ~/.claude/skills/<name>

  if [ -L "$link" ]; then
    current="$(readlink "$link")"
    if [ "$current" = "$target" ]; then
      echo "  ok       $name (already linked)"
      skipped=$((skipped+1))
      continue
    fi
    # Wrong symlink target; repoint it.
    rm "$link"
    make_link "$target" "$link"
    echo "  repoint  $name (was -> $current)"
    fixed=$((fixed+1))
    continue
  fi

  if [ -e "$link" ]; then
    # A real file/dir lives here. Do NOT clobber it; the user may have a hand-installed copy.
    # This is the DRIFT HAZARD: the runtime loads that copy, edits in the repo do nothing,
    # and the two silently diverge. It bit this lab once already (look-driven-iteration,
    # repaired by commit e15424e). A quiet one-line SKIP reads like "ok" in a wall of "ok",
    # so it is counted separately and re-reported loudly at the end.
    echo "  SHADOWED $name (a non-symlink exists at $link -- the repo copy is NOT what loads)"
    shadowed+=("$name")
    continue
  fi

  make_link "$target" "$link"
  echo "  link     $name"
  linked=$((linked+1))
done

echo
echo "Done. linked=$linked  repointed=$fixed  skipped=$skipped  shadowed=${#shadowed[@]}"
echo "Skills load at session start, so start a NEW Claude Code session to pick up changes."
echo

if [ "${#shadowed[@]}" -gt 0 ]; then
  echo "=============================================================================="
  echo "!! ${#shadowed[@]} SKILL(S) ARE SHADOWED -- editing the repo does NOTHING for these:"
  for name in "${shadowed[@]}"; do
    echo "     $name"
  done
  cat <<'SHADOWNOTE'

  A real directory in ~/.claude/skills/ masks the repo copy. The runtime loads the
  masking copy; your repo edits go nowhere, and the two drift apart silently.

  To fix, per skill -- diff FIRST, never assume the repo copy is the newer one:
     diff -r ~/.claude/skills/<name> ./skills/<name>
     mv ~/.claude/skills/<name> /tmp/<name>.bak   # move aside, do not delete
     bash install.sh                              # relinks it
  If the diff shows the installed copy is ahead, copy it into the repo and commit
  BEFORE relinking, or you will throw the newer version away.
==============================================================================
SHADOWNOTE
fi
cat <<'NOTE'
------------------------------------------------------------------------------
NOT handled by this script: hook wiring in ~/.claude/settings.json.
Some skills (e.g. managing-assumption-debt) need SessionStart / PreCompact hook
blocks in settings.json to be load-bearing. This script deliberately does not
touch settings.json; manage those hook blocks through your own settings.json
workflow (however you keep that file current across machines).

The command paths point at the hook scripts in this repo, e.g.:
  "SessionStart" -> python "<repo>/skills/managing-assumption-debt/hooks/inject_standing_layer.py" "<path-to-your-logbook>"
  "PreCompact"   -> python "<repo>/skills/managing-assumption-debt/hooks/capture_on_compact.py"   "<path-to-your-logbook>"

Confirm those blocks exist in this machine's settings.json before relying on them.
------------------------------------------------------------------------------
NOTE
