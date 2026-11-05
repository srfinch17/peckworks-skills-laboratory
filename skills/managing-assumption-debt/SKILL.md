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

## The seven classes (with their tells)

These replaced the original four on 2026-11-05, after a data audit of 178 logged episodes found that
only a third fit the original names and that one class the original list did not have held 46 percent
of them. Every episode is filed under exactly ONE class, by its root, not its symptom. Where two fit,
take the earlier one in this table.

| Class | What happens | The tell to watch for |
|---|---|---|
| **external-boundary** | Something is pushed, published, sent, deleted or exposed without the check that line requires | About to cross the line with nobody having asked "is this right, is this safe?" |
| **provenance-drift** | What the agent built is treated as what the human knows or can defend, or an invented fact about their skills, history or domain is handed to them as real | A fact about the collaborator you *inferred* but they never *stated*; "we built it" read as "they know it" |
| **commission-misread** | The human's words are read as a pointer into your own model, so the wrong feature, object, scope or deliverable gets built or fixed | A request that survives one round in the same words; a question answered with a build |
| **shared-state** | An ownership or order assumption about a shared thing: two machines or copies, a default sized for another caller, a file two parties write, a mask built before the thing it must hold | "It's there / it's in sync / that's mine" said without a glance |
| **silent-override** | You do the opposite of a stated preference, rule or protocol and justify it to yourself | Thinking "best practices / convention" instead of asking; a rule in context not followed |
| **scope-creep** | A rule stated broadly is applied outside the scope it was written for | Absolute words: *never, always, all, every, no* with no stated boundary; a rule's number carried to a new context |
| **artifact-trust** | A count, probe, metric, memory note, summary, code read or green result is trusted instead of the ground truth it describes | The feeling of already knowing; "no error" read as "working"; a fix declared on a number that could not see the bug |

**artifact-trust is the dominant class by a wide margin** (82 of 178 at the audit). It is never a knowledge
gap: the check is always cheap (one grep, one diff, one render, one `git log`) and is skipped because the
invented version feels like knowing. Open the thing before asserting about it.

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

## The escalation vocabulary (unproven; kept to three lines)

A light flag is one line that names the assumption and keeps moving. *"I'm willing to fight about
this"* is the scarce token for a load-bearing, hard-to-reverse call. *"I think we're protecting an
investment, not making the right call"* names sunk cost out loud. Default is deference. **Audit note
2026-11-05:** across 108 sessions these phrases were never used outside the skill text itself; the
section is kept short rather than cut so either party can still invoke it, and it is not load-bearing.

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
Each episode records, in about 150 words:

> date - **class** (one of the seven) - **recurs** (the earlier episodes of the same root, or none) -
> the assumption - **the tell** (the early signal that would have caught it) - the cost -
> the durable fix (a guard, a gate, a test; a reminder only when nothing mechanical exists)

The `Class` and `Recurs` fields are what make the log calibrate instead of merely grow. The
SessionStart hook counts them over the newest 30 episodes and injects the top three recurring classes,
each with its repeat count and latest episode id, into every session. **Before acting in one of those
classes, open the latest episode named.** A data audit on 2026-11-05 found 29 percent of 178 episodes
were admitted repeats, several within hours of the rule being written, while the injected layer had
absorbed no new weight in 36 episodes: the repeat classes were in the log and never in front of a
session. Counting them is the mechanical form of distillation.

**Every ten episodes, one standing weight is added or retired.** The hook tracks episodes since the
standing layer last changed and nudges when ten have landed. An episode that changes no weight is a diary
entry, not calibration. The 150-word cap is enforced the same way: the hook names the newest episodes
over it (env `ASSUMPTION_DEBT_EPISODE_WORDS`). Detail belongs in the project diary the episode points to;
the audit found episode length had tripled since June and the log was eating its own loop (EP-161's
lesson, applied to this log).

Over time this becomes a personalized profile of *this* collaborator's recurring blind
spots - earned the way real familiarity is earned, through a history of surprises, not a
declared list of traits. **If a personal logbook exists for this collaborator, consult it at
the trigger moments above** and record a new episode whenever a fresh debt comes due. See
`LOGBOOK.template.md` for the schema.

**Write new episodes at the TOP of the Episodes section, and take the id from the SessionStart
hook's status line rather than reading either end of the file.** "Append" is the wrong verb for
a newest-first log and caused a real failure: one logbook drifted into two independently
numbered regions, the tail one silently grew past the top one in date, and ten ids collided
while the newest episode sat last, so every session-start read of the top missed three weeks.
The `inject_standing_layer.py` hook now publishes the next free id and warns on duplicates or
broken ordering, because the collisions happened for want of a knowable next number.

**The Date line is what the ordering check reads.** It takes the first date on the `- **Date:**`
line; a range (`2026-08-05/06`, `2026-08-03 to 08-06`, `2026-10-01 to 2026-10-02`) sorts by its
END date. Dates in the prose around it are ignored. Field case 2026-10-05: the full-date range
form was not recognised, so an episode spanning two days sorted by its start and the hook raised
a false "not newest-first" warning on a correctly ordered log. Fixed in the hook with a test; if
the warning names an episode whose Date line starts with a range, suspect the parser before
reordering anything.

**When the logbook outgrows about 200 lines, split it; never truncate it.** Keep the standing layer and the newest episodes in the main file; move older episodes verbatim to sibling files named `<logbook stem>_archive_<YYYY-MM>.md` (newest first), and long reference sections (such as the working countermeasures) to their own sibling file with a pointer. The SessionStart hook reads every `<stem>_archive*.md` for the next free id and the duplicate check, so an archived id is never reused; verify after a split that the published episode count and next id are unchanged. The hook also warns at session start when the main file passes its line cap (default 200, env `ASSUMPTION_DEBT_MAIN_CAP`).

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
- "It's basically done / it didn't error, so it's working" (artifact-trust)
- "I already know what that file / count / note says" (artifact-trust; open it)
- "The rule says never, so I'll bail" (applying a rule past its intended scope)
- "We've spent so much on this already" (sunk cost talking)
- About to push / send / publish without anyone asking "is this right, is this safe?"
