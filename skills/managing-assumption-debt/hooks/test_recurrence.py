"""Assert-based checks for the recurrence counter, distillation nudge and length cap.

Synthetic logbook text only - no personal data. Run: python test_recurrence.py
"""
import inject_standing_layer as h


def ep(n, cls=None, recurs=None, words=20):
    out = f"### EP-{n:03d} - title\n- **Date:** 2026-10-{min(n, 28):02d}\n"
    if cls:
        out += f"- **Class:** {cls}" + (f" | **Recurs:** {recurs}" if recurs else "") + "\n"
    return out + "- body " + "word " * words + "\n\n"


LOG = (
    ep(6, "artifact-trust", "EP-004, EP-002")
    + ep(5, "commission-misread")
    + ep(4, "artifact-trust", "EP-002")
    + ep(3, "scope-creep")
    + ep(2, "artifact-trust")
    + ep(1)                       # pre-schema episode: no Class line, counted as unclassified
)

# Per-class tally over the newest N episodes: count, how many are repeats, latest id.
tally = h.class_tally(LOG, window=5)
assert tally["artifact-trust"] == {"n": 3, "recurs": 2, "latest": 6}, tally
assert tally["commission-misread"] == {"n": 1, "recurs": 0, "latest": 5}, tally
assert "scope-creep" in tally and tally["scope-creep"]["n"] == 1
assert "unclassified" not in tally          # EP-001 falls outside the window of 5
assert h.class_tally(LOG, window=6)["unclassified"]["n"] == 1

# The injected summary names the top classes, repeat share, and the latest episode of each.
line = h.recurrence_summary(LOG, window=5, top=2)
assert "artifact-trust 3 (2 repeats, latest EP-006)" in line, line
assert "commission-misread 1" in line and "scope-creep" not in line, line
assert "2 of 5" in line, line               # repeat share in the window

# Archive text contributes episodes too (older than the main file's).
assert h.class_tally(ep(9, "scope-creep") + LOG, window=20)["scope-creep"]["n"] == 2

# Length cap: the newest episode over the word cap is named; one under it is not.
assert h.long_episodes(ep(7, "scope-creep", words=300) + LOG, cap=150) == [7]
assert h.long_episodes(LOG, cap=150) == []

# Distillation nudge: N episodes since the standing layer last changed.
# state is a dict {"layer_hash": ..., "episodes_at_change": ...}; the function returns
# (new_state, due) and is pure so the test needs no files.
layer = "## Standing trust weights\n- a weight\n"
state, due = h.distillation_check({}, layer, n_eps=100, every=10)
assert due is False and state["episodes_at_change"] == 100          # first sight: baseline, no nudge
state, due = h.distillation_check(state, layer, n_eps=109, every=10)
assert due is False
state, due = h.distillation_check(state, layer, n_eps=110, every=10)
assert due is True and state["episodes_at_change"] == 100           # nudge, baseline unchanged
state, due = h.distillation_check(state, layer + "- a new weight\n", n_eps=111, every=10)
assert due is False and state["episodes_at_change"] == 111          # layer changed: baseline resets

print("all checks pass")
