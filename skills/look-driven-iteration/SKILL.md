---
name: look-driven-iteration
description: Use when verifying fixes, debugging visual issues, or checking system behavior — ensure you measure and verify against what the downstream consumer actually uses, not a proxy metric that may share the same defect.
---

# Look-Driven Iteration

## Overview

Bugs hide in the gap between what you measure and what the user sees. A metric can report "fixed" while the visual glitch remains, or a guard can say "safe" while the blast radius escapes — because the instrument shares the defect's assumption about what matters.

This skill enforces a single discipline: when a fix needs verification, measure against the actual downstream consumer — the renderer, the slicer, the display, the user's gesture — not a proxy that runs parallel to it. Corollary: when a metric and a human report disagree, the human is describing the real consumer.

## Verify against what the consumer consumes

A fix "verified" against a quantity nobody looks at is not verified. Two failures from one session, same shape:

- A 3D viewport flipped the model on screen. The rotation guard measured the camera's angle about the orbit PIVOT; the thing that actually flips the picture is the camera's angle about the LOOK-AT point, which is what `lookAt()` consumes. Those are equal until the user pans — exactly the case being reported. A probe built on the same wrong quantity reported "0.0 degrees of swing" at every drag speed, and the bug was still there. The fix was invisible to the instrument because the instrument shared the bug's assumption.
- A CAD part built without error and looked plausible, but the profile was wrong (a circle unioned with a rectangle still hangs below the intended flat). No exception, no visual tell at a glance. Arithmetic caught it: expected removed volume vs actual.

The rule: identify the quantity the DOWNSTREAM consumer actually uses - the renderer's look-at vector, the slicer's solid volume, the pixels on screen - and verify against that one. Corollary: when a metric and a human report disagree, the human is describing the real consumer; your metric is a proxy that may share the defect.

And the cheap habit that catches both: for anything judged by eye, reproduce the user's exact GESTURE and look at the frames before claiming a fix. Numbers are supporting evidence, never the verdict.

## Predict the number BEFORE you build, then compare

State the value you EXPECT, in advance, then run the thing and compare. A number produced afterwards gets rationalised against whatever came out; a number committed to beforehand is a test that can actually fail.

It is nearly free and it converts "it built" into "it's right." A CAD groove: predicted π(15.5²−14.5²)×1.0 = 94.25mm³ removed, actual 94.2. A screen-space stroke traced across a part of known width: predicted 25mm, measured 26.2 — close enough to confirm the projection math, with the 1mm gap explained by eyeballing an edge off a JPEG rather than by a defect. Both took one line of arithmetic.

When the prediction and a rough visual estimate disagree, trust the arithmetic and go find the estimate's error.

## Pick an instrument that discriminates the thing in question

Match the quantity to the question, and notice when your usual instrument cannot distinguish the outcomes you care about:

- **Magnitude questions** ("did the right AMOUNT change?") → volume, byte count, row count, duration.
- **Identity/structure questions** ("did I get the geometry I MEANT?") → counts of parts: faces, edges, nodes, elements, routes.

A worked case: a groove cut flush against an existing wall could either FUSE with that wall or leave a hairline ridge standing. Volume blurs the two; the topology counts settle it outright. The build reported +2 faces / +3 edges — with **no new face at the shared radius** — which is the fused result. A ridge would have been +3/+4. The counts were already being printed and cost nothing; they simply had to be predicted and read.

## Prove the instrument is live before diagnosing the system

A readout that says "nothing happened" may mean your instrument stopped, not that the system is broken. Confirm the instrument moves at all before you start diagnosing.

A live telemetry pane in a browser app appeared frozen across several interactions: clicks dispatched, listeners fired, the camera seemed not to move. It nearly became a bug report. Nothing was wrong — the tab was backgrounded, so `requestAnimationFrame` was throttled and the pane had stopped refreshing, while screenshot capture still forced a paint and looked normal. Anything driving a browser through automation is exposed to this: rAF, timers, and animation loops are all throttled or paused in background tabs.

What settled it was the previous section's habit. After one real interaction, the resulting angles were exactly what that drag would produce **starting from the state the earlier click should have set** — proving the click had worked all along and only the display was stale. Arithmetic on the numbers you already have will often tell you which of the two is broken.

The rule: one real interaction, confirm the readout changes, and only then believe what it reports.
