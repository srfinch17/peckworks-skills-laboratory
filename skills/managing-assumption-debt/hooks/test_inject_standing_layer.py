"""Assert-based checks for inject_standing_layer.audit / episode_date.

Synthetic logbook text only - no personal data. Run: python test_inject_standing_layer.py
"""
import inject_standing_layer as h


def ep(n, date_line=None, note=None):
    out = f"### EP-{n:03d} - title\n"
    if note:
        out += f"> {note}\n"
    if date_line is not None:
        out += f"- **Date:** {date_line}\n"
    return out + "- **Type:** t\n- body\n\n"


# Correctly sorted per the logbook's convention: range episodes sort by END date,
# and a meta-note above the Date line may carry a LATER date than the event.
GOOD = (
    ep(7, "2026-08-21")
    + ep(6, "2026-08-19", note="(Renumbered from a duplicate on 2026-08-20: ...)")
    + ep(5, "2026-08-05/06")
    + ep(4, "2026-08-03 to 08-06")
    + ep(3, "2026-08-04")
    + ep(2, "career session deadbeef")   # undated: skipped, never a warn
    + ep(1, "2026-08-01")
)

# Date extraction: Date-line anchored, range tails resolve to the END date.
assert h.episode_date("- **Date:** 2026-08-04 (x)\n") == "2026-08-04"
assert h.episode_date("- **Date:** 2026-08-05/06 (x)\n") == "2026-08-06"
assert h.episode_date("- **Date:** 2026-08-03 to 08-06 (x)\n") == "2026-08-06"
assert h.episode_date("> note from 2026-08-20\n- **Date:** 2026-08-19 (x)\n") == "2026-08-19"
assert h.episode_date("- **Date:** career session deadbeef\n") is None
assert h.episode_date("no date line at all\n") is None

n, next_id, warns, undated = h.audit(GOOD)
assert (n, next_id, undated) == (7, 8, 1), (n, next_id, undated)
assert warns == [], warns

# The guard must still FIRE: bury the newest episode mid-file.
BURIED = ep(6, "2026-08-10") + ep(7, "2026-08-21") + ep(5, "2026-08-05")
warns = h.audit(BURIED)[2]
assert len(warns) == 1 and "EP-006 dated 2026-08-10 sits above newer EP-007 dated 2026-08-21" in warns[0], warns

# Duplicate-id warn unchanged.
warns = h.audit(ep(3, "2026-08-21") + ep(3, "2026-08-20"))[2]
assert any("duplicate ids EP-003" in w for w in warns), warns

print("all checks pass")
