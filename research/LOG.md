# Research log

Newest entries at the top. Every research session adds an entry: date, what
was asked, what was searched, what was found (with sources), what was ruled
out, and next steps. Person ids refer to `data/tree.json`.

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
