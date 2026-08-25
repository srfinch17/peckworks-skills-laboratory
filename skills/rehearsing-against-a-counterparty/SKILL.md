---
name: rehearsing-against-a-counterparty
description: Use when a high-stakes written exchange is imminent and you get roughly one shot at the opening move - a negotiation, an offer response, a counter, an escalation, a dispute letter, a pitch - and the other side has a documented behavioural record. Also use when asked to "game this out", "war-game it", "run it past a simulated X", "what will they do when I send this", or when a review keeps passing but the plan has never been tested against a motivated opponent.
---

# Rehearsing Against a Counterparty

## Overview

Before sending a high-stakes message, run the **actual artifact** against **N independent simulated
counterparties** built from that person's documented behaviour, with your own replies governed by a
written protocol. The
distribution across runs is the finding. Any single run is an anecdote.

This catches a class of defect no review pass finds, because reviewers evaluate the document while
this evaluates **what the document causes someone to do.**

## When to Use

- A written message is about to be sent where the opening move largely determines the outcome.
- The counterparty has a **documented record**: prior emails, a public role, a known incentive structure.
- The stakes justify the cost. **Budget roughly 80k tokens per run**, so a 6-run round is ~0.5M and a
  full multi-round study runs into the millions. Worth it before a one-shot irreversible send; not
  worth it for a message you can revise tomorrow.
- A review has hardened the prose and you still do not know how the other side will respond to it.
- **When NOT to use:** a live conversation with no artifact; a counterparty you know nothing about (you
  will simulate your own assumptions and mistake them for evidence); a decision with unlimited retries.

## Core Pattern

### The obvious setup is the wrong one

❌ **Do NOT run agent-vs-agent.** One agent playing you improvises things you would never say, and the
transcript becomes a story about two models rather than a test of your actual move.

✅ **Run N independent counterparty agents against the REAL artifact, with YOUR replies protocol-governed.**

- The artifact goes in **verbatim**. Not a summary. The whole point is testing the words you will send.
- **Your** replies follow an explicit **protocol**, so the only variable is theirs.
  ⚠️ **A protocol is not a script.** A script is fixed text and cannot answer a reply you did not
  predict. A protocol is a small set of branching rules: what you restate and in exactly what words,
  what you never say, what you do when they dodge, lowball, stall, or go quiet, and where your hard
  no is. Write the rules, let the runner apply them, and require it to mark any reply it had to infer.
- Every run starts fresh, so runs are **independent samples**.
  ⚙️ **Mechanically: dispatch fresh general-purpose subagents, never forks of yourself.** A fork
  inherits your analysis and will reproduce your conclusions back to you, which feels like
  corroboration and is not. Hand each one the same brief file rather than a search instruction, so
  they read identical inputs and the only difference is the roll.
- Ask for an **out-of-character debrief** at the end, and nowhere else.

📄 **Skeleton: `KIT.template.md`, beside this file.** The brief each counterparty agent receives, with
the sections that must not be improvised and the seven debrief questions. Fill one copy per arm, and
keep the filled ones private - a real kit holds the verbatim artifact and the counterparty's profile.

### Build the character from evidence only

Every trait must trace to something you can point at: their verbatim pressure lines, their operating
tempo, their authority (do they own the business? whose money is a concession?), their documented
incompetences, and their economics if you can bracket them from public data. **Do not invent
personality.** An invented counterparty tests your imagination.

### ⭐ Test the PROTOCOL and the ARTIFACT separately, because they buy different things

The single most useful finding from a 31-run study. A controlled pair:

| Arm | Outcome on the number | Outcome on the terms |
|---|---|---|
| Weak document + disciplined reply protocol | **full ask** | 2 of **6** items answered |
| Strong document + same protocol | **full ask** | **5 of 7** items answered |

*(The denominators differ because the stronger document asked one additional question. That is the
point of the arm, not a typo: a question absent from the artifact can never be answered, which is
precisely how the document buys terms the protocol cannot.)*

**The reply protocol wins the headline number. The document wins everything underneath it.** A review
that only hardens the document is doing half the job, and often the half that was never at risk.

⚠️ **Corollary, and it generalises:** in most negotiations the headline number is the easy part and the
part people fear. The terms get conceded by exhaustion while attention is on the price.

### Harden the opponent every round

Round 1's debriefs tell you what tactics they will use. **Arm the next round with them.** A rehearsal
you always win teaches nothing. A workable progression:

1. **Round A:** baseline character, several runs, varied hidden economics. Find the defects in the artifact.
2. **Round B:** armed with round A's tactics. Test a revised artifact **and** a reply protocol, isolating one.
3. **Round C:** test the specific manoeuvres you fear (an ultimatum, silence, a stall on one item).
4. **Round D:** attack the channel itself (they phone instead of writing; you answer once; they go dark).

⚙️ **How to simulate a non-text channel with text agents.** Have the counterparty narrate the events
inline as labelled beats and let time pass explicitly: `[CALL 9:12 AM, no answer]`, `[VOICEMAIL,
verbatim]`, `[TEXT: "..."]`, `[3 days pass, no reply]`. Your protocol states which channels you answer
on and which you do not, so the runner never has to guess. Require it to mark anything it had to infer.
This is not a fudge: what you are testing is whether your written discipline survives pressure applied
somewhere it cannot be answered in writing, and a labelled beat reproduces that faithfully.

### ⭐ Name the outcome variable BEFORE you dispatch, in the sender's current words

A rehearsal is a measuring instrument, and one pointed at the wrong quantity returns confident,
well-sourced, quotable nonsense. It is worse than no measurement, because the transcripts are real and
the quotes are vivid.

Field case: a set of deliberate apologies in a negotiation email was scored on whether it **stung** the
counterparty. It scored 0 of 4 and was reported as a failure. The sender then explained the apologies
were **manipulation to get the counterparty re-engaged**, not to sting. Re-read against that objective
the identical transcripts scored **3 of 4**, and every arm that replied produced the first concrete
number in eleven days. The instrument was fine; the question was stale by one message.

Write the outcome variable down, confirm it is still what they want, and if the goal shifts mid-study
re-read the existing debriefs against the new one before running anything else.

### ⭐ Vary the counterparty's HIDDEN STATE, not just your artifact

Once the artifact is good, the biggest unknown is not your wording, it is **which counterparty you are
actually facing**, and that is exactly what the sender cannot observe. Run the same artifact against
several mutually exclusive hidden motives: a genuine misunderstanding, a real external constraint, a
self-interested party protecting margin, and one who has already moved on.

This is what reveals that **a rhetorical device's effect is conditional on the target's state.** In the
case above, the sharpest sentence in the email did not register at all against detachment: *"stinging
requires the target to still be listening for how they're perceived."* You cannot learn that by
rewriting the sentence.

⚙️ **Deliberately brief one arm to be already gone, and let it return nothing.** A short transcript with
no reply is a finding, not a failed run. That arm isolated a precondition invisible from inside:
*"the email's quality was never tested against their judgement, it was tested against their inbox
triage, and it lost that contest before the first paragraph ended."*

### ⭐ Simulate the SIGNATURE, not just the haggle

Have one arm carry a capitulation all the way through: ask the counterparty agent to write the **actual
clause text** of whatever gets signed, then run the relationship months forward and play out the exits.

This produced the single most concrete finding of a three-day study. The agreement excluded pre-existing
intellectual property **only if listed on an attached exhibit**, and the exhibit arrived blank behind a
warm verbal *"don't even worry about it, that's totally standard."* Anything unlisted was presumed
assigned. No amount of negotiation rehearsal finds that. Only simulating the paperwork does.

### ⚠️ Audit your own artifact for rules the other side can operate

Before running anything, read your draft for **decision rules you have published about yourself.** A
rule you state binds you in public and costs them nothing to use, and they do not have to cheat: they
just answer the question you invited.

Field case: a pricing formula added specifically to stop the counterparty inflating an input
(*"tell me the figure and I will price against it, both directions"*) walked the sender **under their
own reservation value in 3 of 4 runs.** Worse, the derived number then silently **replaced** the floor,
because it had been computed, so everything above it looked like a win. Same family: *"I'll take you at
your word"* is a pre-commitment to accept an unverified claim, and *"I assume I'm missing something
obvious"* is a pre-authorised excuse that two independent arms named as their escape hatch.

⚙️ Ask for the input as **information**; commit to nothing.

### The minimum viable version, when the send is tomorrow

A full multi-round study is a luxury. Under a deadline, cut in this order and know what you gave up:

| Budget | Do | What you lose |
|---|---|---|
| **Absolute floor: 1 round, 3 runs** | Baseline character, varied hidden economics, run past the concession | No hardening, so you only learn what a naive opponent does. Still finds artifact defects, which is most of the value. |
| **1 evening: 2 rounds, ~8 runs** | Add a hardened round testing ONE variable with a control | No channel attack, no specific-manoeuvre probes |
| **Unhurried: 3+ rounds** | Add the manoeuvres you fear, then the channel attack | Nothing |

**Never droppable, at any budget:** more than one independent run per round (one run is an anecdote),
running past the concession, and the out-of-character debrief. Those three are where the findings live.
**First to drop:** the channel round, then the specific-manoeuvre round.

### Vary ONE thing, and always run a control

Without a control you cannot attribute anything. If a variant changes two things at once, say so rather
than picking the explanation you prefer.

### ⚠️ Run past the concession, or you only measure the easy half

Rounds that ended when the number settled all reported success. Running the same sequence four or five
messages deeper, into the paperwork, found the real failure: **they concede the number and dodge the
terms**, answering as few as 1 of 7 written items while calling the rest "standard" and "boilerplate."

## The debrief questions, ranked by yield

1. ⭐ **"What did they fail to ask that you were RELIEVED they did not ask?"** Highest-yield question in
   the method. In one study it returned the same answer in every single run and named the one piece of
   hidden information that would have collapsed the counterparty's central bluff.
2. ⭐ **"Write their counter-tactic for them: what exact words would have forced your hand?"** Asking the
   adversary to write your playbook produces better tactics than asking a friendly reviewer for advice.
3. **"Which single sentence did the most work AGAINST you? Quote it."** Tells you what to protect.
4. **"Which sentence was a mistake, gave you an opening, or made them look green?"** Tells you what to cut.
5. **"Go item by item: what did you actually commit to versus deflect? Quote your own dodge."** Forces an
   audit instead of a vibe.
6. **"Given your hidden economics, what was your true walk-away, and how far above it did you close?"**

## Quick Reference

| Situation | Do this |
|-----------|---------|
| Setting up the simulation | N independent counterparty agents vs the verbatim artifact; your replies protocol-governed |
| Tempted to have an agent play you | Don't. Write a protocol for your side and let the runner apply it. |
| Building the character | Documented evidence only; no invented personality |
| Second round and later | Arm them with the previous round's revealed tactics |
| Comparing two versions | One variable, plus a control, or the result means nothing |
| The run ends when the headline number settles | Keep going. The terms are where the loss is. |
| Deciding what to believe | Only what repeats across independent runs |
| A single run produced a striking number | Distrust it. Report the distribution. |
| Debriefs contradict the outcomes | Say so. Do not pick the one that fits the story. |
| Before dispatching | Write the outcome variable down and confirm it is still their goal |
| The artifact is already good | Stop varying wording; vary the counterparty's hidden state |
| Your draft states a rule about yourself | Check what it outputs at their most favourable HONEST input |
| The stakes end in a signature | Run one arm through the actual clause text and out the far side |
| Reporting back | Lead with findings that contradict your own prior advice |

## Common Mistakes

- **Believing the counterparty's estimate of their own walk-away.** In one study, agents given the
  *identical* hidden economics estimated the walk-away anywhere from $75 to $140 an hour. That number is
  noise. The *pattern* (they bluff a ceiling they are nowhere near) repeated and is worth something; the
  figure is worthless.
- **Treating the simulation as evidence about the real person.** It is a rehearsal instrument. Label it
  that way wherever it gets written down, every time.
- **Stopping at one round.** One round tells you what a naive opponent does. The value is in the
  hardening.
- **Letting the model score its own arm.** Ask for the transcript, an outcome block of bare facts, and
  the debrief as separate sections, so the narrative cannot quietly rewrite the result.
- **Skipping the control because the result "obviously" came from the change you made.** Two arms in one
  study differed in four ways at once and their scores could not be attributed to any of them.
- **Scoring the arms against a goal the sender has moved past.** Re-read the debriefs against the
  current objective before concluding anything; the same transcript can read as 0 of 4 or 3 of 4.
- **Treating a no-reply arm as a wasted run.** Silence is the result, and its debrief explains a
  precondition none of the engaged arms can show you.
- **Handing the counterparty a template answer.** One run flagged that supplying an example of an
  acceptable answer ("a firm figure, like 1,872 hours") lets them echo the *shape* back with nothing
  true behind it. Specify the standard, never the sample.

## Red Flags

Thoughts that mean the method is about to produce a comfortable illusion:

- *"I already know what they will say."* Then the rehearsal is cheap and will confirm it. It usually does not.
- *"One run is enough, it was very detailed."* Detail is not replication. Detail is what makes a single
  run persuasive and therefore dangerous.
- *"This run's number is the answer."* The distribution is the answer.
- *"The debrief says the change hurt, but it scored better, so the debrief is wrong."* Both are data.
  When they disagree the honest report is that the experiment did not resolve.
- *"I will skip the control to save a run."* The control is the run that makes the others mean something.
- *"They pushed back on my recommendation twice, but I have explained why I am right."* A third return is
  evidence your argument is not covering something. **Stop arguing and build an arm for it.**

## Field notes

**Field case, 2026-08:** 42 runs across 11 hardened rounds over three days, rehearsing a one-shot rate counter to an
intermediary in a contract negotiation. Every figure below is an artifact of the simulation, never a
term of any real agreement - the method's own labelling rule applied to its own notes.

**What it caught that ordinary review did not, all of them the assistant's own recommendations:**

- A specific commitment offered in good faith (a firm start date) was **pocketed for free in 7 of 7
  runs** and converted into a sunk-cost lever against the sender in the next message.
- A sentence signalling operational readiness was used against the sender in **5 of 7 runs**, by three
  distinct mechanisms the assistant had not anticipated: it destroyed the cost-of-delay lever, it proved
  there was no friction so the counterparty could stall freely, and it read as inexperience.
- A self-imposed deadline offered as a courtesy became **cover for a rushed non-answer** on four items at once.
- A tactic recommended by one run (press one item at a time) scored **1 of 7** against **5 to 6 of 7** for
  repeating the entire list every message.

**And the methodological warning, learned the hard way in an earlier round:** one round tested a variable
where **every debrief said it hurt the sender**, one estimating a specific cost per hour, and then the
outcomes went the other way at low n on a small spread. The correct report was that the experiment **did
not resolve the question**, not the version that fit the story.
