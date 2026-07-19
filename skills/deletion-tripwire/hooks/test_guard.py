#!/usr/bin/env python3
"""Self-check for guard_destructive.py — assert-based, no framework. Run directly."""
import json
import os
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guard_destructive import decide  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def check(name, got, want):
    verdict = got[0]
    assert verdict == want, f"{name}: want {want}, got {got}"
    print(f"  ok  {name}")


def main():
    ledger = tempfile.mkdtemp(prefix="tripwire-test-")

    # --- destructive: block ---
    check("rm -rf", decide("Bash", "rm -rf /old", ledger), "block")
    check("rm -fr", decide("Bash", "rm -fr ~/x", ledger), "block")
    check("rm --recursive", decide("Bash", "rm --recursive x", ledger), "block")
    check("compound rm -rf", decide("Bash", "cd /tmp && rm -rf cache2", ledger), "block")
    check("git clean -fdx", decide("Bash", "git clean -fdx", ledger), "block")
    check("git reset --hard", decide("Bash", "git reset --hard HEAD~1", ledger), "block")
    check("find -delete", decide("Bash", "find . -name '*.log' -delete", ledger), "block")
    check("find -exec rm", decide("Bash", "find . -name x -exec rm {} \\;", ledger), "block")
    check("shutil.rmtree", decide("Bash", "python -c \"import shutil; shutil.rmtree('x')\"", ledger), "block")
    check("dd of=device", decide("Bash", "dd if=/dev/zero of=/dev/sda", ledger), "block")
    check("Remove-Item -Recurse", decide("PowerShell", "Remove-Item -Recurse -Force C:\\old", ledger), "block")
    check("Remove-Item -r abbrev", decide("PowerShell", "Remove-Item -r C:\\old", ledger), "block")
    check("rm alias -Recurse", decide("PowerShell", "rm -Recurse .\\stale", ledger), "block")
    check("rd /s /q", decide("PowerShell", "rd /s /q C:\\old", ledger), "block")
    check("del /s", decide("PowerShell", "del /s /q folder", ledger), "block")
    check("robocopy /MIR", decide("PowerShell", "robocopy a b /MIR", ledger), "block")
    check("robocopy /PURGE", decide("Bash", "robocopy old new /PURGE", ledger), "block")
    check("format drive", decide("PowerShell", "format D:", ledger), "block")
    check("mkfs", decide("Bash", "mkfs.ext4 /dev/sdb1", ledger), "block")

    # --- benign: allow (the tripwire must stay quiet or it gets tuned out) ---
    check("rm single file", decide("Bash", "rm notes.txt", ledger), "allow")
    check("grep -r", decide("Bash", "grep -r foo .", ledger), "allow")
    check("git status", decide("Bash", "git status", ledger), "allow")
    check("git commit hard msg", decide("Bash", 'git commit -m "hard reset lesson"', ledger), "allow")
    check("npm run format", decide("Bash", "npm run format", ledger), "allow")
    check("Remove-Item single", decide("PowerShell", "Remove-Item foo.txt", ledger), "allow")
    check("ls", decide("PowerShell", "Get-ChildItem -Recurse .", ledger), "allow")

    # --- ephemeral allowlist: single simple target only ---
    check("rm -rf node_modules", decide("Bash", "rm -rf node_modules", ledger), "allow")
    check("rm -rf __pycache__", decide("Bash", "rm -rf src/__pycache__", ledger), "allow")
    check("node_modules plus more", decide("Bash", "rm -rf node_modules /home", ledger), "block")
    check("node_modules compound", decide("Bash", "rm -rf node_modules && rm -rf /etc", ledger), "block")

    # --- approval token + ledger ---
    fresh_id = "20260719-120000-test"
    with open(os.path.join(ledger, fresh_id + ".md"), "w") as f:
        f.write("test entry")
    check("token + fresh ledger", decide("Bash", f"rm -rf /old  # tripwire-approved:{fresh_id}", ledger), "allow")
    check("token, no ledger file", decide("Bash", "rm -rf /old  # tripwire-approved:nope", ledger), "block")
    stale_id = "20260719-000000-stale"
    stale_path = os.path.join(ledger, stale_id + ".md")
    with open(stale_path, "w") as f:
        f.write("stale entry")
    old = time.time() - 3600
    os.utime(stale_path, (old, old))
    check("token + stale ledger", decide("Bash", f"rm -rf /old  # tripwire-approved:{stale_id}", ledger), "block")

    # --- end-to-end: the real stdin/exit-code hook contract ---
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": "rm -rf /old"}})
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "guard_destructive.py"), ledger],
        input=payload, capture_output=True, text=True,
    )
    assert proc.returncode == 2, f"e2e block: want exit 2, got {proc.returncode}"
    assert "TRIPWIRE" in proc.stderr, f"e2e block: stderr missing protocol: {proc.stderr!r}"
    print("  ok  e2e block via stdin (exit 2 + protocol on stderr)")

    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": "git status"}})
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "guard_destructive.py"), ledger],
        input=payload, capture_output=True, text=True,
    )
    assert proc.returncode == 0, f"e2e allow: want exit 0, got {proc.returncode}"
    print("  ok  e2e allow via stdin (exit 0)")

    print("\nAll tripwire checks passed.")


if __name__ == "__main__":
    main()
