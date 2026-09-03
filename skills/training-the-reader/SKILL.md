---
name: training-the-reader
description: Use when a teaching or study artifact must get plainer across repeated cold reads; when the same reader stalls keep recurring page after page (a term used before it is defined, a number with no origin, a 40-word sentence, a picture that decorates instead of carrying the mechanism); when a rewrite must keep code, figures and tables frozen while only the prose changes; or when cold reads and Feynman-style rewrites are being delegated to cheaper models and each read should start from what the last one found instead of re-deriving it.
---

# Training the Reader

## Overview

The reader's intelligence lives in a file, not in a model. Every cold read starts by reading the
defect catalog, every read ends by appending to it, and any defect class seen twice is promoted
from a judgment the reader must make to a check a script makes for free. Over time the cheap
model spends its tokens only on what scripts cannot judge: does the everyday picture carry the
mechanism, and would a person have to read this twice.

**REQUIRED BACKGROUND:** superpowers:iterative-lesson-refinement (the reader profile the twin is
derived from) and educational-html-prep (the Feynman page rules). This skill adds the learning
loop those two lack: a catalog that grows, an audit contract that feeds it, a promotion rule.

## When to Use

- The maintainer says a page is "word salad", "verbal insanity", "impossible to learn from".
- A cold read returned findings you have seen on an earlier page.
- Many files must be rewritten plainer with the code, figures and numbers untouched.
- The frontier model's quota is the bottleneck and the words will be READ, not spoken.

Not for: checking truth (use nemesis-review), first-draft authoring, or pages a script can
fully verify.

## The Loop (one file or one page at a time)

| Step | Who | What |
|---|---|---|
| 0 Archive | script | Copy the original beside the target. Every later check diffs against it. |
| 1 Gate | script, zero tokens | `scripts/check_plain.py <file> --orig <original> --config <project.json>`: frozen blocks unchanged, not longer, no sentence over the cap, banned words, term before definition, number without origin, table spacing. `--selftest` first. |
| 2 Read | cheap model | Dispatch from `references/dispatch-templates.md`. The reader reads `references/defect-catalog.md` FIRST, then the page, and reports quote-only findings plus the audit lines. |
| 3 Fix | cheap model | Rewrite prose under the frozen contract; frontier writes only the analogy seeds and verifies corrections. |
| 4 Re-gate | script | Same command. A fix that fails the gate is not a fix. |
| 5 Append | orchestrator | Copy the read's NEW CLASS and RECURRENCE lines into the catalog with the quote. |
| 6 Promote | orchestrator | A class seen twice gets a check in the gate, negative-tested (see guarding-silent-failures). |

## Model Routing

| Work | Model | Why |
|---|---|---|
| Gates, archives, table normalizing, assembly of frozen blocks | script | Zero tokens, never drifts |
| Cold reads with the catalog in hand | cheap (Sonnet-class) | Judgment is adequate once the catalog carries the intelligence |
| Prose rewrites under the gate | cheap | The gate refuses the countable failures; the charter carries the rest |
| Analogy seeds, catalog entries, verifying a correction, the reader model | frontier | Wrong seed or wrong reader model generates a whole class of defects |

## Token Rules (each from a real loss)

- **Write the whole file first, then gate.** A killed agent leaves a finishable file.
- **Assemble by script for anything over ~20 KB.** One 34 KB Write exceeded the output cap.
- **Waves of three or four agents.** A twelve-agent wave died on a five-hour usage limit twice.
- **One read, one write, at most three fix rounds** per file. Never re-read an original.
- **The orchestrator never loads the page.** It reads reports and gate output only.
- After a kill, message the SAME agent first; its transcript persists. Re-dispatch only if that fails.

## The Frozen Contract (the rewrite rule)

Frozen, asserted by the gate: section headings (the numbered core, not a suffix after a colon),
every code block, every figure, every table value, every measured number. Prose is everything
else, and the rewrite must be SHORTER than the original. A bold "say this out loud" line may be
shortened, never lengthened or removed.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Reader re-derives the profile and catalog from scratch each dispatch | Ten-line dispatch pointing at both files |
| Picture opens the section but the code shows a different bug | Reader checks the picture against the broken code's actual line |
| Rewriter adds definitions and blows the length cap | Cut a repeated explanation, never a definition |
| Freezing a heading whose suffix contains a banned word | Freeze `## N. TITLE`; the suffix is prose |
| Gate splitter treats a bullet list or a bold label as one 150-word sentence | Split on blank lines, bullets, bold labels, semicolons; strip inline code before tags |
| A table followed by prose with no blank line renders an extra row | Normalizer inserts the blank line |
| Findings answered, catalog never updated | Step 5 is not optional; the next read pays for it |
| A seed picture handed to a writer as fact | Seeds are hypotheses; the writer checks the picture against the broken code's changed line (catalog C10); four of sixteen seeds were wrong |
| A scripted fix trusted because it printed "ok" | Count-assert every replace, exclude frozen regions, make prose regexes wrap-tolerant, re-run the full gate after each script |
| A new gate wired into a pipeline stage that never sees what it checks | Wire it where the whole artifact exists, then count the cases it must refuse BEFORE trusting the first green build: a done-line gate placed after the builder had peeled the done line off passed ten sheets, eight of which it should have refused |
| A scripted structural edit whose regex treats a markup prefix as text | Anchor the prefix explicitly (an optional `(> ?)?` let `(.*\S)` capture the `>` itself and three labels lost their blockquote), then grep for the damage signature and render one touched page before the gate's PASS is believed; a blank line inside a paragraph is not a gate class |
| A filler trim that lands inside a frozen block | Assert the match sits outside code, svg and tables before replacing; the frozen-svg check caught a five-character trim inside a figure caption |
| The first sweep of a new check trusted | Positive-test the guard: 59 of the first 70 hits were the gate's own artifacts (headings read as prose, bold labels split from their definitions, thousands separators, defined numbers re-flagged) |

## Provenance

- 2026-09-02, born: a 21-walkthrough interview-prep library the maintainer called "verbal insanity" after a
  rebuild had reused it verbatim. Baseline cold reads 7 teach / 5 finish. After the loop: 21/21 files pass
  the gate, ten day pages cold-read by catalog-armed cheap readers (teach 7 to 8, finish 6 to 7; one page
  re-read after fixes moved 5 to 7), a 220k-token picture sweep found eight defects four full reads had
  missed, and eight judgment classes became script checks the same day. Catalog at 37 classes.
- 2026-09-02, the guard guarded its author: four of the orchestrator's own scripted fixes broke files in
  ways that looked finished (a regex ate two time lines, a trim edited a frozen table row, a normalizer
  overran a length ceiling by one character, an example id in a command line inflated every plan chip).
  Every one was caught by a check written hours earlier for a different reason.
- 2026-09-02, second pass: nine pages re-read after fixes by catalog-armed cheap readers on plain-text renders
  (80k-106k tokens per read, about half the HTML cost), each told the previous reads' findings and made to quote
  where each fix landed before scoring. Finish scores reached 7 or 8 on all ten pages (two needed a third read).
  Five new classes (C38-C42); five judgment classes became builder rules the same day (a conditional done line,
  no typed totals, no pronouns, a legend derived from the chips, hub chips synced from the pages). Three of the
  orchestrator's own scripted fixes misfired and were caught by gates or renders, never by their own success
  messages.
