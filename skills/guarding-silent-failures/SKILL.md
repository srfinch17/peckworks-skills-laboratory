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
  interaction and confirm the readout moves.

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

## The order to work in

1. Ask what would tell you if this were wrong. If nothing would, stop and add something.
2. State the expected number before running.
3. On a mismatch, diagnose by measuring the real artefact — not by re-reading the code.
4. Fix the cause, then assert the invariant so it cannot return silently.
5. Prove the assertion fires: break it on purpose once.

## Provenance

Distilled 2026-08-09 from a peckworks-cadmesh session that hit all of these in one day: a fillet
that ate 38% of a part and rendered fine, an AO pass that rendered pure black with no console
error (a missing `RenderPass` meant AO was multiplied over an empty buffer), an AO pass that then
"worked" and did nothing (normalised-depth units), a ridge probe that was blind to splines, a
cleanup that reported removing twelve files it had not touched, and a build check that was flaky
because `publicDir` copied 15MB of models into `dist/` on every run. Related skills:
[cadquery-modeling] for the geometry-specific traps, [look-driven-iteration] for output judged by
eye, [nemesis-review] for adversarial review before committing.
