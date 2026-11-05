# Assumption Debt Logbook - <collaborator name>

This is the *fuel* for the `managing-assumption-debt` skill: a running record of the moments
an assumption diverged from reality, what it cost, and what would have caught it. It is
personal and should live wherever this collaborator's private memory lives, NOT in shareable
code. The skill (the engine) consults this file at its trigger moments and appends to it
whenever a fresh debt comes due.

Each episode is a compressed surprise. Over time these become calibrated trust: you learn
when this person's conviction means defer, and when it means they are in sunk-cost mode.

---

## How to add an episode

Copy the block below to the top of the Episodes list (newest first) and fill it in. Write
it when a debt *comes due* - that is when the lesson is sharpest and the cost is concrete.
Keep it to about 150 words; the SessionStart hook names episodes that run over.

```markdown
### EP-NNN - <short title>
- **Date:** <when it formed / when it came due>
- **Class:** external-boundary | provenance-drift | commission-misread | shared-state | silent-override | scope-creep | artifact-trust | **Recurs:** EP-aaa, EP-bbb (earlier episodes with the same root; omit if none)
- **The assumption:** what was quietly believed
- **The tell:** the early signal that would have caught it at formation
- **The cost:** what it actually cost (tokens, rework, real-world consequence)
- **Durable fix:** a guard, gate or test where one exists; a reminder only when nothing mechanical does
```

The `Class` line must be exactly `- **Class:** <slug>` optionally followed by ` | **Recurs:** EP-...`;
the hook parses it. Class slugs are defined in the skill's class table.

## Standing trust weights (updated as episodes accumulate)

A short, evolving summary distilled from the episodes - the "I know this person" layer.
Examples of what goes here: domains where their gut beats mine and I should defer; domains
where they tend toward sunk cost and I should push; recurring blind spots to watch.

- _(none yet)_

## Working countermeasures (debts that are now structurally prevented)

When a recurring debt gets a mechanical guard, record it here so it is not reinvented.

- _(none yet)_

---

## Episodes (newest first)

_(none yet - add the first one when a debt comes due)_
