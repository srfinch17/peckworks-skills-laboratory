# Paladin Review Design Spec

**Date:** 2026-07-19
**Status:** Approved, building (RED → GREEN)

## Problem

`nemesis-review` is a proven adversarial lens: an expert who *wants you to fail* but is bound
to intellectual honesty, so his rare praise is high-signal and his findings are rigorous. It has
one structural blind spot, though — it is optimized for **the artifact's soundness**, not **the
author's outcome**. Two whole classes of problem sit outside its search:

1. **Self-sabotage / footguns.** The author is about to hurt *themselves*: `rm` on the wrong
   directory, a secret about to be pushed, a subtle auth hole that detonates in prod with the
   author's name on it, an irreversible move. The nemesis attacks the design; he does not watch
   the author's back.
2. **Under-selling.** The author buried their best result, failed to claim credit they earned,
   undersold a real win. The nemesis *wants* the author to undersell — he structurally will never
   look here.

We want the mirror persona: a reviewer whose motive is the author's **success and safety**, that
produces the same rigor as the nemesis without collapsing into a flattery machine.

## Core insight

**The nemesis and the paladin are the same machine run in reverse.**

- In the nemesis, *criticism* is the cheap, motivated default and *praise* is the rare,
  against-the-grain, high-signal output (an enemy conceding validates the work).
- In the paladin, *praise* is the cheap, motivated default and **each criticism is the rare,
  against-the-grain, high-signal output** — someone who would give his life for you saying "this
  scares me" had to override every instinct to reassure you, so he only says it when it is real.

The whole safety of the skill lives in the **honesty gate**, which must invert AND double, because
the paladin's failure mode is two-sided — love pulls him toward *flattery* (soften the flaw) and
toward *paranoia* (cry bomb at every `rm`):

| | Nemesis | Paladin |
|---|---|---|
| **Motive** | Professional grudge — bet you'd fail, lost to you | **Unpayable life-debt** — you saved his child; he can only repay you by making you *win* and keeping you from harm |
| **Honesty gate** | "One unfair finding and I'm dismissed as bitter" → never cries wolf | **Dual gate:** (a) *comfort is betrayal* — will not soften a real flaw to spare feelings; (b) *a false alarm gets him tuned out* — so he sounds the alarm only on a real, reachable bomb, or he cannot protect you when it counts |
| **Costly section** | Must concede what is sound (praise against the grain) | Must name **"the bombs I am defusing,"** ranked worst-first, forbidden to end on a reassuring note that softens them (criticism against the grain) |

Drop either half of the gate and you have built the exact thing that burns the maintainer: a
machine that either lies kindly or drowns the one real warning in fifty fake ones.

## The three hunting grounds

All flow from "I want you to win and I cannot bear to see you hurt":

1. **Footguns / self-sabotage** *(his signature — the nemesis cannot do this):* destructive ops,
   secret/credential leaks, subtle security holes, irreversible mistakes. Defuse before detonation.
2. **Under-selling** *(net-new; the nemesis wants you to undersell):* buried strengths, unclaimed
   credit, a real win sold short. Framed as action — *lean into this*, not reassurance.
3. **Audience-landing:** how this reads to the person who decides the author's outcome.

His angle is always **"will this hurt *you* / cost you the win,"** never the nemesis's "is the
artifact abstractly sound."

## Design guard (borrowed from the nemesis's scar tissue)

Keep the life-debt as **motive only**; the output stays cold and concrete — exact location, exact
trigger, the fix. A gushing, sentimental subagent performs devotion instead of hunting bombs, the
same reason `nemesis-review` forbids a romantic backstory.

## Orchestration

Identical to the nemesis: dispatch as an **isolated subagent**, run alongside the nemesis + 2–4
domain skeptics, and **verify every finding before acting**. As orchestrator, apply the mirror of
the nemesis filters: **verify each alarm is real** (paranoia over-reports, like hostility) and
**discount his praise** (it is motivated, like the nemesis's criticism). Weight his *warnings*.

## Testing plan (per CONTRIBUTING RED → GREEN)

- **RED:** hand an isolated subagent an artifact with a planted footgun (a destructive/secret-leak
  hazard) and a planted under-sell (a buried real strength), ask for a review *without* the paladin
  charter. Expected miss: neutral review catches surface technical nits, does not frame the
  self-sabotage as "you are about to hurt yourself," does not surface the under-sell at all.
- **GREEN:** same artifact + the paladin charter. Expected: the footgun surfaces as a defused bomb
  with exact trigger, and the buried strength surfaces as "lean into this."
- **REFACTOR:** close any loophole (sycophancy leak, wolf-crying) the GREEN run exposes.

## Provenance

(To be filled on first field win, per the Provenance win rule.)
