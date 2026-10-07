# Research log

Newest entries at the top. Every research session adds an entry: date, what
was asked, what was searched, what was found (with sources), what was ruled
out, and next steps. Person ids refer to `data/tree.json`.

## 2026-10-07 — GEDCOM imported (349 people, 177 families)

- Imported `data/source/Meier_Family_Tree.ged` (Ancestry export of "Meier
  Family Tree", 7 Oct 2026). Owner/root set to Johnny Meier (I282604492552),
  b. 1992 Alexandria VA; parents Thomas Francis Meier and Sharon Maria
  Petriello. 301 ancestors are linked; earliest births around 1475–1500
  (Younges/Young, Gooch, Maloy/Morton lines).
- Captured from the GEDCOM per person: vital events, residences (35 people),
  159 record citations (75 people), two WWII draft registrations (tagged
  `military`), arrival/naturalization/probate events, and the titles of 104
  media items attached in Ancestry (91 people). The export contains no media
  files; those must come from the owner's Google Drive.
- Confidence: everyone is `unverified` except the owner (`confirmed`). The
  owner should tell us which lines are documented so they can be upgraded.
- Data quirks to clean up later: 13 people have no sex recorded (owner fixed by
  hand); some Ancestry names carry slashes/alternates (e.g. "Jane\Jena Maloy
  \Morton (Horne)"); surname casing varies (Mcguire/McGuire, BEGELSPACHER);
  one "Arrival" event has the junk date "True Love".
- Next: attach Drive media with `scripts/attach_media.py`; ask the owner for
  known family stories; research the main surnames (Meier, Petriello,
  Cognetti, Colosimo, Ferlaino, McGuire, Moraca, Fiorillo, Pringle).

## 2026-10-07 — Site built, awaiting GEDCOM

- Built the website and data pipeline. The tree currently shows a fictional
  sample family (`data/tree.json` has `"sample": true`).
- Waiting on: the owner's GEDCOM export (to `data/source/`) and a Google Drive
  of media and documents to attach per person.
- Next steps once the GEDCOM arrives:
  1. `python3 scripts/import_gedcom.py data/source/<file>.ged`
  2. Set `rootPerson`/`owner` in `data/site.json` to the owner's id; set
     `sample` to false (the importer does this).
  3. Mark the owner's direct documented line as `confirmed` and everyone else
     `unverified` until researched.
  4. Attach media from the Drive with `scripts/attach_media.py`.
  5. `python3 scripts/build.py`, commit, push.
