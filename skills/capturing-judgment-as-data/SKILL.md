---
name: capturing-judgment-as-data
description: Use when correctness is a human's opinion rather than something a test can decide - visual or generative output, tone, taste, UX feel, "does this read as natural" - and their verdicts should survive the session. Also use when feedback keeps arriving as comments that cannot be reproduced, when a fix was declared verified against an instrument the human cannot see, when planning to carry learnings into a successor project, or when asked to build an agent that judges or screens output.
---

# Capturing Judgment as Data

**The human is the scarce resource. Everything else is cheap.** Compute is cheap, storage is cheap,
your time is cheap. Their attention is the one input that cannot be scaled, and it is normally spent
once and thrown away: "that looks wrong", acted on, evaporated.

**The goal is an asymptote: drive the number of future human judgments toward zero.** Not by guessing
what they would say, but by extracting so much durable, replayable signal from each interaction that
the same question never has to be asked twice - not in this project, and not in the next one.

Two operations follow from that:

- **Maximize yield per interaction.** Every time they look at something, harvest every atom
  available: their words, the exact state, the vantage, the artifact, the instrument settings, the
  code version. They supply one sentence; the machine supplies everything needed to make that
  sentence permanently useful.
- **Never spend a judgment you could have screened.** Anything with a right answer is yours to check.
  Their attention is reserved for what only a human can settle.

**Core principle: a judgment is only worth what you can reproduce.** An opinion welded to the exact
state that produced it is an asset that compounds. The same opinion floating free is a rumour.

Loop mechanics - cheap render, isolation controls, how often to interrupt them - belong to
**look-driven-iteration**. Use that for the loop. Use this for the record and what you do with it.

## When to use

- Starting anything where a human is the acceptance test (generative art, geometry, layout, motion,
  copy tone, audio, "feel")
- Their feedback keeps being unreproducible ("the middle one was wrong" - which one?)
- You are about to run a review round and have no plan for where the answers go
- A successor project will need what this one learned
- Someone asks for an evaluator, judge, screener, or "an agent with our taste"

**Not for:** work with a real oracle. If a test can decide it, write the test.

## The four laws

Each one is a failure that actually happened, not a preference.

### 1. Give the AI the same sensor the human has

If they judge by looking, you must look. Measuring what is convenient to compute instead of what
they can perceive produces confident, wrong conclusions.

A generator's owner reported bark "breaking into pixelated garbage". The agent measured the
*mathematical field* and found it smooth, twice declared the bug fixed, and was twice told it wasn't.
The defect was in the *rendered triangles*, then in a *shading flag* - neither visible to the
instrument it had chosen. Nothing was learned until the agent drove the real app to the owner's exact
camera and looked at the same pixels.

**Practice:** before trusting any metric, confirm it can see the reported symptom. If they say
"jagged", measure jaggedness, not amplitude. If you cannot perceive the artifact at all, get that
capability before diagnosing.

### 2. Make a data point nearly free to produce

Cost per judgment sets sample size, and sample size decides whether you get signal or anecdote. One
button plus speech-to-text turned a reviewer from three grudging comments into thirty rich ones in
the same sitting.

**Practice:** the human should produce a complete record with one click and one utterance. No
copy-paste, no filling in fields, no switching windows, no describing where they were looking. Every
step you leave in the way is a record you will not get.

### 3. Log the question next to the answer

An unprompted "this looks bad" is nearly worthless later. "Does the grain break at the branch? -
yes, still" is a labelled example: it has a claim, a verdict, and a subject.

**Practice:** drive review rounds from named trials. Each preset loads a full configuration AND
pre-fills the comment box with its id and the specific question. The human types under it. Both
halves land in the record together.

This is also what makes the log trainable later. Question + verdict is a label. Free-floating
complaint is not.

### 4. One change at a time

Two changes shipped together make the result unattributable for BOTH of you, and the human cannot
tell you which one to keep.

A round shipped a new generation model and a rendering fix together. The output changed a lot, the
owner said "you've gone backwards", and neither party could say which change was responsible. It
cost a full round to isolate by reverting one and re-rendering.

**Practice:** one variable per round. If you must ship two, say so explicitly and keep a way to
toggle each. When a result is confusing, revert one thing and re-render before theorising.

## The record

Every entry, written atomically, one click:

| Field | Why it earns its place |
|---|---|
| **The question asked** | Turns a complaint into a labelled example (law 3) |
| **The human's verdict, free text** | Their words are the best signal you will get. Do not force a form |
| **Full state, verbatim as consumed** | Must replay EXACTLY. Serialize what the generator eats, not a summary |
| **Vantage point** | Camera / scroll / zoom / which screen. "It's wrong on the left" is meaningless without it |
| **The artifact itself** | A screenshot or capture. The one field people skip and regret |
| **Instrument state** | Quality, resolution, sample rate, WHICH RENDERING MODE. See below |
| **Code version** | Commit hash. Params alone do not reproduce anything a year later |

### The instrument-state field is the one you will forget

A project lost an entire round because the record did not say whether the preview was flat-shaded or
smooth-shaded. The human was describing a *shading artifact*; the agent read it as a *geometry
defect* and rebuilt geometry twice. One boolean in the record would have ended it immediately.

The general form: **record the settings of the thing doing the showing, not just the thing being
shown.** Whatever could make the same output look different is part of the record.

### Code version is what makes it survive

Parameters replay against *today's* code. To rebuild an artifact a year later, or to compare this
project's verdicts against a successor's, the record needs the commit. Without it the archive
degrades into "someone once disliked something roughly like this".

## Yield: how many atoms per interaction

An "atom" is one durable, independently useful fact extracted from a human touch. A comment logged
as prose is one atom. The same comment logged with question, state, vantage, artifact, instrument
and version is seven, and only the first one cost them anything.

**Capture everything the machine can see, not just what they said.** They should never be asked to
supply a fact a program could have recorded - what the settings were, where they were looking, what
build it was. Asking them to describe those things burns the scarce resource on clerical work and
gets a worse answer than the machine would have given.

**Enrich rather than interrogate.** The instinct when you want more data is to ask more questions.
Wrong direction: add more automatic capture instead. One utterance against a rich record beats three
utterances against a thin one, and costs a third as much of them.

**Track the trend, not the total.** The metric that matters is human touches per resolved defect, and
it should fall over the life of a project. If round five needs as much of them as round one, the
capture is not compounding - the records are not being harvested, or you are asking them things you
could have screened. Most projects will not reach zero. Every project should be heading there.

## The harvest

A log becomes a dataset in three steps. Do them while the project is warm; nobody reconstructs
context later.

1. **Extract a defect vocabulary.** Read the log and name the recurring complaints in *the human's
   own words*, each with the axis it varies on (too much / too little / wrong place / wrong shape).
   Twenty entries usually collapse into a dozen named defects.

2. **Convert judging into screening.** Agents are unreliable at open "what is wrong with this?" and
   good at closed "is defect R3 present here, yes or no?". The vocabulary is what makes that switch
   possible. Never ask an agent for taste when you can ask it for a checklist.

3. **Keep the negatives.** A log of only complaints trains a screener that condemns everything.
   Deliberately capture "this one is right" entries; they are as valuable as the failures and people
   never volunteer them.

4. **Retire questions.** Each harvested defect should become an automatic check, a guardrail on the
   input range, or a screening item an agent runs unattended - and then never be asked of the human
   again. A vocabulary entry that still requires a human every round has not been harvested, only
   written down. This step is the asymptote; without it the log is an archive, not an engine.

**Porting:** the vocabulary is domain-specific and does not transfer. The *record schema*, the
question/verdict shape, and the harvested checks' STRUCTURE do. Set the capture up on day one of the
successor project, not on day forty - and seed its screening pass from the predecessor's vocabulary,
so the new project starts where the old one finished rather than at zero.

## What agents can and cannot judge

Objective and checkable is yours: is there a repeating lattice, did geometry break, is the value out
of range, did it regress against the last capture. Run those solo and stop spending human attention
on them.

Taste is theirs, and so is noticing what nobody was looking for. Bring them few, high-leverage
choices rather than a long queue of things you could have screened yourself. See
**look-driven-iteration** for how that division plays out during a round.

## Common mistakes

| Mistake | Fix |
|---|---|
| Capturing state but not a picture | Add the screenshot. It is the field that resolves arguments |
| Recording parameters, not the version | Add the commit hash |
| Asking "what do you think?" | Ask a specific question and log it with the answer |
| Building a form for them to fill in | Free text plus automatic capture. Forms suppress the best signal |
| Only logging failures | Solicit positives explicitly |
| Trusting your metric over their eye | Confirm the metric can see the reported symptom (law 1) |
| Harvesting "later" | Extract the vocabulary while the project is warm |
| Asking them to type what a program could record | Automatic capture. Their words are for judgment only |
| Asking more questions to get more data | Add more automatic capture instead - richer records, fewer asks |
| Same defect asked about every round | It was never harvested. Turn it into a check or a guardrail |

## Red flags

- "I verified it with a measurement" - can that measurement perceive what they described?
- "I'll capture the state, the screenshot is overkill" - it is the field you will want most
- "Let me ship both fixes and see" - unattributable for both of you
- "They said it looks bad" recorded with no question attached - unlabelled, nearly worthless
- Reproducing a logged verdict requires guessing anything - the record is incomplete; fix the capture
- About to ask them something with a right answer - screen it yourself; their attention is the budget
- Round five costs them as much as round one - nothing is being harvested; the log is not compounding

## Testing note

This skill was written from an observed baseline rather than staged pressure scenarios: the failures
in laws 1, 3 and 4 are verbatim from a session where an agent without this guidance committed all
three. Subagent pressure-testing was not run because the maintainer has a standing instruction
against dispatching agents. Treat the rationalization coverage as unvalidated and tighten it the next
time one of these failures recurs.
