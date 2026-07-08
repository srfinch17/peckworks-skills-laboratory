# Inline-SVG diagram patterns (themed, offline, responsive)

Copy-paste skeletons for the diagram types that recur in the maintainer's teaching pages. All use the THEME
hexes directly (SVG attributes can't read CSS vars). Wrap every diagram in `<div class="fig">…<p
class="figcap">…</p></div>`. Always set `viewBox` and OMIT width/height so it scales. Always add
`role="img"` + a descriptive `aria-label`.

## Theme hexes (for fill / stroke)

```
ink #0D1015 · ink-2 #151A21 · ink-3 #1C2330 · line #2C3442 · line-soft #212834
text #EAEDF3 · muted #94A0B2 · muted-2 #5F6A7B · C7CEDA (soft body text)
signal #FF8A3D (orange, the one thing that matters) · have #2BE0CE (teal, owned/correct)
partial #F5C13D (amber, caution/tuning) · adjacent #6E9BFF · violet #B98CFF
teal-tinted fill #102a28 · orange-tinted fill #17120a · amber-tinted fill #14110a
```

Label font: `font-family="'IBM Plex Mono',monospace"` for codes/labels, `'IBM Plex Sans',sans-serif`
for descriptive sub-text. SVG `<text>` does NOT wrap — use multiple `<text>` lines or `<tspan>`.

## Arrow marker (define once per SVG, reuse)

```html
<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="5" refY="4.5" orient="auto">
  <path d="M0 0L9 4.5L0 9z" fill="#2C3442"/></marker></defs>
<line x1="142" y1="78" x2="184" y2="78" stroke="#2C3442" stroke-width="2" marker-end="url(#ar)"/>
```
Give each SVG its own marker `id` if multiple diagrams share a page (ids are global). Use `--have`
teal markers for "data flows" and `--signal` for the primary path.

## Pattern: staged pipeline (left→right flow)

Rounded-rect stages joined by arrows. One accent for active stages, dashed/ink for inert ones.
Two lanes (e.g. "ingest once" / "per request") with a shared datastore between them reads well.

```html
<rect x="20" y="50" width="120" height="56" rx="10" fill="#151A21" stroke="#FF8A3D"/>
<text x="80" y="76" text-anchor="middle" font-family="'IBM Plex Mono',monospace" font-size="12"
      font-weight="600" fill="#FF8A3D">CHUNK</text>
<text x="80" y="93" text-anchor="middle" font-family="'IBM Plex Sans',sans-serif" font-size="10.5"
      fill="#94A0B2">split up</text>
```
(See the RAG pipeline in AI-Native_Roadmap.html `#focus-rag` for the full two-lane version.)

## Pattern: nested boxes = progressive disclosure / containment / scope

Concentric rounded rects, outermost = broadest/loaded-last, innermost = core/always-on. Outer dashed
muted, inner solid + tinted fill. Add a vertical "cost ↑ / loaded as needed" arrow on the right.
Perfect for: Claude Skill levels, scope/permission layers, context-window framing.
(See `#focus-skills` in the roadmap.)

## Pattern: container / box model (Docker, sandboxing, isolation)

An outer "host" frame containing a horizontal row of isolated boxes sitting on a shared "engine" bar
at the bottom. Optionally a small "blueprint → instance" flow above it (`docker run`). The teaching
point — shared substrate (one OS) vs. per-box isolation — is carried by the layout itself.
(See `#focus-docker` in the roadmap.)

## Pattern: comparison columns (A vs B, before/after, L2 vs L3)

Two or three columns of increasing height (a staircase) or side-by-side panels; highlight the
"target"/"after" column in `--signal` with a top accent bar and a badge. The rising-staircase variant
doubles as a "levels of maturity" visual. (See the L1→L2→L3 staircase at `#start`.)

```html
<rect x="610" y="62" width="258" height="228" rx="11" fill="#17120a" stroke="#FF8A3D" stroke-width="1.6"/>
<rect x="610" y="62" width="258" height="3" rx="1.5" fill="#FF8A3D"/>   <!-- top accent bar -->
<rect x="630" y="232" width="150" height="26" rx="13" fill="#FF8A3D"/>  <!-- badge -->
<text x="705" y="249" text-anchor="middle" font-family="'IBM Plex Mono',monospace" font-size="11.5"
      font-weight="700" fill="#17120a">◀ THE TARGET</text>
```

## Pattern: datastore cylinder (DB / vector store / queue)

```html
<ellipse cx="580" cy="60" rx="62" ry="13" fill="#102a28" stroke="#2BE0CE"/>
<path d="M518 60 V128 A62 13 0 0 0 642 128 V60" fill="#102a28" stroke="#2BE0CE"/>
<ellipse cx="580" cy="60" rx="62" ry="13" fill="#0D1015" stroke="#2BE0CE"/>  <!-- top lid on top -->
<text x="580" y="98" text-anchor="middle" font-family="'IBM Plex Mono',monospace" font-size="12.5"
      font-weight="700" fill="#2BE0CE">Qdrant</text>
```

## Section kicker icons (lucide-style, ~18–19px, stroke=currentColor)

Drop inside a `.kicker`; color follows the section accent via `currentColor`.
`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">…</svg>`

- **layers** (orientation/levels): `<path d="M12 2 2 7l10 5 10-5-10-5Z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>`
- **graduation-cap** (courses): `<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>`
- **sparkles** (skills/AI): `<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .962 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.962 0z"/>`
- **package/box** (docker/containers): `<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>`
- **database/cylinder** (RAG/data): `<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>`

## Checklist before shipping a diagram

- [ ] `viewBox` set, no width/height → responsive.
- [ ] Every label legible at page width; nothing overlaps (verify in a screenshot, not source).
- [ ] The ONE key idea is in `--signal` orange; supporting detail is muted.
- [ ] `role="img"` + `aria-label` describing it in words.
- [ ] Marker ids unique if the page has multiple SVGs.
- [ ] `.figcap` states the takeaway in one sentence (not a restatement of the title).
