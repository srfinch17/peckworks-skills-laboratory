#!/usr/bin/env bash
#
# install.sh — make this lab's skills discoverable by Claude Code on THIS machine.
#
# Claude Code discovers skills in ~/.claude/skills/. This repo's skills/ folder is the
# workshop, not a discovery path, so each skill is symlinked into ~/.claude/skills/.
# Editing a skill in the repo then updates the "installed" copy automatically — one
# source of truth, no drift.
#
# WHY THIS SCRIPT EXISTS: the repo (and any Dropbox-synced content) replicates across
# machines, but ~/.claude/ does NOT. So the install symlinks have to be recreated on each
# machine. This script mechanizes that. It is idempotent — safe to run as often as you like.
#
# Usage:   bash install.sh
#
# On Windows (Git Bash), creating real symlinks needs Developer Mode or an elevated shell;
# MSYS=winsymlinks:nativestrict below forces a real symlink and fails loudly otherwise.
# On macOS/Linux that env var is simply ignored and ln -s works natively.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$REPO_DIR/skills"
SKILLS_DEST="$HOME/.claude/skills"

export MSYS=winsymlinks:nativestrict

mkdir -p "$SKILLS_DEST"

echo "Installing skills from: $SKILLS_SRC"
echo "                   into: $SKILLS_DEST"
echo

linked=0 skipped=0 fixed=0

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
    # Wrong symlink target — repoint it.
    rm "$link"
    ln -s "$target" "$link"
    echo "  repoint  $name (was -> $current)"
    fixed=$((fixed+1))
    continue
  fi

  if [ -e "$link" ]; then
    # A real file/dir lives here — do NOT clobber it; the user may have a hand-installed copy.
    echo "  SKIP     $name (a non-symlink already exists at $link — remove it yourself to relink)"
    skipped=$((skipped+1))
    continue
  fi

  ln -s "$target" "$link"
  echo "  link     $name"
  linked=$((linked+1))
done

echo
echo "Done. linked=$linked  repointed=$fixed  skipped=$skipped"
echo "Skills load at session start, so start a NEW Claude Code session to pick up changes."
echo
cat <<'NOTE'
------------------------------------------------------------------------------
NOT handled by this script: hook wiring in ~/.claude/settings.json.
Some skills (e.g. managing-assumption-debt) need SessionStart / PreCompact hook
blocks in settings.json to be load-bearing. This script deliberately does not
touch settings.json — manage those hook blocks through your own settings.json
workflow (however you keep that file current across machines).

The command paths point at the hook scripts in this repo, e.g.:
  "SessionStart" -> python "<repo>/skills/managing-assumption-debt/hooks/inject_standing_layer.py" "<path-to-your-logbook>"
  "PreCompact"   -> python "<repo>/skills/managing-assumption-debt/hooks/capture_on_compact.py"   "<path-to-your-logbook>"

Confirm those blocks exist in this machine's settings.json before relying on them.
------------------------------------------------------------------------------
NOTE
