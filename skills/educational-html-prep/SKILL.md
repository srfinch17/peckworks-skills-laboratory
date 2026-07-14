---
name: educational-html-prep
description: >-
  Build or upgrade Feynman-style HTML study/teaching pages for the maintainer's job-search & AI-native
  learning workspace, matching the dark "mission-control" dashboard identity. Use this WHENEVER
  the maintainer asks to "flesh out / punch up / make a learning page", turn dense notes or a markdown
  study pack into real teaching material, add diagrams/charts/icons to a study or reference page,
  make a guide "top notch" or "ace-interviews" ready, build interview-prep or onboarding HTML, or
  create a themed standalone HTML page in this workspace. Also use it when adding inline SVG
  diagrams to explain a concept, or when he says "do the same to the rest of the library". Covers
  the teaching method (plain-English → analogy → diagram → defend-it Q&A), the THEME tokens, the
  reusable CSS kit, inline-SVG diagram patterns, and the dashboard-registration workflow.
---

# Educational HTML Prep

Turn a topic the maintainer needs to *learn and defend in interviews* into a page he can read top-to-bottom
and walk away genuinely understanding: Feynman-grade teaching inside the existing mission-control
visual identity. This is for his job-search learning workspace (the AI-Native roadmap,
the Study/ pages, company-specific interview prep, the dashboard guides).

## The prime directive: teach, don't just present

A good page here is not a styled dump of notes. It makes a beginner *get it*. For every concept:

1. **Plain-English claim first.** One sentence, no jargon, the way you'd explain it to a smart
   friend who's never seen it. ("RAG turns a closed-book exam into an open-book one.")
2. **A Feynman analogy.** A concrete everyday image that carries the mechanism (image=recipe,
   container=the cooked meal; a skill's description = the spine label on a binder). Put it in a
   `.analogy` aside.
3. **A diagram.** If the idea has structure, flow, or levels, *draw it* as inline SVG. A picture
   replaces three paragraphs. (See `references/svg-diagrams.md`.)
4. **"Defend it cold" Q&A.** 2 to 4 `.qa` blocks: the hard questions the topic invites, answered so the
   reader can CHECK whether he truly understands (could he re-derive this answer, closed-book, in his own
   words?). Defend-cold means UNDERSTANDING deep enough that any question gets a real answer; it does NOT
   mean rehearsing lines. The maintainer is studying to genuinely know the thing (the lesson of a lost
   final-round interview was shallow ownership, and a scripted answer is shallow ownership in nicer
   clothes), so anticipate the follow-up that exposes a bluff, and answer it by teaching the mechanism.
5. **Tie it to what he's actually built.** Map the concept to a real repo (peckworks-rag-lab,
   appointmentflowoptimizer, esp32s3matrix) so it's anchored, not abstract, but never claim a skill
   he doesn't have. HAVE / PARTIAL / GAP must stay honest.

Order matters: concept → analogy → diagram → run-it/see-it → defend-it. Lead with the why before
the how.

## Non-negotiable constraints (these are the maintainer's standing rules)

- **PRIVATE TEACHING TOOL, understanding-first (recalibrated 2026-07-13, the maintainer's explicit
  correction).** A learner page exists to TEACH the maintainer, full stop. It is never shown to anyone
  else and is not a showcase; the interview matters only as the place understanding gets tested, never as
  the thing the page optimizes. Concretely BANNED in any learner page: scripted first-person answers in
  quotes for the reader to recite; impression-management coaching ("what to volunteer", "how to sound",
  "what to say in a screen"); framing any section as interview strategy. `.qa` blocks are comprehension
  self-tests answerable in the reader's own words. Honesty bookkeeping (HAVE/PARTIAL/GAP, provenance
  lines) STAYS, phrased as facts about his current knowledge, not tactics. When a QA panel uses an
  interviewer persona, apply its findings about TRUTH (overclaims, contradictions, terms used but never
  taught) and translate its findings about PERFORMANCE (a better line to say) into teaching the
  underlying mechanism, or drop them. (Origin: Learning_React v1.1 drifted into scripted answers and
  volunteering tactics; the maintainer caught it: these pages "are not a resume showcase, they are
  supposed to be a feynman like tool to teach me something.")
- **Match the identity; never invent a new palette.** Reuse the THEME tokens below. Bright,
  saturated, clearly-distinct sections with icons and colorful chips. This OVERRIDES any generic
  "take an aesthetic risk" design instinct; the whole library must feel like one product.
- **Never fabricate the maintainer's experience.** Every claim must be one he can defend. If something is a
  GAP, say GAP and point at the rep that closes it. AI-first claims pass the Review Board bar.
- **NO EM-DASHES in the rendered page (the "—" character).** The maintainer hates them as AI-slop and got burned
  by em-dashes shipping on resumes he had already sent (2026-06-24). This applies to ALL visible copy:
  headings, body, `.analogy`/`.qa` text, figure captions, SVG `<text>` labels. Use commas, colons, periods,
  or parentheses; use "to" for ranges. It is a standing GLOBAL preference (recorded in the maintainer's private memory).
  Before declaring done, grep the file for "—" and replace every hit. (En-dashes in pure number ranges are
  tolerated, but prefer "to".)
- **⚠️ A page you build for the maintainer is a STUDY AID, not evidence the maintainer authored or owns its ideas.**
  These pages carry his name in the header and speak in first person ("I designed…", "your question,
  answered"), which makes them look, later, like a record of his original thinking. They are not.
  When the page teaches an *industry concept* (RAG, self-healing, MCP), say so plainly inside the page,
  and **NEVER** let the page become downstream evidence: do not write memory notes like "(the maintainer's own
  idea)", and do not flip a roadmap/resume status to HAVE/"concept owned" because a teaching page exists.
  The page teaches the pattern; only a *repo he built* or *thinking he can defend cold* earns the claim.
  (Learned 2026-06-22: the Orchestration_Handbook self-healing section got escalated into "the maintainer
  theorized self-healing systems" across the roadmap + a build spec; the maintainer didn't recognize the page
  (*"I don't even remember writing it"*), and it all had to be recalibrated to GAP. See the
  `resume-claim-grounding` memory.)
- **Offline-first.** Inline everything that matters (SVG, CSS). Google Fonts may load from CDN but
  must degrade gracefully (always give a `system-ui` fallback). No build step, no external JS libs.
- **Self-contained pages.** One `.html` file, internal `<style>`, internal SVG. It must open from
  `file://` and survive the dashboard's `guides/` wipe-and-regenerate.

## Two page modes: study aid vs. standalone product page

This skill's defaults assume a **study aid** living *inside* the job-search workspace. But the same
theme + teaching method also makes an excellent **public landing/info page for one of the maintainer's own
shipped projects** (e.g. the clipmeta GitHub Pages page, in the project's own repo under `docs/`).
When the page is a standalone product page, **three of the defaults above invert**; apply these
carve-outs (verified building the clipmeta page, 2026-06-22; see the `peckworks-clipmeta`
`project-landing-page` memory):

- **Give it its OWN identity, not the L1→L2→L3 staircase favicon.** The "one identity, never invent
  a new mark" rule is scoped to the job-search *library*. A separate public product deserves its own
  favicon/brand (clipmeta got a film-frame + tag mark). Still inline it as a data-URI for offline
  safety (just don't reuse the staircase).
- **Do NOT register it in `dashboard.py`'s `GUIDES`.** That registry is only for the job-search
  workspace. A product page lives in its own repo and is deployed by *that* project (GitHub Pages
  `main → /docs`), so the "never orphaned → add a GUIDES row" step does not apply.
- **The authorship-fabrication warning relaxes but stays honest.** The ⚠️ "a page you build is
  not evidence the maintainer authored its ideas" rule exists because *study aids teach industry concepts*.
  A page **about the maintainer's own project** legitimately speaks in first person and claims the work, which
  *is* his. Keep the honesty bar for any *general* concept the page also teaches (MCP, the MP4
  format), and never invent screenshots/benchmarks: use clearly-labeled placeholder slots the owner
  fills from real use. (clipmeta's launch is gated on the maintainer dogfooding it first; the page was built
  and approved but deliberately not published.)
- **Still applies, unchanged:** the teaching sequence (plain-English → analogy → diagram → defend-it
  Q&A), THEME tokens, the CSS kit, offline/self-contained, and (non-negotiable) **serve +
  screenshot every inline-SVG diagram before declaring done** (see below; SVG text overflow and
  label collisions are invisible in source).

## The visual identity (THEME tokens)

Use these exact values (they mirror `dashboard.py` THEME_VARS). Define them as CSS `:root` vars on a
new page; for inline SVG `fill`/`stroke`, use the raw hex (SVG attributes don't read CSS vars).

```
--ink:#0D1015   --ink-2:#151A21   --ink-3:#1C2330        (backgrounds, darkest→lighter)
--line:#2C3442  --line-soft:#212834                       (borders)
--text:#EAEDF3  --muted:#94A0B2   --muted-2:#5F6A7B       (text)
--signal:#FF8A3D   orange: primary accent / "the point" / HAVE-of-attention
--have:#2BE0CE     teal: built/owned/correct
--partial:#F5C13D  amber: in-progress / caution / tuning
--adjacent:#6E9BFF blue     --violet:#B98CFF: secondary categories
--offer:#2EE36E green   --deny:#FF5C82 pink
Fonts: "Space Grotesk" (display/headlines), "IBM Plex Sans" (body),
       "IBM Plex Mono" (code, labels, eyebrows, data).
Teal-tinted panel fill for "owned" callouts: #102a28. Orange-tinted: #17120a.
Grid background + radial fade = the mission-control texture (see an existing page).
```

Section accent convention: give each major teaching block ONE accent via the `.teach`,
`.teach.cyan`, `.teach.violet`, `.teach.amber` variants, and carry that color through its kicker
icon, list bullets, and diagram highlights. Distinct color per section = the "clearly-distinct,
icon'd sections" the maintainer asked for.

## The reusable CSS kit

`assets/teaching-kit.css` holds the full set of utility classes used across the library:
`.teach` (accent-barred teaching panel) and `.cyan/.violet/.amber` variants, `.kicker` (eyebrow +
icon), `.fig`/`.figcap` (SVG figure frame), `.analogy` (Feynman aside), `.tgrid`/`.tcard` (mini
card grid), `.qa` (defend-it Q&A), `.courses`/`.course` (course-link cards). When building a NEW
standalone page, paste this kit into its `<style>` (after the page's `:root` token block) so it
stays self-contained. When ENHANCING a page that already has the kit (e.g. the roadmap), reuse the
existing classes (don't duplicate them).

### Two components added 2026-06-30 (Learning_Python + Learning_ClaudeCode_Commands)
- **`.cmp` side-by-side comparison**: a 2-column grid of two labeled code panels for "B explained via
  the A you already know" topics. Built for Python-for-a-C#-dev: blue `.lbl.cs` panel left, teal `.lbl.py`
  panel right; each `.col` wraps a label bar + a `pre`. **Lesson: for a TRANSLATION topic (learn
  language/tool B from the A the reader knows), side-by-side code beats a diagram**: put the two literally
  next to each other and the eye does the mapping. Collapses to 1 column under ~640px. Use `--adjacent`
  (blue) for the "known" side, `--have` (teal) for the "new" side. (Definition in `assets/teaching-kit.css`.)
- **`.cmdtbl` catalog table**: compact 2-col `<table>` (mono command/term in `--have`, description) for a
  reference page that must list MANY items briefly (e.g. the ~70 Claude Code slash commands). Group the
  items into several `.teach` blocks by theme, each holding one `.cmdtbl`, instead of one card per item.
  Optional inline `.pill` / `.pill.flow` tag to mark item subtypes. (Definition in the kit.)
- **Reference page vs lesson page:** when the maintainer wants a *reference* ("general learning, not interview prep"),
  drop the `.qa` "defend it cold" blocks and the interview framing; keep the teach → analogy → example
  rhythm and close with a short practical "why this page exists" `.ground` note instead. Lessons keep the
  adversarial Q&A; references don't.
- **Deep-dive selection = the reader's GOAL, not item popularity.** When asked to "add a few more deep
  dives, use your judgment," pick the items that retell the maintainer's THESIS. For the slash-commands page the
  winning four were the AI-native governance stack (`/memory`+CLAUDE.md, `/hooks`, the review gate, parallel
  orchestration) because together they *are* his positioning. A coherent cluster that spells out his pitch
  beats a longer flat list. Each deep dive: kicker → plain claim → `ul` of mechanics → `pre` examples → an
  `.analogy` that ties to the why.
- **Disambiguating a CONFUSABLE SIBLING feature (added 2026-07-02, ultracode deep dive).** When a page
  teaches a thing the reader will confuse with a well-known neighbor (ultracode vs `/effort max`), the
  highest-value figure is a **two-panel SVG comparison built around the SINGLE axis that separates them**
  (here: go DEEP / one agent thinks harder, vs go WIDE / a lead fans out to many subagents), one accent
  color per panel (orange `--signal` = max, violet `--violet` = ultracode). This is NOT the `.cmp` code
  grid; `.cmp` is for translating code B↔A. This is a plain inline-SVG two-box figure because the subjects
  are *behaviors/shapes*, not code. The reader's real question is "how is this different from the one I
  know," so answer it spatially, side by side, with the one distinction bolded. Pair it with an `.analogy`
  that names the same axis ("your best engineer all-nighter" vs "staffing a team with a lead"). Also:
  **inserting a deep dive MID-sequence into a numbered reference page means renumbering** the nav codes,
  every following `<h2 class="sh"><span class="n">`, and the footer version line (not just appending).
- **Em-dash watch (recurring):** they sneak into SVG `<text>` labels AND code-block comments. The pre-ship
  grep for "—" is non-optional; sibling pages (Learning_Docker) shipped with stray em-dashes, so don't
  copy a sibling's header line without re-checking it. (Learning_RAG "v3.1 FINAL" carried ~40, including
  one in the `<title>` browser tab; Learning_Docker "v2.1 FINAL" carried 49 more that survived until
  the 2026-07-06 library sweep. A page marked final is not exempt from the grep, and the rule is
  grep any page you TOUCH, not only pages you create.)

### Components + rules added 2026-07-05 (Learning_RAG v4, the clipmeta-mission revamp)
- **The WORKED TRACE (`.step` + `.chunk`, defs in the kit) is the highest-value section of a pipeline
  lesson:** walk ONE real input through every stage end-to-end (real question → retrieved chunks as
  cards with score chips → the assembled prompt → the cited answer), then the **failure twin** (the same
  pipeline refusing an input it can't handle). Isolated-persona QA rated the trace the best section on
  the page. Two hard rules: (a) the example must not disprove its own lesson: demonstrating semantic
  search with a question that near-quotes the source chunk proves keyword search would work too, so
  paraphrase until zero surface tokens overlap; (b) **watermark invented numbers IN the artifact**
  ("sim 0.78", "(simulated)"), not only in a caption; realistic fake output becomes "observed data"
  one lazy memory later. (c) **When the trace demos a REAL system the reader can inspect (their own
  API/device/repo), ground every endpoint against the FULL handler, both the success AND error paths,
  not a grep of error returns.** A grep of the 4xx/error strings shows you how it rejects but hides
  success-path behavior, the response shape it actually returns and any silent normalization (clamping,
  defaulting, echoing the input back). Read each demoed endpoint's whole handler. (Field case 2026-07-07,
  a matrix-board REST page: grounding on the doc + an error-return grep taught two confident falsehoods
  about the reader's own device, that it 400s on out-of-range input, when the firmware clamps and returns
  200, and that success is a bare `{status:ok}`, when it echoes the value set. An armed nemesis reading
  the real handler caught both; a curl of the device would have detonated them live. On a page whose
  example is the reader's own hardware, "verify every claim against the source" is the whole ballgame.)
- **`.evtbl` starter-eval table (defs in the kit):** when a lesson precedes a hands-on build, ship a
  runnable "steal this" table of input → expected-result pairs (plus a negative/refusal probe row,
  class `probe`) drawn from the learner's real corpus. Turns the first run into a measurable experiment.
- **Home-stack currency check:** in a `.cmp` translation section, verify every claim about the READER's
  own stack against its CURRENT state ("SQL can't do vectors" died on SQL Server 2025's DiskANN vector
  indexes). Translation sections date fastest exactly where the reader is most expert.
- **End a project-primer with a MISSION section:** corpus/scope in and out (with the defensible reason
  for what's out), the exact commands, a "make it yours" step, and a definition of done. Gate any
  first-person "walk me through what I built" story card ("true only AFTER the mission") until the
  learner has actually run it; a study page that scripts past-tense accomplishment is a provenance trap.
- **Verify-step gotcha:** after editing a served page, Playwright can screenshot a STALE cached copy
  (re-navigating to the same URL or a #hash does not re-fetch). Hard-reload with a cache-buster query
  (`?v=N`) and glance for one of your new strings in the shot before trusting it.

### Components + rules added 2026-07-05 (Learning_VSCode, the Visual-Studio-to-VS-Code page)
- **`.mtbl` translation-mapping table (defs in the kit):** the `.cmp` counterpart for TOOL/UI
  translation topics (editor, IDE, platform, workflow), where the subjects are features, not code.
  Three columns: the KNOWN thing (mono, `--adjacent` blue), its NEW twin (mono, `--have` teal), and
  a plain "how you get there" cell (the shortcut / menu path). Same known=blue / new=teal color
  contract as `.cmp`. Used twice on the page: the window-to-window translation table and the
  keyboard cheat sheet. Rule of thumb: code-to-code translation → `.cmp` side-by-side panels;
  feature-to-feature translation → `.mtbl` rows.
- **Answer the commissioner's VERBATIM questions as `.qa` blocks.** When a page is commissioned by a
  frustrated, question-filled ask ("do I need a folder?", "will it write files I have to commit?"),
  quote each literal question as a `.qa` with a "YOUR Q" tag and answer it in place, in the section
  that teaches the underlying concept. The reader sees their exact words taken seriously, and the
  page doubles as a checklist that nothing they asked went unanswered.
- **Topbar navcodes must be SHORT: one word after the number.** The topbar `.wrap` has a fixed
  54px height; two-word labels on a 9-section page wrapped the navcodes out of the bar and spilled
  them over the hero content. `05·files` not `05·what it writes`. Two short rows do fit inside the
  54px; long labels do not. Check the topbar in the hero screenshot, not just the figures.
- **SVG callout lines must END INSIDE the zone they label, not at its boundary.** A leader line
  terminating on the border between two zones reads as pointing at whichever zone has content
  nearest the endpoint (a sidebar callout that stopped at the sidebar/editor boundary read as
  labeling the editor's code). Land the endpoint several px inside the target region.
- **De-escalate before you teach (frustrated-learner pages).** When the ask itself says "I feel
  like I'm missing something / it's really easier than I think," open the hero by naming and
  defusing that feeling ("you are not missing something; you are used to the factory") and defuse
  each gripe explicitly where it's taught (the command palette is a search box, not a memory test).
  Emotional acknowledgment first buys the attention the mechanics need.
- **STANDING RULE: every standalone learning page needs a back-to-dashboard link (added 2026-06-30 after
  the maintainer: "these pages launch with no way back").** Put a `.backdash` pill as the FIRST child of the topbar
  `.wrap` (before `.brand`): a left-chevron + the **career-dashboard staircase mark** (the same teal/amber/
  orange bars as the favicon, as inline SVG) + "Dashboard". Class defs are in `assets/teaching-kit.css`.
  ⚠️ **PATH IS PER-FILE BY DEPTH**, because `type:"html"` guides are linked IN PLACE at their source (not
  copied to `guides/`): a page one folder under root (e.g. `AI-Native Target Roles/`) uses
  `href="../CareerDashboard.html"`; a root-level page uses `href="CareerDashboard.html"`. Compute it as
  `"../" * depth + "CareerDashboard.html"`. Do NOT add this to a public PRODUCT page (e.g. the GitHub Pages
  portfolio), only to dashboard-library study pages.

### Rules added 2026-07-06 (Learning_RAG §03: the target reader stalled live, mid-read)
The page's own target reader stopped reading and rejected the translation section: it used `float[384]`,
"nearest-neighbor", "ANN index", and an invented `Similarity()` SQL function before defining any of them,
and the isolated-persona QA pass had missed all four. Permanent rules:
- **Define-on-first-use is a HARD ordering constraint across the WHOLE page, not a per-section virtue.**
  A term defined in section 05 is undefined in section 03. Before shipping, walk the page in reading
  order and check every term of art against the earliest place it appears, including diagram labels,
  hero copy, and code comments, which the reader hits first. If a later section owns the deep dive, the
  first appearance still gets a one-clause gloss ("to *embed* a text is to compute its *vector*, a
  fixed-length list of numbers encoding its meaning; section 03 makes this precise").
- **Every literal number must carry its origin at first use.** A bare "384" (or 512, or 0.7) reads as
  arbitrary and destroys trust ("is there a reason it's not 324?"). State what fixes the number (the
  model's architecture: MiniLM works 384 wide per layer, 12 parallel attention blocks of 32; and get
  this FACT-CHECKED, the first draft of this very rule said "6 × 64" and was wrong), whether the
  reader can change it (only
  by swapping models, then re-embedding everything), and give it an analogy class (a hash width:
  SHA-256 always emits 256 bits regardless of input). Also mark example values AS examples ("k = 5 is
  this page's example; k is a knob, not a law") and name the corpus behind any scale claim ("fine at
  the lab's ~40-file corpus"), or the number reads as smuggled in.
- **Label pseudo-code as PSEUDO in the artifact: before the panel, in the panel label, and in a code
  comment.** An invented function in the reader's HOME language is a trap for exactly the expert the
  translation section targets: a T-SQL veteran will try to place `Similarity()` among the real functions
  he knows and conclude he's ignorant or the page is lying. Say it's invented, say why (to show the
  shape), and name the real construct it stands for (`VECTOR_DISTANCE` in SQL Server 2025).
- **QA a translation section with a KNOWN-side expert persona.** The standard noob/basics/expert pass
  missed all of the above because no persona was expert in the reader's home stack; only a SQL Server
  veteran instantly catches a fake T-SQL function or a wrong "computed column" analogy. When a page
  teaches B via known-A, one isolated reviewer must be an A-expert with ZERO B knowledge, reading in
  order, instructed to flag (1) any term used before defined, (2) any number without an origin, (3) any
  construct in language A they cannot place that isn't labeled invented.
- **Don't switch metaphors without a bridge.** If a vector was introduced as a POINT on a scatter plot,
  "vectors pointing the same direction" is a stall. Bridge in place: "a vector is both a point AND the
  arrow from zero out to that point; cosine compares the arrows' directions."

### Rules added 2026-07-07 (Learning_Docker post-patch rot: compliant on every rule, worse to read)
A fix pass applied 8 first-use glosses + purged 49 em-dashes, verified each finding applied and the
grep clean, and shipped a page the reader called the worst in the library. Every individual rule was
satisfied; the READING EXPERIENCE was never re-checked. Permanent rules:
- **Weave glosses, don't bolt them.** A first-use definition must be a teaching sentence (or a
  reorder so the definition precedes the use), never a parenthetical rammed into an existing
  sentence. One parenthetical max per sentence; if a sentence needs two glosses, split or
  restructure it. Tell: a sentence where the reader parses two nested asides before reaching the verb.
- **Never bulk-substitute punctuation.** An em-dash purge (or any mechanical text rewrite) must
  rewrite each SENTENCE, not swap the character; wholesale dash→colon produces colon soup. Tell:
  two or more colons in one sentence. Re-read every touched sentence aloud-in-your-head.
- **A patch pass ends with a whole-page re-read, not a checklist.** N locally-correct fixes can sum
  to a worse page. After applying findings, run a fresh READER-TWIN over the WHOLE artifact, and the
  delivery gate applies retroactively to any page a fix pass touched.
- **Code comments are not footnote space.** A comment longer than ~8 words belongs in a bullet
  below the block; long comments force horizontal scroll and bury the code's shape.
- **Worked trace is required for hands-on TOOL pages, not only pipeline lessons.** A build/run tool
  (Docker, git, a CLI) needs one real command sequence end to end with illustrative-watermarked
  terminal output, including the payoff moment (the cache hit, the failure twin). Descriptions of
  commands followed by interview Q&A teach recitation, not the tool.

### Rules added 2026-07-10 (Learning_CodebaseRAG, a defend-cold build log of the maintainer's OWN measured project)
A project build-log page (a diary of real changes + measured results, not a concept primer) has failure
modes a concept page does not. An armed nemesis caught three claims that would each have detonated on the
first interview follow-up; all three passed the reader-twin, which checks clarity, not truth. Permanent rules:
- **Verify every measured number against the repo's own source-of-truth, not the conversation.** On a page
  that reports the maintainer's own results, a figure written from memory or a session summary is a
  provenance trap: a fabricated "5 of 18 answers lost" contradicted his own `DECISIONS.md` ("7 of 18"), the
  exact number an interviewer who skims the public repo catches. ARM the nemesis panel with the ground-truth
  files (the decisions log, the results JSON, the actual handler) and instruct it to diff every quantitative
  claim against them. A number that disagrees with the maintainer's own repo is worse than an unmotivated
  one (the 2026-07-06 origin rule): it reads as a bluff, which is his #1 high-stakes hazard.
- **When a build-log narrates several sequential changes, check whether a later one NULLIFIES an earlier
  one, and make the page own the interaction.** Two individually-good changes shown as two clean wins is a
  trap: here, raising the refusal floor (change 1) was silently retired by the embedding swap (change 2),
  which lifted every score above the floor so it now catches zero of the fakes it was tuned to catch. The
  nemesis asks "didn't your second change undo your first?", and the honest answer ("yes, and that is why
  refusal now rests on the other layer") is MORE sophisticated than either win alone. Trace change-order
  effects explicitly.
- **Scope every absolute privacy/security negative to the exact stage; they are almost always false at some
  boundary.** "No code leaves the machine" was true for ingest/embed/retrieve but false at answer time (the
  retrieved passages go to the cloud model). Rewrite absolute negatives ("never", "fully offline", "nothing
  leaves") as stage-scoped claims. And when the maintainer's OWN public repo makes the same loose claim
  (this one did, in README + DECISIONS), FLAG it to him as a public-repo accuracy bug; do not silently copy
  it onto the study page. External-boundary claims are his hard-stop territory.
- **Both SVG failure modes from the workflow step-4 list bit again on the first render**, confirming the
  serve+screenshot gate is non-optional: a long ceiling label ran off the `viewBox` right edge, and the
  angle-labels plus their arc collided into garbled text at a shared origin. Both looked fine in source. Fixes
  were to left-anchor / shorten the overflowing label, and to delete the redundant label and spread the rest
  into the empty wedges around the origin. (Windows note: `Start-Process python -m http.server` with a
  spaces-path `--directory` arg silently exits; pass `-WorkingDirectory` instead.)

### Rules added 2026-07-11 (Learning_RAG v5: flight-plan-to-diary refresh + the interactive vector globe)
A page written as a mission FLIGHT PLAN got refreshed into a DIARY after the mission actually ran, then a
library-free interactive 3-D widget was added. New rules, all field-proven this run:
- **Refresh to a diary, but never fabricate the diary.** Flip "you will" to past tense ONLY for events the
  record supports. A prediction with no receipt ("you will hit this chunking hazard") becomes a present-tense
  hazard note, not a fake memory; converting it to "you hit this" invents an observation, the exact
  provenance trap the maintainer got burned by.
- **Arm the nemesis with the per-item RESULT files, not just the decision log.** This run's two best catches
  lived in per-question eval JSON that no prose summary mentioned: a guardrail whose measured score at the
  shipped config was 0-of-4 while the page said "refusals measured ✓", and two interventions that both hit
  the same 61% headline while sharing only 7 of their 11 item-level hits. Two rules fall out: when two
  aggregate numbers "match," diff the per-item records before the page says "confirmed"; and when a page
  says "measured," make it state the number, especially when the number is 0. The honest, caveated version
  of both reads MORE senior than the clean version, not less.
- **Reviewers race your fixes.** Agents dispatched before or during a fix batch report findings against the
  file as it was when they read it; three of four reviewers this run flagged at least one already-fixed
  item. Triage every finding against the CURRENT file before re-fixing, or you will churn.
- **An interactive canvas widget fits the offline-first constraints.** ~150 lines of hand-rolled vanilla-JS
  3-D on a `<canvas>` (rotation matrix, orthographic projection with mild perspective, painter-sort) runs
  inline with no libraries and works from `file://`. Design lessons: (a) find the picture where an invariant
  becomes physical: length-1 normalized vectors mean every chunk lives ON one unit sphere, so meaning IS
  direction and cosine IS closeness on the globe (analogy: cities on a globe, angle from the core = near);
  (b) place stand-in points at REAL angles matching the page's quoted scores so the rendered geometry is
  honest, and watermark where the scores came from; (c) give every point a fixed per-label dy offset:
  an interactive view collides at SOME rotation, and the INITIAL frame is the one to screenshot-verify
  (it is also all a prefers-reduced-motion user ever sees, so gate auto-rotate on that media query);
  (d) auto-rotate until first pointerdown, wheel-zoom clamped with preventDefault only over the canvas.
- **Verify an interactive beyond a screenshot.** A static shot proves one frame. Also: wrap init in
  try/catch setting `window.__ok` / `window.__err` and read them via browser evaluate; dispatch synthetic
  PointerEvents to exercise drag and click; count non-transparent pixels via `getImageData` to prove the
  canvas painted; and check one interaction's readout against the math (a clicked cos 0.45 must report
  acos = 63 degrees). All four caught nothing this run only because they existed.
- **An un-numbered "Interlude ·" card beats inserting a numbered section.** A new mid-page teaching block
  as a `.teach` card inside an existing section avoids renumbering nav codes AND every "section NN"
  cross-reference in prose, which is where renumbering errors breed.

### Rules added 2026-07-12 (the codebase-rag public Pages tour: a product page that cites its own repo as receipts)
A public repo-tour page (portfolio angle, hiring-manager reader, served by GitHub Pages from the repo
root) shipped after a three-lens panel (reader-twin + IR-domain skeptic + armed nemesis). New rules:
- **"Committed in this repository" is a claim to verify with `git ls-files`, never the local disk.**
  The page's whole thesis was receipts; the receipts (eval result JSONs) were GITIGNORED: present
  locally, absent from the public repo. The reader-twin and domain skeptic both sailed past it (they
  read the artifact); only the nemesis, told to follow the page's own directions to the evidence,
  checked what was tracked. Prefer fixing by COMMITTING the receipts (rescope the ignore) over
  softening the claim; committing preserves the page's thesis.
- **The project's own ground-truth docs are reviewable claims, not ground truth.** A number copied
  faithfully from the decision log ("7 of 18") was refuted by the rawest committed record (per-item
  eval JSON computes 6). Layering: raw result records > summary/decision docs > prose. Instruct the
  nemesis to RECOMPUTE load-bearing numbers from the raw layer, not cross-reference the summary; a
  page can be 100% faithful to a wrong source. When layers disagree, correct the artifact AND the
  mid-layer doc in the same change, and hunt the wrong number in SIBLING artifacts (it had already
  propagated to two learner pages).
- **When a viz composites disparate measurements onto one shared axis, the caption must split real
  from staged.** Plotting five different questions' top-chunk cosines against a single "reference
  question" axis reads as real geometry; the honest caption is "real measured cosines, staged
  layout," naming the arbitrary dimension (azimuth, chosen for label spacing). Interactive readouts
  must not re-state the fiction ("from its question," not "from the question"). Numbers-true and
  framing-true are separate checks: the domain skeptic verified every cosine CORRECT while the
  nemesis correctly attacked the same figure's geometry claim.
- **Real clustered data breaks canvas labels; split label from readout.** Honest scores all landed
  within ~52° of the pole, and long labels collided at the initial frame. Fix: short on-canvas
  labels ("hit · 0.85") + the full name in the click readout. Related layout traps, both bit this
  run: 9+ navcodes escape a FIXED-height 54px topbar (use min-height + vertical padding so the
  second row stays inside the bar), and under ~720px wide the page needs a media block (nav as a
  single scrollable row, wide tables display:block overflow-x) or mobile gets a 300px sticky bar
  plus horizontal body scroll.
- **Don't self-label honesty.** The reader-twin counted "honest" as self-description 8+ times;
  repeated trust-narration reads as the exact tell it tries to prevent. Disclose the ugly number
  plainly where it matters and let the receipts do the trust work. Same family: never narrate the
  epistemic strategy ("this is stated deliberately because...") - just state the fact.
- **Product-page voice, confirmed again:** no interview/defend framing on a public product page even
  when its content was born from interview-prep material (the commissioner said so explicitly);
  repo-tour voice, decision-fork cards instead of Q&A drills, and glosses still at FIRST use in
  reading order including hero chips and stat-tile cells (MCP, MRR, and the target repo's name were
  the misses this run).
- Tooling note: the Playwright MCP screenshot tool writes only inside the served repo's
  `.playwright-mcp/` (its allowed root); save shots there by absolute path, and DELETE the folder
  plus any stray QA files before committing - the nemesis flagged the debris as a publish tripwire
  one `git add .` away from shipping.

### Rules added 2026-07-13 (Learning_PlantFloor: a PRE-BUILD primer for a phased, two-lane architecture)
A learner page teaching a system that will be BUILT IN PHASES (phase 1: a bridge process relays device
data into the pipeline; phase 2: the device speaks the protocol itself) went through the standard
three-lens gate. New rules, all field-proven this run:
- **Gate every mechanism claim to the PHASE where it actually holds.** The page narrated MQTT's last-will
  offline detection as a generic "the device vanishes" story; in the phase-1 architecture the BRIDGE, not
  the device, holds the broker connection, so a device drop fires no last-will at all: the mechanism is
  only true in phase 2. Both sympathetic lenses verified the mechanism as CORRECT in isolation and sailed
  past; only the nemesis asked "whose connection is it in phase 1?" On any staged architecture, test each
  taught mechanism against the stage that owns the connection/resource, tag the claim with its phase in
  the artifact, and add an explicit phase-1 caveat card. Then propagate the same gate into the project's
  plan doc: the ungated version was there too, and fixing only the page leaves the two documents
  reinforcing the same false floor.
- **Passing the page's own self-test does not clear the definitions gate.** The reader-twin answered all
  the closed-book self-tests cold yet stalled hard on three tool proper nouns used but never defined; the
  quiz only tests what it tests, and the untaught names were not in it. Treat the twin's STALL LIST as the
  definitions signal and the quiz score as the comprehension signal; they are different instruments.
- **Pre-build honesty needs a "planned" watermark on size estimates too.** "~100 lines" and "ours" for
  code that does not exist yet read as measured and owned; write "planned: ~100 lines." Cousin of the
  numbers-origin rule: a line count for unwritten code is invented precision.
- **A named-sibling disambiguation is worth one parenthetical, not a paragraph.** When a taught feature
  collides with a formally-named sibling the reader may meet later (classic subscriptions vs a spec part
  literally named "PubSub"), one clause that names it and says "not what this project uses" arms the
  reader; anything longer reads as a footnote-tangent and the twin flags it as pure processing cost.

### Rules added 2026-07-14 (a company interview-prep page: source tiers, retract-in-place, and the flattening trap)
A prep page for a real upcoming conversation went through the full three-lens gate and produced rules that apply to
ANY page whose content is researched rather than invented. All four are field-proven this run:
- **RANK YOUR SOURCES BEFORE THEY SET THE PAGE'S PLAN, AND ESPECIALLY BEFORE THEY SET ITS TONE.** The tiers, worst
  to best: (4) SEO-generated "guide" sites are machine-written, cite nothing, hedge every sentence, and get REFUTED
  under verification; never build on one. (3) Public review/forum aggregates are WEAK: their per-company summary
  statistics are pooled across every role at the company, so a "difficulty 2 out of 5" can be computed from a sample
  containing zero people in the reader's actual field. (2) A message from the person actually running the process is
  PRIMARY: read it like a spec. (1) The organization's own structured record (its ATS/API/config, whatever the
  machine-readable source of truth is) is TRUSTED, because it IS the record rather than a memory of it.
  Field case: a page confidently told its reader the upcoming conversation would be "conversational, difficulty 2 of
  5, coding is light." Adversarial verification killed fourteen of fourteen such claims (they traced to tiers 3 and
  4), and the tier-2 source then stated in writing that it was a rigorous technical assessment. **A page that
  soothes a reader into under-preparing is worse than no page.** When the format is ambiguous, teach to the HARDER
  reading; over-preparation costs an evening, under-preparation costs the thing itself.
- **RETRACT IN PLACE; never quietly rewrite.** If a page has to reverse a claim, assume the reader already read the
  old version. Say what the page previously told them, say it was wrong, name the source that failed, and say what
  replaced it. A silent edit leaves the reader carrying the old belief with no idea it was withdrawn.
- **When the page describes the reader's OWN measured work, diff it against the raw records before they study from
  it.** Not the summary, not the decision log, not your notes: the rawest committed artifact. A study page will
  cheerfully flatten a nuanced multi-step result ("measured a bad baseline, diagnosed it with a probe, predicted a
  ceiling, hit it") into a single-cause slogan ("improved X from 11% to 61%"), and then hand the reader a number they
  cannot reconcile under one follow-up question. **The page can end up LESS honest than the repo it describes**, and
  the reader-twin is structurally blind to it (it checks clarity, not truth). See `nemesis-review`.
- **Teaching a mechanism BACKWARDS is the failure a sympathetic reviewer cannot catch.** A page taught an idempotency
  key as "do the work, then record the key, then respond," which leaves open the exact crash window it had just
  warned about; the correct mechanism claims the key FIRST, atomically, before doing the work. The reader-twin
  paraphrased the wrong version back confidently and scored itself SOLID. Only an armed domain skeptic and the
  nemesis caught it. **For any mechanism with a failure mode, make one reviewer prove the mechanism actually closes
  the hole it claims to close**, rather than checking that the explanation is clear.

### Component added 2026-07-07 (SCROLLSPY: active-section highlight in the jump bar)
**STANDING RULE: every page with a `.navcodes` topbar gets the scrollspy.** As the reader scrolls, the
jump link for the section they're reading glows (orange `--signal`), so the bar doubles as a "you are here"
indicator, not just a jump menu. The maintainer asked for this across the whole library (2026-07-07) and
loves the jump bar; this makes it self-locating. Two pieces, both offline, no libs, degrade gracefully.

CSS (add near the `.navcodes` rules; uses literal orange so it works even if a page is missing a token):
```css
.navcodes a{transition:color .18s ease, background .18s ease, border-color .18s ease, box-shadow .18s ease, text-shadow .18s ease;}
.navcodes a.active{color:var(--signal); border-color:var(--signal); background:rgba(255,138,61,.12); box-shadow:0 0 12px -3px rgba(255,138,61,.6); text-shadow:0 0 9px rgba(255,138,61,.45);}
```
JS (paste once before `</body>`). **Use the trigger-line algorithm, NOT an IntersectionObserver top-band.**
A top-band IO (`rootMargin:'0 0 -75% 0'`) picks the TOPMOST intersecting section, so a trailing section's
tail still in the band wins and the highlight lags one section behind (verified failure 2026-07-07: scrolled
to §04, highlighted §03). The correct semantic is "active = the last section whose top has crossed a line
just below the sticky bar", which is unambiguous:
```html
<script>/* scrollspy (nav active-section highlight): lights the current section's jump link as you scroll */
(function(){
  var links=[].slice.call(document.querySelectorAll('.navcodes a[href^="#"]'));
  if(!links.length)return;
  var byId={},sections=[];
  links.forEach(function(a){var id=a.getAttribute('href').slice(1),el=document.getElementById(id);if(el){byId[id]=a;sections.push(el);}});
  if(!sections.length)return;
  var TRIG=130,ticking=false;
  function update(){
    ticking=false;
    var current=null;
    for(var i=0;i<sections.length;i++){ if(sections[i].getBoundingClientRect().top<=TRIG){current=sections[i].id;} else {break;} }
    links.forEach(function(a){a.classList.toggle('active', !!current && a===byId[current]);});
  }
  function onScroll(){ if(!ticking){ticking=true;requestAnimationFrame(update);} }
  window.addEventListener('scroll',onScroll,{passive:true});
  window.addEventListener('resize',onScroll,{passive:true});
  update();
})();
</script>
```
Notes: the `break` relies on sections being in document order (they are, links mirror section order); `TRIG=130`
clears the 54px sticky bar with headroom; retain-nothing-when-above-first leaves the bar unlit over the hero
(correct, you're not in a numbered section yet). To retrofit the whole library at once, an idempotent injector
(insert CSS before the first `</style>`, JS before the last `</body>`, guarded by a marker string) beats
hand-editing every file; skip the public GitHub-Pages portfolio (separate repo, not a learner). VERIFY it live
(`py -m http.server` + scroll): confirm the right link lights AND that it changes on scroll, the bug is invisible
in source.

## Inline-SVG diagrams: the highest-value move

Diagrams are where these pages beat plain notes. Read `references/svg-diagrams.md` for the full
patterns and copy-paste skeletons (staged pipeline, nested/progressive-disclosure, container/box
model, comparison columns, labeled cylinder for a datastore, arrow markers). Rules of thumb:

- `viewBox="0 0 W H"`, no fixed width/height → it scales responsively inside `.fig`.
- Label everything in IBM Plex Mono ~12 to 14px. Use `<tspan>`/multiple `<text>` for line breaks
  (SVG text does not wrap).
- Use the theme hexes directly. Highlight the ONE thing that matters in `--signal` orange.
- Add `role="img"` + a thorough `aria-label` describing the diagram in words (accessibility +
  it's the figure's spec if you regenerate it).
- Keep it legible, not ornate. A clear three-box flow beats a busy schematic.

## Icons

Use small inline lucide-style stroke SVGs (`stroke="currentColor"`, width ~18 to 19px) in section
kickers so each section reads at a glance. `references/svg-diagrams.md` lists the common paths
(layers, package/box, database/cylinder, sparkles, graduation-cap). Color follows the section accent
via `currentColor`.

## Course / resource scaffolding

When the maintainer is going to take a course (e.g. the Anthropic Academy), add a `.courses` grid of
`.course` cards that link to the REAL course URL and state in the `.cmeta` which capability/module
each one unlocks, wiring study to outcome. Verify URLs are current via the web; don't trust an
aggregator blog. Anthropic Academy lives at `anthropic.com/learn`; individual courses at
`anthropic.skilljar.com/<slug>`; runnable repos at `github.com/anthropics/{courses,
prompt-eng-interactive-tutorial, claude-cookbooks}`; docs at `docs.claude.com`; MCP spec at
`modelcontextprotocol.io`.

## Workflow: building or enhancing a page

1. **Know the subject cold first.** If you can't teach it, you can't write it. Web-search to fill
   genuine gaps before drafting (the maintainer expects the content to be *correct*, not vibes).
2. **Draft into the identity.** New page: start from an existing page's `<head>` (tokens + grid
   texture + kit). Enhancement: insert `.teach` sections at the natural place in the flow.
3. **Diagram the structural ideas.** Don't narrate what a picture should show.
4. **Verify visually: always.** Serve the folder (`py -m http.server <port> --bind 127.0.0.1`;
   Playwright blocks `file://`), navigate to the section anchors, screenshot each new diagram, and
   actually look. SVG coordinate bugs are invisible in source and obvious in a screenshot. Fix and
   re-shoot until clean. Element-screenshot each figure directly (`.fig >> nth=N`), much faster than
   scrolling. The two failures that bite every time and look fine in source: (1) a long `<text>`
   with no `text-anchor="middle"` runs off the right edge of the `viewBox`; (2) two labels whose
   coordinates put them on top of each other. Both only show up in the rendered image.
   On a LONG page (the roadmap, dashboard) a `fullPage` screenshot is too small to read; take
   **viewport** shots scrolled to each diagram. `#anchor` + `scroll-behavior:smooth` does not settle
   before the shot (reading `window.scrollY` right after returns 0), so jump explicitly:
   `browser_evaluate(() => { const y = document.getElementById('ID').getBoundingClientRect().top +
   window.pageYOffset; window.scrollTo({top:y+480, behavior:'instant'}); })`, then screenshot, then
   `scrollBy({top:760, behavior:'instant'})` between figures.
5. **QA gate BEFORE handoff (mandatory since 2026-07-06).** The maintainer reading a page is
   PRODUCTION, never staging: he must never meet a defect a simulated reader could have caught.
   Before announcing any new or substantially revised page as ready, run at least one isolated
   READER-TWIN cold read (derived from the `iterative-lesson-refinement` skill's
   `references/reader-profile.md`) and fix what it finds. A page that skips this gate is not done,
   regardless of how clean it reads to its author. (Origin: the 2026-07-06 RAG §03 stall, where
   the maintainer lost a study session to defects three generic QA passes had blessed.)
   **For an interview-prep / "defend-cold" page, the reader-twin is NOT sufficient on its own:**
   it is sympathetic and catches confusion, not confident-but-wrong claims or unarmed follow-ups.
   Also run a `nemesis-review` adversarial panel (nemesis armed with the audience's expertise, an
   interviewer-follow-up skeptic, and for technical pages a domain-accuracy skeptic), and fix what
   survives verification. (Origin: 2026-07-07, a Docker page that passed the reader-twin 9/10 still
   had three answers that each detonated on the first interview follow-up.)
   **Run every review the page needs in ONE up-front batch, before the maintainer sees it, never
   reactively after he catches a gap.** Reader-twin and the nemesis panel dispatch in parallel; the
   maintainer being the trigger for a QA instrument is the gate running too late. Serial ship-then-
   patch is the single most token-and-trust-expensive mistake in this workflow.
   **Grounding overclaim is the #1 recurring defect in interview-prep pages, and the reader-twin is
   BLIND to it (it checks clarity, not honesty). Hunt it explicitly.** The tell is second-person
   "your pitch / you run X daily / this is your governance story" framing that quietly converts a
   read-about feature into the reader's own claim, on a page that carries his name. Any HAVE claim
   must be something he can defend cold; a capability he has only read about must read as "build
   toward," never as owned. (Field case 2026-07-07: an armed nemesis found this exact overclaim on
   4 of 7 teaching pages, the same pattern that cost the maintainer a real final-round interview.
   The three pages that stayed honest all framed the tool neutrally and led any gap with the GAP.)
   **Invoke the `nemesis-review` skill to run the panel; never hand-roll its charter from memory,
   even if you used it earlier the same session** (reproducing it from memory silently drops its
   pairing and cross-check rules; see that skill's Common Mistakes).
6. **Register it so it's never orphaned.** Any NEW study/reference HTML gets a row in the `GUIDES`
   registry near the top of `dashboard.py` (cat / type / badge / title / desc / src), then re-run
   `py dashboard.py`. The dashboard is the one place all guides live.
7. **Bump the version footer** (the `.meta-line`) with a dated one-liner of what changed, so the
   page advertises its own freshness.
8. **Grep for em-dashes and purge them** before declaring done: search the `.html` for the "—"
   character and replace every hit with a comma/colon/period/paren (see the no-em-dash constraint above).
   This is the cheap mechanical check that catches the default-em-dash regression.
9. **Clean up** the `*-check.jpeg`/`qa-*.jpeg` screenshots and `.playwright-mcp/` when done (housekeeping junk).

## Favicon / browser-tab identity

Every page in the library shares one favicon: the **rising teal→amber→orange staircase** (the
L1→L2→L3 thesis mark). It lives as `favicon.svg` in the workspace root and as a base64 data-URI
`<link rel="icon" type="image/svg+xml" …>` (offline-safe, path-independent; survives the `guides/`
wipe). New standalone pages should paste that same `<link>` into their `<head>`; the dashboard injects
it via a `FAVICON` constant in `dashboard.py`. Don't invent a new mark per page; maintain one identity. See the
[[dashboard-favicon]] memory for the exact data URI and how to regenerate it if the art changes.

## Worked examples

Two canonical references for "what good looks like": study one before building a new page:
- `AI-Native Target Roles/AI-Native_Roadmap.html` (v11+): a capability **scorecard**: "Start here"
  orientation with the L1→L2→L3 thesis staircase, an Anthropic course track wired to modules, and a
  "Today's Focus" deep-dive teaching Claude Skills / Docker / RAG.
- `AI-Native Target Roles/Orchestration_Handbook.html` (v1+): a long-form **lesson** that flows
  basics → orchestration → future: the "console" stack diagram, the toolkit knob-by-knob, a multi-agent
  workflow diagram, MCP-vs-A2A, and a self-healing loop. Good model for a single consolidated teach-through.
Both use: plain-English claim → `.analogy` → inline-SVG diagram → `.qa` defend-it blocks → honest tie to
real repos. That sequence is the skill in one line.
