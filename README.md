# peckworks-skills-laboratory

A workshop where **skills for LLM agents are engineered, not just written**: developed
test-first against baseline agent behavior, hardened by adversarial review, deployed into
the live runtime by symlink, and required to earn their keep with a logged field-win record.

Every skill here is in daily production use in the maintainer's Claude Code setup. Nothing
ships on vibes: a skill exists because an agent was first observed failing without it.

## Quick start

```bash
git clone <this-repo>
cd peckworks-skills-laboratory
bash install.sh        # symlinks every skills/* into ~/.claude/skills (idempotent)
```

Skills load at session start, so open a new Claude Code session to pick them up. Because
they are symlinks, editing a skill in the repo updates the installed copy: one source of
truth, no drift. The skills are also portable to any runtime that reads the
[agentskills.io](https://agentskills.io) `SKILL.md` format: copying a skill folder into
that runtime's skills directory is enough.

One skill (`managing-assumption-debt`) is optionally hook-powered; `install.sh` prints the
`settings.json` wiring it needs at the end of its run.

## The discipline

- **TDD for skills.** RED: run the scenario without the skill and record the exact failure
  and the rationalizations the agent uses. GREEN: write the minimal skill that fixes those
  specific failures. REFACTOR: close the loopholes the agent finds next. The full process
  is in [CONTRIBUTING.md](CONTRIBUTING.md).
- **Adversarial hardening.** Drafts get reviewed by isolated skeptic subagents, including a
  motivated-but-honest adversary (see `nemesis-review`, which is itself a skill here).
- **Provenance, or it didn't happen.** Each skill carries a **dated field record**: the baseline
  failure it was born from, plus dated wins appended whenever it catches something real. Discipline
  and lens skills keep it under a `## Provenance` heading; the ones that accrete lessons run-by-run
  keep it as dated `## Field validation` / `## Rules added <date>` sections instead, because a
  chronological log reads better in place than a single appendix. What is non-negotiable is the
  *date and the specific failure*, not the heading. Pure technical-recipe skills (`cadquery-modeling`)
  are the exception: their evidence is the recipe, which either builds the part or doesn't.
  A skill that fires often but logs no wins is a retirement candidate.
  `tools/skill_usage_report.py` sweeps the local Claude Code transcripts to report fire-rates and
  flag never-invoked skills.
- **Two-tier privacy: engine vs. fuel.** This repo holds the shareable *engine* of each
  skill; the maintainer's personal context (logbooks, run logs, reader profiles, identity)
  is the *fuel*, and it stays out of git. The mechanism is structural, not disciplinary:
  only `*.template.md` schemas are tracked, the real files are gitignored, and the skills
  read the untracked local copies. A skill that needs personal state says "if one exists,
  consult it" and works without it.

## The skills

| Skill | What it does | Born from |
|---|---|---|
| `managing-assumption-debt` | Catches high-leverage unstated assumptions between a human and an agent before they compound; ships SessionStart/PreCompact hooks that re-inject the standing layer | 17 real assumption-debt episodes mined from weeks of transcripts |
| `nemesis-review` | Adversarial review by a motivated-but-unassailable expert: hostile enough to dig, honesty-gated so findings stay defensible, with a mandatory concession section | A design plan whose polite reviews kept passing while real flaws survived |
| `paladin-review` | The supportive mirror of the nemesis: a reviewer bound by a life-debt who protects your *outcome* — catches where you're about to hurt yourself (irreversible / secret-leaking footguns) and where you under-sell a real win, behind a dual honesty gate (no flattery, no crying wolf) | Two neutral reviews that caught a planted secret leak but missed — and inverted — a real bug the author called "nothing risky" |
| `deletion-tripwire` | A mechanical PreToolUse hook that blocks destructive commands until enumerate → confirm → ledger → approve; blast radius is everything *reachable*, and safety comes from enumeration, never prediction | A public data-loss incident (a cleanup followed folder-links into live Documents/Pictures after the agent predicted "safe") plus a local "clean up junk" pass that deleted test evidence |
| `review-court` | The harness that convenes the full panel as a guaranteed ceremony — intent packet, both siblings invoked fresh, domain skeptics, isolated parallel dispatch, orchestrator verify-pass, receipts archived before cleanup | Hand-rolled review ceremonies that silently dropped steps: the pairing rule (seven reviews in a row) and, later, the run's own evidence |
| `iterative-lesson-refinement` | Hardens a teaching artifact into "defend it live" form via isolated learner/expert personas and an escalating cold quiz; 18 generalizable teaching lessons | A clean-reading lesson that scored 10/10 on recall while hiding real holes |
| `educational-html-prep` | The Feynman teaching-page craft: plain claim, analogy, inline-SVG diagram, defend-cold Q&A, plus a reusable CSS component kit and visual-verify workflow | ~15 study pages of accreted rules and repeat mistakes |
| `versioning` | One canonical VERSION stamped into every independently-deployed artifact, each self-reporting, with a drift check | Multi-artifact repos where "is the fix actually deployed?" had no answer |
| `emoting-on-8x8` | Making expressions legible on a 64-pixel LED matrix at low brightness: silhouette test, brightness-band color math, motion-carries-meaning | An ESP32-S3 matrix that kept rendering mud |
| `feynman-explanation` | Explaining to someone working cold: map first, analogy before code, every symbol and acronym defined at first use, a per-learner mastered list so training wheels come off per item | A sharp learner who kept getting buried under unglossed jargon and walls of text |
| `avoid-sycophantic-blowback` | Kills the hype-then-crash cycle when reporting news to a human: calibration before interpretation, a signal-strength taxonomy, mood counterweighting, and a one-word recalibration codeword | A staffing firm's templated shortlist email that got amplified into an emotional crash |
| `sandwich-test` | Closes the intent–interpretation gap at instruction handoff: a five-class misread taxonomy, a tiered live protocol (silent check → state the reading → hard-stop at the irreversible line), and a cold-reader audit that rebuilds the PB&J game's barrier with isolated subagents | The peanut-butter-and-jelly game: an executor following the letter of an instruction while feeling fully compliant |
| `capturing-judgment-as-data` | Turns a human's taste verdicts into a reproducible record instead of unrepeatable comments: pair-structured rounds, frozen baselines and rollback as first-class, drawings over comment boxes | Feedback that kept arriving as comments nobody could reproduce, and a fix "verified" against an instrument the human couldn't see |
| `look-driven-iteration` | The cheap-render → grounded-feedback → measure-then-fix loop for work judged by eye; its core claim is a spending rule — review and tests gate *shipping*, not *exploring* | Expensive verification burned on looks the human had not approved yet |
| `guarding-silent-failures` | Operations that fail while returning valid-looking output, and the checks meant to catch them — including the rule that a clean probe result is only evidence if the probe was first proven able to fail | One CAD session that hit six in a day: a fillet that ate 38% of a part and rendered fine, an AO pass that "worked" and did nothing, a cleanup that reported removing twelve files it never touched |
| `stretching-frontier-tokens` | Spends the strongest model only where the frontier matters: measure the transcript first, then climb *down* — script it, cheapest capable model, frontier only for diagnosis, design, and prose aimed at the human | A measured session where images were 76.7% of all bytes and the frontier model did 100% of the loop, including screenshot choreography |
| `cadquery-modeling` | CadQuery/OpenCASCADE recipes: identify edges by what they *are* with an asserted count, because point-based selectors lie; select topologically when no geometric test can separate the boundaries | `fillet()` dying with "no suitable edges" on geometry whose pocket and outer edge overlap in radius |

A note on flavor: these are **live production copies, not genericized forks.** Some skills
reference the maintainer's own workspace (a study-page dashboard, specific repos, a private
reader profile) because that specificity is what makes them work daily. Treat those parts
as a worked example of the pattern and swap in your own equivalents; the mechanisms
(the personas, the gates, the checklists, the rationalization tables) are the portable part.

## What is a skill?

A folder containing a `SKILL.md` (plus any supporting files). The YAML frontmatter has two
required fields:

- `name`: letters, numbers, and hyphens only
- `description`: third person, starts with "Use when...", describes *when to use the skill*
  (the triggering conditions), **not** what it does step by step

The description is the only thing an agent reads when deciding whether to load a skill, so
it must be rich with concrete triggers, symptoms, and keywords. It must *not* summarize the
workflow: if it does, agents follow the summary and skip the skill body.

## Repository layout

```
peckworks-skills-laboratory/
  README.md
  CONTRIBUTING.md          # conventions + the TDD-for-skills workflow + the win-logging rule
  LICENSE                  # MIT
  install.sh               # idempotent: symlinks every skills/* into ~/.claude/skills
  skills/
    <skill-name>/
      SKILL.md             # required
      <supporting files>   # optional: hooks, CSS kits, references, *.template.md schemas
  tools/
    skill_usage_report.py  # transcript sweep: per-skill fire-rate, last-used, never-invoked
  _template/
    SKILL.md               # copy this to start a new skill
  docs/specs/              # design specs (YYYY-MM-DD-<topic>-design.md)
```

## Contributing

Start from `_template/SKILL.md`, but read [CONTRIBUTING.md](CONTRIBUTING.md) first: the
iron law is *no skill without a failing test first*, and that applies to edits too.

## License

[MIT](LICENSE)
