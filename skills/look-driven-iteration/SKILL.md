---
name: look-driven-iteration
description: Use when building anything whose success is judged by eye rather than by tests - generative or procedural visual output, UI look and feel, layout, plots, 3D geometry, game feel, motion. Sets up a cheap render / one-click grounded feedback / measure-then-fix loop so the human's taste reaches you at low cost and you never burn expensive verification on a look they have not approved. Also use when tempted to review, harden or test-drive visual work before the person has seen it, when a look complaint has survived two or more fix attempts, or when asked whether agents can judge aesthetics.
---

# Look-Driven Iteration

For work where the acceptance test is a person's eye. The failure it prevents is expensive and
common: hardening, reviewing and testing something *before* anyone has looked at it, then having the
look rejected and throwing the verification away with it.

## The rule

**Cheap render → their eye → iterate. Review and tests gate SHIPPING, not exploring.**

One project spent roughly 2M tokens on an adversarial review plus a full TDD build before the owner
saw the output, and he rejected it on sight. The same work, re-run render-first, converged in about a
dozen iterations of 5-20k tokens each.

## Set up the loop before iterating

Four parts. All of them matter; skipping any one collapses the loop back to slow.

1. **Cheap render.** Seconds, not minutes. A live dev view for dials, plus a headless still-render
   command for the final-quality check. If a look takes minutes to see, fix that first.

2. **One-click grounded feedback.** The single highest-leverage piece. Give them a comment box and a
   button that appends, to one file: their free text, the *exact replayable parameters*, and the
   camera or viewport state. No copy-paste, no context switch, and every opinion arrives welded to
   the state that produced it. Without this you get "the middle one looked wrong" and no way to
   reproduce it.

3. **Isolation controls.** Per-section randomizers or presets that vary ONE subsystem while holding
   the seed. Judging whole outputs confounds every variable; judging one section at a time produces
   usable signal.

4. **A read command.** One place you read their whole batch from, so they can log ten reactions
   without ten conversational round-trips.

## Measure the symptom; never build the proposed cause

Their report of **what** is wrong is reliable and often excellent: *"it breaks down about a quarter
of the way up, always in the same place"* pointed straight at a taper curve. Their report of **why**,
and yours, is a lead to verify.

Before writing a fix, reproduce the symptom or measure the quantity your theory predicts. Evidence
from one full session: measuring first was **5/5 correct on the first attempt**; implementing a
hypothesis was **0/3 and round-tripped every time**.

Tells that you are being handed a hypothesis, not a spec:
- "I'm not sure what it's called, but I'm sure there's a setting for it"
- "maybe it's X" / "I think what's happening is..."
- an example number offered while illustrating an idea

For interaction complaints (mouse, gesture, timing) **perform the gesture yourself**. Verifying that
the code does what you coded is not verifying that the experience matches the complaint.

Two toggle discriminators make this near-free when the work is behind flags, and both settle in
minutes what theorizing cannot (field-proven 2026-08-07, one session, both used):

- **"Is this a regression?" - rebuild the last APPROVED state at their exact vantage first.** If
  the reported structure is present there too, it is a pre-existing defect a recent improvement
  made visible (fixing one layer routinely reveals the next - say that out loud), not a
  regression. Tell them which, with the side-by-side.
- **When they name a cause, toggle the suspect feature at their vantage before designing.** Their
  causal chains are diagnostic data, not guesses - one four-part chain ("the malformed area is
  causing the cap ridge, which stops the groove") matched the mechanism one for one - but verify
  with the toggle anyway: a confirmed chain turns the fix from hypothesis into geometry, and a
  refuted one just saved a wasted round.

## Predict the number BEFORE you build, then compare

State the value you EXPECT in advance, then run the thing and compare. A number produced
afterwards gets rationalised against whatever came out; a number committed to beforehand is a test
that can actually fail. It is nearly free, and it is what converts "it built" into "it's right."

Field-proven 2026-08-08, three for three: a CAD groove predicted at π(15.5²−14.5²)×1.0 = 94.25mm³
removed came back 94.2; a screen-space stroke traced across a part of known 25mm width measured
26.2mm, close enough to confirm the projection math with the 1mm explained by eyeballing an edge off
a JPEG. When the prediction and a rough visual estimate disagree, trust the arithmetic and go find
the estimate's error.

**Pick an instrument that discriminates the thing in question.** Match the quantity to the question,
and notice when your habitual instrument cannot separate the outcomes you care about:

- **Magnitude** ("did the right AMOUNT change?") → volume, byte count, row count, duration.
- **Identity/structure** ("did I get the geometry I MEANT?") → counts of parts: faces, edges, nodes,
  elements, routes.

A groove cut flush against an existing wall either FUSES with that wall or leaves a hairline ridge
standing. Volume blurs the two; topology settles it outright — +2 faces / +3 edges with **no new face
at the shared radius** is the fused result, where a ridge would be +3/+4. The counts were already
being printed; they only had to be predicted and read.

## Find the governing formula before tuning constants

If the thing being modelled exists in nature, engineering or an established design tradition, spend a
cheap research pass finding the actual mechanism before adding another anchor. A real formula gives
structure that no amount of constant-fiddling reaches, and it usually explains several complaints at
once. State plainly which parts are established and which are your reading.

## When a complaint survives two fixes, stop tuning

Ask whether the current representation can express the target at all. Round primitives cannot make
ridges; radius modulation cannot make organic bumps, only spheres; isotropic noise cannot make
directional grain no matter the amplitude. If the defect is intrinsic to the representation, change
the representation.

## What agents can and cannot judge

Do not hand aesthetic acceptance to a model, including yourself. Agents looking at output drift
toward "plausible", which is precisely what gets rejected. Passing your own look bar is a milestone,
never approval.

Agents ARE good at, and should be used for:
- **Search** — render N variants across a parameter space in parallel
- **Objective screening** — aliasing, discontinuities, disconnection, unintended symmetry, anything
  checkable without taste
- **Reference measurement** — compare against a chosen reference artifact on NAMED attributes
  (spacing relative to width, counts, angles), which is measurement rather than opinion

The multiplier is on the SEARCH, not the judging: turn "they judge twenty things serially" into
"they pick from six pre-screened survivors". They stay the ground truth; the serial cost disappears.

## The RENDER is an instrument too — section, don't shade

"Objective screening" above assumes the picture reports the geometry faithfully. Often it does
not, and every failure looks like a real defect in the work.

Three distinct lies, all from one visualisation library in a single session:

- **Coplanar surfaces drawn through each other.** Depth sorting is per-primitive, so two parts
  sharing a face interleave. A large wedge of the wrong colour appeared across a panel; it was
  the renderer, and hours went into "fixing" geometry that was correct.
- **Framing that does not match the stated limits.** Axis limits were set to a 28-unit window
  and the output showed considerably more, so a correctly-spaced pattern looked too coarse — and
  got "corrected" to a spacing that was wrong.
- **Detail below the output's resolution.** A defect occupying 0.2% of the object's volume was
  invisible at sheet scale and instantly obvious to the owner at full screen.

**The rule:** when the question is *where is the material, how much of it, and how many*, answer
it from the DATA, not from the picture. Cut a section and measure the section; query the model;
count the entities. For a solid that means intersecting a thin slab and measuring what comes
back — which settled "10 troughs, 9 crests, pitch 3.850mm" exactly, after three shaded renders
had each suggested something different.

Reserve renders for the one thing they are genuinely good at: **does this read as the right
object.** That is a question about gestalt, and it is also the question you should be putting to
the human anyway.

Corollary: if you and the owner disagree about something countable, do not re-render. Count.

## Anchor to an artifact, not a description

Have them choose one reference (a photo, a screenshot, a product they like) early. "More organic" is
unactionable; "further from photo 2's flare angle" is measurable. Without an anchor, your bar and
theirs drift apart silently.

## One change per round, as structure

The rule everyone knows and agents still break under pressure: bundling fixes to "make an
expensive round count". The economics are inverted - a bundled round's verdicts attribute to
nothing - and knowing that does not prevent it. Remove the vehicle instead: a round is a PAIR,
the frozen approved baseline versus the baseline plus exactly one named change, same seed, same
viewpoint. Anything they call worse is deleted the same day, not defended.

Freeze what they approve (version tag + kept renders + a numeric profile of what their eye
reads, e.g. the silhouette outline per unit height). Every candidate diffs against the freeze.
When iteration thrashes, ROLLBACK TO THE FREEZE IS A FIRST-CLASS MOVE - it is one command plus
an identity proof, and it converts despair into a short to-do list.

## Judge form before skin

When output has separable layers (shape vs surface texture vs rendering), judge them
separately, base layer first with the upper layers OFF. One project's every real diagnosis
ended with "turn the texture off to see the truth" - making that the default judging surface,
at the owner's suggestion, killed the is-it-shape-or-skin-or-resolution confound that had eaten
whole rounds. Climb rung by rung (barest form, then each addition), freezing each approved rung.

Corollary, learned expensively: **noise can be load-bearing.** Coarse rendering grit was
supplying organic irregularity the design itself lacked; each cleanup made the output
worse-looking while being MORE faithful. When polish degrades a look-judged artifact, suspect
the design was leaning on an artifact - fill the design gap, do not restore the noise.

## Screen in THEIR viewing conditions, or the screen lies

The screening instrument must reproduce how the human actually looks: their zoom, their
shading model, their lighting. One project burned three rounds on "fixes" its 700px flat-shaded
fixed-light harness crops graded as improvements - the owner's zoomed, smooth-shaded, rake-lit
view called every one unchanged or worse. The moment screening moved into the real app at the
owner's own logged cameras with a raking light, the differences they described were obvious in
a single look. Drive the actual product surface (headless browser + camera-replay hooks +
light controls); keep the offline harness for objective gates only. Raking light deserves
special mention: near-horizontal light is how a human eye hunts sub-mm relief - give the owner
(and yourself) light-direction controls before judging subtle surface work.

## The eval rig itself can lie - rig-anomaly remarks are P0

A comparison rig built mid-project is part of the experiment. A results cache that paired
outputs to inputs by ORDER went silently off-by-one when one send bypassed its bookkeeping,
and A/B buttons showed the owner entirely wrong candidates; a whole round of verdicts had to
be voided. Rules: pair rig outputs to inputs by echoed CONTENT tags, never order; route every
request through one instrumented path; verify the rig by performing the user's own gesture
with the rig SETTLED (a verification probe that races the rig's startup reproduces the same
lie); and when the owner says anything like "these two are not the same thing" about the RIG,
drop everything and audit it - verdicts taken on a broken rig are void and must be re-taken.

**A readout saying "nothing happened" may mean the instrument stopped, not that the system is
broken.** Prove the instrument is live before diagnosing anything. A live telemetry pane appeared
frozen across several interactions - clicks dispatched, listeners fired, the camera seemed not to
move - and nearly became a bug report for code that was working. The tab was backgrounded, so
`requestAnimationFrame` was throttled and the pane had stopped refreshing, while screenshot capture
still forced a paint and looked normal. Anything driving a browser through automation is exposed to
this: rAF, timers and animation loops are all throttled or paused in background tabs, so the picture
can stay honest while the numbers go stale. What settled it was the predict-then-compare habit above
- after one real drag, the resulting angles were exactly what that gesture would produce STARTING
FROM the state the earlier click should have set, proving the click had worked all along. Do one
real interaction, confirm the readout changes, and only then believe what it says.

**This warning has now failed three times, and the reason is how it is indexed.** The three
occurrences were: a frozen telemetry pane; a new feature that looked broken; and — worst — an
app that would not load at all, which got written up as a bug report against working software
before it was caught. That third one was a load path awaiting a single `requestAnimationFrame`
inside its "show the spinner" helper, so the whole pipeline parked forever with a healthy
server, a healthy worker, and no console error. Nothing about that disguise resembles "a frozen
readout", so recognition never fired even though the rule was written down in three places.

**A warning indexed by SYMPTOM cannot fire when the symptom mutates. Bind it to the TOOL.**
The first action of any browser-automation session, before reading anything off the page:

```js
document.hidden === false
  && await new Promise(r => { const i = requestAnimationFrame(() => r(true));
                              setTimeout(() => { cancelAnimationFrame(i); r(false); }, 1000); })
```

If that returns false, nothing the page shows is evidence about the system under test, and
anything gated on a frame will hang forever rather than fail. Two corollaries: prove the real
work is sound by a path that does NOT touch rAF (posting the same payload to a hand-built
worker took ten seconds and settled it); and if the tool cannot bring a window to the
foreground, report that the visual check was **not performed** rather than describing what the
frozen page showed.

## When smoothing keeps failing, the eye is rejecting a SHAPE

A defect that survives multiple continuity fixes (smoother fades, softer edges, C2 kernels) is
not a continuity artifact - the eye is classifying a shape. A uniform radial narrowing band
reads as a lathe mark no matter how infinitely smooth its edges are. At that point stop
engineering smoothness: either put the shape lever itself in front of the owner (feature vs no
feature, measured beforehand to actually remove the complaint), or redesign so the feature is
carried by the structure the owner's green lines describe.

## Probes must see the change before their null means anything

A probe that reads "no change" has to be shown it CAN see the change. Field-proven 2026-09-05/06: two
field probes of a root-to-trunk junction (a surface top line along a ray at the root's azimuth, and a
vertical line above the root's axis) both read a candidate as doing nothing, and both were confounded:
the trunk leaned over its roots so the vertical line hit the trunk's own column, and the run curled off
the ray so the ray passed along the tube's flank. The candidate was in fact changing the geometry, and
the owner's marks found the change as HARM two hours later. Rules: (1) before trusting a null, drive a
change the probe must see and confirm it does; (2) measure from the vantage the human judges from (their
camera, the render), and treat field probes as diagnosis only; (3) a 2D picture of a 3D junction is a
hypothesis, not a model.

## Cheap knob pairs and refutations before any build; stop designing tired

The same arc ran two slider pairs and six mechanism probes, each with a sealed prediction, before a
line of geometry was written, and every one refuted its hypothesis by measurement without spending the
owner's eye. The one BUILD of the arc came at the end of a marathon, on a picture that the next probe
showed was incomplete, and it was harm. When N cheap refutations point at "the representation is wrong",
the right next act is a spec and a review court in a fresh session, not a 150-line law at 2 a.m.

## Field addition (2026-09-12): a dropped candidate is a change to report, and the trial list is an instrument

Three rounds in one day landed on identical geometry. The owner marked the same tree sixteen times
per round and said so in the plainest words available. Nothing was wrong with his marking. Two things
were wrong on my side, both mechanical:

- **I refuted my own candidates silently.** A screened-and-dropped candidate looks, from the owner's
  chair, exactly like no work at all, and worse: like being shown the same thing on purpose. Rule: every
  reply after a round of theirs OPENS with what changed since their last round, item by item, or with
  "nothing changed, do not mark". A reply that buries "skip those buttons" in paragraph six has not said it.
- **The trial list was stale.** Sixteen buttons all loading one baseline plus flags refuted weeks ago.
  The list of things you offer for judgment IS part of the instrument: it shows the baselines and ONE
  candidate pair, and anything refuted or judged is retired the same day. Add a guard on intake too: flag
  any entry whose parameters equal an earlier entry's ("SAME GEOMETRY AS"), so the same mistake cannot pass
  through the brief unnoticed. Guards, not reminders.

Three more, from the same day:

- **A refutation is only as good as its instrument.** A local bark depth cap had been "measured worthless"
  twice on field-domain probes; a mesh-domain instrument calibrated on the owner's own strokes (his red at
  1.5..2.4x the mean, his green at 0.7x) showed it removes the whole class in one run, and he judged the
  result a clear improvement. Before accepting a recorded refutation, ask what
  instrument produced it and whether that instrument can see what the human sees.
- **The resolution-scaling test:** re-mesh at a finer cell and watch how a roughness number SCALES. True
  curvature scales with the cell; mesher sawtooth does not. It settled "is the residual real or an artifact"
  in one run.
- **After N cheap refutations of the same representation, change the representation THAT DAY, with pixels
  to the owner first.** The earlier note in this skill ("a spec and a court in a fresh session") was right
  about the 2 a.m. law and wrong as a stopping rule: three cheap knob pairs (fatten the tube, land it at the
  edge) each cost a round of his time and each failed the same way, because a round tube cannot be a
  buttress. The blade (the root as a tall ellipse whose top edge rides one straight line from where it
  leaves the trunk to its toe, the line measured on the one root he never marks) was built, tested, screened,
  blind-gated and sent as pictures in one evening. Derive the new law from the example they never mark.
- **The blind gate is a pre-filter you can trust.** Twice in one day a fresh judge, not told the intent,
  named the same defect the owner then named in his own words (a bulge where the root meets the trunk).
  A gate FAIL means the candidate is not shown, not shown "for their eye only".


## Field addition (2026-09-20): when the ask is "make it look real", references and numbers come first

Artlab bird feet: three rounds of taste guesses (hooked claws; tiny flat shapes; bold strokes) were all
tossed. The owner pointed out that real finch feet are photographed everywhere and should be looked up. Two Commons
photos, proportions read off as NUMBERS relative to a feature already in the art (forward toe = 1.0 x
tarsus, hallux 0.6, claws 0.3 and gently curved, toes thin and flat, one toe reads from the side with
a second just behind), and round 4 was chosen on sight. This is the "find the governing formula before
tuning constants" rule above, applied to anatomy: when the target exists in nature, spend the cheap
research pass FIRST, downscale the photos (`.playwright-mcp/ref_*_s.jpg`) so you can actually look at
them, write the ratios down, and build to the ratios. Style guesses cost three rounds of his eye.

Also confirmed today: the owner's standing instruction to look at the output after every edit is the
cheap-render rule stated from the other side of the table; and a fix whose measured effect is zero (fillet on an obtuse kink, area
delta 0) must not be shipped as a fix.

## Field addition (2026-09-21): prototype before spec, the gate-hidden week, and a straightened frame reveals hidden seams

Three more from one project week, each paid for:

- **Prototype one instance before you write the spec, and spec before you convene a court.** Two design specs
  went spec then court then refuted, at 130k and 470k tokens each; the second reintroduced a defect a probe had
  measured the night before, because it reused an existing primitive and inherited that primitive's coordinate
  frame without testing it. A one-instance prototype on the cheapest synthetic case (the bench column), measured
  at export resolution and looked at, costs about a tenth of a court and would have shown the failure. Corollary:
  before building on an existing primitive, list its frame, its gates and its constants and test each against the
  last refutation. A reused primitive carries its old failure modes for free.
- **The observation gate needs a release valve.** With "a gate-failed candidate is never shown" in force, a week
  in which every candidate failed the judge left the owner asking whether anything had been built. Report state
  in three words every time (built and parked, loaded, refuted before code, each with its switch); after two gate
  failures in a row, name the switches so the owner can look with their own eyes without you loading a button;
  and cap each defect family: after N refuted representations, stop building and put the decision to the owner
  with the options and their measured costs.
- **When a fix removes the mark and the judge names a new defect elsewhere, ask what the old geometry was
  hiding.** Straightening a leaning trunk removed the owner's bulge and exposed a round-tube junction the lean had
  been leaning away from for two months. One cause, two symptoms; the "new" defect was the older one.

Judges at the millimetre, the working brief: diff map first, crops at 2x and never more (mesh facets read as
teeth beyond that), facets present in both frames are never a defect, a judge reporting no difference where the
pixel diff is large is void for that camera, and a defect is believed when two judges name it at the same camera.

## Field addition (2026-09-22): the recipe, the stand-in, the tree they see, and the count that lied

Six rounds in one day on one project; four things worth carrying to any look-judged work.

- **The recipe that got an approval on the first try, in order:** their marks, with their own colour definitions for
  that entry; the discriminator (render the state WITHOUT the feature at their exact camera: no defect there means
  the feature is the cause, defect there means it is the base shape); a histogram of the feature's own contribution
  at the mesh vertices INSIDE their window, keyed by the feature's own coordinates (not pixels: the bands they mark
  were 5..9 levels of 255 and no threshold separated them from noise); one constraint in THEIR words; a numeric
  prediction sealed before the run (a failed prediction kills a law in one run; three died that way in a morning);
  a guard test on the field; one pair beside the judged button. The owner's verdict: "you got it on the first try,
  remember how you got here."
- **The step that cannot be skipped is the first one.** The same recipe, run on a defect only my probe could see
  (two handed-over grooves measured dead; the fix one sentence, prediction exact, tests green), came back "the
  first one looks better, I can't tell what the second one is trying to do." A clean measurement of an invisible
  defect is still an invisible defect. Own observations are questions for the owner, never builds.
- **A stand-in approval starts the real round.** Three laws approved on a practice column with one fake root produced
  three new defect classes in the first hour on the real tree (a flat flare over long buried runs; roots surfacing
  as islands ahead of their collar; knuckle roots too short to carry a groove). Each needed its own one-constraint
  law; a fixed-millimetre floor failed where a proportional one held. Budget the screen on the real thing, not just
  the port; and screen with the SAME instrument that worked on the stand-in.
- **Probe the thing they see, and do not trust an invariant as a null.** My probes ran on the library's defaults; the
  app the owner judges runs on his approved sliders; those were different trees, and half a day of numbers described
  roots his tree does not have. The instrument's input is the logged parameter block of an entry he made. And the
  rig's triangle count was identical with the change on and off, three runs in a row, while the geometry had
  changed: a count is a liveness check, a checksum of positions is a change detector.
- **Delegation that worked:** an exact spec (the reference implementation named, the hot-loop variables named, the
  constants, the tests, the report format, "declare every deviation") to a cheaper model built the port first time.
  The expensive half was the screen afterwards, and that is the half that is not delegable.

## Field addition (2026-09-24): offer the judging surface in the FIRST build; the no-server version

A tool that stamps a rating badge onto photos was built to match a reference image within a few levels per
channel, and verified by pixel diffs and my own screenshots. The owner's real questions (how big on the photo,
which colours) were questions of taste on HIS photos. The owner had to ask for the loop, in effect: a way to
judge how the overlay's size should be adjusted. Matching the reference was a milestone; it was never the
acceptance test. When the deliverable is visual and the owner will tune it, offer the judging surface in the first
build.

The minimal version, when the owner wants no server (plain HTML and CSS, just open the file):

- **A `-test` flag on the same CLI** that renders every variant into a folder and writes one static `index.html`
  next to them. Opening it by double-click is the whole workflow; change flags, rerun, reload.
- **The exact command that produced the page, printed at the top**, plus a settings table with colour swatches.
  That is the "replayable parameters" half of grounded feedback, for free: whatever he likes, he can copy.
- **Side-by-side axes that match his real decision:** each photo × each candidate size in one row, each state
  on light, grey and dark backgrounds, and a strip at fixed small pixel sizes shown at actual size (where
  legibility dies).
- **Verify the page yourself before handing it over, but not via `file://`**: browser automation refuses it.
  Serve the folder on `127.0.0.1` for the check and stop the server afterwards.

Next rung when his marks start coming in: add the one-click comment box (append text + the page's command to a
file), per "Set up the loop before iterating" above.

## Field addition (2026-09-28): a slow render is a symptom (profile it by feature), and a hash guard makes speed work free of the eye loop

The first rule above says "if a look takes minutes to see, fix that first". Two lessons from doing exactly
that on a deterministic geometry generator whose preview took 18 seconds and whose export took a minute:

- **Profile by feature on a LOGGED configuration before optimizing anything.** The assumed hot spot (a
  1600-line per-point field function; an earlier review had even named the finite-difference gradient inside
  it) was not the lever. One stage profile with per-feature switches showed the texture cost nothing
  measurable, that turning the base bulges off cut evaluations threefold NOT because of their arithmetic but
  because the mesher's safety margin had been widened for every segment by the sum of every feature, and that
  the mesher's own hash-map bookkeeping was a fifth of the time. Time is a symptom like any other: measure it,
  split it by feature, then build. The three changes that followed (a per-segment margin, an exact
  lower-bound cull, typed rolling storage in the mesher) took the preview from 18.4s to 4.5s and the export
  from 62.7s to 15.9s.
- **Guard speed work with output hashes of the real configurations, and it never touches the eye loop.** Before
  the first edit, hash the final output for the owner's own logged settings (seven cases: the trees he judges,
  a full-assembly case, an old-feature case). After each change, hash again; the lines must match exactly. A
  match is a complete proof for a deterministic pipeline, cheaper than any judge, and it means the owner's
  approved look is untouched by construction. When rewriting a driver, keep the old one as an oracle and add a
  test that the two agree byte for byte. A triangle count is NOT this guard (a same count passed as "no change"
  on 2026-09-22 while the geometry had moved): hash the positions and the indices.

The pairing matters: the profile says where the time is, the hash says the fix changed nothing he can see.
Without the second, every speed change would need a round of his eye; with it, none did.

Same day, a process lesson for the plan above the loop: **a direction review with no mechanism is a wish.** A
written review said "print first, product first"; three weeks and fifteen polish rounds later nothing had
moved, because every session opened on the current family's next law and the owner's "go" was a go on that
law. The rules that held in that project were all mechanical (an active-round list, a retired set, a
same-geometry flag). When a review changes direction, give it a gate the same day: the status table carries the
open phase, and every proposed round names the phase it serves.

## Field addition (2026-09-30): an animation's judging surface needs a speed dial

One sample step-through animated figure for a teaching site, with a one-click "copy for Claude" feedback box, was
approved on first look. The owner's very first request was a speed control, then more range, up to sixteen times normal:
at high speed the whole flow plays in about two seconds and its SHAPE shows; stepping shows the detail. Ship the
speed dial in the first build of any animated judging surface. Scale all three clocks from one number: the step timer
in JS, SVG `animateMotion` durations, and CSS transitions (`calc(<time> / var(--sp))`), remembering the original values
so repeated changes never compound. The feedback box delivered step, scenario and viewport width with the note,
which is the grounded-feedback rule above working as designed.
