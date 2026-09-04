---
name: stretching-frontier-tokens
description: Use when the strongest available model is usage-capped or rate-limited and its quota is the bottleneck on real work - "I only get a day or two before my limit resets", burning frontier tokens on mechanical work, transcripts dominated by screenshots or tool round-trips, or planning how to split a working loop across model tiers. Also use before spawning subagents to save quota, to decide what must NOT be delegated.
---

# Stretching Frontier Tokens

**When the frontier model is the scarce resource, spend it only where the frontier matters.**
The failure this prevents: the strongest model does 100% of a loop - including screenshot
choreography, boilerplate plumbing, and log formatting - and the human's quota dies in a day.

## Measure the transcript before theorizing

Session transcripts live on disk (`~/.claude/projects/<project>/*.jsonl`). Have the CHEAPEST
model aggregate them: bytes by message type, base64/image line counts, tool-call counts by name,
largest lines. Observed baseline that motivated this skill: images were **76.7% of session
bytes** (48 screenshots, all 10 largest lines), plus **425 interactive browser tool calls** and
an **18k-token instructions file injected into every session** - none of it frontier work. Your
sinks will differ; measure first, then cut the biggest.

## The ladder (climb down before spending up)

1. **Script it.** Fixed choreography (drive a browser, crop images, parse a log, run tests) is a
   CLI call returning a text manifest - not N tool round-trips each carrying payloads through the
   frontier context. Build the script once; it costs zero tokens forever after.
2. **Cheapest capable model, via subagent.** Mechanical transforms, formatting, forensics ->
   cheapest tier. Vision digests, blind-gate judging, delta comparison -> mid tier (naive eyes are
   often what a blind gate WANTS). Implementation from an explicit spec -> strong-but-cheaper tier.
3. **Frontier only for:** diagnosis of WHY (the documented rate limiter in judgment loops),
   design of the mechanism/law, and prose aimed at the human (questions, trade-offs, verdicts).
4. **Session-level:** routine pattern-following rounds can run as whole sessions on a cheaper
   model with the laws in project memory; book frontier sessions for representation changes,
   complaints that survived two fixes, and consolidation.

## Delegation guardrails (each from a real failure)

- **Delegate only terminal outputs** - a number, a file path, a passing suite, a commit. Never a
  judgment the frontier model would re-derive from the raw data: that pays twice.
- **No delegation under ~10k tokens of work** - re-priming costs more than it saves. Prime
  subagents with one frozen ~60-line round brief, never the full instructions file.
- **Raw human words pass through unsummarised.** A digest may add coordinates and adjacency;
  the human's verbatim sentence always reaches the frontier model.
- **Integrity checks live in scripts, not in cheap models** - a cheap runner will never notice a
  lying rig; a script can assert echoed tags and refuse mismatched output.
- **One agent owns the diff** when a one-change-per-round law is in force; check
  `git diff --stat` against the expected file list.

## Cut the fixed taxes

Everything injected into every request is a tax multiplied by every turn: instruction files that
accumulate history (split to an operational core + a history doc), index files bloated into
paragraphs, full-frame images left sitting in context (crop to the marked region, downscale, cap
per decision, and prefer a subagent reading the image and returning text).

## Do not economize on

The human's capture channel and any append-only judgment record. The human is still the scarcest
resource; a token saved by degrading their signal is the most expensive token in the system.

## Writing the delegation contract (from the first real tiered run)

Quality tracked contract precision, not model tier. Four rules, each observed:

- **Demand evidence, not code.** Contracts that required verbatim result lines and live
  verification got agents that verified BEYOND spec (one drove the real app to prove generated
  DOM matched deleted markup and cache keys were unchanged; another tested the failure path
  unasked). Contracts that only ask for code get code.
- **Mark your claims as beliefs.** A prompt asserted a dependency existed "from prior rounds" -
  false, and a good agent falsified it (package manager + lockfile + history) and routed around
  it. State repo-record claims as "verify before relying"; an agent contradicting your prompt is
  the system working.
- **The orchestrator owns the seams.** Strict per-agent file ownership prevents collisions but
  creates gaps exactly at the boundaries (an agent barred from the manifest installed a
  dependency unpinned). After a fan-out, review the seams - cross-file contracts, manifests,
  registration sites - not just each diff.
- **Stop background processes before dependency installs** - your own dev server holding a
  native module produced EBUSY mid-integration.
- **Keep the words that will be SPOKEN or SENT; delegate the words that will be READ.** On a run with the frontier quota nearly exhausted, the orchestrator hand-wrote only the five verbatim scripts the human would read aloud in a live meeting, marked them "insert exactly as written, do not reword", and delegated every other word: teaching prose, layout, diagrams, a companion card, and the verification passes. **The scarce model's output should be the artifact with the lowest tolerance for paraphrase, not the one with the largest word count.** A subagent asked to improve copy will improve it, which is correct behavior and the wrong outcome when the copy is a script someone rehearses.
- **A deliberately narrowed QA gate is a trade, not a shortcut, and it has to be logged as one.** Under a hard quota ceiling, a full multi-lens gate was replaced by one verifier armed with the four defect classes that actually mattered for that artifact; it returned nine real findings. Record the narrowing wherever the artifact's provenance lives, so a later reader knows which lenses never ran and can run them when the quota returns.

## Testing note

Written from an observed baseline (one session where the frontier model did everything; numbers
above), not staged pressure scenarios - the maintainer has a standing instruction against
dispatch-heavy skill testing. Treat as unvalidated under pressure; tighten on first recurrence,
recording the rationalization used. First execution same day: a 3-model review fan-out + a
3-agent build fan-out moved ~615k tokens of work off the frontier quota with zero collisions;
the contract rules above were added from what that run showed.

## Provenance

- 2026-09-02: a 21-file Feynman rewrite plus ten cold reads ran on ~30 Sonnet-class agents (reads 156k-208k each, pair rewrites 130k-310k, one 220k picture sweep that found what four full reads missed) while the frontier wrote only the charter, the analogy seeds, the catalog entries and the diagnoses and never read a walkthrough end to end. Two waves of 9-12 agents died on the human's five-hour limit; waves of 3-4 with write-the-file-first agents finished with zero kills. A 34 KB single Write hit the 64k output cap; assembly by script from small pieces did not.

## Field validation: the human named the split himself, and the frontier share turned out to be the review gate

Mid-session the user asked for a sanity check: was the only part of a resume-tailoring workflow that needed a
frontier model the customization step itself, with everything else being grunt work? Yes, with one addition that
the same week had demonstrated twice: two cheap-agent deliverables (a dashboard CSS feature, then a follow-up with
web-search logo hunting) each reported grep counts that were all correct while the rendered page was broken in a
way only a screenshot showed. The frontier model's irreducible share is the review gate on what cheap agents
return: read the diff, render the output, verify the report's claims. Grunt that moved off the frontier model:
link extraction, dedup, folder metadata, generate and audit runs, tracker and dashboard refreshes, per-company
logo lookups (about 300k Sonnet tokens for 40 web searches, acceptable where the frontier model would have spent
the same plus its own reasoning). The lever that makes the split pay is BATCHING: per-item inline work by the
frontier model costs about the same as briefing an agent per item, so the agent must take a day's worth of items
and return only the short list that needs frontier judgment.
