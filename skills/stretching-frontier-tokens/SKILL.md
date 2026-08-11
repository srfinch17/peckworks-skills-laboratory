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

## Testing note

Written from an observed baseline (one session where the frontier model did everything; numbers
above), not staged pressure scenarios - the maintainer has a standing instruction against
dispatch-heavy skill testing. Treat as unvalidated under pressure; tighten on first recurrence,
recording the rationalization used. First execution same day: a 3-model review fan-out + a
3-agent build fan-out moved ~615k tokens of work off the frontier quota with zero collisions;
the contract rules above were added from what that run showed.
