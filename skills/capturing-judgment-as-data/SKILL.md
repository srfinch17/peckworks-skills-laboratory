---
name: capturing-judgment-as-data
description: Use when correctness is a human's opinion rather than something a test can decide - visual or generative output, tone, taste, UX feel, "does this read as natural" - and their verdicts should survive the session. Also use when feedback keeps arriving as comments that cannot be reproduced, when a fix was declared verified against an instrument the human cannot see, when planning to carry learnings into a successor project, or when asked to build an agent that judges or screens output.
---

# Capturing Judgment as Data

**The human is the scarce resource. Everything else is cheap.** Compute is cheap, storage is cheap,
your time is cheap. Their attention is the one input that cannot be scaled, and it is normally spent
once and thrown away: "that looks wrong", acted on, evaporated.

**The goal is an asymptote: drive the number of future human judgments toward zero.** Not by guessing
what they would say, but by extracting so much durable, replayable signal from each interaction that
the same question never has to be asked twice - not in this project, and not in the next one.

Two operations follow from that:

- **Maximize yield per interaction.** Every time they look at something, harvest every atom
  available: their words, the exact state, the vantage, the artifact, the instrument settings, the
  code version. They supply one sentence; the machine supplies everything needed to make that
  sentence permanently useful.
- **Never spend a judgment you could have screened.** Anything with a right answer is yours to check.
  Their attention is reserved for what only a human can settle.

**Core principle: a judgment is only worth what you can reproduce.** An opinion welded to the exact
state that produced it is an asset that compounds. The same opinion floating free is a rumour.

Loop mechanics - cheap render, isolation controls, how often to interrupt them - belong to
**look-driven-iteration**. Use that for the loop. Use this for the record and what you do with it.

## When to use

- Starting anything where a human is the acceptance test (generative art, geometry, layout, motion,
  copy tone, audio, "feel")
- Their feedback keeps being unreproducible ("the middle one was wrong" - which one?)
- You are about to run a review round and have no plan for where the answers go
- A successor project will need what this one learned
- Someone asks for an evaluator, judge, screener, or "an agent with our taste"

**Not for:** work with a real oracle. If a test can decide it, write the test.

## The four laws

Each one is a failure that actually happened, not a preference.

### 1. Give the AI the same sensor the human has

If they judge by looking, you must look. Measuring what is convenient to compute instead of what
they can perceive produces confident, wrong conclusions.

A generator's owner reported bark "breaking into pixelated garbage". The agent measured the
*mathematical field* and found it smooth, twice declared the bug fixed, and was twice told it wasn't.
The defect was in the *rendered triangles*, then in a *shading flag* - neither visible to the
instrument it had chosen. Nothing was learned until the agent drove the real app to the owner's exact
camera and looked at the same pixels.

**Practice:** before trusting any metric, confirm it can see the reported symptom. If they say
"jagged", measure jaggedness, not amplitude. If you cannot perceive the artifact at all, get that
capability before diagnosing.

### 2. Make a data point nearly free to produce

Cost per judgment sets sample size, and sample size decides whether you get signal or anecdote. One
button plus speech-to-text turned a reviewer from three grudging comments into thirty rich ones in
the same sitting.

**Practice:** the human should produce a complete record with one click and one utterance. No
copy-paste, no filling in fields, no switching windows, no describing where they were looking. Every
step you leave in the way is a record you will not get.

### 3. Log the question next to the answer

An unprompted "this looks bad" is nearly worthless later. "Does the grain break at the branch? -
yes, still" is a labelled example: it has a claim, a verdict, and a subject.

**Practice:** drive review rounds from named trials. Each preset loads a full configuration AND
pre-fills the comment box with its id and the specific question. The human types under it. Both
halves land in the record together.

This is also what makes the log trainable later. Question + verdict is a label. Free-floating
complaint is not.

### 4. One change at a time

Two changes shipped together make the result unattributable for BOTH of you, and the human cannot
tell you which one to keep.

A round shipped a new generation model and a rendering fix together. The output changed a lot, the
owner said "you've gone backwards", and neither party could say which change was responsible. It
cost a full round to isolate by reverting one and re-rendering.

**Practice:** one variable per round. If you must ship two, say so explicitly and keep a way to
toggle each. When a result is confusing, revert one thing and re-render before theorising.

**Enforcement - because this law is the one agents break under pressure, repeatedly, while knowing
it.** The failure has a specific engine: rounds of human attention feel expensive, so the agent
"makes each one count" by bundling every diagnosed fix into it. The economics are inverted - a
bundled round produces verdicts about nothing, so its yield is zero or negative - but knowing that
does not stop the bundling (a source project's agent apologized for it and did it again the next
round; the human's verdict arc across two bundled rounds went "almost shippable" to "lumpy fucked
up cactus"). What stopped it was removing the vehicle: **a round is structurally a PAIR - the
frozen baseline versus the baseline plus exactly one named change, same seed, same viewpoint.**
There is no third slot for a second change to ride in. Pair-structure the round format itself;
do not rely on discipline at fix time.

**The frozen baseline that makes pairs possible:** when the human approves a state, freeze it -
version-tag it and keep its approved renders. Every candidate is judged against the freeze, drift
is measurable (a numeric profile of what their eye reads, diffed across builds), and when
iteration thrashes, ROLLBACK TO THE FREEZE IS A FIRST-CLASS MOVE: on the source project the
almost-approved build sat in version control the whole time, restoring it cost one command plus an
identity proof, and it converted "are we beyond fixing this?" into a short to-do list. Two rounds
of spiral were spent forgetting how cheap that return trip was.

## The record

Every entry, written atomically, one click:

| Field | Why it earns its place |
|---|---|
| **The question asked** | Turns a complaint into a labelled example (law 3) |
| **The human's verdict, free text** | Their words are the best signal you will get. Do not force a form |
| **Full state, verbatim as consumed** | Must replay EXACTLY. Serialize what the generator eats, not a summary |
| **Vantage point** | Camera / scroll / zoom / which screen. "It's wrong on the left" is meaningless without it |
| **The artifact itself** | A screenshot or capture. The one field people skip and regret |
| **Their marks ON the artifact** | A ring around the thing beats any adjective. See Annotation below |
| **Instrument state** | Quality, resolution, sample rate, WHICH RENDERING MODE. See below |
| **Code version** | Commit hash. Params alone do not reproduce anything a year later |

### The instrument-state field is the one you will forget

A project lost an entire round because the record did not say whether the preview was flat-shaded or
smooth-shaded. The human was describing a *shading artifact*; the agent read it as a *geometry
defect* and rebuilt geometry twice. One boolean in the record would have ended it immediately.

The general form: **record the settings of the thing doing the showing, not just the thing being
shown.** Whatever could make the same output look different is part of the record.

### Give them a pen, and agree what the colours mean

A comment box describes; a drawing points. Add a toggle that lets them draw over the output, and
composite those marks INTO the logged capture. It is cheap (a canvas overlay) and it was the single
biggest jump in signal quality on the project this came from - "on this side, the front chest part"
had cost several rounds of reconstructing which feature was meant.

Two details that matter more than they look:

- **Agree colour semantics, and include a colour for the TARGET.** What settled out was: red = this is
  wrong, worst first; yellow = secondary, or cut-here markers; **green = the shape it SHOULD have,
  drawn over the output**. Green is worth more than the rest combined. "Smoother" is unbuildable; a
  drawn contour is a spec. Ask for it explicitly.
- **Clear the marks per subject.** After a log lands, and whenever a new case loads, wipe the marks and
  leave draw mode. A mark belongs to one subject and one comment; carrying it forward annotates the
  wrong thing, and leaving draw mode on silently steals the drag from the camera.

### Agree the grammar BEFORE round one, and re-agree when marks stop landing

Before the first judged round in any project, write down with the owner what every element of a
record MEANS: each pen colour, a line versus a circle versus a filled scribble, a jagged stroke,
the comment's relation to the marks, and which of those the instruments actually read. Ten
minutes, one page, committed. Field-proven the hard way (2026-09-05): five weeks of rounds ran on
an undeclared grammar; the agent read strokes as exact pixel paths while the owner meant them as
rough windows, "blue" in a comment could not be resolved between two pens, and the loop ended with
the owner rejecting round after round of "fixes" he could not see. His own diagnosis afterwards:
the agent never understood what the marks meant because the meaning had never been explicitly
defined. The grammar is a spec both parties sign, not an
inference the agent makes; when verdicts and instruments diverge, re-read the grammar before
touching either. And treat a round spent fixing the evaluation process as a real round: it is
where the value per iteration is set.

### The instrument sees structure, never wrongness

Field-proven 2026-09-05: a render-domain scorer that measures tone structure under the owner's marks
gripped his DEFECT lines and his SHOULD-BE lines equally (both around the 75th percentile against random
windows), because a wrong band and a right ridge look the same to a local statistic. No pixel measure
knows what is wrong; only the owner does. So an instrument's honest role is a CHANGE instrument at the
owner's windows: before -> after under each mark, normalised by how much the rest of the artifact
changed, plus a calibration-free "did anything happen here" percentile, with verdicts UNCHANGED /
CHANGED / WORSE / NOT VISIBLE and never "fixed". Report two nulls (a random spot at its best angle, and
at one random angle): they answer different questions and disagree usefully.

### Verdicts without their words: the reverse pair

When the owner marks a CANDIDATE and writes no better/same/worse, do not ask again: remove the candidate
under their marks and measure. What falls to background without it was the candidate's own harm; what
strengthens without it was a feature the candidate had filled. Field-proven 2026-09-06: a "bridge"
candidate the owner had marked as an unwanted growth and a hump rising far too high was reverted the
same day by exactly this, with no further question to him.

### Predict UNCHANGED by default

Three sealed predictions of IMPROVED were wrong in one night; the predictions that held said
"unchanged" and "the outline moves out". The bias that predicts improvement is the bias that once wrote
"fixed". Write the sealed prediction as UNCHANGED unless a measurement already showed the change reaching
the owner's marks, and say the confidence.

### Mine the corpus once, then go forward with them

A harvest of old marks (a text re-read under the grammar, then a locate-first visual verification) is
worth exactly one pass: marks drawn on since-changed code are not positives today, and the owner's
memory of what an old mark meant fades (two of three questions came back with no recollection). After that
pass the owner's own ruling applied: stop mining, load a fresh round, let their new marks be the ledger.
Make the first live round a stated CALIBRATION too: report whether the process located what they marked
(line marks at the 82..100th percentile, a stroke they called jagged classed jagged by the rule, rigs
matching their telemetry), not only what the defects were.

### A mark is a window, not a path

Their pen is a thin, freehand, roughly placed line; it is not a measurement. Scoring the exact
pixels under a stroke is a recipe for disaster (field-proven 2026-09-05: a render-domain scorer
that walked the stroke's own pixels saw about a third of the owner's lines and called nothing he
could see "fixed" three rounds running). Treat every mark as
a strip rubbed clear on a steamed window: widen it (5..20px at the owner's zoom; SWEEP the radius
and take the one where separation stops improving) and look THROUGH it at the artifact for what
their WORDS describe. A line's direction is its smoothed direction, never the hand wiggle. Three
grammar rules to confirm with the owner, since theirs may differ: a JAGGED stroke is an
instruction to look for jaggedness (a steady hand does not draw jagged by accident); a bare line
means "a boundary is here"; a circle means "look inside", and its colour says for what. The
comment's words override all of this per entry, and pooled calibrations group strokes by what the
owner SAID a colour meant, never by pen colour alone (they grab the wrong pen and explain instead
of redrawing).

### Code version is what makes it survive

Parameters replay against *today's* code. To rebuild an artifact a year later, or to compare this
project's verdicts against a successor's, the record needs the commit. Without it the archive
degrades into "someone once disliked something roughly like this".

## Yield: how many atoms per interaction

An "atom" is one durable, independently useful fact extracted from a human touch. A comment logged
as prose is one atom. The same comment logged with question, state, vantage, artifact, instrument
and version is seven, and only the first one cost them anything.

**Capture everything the machine can see, not just what they said.** They should never be asked to
supply a fact a program could have recorded - what the settings were, where they were looking, what
build it was. Asking them to describe those things burns the scarce resource on clerical work and
gets a worse answer than the machine would have given.

**Enrich rather than interrogate.** The instinct when you want more data is to ask more questions.
Wrong direction: add more automatic capture instead. One utterance against a rich record beats three
utterances against a thin one, and costs a third as much of them.

**Track the trend, not the total.** The metric that matters is human touches per resolved defect, and
it should fall over the life of a project. If round five needs as much of them as round one, the
capture is not compounding - the records are not being harvested, or you are asking them things you
could have screened. Most projects will not reach zero. Every project should be heading there.

## The rate limiter is instrument correctness, not iteration speed

Once you have a proxy, you will be tempted to iterate against it. Do - but the proxy is now the thing
most likely to waste your time, and it fails quietly. On the project this came from, progress stalled
for several rounds not because tweaking was slow but because the detector was wrong three separate
times: wrong node set, wrong denominator, and no encoded standard. Each time the number moved while
the human saw nothing, or sat still while they saw plenty.

**Five rules, each from a real failure:**

1. **A detector that never reports clean is measuring an intended behaviour.** Two of three flagged
   every configuration on every axis; both were measuring a deliberate taper. Suspect the instrument
   before the artifact.
2. **A detector that reports clean while they see the defect has the wrong denominator or node set.**
   Ask what the HUMAN compares the flaw to. They compare a lump to the surface beside it - so
   normalise by that surface, not by the lump's own size.
3. **Never build a detector on the code you are changing.** One called the very function being
   modified; changing its normalisation changed the detector's units, and a unit change read as a
   regression. Any cross-change comparison needs an instrument the change cannot touch.
4. **Sample multiple viewpoints.** A single-ray probe read clean on the exact case a five-ray sweep
   flagged. Defects visible from one angle are the norm, not the exception.
5. **Calibrate the instrument against them, once.** The endgame move, and the only one that compounds:
   ask them to mark in RED only what is genuinely wrong and in GREEN what is acceptable, then re-aim
   the detector at exactly those cases. Some flagged cases will be correct behaviour - a feature that
   is SUPPOSED to stand out - and no amount of thinking will tell you which. One calibration pass
   beats three rounds of guessing at their threshold.
6. **Anything that SETS experiment state is an instrument too, and it can lie.** On the source
   project a slider clamp silently rewrote every "unseen" input to the same value for four rounds,
   and a test-rig default overrode the human's own recorded preference for four more. Both were
   caught only because the record logs what was USED, not what was asked. A rig must pin what it
   claims to pin, and anything it sets should be diffed against the human's own defaults - a silent
   disagreement there means every verdict judged a tree the human never chose.
7. **A local-defect loop without a target metric is a random walk.** Fixing exactly what they
   circle, round after round, can leave the overall shape wrong forever - each fix reveals the wrong
   shape more clearly and produces a fresh circle. If the target has a name (a reference photo, a
   one-word shape like "starfish"), lead every round with a distance-to-target view and demote the
   circles to second place. Corollary: render the viewpoint the target is DEFINED in, first - the
   source project produced hundreds of side views of a shape whose definition ("a starfish") only
   reads from above.
8. **Their metadata is evidence, not packaging.** The camera pose logged with each verdict cracked
   a defect four rounds of pixel-staring could not: every bad verdict came from high elevation,
   every self-screen from low. Screen at the elevations THEY actually judge from, and when verdicts
   seem inconsistent, diff the view metadata before doubting the person.
9. **Their sentences often contain the algorithm.** "It needs to get so thin that it doesn't have to
   cause any math issues when they merge - maybe they don't even have to meet" specified a
   fade-instead-of-collide mechanism implementable nearly verbatim, after the invented alternative
   had failed. Before designing a mechanism for a complaint, re-read their words as pseudocode.
10. **A hunt may end in a decision, not a fix.** One defect resolved to "the geometry is clean at a
   finer resolution; sampling it costs 3x the time" - a product trade-off only the human can make.
   Recognise that ending: package the A/B evidence and hand over the call instead of forcing a
   code change that quietly picks for them.

## Hunt brackets; do not wait to be handed one

A **bracket** is a present case and an absent case of the same defect under the same code. The
difference between them contains the cause and everything else can be discarded.

This came from the human noticing, in passing, that one output lacked a defect every other output had.
That single observation localised in one measurement what had already survived two wrong fixes. So do
not wait for it:

- **Sweep every axis to its EXTREMES**, not around the defaults. Defaults are where you already looked.
- **Remove whole subsystems.** "With the roots switched off, is it still there?" is the cheapest and
  most decisive question available, and the human can answer it in one sentence.
- **When a defect count scales with a knob, that IS the mechanism.** If artifacts get MORE numerous as
  you add samples, it is a per-sample step, not under-sampling - and those have OPPOSITE fixes. Adding
  samples to a per-sample step makes it worse. Check the direction before choosing a fix.

## Screen your own work before spending their attention

Render every candidate and LOOK at it before it reaches them. This sounds obvious and was the single
most deserved criticism on the source project: a round shipped twelve cases of which one had been
looked at, and most were visibly bad. "You don't need a human to see that."

Screening also lets you CUT cases. Two were dropped on the next round purely because rendering them
first revealed they asked questions the human had already answered.

Screening has a failure mode of its own, and it cost a full round on the source project: looking FOR
your fixes instead of AT the work. Three defects were fixed, their absence was confirmed, and three
NEW defects sitting in the same screenshots shipped unseen - the human's verdict opened with "it
shocks me that you didn't see this." Two rules close it:

- **Diff against the last version they approved, at their logged viewpoints.** A new defect is
  invisible to a checklist of old defects and obvious in a before/after comparison. A numeric
  profile of the thing their eye reads (on the source project: the silhouette outline per unit
  height) diffs across builds and catches what your eye grades past.
- **Enumerate everything you can see FIRST, hostile, as if marking it up for them - then consult
  your fix list.** The fix list is the last thing you check, not the lens you look through.
- **The two rules above are discipline, and discipline loses to cadence - so keep a structural
  guard: candidates that change the artifact's MASS or overall shape go through a blind judge
  (fresh context, told the instrument's quirks, never told what the change was supposed to do)
  before they reach the human.** Field recurrence (2026-08-07, with this skill loaded): in a
  fast one-pair-per-round loop, the author screened a candidate at the human's own camera,
  confirmed the intended ridges, wrote "no junction seam" - and a flank blister in the SAME
  screenshot shipped to the human, who caught it next round with a four-colour markup. The
  author's enumeration was not hostile; it was a fix list wearing a hostile costume. The blind
  gate exists precisely because the author cannot reliably see past their own intent, and
  "the pair cadence is too fast for a gate" is the rationalization to refuse: one gate run
  costs less than the round it saves.

## Their marks are the spec; your observations are questions

Fix only what they marked. A defect you notice that they never marked is a genuine observation - and
it ships as a QUESTION in the next round, never as changed output. On the source project a fix was
built for a texture defect the agent judged in its own screening crops; the human had never marked
it, and the fix manufactured a defect he immediately did mark. The inversion to remember: their
example is not a spec (the classic scope lesson), and symmetrically, your eye is not their bar.

## Predict their verdict, sealed, before they look

Write down what you expect them to say, per case, with a confidence, in a file they do not read. After
their verdicts land, compare. The gap is its own dataset and it is worth more than either half.

It works because it catches overreach in one round rather than three. A prediction of "this defect is
gone" met a verdict of "it moved" - which is a materially different claim, and the protocol forced the
distinction into the open. Predicting mostly PARTIAL is usually the honest position; each fix tends to
remove one mechanism and reveal the next.

## The harvest

A log becomes a dataset in three steps. Do them while the project is warm; nobody reconstructs
context later.

1. **Extract a defect vocabulary.** Read the log and name the recurring complaints in *the human's
   own words*, each with the axis it varies on (too much / too little / wrong place / wrong shape).
   Twenty entries usually collapse into a dozen named defects.

2. **Convert judging into screening.** Agents are unreliable at open "what is wrong with this?" and
   good at closed "is defect R3 present here, yes or no?". The vocabulary is what makes that switch
   possible. Never ask an agent for taste when you can ask it for a checklist.

3. **Keep the negatives.** A log of only complaints trains a screener that condemns everything.
   Deliberately capture "this one is right" entries; they are as valuable as the failures and people
   never volunteer them.

4. **Retire questions.** Each harvested defect should become an automatic check, a guardrail on the
   input range, or a screening item an agent runs unattended - and then never be asked of the human
   again. A vocabulary entry that still requires a human every round has not been harvested, only
   written down. This step is the asymptote; without it the log is an archive, not an engine.

**Porting:** the vocabulary is domain-specific and does not transfer. The *record schema*, the
question/verdict shape, and the harvested checks' STRUCTURE do. Set the capture up on day one of the
successor project, not on day forty - and seed its screening pass from the predecessor's vocabulary,
so the new project starts where the old one finished rather than at zero.

## What agents can and cannot judge

Objective and checkable is yours: is there a repeating lattice, did geometry break, is the value out
of range, did it regress against the last capture. Run those solo and stop spending human attention
on them.

Taste is theirs, and so is noticing what nobody was looking for. Bring them few, high-leverage
choices rather than a long queue of things you could have screened yourself. See
**look-driven-iteration** for how that division plays out during a round.

## Common mistakes

| Mistake | Fix |
|---|---|
| Capturing state but not a picture | Add the screenshot. It is the field that resolves arguments |
| Recording parameters, not the version | Add the commit hash |
| Asking "what do you think?" | Ask a specific question and log it with the answer |
| Building a form for them to fill in | Free text plus automatic capture. Forms suppress the best signal |
| Only logging failures | Solicit positives explicitly |
| Trusting your metric over their eye | Confirm the metric can see the reported symptom (law 1) |
| Harvesting "later" | Extract the vocabulary while the project is warm |
| Asking them to type what a program could record | Automatic capture. Their words are for judgment only |
| Asking more questions to get more data | Add more automatic capture instead - richer records, fewer asks |
| Same defect asked about every round | It was never harvested. Turn it into a check or a guardrail |

## Red flags

- "I verified it with a measurement" - can that measurement perceive what they described?
- "I'll capture the state, the screenshot is overkill" - it is the field you will want most
- "Let me ship both fixes and see" - unattributable for both of you
- "They said it looks bad" recorded with no question attached - unlabelled, nearly worthless
- Reproducing a logged verdict requires guessing anything - the record is incomplete; fix the capture
- About to ask them something with a right answer - screen it yourself; their attention is the budget
- Round five costs them as much as round one - nothing is being harvested; the log is not compounding

## Testing note

This skill was written from an observed baseline rather than staged pressure scenarios: the failures
in laws 1, 3 and 4 are verbatim from a session where an agent without this guidance committed all
three. Subagent pressure-testing was not run because the maintainer has a standing instruction
against dispatching agents. Treat the rationalization coverage as unvalidated and tighten it the next
time one of these failures recurs. First recurrence-tightening applied 2026-08-07: the
screening-for-your-fixes failure recurred WITH the skill loaded (the blister case, above), which
showed the two screening rules alone are discipline and lose to cadence pressure; the structural
blind-gate rule was added in response. Next recurrence should tighten again.

## Field addition (2026-08-27): renderers disagree — law 1 includes WHICH renderer

Art-lab recurrence of law 1 with this skill loaded: a vector file with
ambiguous windings rendered INVERTED in the agent's instruments (pymupdf
raster, Inkscape's boolean flattener) versus the human's browser. Three
confident edit strategies were built and "verified" against the wrong
picture; the human's revert order followed. The sensor question is not just
"look at pixels" but "WHOSE pixels" — probe a few known points in the
human's actual renderer before trusting any raster, and freeze one of their
renders as the ground-truth input for downstream tooling. Corollary
confirmed the same day: an allowed-change zone drawn too generously made the
raster-diff gate blind to the exact failure it existed to catch (wrong
denominator, rule 2's shape appearing inside a verification mask).

## Field addition (2026-08-01): the defect taxonomy + observation gate

When enough verdicts accumulate, distill them into a DEFECT TAXONOMY: one class per recurring
complaint, each carrying the human's exact words and where it shows (including which viewing
angles reveal it). The taxonomy then primes an OBSERVATION GATE: before any candidate reaches
the human, fresh-context agents - told the instrument's known artifacts but NEVER what the
change was supposed to do - judge it ABSOLUTELY against the taxonomy at the human's own logged
cameras. Any hit = a fix round first. Two calibrations proved necessary in practice: (1) a hit
present identically in the already-approved baseline is backlog, not a blocker - verify by
rendering the baseline, never from memory; (2) the gate's value is exactly that its judges do
not know what improved, so never leak the intent into their prompts. In its first week the
gate blocked one regression the author's own before/after framing had graded as an improvement,
and its taxonomy doubled as the training corpus for a future standing look-judge agent - the
log compounds twice.

## Field addition (2026-08-16): the 3D pen, and judges audited like rigs

Two portable upgrades from the bonsai project's heaviest week.

**A pen that draws ON the artifact beats a pen that draws over the viewport.** Raycast the
human's strokes onto the 3D surface and log model-space millimetre polylines alongside the
screen-space ones. The payoff compounds: marks survive camera moves, they become
calibration ground truth for detectors, and twice in one week the human freehand-drew the
EXACT working band of the responsible field feature (edges within a millimetre), turning
"somewhere around here" into a measured assignment. Two intake caveats learned the hard
way: strokes ACCUMULATE while the human orbits, so left/right-of-frame reasoning is invalid
until each stroke is projected onto the logged camera (one entry had 24 of 44 strokes
behind the camera); and the recorded pen-colour NAME can disagree with the human's
narration ("the purple circle" drawn with the magenta pen), so find marks by geometry plus
their sentence, never by palette lookup.

**Blind judges are instruments; audit them like rigs.** A gate judge reported six image
pairs "byte-for-byte identical, sub-pixel jitter only" while checksums and mesh counts
differed and the change was visible at a glance, then rubber-stamped no-harm. Standing
rule: a judge must LOCATE the most visible difference region per pair before its verdict
counts (knowing where is not knowing what was intended, so blinding survives); tell it the
builds are known to differ; checksum the artifacts before believing any "identical" claim;
a judge that cannot find a known change is VOID, exactly like a lying rig. Also blind the
blindfold: renders fed to judges must exclude app UI, or trial captions leak the
experiment (found because the top pixel-differences in one gate pair all sat inside the
note box).

## Field addition (2026-09-12): the same-geometry guard, the four-button list, the opening line

The atomic record captured, faithfully, three rounds of the human marking IDENTICAL geometry, because the
list of buttons offered for judgment had sixteen entries loading one baseline and the AI had dropped its
candidates without saying so. The record was fine; the loop around it had two holes. Three laws, all
mechanical:

1. **The intake brief flags repeats.** For every entry, compare its full parameter set with every earlier
   entry in the brief and print "SAME GEOMETRY AS <entry>" when they match. Marks on a flagged entry are on
   an unchanged artifact and are not scored as new. (bonsai: scripts/roundbrief.ts; it fired four times on
   the batch in question.)
2. **The judged list is the baselines plus ONE candidate pair.** Everything refuted, judged, or superseded
   is retired from the visible list the same day; keep the entries for the record and for replay tooling.
3. **The opening line.** Every reply after a judged round opens with what changed since the last round, by
   item, or "nothing changed, do not mark". A dropped candidate is a change to report.

And one about verdicts: a gate that a fresh, uninformed judge FAILS is not shown to the human "for their
eye only". Twice in a day the fresh judge and the human named the same defect in their own words; the gate
is trusted as a pre-filter, and the human's attention is the scarce resource the whole method exists to
protect.
