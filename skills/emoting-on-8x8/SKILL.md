---
name: emoting-on-8x8
description: Design legible expressions and custom animations for the ESP32-S3 8x8 LED matrix (Claude's expression channel — matrix_express / matrix_animate / the CANNED library in mcp_server/expressions.ts). Use whenever creating, redesigning, or debugging a glyph or animation that has to read on the physical 64-pixel panel — including when an expression "doesn't read," looks like one flat color, flickers, or freezes the board.
---

# Emoting on the 8×8 panel

The matrix is Claude's expression window. The hard part isn't drawing — it's that a
64-pixel panel running at **brightness 5** can show almost no detail and almost no
color nuance. Everything here exists to make a human identify the thing **at a glance**
(the silhouette test). You can't see the LEDs; the user is your eyes — fire, ask, iterate.

## First decide: expression or firmware?

Two build paths — pick before you start, because they deploy completely differently:
- **Frame-based expression** — a glyph/loop you author pixel-by-pixel and push as frames.
  Design it HERE with `matrix_animate`, `save_as` to ship. Zero deploy, instantly
  reversible. Use for emotes, status, wait/idle bits — anything ≤24 hand-drawn frames.
- **Firmware animation** — a generative real-time mode (fire, particles, snow, anything
  parametric or endless). That's a new `anim_*.ino` and needs a **flash**. **Switch to the
  `add-animation` skill** for the 6-step wiring — then come back here for the *legibility*
  craft (brightness bands, silhouette, color choice) while you design the look.

Rule of thumb: **you author the pixels → expression; the board computes them → firmware.**
The three tiers below are all within the *expression* path.

## The iron rule: iterate live, promote winners

There are three tiers, with very different costs. Don't prototype in the expensive one.

| Tier | How | Cost |
|---|---|---|
| **On-the-fly** | `matrix_animate` (raw frames) | zero — instant, primary path |
| **Saved** | `matrix_animate` + `save_as` → JSON on disk | zero rebuild/restart (read at runtime) |
| **Canned** | edit `mcp_server/expressions.ts` → `tsc` | **rebuild + Claude Code restart** |

**Always design with `matrix_animate`.** Get it right live, then either `save_as` it or,
for core vocabulary, paste the final frames into `CANNED`. Editing `CANNED` to prototype
forces the slow restart cycle. Trick: to preview a `CANNED` edit *without* restarting,
re-send the identical frames via `matrix_animate` — the running MCP server keeps serving
old `dist` until CC restarts, so `matrix_express` won't match source until then.

## Mind the brightness-5 thresholds (the #1 cause of "it looks wrong")

The panel usually runs at bri 5. FastLED then scales each channel by 6/256, so a channel
only lights if its value ≥ ~43, leaving just **5 visible levels**. Two consequences bite
constantly:

- **Hues collapse.** red→orange→yellow become nearly one color (orange dies between
  them). For 3 distinct warm shades use **white-hot / yellow / red** (add the blue
  channel for the hottest). For red+orange, push orange green up to ~`#ff8c00` so it
  clears red.
- **Near-equal colors merge.** A cyan window `#bdf4ff` is invisible against a white hull
  `#ffffff` (both ≈ all-channels-max). Use a real **blue** `#2060ff` so it separates.

**Rule:** pick colors that differ in *which channels* are lit, not in subtle hue. For a
brightness gradient, pin levels to band centers so each is distinct on hardware:

| Want level | Channel value |
|---|---|
| 1 (dim) | 64 |
| 2 | 107 |
| 3 | 149 |
| 4 | 192 |
| 5 (bright) | 235 |

If a hue genuinely won't separate, say so — it needs brightness > ~15 — and let the user
choose rather than shipping mud. (See `docs/LED_BRIGHTNESS.md`, `CLAUDE.md`.)

## Static glyphs: downsample, don't freehand

Hand-drawn 8×8 icons look like blobs. Instead: take a **real reference icon**, picture it
solid (flood-filled), and shrink it to 8×8 keeping the **silhouette**. One bold subject,
≤3 colors, dark background, no 1-pixel details, no text beyond ~2 chars. Found a great
starter set already in `data/sketch.html` (the paint app's `STARTERS` — rocket, heart,
star, etc.); reuse those shapes.

**The fast path when the user hands you a reference image** (this nailed the Claude-mascot
alien in minutes): don't eyeball it — run a throwaway Python script.
1. **Mask on the subject's color, not alpha.** Exported PNGs usually have a *solid opaque*
   background (often black), so alpha-masking selects the whole frame — threshold on the
   fill color instead.
2. **Crop to the mask's bounding box**, then box-average the binary mask into 8×8.
3. **Print BOTH a thresholded `#/.` map AND a 0–9 coverage map.** The coverage numbers let
   you hand-judge the borderline cells (eyes, legs) the threshold flips — then snap the key
   *features* by hand (e.g. force the eyes dark even if the average filled them).

**Lock the static resting pose — proportions AND color — to the user's eye BEFORE adding any
motion.** Animating a pose that doesn't yet read just multiplies the iterations; nailing the
static frame first is why the motion then worked first try.

## Animation: motion and contrast carry it, not detail

- **Motion makes the silhouette.** A "busy/working" indicator reads far better as a
  comet traveling a clear path than as discrete state-hops. Give it directional travel.
- **Bursts/explosions flicker — don't morph a shape.** An expanding firework (each frame
  a different concentric ring) reads as disjoint flicker. Switch to a **steady-motion
  field**: falling confetti, drifting mist, a sweep. Celebration reads through color +
  continuous motion, no fragile silhouette needed. Make it loop seamlessly (shift every
  row by 1 each frame over N frames).
- **Attention-grab = photo-negative blink, not on/off flash.** Alternate the glyph with
  its inverse (every lit cell off, every off cell lit), ~3 blinks, then settle on the
  solid glyph (last frame, `loop: 1`). Reads as a deliberate "look here," far calmer and
  clearer than blanking the panel.
- **Animate a character by moving its negative space.** The dark holes (eyes) are the
  cheapest expression on 64 px: slide the 2 eye-pixels left/right = "looking around";
  remove them (eyes→solid) = a blink. No new pixels, no silhouette risk.
- **Translate the whole silhouette ±1px; never deform it** — keep a blank margin row so the
  shape has room to move. A 1px vertical bob + a blink reads as "alive/working"; a 1px
  horizontal sway + eye-darts reads as "idle/playful." So give **sibling animations of the
  same character different motion axes** and they read as genuinely different moods.
- **Fake brightness gradients with one hue at fixed steps.** Bake the dim values into the
  hex (per the band table) rather than relying on FastLED dimming, so trails/glows
  survive bri 5.

## Generate complex animations with a script — don't hand-place pixels

For shimmer/particle/gradient effects (e.g. a Frostbite-style sparkle: an icy mist field
plus points fading on sine-bell curves), write a throwaway Python script that emits the
`{colors, frames}` JSON for `matrix_animate`. Hand-placing 24×64 pixels is error-prone; a
generator nails timing, loops cleanly via modular time, and lets you re-roll. **Quantize
the generator's brightness to the band-center values above** so 3+ shades stay visible —
the first instinct (linear scaling) drops dim levels below threshold and collapses to one
color. Mirror the firmware's real effects when one exists (`anim_frostbite.ino`,
`anim_fireworks.ino`).

## Keep payloads light — heavy frames can crash the board

`/api/display/frames` parses the whole payload with an elastic JSON doc on top of the
request body — a near-max 24-frame, full-panel animation is a ~20 KB transient heap spike.
On a tight heap this trips the firmware's low-heap auto-restart (`esp32_matrix_webserver.ino`)
and the board freezes. **PSRAM must be Enabled** (Tools → PSRAM) — that's the real fix and
the usual culprit. Even so, prefer **few frames and sparse lit pixels**; reach for 24
full-panel frames only when the effect needs it. If you must reproduce a crash to debug,
do it **with the Serial Monitor open** and watch the `[heap] free=…` line — never blindly
re-fire a known crasher.

## Workflow checklist

1. **Design live** with `matrix_animate` (start light; pick colors per the band table).
2. **Fire and ask** — the user is the eyes. One change per state; no spam.
3. **Iterate** on their feedback (motion? contrast? pacing? does it read at a glance?).
4. **Promote the winner**: `save_as` for one-offs, or paste into `CANNED` + `tsc` for core
   vocabulary (then remind the user a CC restart is needed for `matrix_express` to serve it).
5. **Record** what the user likes/dislikes in auto-memory.

> **Live-preview gotcha:** the `UserPromptSubmit` hook fires a wait spinner on *every* user
> message, so whatever you're previewing is overwritten the instant the user types — expect
> to re-fire ("show again") between rounds. It's the hook doing its job, not a bug.

> **The long game (display-agnostic):** the *principles* here — thinking in a semantic
> message, the at-a-glance/silhouette test, iterate-live-promote-winners, motion-carries-
> meaning — transfer to **any** renderer; only the brightness-band/FastLED/downsample
> specifics are 8×8. The presence protocol's "one message, many renderers" is where this is
> headed. Extract a device-agnostic parent skill **when a second renderer earns its own
> emote-design work — not before** (one example can't tell you the right seams).

Spec: `docs/superpowers/specs/2026-06-11-claude-expression-display.md`.
