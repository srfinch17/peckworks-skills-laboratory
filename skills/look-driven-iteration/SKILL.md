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

First check that you are tuning the thing they mean. A complaint names what they SEE ("a line of
stones dividing the land"), not a feature, and the eye maps it onto whichever feature you already
suspect. Render at full size, crop where they point, find the thing in the pixels, trace it to the
code that paints it, and say "it is X, painted by Y" before touching anything. One session spent
two rounds reworking a sand edge beside a deliberate stepping-stone path; the fix was deleting
the path. A feature can be the defect, and locating costs one render.

Then ask whether the current representation can express the target at all. Round primitives cannot make
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

## Field addition (2026-10-02): a second judge reached through chat screenshots, and the mark-scope rule

An icon for a company web page was judged by a colleague of the owner, who saw only screenshots relayed through a chat
and answered with marked-up images. Eighteen rounds, each cheap; four things that made it so, and the one that did not.

- **One preview page per round, three things on it:** the new version marked as the one wired in, the previous
  version beside it, and the reference image. Shown at the real sizes it will live at (both tile widths) and enlarged.
  Open it in the owner's browser; they screenshot it for the judge. The judge never sees your prose, only the page.
- **Change only the marked area, and keep the rest byte-identical.** The one rejected round took a circled corner as a
  licence to redraw the whole front and relayer the drawing; the verdict was to go back to the previous one and work
  only in that area. The tell: your own change list is longer than their mark list. A wider fix is a separate variant,
  never folded in.
- **A mark that admits two readings becomes two variants, with the literal one named.** "Mirror the beam across" in an
  isometric drawing meant mirror in APPEARANCE: the geometric mirror already existed and looked smaller, because near
  members foreshorten. Showing both let the owner pick in one message.
- **Judge size in the row, not alone.** A thin-lined drawing read smaller than its flat heavy-stroked neighbours and
  needed two size bumps; the second one did nothing until the container's padding, the real cap, was measured.
- **Once past three rounds, generate the artifact and the preview page from one script**, so they cannot drift; a
  hand-synced copy produced one malformed file. Isometric drawings are easiest to edit as car-space coordinates run
  through one projection formula, with members drawn as a dark stroke under a narrower light stroke for a 3D bar.

## Field addition (2026-10-02): "pop it open" is the judging surface, and the review waits for the verdict

Screensavers, one day, five builds. The owner's whole judging loop was: I launch the saver full screen for him
(`Start-Process X.scr /s`, he moves the mouse to close it), he says "open it one more time" two or three times,
then one line of verdict: approved, or close but smooth out one named motion, or a named thing he could
  not see. No comment box was needed; the launch IS the one-click surface. Things that held:

- **Hold the hostile review until the verdict, then run it once.** Both nemesis runs came after approval and
  returned 11 real findings, none about taste (a boat over land on 1 seed in 13; birds tangling on half of
  seeds). Reviewing first would have risked 390K on a look he might have sent back, as in EP-132. He asked for
  the review himself once the look was settled.
- **State the reading of an ambiguous complaint in one line and start.** A complaint that a figure had one hand
  and that its wave was visible was read as "no fingers on the hanging hand, and the wave is a frozen pose"; he
  corrected mid-turn (the wave was NOT visible), which landed in the same build. Say the reading;
  do not stop to ask.
- **A "smooth it out" complaint on a flip-book is a pose count and an easing problem**, not a speed problem: 6
  wing poses snapped, 24 did not; the bend of the wing against the stroke and an eased glide transition were
  what read as "fluid".
- **Animation below one pixel is not animation.** A bob of 0.43 px rounded to zero every frame while its
  reflection flickered one pixel. Set a floor in pixels and round the pair together.
- **Tell the owner the measured hands-off time of any test that his input aborts.** "25 seconds" for a
  two-minute run produced two rounds of false FAILs and a misdiagnosis (EP-134).

## Field addition (2026-10-07): numbered cards that never move, sets kept as history, and the live card with its command

Seven judged rounds of a photo footer in one day, through a page served over a tunnel to the owner and his colleagues.
What made it fast:

- **Permanent card numbers.** Every variant got a number on the card; a removed card's number is never reused and a
  new round is appended as a new set. He judged by number ("card 47 is the consensus") across rounds and people, and
  nobody had to describe a picture. The one time a card was dropped (a rule made it impossible) its number stayed a
  gap, by design.
- **Every set stays in the generator behind a switch.** When he said "drop all the rest", the sets were hidden, not
  deleted; two earlier sets had lived only in a scratch folder and he asked, unprompted, for all past iterations to be
  recoverable. Keep the definitions in the repo and a dated history file with the verdict of each round; the caption
  of every card carries the exact command that reproduces it.
- **A live card beside the static ones, with the command printed under it.** Once the look was close he wanted dials:
  text, font and style, QR on/off and size, rating, every meter colour. The card is a browser rendering from the
  library's own geometry, and under it the command that renders the same thing for real, so a reaction becomes a
  reproducible run. The dials that moved the design were the ones a generator could not guess (font, QR size by whole
  steps).
- **Say what is unreachable before building.** "Make the QR 10 to 20 percent bigger" was impossible without blurring
  the code (whole pixels per module), so the page showed both reachable steps and said why, up front. He accepted it
  without a round lost.
- **The owner is also an instrument.** He scanned the code with his phone. Ask for that proof when a device is the
  consumer; the decoder on the file is the floor, not the ceiling.
- **Driving beats looking before any claim.** A screenshot of the live card showed "a code in a tile"; the code was
  the wrong one (a sibling page's sample link) and he saw it. A tester that drove the page then found a second bug a
  picture cannot show. For anything a person clicks: a driving tester plus running its command, then the claim.


## Field addition (2026-10-06): a trade between two defects is theirs to judge, and the dial sweep names the body

Two from one night, paid for with fifteen days:

- **When a candidate removes THEIR mark and the gate refuses it for a DIFFERENT defect, that is a trade, and a
  trade is theirs to judge, by eye.** The 2026-09-21 valve (name the switches, put the options in prose) was in force
  and did not reach the owner: a visual judge does not decide from prose. The candidate that emptied the owner's
  months-old circle stayed parked behind a gate that had never been calibrated to rank two defects, and the owner
  marked the same mound again ("you have been unable to fix this for literally months"). The gate ranks harm on the
  SAME mark; for a different defect elsewhere, load the pair beside the baseline, name the cost in the trial text in
  everyday pictures ("mound for knob"), seal the prediction, and let their eye rank the two.
- **Sweep the existing dials at their camera before designing any law.** Fourteen renders (every root dial, the lean,
  the curve, the parked flag) on one contact sheet took fifteen minutes and said what months of laws had not: no root
  dial touched the mound; only a straight trunk foot did. A dial sweep is a discriminator for which BODY owns a defect.
  Then locate the cost the same way: "feature on minus feature off" along rays from the axis, tabled by height and
  azimuth, found the knob at one address (one root's bulge and tube stacking on the vertical flank) in three probes.
- **A pixel scorer is void when the candidate moves the model in the frame.** The straightened trunk shifted everything
  left; the scorer's fixed windows then compared different parts of the tree and said WORSE. Say "void", never report
  the number.

## Field addition (2026-10-07): motion is not a still, and check the medium's ceiling first

Two misses in one night on a screensaver build, both of which a still render passed.

**Motion needs motion instruments.** Three verdicts in a row were about movement ("standing
waves", "not flowing smoothly"), and each fix was checked with stills plus a headless draw-time
number. Neither can see motion. The real frame log on the person's own display showed 41 fps with
17 to 59 ms gaps (a 64 Hz timer out of step with a 60 Hz screen), and a frame-dump measurement showed
the "flowing" texture dissolving in place. When the words are about motion, build these before the
next fix: (1) dump consecutive frames and measure whether a patch's detail reappears SHIFTED a few
frames later (travel) or merely changes (shimmer); (2) log real frame intervals on their display,
which is the only check that includes presenting and pacing. Draw time is not frame rate.

**Check the medium can reach the look before polishing in it.** The ask was "as photorealistic as
possible"; five rounds tuned a code-painted scene that could only ever be an illustration ("so
laughably bad it makes me think you made it bad on purpose"). The 2026-09-20 addition above
already said references come first; it was not applied because every round compared the render
with the previous render. Put one real reference next to the first cheap render and ask "can this
medium get there?" If not, change the medium (here: a real photo with only the moving parts
animated got "much better" on first sight) before spending a single polish round.

## Field addition (2026-10-09): a comparative verdict is not a pass, and anything alive is followed before it is shown

The motion rule above was applied to the water and not to the fish swimming in it. The person's
first verdict on the photo scene had been "ok much better" (next to a far worse painted one). Two
sessions of additions later, checked on stills and section timings, they watched it once and
retired it: the fish "were just stupid overlays that wiggled in place, then slid around ... behaved
exactly how fish don't". The fish were one side-on picture, flipped to turn, slid to dart.

**A comparative verdict approves the direction, not the parts.** "Better" next to a worse build
says keep going. Go back for a verdict on each moving element they have not named, and when they
ask to make something "more visible", first ask whether it belongs there at all (no fish is
visible under a mirror-bright reflection).

**Anything alive passes four gates or is left out.** Really visible where it is; drawn in the
scene's own perspective (an overhead view needs a top-down animal, never a side view turned);
turns by bending (a spine that follows the path the head took) or as a rigid whole, never by
flipping a picture; moves the way that animal moves, checked against footage. Absence beats a fake:
on a real photo the fake creature is the one thing the eye goes to.

**Follow it before showing it.** The cheap render for a moving actor is not a still: log its
position every frame, dump the frames, and make a strip of crops centred on it (one tile every
few frames, stamped with time and state). Plot its path over minutes on several seeds. Built that
way the next day, the replacement scene's koi, swallows, dragonflies and snake surfaced three
steering bugs (an actor trapped, laps in one lane, an orbit round a waypoint) before any render
reached the person. Before adding to an existing build, watch all of it in motion and raise its
weakest actor first; never polish around a rotten core.

## Field addition (2026-10-09, evening): measure the invariant, move the whole field, name the mechanism behind the complaint

Four judged rounds on one screensaver shore in one evening (grass, rocks, a turtle, cattails), each
answered within the hour by the owner's own idle screensaver showing the newest build. What held:

- **A picture of the invariant is not a measurement of it.** A 48-tile follow strip centred on the
  turtle's nose read as "nose first"; the body was laid out ahead of the nose and it swam tail first.
  He saw it in one look. Before showing anything that moves, write the one number that is wrong if
  the thing is backwards, mirrored or inverted (here cos(body axis, velocity) over every moving
  frame) and compute it; then look at the strip. The strip now carries head, tail and velocity marks.
- **Moving sprinkles on a static field read as "the ground moves in spots".** Static carpet of
  blades plus 800 swaying tufts measured 1.1 mean change per frame on a lawn patch and looked still;
  sliding and brightening the whole carpet by the wind field took it to 3.1 and the wave showed. When
  the ask is "wavy", the FIELD must move, not things standing in it. A per-frame change number on a
  fixed crop is the instrument for a moving field; the follow strip is for an actor.
- **Translate the complaint into the drawing mechanism before touching a constant.** "A white line
  of rocks" was a pale pen round each stone's foot. "Rocks on top of the water" was the waterline
  drawn straight across each stone (the bank curve) instead of round its own rim. "Gray circles" was
  a radial gradient (a pillow) with ruled creases and polka-dot grain. Each took one change once the
  mechanism was named, and the first guess at each (fade by depth, thinner pen, smaller dots) was a
  tuning of the wrong mechanism.
- **Under water things go darker and bluer, never paler.** Mixing a submerged stone toward the pale
  water colour made fog; mixing a band inside its rim toward water darkened by a third made a wet
  flank with a waterline. The same held for the pond's shallows earlier. Know the direction a medium
  pushes colour before blending toward it.
- **Jittered grids still read as planted rows.** Tufts one per cell with random offsets looked
  sown in lines at 75% occupancy; random placement with a minimum-spacing rejection looked like a
  lawn. Parallel shadow strokes at 34 alpha wove a lattice; 16 alpha and 60% length read as grass.
- **Measure the heavy size after every look change, not at the end.** Taller grass doubled the tuft
  pages' area and pushed 4K from 15 to 21 ms a frame with nothing visibly wrong. Two mechanical cuts
  (sprites stamping only each row's painted stretch; the carpet refreshed on alternate rows from a
  kept copy, checked for comb by odd-versus-even frame change) got it back under a sixtieth. A look
  round that ends over budget on his screen is a round he will send back for stutter.
- **The idle timer is a judging surface.** He asked for the Windows screensaver off while work runs
  and on, pointing at the newest build, when it is done (`scripts\saver.ps1`): he then sees the latest
  work by walking away and gives one line on return. No "run it" round-trips, no UAC, no install.

## Field addition (2026-10-11): a steered creature's default bug is a standstill, and the feeler must be finer than the obstacle

Three rounds on one overhead pond in two days (minnow schools and a dragonfly's game, a lizard and a
log, a snake that steers and startles), each verified by instruments before the owner saw it, each
approved in one line. What held:

- **The bug a still cannot show is the creature that STOPS.** Five times in three days the failure
  was not a wrong look but a standstill: a lizard that crashed its own update and was visible 0 s of
  60 (its stills looked fine), a lizard flipping Dash and Bask thirty times a second on a rock's wet
  side, a snake jammed against a lily pad for two minutes on every seed, and earlier a swallow
  orbiting a waypoint for 52 s and a turtle out of view 40 to 70 s in 180. Every one showed in a
  timeline (position and state every five seconds, visible seconds per minute, longest standstill)
  and none in a frame. For anything with a goal, the timeline is the FIRST instrument, before the
  follow strip; read the longest standstill as a number. Then the strip, for the look (that is what
  caught fish wriggling like worms and a tail folding into a hairpin).
- **A sensor spaced wider than the smallest thing it must see is blind to it up close.** The snake's
  feelers sampled at 0.35, 0.7 and 1.0 of a body length ahead; a lily pad is a tenth of that. Pressed
  against the pad, every feeler landed in clear water beyond it, the goal's pull held the nose on the
  pad, and the step was refused for ever. Feelers from just past the snout outward, AND the refused
  step itself forcing an avoidance turn, ended it. Any "never stuck" rule (a step is refused when it
  would enter something) is a deadlock unless the refusal feeds back into the steering.
- **The obstacle model is per layer.** The same lily pad is no wall to a koi (it swims under; the
  pad's soft painted edge had once trapped fish as a ring of wall) and a hard wall to a snake on the
  surface. Hold obstacles as what they are (circles, a capsule for the log) and let each creature's
  layer decide which ones count, rather than one shared mask.
- **Two of his standing instructions can collide, and the collision is mine to see.** "Pop the build
  open for me" and "leave the idle key pointing at the newest build" are the same file opened
  twice; a follow-up publish then fails "file in use". Publish everything ready before the pop-open.
  When a standing rule is added, check it against the others on the same resource.
- **A finish line that is taste cannot be met by the builder.** A goal ending in "cute" and "awesome"
  has no instrument; the stop hook rejected every finish report and several turns
  went on repeating the same line. Say once what only the person can judge, name the two moves open
  to them (clear the goal or give the line), and stop.
- **Verdicts are arriving on the strength of the instruments.** "Yes, push" came before any look
  verdict on two rounds (the push had been held for his word). The instrument routine (timeline,
  nose-first, clearance, flee response, back-to-back cost, verify) is what he is trusting; keep it
  complete every round, and keep the look question open in the final line, because the push yes is
  not the look yes.
- **Today's cost number is not yesterday's.** The same build read 12.6 ms one day and 15.8 the next
  at 1440p. Only old-versus-new back to back in the same minutes says what a change cost (here:
  nothing). A number against the table is a mood reading.

## Field addition (2026-10-15): the state lives on the beads, a side is measured, and the same-scene gate

Sakura Pond thirteen and fourteen (a really deep pond, fish that tilt into a dive, petals shoved
aside), both pushed on one "commit and push" before any look verdict, the third round in a row.

- **A property that can be partly true belongs on the points, not on the thing.** One depth per fish
  could not tilt, could not vanish head first, could not shove a petal with only the back that is up
  at the surface. Depth per spine point gave all three for free, and the petal rule fell out of it
  ("pieces shallower than a half width push"). When an owner says a thing is half in one state, move
  the state to the beads before adding a cue.
- **A cue with a SIDE is a claim about the running code's convention, not about geometry.** The sun
  gleam was put on the shaded flank because I derived "which side is v positive" from the normal on
  paper; the painter runs its pieces nose to tail, so v runs the other way. A crop at 8x could not
  tell the gleam from the dorsal line three pixels off; a sixteen-sample brightness profile across the
  body at one frame settled it in one line of numbers. Any gleam, shadow, lean or lift is checked by a
  profile against the scene's own shadow direction before it is shown.
- **The same-scene gate comes before any number.** Three rounds in a row moved a dice roll (traits
  dealt, an island placed earlier, a petal's size rolled before its life), and each time an
  old-versus-new timing or behaviour comparison was comparing two different scenes; each time a
  SECOND instrument had to find it (a pixel diff, a section timer blaming an untouched part). Now one
  tool renders a frame from each build at one seed and prints the share of pixels that differ
  (kit `motion/samescene.py`); it runs before the first timing is read. A guard beats remembering.
- **A rule with a number carries the scope it was written for.** A "bed-forced rise is exempt from the
  rise limit" rule, asked for by a reviewer when the pond was shallow, became a 50-pixel slide when
  the pond went three times deeper. When the quantity a rule leans on moves by 2x, re-run the
  instrument that justified the rule rather than carrying the rule.
- **The lag between the leading and trailing part of one body is a metric.** "Seconds the tail is
  seen after the head is gone" caught a fish hung nose down for eight seconds that nose-first,
  clearance, standstill and slide all passed. For any state that travels along a body, log the lag.
- **An owner's world law, said once about one element, is a gate for every element after it.**
  "Nothing can clip through anything in this universe" was said about petals; it now means every new
  thing declares, in the docs, what it is solid to and what it passes under, and the known
  exceptions are listed as the likely next round rather than left for the owner to find.
- **His next list is the verdict.** Three rounds pushed on the instruments before any look line; the
  look line never came separately, the next spoken list did. What he does not name is accepted for
  now; carry the open taste questions in memory and do not re-ask them.

## Field addition (2026-10-16): decompose the measured shape by its sources before tuning the shape

A complaint about a shape ("a super wiggle that ripples down the body like a worm") was measured (bend reversals
along the drawn body: a quarter of frames), two plausible causes were fixed (the wave's envelope, a filtered turn
rate), and the metric barely moved. The fix that worked came from a reviewer who subtracted each point's KNOWN
screen offset (the depth-driven sink) from the drawn shape and re-ran the same metric: the planar shape alone
reversed on 0.1 to 0.35% of frames, so 95% of the symptom was the depth laid along the body, which three different
mechanisms were stepping. Rule: when a shape metric survives a fix, do not tune the shape further; subtract every
known contribution to the drawn shape one at a time (an offset, a projection, a wave, a history) and re-measure
after each. The source whose removal collapses the number is the cause, and it was not the one the complaint's
words pointed at. Pairs with "When a complaint survives two fixes, stop tuning": this is what to do instead.

## Field addition (2026-10-19): a diagnosis from code is a hypothesis until a crop shows it, and two keep-out classes

A look complaint ("tadpoles can swim on top of the petals") was diagnosed in a harvest from the draw order and
written down as fact with a fix plan. The next session rendered first, as "When a complaint survives two fixes"
asks, but BEFORE any fix: old build and new at the logged moments the mechanism predicted, side by side at 4x. The
sheets were identical, and the thing the owner saw was a different element entirely (a heap of petals painted once
into the backdrop, which every mask called open water, with the animals drawn crisp over it). The code-found bug was
real and rare (seconds per four minutes); his words said "currently", which names something seen whenever he looks.
Rules: (1) a diagnosis made from code, a summary or a reviewer's note is a HYPOTHESIS until a crop shows the pixels it
names; write it with that word or with the crop's file name, never as a plain sentence, and make the render the
first act of the session that builds on it; (2) when the mechanism's rate does not match the complaint's rate
("sometimes" against "currently"), look for a second mechanism before building the first; (3) a mask built from
geometry is a claim about the picture and the painter decides what is on top: anything painted once at or above a
live layer is in that layer's stencil or copied back over it every frame (third instance of this class).

The fix then needed two kinds of keep-out, and one mechanism could not serve both: as a WALL the heap's zone penned a
scattered group in a pocket for three minutes; as nothing it filled with resting animals. Steering obstacles come in
two classes, solid and "pass through but never settle"; steps test the first, placements (home, spawn, perch, slot)
test both. And a placement test written apart from the step rule is always weaker than the step rule (fourth
instance): a home passed its own test while every step from it was refused, and the animals were born on one pixel
for a whole run. The placement test calls the step test at that point and then samples a ring round it.

## Field addition (2026-10-20): pacing over a whole start, a hitch as a first-use cost, pace as species, and the event log that locates a complaint

Sakura Pond, rounds twenty to twenty-two in one day: the chance meal of tadpoles, the turtle's feet, tadpole haunts, koi
company, then "find ways of speeding things up, smoothing things out", then two one-line looks ("the tadpoles swim a little
bit too fast ... like mosquitos", "the new duck ... wings are floating specs above the body").

- **Pacing is measured over a whole run START, not a settled window.** A 15 s on-screen log read an even 17 ms a week ago
  and the number stood in three documents; the first log over a start read half the frames at two pages, a steady 60 only
  from 5.3 s, and on one run never, because a pump with hysteresis sat on its own way-back line. Any "smooth" claim carries
  the start-of-run log beside it, and is re-measured whenever the settled cost moves (every round that adds an animal).
- **A dropped frame the averages hide is a first-use cost until proved otherwise.** Tiered JIT's rough code for the first
  seconds; a full-strength compile of an animal's code on the frame it first appears; the framework's generic code for your
  own types compiled when a collection spread or a LINQ call first runs; a pool trim. The instruments: a per-section WORST
  frame with its frame number (an average cannot show one frame), the update timed in laps of its own, and the runtime's own
  list of what it compiled and when (DOTNET_JitDisasmSummary=1: the END of the list is what compiled mid-run). The fixes
  are structural: tiers off, everything pre-compiled at start, no LINQ or spreads on per-frame or per-event paths.
- **A tiny animal's pace IS its species to the eye.** Ten body lengths a second switched on and off dead, with a ten-beat
  tail, read as a mosquito; five for half a second, seven beats, a coast to a stop read as a tadpole. When a complaint names
  a species, the speed and the beat are the first dials, judged on a 4x strip at the real rate PLUS a per-frame speed trace
  across the state change (the strip could not tell that the first fix had not run, the trace could: the previous state
  zeroed the value the next state was meant to ease).
- **A look complaint about an animal is located through the animal's OWN event log, then a dump at the log's dials.** "The
  new duck ... wings floating above the body" could have been the flap or the ride; stills on two seeds, the duck log at
  20x for the cute events' frames, then dumps at those frames and 4x strips named it in one pass: a duckling riding on its
  mother's back. Two cosmetic rescues judged on the same strip, then the feature came out of the dice (its code kept, its
  roll kept so the scene's dice hold). Deleting a behaviour is a legitimate fix when its drawing cannot carry it.
- **A helper's cute or event animation gets a 4x strip before the merge, not after his look.** The ride had been built by
  a helper, measured for overlap and shudder, reviewed by the nemesis for solidity, and never judged by eye at 4x; it reached
  him. Every event an agent builds is on a strip in the brief's deliverables.

## Field addition (2026-10-26): motion proved is not motion seen, one painter term is not the line, and a rules file that ate its own loop

Sakura Pond, rounds twenty-eight to thirty in one day (a living shoreline, the snake's orbit, the deep, the frogs), and
"fix claude.md" before any of them.

- **Motion proved is not motion seen.** The first lapping water's edge moved 3 px up the sand and back; a pixel trace down
  one column across two frames proved it, and the 8x strip and the change map showed nothing, because the flooded sand took
  the water's colour and the bared sand the dry colour: each frame alone was a rest frame. Motion that leaves no trace is
  invisible. A wetness memory (dark sand drying over six seconds) made it readable and the change map count rose from near
  zero to 102,000 pixels. Two numbers, in order: the trace that proves the thing moves, then the between-frame change count
  over seconds that proves an eye could see it move.
- **One painter term found is one term.** "The boundary goes over the rocks" was located, before coding, to the rock wrap's
  wide rim mix; that term was rewritten and the crops showed solid stones with the water round them, so the round was called
  done. Two other terms drew the same bank curve across the stone's face and the complaint came back in the same words. After
  locating a line, grep every pass that paints near that curve; and verify a line complaint by the line's ABSENCE at the
  pointed spot on the fixed build, with the fix's own change map tracing along the line he named, never by the presence of
  the new feature. [EP-162]
- **The loop's own notes can eat the loop.** The project's rules file took a diary entry per round until it was 184,591
  characters, 4.6 times the tool's "large file" warning, and the warning printed to the human at every session start, never
  to the agent appending. Rules and diary split, a size FAIL in the verify step, and two rounds later the rules file was 122
  characters under its own cap: a ceiling without a rule for what leaves is a reminder. Every addition moves an older passage
  out verbatim; a harvest that ends within 10 percent of the cap prunes first. [EP-161]

## Field addition (2026-10-28): a motion complaint is located in the logs by distance to the named thing, a metric is checked against the picture it claims, and a fix that slows a thing shrinks its probes

Sakura Pond, round thirty-nine: "the fish get all janky [near the rocks] and so do other animals. also make the snakes
look more natural. drop the checkered one."

- **Split by distance to the thing he named, on the last build's own logs, before any render.** Every motion number
  (nose jerk, turn-rate change and its sign flips, speed and depth steps, the sharpest drawn bend, refusals by cause)
  within 0.08u of a stone against the rest, per animal. It found two stutters that no standstill count would have
  (a 60 Hz freeze-and-step up a flank; a tail beating at full cruise against a shoulder) and cleared the turtle in
  the same pass. One table, one pass, the place and the animal he meant.
- **A number is checked against the picture it claims before it is a finding.** Two of the split's numbers were
  false leads: the turn-rate flips were a climb flag flickering on a fish whose heading drifted smoothly, and the
  spine kink was the tail fin's four points. The order that held: split by distance, trace the worst episode frame
  by frame with the rule's own inputs, then crop the trace at 4x. The trace is what says "this is the jank".
- **A fix that slows a thing shrinks every probe measured in its steps.** The first fix (a refused fish slows to a
  crawl) exposed a 115 s jam because the probe for a way out reached a fifth of a pixel. Every probe gets a floor
  in pixels, and every fix pass is a whole set again at both sizes: three of this round's three builds found a
  second cause.
- **The look change rode on the same instruments.** The snake's redraw (a head and neck, a round body in rows of
  scales, soft marks, the body a hair under) was judged on 4x crops of the old and new build at the log's own
  surface windows, two skins of the four; the two unseen are named as unseen in the handoff.

## Field addition (2026-10-30): "look at some photos" is a brief about the common denominator, a palette is chosen by its OUTPUT, and a new kind reuses the old body

Sakura Pond, round forty-four: "the underwater look and the terrain need work. look at some online photos or something to
get a better idea. also, i want a little more activity in the "deep sea" areas ... add something else down in the deep
that im forgetting."

- **Locate first, then look at the photos for what EVERY one has in common.** The published render said what was wrong in
  two nouns (a flat teal field with a scatter of dark discs; a boulder on a bald lit dome ten times its width). Two image
  searches then named the brief: every real pond bottom is a carpet of DISTINCT things, each lit and shaded, algae on all
  of them, leaves, twigs, rubble at a boulder's foot, and the water is green. The lesson that generalises: a field with a
  grain (dots, noise) reads as paint; a carpet of individually lit objects reads as a place. Write the common denominator
  into the round's notes before any constant moves, so the next "more" has an anchor.
- **Under a dimming filter, pick a palette by what the filter OUTPUTS, not by the input colour.** Two catfish palettes
  vanished on the bed: the depth rule keeps 0.14 of red, 0.4 of green and 0.48 of blue, then mixes 0.62 of water, so every
  mid tone lands within a few levels of the silt. Making the fish paler moved it by the same few levels. What read was
  CONTRAST inside the thing (a dark back against pale mottling) and a smaller share of the filter. Compute or sample the
  filter's output at the depth the thing lives at before choosing its colours.
- **A third kind reuses the body and the mind; what it needs of its own is its WALLS.** The catfish was the koi's enum,
  dice weights and a constructor branch. Its two real lessons were steering: a bottom dweller lives within a hair of its
  own depth cap, so a clearance floor derived from that cap makes every hollow a wall (it yo-yoed), and a floor that
  follows its depth down a slope keeps the slope open (it climbed a boulder). One fixed floor and no climbing fixed both;
  found in the first logged runs, before any strip.
- **A pixel gate that cannot pass is not a failed gate; prove the invariant another way.** The water's colour changed on
  every water pixel, so the same-scene gate read 67 percent different. The dice were proved unmoved by the start logs
  (the island, the formations and the log at the same places in old and new), and only then were the behaviour numbers
  compared.

## Field addition (2026-11-02): a page he reads gets agents' screens before his eye, stills lie about animation, and a look handoff is one line plus the page opened

A project tracker page, two rounds in one evening. The first cut, built by a Sonnet agent to a brief that said
"concise", came back "pathetic no-pizazz page ... i know you're holding out on me". Three things that generalise:

- **The design is the main session's; the build and the judging are delegable.** A builder briefed with "concise" for a
  page the owner will look at produces a plain page every time. Draw the design yourself from the owner's own taste rules
  (here: pastel tokens, visible edges, faint pulsing line art never on text, motion only where data moves, toys that
  reveal the data, a replay button and a speed dial), then delegate. Before the owner's eye, two cheap agents: a Sonnet
  screen of the full-page screenshots in both themes for OBJECTIVE items (overlaps, clipping, contrast, edges, alignment:
  five real defects and one wrong call in 82K) and a Haiku cold read of the text render for the words (92K). The owner's
  standing ask is non-frontier wherever quality holds; this is where it holds.
- **A headless still lies about anything animated.** Count-ups are caught mid-count, staggered reveals show their first
  item only, actors on wires are invisible. The Sonnet screen read the mid-count numbers as a data change. Two rules:
  the HTML carries the final value and the script animates toward it, so a still is never wrong; and a page probe drives
  the page (CDP, a fixed profile folder) and asserts the motion: an actor's position sampled across frames rises along its
  wire, the padlock shuts, hover picks the pane, the rings fill, every timeline entry reaches opacity 1. The probe's first
  FAILs were the instrument both times (the animator pauses off-screen and the probe had not scrolled; a regex evaluated
  in the page came back NaN through CDP): parse outside the page, scroll first, and read the raw attribute before fixing.
- **A look handoff is one sentence and the page opened in the owner's browser.** Three tables of who judged, routing
  and what only he can do got "im confused on what im supposed to be looking at rn". Open it for him (`Start-Process`),
  say what it is in one line, say what you want from him in one line. Status tables are for "how we doing" (EP-236).

## Field addition (2026-11-02, night): the debug build is the first render, and a tone is set by the painted pixel

Sakura Pond, three builds of a one-pixel sparkle tuned on crops that showed nothing, then one build with every flash
forced solid white that settled "does it reach the frame" in a single render. Then a rock's underwater foot painted at
three greys that all read pale, because the light net lifted that ring 25 levels and the constant typed was not the tone
painted; sampling the foot against the bed beside it found the grey in one step. Three rules, each cheap:

- **A per-pixel or soft effect's FIRST render is the solid-colour debug build**: every pixel it would touch at full alpha,
  counted. A count from the effect's own loop ("on: 30") says the code ran, not that an eye gets anything.
- **Thresholds on a generated field come from its histogram**, logged in the effect's own header (the net's brightest 1.5
  percent is a node, its brightest 0.2 percent is white), never a guessed level (185 passed 0.4 percent of the page).
- **A tone is set by sampling the painted result against its neighbour**, moving the input until the measured difference
  is the one wanted; anything downstream of the constant (a depth rule, a light pass) makes the constant's value a guess.

And the morning's rule from the same project (a fix that works only by enlarging or recolouring a shape has a constant
upstream) failed to fire that night on the same constant in a new shape, a column instead of a tombstone. Index such a
rule by the LEVER ("the slant is the first lever for anything too tall below the water"), not by the shape it last made.

## Field addition (2026-11-03): a cure reroutes the simulation, and three cuts on one probe name the architecture

Sakura Pond, round forty-seven. The snake's 90 degree corner was located to one frame before any cut (the head pivoting in a
crease while the body lay still) and cured in one build (sweep the laid body with the head, joint 177 to 6 degrees). Then the
measurement moved out from under the cure: the swept body changed the koi's paths, their touches changed the snake's startles,
and two seeds that had been clean stood 52 s and 279 s in jams of a probe written that morning. Four cuts on that probe's
acceptance rule in one evening, each curing one seed and jamming another, before it was parked.

- **A cure that changes an animal's path restarts the measurement.** In a deterministic world the start logs prove the scenery
  unmoved, so every jam that appears after the fix is LATENT (the new paths found it), not caused; it still gates the ship.
  Run the whole seed set after each cut and read the new jams as findings, not regressions.
- **Three cuts on ONE mechanism's acceptance rule is the signal, not the fourth cut.** Each cut was a margin or a tier in one
  test; the class of the test was wrong (a local room-gain probe cannot name the way out of a closed pocket). Park with the
  diff, the measure and the named architecture; ship the build that never carried the branch.
- **Three cures of three different mechanisms is ordinary work**, not the signal: the lizard's afternoon was a bask under a
  clump's leaves, a dash's first step into water and a jerky pivot, each located in the pixels, cured, measured and kept.
