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
- **⚠️ KNOWLEDGE FRAMING DEFAULTS DOWN, and it leaks through ANALOGIES.** When you describe what the
  maintainer already knows, the safe default is "might know a little of this, better review" or "did
  this a long time ago, definitely review." Never "this is your wheelhouse" unless a baseline file or
  a repo literally supports it. **The specific tell to grep your own drafts for: an analogy that
  morphs into an experience claim.** "Same shape as the X you built" is fine and useful. "…which is
  20 years of your life" is a fabricated competence claim wearing a rhetorical flourish, and it is
  the exact seam where inflation hides, because the surrounding paragraph is usually honest.
  This rule covers the CHAT PROSE around a page, not only the page: the artifact can be clean while
  the conversation delivering it inflates him. (Learned 2026-08-01, four days before a hiring-manager
  interview: "MCP servers run in containers behind a gateway, which is 20 years of your life." True
  for the *service* patterns he owns, false for containers, which he first touched that same year on
  two local projects and has never deployed. He caught it himself and asked for the rule. His
  articulation is worth keeping: *"The better I know stuff, the easier it is to explain it to experts
  who can tell if I'm bullshitting."* Logged as EP-047 in the assumption-debt log.)
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
  (`?v=N`) and glance for one of your new strings in the shot before trusting it. Sibling gotcha
  (2026-07-15): on a page with `scroll-behavior:smooth`, `scrollIntoView()` + an immediate screenshot
  captures MID-ANIMATION (the shot shows the wrong section while your evaluate call returns the right
  element). Scroll with `behavior:'instant'` (`window.scrollTo({top: el.getBoundingClientRect().top +
  window.scrollY - navOffset, behavior:'instant'})`) before shooting. Also: the Playwright MCP blocks
  `file://` URLs, so a local page must be served over http (`py -m http.server`) to verify at all.

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

### Rules added 2026-07-20 (a 50-question interview Q&A study page, an 18-subagent single-page build)
- **Scale rule for a many-card page: cap diagram proposals up front.** When drafting a large multi-section page with one subagent per section, tell each to propose a diagram ONLY for its anchor / highest-value item, not every item. A 50-card build had the drafters propose 40 diagrams; 12 were used and 28 stripped, a wasted pass. Diagrams are the highest-value move, but one per section is the practical ceiling for a Q&A-style page.
- **Delegate the mechanical bulk; keep verification and the final edits.** For a big teaching page, delegate to subagents: per-section answer drafting (web-verified, written to files), HTML assembly (draft files to cards, editing the page in place), SVG generation, and fix application, so the 50-card bulk and the raw drafts never enter the orchestrator's context. The orchestrator keeps the scaffold, the diagram VISUAL verification, the QA synthesis, and the final surgical edits. Proven on an 18-subagent, roughly 3M-token single-page build.
- **A dedicated Q&A card component.** A many-question page wants a `.qacard` (question, one-line claim, answer) with a distinct `.fu` follow-up inset (an amber "defend-it" block) as the structural heart, plus per-theme accent variants so sections stay visually distinct across 50 cards.
- **Cheap deterministic diagram gate (complements the screenshot pass).** One browser_evaluate over every `.fig svg` that estimates each `<text>` element's right edge (x plus length times a per-anchor factor) against the viewBox width flags the number-one failure (text running past the edge) across all figures in a single call. Use it as a fast pre-filter; still do the visual pass for label collisions, which this does not catch.
- **At scale, the whole-page re-read finding is CROSS-CARD inconsistency, not just within-card roughness.** The post-patch reader-twin caught a card whose opening sentence contradicted the NEXT card and its own diagram (latency: it listed queue and time-to-first-token as peer clocks while the diagram and the next card folded queue INTO time-to-first-token). Additive glosses also bolt awkwardly (a definition nested inside another definition reads three times before the verb). Reconfirms the patch-pass-ends-with-a-whole-page-reader-twin rule, and adds: at scale, hunt contradictions BETWEEN adjacent cards and between a card and its own figure, not only sentence-level clumsiness.

### Rules added 2026-07-22 (Learning_ClaudeHarness: a fast-moving-tooling primer)
- **Context-constrained build chain.** When the orchestrator's own context is degraded, build the page via
  subagents instead of drafting inline: research-to-disk (facts written to a file) -> plan-to-disk (structure
  written to a file) -> an author subagent that reads those two files and writes the HTML -> the standard
  QA-gate subagents (reader-twin + technical-accuracy skeptic) -> a fix subagent that applies findings, so the
  page content itself never has to enter the orchestrator's context. Note: read-only agents such as
  `claude-code-guide` cannot Write the research file (they carry no Write/Bash tool); use a `general-purpose`
  agent for any step that must persist a file to disk.
- **Fast-moving tooling goes stale even in a fresh research pass.** For a page about rapidly-changing tooling,
  the technical-accuracy skeptic MUST verify against LIVE primary docs (WebFetch), not just re-check the
  research file, because the research itself can already be months stale. Field case: a harness page claimed a
  LiteLLM proxy was REQUIRED to run a local model; the doc-verifying skeptic found that Ollama, llama.cpp, and
  vLLM had shipped native Anthropic-Messages-API endpoints roughly six months earlier, making the proxy
  optional, not required. The reader-twin (a clarity lens, not a currency lens) was blind to the staleness;
  only the live-doc skeptic caught it. On any page about tooling that changes fast, treat "verified against the
  research file" and "verified against the live docs today" as two different, both-required checks.

### Rules added 2026-07-31 (a two-protocol page where a spec revision landed 2 days before the build)

A page teaching two fast-moving open protocols, gated by a nemesis + live-doc accuracy skeptic +
reader-twin panel, then re-gated by a SECOND fresh reader-twin after the fixes. Four durable rules:

- **The most likely place for a confident-but-wrong claim is the MOTIVATING claim, not the factual
  ones.** The accuracy skeptic verified 58 factual claims (0 wrong). The nemesis found the blocker
  in the page's own "and here is WHY this matters" paragraph, which overstated what the spec
  guaranteed. Facts get verified because they are checkable; motivation gets asserted because it
  feels like framing rather than a claim. **Point one reviewer explicitly at every "why this
  matters" and "the whole point is" sentence and make them check it against the source.**
- **The cheap deterministic diagram gate is blind to two whole classes of defect.** A
  browser-side pass over every `.fig svg` comparing each `<text>` bbox against the viewBox and
  against sibling text bboxes catches overflow and label collisions, and it is worth running. It
  CANNOT see (a) a leader line or curve passing THROUGH a box it does not belong to, or (b) a
  paint-order defect where a later element covers an earlier label (an animated pulse circle
  declared after its text will grow over that text). Both shipped past a clean gate and were
  obvious in the first screenshot. **The gate is a pre-filter; the visual look is still mandatory,
  and z-order is a thing to look for by eye specifically.**
- **⚠️ THIRD BLIND SPOT, AND IT IS THE COMMON ONE: the gate compares text to the VIEWBOX, not to the
  BOX THE TEXT SITS IN.** A flow diagram of labelled boxes passed a clean overflow-and-collision
  check while one box's subtitle visibly spilled past both of its borders into the arrows on either
  side. Nothing overflowed the viewBox, and no two labels overlapped each other, so the gate had
  nothing to say. The fix is one more comparison, and it is cheap: for each `<text>`, find the
  `<rect>` whose area contains the text's centre, then assert the text's bbox sits inside that rect
  with a small margin. In practice a fixed-width box has a character budget (roughly
  `width / 6.6` at 11px monospace), so the durable version is an ASSERT IN THE GENERATOR on label
  length, not only a check on the render: `assert all(len(s) <= 15 for s in subtitles)` fails at
  build time, before a screenshot is even taken. Same lesson as the other two blind spots: the
  deterministic gate is a pre-filter, the eye is the gate, and every defect the eye catches should
  become a new deterministic check so it is caught for free next time.
- **New post-patch failure signature: prose that pre-emptively defends its own additions.** When a
  fix batch adds explanation, the additions tend to arrive wearing an apology: "You may never have
  used any of these, so briefly...", "Three more are worth naming so they do not read as noise."
  The reader-twin flagged both as a tell that made it start reading those paragraphs as padding.
  Related and worse: **a section that announces its own apparent contradiction and then resolves
  it** ("these two facts need reconciling, because at first glance they disagree"). That is the
  page arguing with itself in front of the reader. **Say the distinction once, cleanly, the first
  time.** If a correction genuinely needs to be set apart from the confident claim it qualifies,
  give it its OWN accent panel with its own kicker rather than burying it mid-flow; the same page
  did this well in one section and badly in another, and the twin named the difference unprompted.
- **Retract-in-place scales better than a sweep on a page you did not author.** A sibling page was
  found to teach a superseded naming convention in roughly 50 places, all individually harmless.
  Rewriting 50 strings in someone else's page is 50 chances to introduce a NEW error for zero new
  understanding. **A dated correction banner at the top, giving the old-to-new mapping and pointing
  at the current page, is the better trade.** Reserve in-place edits for claims that are outright
  WRONG (that sweep also turned up a governance claim that contradicted its own page two lines
  later, which absolutely did need fixing in place).

### Rules added 2026-08-07 (a coding/DS&A interview-prep page: a compile-and-run code gate, and reassurance as under-preparation)

A page teaching real code (worked snippets meant to run) went through a panel of a nemesis, a
dedicated code-accuracy skeptic, and two reader-twins, isolated. Two rules, both field-proven:

- **For a page teaching real CODE, the code-accuracy gate is COMPILE-AND-RUN every snippet in a
  real project, not a hand-trace.** It is cheap and definitive, and it finds input-edge bugs a
  hand-traced "edge-case list" misses. Field case: the code-accuracy skeptic built a small project
  and ran every snippet; the nemesis independently did the same AND ran 20,000 randomized trials
  against a brute-force oracle. Both caught an empty-input bug (a function returning a sentinel
  max-int on an empty array) that the page's OWN hand-written edge-case walkthrough had listed
  around without catching. Stage the walkthrough over the edges of EVERY input the code takes, not
  just the one the worked example varies (an empty SECOND array was the miss while the example
  only varied the first). This is the "build and measure the real thing" rule (see
  `nemesis-review`'s tenth success) applied to a teaching page's code: the snippet IS the artifact,
  run it.
- **Reassurance-into-under-preparation is the coding-prep analog of grounding-overclaim.** A prep
  page can blow smoke AT the reader, not just overclaim ABOUT him: an over-reassuring sentence (a
  stated failure floor, a difficulty statistic scoped to the wrong population, a "this is designed
  to be easy" framing built from one anecdote) licenses him to prepare less for the hardest gate.
  Both reader-twins were BLIND to this class entirely, they check clarity, not honesty of
  reassurance. Hunt it with a nemesis, and treat every reassuring sentence like a "why this
  matters" claim, checked against its source tier before it ships. Cross-reference the
  `avoid-sycophantic-blowback` discipline: a page that soothes the reader into under-preparing is
  worse than no page. Reconfirms the fix-pass-creates-defects rule above: the post-fix reader-twin
  still caught a residual term-before-definition and a gloss wedged mid-clause, so re-run a
  reader-twin over the whole artifact after any fix batch, even a small one.

### Rules added 2026-08-14 (a recruiter-syllabus prep page: the honesty table, and redundant SVG labels)

- **Verify the artifact's own honesty apparatus FIRST, not last.** A prep page carried an
  honest-claims table whose stated purpose was "every claim grounded to the record or marked GAP,"
  and the adversarial reviewer found the page's worst defect in its FIRST CELL: a
  years-of-experience figure larger than the number on the maintainer's own outbound record. The
  honesty table READS as the check, so every pass skips it as meta; it is actually the
  highest-risk surface on the page. Point the record-armed reviewer at the HAVE/GAP table before
  anything else, and treat the maintainer's outbound record (the resume the other party holds) as
  the CEILING for any number the page suggests saying aloud. Corollary: a computable sum sitting
  near a capped claim (four tenures that add past the cap, two screens from "say the smaller
  number") is the same defect family as a rounding-up phrase; reconcile it in place or remove the
  computable form.
- **The top SVG label-collision source is REDUNDANT label text: when an arrow's target is visible,
  drop the target's name from the label.** Two figures in one build shipped leader lines striking
  through their own labels ("waits for row 2" crossing the very line that points at row 2), a
  class the deterministic bbox gate cannot see. The durable fix was semantic, not geometric:
  shorten the label to its number and verb ("3. waits") and let the arrowhead carry the object.
  Shorter labels also survive re-layout, where a nudged long label finds a new line to collide with.
- **When two research inputs both claim the primary source and disagree on a number, check
  INTERNAL consistency before fetching anything**: in one run, a research report's own quarterly
  data table refuted its own headline growth percentage by simple arithmetic, settling the dispute
  before the tiebreaker fetch (which then confirmed it). And for figures the reader will recite to
  an insider, the organization's own published boilerplate outranks third-party encyclopedias even
  where they conflict; cite the source the room would check.

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

   ⚠️⚠️ **ACCURACY REVIEW IS NOT PEDAGOGY REVIEW, AND ONLY RUNNING THE FIRST IS THE #1 WAY THIS
   SKILL FAILS (2026-08-04, the worst delivery failure on record).** A page can be fully accurate,
   well-sourced, honestly caveated, self-tested, and still be UNLEARNABLE, because the failure lives
   in ORDER and REGISTER rather than content. The maintainer read exactly such a page the night
   before a decisive interview and stopped at section 3 of 11: *"LLM bullshit word salad... impossible
   to learn from... using terms before they're defined."* Every fact in it was true. **Before shipping
   any teaching page, run these four checks; all are countable, so none of them require judgment:**
   - **Motive-last.** Does any section list consequences and then reveal, at the bottom, the single
     idea that makes the list re-derivable? That section is upside down. Invert it: something breaks,
     why, the fix (which the reader should be able to GUESS by the time it arrives), what falls out.
     The target sensation is the heading "the fix, which you can now guess" being literally true.
   - **Self-tests that restate.** Grep each answer's content against the section body above it. An
     answer whose substance already appears verbatim above is a third paragraph wearing a quiz
     costume. A real answer adds an angle, a number, or a sharper framing.
   - **Term-before-definition.** Build the table: every load-bearing term, its first use, its
     definition. Any gap larger than zero sections is a defect, including inside SVG labels, code
     comments and captions. Watch for the same word carrying two meanings in one page (a gateway
     "front desk" and the context-window "desk" will collide).
   - **The antithesis couplet.** Count `is not X, it is Y` and its variants. One is rhetoric; thirty
     is the machine cadence a human hears as inhuman. Test each: *did anyone actually believe the
     negated half?* If not, delete the negation and keep the assertion.

   **And for any page making claims about the reader's own code or own long-held tools, the
   reader-twin is not enough: add a hostile reviewer with repo access.** In the same 2026-08-04 case
   the rebuild's panel found four claims about the maintainer's own public repos that were
   falsifiable in a browser (a negotiation that "refuses" what it actually declines to advertise, a
   tool count off by one, a "no SDK" claim true of one repo and stated over two, and a history claim
   about the IDE he had used for 25 years). **Zero of those were catchable by an accuracy pass or a
   sympathetic reader.** See `nemesis-review` and `paladin-review`; the adversary finds what is
   false, the guardian finds what is buried.

   **Three more rules measured in that same run (2026-08-04, 7 reviewers over 2 pages, and the
   blockers did not overlap AT ALL between lenses):**
   - **THE FIX PASS CREATES DEFECTS. Budget the re-review as part of the fix, never as a bonus.**
     About forty edits produced four broken "section NN" pointers (from inserting one new section),
     a hero count that no longer matched the page, and a live self-contradiction where one section
     said "18 questions" while another said 22 and explicitly warned that saying 18 breaks the
     arithmetic. Every one was introduced BY the fixes. After any substantial fix batch, re-run a
     fresh reader-twin over the WHOLE artifact and grep specifically for: cross-references to
     renumbered sections, counts stated about the page's own contents, and the same fact stated
     differently in two places.
   - **A DISTINCTIVE claim is still a claim, and it is the least likely to be checked.** "The only
     one that...", "the first...", "unusually..." read as enthusiasm rather than assertion, so
     nobody verifies them. One page's entire headline ("the only requisition in the search that
     requires Claude by name") was refuted in thirty seconds by the maintainer's own archive, which
     contained at least eight counter-examples including one he had annotated himself. **If a
     sentence claims uniqueness or rarity, grep the corpus that would disprove it before shipping.**
   - **Hedging a credential the source states plainly is a defect in the other direction.** A page
     marked his degree PARTIAL and coached him toward the requisition's "or equivalent experience"
     escape hatch, while his resume asserts a named BS from a named university, unhedged. That is not
     caution, it is inventing a weakness on the one item a recruiter screen actually verifies.
     **Check what the source document asserts before softening anything.**

   **Three more, from the 2026-08-05 follow-up run (a design-story page, lean twin+nemesis panel;
   zero blocker overlap between the lenses for the third measured time):**
   - **THE SCAR RULE: when the maintainer's own project MEASURED a mechanism failing, never cite
     that project as clean support for the mechanism.** A page taught a similarity-floor refusal
     gate and cited his RAG repo as the receipt; the repo's own README documents that exact gate
     failing (0 of 4, score bands overlap). The fix is promotion, not concealment: lead WITH the
     negative result and derive the design from it ("I built this, measured it, it failed, which is
     why the design does X instead"). A quoted negative result of your own is the most credible
     sentence available; a counterexample cited as support is the least. Corollary: teaching the
     TEXTBOOK idealization of a mechanism his measurements contradict ("unrelated text scores near
     zero" versus his measured floors of 0.25 and 0.57) is the same defect in prose form.
   - **BUILD FROM THE LEARNER'S OWN QUESTIONS WHEN YOU CAN.** The strongest sections of that page
     were the ones the maintainer asked for mid-conversation ("who computes the confidence
     number?", "how does the agent reach the databases?"). A page grown from a live design dialogue
     answers questions a research-grown page never thinks to ask, and the learner already owns half
     the material because he co-derived it. When the maintainer is narrating a problem, treat every
     question he asks as a section request.
   - **IN THE LAST HOURS BEFORE THE EVENT, THE FORMAT IS CHAT PARAGRAPHS, NOT NEW PAGES.** Short
     primers in conversation, each grounded by opening the actual source first (own-repo claims
     especially; the write-safety primer surfaced hard-assert and concurrency details memory would
     have flattened), each ending with a one-liner the maintainer can say aloud. Let his follow-up
     questions drive depth instead of pre-building it.
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

   ⚠️ **A SUBAGENT TOLD "DO NOT REVEAL THE RESEARCH" WILL STILL LEAK IT, BECAUSE IT HAS IT.** A prep
   page built by a strong subagent under an explicit no-reveal instruction still shipped three
   leaks: an age claim about a named interviewer, a personality attribution ("someone who measures
   things"), and a question routed to one person by name because research showed his interest in
   that topic. The instruction was obeyed as a TOPIC ban and violated as a PHRASING leak. Two
   mechanical fixes, strongest first: **(a) keep the research out of the builder's context entirely**
   and pass only the behavioral conclusion ("ask him real questions and let him talk"), never the
   evidence; or **(b) run a dedicated leak lens** whose only job is flagging any sentence that could
   only have been written by someone who researched the room, including lines scripted into the
   reader's own mouth. A general hostile lens does NOT reliably catch this, because a leak reads as
   helpful specificity rather than as a defect. Worst instance: the leaked age claim had already been
   contradicted by the reader's own in-room observation days earlier, so a refuted research artifact
   outlived its refutation by being re-stated in a new document.
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

### Rules added 2026-08-10 (an MCP-internals page, a panel-prep page, and two library upgrades in one run)

Four durable additions, all field-proven. The panel this run prepared for was a technical one, and the
reviewers were a repo-armed nemesis plus two isolated reader-twins.

- **⭐ NEW COMPONENT: the self-test whose answers are actually hidden.** A reader-twin scored a
  thirteen-question closed-book section **1 out of 5** and reported skimming it: *"the answer sitting
  right under the question... I'm not testing myself, I'm reading a FAQ."* Stacked question-and-answer
  pairs at the end of a long page are where fatigue peaks and the format defeats its own purpose. Fix:
  native `<details>` / `<summary>`, no JavaScript, offline-safe, one row per question with the answer
  collapsed. Verify with a browser check that answers are hidden by default (`offsetHeight === 0`) and
  that a row opens. The instruction line matters as much as the mechanism: *"say your answer out loud
  first, then open the row."* Class defs (`.qz`, `.qz summary`, `.qz .ans`) belong in the kit.
  Rule of thumb: **more than about four questions in one block, hide the answers.**

- **⭐ TEACH TOPIC B THROUGH THE TOPIC THE LEARNER JUST LEARNED, AND LEAD WITH "SAME SHAPE, DIFFERS IN
  EXACTLY ONE THING."** Two protocols taught hours apart became nearly free the second time because the
  page opened by naming the identity (both are JSON-RPC over a child process with a capability
  handshake) and then isolated the single real difference (one frames messages by newline, the other by
  a byte-count header). The difference is where the teaching lives, because a genuine engineering
  tradeoff sits inside it. This is stronger than the usual analogy move: the vehicle is not an everyday
  image, it is **a thing the reader verifiably understood an hour ago**, so the transfer is exact rather
  than approximate. When two topics on the roadmap are structurally related, sequence them deliberately
  and make the second one a delta.

- **⚠️ A WRONG EXPLANATION INSIDE A SELF-TEST ANSWER IS WORSE THAN THE SAME ERROR IN PROSE, because the
  format instructs the reader to memorize and say it.** The nemesis found a mechanically wrong framing
  explanation that had been written into a closed-book answer, i.e. into the one part of the page whose
  entire purpose is to be reproduced out loud under pressure. Prose gets skimmed; a quiz answer gets
  rehearsed. **Verify every self-test answer to the same standard as a load-bearing factual claim, and
  hunt them specifically**, because a reviewer reading for clarity will pass over a confidently wrong
  answer exactly as fast as a correct one. Related: the honest replacement was also the *better*
  answer, which is the recurring pattern in this file.

- **⚠️ WHEN A PAGE MANUFACTURES ITS OWN APPARENT CONTRADICTION, IT MUST RESOLVE IT ON THE PAGE.** Two
  sections stated facts that were each true and that looked mutually exclusive four sections apart
  (a rule forbidding a null identifier, and a case that legitimately sends one). The nemesis flagged
  that the page *"builds the trap and never disarms it"*, and that the reader had been instructed to say
  both halves aloud. The resolution existed and was one sentence: the two rules govern different
  message directions. **Grep a finished page for pairs of confident claims that a hostile reader would
  put next to each other, and either reconcile them in place or cut one.** Anticipating the collision is
  cheap; meeting it live is not.

### Rules added 2026-08-11 (a technical-domain page built, panel-reviewed, then rebuilt from zero)

A page teaching REST API design for an upcoming technical interview went through a four-lens gate: a
compile-and-run code skeptic, an adversarial reviewer, a guardian reviewer, and a cold reader-twin.
It was then thrown away and rewritten, and the rewrite was cheaper than the patch pass would have been.
Four durable rules.

- **⭐ STATE THE READER MODEL EXPLICITLY BEFORE WRITING, AND CHECK IT AGAINST EVIDENCE. A wrong reader
  model generates a CLASS of defects at once, not a list of them.** The page was framed in its first
  paragraph as "a refresher for someone who has already shipped these." That single choice independently
  produced: a practitioner voice ("a CDN never reaches my servers"), no line anywhere marking what the
  reader had actually operated, eleven separate promises that a given sentence would impress the
  interviewer, over-explanation of the language he owns cold, and under-explanation of the exact
  mechanisms he had never touched. The panel reported these as five or six findings. **They were one
  finding.** The maintainer fixed it in one sentence ("assume I have never built one") and every symptom
  resolved together.
  **Two independent axes, and both must be stated:** what the reader knows COLD, and what the reader has
  actually OPERATED. Getting the first wrong produces condescension. **Getting the second wrong produces
  claim inflation**, which is the expensive one, because the page then coaches a voice the reader cannot
  back up when asked "where did you do this?"
  **The tell, and it is countable: when a review panel returns several findings that all point at
  register, framing or emphasis rather than at facts, stop patching and re-examine the reader model.**
  Factual defects are independent; register defects arrive in correlated clusters because they share a
  cause. A panel is excellent at symptoms and poor at root cause; the orchestrator owns that synthesis.

- **⭐ ANY PAGE TEACHING WHAT THE READER HAS NOT OPERATED NEEDS AN HONEST-CLAIMS SECTION BY DEFAULT.**
  Not as a patch after a reviewer flags it. A page about problems at a scale the reader has never worked
  at is a claim-inflation hazard *by construction*, and the guardian lens will say so every time. Build
  in: a HAVE / STUDIED table sourced to primary documents, and one rehearsed sentence the reader
  volunteers EARLY rather than surrendering under follow-up. The ordering is the whole mechanism. Said
  first it reads as calibrated seniority; extracted third it reads as someone caught out. Corollary that
  paid off here: the honest inventory surfaced genuinely relevant experience the page had ignored, so the
  section made the reader look *stronger*, not weaker.

- **⚠️ THE EXECUTING LENS BEATS EVERY PROSE LENS ON BEHAVIORAL CLAIMS, AND THE PROSE LENSES DO NOT KNOW
  IT.** The page claimed that inserting a row during offset pagination causes both a duplicate and a
  skipped row. An adversarial reviewer, a guardian reviewer and a cold reader all read that sentence and
  none flagged it. A simulation walking every page to exhaustion settled it immediately: **an insert
  duplicates and skips nothing; a delete skips and duplicates nothing.** The same lens captured a
  cache-fingerprint bug off a live response header (a byte array interpolated into a string yields the
  literal type name, so every record got an identical fingerprint) and measured an authorization sample
  approving another user's record. Generalize past code: **any claim of the form "under scenario X,
  behavior Y happens" is a claim you can simulate**, and prose review only evaluates whether a sentence
  reads as true.

- **⚠️ THE EM-DASH CHECK MUST COVER HTML ENTITIES.** A grep for the literal character reported clean and
  a screenshot showed four em-dashes rendering, written as `&#8212;` inside SVG `<text>` labels. All four
  forms render identically: `—`, `&#8212;`, `&mdash;`, `&#x2014;`. Prefer `&#183;` as a separator inside
  diagram labels. This is the general rule in miniature: **a clean grep is only as good as the forms it
  searches for, and an encoding the renderer resolves is a form.** It was found by looking at the render,
  which is the standing argument for the visual gate being mandatory rather than a nicety.

### Rules added 2026-08-13 (a panel-prep page rebuilt from zero after the reader bounced off a gate-clean version)

The predecessor page was accurate, sourced, and had passed the full four-lens gate. The maintainer
read it and stalled on passage after passage, pasting each into chat in real time. The rebuild on a
corrected reader model passed the same panel with only narrow factual findings and no register
findings. Five durable rules:

- **⭐ THE READER MODEL HAS A THIRD AXIS: WHAT THE READER HAS FORGOTTEN OF THEIR OWN WORK.** Beyond
  knows-cold and has-operated, state what has decayed. The load-bearing fact the gate-clean page
  missed was one the reader then supplied himself: assume everything about his own repos, and the
  protocol they implement, is forgotten. Built-months-ago predicts nothing about can-explain-today.
  Gates verify truth and clarity; a wrong reader model passes both, so the orchestrator owns the
  model, and the reader-twin's charter must state all three axes explicitly.
- **⭐ THE LIVE READER MID-READ IS AN INSTRUMENT NO TWIN MATCHES, AND EVERY PASSAGE THEY PASTE BACK
  IN FRUSTRATION IS A SECTION REQUEST.** Each pasted "what does this mean" block was answered in
  chat from zero AND became a taught section of the rebuild (a grounding section, a pairing section,
  a worked dialogue, a five-decision walkthrough, a translated code comment). The finished page's
  strongest sections were commissioned this way. This is build-from-the-learner's-questions
  sharpened: a complaint IS the commission, not a wording note.
- **⚠️ A WORKED DIALOGUE IS THE HIGHEST-RISK BLOCK ON A PREP PAGE.** It is the one block the reader
  absorbs verbatim, in their own voice, so its claims feel like recall to writer and reader alike.
  Both hostile lenses' top findings sat inside the dialogue: a capability claim the reader's own
  code refutes (schema validation that does not exist; enforcement lives per-handler), and a
  research leak scripted into the reader's mouth (a question presupposing a fact only
  audience-research could supply). Verify every scripted line at as-sent-resume rigor against the
  source, and sweep all sayable lines for facts that could only have come from researching the
  audience.
- **⚠️ A VERBATIM QUOTE FROM THE READER'S OWN CODE IS A RECEIPT, NOT TEACHING.** Comments compress.
  Teach the mechanism first, show the quote as the checkable receipt, and attach a one-breath
  translation directly after it, so the quote never has to carry the teaching load. The reader
  bounced off his own class comment until it was walked clause by clause.
- **⚠️ RETIRE ROUNDING-UP PHRASES WHEREVER THE RATIO IS CHECKABLE.** "Nearly doubled" for a 1.66x
  gain survived multiple gates and two upstream memory documents before an adversarial pass divided
  the raw numbers. State the two numbers; the phrase is drift, and the reader's audience contains
  people who divide.

### New page GENRE added 2026-08-14: the GLANCE CARD (at-a-glance monitor crib sheet)

Commissioned the night before a decisive panel interview: 2-4 single-screen pages the maintainer
keeps on the monitors behind his laptop during a video call, to glance up at if he freezes. A
distinct genre from a teaching page, with its own rules, all field-proven in one build-fail-rebuild
cycle that same night:

- **What it is:** one viewport, ZERO scrolling ever, read-at-a-glance from several feet away. Huge
  bold keywords (20-40px) carrying the load; tiny mono subtext only as memory fuel; boxed-flow
  diagrams (stages with arrows) over prose; one accent color per card. No self-tests, no narrative,
  no links: it is a crib sheet, not a lesson. Content comes ONLY from an already-gated prep page,
  because a glance card inherits zero of its own verification.
- **⭐ DESIGN AT THE TARGET WINDOW'S ASPECT RATIO; an auto-fit scaler cannot fix a wrong-aspect
  layout, it can only MASK one.** The first build laid cards out landscape (~1240x770) and shipped
  with a script that scales content to fit any window. The maintainer's real windows were PORTRAIT
  halves of landscape monitors (~1000x1200). The scaler dutifully shrank the landscape design by
  width, producing tiny text over a half-empty screen: technically no overflow, practically
  unreadable, and the maintainer bounced hard. The fix was a redesign at ~980px-wide portrait, not
  a scaler tweak. **The reported window size is a DESIGN input, not just a verification size**:
  having the exact dimensions in hand (a screenshot was provided) and using them only to verify is
  the trap; lay the content out for that shape first.
- **Still ship the auto-fit scaler as the safety net** (transform scale = min(vw/w, vh/h, cap),
  re-run on resize, center horizontally with the leftover width). It absorbs the difference between
  design size and the real window so no snap arrangement can ever cut content off or scroll.
- **Verify RENDERED at the exact reported window dimensions**, not a default viewport. The
  em-dash/entity grep still applies (crib cards ship the same banned characters as any page).
- **One card should be the PANIC card:** the recovery moves for going blank at the very top (say
  the question back, name the boundary, start from the concrete thing you built, say-so-and-move),
  then the say/never-say list and the two or three highest-stakes stories in compressed form. The
  freeze is the moment the cards exist for, so the freeze card leads.
- Register the cards on the dashboard and chip them onto the interview card so they are findable
  in one click on the morning.

### Rules added 2026-08-19 (a four-topic primer built and gated in one session: twin, accuracy skeptic, nemesis, then a post-fix twin)

Four durable additions. The run is also the cleanest measurement yet of what a fix pass costs.

- **⚠️⚠️ A FOURTH BLIND SPOT IN THE DETERMINISTIC DIAGRAM GATE, AND IT IS THE WORST ONE, BECAUSE THE
  GATE REPORTS CLEAN WHILE THE PAGE IS VISIBLY BROKEN: CSS transforms on SVG elements resolve
  `transform-origin` against the VIEWBOX, not the element.** A row of animated progress bars
  declared at `x="70"` with `transform-origin:left center` and an animated `scaleX` did not grow
  from their own left edge; they scaled from `x=0`, sliding left across the canvas and covering the
  row labels at `x="20"`. **The bbox gate cannot see this by construction**, because `getBBox()`
  returns UNTRANSFORMED geometry: every element measured exactly where it was authored, so overflow,
  collision and inside-the-box checks all passed while the render was mangled. Only the screenshot
  caught it. **Fix: `transform-box: fill-box` on every animated SVG element** (SVG's initial
  `transform-box` is `view-box`, which is almost never what you want). Generalizes: *any* check that
  reads authored geometry is blind to *any* defect introduced by rendering, so animation and
  transforms move a page's failure modes out of the gate's reach entirely. If a page animates, the
  screenshot is not a nicety, it is the only instrument that works.
- **⚠️ AN IMPOSSIBILITY CLAIM ABOUT THE READER'S OWN MEASURED DATA IS ONE PARAMETER SWEEP FROM
  REFUTATION, AND NOBODY SWEEPS IT.** A page taught that a similarity threshold could not separate
  two populations, "no threshold exists," derived from a real overlap in the reader's committed
  results. The nemesis swept every candidate floor against the raw per-question scores and found one
  that catches 4 of 4 at a cost of 5 of 18 false positives. **Nothing was fabricated; "separates"
  had silently meant "separates perfectly."** The honest replacement is strictly stronger: a priced
  tradeoff the author declined, with the price stated, rather than a wall. **Rule: when a page says a
  mechanism is impossible, cannot work, or that no value of X would help, SWEEP X against the raw
  records and state the cost instead.** Impossibility is the most checkable claim on any page and the
  least checked, because it reads as a conclusion rather than an assertion. Same family as the
  motivating-claim rule; the tell is any absolute quantifier ("no", "never", "cannot", "any").
- **⚠️ IDENTICAL NUMBERS IN A COLUMN READ AS REPLICATION. CHECK WHETHER EACH ROW COULD HAVE PRODUCED
  A DIFFERENT VALUE.** The same page showed a guard scoring "0 of 4" on three runs, in the same
  visual weight as its other metrics. Two of those runs had the threshold configured below every
  score in their own result file, so refusing anything was arithmetically impossible: those zeros
  were **not measurements**, and only the third row tested the shipped configuration. **Before a
  results table implies n=3, verify each row's configuration could have moved the number.** Print the
  varying parameter as its own column; a constant that was not actually constant is where a table
  lies without a single wrong digit.
- **⭐ TRACK THE READER-TWIN'S TWO SCORES SEPARATELY, BECAUSE A FIX PASS TRADES THEM AGAINST EACH
  OTHER.** Twin 1 scored the draft 7/10 "did this teach me" and 6/10 "could I finish it without
  disengaging." A ~30-edit fix pass answering every finding moved it to **8 on teaching and 5 on
  engagement**: comprehension up, completion down, because the fixes were definitions, caveats and
  precision, and all three add mass. The twin named the mechanism: nine warning blocks meant the
  warning symbol stopped signalling, one finding got fully restated in three separate sections, and
  one term got defined twice 200 words apart. **A fix pass is not done when the findings are
  answered; it is done when the second score has not dropped.** Practical countermeasures, all from
  that twin: cap the alarm symbols per page, state a finding once and cross-reference it rather than
  re-telling it, and after inserting a definition grep the rest of the page for the older gloss of
  the same term. Corollary worth its own line: **a page can fail by being MORE correct.**
