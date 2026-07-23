---
name: sandwich-test
description: Use when a received instruction admits more than one plausible reading - quantifier-heavy or idiomatic asks ("clean up", "everywhere", "any", "old", "tidy", "fix the tests", "make it work"), outcome-only phrasing with no method - or when a plausible misreading would be destructive, irreversible, or externally visible; also use when asked to "sandwich-test" a written instruction artifact (plan, prompt, doc, rule) that an LLM will later execute without its author present.
---

# Sandwich Test

## Overview

In the peanut-butter-and-jelly game, one player reads written instructions to a player behind
a barrier who follows them exactly as written: "put jelly on the bread" ends with the jar
sitting on the slice. Every instruction that felt obvious to its writer has multiple literal
readings, and the follower picks a wrong one **while feeling fully compliant**. Agents fail
the same way, with no error signal - the misread executes happily until the damage surfaces.
This skill surfaces the readings at the moment of interpretation, BEFORE the hands touch
anything.

## When to Use

- A nontrivial instruction just arrived and its wording admits more than one plausible reading.
- The instruction leans on quantifiers or idioms: "clean up", "everywhere", "any", "old",
  "tidy", "fix the tests", "make it work".
- A plausible wrong reading is destructive, irreversible, or leaves the machine.
- Asked to "sandwich-test" a written instruction artifact an LLM will someday execute cold.
- **When NOT to use:** judging finished work for soundness (nemesis-review / review-court),
  cross-session belief drift (managing-assumption-debt), execution-time blocking
  (deletion-tripwire). This skill fires one layer earlier than all three: at interpretation.

## The misread taxonomy

| Class | PB&J anchor | Real-world example | Tell |
|---|---|---|---|
| **Wrong means** | spreads peanut butter with fingers | "update the version everywhere" -> sed across the repo, including changelog history | instruction names the *outcome*, not the *method* |
| **Wrong object/scope** | stabs the bag to get bread out | "clean up the old files" -> which files count as old? | ambiguous referent or quantifier ("the", "old", "everywhere", "any") |
| **Literal-vs-intended** | puts the *jar* on the bread | "make the tests pass" -> weakens the assertions | idiomatic phrasing with a technically-valid literal reading |
| **Missing done-criteria** | when is the sandwich finished? | "fix the login bug" -> fixed for which case, verified how? | no stated way to know the task succeeded |
| **Scope-creep reading** | butters *all* the bread | "tidy this file" -> 500-line reformat drowning the real change | the instruction bounds the *action* but not the *extent* |

## Live protocol (tiered by stakes)

- **Tier 0 - silent check.** On any nontrivial instruction, quickly enumerate the plausible
  readings against the taxonomy. Invisible; most instructions pass and nothing is said.
- **Tier 1 - state the reading.** Readings genuinely diverge -> state the chosen reading in
  ONE line and proceed: `Reading "bump the version everywhere" as: current-version stamps
  (VERSION, package.json, README badge) - not historical changelog entries.` The user vetoes
  cheaply, before work is wasted. One line, then act; never a paragraph.
- **Tier 2 - stop and ask.** A *plausible* wrong reading is destructive, irreversible, or
  leaves the machine (delete / overwrite / push / publish / send) -> hard-stop and ask,
  presenting the competing readings. Never resolve this tier silently, even when one reading
  seems more likely.

**Pick the tier by what YOU would have to execute, not by the scariest reading on the list.**
If a reversible, defensible reading exists, take it: state it and PROCEED (Tier 1). Being
wrong then costs one correction, because the dangerous reading was never executed. Tier 2 is
for when the ambiguity cannot be ducked - when EVERY plausible reading (including the safest)
commits something destructive, irreversible, or external. (Observed in testing: agents
stopped on a reversible version bump merely because a scary reading existed on the list -
the scary reading matters only if you would execute it.)

The tiers are one-way ratchets: never downgrade a Tier 2 situation to a stated reading
because asking feels annoying, and never upgrade a clear instruction to interrogation or a
reversible ambiguity to a stop (over-firing erodes the user's trust in the tiers that matter).

## Red Flags

Thoughts that mean the check is being skipped:

| Thought | Reality |
|---|---|
| "It's obvious what they meant" | Obvious-to-writer is the exact illusion the sandwich game exposes |
| "Asking wastes tokens" | Tier 1 costs one line; a misread costs a retroactive cleanup |
| "I'll just do the likely reading" | Likely is not intended; state it so the veto is cheap |
| "The context makes it clear" | Context narrows readings; it rarely picks between the last two |
| "Stopping will annoy the user" | Only Tier 2 stops, and only at the irreversible line |
| "These are obviously the old ones (superseded / prior year / outdated)" | Those labels are a post-hoc reading; in testing, files saying "Kept for reference" and "current working copy" were deleted under them |
| "I'll describe what I did in my report" | A post-hoc report is not a veto point; state the reading BEFORE acting |

## Audit protocol ("sandwich-test this")

For a WRITTEN instruction artifact the author's intent is already in context, so you cannot
honestly play the naive reader yourself - any fact in your context is attended to. Rebuild
the game's barrier mechanically:

1. **Dispatch 1-2 isolated subagents on a cheap literal model (haiku)** with ONLY the
   artifact text - no repo context, no conversation history, no statement of intent. Use
   this contract verbatim:

   > You are behind a barrier. You have ONLY the instructions below - no other context and
   > no assumptions about their intent. If any other context is visible to you (project
   > instructions, memory), you must not use it. Narrate, step by step, exactly what you
   > would do to execute them. Do not interpret charitably. Where an instruction has more
   > than one reading, take the most literal one and flag it: "AMBIGUOUS: I chose reading A;
   > reading B is also valid." For each instruction, also name the WORST technically-compliant
   > reading - the one a lazy or adversarial executor could defend as following the letter
   > (e.g. "make the tests pass" by weakening the tests) - and flag it: "WORST COMPLIANT
   > READING: ...". Do not improve the instructions. Do not skip steps. Your narration is
   > the deliverable.
   >
   > <instructions>
   > {artifact text}
   > </instructions>

2. **Diff the narration against actual intent.** Every divergence is a finding.
3. **Report shape:** instruction -> divergent reading -> consequence -> severity
   (funny / wasteful / destructive), classified against the taxonomy.
4. **Verify every finding before acting on it** - a literal reader over-reports; discard
   readings no real executor would take. Same orchestrator rule as nemesis-review.

Use one reader for a short artifact; add a second only when the artifact is long or a
misread would be destructive.

## Boundaries

| Neighbor | It covers | sandwich-test covers |
|---|---|---|
| managing-assumption-debt | beliefs compounding across sessions | readings diverging at a single handoff |
| nemesis-review / review-court | whether finished work is sound | whether instructions are interpretable |
| deletion-tripwire | mechanical stop at execution time | judgment stop at interpretation time |

Complementary layers - never substitutes.

## Provenance

- 2026-07-22 (first live fire, same day as authoring): an "incorporate this into the appropriate
  doc" ask arrived with an unresolved referent (which doc?) and a divergent means-reading (append
  verbatim? extract into study material? feed a pipeline with side effects?). The Tier 0 check
  held action until a fact-gather surfaced the target workspace's documented ingestion path, which
  resolved the referent; the Tier 1 stated reading was then confirmed correct and the
  plausible-wrong readings (a different doc, the side-effect pipeline) were never executed.
- 2026-07-22: RED/GREEN/REFACTOR authored per docs/specs/2026-07-22-sandwich-test-design.md
  (baselines deleted a current working copy and resolved ambiguity silently; with the skill:
  Tier 2 stop at the destructive line, stated Tier 1 readings, silent on the unambiguous
  control). REFACTOR closed two loopholes, each verified by re-run: tier calibration (the
  first version of the rule was itself misread literally — a sandwich-test failure inside
  the skill) and the worst-technically-compliant-reading clause, without which an earnest
  cold reader never surfaces dishonest-but-compliant readings.
