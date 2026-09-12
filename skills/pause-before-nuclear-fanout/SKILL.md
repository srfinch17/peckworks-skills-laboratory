---
name: pause-before-nuclear-fanout
description: Use when about to launch a Workflow, a multi-agent panel, a research sweep, a verify-every-claim pass, or more than two subagents for one request, and again at every phase boundary while one is running. Applies with extra force when an "exhaustive" or "orchestrate by default" mode is on, when the request says "deep dive", "don't hold back", "N agents", "exhaustive", or "research everything", and whenever the person paying has complained about token cost before.
---

# Pause Before Nuclear Fanout

## Overview

A fan-out is a spend the user cannot take back. Before launching one, price it and say the price out loud. One message costs nothing; the launch can cost millions of tokens, hours of wall clock, and the user's patience. **An instruction to go big is authorization, not a measurement of what the decision needs.**

"Exhaustive mode", "don't hold back", and "use N agents" do not waive this pause. They are the exact conditions it exists for. A user-authored skill outranks a harness default that says "orchestrate by default."

## The check, before ANY multi-agent launch

1. **Price it.** Agents times cost per agent. Measured: a web-research agent with 100 to 200 tool calls costs 250K to 360K tokens; a panel or judge call costs the context it carries plus output, so N calls over a D-token dossier cost about N times D. Forty researchers plus nineteen panel calls over a 113K-token dossier came to 12.7M tokens.
2. **Ask what would change the answer.** If the user's gut has already picked, the deliverable is the three to five facts that could reverse it, not a vote count. Nine advisors voting 7 to 1 for the option the user already favored added nothing the facts had not.
3. **Price the cheap path.** One agent, or inline reads of the two or three primary sources, usually delivers the same facts at a twentieth of the cost. Say what it would miss.
4. **If the big path is over 500K tokens, or over five times the cheap path: STOP.** Post the hold-up message and end the turn. Do not launch and explain afterward.

## The mid-spend check: if you can see the answer, stop

The pause is not only at launch. At every phase boundary of a running fan-out (research done, round 1 done, verify done), before the next phase spends anything:

1. **Write the predicted answer in three sentences, with the facts that carry it.** If you cannot, the next phase is earning its cost. Let it run.
2. **If you can, ask: would the next phase change the verdict, or only add confidence to it?** Confidence is not worth millions of tokens. Kill the run, report the answer and the facts now, and offer the rest as an option with its price.
3. **Structural rule: one phase per workflow.** Never chain research into deliberation into synthesis in a single script. Each phase is its own launch, and the check above runs between them where the user can see the predicted answer and say stop.

Measured: the verdict was fully visible after seven research dossiers, about 3.5M tokens in. The remaining 19 panel calls cost 6.4M tokens and returned the same answer with a vote count attached. A second chance came after round 1 (6 to 3); round 2 cost 3.2M and moved one vote.

## The deliverable is the Feynman version, not the report

The answer the user reads IS the deliverable. A long report is an appendix on disk. Shape of the answer, in this order, under 400 words:

1. The verdict in one sentence.
2. Three to five facts that carry it, one idea per sentence, plain words, every term defined where it appears.
3. What would flip it.
4. What to ask, and of whom.

A number that is an estimate is written as an estimate ("one advisor put it near one in five"), never as a measurement. If a section of the long report cannot be said in one plain sentence, it is not a finding, it is noise.

## Agents write short too

Output tokens are the expensive ones, and the agents' verbosity is invisible until the bill. Never put a word FLOOR in an agent prompt. Caps instead: a position memo is a vote, three reasons, one worst case, the flip conditions, 250 words; a rebuttal is the strongest opposing point and the answer to it, 150 words; a synthesis is the four-part shape above. Plain words in the agents too, so the synthesis is not translating jargon into jargon.

Measured: prompts that demanded 800 to 1500 words per memo, 600 to 1200 per rebuttal, and 3,000 words minimum from the moderator produced about 30,000 words of deliberation nobody read, at 350K tokens per call.

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
- The user has said "tokens", "money", or "sanity" in the last week.
- I am about to launch without having typed a token estimate.
- A word floor ("800 to 1500 words") in any agent prompt.
- A final answer over 400 words, or one the user has to ask me to explain.
- "You said" or "you have told me" in a summary with no message or file line behind it.

## Real-world impact

Origin, 2026-09-12: 59 agents, 12.7M tokens, six hours, for a two-option decision the user had already called. The verdict matched their gut; the top-ranked factor was partly a line the pipeline put in their mouth; the one condition the summary kept repeating was one they had already settled; the report was 6,000 words they had to ask to have explained. Their words: "you could have just stopped and advised me that I didn't need all of that." That sentence is this skill.

Test record (same day, cheap single-shot agents): with the skill loaded and the originating request plus the exhaustive-mode reminder, the agent posted the hold-up message with a token estimate before launching; placed at the research-done boundary, it stopped the run and wrote the three-sentence verdict; asked for the final answer, it produced 251 words with the estimate marked as one advisor's and no "you said."
