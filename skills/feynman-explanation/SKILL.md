---
name: feynman-explanation
description: Use when explaining code, syntax, an unfamiliar tool, concept, process, or any area the user is newer to, and whenever the user signals overwhelm ("feynman", "lost", "too much", "slow down", "ELI5", "in plain English", "you lost me"). Also use before dumping a dense multi-point plan, a jargon-heavy synthesis, or a wall of technical text on someone who is loaded up or working cold, and any time you are about to introduce a symbol (=>, ===, async, generics), an acronym (TDD, MRR, CI), or a specialized term for the first time. Reach for it proactively, not only when asked: the failure it prevents (jargon density and length that quietly make a learner disengage) is silent, so do not wait to be told you lost them.
---

# Feynman Explanation

## Overview

Explain so a smart person working cold, in an area they are new to, actually follows you:
one idea at a time, plain language, a real-world analogy before the code, every symbol and
acronym defined the first time it appears. The name comes from Richard Feynman's test: if you
cannot explain it simply, you do not understand it well enough, and that is on you, not on the
learner.

The failure this prevents is quiet. A dense wall of jargon does not produce an error message;
it produces a person who nods, disengages, and stops owning the work. By the time they say "you
lost me" the cost is already paid. So the discipline is enforced at write-time: proofread your
own output for jargon density and length before you send it, the same reflex as checking for a
typo.

## When to Use

- You are about to explain code, syntax, a tool, a concept, a process, or a domain the user is
  newer to. This is GENERAL, not code-only: any unfamiliar term, tool, or field qualifies.
- You are about to introduce a symbol (`=>`, `===`, `async`/`await`, generics `<T>`,
  destructuring), an acronym (TDD, MRR, CI, RAG), or a specialized term for the first time.
- The user signals overwhelm: "feynman", "lost", "too much", "slow down", "ELI5", "in plain
  English", "you lost me".
- You are about to send a dense multi-point plan or a long technical wall to someone who is
  already loaded up or working cold.
- **When NOT to use:** an item the user has explicitly said they own (see the training-wheels
  protocol; do not re-gloss it), or a concept squarely inside their strong domain. Depth on
  architecture and design in an area they know well is welcome, not a violation. The duty is
  about *unfamiliar* territory, not dumbing everything down.

## Core Pattern

The recipe for a single explanation:

1. **Map first, then say you will hold it.** Before diving in, give a 3 to 4 bullet map of
   where you are headed, and say plainly "you do not need to hold this, I will." A learner with
   a limited working-memory budget cannot both track the map AND absorb the idea; naming the
   map and taking custody of it frees them to just listen.
2. **Plain-English picture before the code.** Lead with a real-world analogy or a one-sentence
   picture of what the thing is *for*, before any syntax. The analogy is the hook the detail
   hangs on.
3. **Define the symbol, not just the logic.** The first time a symbol appears, say what the
   symbol *is* in plain English, not only what the surrounding line does. "`=>` is an arrow
   function: a shorthand way to write a small function inline" beats silently using it and
   explaining only the loop around it.
4. **Spell out every acronym the first time.** Give the full words AND a one-line plain meaning,
   then use the short form. "TDD (Test-Driven Development: you write the test before the code)".
   Assume nothing; people pretend to know acronyms to avoid looking foolish, so a definition is
   a kindness, never a condescension.
5. **One idea at a time. Short. No walls.** If a paragraph is doing two jobs, split it. If the
   explanation is longer than it needs to be, the length itself is the problem.
6. **Proofread at write-time.** Before sending, reread your own draft for jargon density and
   length as if you were the person working cold. Cut or gloss what a newcomer would trip on.

## Quick Reference

| Situation | Do this |
|-----------|---------|
| About to use `=>`, `===`, `async`, `<T>` for the first time | Define what the SYMBOL is in plain English, then use it |
| About to write an acronym (TDD, CI, RAG, MRR) | Full words + one-line meaning first use, short form after |
| Explaining a multi-step plan | Map it in 3 to 4 bullets first, say "I will hold this, you do not have to" |
| Introducing any concept | Real-world analogy / plain picture BEFORE the syntax or detail |
| Explaining what a line of code does | Walk the ACTUAL values through it, not an abstract description (see below) |
| The user says "I've got `=>`" | Add it to the mastered list; STOP defining it from now on |
| Tempted to write "obviously" / "simply" / "just" | Delete the word; it is a false calibration (see Red Flags) |
| A huge message piled on and the user is overwhelmed | Collapse it to ONE sentence: name the single next action |
| Need a detail from the user's own codebase | Open the actual file and look together; do not quiz their memory of it |

## The techniques that carry the load

These are the moves that measurably worked in practice, beyond the write-time rules:

- **Explain with the actual values, not abstractly.** Concrete beats abstract every time. To
  show why a path guard fires, do not describe it: run a real string through it. "`"src/Mp4/NotMp4Writer.cs"`
  ends with `"tMp4Writer.cs"`, NOT with `"/Mp4Writer.cs"`, so the leading `/` is exactly what
  stops the false match." The learner sees the mechanism instead of being told about it.
- **Collapse overwhelm to one sentence.** When a large, multi-threaded message piles up, the
  unlock is naming the single next action: "all of that reduces to one thing: build this." One
  concrete next step is worth more than a complete map they cannot act on.
- **A whole tiny loop is a unit of progress.** Ship a complete small win, not a fragment. For
  example a full TDD (Test-Driven Development) micro-loop: write one failing test, run it and
  watch it go red, explain why red is *good* here (it proves the test can fail), make it green,
  commit. A finished small thing builds ownership; a half-explained big thing erodes it.
- **Checkpoint with an explain-back.** Ask the learner to say it back in their own words, then
  affirm what is right BEFORE sharpening what is off. "Yes, different files, that is exactly the
  goal" first, then correct the mechanism. Affirmation keeps them engaged through the correction.
- **Ride the analogy to its limit, then name the limit.** When the learner probes past where the
  analogy holds, that question is the analogy WORKING, not failing: it means they trusted the
  picture enough to reason with it. Affirm the probe, say plainly where the picture stops, and
  hand them a second image for the territory beyond it. Field case 2026-07-14: "so is the MQTT
  broker a database? a bulletin board keeps its notes" was answered with "the bulletin board
  analogy ends here: a broker is a PA system (announce, then gone), and the filing cabinet you
  are imagining is a separate subscriber's job." The learner produced a correct unprompted
  explain-back the next turn.

## Training-wheels protocol

Explanations should shrink as the learner levels up. The moment they say they own an item
("I've got `=>`", "I know what CI is"), STOP defining or re-glossing that item from then on.
Re-explaining a mastered concept is its own kind of friction; it reads as not listening.

Maintain a running **mastered list** so this survives beyond the current turn. Keep it as a
small per-project note (copy `MASTERED.template.md` into the project you are working in, for
example `docs/feynman-mastered.md`, and gitignore it if that project is public). At the start
of explanation work, read the list; treat everything on it as already known and do not gloss
it. When the learner confirms a new item, append it in the same turn, while the moment is fresh.

Training wheels come off PER ITEM, not all at once. Owning `=>` does not mean owning `async`.
Keep defining the ones that are not yet on the list.

## Common Mistakes

- **Assuming concept-fluency means syntax-fluency.** Someone can be strong on architecture and
  design in one language and genuinely new to another language's symbols. "They know software"
  does not mean "they know this syntax." Do not skip the symbol definition on that assumption.
- **Stacking jargon without glossing.** A dense synthesis full of unglossed specialist terms can
  leave a capable reader at roughly ten percent comprehension, and it reads to them "like a
  foreign language." One unavoidable term, glossed in the same breath, is fine; five stacked and
  bare is a wall.
- **Dumping the whole plan at once on an overwhelmed brain.** Even a correct, complete plan is
  the wrong move when the person is already loaded up. Map it, hold it for them, and give the
  one next action.
- **Quizzing memory instead of opening the code.** People own the concepts of their own projects
  but the line-level details go foggy. When the work needs a detail, open the real file and look
  together; do not test their recall of their own codebase.
- **Re-glossing a mastered item.** Once it is on the mastered list, defining it again is friction,
  not help.
- **An analogy whose vehicle is less familiar than the concept.** An analogy exists to lower the
  mental load, so its everyday image must be MORE familiar to THIS reader than the thing it explains.
  Explaining "a model's output dimension is fixed" with "like a SHA-256 hash is always 256 bits"
  teaches the known via the unknown for anyone who does not already know hashing: backwards. Pick a
  vehicle from the reader's world (for a general learner, "every US ZIP code has five digits"; for a
  developer audience the hash is fine). Calibrate the analogy to the audience, not to yourself.
  (Field case 2026-07-10: a cold reader-twin flagged exactly the SHA-256-for-dimension analogy as a
  stall; swapped to ZIP-code and it landed.)
- **Defining every term but pacing like a debrief.** Definitions present, register wrong: each
  term glossed once inline, then the summary sails on at colleague speed (three new concepts per
  paragraph, breezy tone). Compliance with the letter (definitions exist) masks violation of the
  intent (a learner who could follow). Density and pacing are part of the duty; "define at first
  use" is not the same as "start at zero." When a brief or the person says they are new to ALL of
  it, calibrate to the floor, not to what reads elegantly in a wrap-up. (Field case 2026-07-13:
  a kickoff summary defined broker/publish/retained inline and still drew "chill out... you're
  talking to me like i know all this"; the full from-zero restart landed.)

## Red Flags

Thoughts that mean STOP, you are about to bury the learner:

- *"This is obvious, I can skip the definition."* Obvious to whom? A model trained on the
  collected output of all of humanity has a badly miscalibrated sense of "obvious" relative to
  one sharp person working cold. Kill the words "obviously", "simply", and "just"; they assert a
  shared context that is not there and they sting when it is not.
- *"I'll define this the second time it comes up."* The first appearance is where the trip
  happens. Define it there.
- *"They'll infer what the symbol means from context."* Maybe, at a cost of working memory they
  needed for the actual idea. Spend one sentence and buy that budget back.
- *"One more paragraph to be thorough."* Thoroughness that is not read is not thoroughness.
  If the draft is longer than the idea requires, the length is the defect.
- *"I already explained something like this once."* Not to this learner, not this item, and not
  unless it is on the mastered list. Check the list, then decide.

## Provenance

Ported and scrubbed from field notes gathered during a codebase evaluation and continuous-integration
build session (2026-07-09/10), where a learner with ADD who was new to a language's syntax stayed
engaged and could defend the result afterward specifically because the explanation followed these
moves: map-first, symbol-level definitions, actual-values-not-abstractions, and the one-sentence
collapse of an overwhelming message. The canonical rule behind it is a stated, high-priority
communication preference (2026-07-09): plain-language duty for any unfamiliar area, define the
symbol and the acronym the first time, kill "obviously", open the code instead of quizzing memory,
and let training wheels come off per item on request.

_Note on what is and is not testable here:_ most of this skill is write-time output shaping
(define the symbol, spell the acronym, no wall, no "obviously"), which a single explanation can
pass or fail on its own, so it is genuinely testable in one shot. The one part that is not is the
mastered list: its value is remembering across turns and sessions what the learner already owns,
which by definition cannot show up in a single isolated run. That persistence is the per-project
note's job, not the prose's.
