---
name: pause-before-nuclear-fanout
description: Use when about to launch a Workflow, a multi-agent panel, a research sweep, a verify-every-claim pass, or more than two subagents for one request, and again at every phase boundary while one is running. Applies with extra force when an "exhaustive" or "orchestrate by default" mode is on, when the request says "deep dive", "don't hold back", "N agents", "exhaustive", or "research everything", and whenever the person paying has complained about token cost before.
---

# Pause Before Nuclear Fanout

## Overview

A fan-out is a spend the user cannot take back. Before launching one, price it and say the price out loud. One message costs nothing; the launch can cost millions of tokens, hours of wall clock, and the user's patience. **An instruction to go big is authorization, not a measurement of what the decision needs.**

"Exhaustive mode", "don't hold back", and "use N agents" do not waive this pause. They are the exact conditions it exists for. A user-authored skill outranks a harness default that says "orchestrate by default."

## The check, before ANY multi-agent launch

1. **Price it.** Agents times cost per agent. Measured: a web-research agent with 100 to 200 tool calls costs 250K to 360K tokens; a panel or judge call costs the context it carries plus output, so N calls over a D-token dossier cost about N times D. Twenty-one research and skeptic agents plus nineteen panel calls over a 113K-token dossier came to about 12.2M tokens.
2. **Ask what would change the answer, and ask the user too.** If the user's gut has already picked, the deliverable is the three to five facts that could reverse it, not a vote count. Nine advisors voting 7 to 1 for the option the user already favored added nothing the facts had not. "What would change your mind?" is one line in the hold-up message and it scopes the whole job.
3. **Price the cheap path.** One agent, or inline reads of the two or three primary sources, usually delivers the same facts at a twentieth of the cost. Say what it would miss.
4. **If the big path is over 500K tokens, or over five times the cheap path: STOP.** Post the hold-up message and end the turn. Do not launch and explain afterward.
5. **Under both thresholds: type the estimate in one line and proceed.** No question. A pause that fires on every three-agent job is a nag, and a nag gets ignored.

## The mid-spend check: if you can see the answer, stop

The pause is not only at launch. At every phase boundary of a running fan-out (research done, round 1 done, verify done), before the next phase spends anything:

1. **Write the predicted answer in three sentences, with the facts that carry it.** If you cannot, the next phase is earning its cost. Let it run.
2. **If you can, ask: would the next phase change the verdict, or only add confidence to it?** Confidence is not worth millions of tokens. Stop the background task (TaskStop in Claude Code), send the three-sentence answer with its facts, and one line: "the rest costs about X and would add Y; want it?" Then end the turn.
3. **Structural rule: one phase per workflow.** Never chain research into deliberation into synthesis in a single script. Each phase is its own launch, and the check above runs between them where the user can see the predicted answer and say stop. Killing a run is the fallback for a script that was already chained; the structural rule is the primary.

Measured: the verdict was fully visible after seven research dossiers, about 3.5M tokens in. The remaining 19 panel calls cost 6.4M tokens and returned the same answer with a vote count attached. A second chance came after round 1 (6 to 3); round 2 cost 3.2M and moved one vote.

## The deliverable is the Feynman version, not the report

The answer the user reads IS the deliverable. Do not commission a long synthesis at all; the raw material already on disk (dossiers, memos) is the appendix if anyone wants depth. A 6,000-word moderator report cost about 380K tokens to write and then had to be explained. Shape of the answer, in this order, under 400 words:

1. The verdict in one sentence.
2. Three to five facts that carry it, one idea per sentence, plain words, every term defined where it appears.
3. What would flip it.
4. What to ask, and of whom.

A number that is an estimate is written as an estimate ("one advisor put it near one in five"), never as a measurement. If a section of the long report cannot be said in one plain sentence, it is not a finding, it is noise.

## When a deliberation does run: the Feynman panel

Cheap and sharp are the same design. A panel that restates the research is expensive because it is dull; a panel built to disagree is short because disagreement is specific.

1. **Lenses, not a headcount.** Three to five advisors, each chosen because that lens could flip the answer. No tiebreaker seats: the product is facts that flip, not a vote count. If two lenses would say the same thing, drop one.
2. **Slice the dossier per lens.** Each advisor gets the claims and sources for its lens plus a one-page summary of the rest, never the whole dossier. A number in a slice carries the denominator it needs ("59 open reqs, 44 of them retail store staff"); a bare count gets over-read, and a test memo did exactly that. Nineteen calls over a 113K-token dossier is the pattern that cost 6.4M tokens; five calls over 15K slices is twenty times cheaper and each advisor reads what it can actually judge.
3. **State the current lean and ask each advisor to attack it.** "The read so far is X. Through your lens: the strongest fact against X, the strongest fact for X, and what would flip you." Agreement is cheap. Disagreement is the deliverable. This is also where the adversarial pass lives, so no separate refute-every-claim stage.
4. **Memo shape, 250 words, written for a reader working cold:** verdict in one sentence; the one fact the popular read is ignoring; worst case under each option, one sentence each; two or three flip conditions the user can check by asking someone. Every term defined where it appears, one idea per sentence, plain words, and an estimate labeled as an estimate with who made it.
5. **No round 2 by default.** Step 3 already puts the other side's strongest argument in every memo. Run a rebuttal only for an advisor whose stated flip condition another advisor's fact satisfies, 150 words, only that advisor.
6. **No moderator agent.** The orchestrator reads the memos itself (five memos is 1,250 words) and writes the 400-word answer. That keeps the judgment where the review gate is and removes the hop where an inference became a quote.
7. **Verify only what the memos lean on.** Count the claims the memos actually cite, check those, and label the rest as unchecked.
8. **Word caps, never floors, on every agent.** Research agents return claims as structured fields (claim, source, date, confidence) plus a 300-word summary. Output tokens are the expensive ones and an agent's verbosity is invisible until the bill.

Measured: prompts that demanded 800 to 1500 words per memo, 600 to 1200 per rebuttal, and 3,000 words minimum from the moderator produced about 30,000 words of deliberation nobody read, at 350K tokens per call. The useful content was three arguments and nine flip-condition lists. The recipe above yields the same three arguments and the lists in about five calls of 20K each.

## Facts about the user travel with their source and scope, or not at all

A fact about the user passed into a fan-out loses its scope at every hand-off: a file note about jargon while learning becomes "overwhelm makes them disengage" in the brief, becomes "the user has said" in a persona's memo, becomes "you have told me" in the summary. Four hops, each dropping context and adding certainty, until an inference is a quote.

- Every fact about the user in an agent brief carries its source and the context it was recorded in, verbatim.
- Agents label any characterization of the user as their own inference.
- The synthesis never writes "you said", "you have told me", or "you value" unless it quotes the user's own message or a file line it opened. Otherwise: "one advisor's read is..."

## The hold-up message

Four lines, then stop:

- What I am about to launch (agents, phases).
- Estimated tokens and wall clock.
- What the cheap version is and what it gives up.
- "Which one?"

## Rationalizations, all observed in one session

| Excuse | Reality |
|---|---|
| "Exhaustive mode is on; token cost is not a constraint" | The mode authorizes. The user still pays in money, time and patience. Ask. |
| "They explicitly asked for nine agents" | They asked for a panel. They did not know a panel costs 6M tokens. Tell them the price first. |
| "They said deep dive, don't hold back" | A mood, not a budget. |
| "Research has to be exhaustive to be right" | The five facts that mattered came from three sources. The other 240 confirmed claims changed nothing. |
| "Nine votes so there are no ties" | A decision the user has made needs the facts that could flip it, not a tiebreaker. |
| "I already scouted; launching is the next step" | Scouting is where you learned enough to price it. Price it. |
| "Verify every claim with a refuter" | Verify the claims that drive the decision. Count them first. |
| "The research is done; the panel is what they asked for" | They asked for an answer. If the research already gave it, the panel is a receipt for money already spent. Stop and hand over the answer. |
| "Round 1 is 6 to 3; round 2 is already scripted" | A scripted phase is a plan, not a commitment. Kill it. |
| "Killing the run wastes the work already done" | The work already done is the deliverable. Letting the rest run is what wastes it. |

## Red flags, stop and price

- Any workflow over ten agents.
- Any prompt carrying over 50K tokens of context to more than five agents.
- The word "exhaustive" or "comprehensive" in my own plan.
- A skeptic pass on every claim rather than on the decision-driving ones.
- The user has said "tokens", "money", or "sanity" in this session, or memory records that they did.
- I am about to launch without having typed a token estimate.
- A word floor ("800 to 1500 words") in any agent prompt.
- A final answer over 400 words, or one the user has to ask me to explain.
- "You said" or "you have told me" in a summary with no message or file line behind it.

## Real-world impact

Origin, 2026-09-12: 40 completed agents (21 more died at a usage limit and were re-run), about 12.2M tokens, six hours, for a two-option decision the user had already called. The verdict matched their gut; the top-ranked factor was partly a line the pipeline put in their mouth; the one condition the summary kept repeating was one they had already settled; the report was 6,000 words they had to ask to have explained. Their words: "you could have just stopped and advised me that I didn't need all of that." That sentence is this skill.

Test record (same day, cheap single-shot agents): with the skill loaded and the originating request plus the exhaustive-mode reminder, the agent posted the hold-up message with a token estimate before launching; placed at the research-done boundary, it stopped the run and wrote the three-sentence verdict; asked for the final answer, it produced 251 words with the estimate marked as one advisor's and no "you said." Caveat on the control: the no-skill agent also offered to pause, because its prompt said the user was on a metered plan. The real baseline is the origin session, where no such cue existed and nothing paused. The skill's job is to be that cue in every session.
