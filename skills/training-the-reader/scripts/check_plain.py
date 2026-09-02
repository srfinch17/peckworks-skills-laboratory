#!/usr/bin/env python
"""check_plain.py: the plain-prose gate for a teaching markdown file (training-the-reader).

    py check_plain.py <rewritten.md> --orig <original.md> [--config project.json] [--drill]
    py check_plain.py <file.md>                       # prose-only checks, no original
    py check_plain.py --selftest

Frozen versus the original: the numbered section headings (their core, before any colon),
every fenced code block, every <svg> block, every table cell value, and length (the rewrite may
not be longer). Prose rules: no sentence over max_words; none of the banned patterns; no
em-dash form; no term of art used before a defining cue; no percentage or large count without
a source cue in the same sentence; no markdown heading syntax quoted in prose.

A project config (JSON) overrides any DEFAULTS key. Everything here is a heuristic a reader
would otherwise spend tokens on; false positives are cheaper than the reader re-finding the
class a fifth time. Exit 1 on any problem.
"""
import json
import os
import re
import sys

DEFAULTS = {
    "max_words": 30,
    "beats": 12,
    "drill_beats": 7,
    "code_fence": "csharp",
    "require_shorter": True,
    "banned": [
        r"\bobviously\b", r"\beasy\b", r"\btrivial(ly)?\b", r"\bsimply\b", r"\bof course\b",
        r"\b\d+ years of\b", r"\byour ground\b", r"\bsecond nature\b", r"\bknow this cold\b",
        r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
        r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]* \d{1,2}\b",
    ],
    # terms of art the reader has NOT been taught; the first prose use must sit in a sentence
    # with a defining cue. A project lists its own.
    "terms": [],
    "definition_cues": [r"\bis\b", r"\bmeans\b", r"\bcalled\b", r"\(", r":", r"=", r"\bthat is\b",
                        r"\bin plain words\b", r"\bdefined\b", r"\bare\b",
                        r"\ban? (?:[\w-]+ ){1,3}(?:is|holds|keeps|walks|stores|hands|gives|returns|pops|counts|tracks)\b"],
    "origin_cues": [r"\bdataset\b", r"\breport", r"\bheader\b", r"\bbeat \d", r"\bmeasured\b",
                    r"\bran\b", r"\brun\b", r"\bcounted\b", r"\btable\b", r"\btest", r"\bfrom the\b",
                    r"\bstatement\b", r"\bconstraint", r"\bexample\b", r"\bthe code\b", r"\bprinted\b",
                    r"\babove\b", r"\bbelow\b", r"\bLC \d", r"\bLeetCode\b", r"\bits own\b", r"\bsource\b",
                    r"^\"", r"\bsays?\b", r"\bsaid\b", r"\banswer", r"\bverified\b", r"\bcompiled\b",
                    r"\bthat is\b", r"\babout\b", r"\bsay\b", r"\bsuppose\b", r"\bimagine\b", r"\bfor example\b",
                    r"\bdivide\b", r"\btimes\b", r"\bplus\b", r"=", r"\^", r"\bwindow\b", r"\bcapacity\b",
                    r"\bdefault\b", r"\bcrash", r"\bgrid\b", r"\bminutes? is\b"],
    "number_pattern": r"\b\d+(?:\.\d+)?%|\b\d{1,3}(?:,\d{3})+\b|\b\d{3,}\b(?! ?(?:ms|px|pt|s\b))|\b\d+ (?:mentions|reports|entries|candidates|cases)\b",
    # sections that must OPEN with an everyday picture (catalog C09/C18): section numbers + the cue
    # a picture sentence carries. Empty list = no check. The picture must appear within the first
    # `picture_window` characters of the section's prose.
    "picture_beats": [],
    "picture_cues": r"\b(Picture|Imagine|Think of|Suppose|Say you|Say there)\b",
    "picture_window": 900,
    # a unit must state its own time cost near the top, so a plan can derive chips from it (C14)
    "require_time_line": None,   # e.g. r"Reading time: about \d+ minutes"; None = no check
}

CODE_RE_T = r"```%s\n.*?```"
SVG_RE = re.compile(r"<svg\b.*?</svg>", re.S)
BEAT_RE = re.compile(r"^## (\d+)\. .+$", re.M)


def load_config(path):
    cfg = dict(DEFAULTS)
    if path:
        with open(path, encoding="utf-8") as f:
            cfg.update(json.load(f))
    return cfg


def prose_only(text, cfg):
    text = re.sub(CODE_RE_T % cfg["code_fence"], " ", text, flags=re.S)
    text = SVG_RE.sub(" ", text)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^\|.*$", " ", text, flags=re.M)
    text = re.sub(r"^#{1,6} .*$", " ", text, flags=re.M)         # headings are not prose
    text = re.sub(r"`[^`]*`", "code", text)                     # inline code FIRST: a bare <= is not a tag
    text = re.sub(r"</?[A-Za-z][^>]*>", " ", text)              # real tags only
    return text


def sentences(text):
    """A blank line, a bullet, a heading or a bold label ends a unit; punctuation inside a line ends one only at . ! ?"""
    out = []
    for block in re.split(r"\n\s*\n|\n(?=\s*(?:[-*>]|\d+\.|#))", text):
        flat = re.sub(r"\s+", " ", block).strip(" >-*#")
        parts = re.split(r"(?<=[.!?])\**\s+(?=[A-Z\"'(*`])", flat)   # a colon or semicolon joins, it does not end
        out.extend(p.strip() for p in parts if len(p.strip()) > 1)
    return out


def table_values(text):
    vals = []
    for line in text.splitlines():
        if line.startswith("|") and not re.match(r"^\|[\s\-:|]+\|$", line):
            vals.append([c.strip() for c in line.strip("|").split("|")])
    return vals


def check(path, orig=None, cfg=None, drill=False):
    cfg = cfg or DEFAULTS
    problems = []
    new = open(path, encoding="utf-8").read()
    heads_new = [m.group(0) for m in BEAT_RE.finditer(new)]
    want = cfg["drill_beats"] if drill else cfg["beats"]
    if len(heads_new) != want:
        problems.append("section headings: found %d, expected %d" % (len(heads_new), want))
    prose = prose_only(new, cfg)
    sents = sentences(prose)
    long_ones = sorted(((len(s.split()), s[:110]) for s in sents if len(s.split()) > cfg["max_words"]), reverse=True)
    for n, s in long_ones[:8]:
        problems.append("sentence of %d words (max %d): %s..." % (n, cfg["max_words"], s))
    if len(long_ones) > 8:
        problems.append("...and %d more sentences over %d words" % (len(long_ones) - 8, cfg["max_words"]))
    for pat in cfg["banned"]:
        m = re.search(pat, prose, flags=re.I)
        if m:
            problems.append("banned: %r" % m.group(0))
    for form in ["—", "&#8212;", "&mdash;", "&#x2014;"]:
        if form in new:
            problems.append("em-dash form present: %r" % form)
    if re.search(r"(?<!`)## ?\d", prose):
        problems.append("markdown heading syntax quoted in prose ('## N'): say what the reader sees")
    if cfg.get("require_time_line") and not drill and not re.search(cfg["require_time_line"], "\n".join(new.split("\n")[:8])):
        problems.append("no time-cost line in the first 8 lines (expected %r)" % cfg["require_time_line"])
    # a list flattened into one line renders as a wall (C24): three or more " - " item separators on one line
    for line in new.split("\n"):
        if not line.startswith(("|", "```", "<")) and len(re.findall(r"\s-\s(?:`|\*\*)", line)) >= 3:
            problems.append("flattened list on one line (%d items): put each item on its own line: %s..." % (len(re.findall(r"\s-\s(?:`|\*\*)", line)), line[:80]))
    # a bullet list glued to the paragraph above it renders as one wall (C24, second form): the
    # markdown converters in use need a blank line before the first "- " item
    lines = new.split("\n"); in_code = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            in_code = not in_code
        if in_code or i == 0:
            continue
        prev = lines[i - 1]
        if re.match(r"\s*[-*] ", line) and prev.strip() and not re.match(r"\s*[-*] ", prev) and not prev.startswith(("|", "#", ">")):
            problems.append("list glued to the paragraph above it (needs a blank line before): %s..." % line[:60])
    # ordinal-position phrases go stale whenever a unit moves between days (C25)
    m = re.search(r"\b(First|Second|Third|Fourth) (problem|unit) (of the day|today|of the day's plan)\b", "\n".join(new.split("\n")[:8]))
    if m:
        problems.append("ordinal plan phrase in the header (%r): it goes stale when the unit moves; name the day only" % m.group(0))
    # required opening picture (catalog C09 / C18): the section's first prose must carry a picture cue
    for beat in cfg.get("drill_picture_beats", []) if drill else cfg.get("picture_beats", []):
        m = re.search(r"^## %d\. .*$" % beat, new, re.M)
        if not m:
            continue
        nxt = re.search(r"^## \d+\. ", new[m.end():], re.M)
        body = new[m.end(): m.end() + (nxt.start() if nxt else len(new))]
        head = prose_only(body, cfg)[: cfg.get("picture_window", 900)]
        if not re.search(cfg["picture_cues"], head):
            problems.append("section %d has no everyday picture in its opening (no %s within %d chars)"
                            % (beat, cfg["picture_cues"], cfg.get("picture_window", 900)))
    # term before definition (first prose use must carry a defining cue)
    cues = [re.compile(c, re.I) for c in cfg["definition_cues"]]
    for term in cfg["terms"]:
        for i, s in enumerate(sents):
            if re.search(r"\b%s\b" % re.escape(term), s, re.I):
                # a short label ("Memo.") takes its definition from the sentence that follows it
                window = s if len(s.split()) > 6 else s + " " + (sents[i + 1] if i + 1 < len(sents) else "")
                if not any(c.search(window) for c in cues):
                    problems.append("term %r first used without a definition: %s..." % (term, s[:100]))
                break
    # number without origin
    numpat = re.compile(cfg["number_pattern"])
    ocues = [re.compile(c, re.I) for c in cfg["origin_cues"]]
    seen_numbers = set()
    for s in sents:
        for m in numpat.finditer(s):
            num = m.group(0)
            if num in seen_numbers or re.match(r"^(19|20)\d\d$", num):
                continue
            seen_numbers.add(num)              # only a number's FIRST use needs its origin
            if not any(c.search(s) for c in ocues):
                problems.append("number %r with no origin at its first use: %s..." % (num, s[:100]))
    # frozen parts versus the original
    if orig:
        old = open(orig, encoding="utf-8").read()
        core = lambda h: h.split(":")[0].strip()
        if [core(h) for h in heads_new] != [core(m.group(0)) for m in BEAT_RE.finditer(old)]:
            problems.append("section headings differ from the original (the numbered core is frozen)")
        code_re = re.compile(CODE_RE_T % cfg["code_fence"], re.S)
        if code_re.findall(old) != code_re.findall(new):
            problems.append("code blocks differ from the original; they are frozen")
        if SVG_RE.findall(old) != SVG_RE.findall(new):
            problems.append("svg block differs from the original; it is frozen")
        missing = sum(1 for row in table_values(old) for cell in row[1:]
                      if cell and cell not in new and not re.match(r"^[-A-Za-z ]+$", cell))
        if missing:
            problems.append("%d table cell values from the original are missing (values are frozen)" % missing)
        if cfg["require_shorter"] and len(new) > len(old):
            problems.append("rewrite is LONGER than the original (%d > %d chars); it must be shorter" % (len(new), len(old)))
    return problems, new


def selftest():
    bad = ("# WALKTHROUGH 99 - Test\n\n" + "".join("## %d. T%d\n\nShort.\n\n" % (i, i) for i in range(1, 13))
           + "This sentence is deliberately padded with many many extra words so that it runs well past "
             "the thirty word ceiling that the gate enforces for plain prose everywhere on every page in "
             "this whole library tonight. Obviously fine. Pop the heap twice. We saw 23.8% of them. "
             "See the section headed ## 9.\n\n**Name key.** - `a` = one - `b` = two - `c` = three - `d` = four\n"
             "**Legend.**\n- `x` = glued\n")
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_check_plain_selftest.md")
    open(p, "w", encoding="utf-8").write(bad)
    cfg = dict(DEFAULTS); cfg["terms"] = ["heap"]; cfg["picture_beats"] = [7]
    try:
        probs, _ = check(p, cfg=cfg)
    finally:
        os.remove(p)
    want = ["sentence of", "banned", "term 'heap'", "number '23.8%'", "markdown heading", "section 7 has no everyday picture", "flattened list", "list glued"]
    for w in want:
        assert any(w in x for x in probs), (w, probs)
    print("SELFTEST PASSED (%d classes caught)" % len(want))
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if not argv:
        sys.exit(__doc__)
    path = argv[0]
    orig = argv[argv.index("--orig") + 1] if "--orig" in argv else None
    cfg = load_config(argv[argv.index("--config") + 1] if "--config" in argv else None)
    probs, new = check(path, orig, cfg, drill="--drill" in argv)
    for p in probs:
        print("FAIL:", p)
    longest = max((len(s.split()) for s in sentences(prose_only(new, cfg))), default=0)
    print("%s: %d chars, longest sentence %d words" % (os.path.basename(path), len(new), longest))
    print("PASS" if not probs else "FAIL (%d problems)" % len(probs))
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
