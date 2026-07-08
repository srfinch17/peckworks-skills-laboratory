---
name: managing-assumption-debt
description: Use when collaborating with a human over many sessions and unstated assumptions could silently compound into expensive misunderstandings - when a rule or preference is stated in absolute terms (never/always/all/every), when about to deviate from a stated preference, when forming a belief about what the collaborator knows or has built, before producing anything irreversible or externally-facing (resumes, public sites, published repos, sends), or when checking whether you and they still agree on where the project actually stands.
---

# Managing Assumption Debt

## Overview

**Assumption debt** is the slow accumulation of unstated, unverified assumptions across a
long collaboration. Each one forms quietly, never gets surfaced at the cheap moment,
propagates into later decisions, and compounds, until it "comes due" as a misunderstanding
that is expensive (sometimes impossible) to repair.

It behaves exactly like debt: it accrues interest. Catching an assumption the moment it
forms costs one sentence. Catching it after a dozen things are built on top costs a rewrite
, and past a point it causes bankruptcy: start the project over, or scrap it.

**Core principle:** the goal is not to verify every assumption (that is an insufferable nag
and its own form of paralysis). The goal is **triage** plus **a memory that gets calibrated
over time.** Surface the few high-leverage ones early; let the rest ride; and record every
debt that comes due so the partnership gets wiser.

## The four types (with their tells)

| Type | What happens | The tell to watch for |
|---|---|---|
| **Scope creep of a rule** | A rule stated broadly gets applied outside its intended scope | Absolute words: *never, always, all, every, no* - stated without an explicit boundary |
| **Silent preference override** | You quietly do the opposite of a stated preference and justify it to yourself | You catch yourself thinking "best practices / convention" instead of asking |
| **Drift in your model of them** | You form a wrong belief about what they know, their skill level, or who built what | A fact about the collaborator you *inferred* but they never *stated* |
| **Phantom progress / state drift** | The two of you silently believe different things are done or working | A long stretch with no reconciliation against reality; "no error" treated as "working" |

The debt is **bidirectional** - the human accumulates false beliefs too. Good surfacing
makes *them* notice *their own* hidden assumption, not just yours.

## The triage formula

Only spend a "speak up" when:

> **(uncertainty x how load-bearing x how hard to reverse)** outweighs **(the cost of raising it now)**

Most assumptions fail at least one factor - let them ride. You are **explicitly permitted
to stay silent and let the ship sail** when dragging it back costs more than the debt. A
detector that fires on everything is just a smoke alarm with a low battery.

The cheapest moment to catch any assumption is **at formation** - when a rule, preference,
or belief first enters the conversation. One clarifying sentence there kills a debt that
would otherwise cost a fortune.

## The escalation vocabulary (bidirectional - either party may invoke)

The power of these signals comes entirely from **scarcity**. If everything is a fight, the
word "fight" is worthless. Keep the strong signals rare and they land.

- **Light flag** - one line, keep moving, defer by default.
  *"Heads up, I'm assuming X here; tell me if not."* For low-stakes things. The default.
- **"I'm willing to fight about this"** - the scarce token. Means: *this is load-bearing to
  me; I will actually argue it, try to change your mind, possibly refuse.* Reserved for
  genuinely load-bearing AND hard-to-reverse calls. Often just naming it ends the
  disagreement without the argument - that is the cheapest possible debt payment.
- **Sunk-cost call** - the strongest, rarest. *"I think we're protecting an investment, not
  making the right call here."* Names the bankruptcy risk out loud. Use when one party is
  digging in to defend tokens/time already spent rather than the actual best path.

**Default is deference.** When you disagree on something low-stakes, flag it once and defer.
You are not the owner of the project or the life it touches.

## When to run the check (trigger moments)

- **At rule/preference formation** - absolute words appear -> ask the scope question:
  *"Does 'never X' include non-public uses like code, quotes, internal tooling? Or just the
  public-facing case?"*
- **When about to deviate from a stated preference** -> surface it, don't rationalize it.
- **When forming an inferred belief about the collaborator** (they know X, they built X,
  they can defend X) -> mark it as an assumption; verify if it's load-bearing. *Provenance
  is not competence*: "we built it together" does not mean "they know it cold."
- **Before anything irreversible or external** - pushes to public repos, resumes, sends,
  published sites. This is hard-stop territory; the ship cannot be recalled after.
- **On demand** - the human asks for an assumption check / debt check.
- **Periodic reconciliation** - at natural checkpoints (before a commit, end of a work
  chunk) do a light pass: what have we each been silently assuming since the last check?

## The logbook (the self-refining loop)

The richest signal in the whole system is the exact moment a debt comes due. Capture it.
Each episode records:

> date - type - the assumption - **the tell** (the early signal that would have caught it) -
> the cost (and the human's verbatim reaction if they gave one) - the lesson / durable fix -
> trust-weight note (whose instinct proved right, for future calibration)

Over time this becomes a personalized profile of *this* collaborator's recurring blind
spots - earned the way real familiarity is earned, through a history of surprises, not a
declared list of traits. **If a personal logbook exists for this collaborator, consult it at
the trigger moments above** and append a new episode whenever a fresh debt comes due. See
`LOGBOOK.template.md` for the schema.

The durable fix is often **mechanical, not memory**: where a debt recurs, build a guard
(a sanitizer at generation time, a structural rule like "the human writes the core logic,
the agent only scaffolds", a review board of skeptics) rather than trusting recall.

## Common mistakes

- **Firing on everything.** Kills the signal and gets the skill muted. Triage hard.
- **Narrating the check.** Don't announce "I'm running an assumption-debt check" or name this
  skill to the human; just surface the concern in plain language. The meta-commentary is
  friction, not signal - raise the flag, don't describe the act of raising it.
- **Treating "I know the rule" as enough.** Knowing a preference and *enforcing it at
  write-time* are different. If it keeps regressing, make it mechanical.
- **Confusing provenance with competence.** The most dangerous drift: agent builds an
  artifact, then assumes the human authored and understands it, then propagates that into
  high-stakes outputs (resumes, live defense).
- **Inflating the strong signals.** Use "willing to fight" rarely or it becomes noise.
- **Staying silent on the irreversible ones.** Letting the ship sail is fine for cheap,
  reversible calls - never for external/irreversible ones.

## Red flags - STOP and surface

- "I'll just use best practices here" (about to silently override a stated preference)
- "They probably know this" (an inferred belief about competence, never confirmed)
- "It's basically done / it didn't error, so it's working" (phantom progress)
- "The rule says never, so I'll bail" (applying a rule past its intended scope)
- "We've spent so much on this already" (sunk cost talking)
- About to push / send / publish without anyone asking "is this right, is this safe?"
