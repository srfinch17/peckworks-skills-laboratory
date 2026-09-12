# PreToolUse guard (Workflow): refuse a multi-agent launch whose script does not carry a typed token
# estimate and a cheap path, and refuse a launch over the pause threshold unless the user approved it.
#
# The skill says "type the estimate before launching"; this makes the typed estimate a precondition.
# The estimate lives as comment lines at the top of the workflow script (comments are safe inside
# the script's pure-literal `meta` rules):
#
#     // est-tokens: 120k
#     // cheap-path: one Explore agent reading the two primary sources, ~15k
#     // user-approved: yes        <- only after the hold-up message was posted and answered
#
# Wire in ~/.claude/settings.json under hooks.PreToolUse with matcher "Workflow".
# `python guard_fanout.py --selftest` runs the cases below.
import sys, json, re, pathlib

THRESHOLD = 500_000
EST = re.compile(r"^\s*//\s*est-tokens:\s*([\d.,]+)\s*([kKmM]?)", re.M)
CHEAP = re.compile(r"^\s*//\s*cheap-path:\s*\S", re.M)
APPROVED = re.compile(r"^\s*//\s*user-approved:\s*(yes|true)", re.M | re.I)


def parse_tokens(num, unit):
    n = float(num.replace(",", ""))
    return int(n * {"k": 1_000, "m": 1_000_000}.get(unit.lower(), 1))


def deny(reason):
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        },
        "systemMessage": reason.split("\n")[0],
    }


def decide(tool_input, read_file=lambda p: pathlib.Path(p).read_text(encoding="utf-8")):
    script = tool_input.get("script")
    if not script and tool_input.get("scriptPath"):
        try:
            script = read_file(tool_input["scriptPath"])
        except OSError as e:
            return deny(f"BLOCKED: could not read scriptPath to check the estimate ({e}).")
    if not script:
        return {}  # a saved workflow by name: nothing to inspect
    m = EST.search(script)
    if not m or not CHEAP.search(script):
        return deny(
            "BLOCKED by pause-before-nuclear-fanout: the script has no typed estimate. Add two comment "
            "lines at the top: `// est-tokens: <N>k` and `// cheap-path: <what one agent or inline reads "
            "would give>`. Price it before launching; if it is over 500k tokens, post the four-line "
            "hold-up message and end the turn."
        )
    est = parse_tokens(m.group(1), m.group(2))
    if est > THRESHOLD and not APPROVED.search(script):
        return deny(
            f"BLOCKED by pause-before-nuclear-fanout: estimate {est:,} tokens is over the "
            f"{THRESHOLD:,} pause threshold. Post the hold-up message (what, estimated tokens and wall "
            "clock, the cheap path, 'which one?') and END THE TURN. Relaunch with `// user-approved: yes` "
            "only after the user answered."
        )
    return {}


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        d = lambda s: decide({"script": s})
        ok = "// est-tokens: 120k\n// cheap-path: one Explore agent\nexport const meta = {}\n"
        assert d(ok) == {}
        assert "no typed estimate" in d("export const meta = {}\n")["hookSpecificOutput"]["permissionDecisionReason"]
        assert "no typed estimate" in d("// est-tokens: 120k\nexport const meta = {}\n")["hookSpecificOutput"]["permissionDecisionReason"]  # cheap-path missing
        big = "// est-tokens: 6.4m\n// cheap-path: read the memos myself\nexport const meta = {}\n"
        assert "over the 500,000" in d(big)["hookSpecificOutput"]["permissionDecisionReason"]
        assert d(big + "// user-approved: yes\n") == {}
        assert d("// est-tokens: 500,001\n// cheap-path: x\n")["hookSpecificOutput"]["permissionDecision"] == "deny"
        assert d("// est-tokens: 500k\n// cheap-path: x\n") == {}  # at the threshold passes
        assert decide({"name": "saved-workflow"}) == {}
        assert decide({"scriptPath": "x.js"}, read_file=lambda p: ok) == {}
        assert "could not read" in decide({"scriptPath": "missing.js"})["hookSpecificOutput"]["permissionDecisionReason"]
        assert parse_tokens("1,200", "k") == 1_200_000 and parse_tokens("2", "M") == 2_000_000 and parse_tokens("900", "") == 900
        print("guard_fanout selftest: 11 cases OK")
        sys.exit(0)
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    if payload.get("tool_name") != "Workflow":
        sys.exit(0)
    out = decide(payload.get("tool_input") or {})
    if out:
        print(json.dumps(out))
    sys.exit(0)
