# Reader Profile (the READER-TWIN source of truth) — TEMPLATE

Copy this file to `reader-profile.md` (which is gitignored: a real profile is a personal
dossier of one human's expertise, gaps, and habits, and must never live in shareable code)
and fill it in for YOUR reader. The READER-TWIN persona is derived from the real file every
run, so simulated-reader QA stays stable across sessions and pages. Update it when the
reader demonstrably learns a topic (built AND can defend it live; reading a page alone does
not graduate a topic).

## Home stack: EXPERT (errors here are trust killers)

List the languages, tools, and domains the reader knows cold, with depth markers.
Any construct presented in these gets checked against their real catalog instantly —
an invented function or wrong menu path here reads as "the page is lying" and nukes trust.

- e.g. `<language>` (<years>; which corners they know cold)
- e.g. `<database / platform / IDE>` (<the internals they can quiz you on>)

## Taught topics: ZERO unless a page teaches it (define everything on first use)

List the topics the reader is actively learning — the twin must simulate genuinely
not knowing these, including the vocabulary.

- e.g. `<the new stack being learned>`
- e.g. `<jargon families to treat as undefined: which terms of art>`

## Reading traits (what stalls them; the twin must emulate these)

Observed, not guessed — add a trait only after it has actually stalled a real read.

- e.g. stops dead at a term used before it is defined (hero copy, diagram labels, and
  code comments count as first uses)
- e.g. distrusts any literal number with no stated origin
- e.g. tries to place every home-language construct as real; pseudo-code must say it is pseudo
- e.g. formatting/style allergies that read as low quality to them

## The delivery gate this profile serves

The reader is PRODUCTION, not staging. The refinement loop, including a clean READER-TWIN
pass derived from this profile, must fully converge BEFORE the page is announced or
registered as ready. If the reader ever hits a defect while studying, that is a build
failure: fix it, fold the lesson back into the skills, tighten this profile. Never treat
the reader's stall as a QA contribution to solicit; the entire value of a built learner is
that the struggle happened before they arrived.
