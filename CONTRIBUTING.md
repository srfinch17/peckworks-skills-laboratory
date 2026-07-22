# Contributing skills

This lab develops skills the same way good code gets written: **test-first**. A skill is
process documentation, so "testing" means watching an agent behave *without* the skill,
then verifying the skill changes that behavior.

## The iron law

> No skill without a failing test first.

If you write the skill before observing baseline behavior, you don't know whether it
teaches the right thing. This applies to edits too, not just new skills.

## RED → GREEN → REFACTOR

| Phase | Code TDD | Skill TDD |
|-------|----------|-----------|
| RED | Write a failing test | Run a scenario *without* the skill; record what the agent does and the exact rationalizations it uses |
| GREEN | Write minimal code to pass | Write the minimal skill that addresses those specific failures; re-run and confirm the agent now complies |
| REFACTOR | Clean up | Close loopholes the agent found; re-test until bulletproof |

**REFACTOR re-runs cover the edited rule's whole blast radius.** When a REFACTOR edits a
rule, re-run the scenario that failed AND every other scenario that rule governs — a fix
validated only on the case that exposed it can silently open an escape hatch in a sibling
case. Motivating case (2026-07-22, `sandwich-test`): the rewritten tier-calibration rule
passed its version-bump re-run but shipped untested against the destructive cleanup
scenario — the skill's flagship case; the final whole-branch review caught the gap and a
fresh regression run closed it.

## When the baseline already passes

A capable model often already does much of what a **persona or lens skill** would do when the
artifact is small and fully in context — it has the judgment and the facts are right there. So a
RED that *doesn't fail* means one of two things, and you must tell them apart: the test is too
easy, or the skill is redundant. Distinguish them by **hardening the artifact** (make the target
subtle, not sign-posted; use a realistic quick-look ask, not a plea for a maximally-thorough
review; sample more than one baseline) and **isolating the differential** — the specific thing the
skill adds that a good neutral reviewer misses — instead of measuring raw capability. If a
hardened, differential-isolating test still shows no gap, the skill isn't earning its keep.

This is the sibling of the memory-skill caveat in `CLAUDE.md`: single-shot tests can't reproduce
cross-session context loss, but they *can* test a lens skill — only if the artifact is hard enough
to separate the lens from baseline competence. Proven authoring `paladin-review` (2026-07-19): the
naive RED caught the planted footgun *and* the under-sell, so it looked like the skill added
nothing; only a subtle, quick-look artifact run against two baselines isolated the under-sell +
blast-radius lens the neutral reviewers missed (and inverted).

## A rule that always fires has a cost — gate it

A safety or coverage rule stated as an absolute ("always convene both siblings," "review after
every task," "run the full ceremony") over-fires: it pays its full price on the many cases where
it has nothing to catch. Three such rules were added and walked back within days in this lab's own
history — mandatory nemesis+paladin pairing, the full-court default, and premium per-task build
reviews — each measured (2026-07-21 token audit) as costing far more than the failure it prevented
(a review's real driver was the ceremony, not the ~83k paladin; builds ran ~1-2.3M, dominated by
premium per-task reviews). The fix is never to drop the safety; it is to **route the rule through a
cheap triage gate** — fire it by the RISK actually present (author-outcome? irreversible?
correctness-only?), not unconditionally. Same shape as the assumption-debt "scope of a rule" trap,
and a sibling of "When the baseline already passes": both are a skill spending effort where the
stakes don't warrant it.

**Measure before you scrap.** Before retiring or blaming a skill for cost, read the real numbers:
every subagent stamps `subagent_tokens: N` in its result, so a transcript grep buckets true
per-skill / per-model cost in one cheap pass. Fire-rate (`tools/skill_usage_report.py`) tells you
IF a skill runs; the `subagent_tokens` stamps tell you what it COSTS — and the two answer different
questions.

## Authoring conventions

- **One skill per folder** under `skills/`, named in active voice (`creating-x`, not `x-creation`).
- **`SKILL.md` frontmatter:** `name` (hyphens only) and `description` (third person,
  "Use when…", triggers/symptoms only; no workflow summary). Max 1024 chars.
- **Keep it scannable:** overview with the core principle, a quick-reference table, a
  common-mistakes section. Use a small flowchart only for non-obvious decision points.
- **One excellent example** beats five mediocre ones in different languages.
- **Separate files** only for heavy reference (100+ lines) or reusable tools/scripts.
- **Match the form to the failure:** prohibitions + rationalization tables for discipline
  failures; positive recipes/contracts for wrong-shaped output.

## Skill types

- **Technique**: a concrete method with steps (e.g. condition-based-waiting)
- **Pattern**: a way of thinking about a class of problems
- **Reference**: API docs, syntax guides, tool documentation
- **Discipline**: enforces a rule under pressure (needs rationalization tables + red flags)

## Starting a new skill

Copy `_template/SKILL.md` into `skills/<your-skill-name>/SKILL.md` and fill it in.

## Logging value: the Provenance win rule

Usage counts are decoration; **logged wins are evidence.** Every skill carries a `## Provenance`
section, and the standing rule is:

> When a skill visibly earns its keep in the field (catches a defect, prevents a bad commit,
> saves a rework cycle), append a dated one-line win to its Provenance section **in the same
> session**: the moment is the signal, and it does not survive until "later."

- Keep entries scrubbed (this repo is public): what was caught and why the skill's mechanism
  caught it, never the maintainer's personal details.
- Provenance is also the **retirement test**: a skill that fires often but accumulates no wins
  is a deletion candidate. Check fire-rate with `tools/skill_usage_report.py`, which sweeps the
  local Claude Code transcripts and flags lab skills that are never invoked.
- Formal A/B evals (baseline vs with-skill) remain the only measure of the counterfactual;
  reserve them for authoring time and major revisions (the RED → GREEN flow above), not
  continuous monitoring.
