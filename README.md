# Meier Family Tree · meiertree.com

A fast, modern, mobile-first family-tree website. Plain HTML/CSS/JS with no
build tooling: the whole site is static files, so it runs from a folder or from
Vercel. The homepage is the interactive tree.

## Features

- **Tree homepage**: hourglass view (ancestors above, descendants below) of any
  person, plus ancestors-only and descendants-only modes. Drag to pan, pinch or
  scroll to zoom, double-tap to zoom in, tap `+` to reveal more generations.
  Tap a person for a sheet with *View profile*, *View their tree* and quick
  jumps to parents, spouse and children.
- **Profiles**: dates, places lived, family, military service, noteworthy
  facts, fun facts, stories, media and documents, sources, research log, and a
  confidence badge showing how solid the link to you is
  (confirmed / probable / possible / unverified). Includes a relationship
  calculator ("James is the grandfather of Emily").
- **People** directory with filters by surname, confidence and tags (military,
  immigrant, artist, …). **Timeline** by decade. **Stories**. **Media** gallery.
- Global search (`/` or ⌘K on desktop, magnifier on mobile).
- Dark navy theme, iPhone-optimised layout with bottom tabs, safe-area support,
  and "Add to Home Screen" support.

## Data

```
data/source/        your GEDCOM export(s)               → never edited
data/tree.json      core tree, generated from the GEDCOM → scripts/import_gedcom.py
data/research/*.json  research per person (bio, facts, media, confidence…)
data/stories.json   long-form stories
data/site.json      title, root person, confidence definitions
media/<id>/         photos and documents per person
data/family.js      GENERATED bundle the site loads       → scripts/build.py
```

### Import your GEDCOM

```sh
cp ~/Downloads/export.ged data/source/
python3 scripts/import_gedcom.py data/source/export.ged
python3 scripts/build.py
```

### Attach a photo or document to a person

```sh
python3 scripts/attach_media.py I12 ~/Downloads/1900-census.jpg \
  --title "1900 US Census, Rochester NY" --date 1900 --type record --source FamilySearch
python3 scripts/attach_media.py I12 portrait.jpg --portrait
python3 scripts/attach_media.py I12 --url https://www.findagrave.com/memorial/123 --type link --title "Find a Grave"
```

The script copies the file into `media/<id>/`, records it in
`data/research/<id>.json`, and rebuilds.

### Edit research by hand

Open `data/research/<id>.json` (schema in `CLAUDE.md`), then run
`python3 scripts/build.py`.

## Run locally

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy on Vercel + meiertree.com

1. Push this repo to GitHub (done).
2. In Vercel: **Add New → Project → Import** the `ancestry` repository.
   Framework preset: **Other**. Build command: *(leave empty)*. Output
   directory: *(leave empty, the repo root is the site)*. Deploy.
3. In the Vercel project: **Settings → Domains → Add** `meiertree.com` and
   `www.meiertree.com`. Vercel shows the DNS records to add at your registrar:
   an `A` record for `@` pointing to `76.76.21.21` and a `CNAME` for `www`
   pointing to `cname.vercel-dns.com` (use the exact values Vercel displays).
4. Every push to `main` deploys automatically; other branches get preview URLs.

`vercel.json` sets caching for `media/` and `images/` and basic security
headers. `.vercelignore` keeps source data and scripts out of the deployment
(only the generated `data/family.js` ships).

## Project memory

`CLAUDE.md` documents the workflow for research sessions and `research/LOG.md`
is the running log, so new findings are written into the repository and the
site in the same step.
