---
name: guarding-silent-failures
description: Use when an operation can fail while still returning valid-looking output - CAD/geometry booleans, image and mesh pipelines, renderers, cleanup and migration scripts, bulk edits, data transforms - or when writing the check that is supposed to catch such a failure. Also use when a test, grep, audit or probe comes back clean and that clean result is about to be trusted, when a fix "worked" but nothing visibly changed, and whenever choosing between fixing a magic number and installing an assertion.
---

# Guarding silent failures

Two halves of one problem, and they compound:

1. **The system fails without saying so.** It returns a valid object, exits zero, renders
   plausibly — and is wrong.
2. **The check you wrote to catch that cannot see it.** It reports clean because it is blind,
   not because the thing is fine.

A silent failure plus a blind check is indistinguishable from success, all the way to the
customer / the printer / production.

## Spotting a silent-failure mode

Ask: **if this went wrong, what would tell me?** If the honest answer is "it would look fine",
you are in this territory. Strong signals:

- The operation returns a *typed* result (a solid, an image, a dataframe) rather than a status.
  Type-correct is not value-correct.
- The library is a native/geometry/optimising kernel — OCC, mesh booleans, offsets, GPU passes.
  These are full of "valid but wrong".
- The output is judged by eye, and the eye has no reference to compare against.
- The failure would show up as *absence* (something missing, nothing drawn, zero rows) — absence
  reads as "nothing to report".

**Worked:** a 0.6mm edge fillet on an ellipse-based part consumed **1890mm³, 38% of the object**,
returned a perfectly valid solid, exported without complaint, and rendered as a plausible
keychain. Nothing in the build output was red. The only thing that caught it was a volume
predicted *before* the build.

**Worked, the absence case:** a cut that removed **0.0 mm³**. The cutting tool was built from
overlapping shapes in one call, which quietly corrupted it; the boolean then succeeded, returned
a valid solid, exported cleanly, and left the volume untouched. Two consecutive design changes
produced byte-identical volumes before anyone noticed — *that* coincidence was the only tell.
An operation that removes, adds, replaces or migrates has a failure mode of **doing nothing**,
and doing nothing raises no error anywhere. Any such call gets a before/after delta asserted
against a rough expectation, computed from geometry rather than from the last run.

## Predict the number before you run it

The cheapest possible detector. State the expected value **in advance**, then compare.

A prediction made afterwards is fitted to whatever came out and cannot fail. Made in advance it
is a real test, and it costs one sentence.

This also catches the inverse — a fix that "worked" and did nothing. SSAO ambient occlusion was
wired up, ran without error, and produced almost no occlusion, because its `min/maxDistance` are
*normalised* depth (a fraction of `far - near`) and the camera's far plane was 50× the model. The
numbers looked reasonable; the units were wrong.

## Guard the invariant, not the number

When you find the value that makes it work, you have not fixed anything — you have found a value
that works *today*. Ask what INVARIANT the failure violated, and assert that.

```python
before = part.val().Volume()
part = part.edges(">Z or <Z").fillet(EDGE_ROUND)
removed = before - part.val().Volume()
assert removed < MAX_REMOVED, (
    f"the fillet removed {removed:.1f}mm3, expected about 21 - the junction has gone acute"
)
```

`ARCH_INSET = 1.5` was luck. The assertion is the fix: it survives someone changing an unrelated
parameter two months later, and it names the cause in the failure message.

Corollary: **prefer the check that fails LOUDLY.** Where a value sits near a limit but the failure
mode raises an exception (rather than quietly mangling output), sitting near the limit is safe —
the build stops. Reserve the margin-hunting for the silent ones.

## A DERIVED count drifts; a COUNTED one cannot

If a quantity is countable by looking — flutes on a wall, columns in a report, retries in a
log — treat it as a **measurement**, not something to compute.

Deriving it hides two failures at once. `n = round(run / pitch)` silently rounds to the wrong
integer, and then it *re-derives* every time anything upstream changes, so a value that was
right yesterday quietly becomes wrong when an unrelated margin moves. Both look like arithmetic
working correctly.

Measured on a fluted wall: `round(run / pitch)` gave 11. The object has 10, which the person
holding it counted in about two seconds and which re-measuring the photograph then confirmed
exactly. The pitch was right the whole time; the count was never a question the arithmetic
should have been answering.

**Apply:** make the count the input and let the extent follow from it. If it must be derived,
assert it against an independently observed value, and print it every run so a drift is visible
rather than inferred.

## Silent failure needs a DEFAULT, not a feature

If the failure is invisible, shipping the detector as an option someone must discover is not
enough. A raised feature was unreadable in a 3D viewer because a flat top and the flat floor it
sits on have identical normals — no light can shade them differently. The fix (edge outlines)
was made the **default**, not a checkbox to find, precisely because the failure it prevents is
silent.

## Prove the check can fail

Before trusting a clean result, make the check produce a FAILURE on a case you know is bad. If
you cannot make it fail, you have not got a check.

Failure modes to look for in your own probe:

- **A filter that matches nothing and reports success.** A cleanup printed
  `removed 12 stale files` while its filter silently matched zero, because the "removed" message
  was unconditional. Re-listing the directory found all twelve still there. *Print what you
  actually touched, not what you intended to.*
- **A test blind to the very type it hunts.** A probe for hairline seams filtered edges by
  `boundingBox.zmax - zmin < 1e-7`. OCC pads bounding boxes for spline geometry, so curved edges
  can never pass that test — and the hunt was for curved edges. It returned zero. The tell was in
  the output: the results contained only `LINE` and `CIRCLE`, never the spline types being looked
  for. **If a result set is missing the category you are searching for, suspect the filter.**
- **A selector that silently falls through.** `document.getElementById('tele')` (the element is
  `telemetry`) hit a fallback path that happened to return plausible text, which read as a frozen
  readout and nearly became a bug report about the wrong subsystem.
- **A stale instrument.** Prove the instrument is LIVE before diagnosing the system: do one real
  interaction and confirm the readout moves. Knowing this rule does not prevent it — the same
  trap (a backgrounded browser tab throttling `requestAnimationFrame`, so a polled readout froze
  while the feature worked) recurred months later *with the rule already written down*. What
  prevents it is mechanical: drive a **synchronous** update path instead of waiting on a polled
  one, and check the liveness flag (`document.visibilityState`) before believing a negative.
- **A safeguard known only by its name.** `gh pr merge --auto` was reported as "merges when CI
  goes green, so the test gate holds." The repo had no branch protection and no rulesets, so
  "requirements met" was always true and the flag merged on the spot; it landed one second after
  the checks finished, which made it LOOK gated. A red run would have merged identically. Before
  saying something is gated, blocked, or protected, read the config that enforces it (the ruleset,
  the required check, the hook), not the flag or the workflow name. A guard you have only heard
  described is a claim. (2026-09-10)

- **A check that cannot fire on the data you have.** The most dangerous disguise, because
  everything about it looks like a pass. A new overhang-angle check reported "safe" across every
  part in a repo — correctly, because every part was an extruded profile whose walls are all
  vertical, so the warning branches were *unreachable*. A clean sweep and a dead check are
  indistinguishable on that data.

  **Fix: build the fixture that must fail.** Not a unit test of the function — an input chosen so
  that a working check has no choice but to complain. Here: a sphere on a post, whose underside
  sweeps every overhang angle from vertical to straight-down in one continuous surface. All four
  severity tiers appeared, worst included, and only then was the clean result on the real parts
  worth anything. Then delete the fixture; its job was to license one conclusion.

  Ask it as: *what input would make this scream?* If you cannot name one, or the answer is "none
  of our data", the check is decoration.

- **A probe that reaches nothing — the check is sound, your test of it is hollow.** The mirror
  image of every entry above, and it produces a FALSE ACCUSATION rather than a false pass. To
  prove a fit-check could fail, the input constant it "depends on" was reassigned after import
  and the check re-run. It stayed silent, and the check was about to be reported as blind. It
  was not: every value the check actually reads had been **derived from that constant at import
  time**, so mutating the constant afterwards changed no state the check consults.

  **Mutate what the check READS, not what conceptually causes the problem.** In any module where
  constants are derived at load time — `WIDTH = LENGTH / ASPECT`, config resolved once, a cached
  schema — those are two different values, and the gap is silent in both directions: a sound
  check looks blind, and a blind check can look sound. Either poke the derived value directly,
  or `reload()` the module and mutate before derivation runs.

  The tell: **a probe that changes nothing observable.** Before concluding "the check is broken",
  confirm your mutation actually moved a value the check reads. Print it.

## A guard that fires on legitimate content is worse than no guard

Everything above protects against a check that cannot fail. The opposite defect is cheaper to
create and costs more over time: a check that fires *correctly by its own logic* on content that
is supposed to be there. Nobody deletes such a guard. They start ignoring it, and then it is
still running while protecting nothing.

Field case, 2026-08-22. A page-checker was built with a banned-phrase list: several claims that
had been verified false and must never reappear. First run, three hits. All three were legitimate:
the page's own **correction banner** and its **changelog** quote each retracted claim on purpose,
in order to say it was wrong. A fourth near-miss was the *correction itself* ("it is **not** the
only event that can block"), which contains the banned string as a substring of its own negation.

**The rule: a guard must know where its pattern is ALLOWED to appear.** Three shapes, cheapest first:

- **Scope the input.** Strip the regions whose job is to quote the forbidden thing before scanning
  (here: correction blocks and the changelog). This is usually the honest fix, because those
  regions are structurally identifiable, and it keeps the pattern simple.
- **Handle the negation.** `the only event that can block` matches inside `is not the only event
  that can block`. A fixed-width lookbehind (`(?<!not )`) costs nothing and removes a whole class
  of self-inflicted hits.
- **Never loosen the pattern to silence a hit.** That trades a false positive for a false negative,
  which is the failure the guard existed to prevent. Narrow the SCOPE, not the pattern.

**Both halves are required, and they are one test run apart.** Prove the guard fails on real
defects (introduce each one deliberately; four defects, four catches), and prove it stays silent on
the legitimate content that most resembles a defect. A guard verified in only the first direction
gets disabled within a month by the person it was built for, and a guard verified in only the
second direction is decoration.

Related and worth checking at the same time: a warning that fires on 15 unrelated items because a
key was over-normalized trains the reader to ignore the one real hit. Precision in a guard is not
politeness, it is what keeps the guard alive.

## Isolate by ingredient, not by intuition

When something fails only sometimes, build the matrix. A pocket-rim fillet raised
`StdFail_NotDone` on a finished part; each ingredient alone was fine:

| configuration | result |
|---|---|
| plain slab | OK |
| + arch and opening | OK |
| + edge fillet | OK |
| **all three** | **fails** |

The lesson generalises: **a feature can be individually compatible with every other feature and
still fail with all of them.** Pairwise testing would have found nothing. Vary one ingredient at
a time against the full stack.

## Guard the EXITS, not the artefact

The same blindness in a different domain: when something must not escape — a secret, an
unprotected invention, PII, a pre-release asset — the instinct is to mark the *artefact*
dangerous. But an artefact leaves through **paths**, and each path needs its own guard.

A sensitive CAD file was protected by renaming every export with a `PRIVATE_` prefix, so
publishing it took a deliberate rename rather than a habitual drag-and-drop. Real guard, and it
covered exactly one exit. The project's "Checkpoint" button ran `git add -A`, and the file was
untracked — one press would have written it into git history permanently, where removal means a
rewrite. The prefix was irrelevant to that path.

Enumerate the exits and check each: manual copy, `git add -A` from any script or button, an
upload dialog, a **screenshot**, a log entry, a published artefact, a report from a subagent.
Weight by reversibility, not likelihood — guard the irreversible exit first.

Two corollaries:
- **When a general rule meets a sensitive case, surface the conflict rather than silently
  applying either.** A rule said screenshots are versioned because "the picture and the comment
  are each half the design record" — right for the ordinary case, wrong for the sensitive one,
  where a render discloses nearly as much as the source file.
- **Name the contradiction in the config itself.** An ignore rule that deliberately contradicts
  the rule six lines above it reads as an oversight unless it says why it exists.

## Match the guard's BLAST RADIUS to what it actually protects

A guard has two decisions, not one: *what does it detect*, and *how much does it destroy when
it fires*. Getting the second wrong turns a correctness win into a productivity loss, and the
team learns to route around the guard.

A caching layer for expensive CAD art verified its own round trip: write the solid to STEP,
read it back, compare volume and face count before trusting the cache. The first version
`assert`ed. That would have killed a **forty-five-minute** build at its very end — over a
*cache*. The solid in memory was perfectly good; only the bank was suspect. The fix was to
narrow the blast radius, not the check:

```python
if not round_trip_ok:
    step.unlink(missing_ok=True)        # refuse the BANK
    print("!! not banked, rebuilt every time: <reason>")
    return art                          # the BUILD carries on
```

Losing a cache is a slow build. Trusting a bad cache is a wrong part. Only the second is worth
stopping for.

The opposite call, made in the same codebase on the same day, is equally important: a
split-to-objects guard on printed parts **does** refuse the whole export, because there the
artefact itself is the thing that is wrong and shipping it wastes a print.

Ask: *if this fires, what is actually unsafe?* Fail exactly that much — no more, and no less.

### Shape the opt-out so a mistake fails LOUD

A guard that legitimate cases must escape needs an override, and the override's failure mode is
part of the design. Prefer one where a mis-configuration makes the guard **stricter**:

- Default ON, with a named constant as the opt-out (`EXPECT_SOLIDS = 3`, declared in the file it
  describes, next to the reason). New code is guarded without anyone remembering to ask.
- Key the opt-out by NAME, not position. A typo then matches nothing, so the strict default
  applies and the build stops — annoying, visible, safe. Had it matched loosely, the typo would
  have silently disabled the guard.
- Check which way your override fails before you ship it. "Wrong config ⇒ guard off" is the
  same silent-failure shape the guard was written to eliminate.

## An exception is not proof that nothing happened

The other half of "it failed but looked fine": **it failed loudly, and the message described
only the part it noticed.** A traceback feels like a clean abort — the operation did not
finish, so surely it did not do anything. That inference is wrong whenever the operation
destroys before it creates.

**Worked:** a small patch script did `open(path, 'w').write(new_text)` on a 21 KB reference
document. The write raised `UnicodeEncodeError` — an astral-plane emoji had been written as a
surrogate-pair escape (`\uD83D \uDEA9`) instead of `\U0001F6A9`, so the string held two
lone surrogates. The traceback said the text could not be encoded. What it did **not** say is
that `'w'` had already truncated the file to **zero bytes** before the encoder ever ran. The
next command re-ran the patch against the now-empty file and reported
`AssertionError: anchor not found` — a second, entirely misleading error pointing at the patch
logic instead of at the destroyed file. Recovery was possible only because the file happened
to be committed.

**The generalisable shape:** truncate-then-write, delete-then-copy, drop-then-recreate,
`>` redirection, `tar -x` over a live tree. Each has a window where the old thing is gone and
the new thing does not exist yet. An error thrown inside that window leaves the destination in
a state no error message mentions.

- **Read the error for what it claims, not for what you hope it implies.** "Could not encode"
  is a statement about the encoder. It is not a statement about the file.
- **After any failed operation that writes, look at the target before doing anything else.**
  `wc -c`, `git status`, `ls -l`. One command. The misleading second error above would never
  have been raised if the file had been checked first.
- **The fix is structural, not careful.** Write to a temporary path, then rename over the
  target. `os.replace(tmp, path)` is atomic on POSIX and Windows, so a failure anywhere in the
  write leaves the original untouched. Same idea as guarding the exits: make the destructive
  step unreachable rather than remembering to avoid it.
- **Version control is a backstop, not a guard.** It covers only what was committed, and does
  nothing for generated artefacts, untracked files, or anything mid-session.

```python
tmp = path + '.tmp'
with io.open(tmp, 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_text)          # any failure here leaves `path` intact
os.replace(tmp, path)          # atomic swap
```

**This guard paid for itself the same hour it was written.** The very next patch — the one
adding this section — hit the identical encoding fault, and because it wrote through a temp
file the target survived untouched; only the `.tmp` was zeroed. A structural guard is worth
more than the lesson that produced it.

⚠️ **Related trap, same root cause:** the escape sequences never survived the shell. A heredoc
that looked literal collapsed doubled backslashes, so `\\uD83D` in the source arrived at
the interpreter as `\uD83D` and produced a real lone surrogate. **When file content contains
backslash escapes, do not route it through a shell heredoc** — use a direct file-write tool, or
build the backslash at runtime (`BS = chr(92)`) and substitute a placeholder.

## A formula can be wrong in a direction none of your checks can see

(2026-08-27, a health-data dashboard audited against its own raw records.)

A repo carried `fat mass = 0.69 x weight` for months. The real fit was affine:
`0.693 x weight - 87`. Dropping the intercept made it wrong by ~87 units **at the level**
(it implied 69% body fat where the truth was 28%) while staying **exactly right for
changes**, because the intercept cancels in a subtraction.

It survived every review because **every check anyone had ever run on it was a delta check.**
The verification in the notes literally read "Δweight +2.5, Δfat +1.7, 0.69 x 2.5 = 1.7 ✓".
That check cannot fail no matter how wrong the intercept is.

- **Ask of any load-bearing formula: what class of check would this pass even if it were
  wrong, and has every check so far been that class?** Then run one deliberately outside it.
  For a linear relation the two classes are *level* and *slope*: if you have only ever tested
  on differences, evaluate it once at a single real point. It takes seconds.
- **A clean check history is evidence about your checks, not about the formula.** The longer a
  number has "held up," the more selected the surviving checks are for insensitivity.
- Same family, same run: **a one-sided threshold used to select "typical" cases recruits the
  outlier as evidence for the norm.** Selecting logged days `>= 2000` to characterise a normal
  day swept in a documented binge at 3,020, and the sentence built on it then cited the binge as
  proof of normality. **Bound both ends, and name what you excluded** where the reader can see it.
- And: **deduplicate before you aggregate.** A mean over raw rows double-counted repeat
  measurements taken seconds apart, silently weighting those days twice. The tell was that the
  same document *argued in prose* that a repeat inside a session is one reading. **When an
  artefact states a methodological rule, grep its own computations for violations of it** — that
  contradiction is invisible to every reviewer reading only the prose.

## An aggregate metric can read 100% while the decision it stands for reads 0%

(2026-09-07, a linter built to predict document-layout defects before rendering.)

The tool simulates a typesetter's greedy line wrap and asks one question: **is a paragraph's last
line a single stranded word?** It passed its own selftest. It passed a negative control against
every existing document. It shipped.

Then a second, independent instrument refused a document the linter had just called clean.

Measured against 269 real paragraphs extracted from 12 rendered PDFs:

| tolerance | line-count agreement | **real defects caught** | false alarms |
|---|---|---|---|
| as shipped | **269 / 269** | **0 of 3** | 0 |
| +2pt | 269 / 269 | 2 of 3 | 0 |
| +3pt | 268 / 269 | **3 of 3** | 1 |

**Line-count agreement was perfect and recall was zero, at the same time.** The simulation was
systematically about one word conservative on every line, from measuring text read back out of a
PDF (roughly 0.7% wide) rather than measuring it the way the renderer does. A bias that is
*consistent* does not move a count: every line broke one word early, so the number of lines came
out right and the position of the last break came out wrong. The defect lives entirely in the
quantity the count throws away.

- **Write the confusion matrix for the decision the guard actually makes**, not for a quantity
  that correlates with it. Real defects caught, false alarms raised. Everything else is a comfort
  metric, and a comfort metric that reads 100% is worse than no metric because it ends the inquiry.
- **Ask what the guard's output is a THRESHOLD on**, then test at that threshold. Here the count
  was an aggregate and the decision was a boundary; agreement on the first is nearly uninformative
  about the second.
- **Calibrate against rendered output, not against the constants in the source.** The geometry
  derived by reading the renderer's own configuration was exactly right (frame widths verified to
  the point against the PDFs) and the model built on it was still biased, because the bias entered
  through the measuring function, not the parameters.
- **Choose the error direction on COST, and say the cost out loud.** A false alarm here costs one
  look at a sentence; a miss costs a full render-and-check round, which is the entire reason the
  tool exists. That makes 1 false alarm in 269 the correct price for full recall, and it is the
  opposite of the tidy choice.

**Sibling failure in the same session, worth stating separately: an exclusion written for one case
silently covers every case that shares its shape.** The independent gate skipped single-word lines
where `text.isupper()`, intended to ignore a section heading called `EDUCATION`. It therefore also
ignored **acronym** orphans (`CSS3`). A second exclusion, `len(text) > 3`, ignored **short**
orphans (`40%`). Both were real defects sitting in finished, ready-to-send documents, and both
surfaced only because a second instrument disagreed with the first. **When you write an exclusion,
name the case it is for in a comment and then ask what else matches that predicate.**

## Your own repair can carry the bug it repairs, one abstraction level up

(2026-09-08, two files flipped in one session by the logic written to stop the flip.)

A known hazard: reading a text file with a helper that normalises line endings, then writing the
result back as bytes, silently rewrites every line in the file. It is documented, it is understood,
and it was hit anyway on a 1,734-line configuration file **while writing the section about
preventing mistakes.**

The second hit is the one worth keeping. The fix written in response detected the file's ending
with, in effect, `use CRLF only if EVERY line is CRLF`. The next file was mixed (1,533 CRLF plus 9
stray LF from some earlier edit), the unanimity test failed, and it flipped 1,552 lines.

- **A guard derived from a clean mental model meets files that are not clean.** Real artefacts are
  mixed: mixed endings, mixed encodings, mixed conventions. **Detect by majority, never by
  unanimity**, and treat "all of them agree" as a claim to verify rather than a shape to assume.
- **Print the invariant on both sides of the write.** Both slips were visible within one second
  purely because the patch script printed before/after counts of each ending. The measurement cost
  nothing and was the entire difference between a caught defect and a silent 1,700-line diff.
- **This is the same shape as the guard carrying the bug it exists to catch (above), moved one level
  up: the REPAIR carried the bug the repair was for.** When you write a countermeasure immediately
  after being burned, that code is written under the same assumptions that produced the burn. Run it
  against the ugliest real input you have, not against the clean case you were just thinking about.

## A record with two arrival paths defeats a check that reads one

A guard can be correct, tested, and quietly covering half its population, because you asked
whether the LOGIC was right and never asked what the INPUT set actually contains.

A duplicate-detection check keyed on a requisition id parsed from a job posting file. It had
worked all week, and it had just caught a real duplicate that morning. It then reported **NEW** for
a job the user had already applied to: same requisition, same title, same salary band.

**The cause was not the logic. It was an arrival path nobody had enumerated.** That application
had been submitted through the EMPLOYER's own hiring system rather than the job board, so the
board id for it existed nowhere on disk, and every future re-posting of that requisition on any
board would read as brand new forever. An entire population was invisible.

The same codebase had already suffered the identical shape a day earlier: records in one state
stored their source in a differently-named file, so the id parser returned nothing for all of them.
Two instances, same question unasked.

⚙️ **Ask of every guard: what are ALL the ways a record of this kind gets created, and does the
check read every one of them?** Enumerate the paths, not the logic. A guard that reads one path
is not wrong, it is scoped, and nothing in its output tells you where the scope ends.

⚙️ **The fix should widen the input, not add a special case.** Here: any record may now declare
extra ids with an explicit marker line, read from every file type a record can carry. That covers
the known gap and the next one, instead of hard-coding the employer-system case.

⛔ **A false NO is worse than a false YES.** A false yes gets investigated. A false no ends the
search and looks exactly like an all-clear.

## An artifact must satisfy the rule it publishes

A standards page was written to stop a recurring defect. Its build checklist told the reader to
grep any finished page for three specific phrases, and to treat a page missing all three as
unfinished.

**The page itself failed that grep.** One of the three phrases had wrapped across a line in the
page's own markup, so the check it published returned nothing on the file that published it. An
assertion caught it before the file was ever written; no human review would have, because the
prose read as authoritative and the rule read as obviously satisfied.

Worse, the published rule was itself wrong: it said to grep, and a plain grep dies on a line wrap.
So the artifact carried a check that could not do its job, aimed at a page that could not pass it.

⚙️ **Whenever you write a rule INTO an artifact, run that rule against the artifact before
shipping.** It costs one command and it is the cheapest possible test of whether the rule is
executable at all.

⚙️ **And read the rule as an implementer would.** "Grep for X" is a specification. If X can wrap,
contain an entity, or vary in case, the specification is incomplete and every future reader will
inherit the incompleteness. Say "grep whitespace-normalized", or ship the command.

📌 A checklist inside a document has the same borrowed trust as a verification artifact: it looks
like the checking already happened.

## A control that is too easy proves nothing

(2026-09-08. Three guards in one day passed a control that could not fail, and each shipped its real
failure mode untested.)

- A freshness checker was proven able to reject a folder titled "Underwater Basket Weaver". It could
  not tell **"Senior Software Engineer, Backend" from "LEAD Software Engineer, Backend" at the same
  company**, and reported twelve live matches of which roughly five were real, four were sibling
  postings, and three were nonsense.
- A batch transform asserted that the string it removed was gone and that it had introduced no
  forbidden character. Both true. It had also **deleted the name, contact line, summary and skills**
  from nine documents.
- A layout linter matched the renderer's line counts 269 times out of 269 and caught **none** of the
  three real defects it existed to find.

**A test proves only what it DISCRIMINATES.** A control that is obviously different from a real
defect is free to pass, so passing it carries no information. **Choose the control that is the
NEAREST thing the guard could confuse**: the sibling case, the off-by-one-level case, the
same-shape-different-meaning case. If the control is easy, it is decoration.

**Assert what must SURVIVE, not only what CHANGED.** This is the second half and it is the one that
bites hardest on transforms. Checking your own edit tells you nothing about the collateral. Add
invariants for the things whose loss would be catastrophic and silent: the document still contains
its identifying header, the required sections are still present and still the same count, the file
did not shrink by more than a small margin. In the case above, the size check alone would have
caught it in one second: the damaged files went from 8,000 characters to 4,400.

**Snapshot before the first write on any batch transform.** The recovery above cost five minutes
instead of a day purely because sixteen originals had been copied aside first, by convention rather
than by foresight.

⛔ **And a guard that answers NO wrongly is worse than no guard.** The same day, an employer-history
check reported "NO history" for a company with four records on file, because its name-normalising
function split camelCase on a lowercase-to-uppercase boundary only and therefore never split an
ACRONYM followed by a word. **33 employers were silently invisible** to a check that had caught a
real duplicate hours earlier, which is precisely why nobody doubted it. A false NO ends the search;
a false YES at least gets investigated.

## A written record is a measurement with no expiry date

(2026-09-08. Four recorded claims failed in a single day, in both directions.)

A fact gets checked once, written down, and from then on it is inherited rather than re-examined,
because the writing itself reads as the check having happened. **Nothing in a corpus expires on its
own and nothing announces that it has gone stale.** Worse, the confidence a note carries tracks its
AGE rather than its accuracy, and it runs the wrong way: the older a note is, the more settled it
feels and the less likely anyone is to test it.

In one day, four notes in a long-running collaboration were found wrong:

- A capability recorded as "a worked design, not deployed" had in fact **shipped**, so a true and
  valuable claim had been suppressed from every document for a month.
- A hard constraint ("there are no paying clients") that justified banning two words turned out to
  rest on a **false premise**, so a true word had been banned.
- A phrasing the collaborator had personally approved months earlier was, on re-reading, **not true
  of him any more**, and was about to ship in a document.
- A job requisition retired on **five agreeing "dead" signals** was open the whole time.

- **A record that BLOCKS something deserves more scrutiny than one that PERMITS something.** A block
  is silent. Nobody notices the sentence that was never written, the claim that was never made, the
  option that was never considered, so a wrong block can persist indefinitely with zero feedback.
  Three of the four above were blocks.
- **Agreement between sources that share a failure mode is not corroboration.** The retired
  requisition died on five signals that were all downstream job boards, each with its own expiry
  clock, none of them the employer. Before counting agreeing sources, ask how they could all be
  wrong together.
- **The counter is asking the person, not building another instrument.** All four were caught by the
  human: two volunteered, two from a direct question. **Zero were caught by a script**, and three
  new guards were written that same day. Instrumentation catches drift in things you compute. It
  cannot catch decay in things you were told.
- **When a record is corrected, supersede it in place and date it, the same hour.** Do not delete:
  the wrong version is evidence about how the error propagated, and a reader who half-remembers the
  old claim needs to see it explicitly retracted rather than silently absent.

## A stated intention is an artefact that looks like the work

(2026-09-08, the mechanism named by a human collaborator who had solved it for themselves
years earlier.)

A turn of work ended with the sentence "Building the three now" and no build. The more instructive
repeat came next: the following turn opened by correctly stating "I did not build the three", and
then did something else. **Naming the omission did not reinstate it.**

Their account, from lived experience: announcing what you are about to do delivers
part of the feeling of having done it, so the drive to actually do it drops and the item gets
skipped. His countermeasure is a habit, not a reminder: **do not say you are doing a thing, or
nearly done with it, until it is done.** Nobody needs the announcement before the result anyway, so
it buys nothing and costs the follow-through.

- **The hazard is the UNACTIONED announcement, not narration.** A sentence of intent immediately
  followed by the action is safe: nothing sits in the gap, because there is no gap. Past tense about
  finished work is safe. A *conditional* offer at a stopping point ("say the word and I will") is
  safe and is the right way to end. The dangerous form is declarative, first person, future tense,
  with nothing after it.
- **Prefer a gate on the ARTEFACT over a gate on the SENTENCE.** The tempting fix is a hook that
  scans outgoing prose for intent language. It fires on every honest handoff, and a noisy check
  trains you to ignore it (see above). The fix that paid was re-running the job's own opening
  inventory as a CLOSING gate: every item in a batch must end as a built thing, a recorded
  rejection, or a recorded deferral. It exited non-zero and named **24 decisions that existed only
  as sentences** in a report, which no prose check could have found.
- **The general shape: any inventory taken at the start of a batch can be re-run at the end as a
  completeness gate, for free.** You already wrote the hard part. Inverting its pass condition turns
  "what is new?" into "what did I fail to resolve?".



When a factual claim is retracted, the instinct is to fix the artefact in front of you, announce
the correction, and move on. That fixes one *instance*. The claim is a **population**: every copy
already written to disk still carries it, and nothing about the announcement reaches them.

Measured, three times in one workspace: a corrected number was fixed in the new batch and left
standing in two older staged documents; then a retracted provenance claim ("hand-wrote X") was
still sitting in three artefacts **three weeks after** the retraction, one of which shipped to its
recipient hours before it was caught.

**The hand-search does not close this, and the reason is structural.** Each manual sweep re-picks
which spellings to look for, so each sweep re-earns its own blind spot. Three separate greps for
`hand-wrote` all came back clean while `hand-written` sat untouched in three files, because no
sweep happened to choose that form. Adding the retraction to a mechanical guard surfaced **six**
carriers on its first run.

- **When a claim is retracted, add it to the guard in the same hour.** Not to a memo, not to a
  memory file, not to a checklist. To the thing that runs and refuses.
- **Enumerate the variants at guard-writing time**, when you are thinking about the claim:
  hyphenated, unhyphenated, past tense, participle. The guard searches them all forever; you will
  not.
- **Sweep the whole population, not the new batch.** The carriers are, by definition, in the old
  material nobody is currently looking at.

### The guard will carry the bug it exists to catch

The banned-phrase check above matched **case-sensitively**, so `hand-wrote` could never have
matched `Hand-wrote` at the start of a bullet. That is exactly the failure class the guard was
written to prevent, living inside the guard. A tool that checks for a family of mistakes is
written by someone thinking about that family, which is precisely the state in which you stop
checking yourself.

**So negative-test every guard before believing it**, and include *negative controls* — inputs
that must stay clean. A guard that flags everything is indistinguishable from a guard that works,
until it costs you a correct sentence. The check that shipped here runs ten cases, three of which
assert the *correct* phrasing is NOT flagged.

### Corollary: a noisy check trains you to ignore it

A leakage scan for cross-company names returned 44 hits on 45 documents. Every one was the word
"Salesforce" appearing as a genuine skill. A check with that signal-to-noise ratio does not get
tuned, it gets dismissed — and the next time it fires for real, it is dismissed too. Whitelist the
known-good before the check goes into anyone's routine.

## The order to work in

1. Ask what would tell you if this were wrong. If nothing would, stop and add something.
2. State the expected number before running.
3. On a mismatch, diagnose by measuring the real artefact — not by re-reading the code.
   **If the mismatch was an exception from something that writes, look at the target file
   first** — the error described the failure, not the damage.
4. Fix the cause, then assert the invariant so it cannot return silently.
5. Prove the assertion fires: break it on purpose once — and if your real data cannot make it
   fire, build the fixture that can.

## Provenance

Extended 2026-08-19 with the truncate-then-fail case: a `UnicodeEncodeError` mid-write that
emptied a 21 KB document, a second misleading `anchor not found` error on the retry, and the
shell-heredoc backslash collapse that caused the encoding fault in the first place.

Distilled 2026-08-09 from a peckworks-cadmesh session that hit all of these in one day: a fillet
that ate 38% of a part and rendered fine, an AO pass that rendered pure black with no console
error (a missing `RenderPass` meant AO was multiplied over an empty buffer), an AO pass that then
"worked" and did nothing (normalised-depth units), a ridge probe that was blind to splines, a
cleanup that reported removing twelve files it had not touched, and a build check that was flaky
because `publicDir` copied 15MB of models into `dist/` on every run. Related skills:
[cadquery-modeling] for the geometry-specific traps, [look-driven-iteration] for output judged by
eye, [nemesis-review] for adversarial review before committing.
- 2026-09-02: a new plain-prose gate's first sweep returned 70 hits, 59 of them the gate's own artifacts (headings counted as prose, a bold label split from the definition after it, "1,000" read as "000", a number re-flagged at every reuse after being sourced once). Positive-testing the guard before queuing human work on its output saved a 59-item false fix list. The same day four of the orchestrator's own scripted fixes failed while printing success and were caught only by gates written for other reasons.

## Field case: an attribute is not a state (2026-09-09)

A slide-out panel's body had `hidden` set and the acceptance recorded `bodyHidden: true`, and
the panel rendered OPEN, because an author rule `section.tool { display:flex }` beats the UA
`[hidden]`. The check measured the attribute the code set, not the effect the user sees; it
could not fail. Rule: prove a UI state by its computed effect (`getComputedStyle(el).display`,
a bounding rect, a pixel), never by the flag that was supposed to produce it. Same family: a
dock "fit" measured with three hint lines EMPTY (0 px each under `:empty{display:none}`) passed
a panel that overflowed once they were populated; populate every state line, then measure.
Both found by reviewers who asked "what would this check look like if the thing were broken?"

## Field case 2026-09-10 — an instrument blind to its own first write

`nothing_lands_under_projects` snapshotted the tree in case 5 — after case 1 had already
written `__pycache__/model.pyc` beside the model. The check passed on every run while the
law it enforced ("a preview writes nothing under projects/") was false. Two lessons: (1) take
the BASELINE before any action in the process, not before the case; (2) the fix was proven by
making the test fail on purpose (comment out `sys.dont_write_bytecode`, watch red, restore,
watch green) — a guard that has never been red has not been tested. Same night, the other
direction: a literal 50 ms poll "z==7 && spinner hidden && slider==3" counted 160 samples of a
LEGITIMATE state (the first build truthfully shown, spinner already run, second build queued);
the per-swap MutationObserver that asked the real question ("was a spinner shown for THIS
landing") found 0. An instrument can also be wrong by counting the truth as a failure — write
the question the check answers, then check the check answers it.

