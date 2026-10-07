# Meier Family Tree — project memory

This repository is the persistent memory for the family-history project. Read
this file first in every session. Everything learned through research must be
written into the files described below **and** reflected on the website, never
only in chat.

## What this is

A static, dependency-free family-tree website (HTML/CSS/JS, hash-routed SPA)
deployed on Vercel at **meiertree.com**. The homepage is the interactive tree.
The owner is J.J. Meier (jjmeier51@gmail.com); their person id is in
`data/site.json` → `owner` / `rootPerson`.

## Where data lives (source of truth)

| File | Purpose | Who edits |
| --- | --- | --- |
| `data/source/*.ged` | The owner's GEDCOM export(s) from Ancestry | owner uploads; never edit |
| `data/tree.json` | Core tree: people, families, vital events, residences, notes. **Generated** from the GEDCOM by `scripts/import_gedcom.py`. | script only |
| `data/research/<personId>.json` | Everything learned by research for one person (see schema below). Survives GEDCOM re-imports. | Claude + owner |
| `data/stories.json` | Long-form family stories | Claude + owner |
| `data/site.json` | Title, root/owner person, confidence-level definitions | owner |
| `media/<personId>/` | Photos, documents, records attached to that person | `scripts/attach_media.py` |
| `research/LOG.md` | Chronological research log (what was searched, found, ruled out, next steps) | Claude, every session |
| `research/people/<personId>.md` | Optional long-form research notes per person (evidence, reasoning, open questions) | Claude |
| `data/family.js` | **Generated** bundle the site loads. Never hand-edit. | `scripts/build.py` |

## Standard workflow for a research session

1. `git pull`, read `research/LOG.md` (latest entries) and this file.
2. Do the research the owner asks for.
3. Record findings:
   - facts, confidence, residences, military, fun facts, sources, research log →
     `data/research/<id>.json`
   - files found (census images, records, photos, newspaper clippings) →
     `python3 scripts/attach_media.py <id> <file> --title ... --date ... --type record --source ...`
   - links to online records → `attach_media.py <id> --url ... --type link`
   - narrative → `data/stories.json` or `research/people/<id>.md`
   - a dated entry in `research/LOG.md`
4. `python3 scripts/build.py` (validates and regenerates `data/family.js`).
5. Commit with a descriptive message and push. Vercel deploys automatically.

If the owner provides a new GEDCOM: copy it to `data/source/`, run
`python3 scripts/import_gedcom.py data/source/<file>.ged`, then `build.py`.
Person ids come from the GEDCOM (`I123`); keep them stable so research files
keep matching. If Ancestry renumbers ids on export, map old→new ids before
replacing `tree.json` and rename the research files accordingly.

## Research file schema (`data/research/<id>.json`)

```json
{
  "id": "I12",
  "link": { "confidence": "confirmed|probable|possible|unverified", "note": "why" },
  "tags": ["military", "immigrant", "artist", "athlete", "notable", "clergy", "politician", "author", "pioneer"],
  "summary": "One-sentence summary shown at the top of the profile.",
  "bio": "Longer narrative. Blank lines separate paragraphs.",
  "photo": "media/I12/portrait.jpg",
  "funFacts": ["..."],
  "residences": [{ "date": "1900–1910", "place": "Rochester, New York", "note": "optional" }],
  "military": [{ "branch": "US Army", "service": "1917–1919", "rank": "", "unit": "", "theatre": "", "note": "" }],
  "notable": "Why this person is noteworthy (famous, awards, public roles).",
  "events": [{ "title": "Naturalized", "date": "1905", "place": "", "description": "" }],
  "facts": [{ "label": "Religion", "value": "Lutheran" }],
  "media": [{ "file": "media/I12/1900-census.jpg", "type": "record", "title": "1900 US Census", "date": "1900", "source": "FamilySearch", "note": "", "people": ["I13"] }],
  "sources": ["Citation or URL", "..."],
  "researchLog": [{ "date": "2026-10-07", "note": "Found 1900 census; confirms parents." }]
}
```
Any key here overlays the same key on the person from `tree.json`.

## Confidence scale (link to the owner)

- **confirmed** — documented by primary records (birth/marriage/death, census
  chain, DNA match) all the way to the owner.
- **probable** — strong secondary evidence; one more record would confirm.
- **possible** — a reasonable guess from indirect evidence; flag clearly.
- **unverified** — nothing beyond the imported tree yet (default).

Change confidence only with a sources entry and a researchLog note explaining
why.

## Conventions

- Dates: ISO `YYYY-MM-DD` when exact, else `YYYY`, `ABT 1890`, `BEF 1900`,
  `BET 1890 AND 1892` (GEDCOM style is accepted).
- Places: most specific first, comma separated (`Rochester, Monroe, New York, USA`).
- Media files: lowercase, hyphenated, descriptive (`1900-census-rochester.jpg`),
  under 2 MB where possible. Portraits: add `--portrait` so they show as the avatar.
- Never put living people's exact birth dates in the public site without the
  owner's okay; the site is public at meiertree.com.
- Keep `data/tree.json` untouched by hand; it is regenerated from the GEDCOM.

## Code map

- `index.html` — shell; `css/app.css` — navy theme (tokens at top)
- `js/data.js` — data access, dates, relationship calculator
- `js/app.js` — router (`#/`, `#/tree/<id>`, `#/person/<id>`, `#/people`,
  `#/timeline[/<id>]`, `#/stories[/<id>]`, `#/media`), sheet, search, lightbox
- `js/views/tree.js` — hourglass/ancestor/descendant layout, pan, pinch, inertia
- `js/views/profile.js` — person page sections
- `scripts/` — `import_gedcom.py`, `build.py`, `attach_media.py`

Test locally: `python3 -m http.server 8000` then open http://localhost:8000.
Run `python3 scripts/build.py --check` before committing.
