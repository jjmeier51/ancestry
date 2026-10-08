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
| `data/additions.json` | People and families the research added beyond the GEDCOM, plus parent corrections (`setParents`) for GEDCOM people. **Generated** by `scripts/import_handoff.py`; later research additions can be appended by hand (ids `H####`, families `HF####`). | script + Claude |
| `data/additions-manual.json` | Hand-maintained additions in the same shape as `additions.json` (people `M####`, `setParents`, families `MF####`). Applied by `build.py` after the generated file. Use this for people added after the handoff (e.g. the owner's brothers). | Claude + owner |
| `data/story-exclusions.json` | Story ids hidden from the site because they are research notes or corrections, not family stories (their text stays in `data/stories.json` and `research/story-notes.md`). | Claude |
| `data/handoff_ids.json` | Stable id map for people created from the handoff. Never edit. | script only |
| `research/imported/` | The owner's uploaded research reports and the 1.3 MB project handoff (Oct 2026). Read-only sources. | owner uploads |
| `research/lines.md`, `sources.md`, `open-questions.md`, `owner-preferences.md` | Reference copies of the handoff's lineage narrative, sources consulted, open questions and the owner's stated preferences. Start research here. | script; Claude appends |
| `data/family.js` | **Generated** bundle the site loads. Never hand-edit. | `scripts/build.py` |

## Owner preferences (from the handoff, keep following them)

1. Uploaded reports and later research override the Ancestry tree where they conflict.
2. Look for standout people: war heroes, celebrities, athletes, politicians; include distant cousins, not only direct ancestors.
3. Highlight ties to **Long Island**, **Northeastern Pennsylvania** and **Virginia**.
4. Fill gaps, add colour (interesting facts), convert probable links to confirmed with records, push the Meier line back, pin every line to specific towns and people.
5. Label every finding with confidence and a source. Living people outside the owner's immediate family are not researched beyond names already in the tree. On 8 Oct 2026 the owner asked for research on his immediate living family (his household, his father's siblings, his mother's brothers): use public records and obituaries only, never people-search sites, and never record addresses or phone numbers.
6. Short questions get short answers.
7. The owner's Google Drive folder of Ancestry screenshots is public: https://drive.google.com/drive/folders/1nLAbzaMlKOSgimj590vLgkfDQMesBRVJ (already downloaded and attached as media).

## Key facts (Oct 2026 state)

- Owner: John Joseph "Johnny" Meier, b. 16 Jun 1992 Alexandria City Hospital, lives in Ashburn VA, id `I282604492552`. Parents Thomas F. Meier (b. 1959) and Sharon M. Petriello (b. 1960). Brothers Thomas Francis "Tommy" Meier Jr. (`M0001`, b. 30 Jul 1990) and Matthew "Matt" Meier (`M0002`, b. 22 Jan 1998), both in Ashburn VA. The owner supplied these details on 8 Oct 2026 and approved showing them. Owner is engaged to Shannon McCarthy (`M0019`); Tommy Jr. is married to Laura (`M0020`), son Luca (`M0021`). Thomas Sr.'s siblings (`M0012`–`M0018`): Kathy, Danny, Jamie, Susie, Nancy, Jack, Terry, all Levittown, years estimated. Maternal grandfather John T. Petriello Sr. died 1 Mar 2025; grandmother Mary Cognetti Petriello living; uncles John Jr. (d. 2024) and Paul.
- A family in `additions-manual.json` may carry `"status": "engaged"` (or `"partner"`); the site labels the couple accordingly.
- Meier line (confirmed to Munzingen, Baden): James C. (1928–2008) → William F. (c.1904–1963) → Henry J. (1866–1940) → Friedrich Mayer (1835–1913) → Heinrich Mayer (c.1796) → Michael Mayer, carpenter. Spelling went Mayer → Meyer/Myer → Meier (first on the 1892 marriage docket).
- Only proven Revolutionary patriot: Ensign Thomas Lamoreaux (SAR P-232580). Bull Smith of Smithtown is a 10th-great-grandfather (`I282608065309`).
- Blood cousins include President Benjamin Harrison (6C5R), First Ladies Anna Symmes Harrison and Julia Gardiner Tyler, Titanic victim James Clinch Smith, NYC Mayor Cornelius Van Wyck Lawrence. See `research/lines.md`.
- Disproven or unproven lines stay in the tree with `unverified` badges and a note: the Sayre/Josiah Topping parents, the Youngs/Horne ancestry of Mary Wells, Bull Smith's "Sir Samuel" parents, the Brewster line, "Captain" Johann C. Doll.
- Open questions and the records that would settle them: `research/open-questions.md`.

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
   - New person found by research: add to `data/additions.json` → `people` (next free `H####` id) and a family in `families` (or a `setParents` entry for a GEDCOM person whose parents were wrong, with `reason`), then write `data/research/<id>.json`.
   - **Do not re-run `scripts/import_handoff.py`** unless the handoff file itself changes: it regenerates the research files of every handoff person (it keeps `media`, `photo` and researchLog entries dated after 2026-10-08, but overwrites other fields).
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

## What counts as a story

The Stories page is for family history: events, anecdotes, traditions, places
and people. Never publish research process as a story ("the tree was wrong
about X", "record Y confirms Z", ruled-out leads). That belongs in
`research/LOG.md`, the person's `researchLog`, or `research/story-notes.md`.
If the owner reports a correction, log it; do not write it up as a story.

A research file with `"manual": true` is hand-maintained (the owner's own
details, for example) and is never overwritten by `import_handoff.py`.

## Conventions

- Dates: ISO `YYYY-MM-DD` when exact, else `YYYY`, `ABT 1890`, `BEF 1900`,
  `BET 1890 AND 1892` (GEDCOM style is accepted).
- Places: most specific first, comma separated (`Rochester, Monroe, New York, USA`).
- Media files: lowercase, hyphenated, descriptive (`1900-census-rochester.jpg`),
  under 2 MB where possible. Portraits: add `--portrait` so they show as the avatar.
- Living people (no death record, born within 105 years) show only a birth
  year on the public site; `scripts/build.py` reduces the date automatically
  (`privacy.livingBirthDates` in `data/site.json`). Full dates may be kept in
  `data/tree.json` and `data/research/` for the owner's records.
- Keep `data/tree.json` untouched by hand; it is regenerated from the GEDCOM.

## Code map

- `index.html` — shell; `css/app.css` — navy theme (tokens at top)
- `js/data.js` — data access, dates, relationship calculator
- `js/app.js` — router (`#/`, `#/tree/<id>`, `#/person/<id>`, `#/people`,
  `#/timeline[/<id>]`, `#/stories[/<id>]`, `#/media`), sheet, search, lightbox
- `js/views/tree.js` — hourglass/ancestor/descendant layout, pan, pinch, inertia
- `js/views/profile.js` — person page sections
- `scripts/` — `import_gedcom.py`, `build.py`, `attach_media.py`, `import_handoff.py` (one-off merge of the project handoff), `attach_drive_screenshots.py` (one-off)

Test locally: `python3 -m http.server 8000` then open http://localhost:8000.
Run `python3 scripts/build.py --check` before committing.
