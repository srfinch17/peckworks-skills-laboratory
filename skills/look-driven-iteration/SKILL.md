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

## When smoothing keeps failing, the eye is rejecting a SHAPE

A defect that survives multiple continuity fixes (smoother fades, softer edges, C2 kernels) is
not a continuity artifact - the eye is classifying a shape. A uniform radial narrowing band
reads as a lathe mark no matter how infinitely smooth its edges are. At that point stop
engineering smoothness: either put the shape lever itself in front of the owner (feature vs no
feature, measured beforehand to actually remove the complaint), or redesign so the feature is
carried by the structure the owner's green lines describe.
