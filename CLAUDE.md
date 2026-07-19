# peckworks-skills-laboratory: Project Brief (read me first)

A workshop for developing, testing, and refining **skills** for Claude and other LLM agents.
Each skill is a self-contained `SKILL.md` (plus supporting files) in a flat `skills/` namespace.

> **Privacy: this repo is PUBLIC** (github.com/srfinch17/peckworks-skills-laboratory, since
> 2026-07-08; every push ships to the world). NEVER write the maintainer's real name into any
> file here (code, comments, docs, skills). Refer to "the user" / "the maintainer". Personal,
> identity-specific content (a personal logbook, a real reader profile, named companies from
> the job search, private-memory-store paths) lives in the maintainer's PRIVATE memory or in
> gitignored local files; only `*.template.md` schemas are tracked. The full pre-public
> history lives ONLY in the local `private-history` branch: NEVER push it anywhere.

## Layout

```
skills/<skill-name>/SKILL.md   # one skill per folder; required frontmatter: name, description
_template/SKILL.md             # copy to start a new skill
docs/specs/                    # design specs (YYYY-MM-DD-<topic>-design.md)
install.sh                     # idempotent: symlinks every skills/* into ~/.claude/skills
README.md · CONTRIBUTING.md    # what a skill is · the test-first workflow + conventions
```

## How we work here

- **Test-first (TDD for skills).** No skill ships without first watching an agent behave
  WITHOUT it (baseline), then verifying the skill changes that behavior. RED → GREEN →
  REFACTOR. Full process in `CONTRIBUTING.md`. This applies to edits too, not just new skills.
- **Frontmatter rules:** `name` (letters/numbers/hyphens only); `description` third-person,
  starts with "Use when...", describes ONLY triggering conditions; never summarize the
  workflow (agents follow the summary and skip the skill body if you do).
- **Match the form to the failure:** prohibitions + rationalization tables for discipline
  failures; positive recipes/contracts for wrong-shaped output.
- One excellent example beats five mediocre ones. Separate files only for heavy reference or
  reusable tools.
- **Cost discipline:** low-judgment work (bulk mechanical edits, sweeps, memory/notes
  housekeeping, CLAUDE.md touch-ups) goes to cheap subagent models (haiku); the main model
  writes the rules, reviews the output (cheap models introduce real defects), and owns
  anything committed or pushed.

## Installing these skills

The `skills/` folder is the *workshop*, not a discovery path. Claude Code loads skills from
`~/.claude/skills/`, so each skill is **symlinked** there (edit in the repo → the installed
copy updates; one source of truth). Run `bash install.sh` to (re)create the symlinks: it is
idempotent, auto-discovers every `skills/*/SKILL.md`, and won't clobber a real non-symlink.

**Per-machine, and not synced by Dropbox:** `~/.claude/` lives outside Dropbox, so the install
symlinks (and any hook wiring in `~/.claude/settings.json`) must be reconstituted on each
machine; `install.sh` handles the symlink half. Skills load at session start, so restart to
pick up changes. (`.gitattributes` pins `*.sh` to LF so the script can't get CRLF-mangled.)

## Skills here

### `managing-assumption-debt`  (status: deployed + tested + hooked)
Catches high-leverage unstated assumptions early, before they compound into expensive
misunderstandings. Two-tier design:
- **Engine (here, shareable):** `skills/managing-assumption-debt/SKILL.md` +
  `LOGBOOK.template.md` + `hooks/`. The concept, the four debt types + tells, the triage
  formula, the bidirectional escalation vocabulary (light flag / "I'm willing to fight about
  this" / sunk-cost call), the trigger moments, and the logbook loop.
- **Fuel (the maintainer's PRIVATE memory, not in this repo):** a personal logbook of real
  assumption-debt episodes. The engine only says "if a personal logbook exists, consult it."
- **Hooks (`hooks/`, generic, logbook path passed as an argument):**
  `inject_standing_layer.py` (SessionStart: re-injects the logbook's standing layer each session
  + a 7-day human reminder) and `capture_on_compact.py` (PreCompact: prompts a capture pass
  before context is summarized). Wired in the maintainer's live `~/.claude/settings.json`.
- Design of record + full test log: `docs/specs/2026-06-30-assumption-debt-design.md`.

**Key lesson from testing this skill (applies to ANY memory-type skill):** a SKILL.md does not
self-improve, and modern models already have strong in-the-moment judgment whenever the facts are
in context. The failure this skill prevents is context LOSS across sessions/compaction, which is
NOT reproducible in single-shot subagent tests (any fact in the prompt is present and attended to).
So the load-bearing value lives in the MEMORY + HOOK re-injection layer, not the judgment prose.
Invest there. The engine remains worth keeping: it is safe (does not over-fire), it adds
scope-probing + a shared escalation vocabulary, and it gives the discipline to consult the logbook.

**Next (optional):** a PreToolUse boundary guard (advisory-inject hard-stop before push/publish/send).

### `iterative-lesson-refinement`  (status: field-proven engine port, 2026-07-05)
Hardens a teaching/study artifact into defend-cold form by testing it against ISOLATED persona
subagents (NOOB / BASICS / EXPERT), grading an escalating cold quiz, and folding generalizable
teaching lessons back into the skill. Two-tier, like assumption-debt: the lab holds the scrubbed
**engine** (the loop, quiz design, the 18 teaching lessons, the cheap 2-agent "targeted
validation" mode for revamps); the maintainer's topic-specific run logs stay in the private
workspace. Provenance: 3 topics, 6+ passes, documented RED baseline (a clean-reading page scored
10/10 on recall while hiding real holes) and GREEN results in the skill's Provenance section.
**Single source of truth (2026-07-05):** the maintainer's former personal copy was archived
to private memory and replaced with the `install.sh` symlink, so this lab copy IS the live
skill. Future "fold the lesson back into the skill" steps edit THIS file, which lands in a
public repo, so each added lesson must stay generalizable and scrubbed (the skill already
mandates recording only generalizable lessons, never learner-specific facts).

### `nemesis-review`  (status: field-proven; deployed)
An adversarial review run by a fictional **expert who wants you to fail** but whose ego depends on
being **unassailable**, so he will not fabricate, inflate, or cry wolf. He concedes (through
gritted teeth) whatever is genuinely sound. The hostility is a lens for candor and effort; the
honesty gate keeps the output signal. Three load-bearing elements: motivated (professional, not
personal) hostility, the honesty gate, and a mandatory concession section (the trust anchor and
highest-value signal). Skill: `skills/nemesis-review/SKILL.md`, with the reusable dispatch charter
inline.
- **Orchestration rules:** run the nemesis as an ISOLATED subagent beside 2 to 4 dispassionate domain
  skeptics (breadth), then verify every finding yourself before acting; hostility's failure
  mode is false positives. Convene its sibling `paladin-review` (below) alongside it — the pair
  is run together.
- **Provenance:** first proven 2026-07-01 on the peckworks-bonsai trunk-engine plan (found net-new
  issues the polite reviewers missed; its concessions independently validated the architecture).
  Full episode lives in the maintainer's PRIVATE memory (`nemesis-review-works`), not this repo.

### `paladin-review`  (status: born here 2026-07-19; RED/GREEN tested)
The supportive mirror of `nemesis-review`: a reviewer who owes you an unpayable life-debt (you
saved his child) and repays it only by making you WIN and keeping you from harm. Same rigor,
opposite motive — the nemesis attacks whether the work is *sound*; the paladin protects your
*outcome*, hunting the two things a soundness reviewer structurally can't: where you're about to
**hurt yourself** (a destructive / irreversible / secret-leaking footgun) and where you're
**under-selling a real win**. The whole safety lives in a *dual* honesty gate — comfort-is-betrayal
(no flattery) AND a-false-alarm-gets-you-tuned-out (no crying wolf) — guarding both sides of its
two-sided failure mode. Skill: `skills/paladin-review/SKILL.md`, dispatch charter inline.
- **Orchestration:** run it ISOLATED beside `nemesis-review` + domain skeptics; as orchestrator,
  verify every alarm (paranoia over-reports, the mirror of the nemesis's false positives) and
  DISCOUNT its praise (motivated), weighting its warnings. Never substitute it for a correctness
  review — a capable neutral reviewer already catches most defects and secret leaks.
- **Provenance:** RED/GREEN at authoring (2026-07-19). Two neutral baselines caught the planted
  secret leak but MISSED and inverted the under-sell; the charter surfaced it plus the fixed bug's
  blast radius, while visibly refusing to flatter or cry wolf. Design spec:
  `docs/specs/2026-07-19-paladin-review-design.md`.

### `educational-html-prep`  (status: field-proven; ported from personal 2026-07-05)
The Feynman teaching-page craft: plain-claim → analogy → inline-SVG diagram → defend-cold Q&A,
the mission-control THEME tokens, the reusable `assets/teaching-kit.css` component kit, the
inline-SVG patterns (`references/svg-diagrams.md`), and the serve+screenshot visual-verify
workflow. The maintainer's most-used homegrown skill (11 invocations at port time). Scrubbed
port of a personal skill that accreted rules across ~15 pages; some content is specific to the
maintainer's career workspace (dashboard registration, back-link): kept because this is the
live skill (symlinked), not a genericized fork.

### `emoting-on-8x8`  (status: field-proven; ported from personal 2026-07-05)
Designing legible expressions/animations for a 64-pixel LED matrix at low brightness: the
silhouette test, brightness-band color math, downsample-don't-freehand, motion-carries-meaning,
iterate-live-promote-winners. Companion to the maintainer's public esp32s3matrix repos.

### `versioning`  (status: field-proven; ported from personal 2026-07-05)
One canonical VERSION file stamped into every independently-deployed artifact, each made
self-reporting, plus a drift check and the "a bump is not live until its artifact redeploys"
rule. Distilled from the esp32s3matrix/expression-studio repo split; also the pattern behind
clipmeta's release flow.

### `feynman-explanation`  (status: born here 2026-07-10; scrubbed; RED/GREEN tested)
The plain-language explanation discipline: one idea at a time, a real-world analogy before the
code, define the SYMBOL (not just the logic) and spell out the acronym the FIRST time each
appears, kill "obviously", open the real code instead of quizzing memory, and proofread output
for jargon density + length at write-time. Includes the field-proven techniques (map-first and
"I'll hold it", explain with actual values not abstractions, collapse overwhelm to one next
action, the whole-tiny-TDD-loop unit of progress, explain-back checkpoints) and the
training-wheels protocol (a per-project "mastered" list; once the learner owns an item, stop
re-glossing it, per item). Two-tier like the others:
- **Engine (here, shareable):** `skills/feynman-explanation/SKILL.md` + `MASTERED.template.md`
  (the mastered-list schema). Scrubbed to "the learner"/"the user".
- **Fuel (per-project, local):** the real `MASTERED.md` lives in whatever project is being
  worked in and is gitignored; only the template is tracked here.
- Scrubbed public port of the maintainer's private, high-priority communication rule
  (`preferences.md`, Communication, 2026-07-09: ADD + new-to-a-language + Feynman duty,
  training-wheels-off-on-request, spell-out-acronyms). Seeded from field notes taken during the
  2026-07-09/10 codebase-rag eval + CI build, where the method demonstrably kept an overwhelmed
  learner engaged and able to defend the result. **Testability note:** unlike the memory-type
  skills, most of this one is write-time output shaping and so is genuinely testable in a single
  isolated run; only the mastered-list persistence is the un-testable cross-session layer.
