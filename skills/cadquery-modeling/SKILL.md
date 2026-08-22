---
name: cadquery-modeling
description: Write and debug CadQuery/OpenCASCADE parametric CAD models in Python. Use when creating CAD geometry for 3D printing (peckworks-cadmesh model.py files or similar), when fillet() or chamfer() throws StdFail_NotDone / "BRep_API: command not done", or when a boolean-heavy solid refuses edge operations.
---

# CadQuery modeling

Shared venv, deliberately placed **outside** the cloud-synced tree to avoid sync churn — `~/.venvs/peckworks-cad/` (on Windows, `%USERPROFILE%\.venvs\peckworks-cad\Scripts\python`). A venv inside Dropbox/OneDrive gets thousands of files re-uploaded on every install.

## Picking the right edge (the second-biggest time sink)

Point-based selectors lie. A pocket contributes TWO identical circles (top rim and floor) plus vertical seam lines on its wall, and `NearestToPointSelector((r, 0, top))` picks the seam line — nearest by *centre*, not by "on this circle" — then `fillet()` dies with "There are no suitable edges". Identify edges by what they ARE, and assert the count:

```python
rim = [e for e in part.edges().vals()
       if e.geomType() == "CIRCLE"
       and abs(e.Center().z - TOP_Z) < 1e-6           # height separates rim from floor
       and abs(e.Length() - 2 * math.pi * r) < 0.5]   # size separates it from other circles
assert len(rim) == 1, f"expected 1 edge, found {len(rim)}"
part = part.newObject(rim).fillet(R)
```

Before guessing, print the edge table: `python tools/build.py <project> --edges` in peckworks-cadmesh dumps every edge with type, length, centre, z-span and radius. One look beats three selector attempts.

### When NO geometric test can work, select topologically

The recipe above (geomType + size + height) works on a circular pocket. On a **square or oval** pocket it is unusable, and so is any distance-from-centre test — which is the non-obvious part:

> On a 31mm rounded square with a 2mm rim, the POCKET's corners reach 18.8mm from centre while the OUTER edge midpoints sit at only 15.6mm. **The two boundaries overlap in radius.** No radial threshold can separate them.

And an offset ellipse is neither a circle nor an ellipse — it is a general curve, so there is no `geomType` to match at all. Ask the topology instead:

```python
tops = [f for f in part.faces().vals()
        if f.geomType() == "PLANE" and abs(f.Center().z - TOP_Z) < 1e-6]
assert len(tops) == 1, f"expected 1 top face, found {len(tops)}"
holes = tops[0].innerWires()            # ring opening + pocket
assert len(holes) == 2, f"expected 2 holes, found {len(holes)}"
pocket = max(holes, key=lambda w: w.BoundingBox().xlen)
part = part.newObject(pocket.Edges()).fillet(R)
```

This does not care what the curve IS. Assert the hole count so a changed topology fails loudly instead of filleting the wrong boundary.

## Offset arithmetic (rims, grooves, insets)

- **Offsetting a rounded rectangle inward by `w` reduces its corner radius by exactly `w`.** A 2mm rim inside a 3mm corner leaves a **1mm** pocket corner; another 1mm groove leaves **0mm** — square island corners. That is correct, not sloppy: the island's corner lands exactly on the centre of the pocket's corner arc, which is what makes the band a uniform width diagonally as well as along the flats. Typing the parent radius (or 0) measures right along the flats and pinches or bulges at the corners.
- **The offset of an ellipse is NOT an ellipse.** Shrinking the semi-axes is the obvious move and is wrong: at 2mm it gives 750.23mm² where a true offset gives 747.98, and the error is not evenly spread — the rim runs narrow at the ends and wide at the sides. Use `Workplane.ellipse(a, b).offset2D(-d)`.
- Workplane's `rect()` has no corner radius, so build a rounded band as one Sketch minus another: `rounded_rect(outer).face(rounded_rect(inner), mode="s")`.

## Curvature sets the fillet threshold, and it is a CLIFF

Where a protruding feature (a loop, a boss) meets a curved body, the junction angle — and therefore whether `fillet()` survives — depends on the body's LOCAL RADIUS OF CURVATURE at that point, not on the part's size.

For an ellipse the curvature radius at the end of the minor axis is `a²/b`. The same 28.58 x 42.87mm oval has a **9.53mm** top when portrait and a **32.15mm** top when landscape. Measured consequences on an identical arch:

| top curvature | seating inset that works | edge fillet at 0.5mm inset |
|---|---|---|
| 9.53mm (portrait) | **≥ 1.0mm** | eats **1890mm³** — 38% of the part |
| 32.15mm (landscape) | any of 0.5 .. 1.5 | correct, ~21mm³ |

It is a cliff, not a slope: 0.9 destroyed the part and 1.0 was fine. So **never carry an inset across a shape change** — re-measure it. And do not sit on the first value that works; that is the edge of a cliff.

Knock-on worth knowing: a deep seating inset drags the junction down beside the pocket rim, which then refuses its own fillet. Fixing the curvature problem fixed the rim fillet too.

## Failures that only appear in combination

A pocket-rim fillet raised `StdFail_NotDone` on the finished part while every ingredient was fine alone — plain slab OK, arch+opening OK, edge fillet OK, all three together FAIL. **A feature can be individually compatible with every other feature and still fail with all of them.** Test against the full stack, varying one ingredient, not pairwise.

## A finished part can refuse EVERY further fillet

OCCT will not round the edge of a round. Once a part has had a blanket pass like
`edges(">Z or <Z").fillet(0.6)`, its top and bottom edges all bound fillet surfaces and further
filleting fails outright with `There are no suitable edges for chamfer or fillet` — including via
the ordinary string selector. Measured on three finished parts, each rebuilt with its own final
pass disabled:

| part | as finished | same part with `EDGE_ROUND = 0` |
|---|---|---|
| disc + pocket + groove | `edges(">Z").fillet(0.1)` **FAIL** | **OK** |
| disc + arch loop | **FAIL** | **OK** |
| rounded square | **FAIL** | **OK** |

This is geometry, not a bad selector and not a broken mechanism — the identical call on an
imported STEP with no prior fillets succeeded on 4 of 5 edges, and on a plain box every time.

Consequences worth planning around:
- **Any interactive "click an edge and fillet it" tool will refuse on already-rounded parts.** Say
  so in the UI, or it reads as a broken button.
- If edges need to stay editable, leave the blanket pass off and apply rounding last, or make it a
  parameter that can be disabled.
- A per-edge refusal is normal too and must be reported per edge, not as a whole-part failure.

## Cut order decides what can be rounded

`fillet()` applies to whatever edges exist when it runs, so the ORDER of cuts sets which rims can be rounded:
- Want a hole's rim rounded with the outer edges? Cut it BEFORE the fillet, in the same `edges(">Z or <Z")` pass.
- Want it left crisp (or it is too small to fillet)? Cut it AFTER.
A 2.4mm hole rim refused every fillet; the same part at 5.4mm across took 0.6mm without complaint. Small rim + fillet = expect failure, and prefer cutting it last.

## Verify by arithmetic, not by "it built"

**Free floor: `Shape.isValid()`** (cadquery 2.8 wraps OCCT's `BRepCheck_Analyzer`). OCCT returns structurally broken solids — an open shell, a self-intersecting face — that still report a `Volume()`, still tessellate, still export, still render, and only fail in the slicer. One line before the export catches that whole class:

```python
if not solid.isValid():
    sys.exit(f"INVALID SOLID: {project} failed BRepCheck_Analyzer. Nothing exported.")
```

Word it as `valid: True`, never as "verified" — a geometrically *wrong* solid is still perfectly valid, so this is a floor, not a verdict. Prove it fires: a box shelled with one face dropped and sewn back into a solid reports `Volume() = 800.0` and trips it.

A wrong solid raises no exception. Check volume against a hand-computed expectation (`π r² d` for a pocket) and watch the volume DELTA between builds — a bad fillet can silently eat 400mm³ (measured worse: **1890mm³, 38% of the part**) and still return a valid solid that renders as a plausible object. State the number BEFORE the build; a prediction made afterwards is fitted to whatever came out. Cheapest possible catch; do it every build. See [guarding-silent-failures].

### Volume is NOT reproducible across processes; topology COUNTS are — ORDER is not

Three separate runs of unchanged code on the same part gave `3709.0172546784365`, `3709.0125436416643` and `3709.0181316673766` — a spread of ~0.006mm³, because OCC's internal ordering shifts with memory layout. Face and edge counts were 19/36 every single time.

So:
- **Never compare volumes with `==`**, and never to more than about two decimals.
- **Compare topology by equality and volume by tolerance.** 0.05mm³ works at keychain scale: ~10× the jitter and still ~2600× smaller than a feature worth detecting.
- A committed build stamp will not match a fresh rebuild exactly, and that is fine. Any scheme that verifies a restore/checkpoint by re-running the build must be written this way or it fails at random and teaches everyone to ignore it.

**But do not read that as "topology is reproducible".** The same non-determinism *permutes the sequence*: two runs of unchanged code both returned 36 edges and put a **different edge at index 3**. This is more dangerous than the volume jitter, because an index looks exactly as stable as a count and is not.

**An edge index is never a selector — not in a script, not in a saved UI edit, not in a config.** Anything that persists `edges()[7]` silently addresses different geometry on the next build. Store what the edge *is* and re-find it:

```python
def edge_id(e):                       # collision-free across every part tested
    c = e.Center()
    return [e.geomType(), round(e.Length(), 2),
            round(c.x, 2), round(c.y, 2), round(c.z, 2)]

hits = [e for e in shape.edges().vals() if matches(edge_id(e), want, tol=0.05)]
assert len(hits) == 1, f"expected 1 edge, matched {len(hits)}"
shape = shape.newObject(hits).fillet(r)
```

`0.05mm` tolerance is ~8× the observed jitter and far below any real feature. Assert the match count — this is the same rule as "assert the inner-wire count", arriving through a different door.

### Face-count deltas: what fused, and what merely looks alarming

Cutting a groove flush to a pocket wall raises the question fused-or-hairline-ridge, and the counts answer it. But the expected delta depends on how many faces the boundary has:

- circular pocket: **+2 faces / +3 edges** = fused (a ridge gives +3/+4)
- rounded-square / rectangular pocket (8-segment boundary): **+5 faces** = fused (a ridge splits each of 8 wall faces, giving +13)
- offset-ellipse pocket (4 spline faces): **+9 faces**, which LOOKS like the ridge signature and is not

For the ellipse case the +9 is 1 groove floor plus 8 walls between the two floor levels (4 outer, 4 island), with the outer groove wall and the pocket wall above being one surface split into two faces. Account for every face before calling it a defect — and note that a hairline ridge has zero volume, so the volume check cannot arbitrate.

## The sketch-first rule (the big one)

Never union separate coplanar extrusions to build one part. The fused shared face is subtly corrupt, and any later `fillet()`/`chamfer()` touching its edges throws `StdFail_NotDone` — often asymmetrically (top face works, bottom fails), and `clean()`, flipping the solid, and switching to chamfer all still fail. Fuse the outline in 2D instead:

```python
profile = cq.Sketch().circle(r1).push([(x, y)]).circle(r2)  # fuses into ONE face
part = cq.Workplane("XY").placeSketch(profile).extrude(t)
part = part.edges(">Z or <Z").fillet(0.6)                   # now works
```

### The SILENT variant — the same corruption that never raises

`StdFail_NotDone` is the loud form. The quiet form removes **nothing at all**, and it is worse.

Cutting with overlapping tools built in one call produces a corrupt compound. The `cut()` then
succeeds, returns a valid solid, exports cleanly, and the volume is **unchanged**:

```python
# WRONG - the circles overlap each other, so the compound is corrupt
cutter = cq.Workplane("XY").pushPoints(pts).circle(r).extrude(h)
solid  = solid.cut(cutter)          # removes 0.0 mm3. No exception. isValid() True.
```

Measured on a fluted wall: scoops 0.55mm deep and 3.3mm wide, cutters of radius 2.7mm at
3.7mm centres. The *bites* did not overlap — a clean ridge survived between them — only the
cutter cylinders did, out behind the wall where nothing was being cut. That is enough.

```python
# RIGHT - one tool at a time, and assert the material actually moved
before = solid.val().Volume()
for pt in pts:
    solid = solid.cut(cq.Workplane("XY", origin=(0, 0, z0)).center(*pt).circle(r).extrude(h))
removed = before - solid.val().Volume()
assert removed > 0.5 * expected, f"cut removed {removed:.1f}mm3, expected ~{expected:.0f}"
```

**The rule that covers both forms:** overlapping geometry may only be fused inside ONE
`cq.Sketch()`. Anywhere else — a `pushPoints` extrude used as a cutter, a union of coplanar
solids — assume it is corrupt and prove otherwise with a volume delta. A boolean whose result
you did not measure is a boolean you did not verify.

### Two cuts sharing one wall will meet

When one feature cuts a wall from outside and another cuts it from inside, write the sum down
and assert it. A wall fluted 0.55mm deep from outside and grooved 1.3mm deep from inside is
1.85mm of removal from a 1.8mm wall: the flutes punched a neat row of holes into the groove.
Every part rendered and exported fine. `FLUTE_DEPTH + SLOT_D < WALL`, asserted, is the fix.

## An interpolating loft OVERSHOOTS where you sampled sparsely

`Solid.makeLoft(wires, ruled=False)` fits a smooth surface **through** your wires — so between
two distant wires it behaves like a spline and **bulges past them**. Sample unevenly and the
sparse span is where the error lives.

A scoop lofted through z-levels clustered at its two fades, with a 5.7mm unconstrained gap down
the middle, cut **0.696mm deep where the constant said 0.55** — 27% over, on the part's signature
feature. `isValid()` passed, the STL exported cleanly, the render looked right. Only sectioning
the solid and walking the profile found it.

```python
cq.Solid.makeLoft(wires, False)   # smooth: splines THROUGH the wires, overshoots the gaps
cq.Solid.makeLoft(wires, True)    # ruled: linear between wires, cannot overshoot
```

**Rule: if you generate the wires yourself, use `ruled=True` and buy smoothness with level
density instead.** Then the shape is exactly what your formula says, the depth guard is
predictable, and smoothness is a knob you control. Reserve smooth lofts for wires you did not
choose the spacing of. Same hazard in any construction that interpolates points you supply —
splines, sweeps, easing curves.

## Tangency, not width, decides whether two scoops leave a ridge

A circular arc meets a flat wall **at an angle**. So whatever survives between two circular
scoops is a flat strip with a hard shoulder either side — a *ridge* at any spacing. Narrow the
gap and you get a thinner ridge; close it completely and you get a cusp. There is no width that
yields a rounded crest.

For a continuous wave, the profile must reach zero **depth and zero slope** together. A raised
cosine over the pitch does:

```python
bite = amp * (1 + math.cos(2 * math.pi * (t - 0.5))) / 2   # t: 0..1 across one pitch
```

Consecutive scoops then hand off tangentially and the surface reads as one wave. Measured: wall
within 0.05mm of full crest went 2% → 22%. **The width constant was deleted, not retuned** — with
a cosine spanning the pitch there is no width to choose. When a complaint names a *character*
(smooth vs sharp, wave vs peak), ask which mathematical property produces it and whether your
current form can express it at all.

## Export tolerance is part of the model's correctness

`cq.exporters.export(shape, path)` defaults to **0.1mm** linear deviation. That is invisible on a
35mm disc (0.3%) and fatal on a 0.55mm relief (18%) — the same number, right and wrong depending
on the subject, which is why it goes unexamined for months.

```python
cq.exporters.export(shape, str(stl), tolerance=0.02, angularTolerance=0.06)
```

**Compute deviation ÷ smallest feature before believing a "faceted / pixelated / stepped"
complaint is about geometry.** Fix it at the shared exporter so every part benefits; triangles
are cheap (18k → 49k, 2.4MB here).

## Edge-treatment robustness order

1. Fillet on a sketch-first solid (works when topology is clean).
2. Chamfer (more robust in OCC; also better for printed bottom edges — counteracts elephant's foot).
3. Restructure the geometry (e.g. round concave 2D corners before extruding).

Beware: `Sketch().vertices().fillet()` grabs invisible circle SEAM vertices (points on a smooth curve — nothing to fillet) and fails. Select the vertices you mean, never all of them.

## Debugging StdFail_NotDone

Don't iterate blind on the real script. Write a throwaway probe: a `base()` builder plus a list of `(name, lambda)` variants, try/except each, print OK/FAIL. One run isolates the poisonous operation — this is exactly how the sketch-first rule was discovered.

## Derive sizes, never type them

Where a family of parts has to share a property (equal face area, a fixed clearance), solve for
the dimension instead of writing it down. A rounded square of side `s` loses `(4 - pi) * r^2` to
its corners, so `s = sqrt(TARGET_AREA + (4 - pi) * r**2)` keeps the face constant whatever corner
radius is later chosen; the same solve with an aspect ratio gives the rectangle, and
`a = sqrt(TARGET_AREA / (pi * ASPECT))` gives the ellipse. Twelve blanks across four shapes then
hold the same 962.113mm² face to within 0.0002%, and turning one landscape is a ONE-constant
change (`ASPECT = 1/1.5`) with every other dimension re-solving.

The same applies to constraints, not just sizes. "The logo must sit below the rim" belongs in the
model as a clearance from which the extrude height is DERIVED — not as a height that happens to
work for one pocket depth. The first version stated the height directly and was correct only
relative to that pocket depth; expressed as `THICK - LOGO_BELOW_RIM`, it cannot silently break
when an unrelated dimension moves.

Useful cross-check: rotating a rounded rectangle 90° must not change its volume, because both its
area and its perimeter are symmetric in width and height. Getting a different number means
something else moved.

## Standard model.py shape

Constants in mm at the top with plain-name comments → `build()` → `cq.exporters.export()` to both STL (printable mesh) and STEP (editable B-rep) → headless PNG preview via `shape.val().tessellate(0.2)` + matplotlib `Poly3DCollection` (Agg backend). Worked example: `peckworks-cadmesh/projects/keychain/model.py`.
