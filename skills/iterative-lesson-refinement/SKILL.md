---
name: iterative-lesson-refinement
description: Use when a teaching or study artifact (HTML page, study pack, explainer, interview-prep doc) must hold up under live questioning, when a lesson "reads fine" but the learner keeps failing follow-up questions, when asked to "battle-test / tighten / refine" a lesson, or when a learner needs to genuinely own a topic fast instead of reciting it.
---

# Iterative Lesson Refinement

## Overview

A QA loop that turns a draft lesson into one that *actually teaches* and that the learner can
*defend live*, by exposing it to **isolated personas** instead of grading your own homework.
Core principle: a lesson's author cannot see its holes, and a persona you role-play inline just
echoes what you already know; isolation is the whole point.

## When to Use

- A teaching artifact must survive a skeptical follow-up ("you said cosine, why not Euclidean?"),
  not just read well.
- The learner is time-starved: the artifact must be as SHORT as possible while still letting them
  do the thing and survive the second question. Brevity is a graded criterion, not an afterthought.
- **When NOT to use:** content nobody must defend (internal notes, logs); or a first draft that
  hasn't been written yet (write the tight draft first, then run the loop).

## The Loop (per topic)

1. **Build/revise** a tight draft. Ground every claim to the learner's real work honestly
   (HAVE / PARTIAL / GAP). If a companion HTML-craft skill exists, use it for the page itself.
2. **Dispatch 4 ISOLATED subagents**, each reading ONLY the artifact file: no answer key, no
   authoring context. Locked roles:
   - **NOOB**: technical generalist who has never met the topic; no outside lookups. Reports
     confusion, drag, and density/overwhelm flags; takes the cold quiz. Your density detector.
   - **BASICS**: surface familiarity; mandate = depth gaps, half-explained terms, "asserted
     without justifying." Takes the cold quiz.
   - **EXPERT**: practitioner + interviewer; mandate = (a) ACCURACY (quote → problem → fix),
     (b) DEFENSIBILITY (the exact follow-up that exposes each weak claim), (c) TIGHTNESS
     (a specific cut list). Does NOT take the quiz.
   - **READER-TWIN** (mandatory since 2026-07-06; the slot whose absence let a stall ship):
     derive it per artifact from `references/reader-profile.md` (the durable profile of the
     actual reader: home-stack expertise, zero-knowledge topics, reading traits; update the
     profile as the reader demonstrably learns topics). The real profile is personal and
     gitignored; copy `references/reader-profile.template.md` to create one for your reader. Shape: deep expert in A (their home
     stack: the language, IDE, or domain the page translates FROM or leans on), ZERO knowledge
     of B (the topic being taught). Mandate: reading in order,
     flag (a) any term used before defined (hero copy, diagram labels, and code comments count
     as uses), (b) any literal number without a stated origin, (c) any construct in language A
     they cannot place that is not labeled invented/pseudo, (d) metaphor switches without a
     bridge, (e) read-twice sentences. This slot exists because the other three CANNOT catch a
     fake construct in the reader's home language or a home-turf falsehood: a 9-page field sweep
     found the generic trio had passed pages 10/10 that the reader-twin then found ~75 defects in.
3. **Grade the cold quiz** against a rubric (answers in the learner's own words, /10); log scores.
   Synthesize the reports → **verify before applying**: an auditor's factual counter-claim ("the
   page's number is wrong") is testimony, not truth; check it against a primary source before
   editing (field case: an auditor confidently corrected a right number to a wrong one; the doc
   fetch caught it). Then revise, and **fact-check any NEW fact the revision itself introduces**
   (fixes are un-audited authoring; a fix pass once shipped a checkably false origin story for
   the very number it was fixing). Record the *generalizable* teaching lesson (not topic facts)
   back into this skill.
4. **Repeat ~2 passes**, escalating quiz difficulty each pass: pass 1 tests the spine (can they
   describe it?), pass 2 tests the defense layer (the second question). Early-exit when a fresh
   NOOB scores ≥8/10 AND the expert flags no accuracy/tightness issues AND a fresh READER-TWIN
   reports zero stalls (no term-before-defined, no unexplained number, no unplaceable construct).
5. **Finalize:** bump the artifact's version footer with what changed; clean up test scraps.

## The delivery gate (non-negotiable)

**Run the WHOLE gate ONCE, UP FRONT, before the learner ever sees the page. Never serially.**
The most expensive failure mode is not a bad page; it is *reactive gating*: ship, let the human
hit a hole, add one QA instrument, ship again, let them hit the next hole. Each round burns their
tokens, their time, and their trust, and it makes the human the trigger for your next QA step,
which is exactly backwards. Before first delivery of any teaching page, in ONE parallel batch:
(1) build it right, most teaching topics are standard, not novel research, so invest the craft up
front; (2) run the full gate at once, the READER-TWIN plus, for a defend-cold/interview page, the
nemesis + interviewer + accuracy panel; (3) fix what survives verification, and re-read the whole
page once (patches can sum to worse); (4) THEN deliver. The human should never meet a pre-gate
artifact, and should never have to name a missing review instrument. If you find yourself adding a
reviewer *because the human asked why you didn't*, the gate ran too late.

**The learner is PRODUCTION, not staging.** The loop exists so the struggle happens before they
arrive: they read to LEARN, never to debug. Therefore an artifact may not be handed to the
learner, announced as ready, or registered in any index until the loop, including a clean
READER-TWIN pass, has converged WITHOUT them.

**Interview-prep / "defend-cold" pages need an ADVERSARIAL pass too, not just the reader-twin.**
The reader-twin is sympathetic; it measures "can I follow this," which catches confusion but
NOT confident-but-wrong claims or unarmed follow-ups. A page whose stated job is surviving a
hostile interviewer must be reviewed by a hostile interviewer. So for any defend-cold page, add
to the gate a `nemesis-review` panel: the nemesis (armed with the audience's expertise) plus an
interviewer-follow-up skeptic ("for each answer, what is my next question, and does the page arm
it?") plus, for technical pages, a domain-accuracy skeptic. Field case 2026-07-07: a Docker page
that passed the reader-twin 9/10 still had three defend-cold answers that each detonated on the
first follow-up (a healthcheck fix that did not fix the race, an EXPOSE claim that ignored
`-P`, and a grounding line that overclaimed a skill the reader had not authored, the exact
trap that had already cost a real final-round interview). Only the adversarial panel caught them. This is why the gate is two instruments,
not one: reader-twin proves it teaches, nemesis proves it does not get the reader killed in the room. If the learner ever hits a defect while studying,
treat it as a build failure with a root cause in this loop (usually a persona slot that didn't
match them): fix the page, fold the lesson back into this skill, and tighten the reader profile.
Do not thank the learner for the QA or frame their stall as a contribution; the moment they are
"helping refine," the artifact has already failed at its one job.

### Targeted validation mode (cheap variant, added 2026-07-05)

When REVAMPING an artifact whose spine already converged in earlier passes, do not re-run the
full 3-persona loop. Dispatch **2 agents in parallel**: a fresh NOOB (cold quiz over old + new
content) and an EXPERT whose fire is pointed at the NEW sections. **Give the EXPERT the
artifact's audience expertise explicitly** (their stack, their era), not just the topic domain:
audience-home-turf claims are the highest-risk content and a domain-only expert sails past them.
Field result: this 2-agent pass caught a false claim about the reader's own database engine that
three earlier full passes had missed. When the artifact is a TRANSLATION ("B via the A you
know"), make the second agent a full READER-TWIN (A-expert, zero B) rather than a domain expert
with audience seasoning; only the twin catches invented constructs in language A.

## Quiz Design (the real gate)

- Author a per-topic quiz; learners answer **in their own words** (no copy-paste).
- A perfect score on a recall quiz proves nothing: the page teaches *its own claims* well.
  The defense-layer quiz (second-order follow-ups) is what catches recite-vs-own.
- If a learner cannot answer, require them to name WHICH word or idea the page failed to give
  them; that names the fix.

## The Generalizable Teaching Lessons (the payload)

1. **Quiz the defense layer, not the page's own claims.** Escalate difficulty each pass.
2. **Define the load-bearing mechanism word on first use.** Beginners stall exactly on the words
   presented AS the machinery (the #1 observed failure mode across every run), not optional jargon.
3. **Never name an interview question you don't arm.** Flagging "be ready to defend X" without
   the material is worse than silence.
4. **A "defend cold" Q&A must carry NEW depth** (second-order follow-ups), never restate the body.
5. **One metaphor per concept**, reused deliberately; three competing metaphors read as padding.
6. **State key numbers once, with their justification**, then reference them.
7. **When you ground a claim to the learner's real work, pre-arm the obvious follow-up.**
   "I ran X on my codebase" → "how exactly?" must be answered ON the page.
8. **Define every borrowed term even inside an advanced section**; name-dropping lets a learner
   recite without owning, the exact thing a follow-up exposes.
9. **Mark the difficulty step-up** ("second-pass layer") so the beginner isn't silently drowned.
10. **Lead with the why before the how:** plain-English claim → analogy → diagram → defend-it Q&A.
11. **A defense answer must be self-contained.** Never let it lean on a term the page never
    defined; that recreates the exact trap the Q&A exists to close.
12. **By the final pass, weight to TIGHTNESS.** Cut any defend-cold card that restates the spine.
    Stop signal: fresh NOOB ~10/10 cold AND expert says "ship after ≤2 one-line fixes."
13. **Check every claim about the reader's OWN home stack against its CURRENT state.**
    Translation sections ("new thing B via the A you already know") date fastest exactly where
    the reader is most expert, and a stale claim there detonates on their home turf. Arm the
    EXPERT persona with the reader's home-stack expertise so it hunts these.
14. **A worked example must not disprove its own lesson, and simulated outputs must be
    watermarked IN the artifact.** Demonstrating semantic search with a question that near-quotes
    its source proves keyword search would have worked too: paraphrase until zero surface tokens
    overlap. Realistic invented scores/terminal output without a "simulated" label become
    "observed data" one lazy memory later; a caption saying "illustrative" is not enough, mark
    the artifacts themselves.
15. **Define-on-first-use is a WHOLE-PAGE ordering constraint, not a per-section virtue.** Hero
    copy, diagram labels, and code comments count as uses; a later deep-dive section does not
    excuse an unglossed first appearance. Walk the page in reading order before shipping. (The
    dominant defect class in a 9-page field sweep, on 8 of the 9 pages.)
16. **Every literal number carries its origin at first use.** What fixes it, whether the reader
    can change it, and an analogy class ("a hash width"); mark example values AS examples ("k = 5
    is this page's example, not a law") and name the corpus behind scale claims. Invented
    precision ("90% of confusion") reads as fake and poisons trust in the real numbers.
17. **Label invented/pseudo-code as pseudo IN the artifact**: before the panel, in the panel
    label, and in a code comment, and name the real construct it stands for. An invented function
    in the reader's home language makes the expert reader conclude they are ignorant or the page
    is lying; both destroy the page.
18. **Home-turf falsehoods are the fastest trust killers.** A wrong claim about the reader's OWN
    tool ("your IDE refuses to start without X") outranks any topic error, because it is the one
    claim the reader can check instantly. The READER-TWIN slot exists to hunt exactly these.

## Subagent Prompt Skeleton

> You are role-playing [NOOB/BASICS/EXPERT] for a lesson-quality test. Stay in character.
> PERSONA: [knowledge level + mandate; for EXPERT also the artifact's AUDIENCE expertise].
> HARD RULES: read ONLY <file path>; no web/outside knowledge beyond your level; be specific,
> not polite. TASK: [confusion/depth/accuracy log] + [cold quiz answered in your own words].
> RETURN in fixed labeled sections (A)…(E).

## Files Convention

Keep a run self-contained in a `LessonLab/` folder: `PROTOCOL.md` (rules of the run),
`quiz_<topic>.md` (questions + rubric), `quiz_log.md` (scores + per-iteration findings + the
generalizable lessons). The log is durable state across the many turns a loop takes.

## Common Mistakes

- **Role-playing the personas inline.** They echo the author's knowledge; only isolated
  subagents produce real confusion data.
- **Treating a 10/10 recall quiz as done.** It proves the page states its own content well,
  nothing more; escalate to the defense quiz.
- **Skipping the loop because the draft "reads clean."** Every field run found real defects in
  drafts that read clean, including factual errors.
- **Letting the loop inflate the page.** Track length trending DOWN while scores hold or rise.
- **Treating convergence as immunity.** A 10/10 across passes proves the CURRENT persona set is
  satisfied, nothing more; if no slot matches the actual reader's profile, the blind spot ships
  with a perfect score. The persona set must span the reader, then convergence means something.
- **Applying an auditor's factual "correction" unverified.** Personas hallucinate with full
  confidence; a counter-claim about a number, API, or doc must be checked against the primary
  source before the edit (else the audit inserts the error it exists to catch).
- **Trusting your own fix.** New facts written during revision got zero persona scrutiny;
  fact-check them like first-draft claims.
- **Serial gating (the token-and-trust killer).** Adding a QA instrument only after the human
  catches its absence. Every review the page needs must run in the SAME up-front batch, before
  first delivery. If the human ever asks "did you run it past X," X should already have run; the
  question means the gate was incomplete, not that the human requested an optional extra.
- **Under-investing the first artifact because the ask sounds basic.** "Make a beginner page on
  a standard tool" is not a research problem; build it to the finished standard the first time.
  The gate confirms quality, it does not rescue a lazy first draft, and rescuing one costs more
  than doing it right did.
- **Ending a fix pass at "all findings applied + greps clean."** Patches are local; convergence is
  global. After applying findings, a fresh READER-TWIN must re-read the WHOLE artifact (field case:
  8 bolted-in glosses + a 49-substitution punctuation purge left a page mechanically compliant on
  every rule and materially worse to read; the reader bounced off it the next day). Fixes must be
  WOVEN into the prose, not bolted on as parentheticals; mechanical character substitution requires
  sentence-level rewriting.
- **Not propagating a fix to its neighbors (the dominant regression mechanism).** When a fix changes
  a load-bearing WORD or CLAIM, it is not done until every place that referenced the old wording is
  updated too: the hero/lede, sibling Q&A cards, SVG diagram labels AND their aria-labels, figure
  captions, and the footer. A prose fix that leaves a diagram or a neighboring card still asserting the
  old thing creates a fresh SELF-CONTRADICTION that reads worse than the original defect. Mechanical
  guard: after any patch, grep the page for the OLD word/claim you just replaced, and check every hit.
  (Field case 2026-07-07: applying an adversarial panel's fixes dropped THREE teaching pages from ~9 to
  6.5 on the post-patch reader-twin, every time because a prose edit did not reach its diagram or its
  sibling cards, e.g. hero still said "no compile step" after the body said "compiled to bytecode"; the
  SVG still said "shippable" and "21" after the prose said "usable" and "modified Fibonacci". All three
  re-verified to 9/10 once every neighbor was propagated. This is the mechanism under the "N fixes sum
  to worse" rule: it is usually an un-updated neighbor, not mere density.)

## Provenance (the test record)

Method developed and field-proven 2026-06-24 → 2026-07-06 across three topics plus a 9-page
library sweep. The sweep (2026-07-06) is the READER-TWIN's origin story: the page's real reader
stalled cold on a section that three converged generic passes (including two 10/10 fresh noobs)
had blessed; reader-matched twins then found ~75 defects across all 9 pages, two false claims
about the reader's own IDE, one wrong fix introduced BY a fix, and one auditor counter-claim
that was itself wrong (caught by fetching the primary docs). Baseline (RED):
a lesson built without the loop scored 10/10 on a recall quiz while carrying defensibility holes,
undefined load-bearing terms, and one factual error, confirming self-review can't see them.
With the loop: topic 1 converged in 3 passes, topic 2 (skill lessons applied up front) in 1 pass
with zero factual errors in its v1, and the 2026-07-05 targeted 2-agent mode caught a false
audience-home-turf claim plus an honesty trap (a first-person past-tense story card for work not
yet done) that three generic passes had missed. Quiz scores climbed or held at every pass while
page length held roughly flat.
