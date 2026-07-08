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

## Authoring conventions

- **One skill per folder** under `skills/`, named in active voice (`creating-x`, not `x-creation`).
- **`SKILL.md` frontmatter:** `name` (hyphens only) and `description` (third person,
  "Use when…", triggers/symptoms only — no workflow summary). Max 1024 chars.
- **Keep it scannable:** overview with the core principle, a quick-reference table, a
  common-mistakes section. Use a small flowchart only for non-obvious decision points.
- **One excellent example** beats five mediocre ones in different languages.
- **Separate files** only for heavy reference (100+ lines) or reusable tools/scripts.
- **Match the form to the failure:** prohibitions + rationalization tables for discipline
  failures; positive recipes/contracts for wrong-shaped output.

## Skill types

- **Technique** — a concrete method with steps (e.g. condition-based-waiting)
- **Pattern** — a way of thinking about a class of problems
- **Reference** — API docs, syntax guides, tool documentation
- **Discipline** — enforces a rule under pressure (needs rationalization tables + red flags)

## Starting a new skill

Copy `_template/SKILL.md` into `skills/<your-skill-name>/SKILL.md` and fill it in.

## Logging value: the Provenance win rule

Usage counts are decoration; **logged wins are evidence.** Every skill carries a `## Provenance`
section, and the standing rule is:

> When a skill visibly earns its keep in the field (catches a defect, prevents a bad commit,
> saves a rework cycle), append a dated one-line win to its Provenance section **in the same
> session** — the moment is the signal, and it does not survive until "later."

- Keep entries scrubbed (this repo is public): what was caught and why the skill's mechanism
  caught it, never the maintainer's personal details.
- Provenance is also the **retirement test**: a skill that fires often but accumulates no wins
  is a deletion candidate. Check fire-rate with `tools/skill_usage_report.py`, which sweeps the
  local Claude Code transcripts and flags lab skills that are never invoked.
- Formal A/B evals (baseline vs with-skill) remain the only measure of the counterfactual;
  reserve them for authoring time and major revisions (the RED → GREEN flow above), not
  continuous monitoring.
