---
name: versioning
description: Establish or maintain version certainty in a repo; one canonical VERSION stamped into every independently-deployed artifact, each made self-reporting, with a drift check. Use when setting up versioning in a new project, when asked "are we current / what's deployed?", when adding a version field/endpoint, or when build/deploy artifacts can silently drift out of sync.
---

# Versioning: know what's actually deployed

The failure this prevents: a repo ships several artifacts that deploy on **separate
steps** (compile/flash, bundle upload, server restart, container redeploy), and *nothing*
reports which version of each is actually live. You're left guessing whether a change
landed. A hardcoded `version: "1.0.0"` that never changes is worse than nothing; it
looks like a signal but isn't.

## The pattern (portable across any repo)

1. **One canonical source of truth.** A single `VERSION` file (SemVer) at the repo root.
   Nothing else is authoritative; everything is *stamped from* it.
2. **Enumerate the deployable artifacts**: the things that ship independently. Ask: "what
   are the separate deploy steps, and could each carry a different version?" Each one is an
   artifact. (Examples: firmware, a static web bundle, an API server, a DB migration set, a
   CLI binary, a published package, a container image.)
3. **Give each artifact a self-report channel**: a way to ask the *running/deployed* thing
   its version: a `/status` or `/version` endpoint field, a served `version.json`, a
   runtime-read manifest, a `--version` flag, an image label, a `__version__`.
4. **Stamp** `VERSION` into each artifact's source (a script that writes the header/manifest/
   constant). Generated files carry a "do not edit by hand" banner.
5. **Add an automatic build marker where it's free**: e.g. a compiler's `__DATE__ __TIME__`,
   a build-time git SHA, an image digest. This updates on *every* rebuild even if someone
   forgets to bump, so it proves the artifact was actually rebuilt.
6. **Check drift**: a tool that reads `VERSION`, probes each artifact's self-report, and
   prints a per-artifact ✓ / ⚠ DRIFT report. Expose it where it's needed (a CLI script, a
   tool the agent can call, a CI gate).

## The rule that trips people up

A version **bump is not live until its artifact is redeployed.** Editing `VERSION` makes the
*repo* say 0.5.0 instantly, but each deployed artifact still reports its old version until
*its own* deploy step runs (reflash / re-upload / restart / redeploy). So:

- **Drift between repo and a not-yet-redeployed artifact is expected, not a bug.** The check
  is telling you "you haven't deployed this one yet," which is exactly what you want to know.
- Therefore **bump deliberately** (a command you run when shipping), not automatically on
  every push; auto-bump-on-push manufactures false drift for changes that never reach some
  artifacts (docs, CI, one service), and you'll learn to ignore the alert.

## Adapting to a new repo (checklist)

- [ ] Create `VERSION` at repo root (start `0.1.0` unless there's reason to call it 1.0.0).
- [ ] List the independently-deployed artifacts. Most repos have 1 to 3; don't invent more.
- [ ] For each, pick a self-report channel and wire it to read the stamped value at
      runtime (so a bump doesn't require recompiling *that* artifact when avoidable).
- [ ] Write a stamp script (`VERSION` → each artifact source). Keep generated files marked.
- [ ] Add a free auto build-marker to any artifact that compiles.
- [ ] Write a check that diffs `VERSION` against each self-report; surface ✓ / ⚠ per artifact.
- [ ] Add a deliberate bump command (`bump:patch|minor|major` → rewrite VERSION, stamp, commit).
- [ ] Document in the repo's CLAUDE.md: the VERSION source, the bump command, what each
      artifact reports, how to check, and the "bump isn't live until redeploy" rule.

## Keep it honest

- Don't add versioning theater. If a repo deploys as one unit, one version + one self-report
  is the whole job; don't split it into fake per-component versions.
- The check must compare the **deployed** self-report, not re-read the repo source on both
  sides (that always "matches" and proves nothing).
- Prefer runtime-read of the stamped manifest over a compiled-in constant when the platform
  allows it; it means a bump goes live on restart instead of a full rebuild.

## Worked example: ESP32-S3 Matrix (a two-repo split)

Originally one repo with three artifacts. A 2026-06 repo split moved the MCP server into
its own repo, so the tooling re-scoped to each repo's *own* artifacts, which is itself a
reusable lesson: **when a repo splits, re-scope `stamp`/`check` to the artifacts that ship
from THIS repo.** A copied tooling file silently checks phantom artifacts that always read
"unknown", or crashes stamping a source file that no longer exists.

**Firmware repo** (`peckworks-esp32s3matrix`): 2 artifacts, both reported by one `/api/status` probe:

| Artifact | Self-report | Stamp target | Goes live on |
|---|---|---|---|
| firmware | `/api/status` → `fw_version` + `fw_built` (auto `__DATE__ __TIME__`) | `esp32_matrix_webserver/version.h` | flash |
| web bundle | `/api/status` → `web_version` (read from `data/version.json` at boot) | `esp32_matrix_webserver/data/version.json` | LittleFS upload |

**Studio repo** (`claude-expression-studio`): 1 artifact, the MCP server (shipped as an `.mcpb`):

| Artifact | Self-report | Stamp target | Goes live on |
|---|---|---|---|
| MCP server | `initialize` serverInfo / `matrix_version` tool | `mcp_server/package.json` (runtime-read) + the `.mcpb` `manifest.json` + `shared/manifest.json` `appVersion` | rebuild + reconnect |

- Canonical per repo: repo-root `VERSION`. Stamp: `scripts/version-stamp.js`. Check: `npm run check`.
- **Don't clobber a field that already means something.** `shared/manifest.json`'s `version` is
  the manifest *schema* version, so the product version is stamped into a separate `appVersion`
  field; never overwrite a schema/format version with the release version.
- **Stamp a hand-formatted or CRLF file with a targeted text edit, not a `JSON.parse`→`JSON.stringify`
  round-trip**; the round-trip reflows aligned columns and can flip CRLF→LF, burying the real
  one-line change in whitespace churn.
- Full design: `docs/superpowers/specs/2026-06-16-version-certainty-design.md` (now in the studio repo).
