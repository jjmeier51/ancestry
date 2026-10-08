# Research brief (copied from John's request, 2026-10-08) + run conventions

## Run conventions (added by the coordinating session)
- Roster: `meiertree_roster.json` was NOT attached, so the roster was derived from the live site data
  `https://www.meiertree.com/data/family.js` (downloaded 2026-10-08, 899 people). Derived roster:
  `_work/roster_derived.json`. Tiers: 1 = direct ancestors (352), 2 = spouses/children of direct
  ancestors incl. ancestors' siblings (191), 3 = everyone else (330), skip = presumed living (26).
- Each worker gets a worklist `_work/worklists/<group>.json`: an array of `{roster, siteRecord}` in
  priority order. `siteRecord` is the person's full site record (bio, sources, researchLog,
  openQuestions, facts, media...). Read it before searching so you never re-report known facts/URLs.
- Each worker writes:
  - `research_output/people/<personId>.json` (one per finished person, schema below), written as soon as
    the person is done.
  - `research_output/_work/<group>/progress.json`:
    `{ "lastUpdated": "...", "completed": [...], "inProgress": "...", "livingDetected": [...], "remaining": N }`
    updated after EVERY person (this is how a later session resumes).
  - `research_output/_work/<group>/new_people.json`, `stories.json`, `leads.json` (arrays, formats below).
  - downloaded public-domain/CC media under `research_output/media/<personId>/`.
- NEW person IDs: each group has its own block so IDs never collide (e.g. NEW-101..NEW-199).
- The coordinating session merges the per-group files into `progress.json`, `new_people.json`,
  `stories.json`, `leads.json`, `media_manifest.csv` and writes `SUMMARY.md`.

---

## Scope
Tiers in order; within a tier, open questions and `possible`/`unverified` confidence first (worklists are
already sorted that way). Do not research `skip` (presumed living) people.

**Living-person rule.** If anyone turns out to be alive (e.g. appears as a survivor in a recent obituary),
stop, mark them `living_detected`, record only the evidence that they're living. Never record addresses,
phone numbers, emails or other contact details of living people. Never record DNA-match data.

**Time box.** Roughly 10–20 min of searching per tier-1 person, less for tiers 2–3. If nothing new after a
reasonable pass, log what you searched (`searchedNoResult`) and move on. Negative results must be recorded.

Spelling variants everywhere (Meier/Meyer/Mayer/Maier, Lamoreaux/Lamoreux/Lamoureux, Croup/Croop,
Petriello/Petrillo, Gianetta/Giannetta, McGuire/Mcguire). Search all of them.
Also look for NEW people, especially famous or noteworthy relatives.

## Where to look
- Indexes/trees (leads, not proof): FamilySearch, WikiTree, Geni, Find a Grave, BillionGraves, Interment.net.
- Census/vital/immigration: FamilySearch collections; NARA catalog; PA State Archives (death certificates
  1906–1975 index, Civil War Veterans' Card File); Ellis Island / Castle Garden / Steve Morse; Germans/Italians
  to America; naturalizations.
- Newspapers: Chronicling America, Fulton History, Google News Archive, PA newspaper archives,
  Wilkes-Barre and Scranton papers; Legacy.com and funeral homes for 20th-c obituaries.
- Books: Internet Archive, Google Books, HathiTrust (Bradsby 1893, Harvey Book, Pelletreau 1898, Southold
  records, Long Island and Wyoming Valley genealogies, county and church histories).
- Volunteer sites: PAGenWeb (Luzerne, Lackawanna), USGenWeb, NYGenWeb (Suffolk), PA-Roots, historical societies.
- Overseas: Antenati; irishgenealogy.ie, NLI parish registers; Archion, Landesarchiv Baden-Württemberg,
  Erzbistum Freiburg church books.
- Military/lineage: Fold3 indexes, DAR GRS, SAR, Rev War pension indexes, WWI/WWII drafts.
- Notables: Wikipedia, Wikimedia Commons, LOC, Find a Grave famous, historical societies.
- Paywalled (Ancestry, Newspapers.com, Fold3 images, MyHeritage): if you see an index entry/snippet but not
  the record, report it as a LEAD (exact collection, search terms, what the snippet shows). A snippet is not a fact.

### Access notes from earlier rounds (Oct 2026)
- WORKS: FamilySearch published-tree JSON `https://www.familysearch.org/service/tree/tree-data/published/persons/{PID}`
  (includes relatives and attached sources; attached record images at
  `https://ancestors.familysearch.org/service/tree/tree-data/published/sources/{PID}/images/i/{n}/image.jpg`;
  US images come through, Irish parish images are empty). FamilySearch ark record pages `familysearch.org/ark:/61903/1:1:XXXX` may 401.
- WORKS: PA death index PDFs (1906–1970s) at `https://www.phmc.state.pa.us/bah/dam/rg/di/r11_090_DeathIndexes/Death_YYYY/...pdf`.
- WORKS: archive.org (advancedsearch API, full text `/stream/<id>/<id>_djvu.txt`), WikiTree API (`api.wikitree.com`),
  Landesarchiv BW free "plink" images, Wikipedia. Google Books/Wikimedia may rate-limit (429): back off.
- BLOCKED (403/Cloudflare): Ancestry, Find a Grave, BillionGraves, FamilySearch record search, Antenati,
  irishgenealogy.ie, registers.nli.ie, HathiTrust full-text search, Geni. Try once via WebFetch/WebSearch; if
  blocked, note it and move on. WebSearch snippets of blocked pages are leads only.
- Chronicling America moved to loc.gov; try `https://www.loc.gov/collections/chronicling-america/?q=...&fo=json`.

## Evidence rules
1. Never invent a URL, citation, page number or record detail. Every URL must be one you actually loaded.
   If a page is blocked, say so; don't guess its contents.
2. Identity: never attach a record on name alone. Require >= 2 independent matching identifiers (name plus
   spouse, parents, birth year within ~2 yrs, place, children). Plausible-but-unproven = candidate, with reasoning.
3. Classify each source: `primary`, `secondary`, `derivative` (index/transcription/user tree). Trees/indexes are leads.
4. Conflicts with the site: never silently overwrite. Record both values, source for each, and your assessment.
5. Confidence: may recommend raise/lower with specific evidence. Definitions: confirmed = link to John documented
   by primary records; probable = strong secondary evidence, one more record would confirm; possible = reasonable
   guess from indirect evidence; unverified = no research beyond the imported tree.
6. Quote sparingly; paraphrase. Short transcriptions of a key record line are fine.
7. Record the access date (2026-10-08 etc.) for every URL.

## Media
For EVERY photo, document, record image, gravestone, clipping, map, book page found (even if not downloadable):
`type` (photo|portrait|gravestone|record|document|newspaper|book|map|link), `title` (short specific caption),
`date` (of the item), `pageUrl`, `directUrl`, `repository`, `rights` (public_domain|cc (+license)|copyrighted|paywalled|unknown),
`downloadable` (true only if public_domain or reuse-permitting CC), `downloaded` (bool), `localPath`,
`people` (roster IDs), `suggestedFile` (`media/<personId>/<short-slug>.<ext>`), `note`.
Download ONLY `downloadable: true` items, to `research_output/media/<personId>/` with the suggestedFile name.
(US works published before 1931, US government works, explicit PD = public_domain. Most Find a Grave photos
and modern obituaries = copyrighted. FamilySearch record images: treat rights as `unknown` unless the item is a
pre-1931 US government record, in which case public_domain is reasonable; say why in `note`.)

## people/<personId>.json schema (keep ONLY new or changed info; omit empty sections)
```json
{
  "id": "I282608053685",
  "name": "Andrew G. Pringle",
  "researchedAt": "2026-10-08",
  "status": "researched | nothing_new | living_detected | blocked",
  "updates": {
    "birth":  { "date": "", "place": "", "sourceRefs": ["S1"] },
    "death":  { "date": "", "place": "", "sourceRefs": [] },
    "burial": { "place": "", "cemetery": "", "sourceRefs": [] },
    "aka": [],
    "occupation": "",
    "residences": [ { "date": "", "place": "", "note": "", "sourceRefs": [] } ],
    "events":     [ { "title": "", "date": "", "place": "", "description": "", "sourceRefs": [] } ],
    "military":   [ { "note": "", "sourceRefs": [] } ],
    "facts":      [ { "label": "FamilySearch ID", "value": "" } ]
  },
  "bioAdditions": "1–3 paragraphs of new narrative, plain prose, citing sources inline by ref (S1, S2).",
  "funFacts": [],
  "conflicts": [ { "field": "birth.date", "siteValue": "", "foundValue": "", "sourceRefs": [], "assessment": "" } ],
  "relationships": [ { "type": "parent | spouse | child | sibling", "personId": "or NEW-101", "evidence": "", "sourceRefs": [], "strength": "proven | probable | candidate" } ],
  "confidenceRecommendation": { "current": "probable", "recommended": "confirmed", "justification": "" },
  "openQuestionsResolved": [ { "question": "exact text from roster", "answer": "", "sourceRefs": [] } ],
  "openQuestionsNew": [],
  "sources": [ { "ref": "S1", "citation": "", "url": "https://...", "class": "primary | secondary | derivative", "accessed": "2026-10-08", "supports": "" } ],
  "media": [ { "...": "fields from Media section" } ],
  "searchedNoResult": [ "Find a Grave: Andrew Pringle, d. 1900, Luzerne Co. (no match)" ],
  "researchLogEntry": "One sentence, e.g. 'Round 4: found 1860 census tying Andrew to Catherine Scott; Find a Grave negative.'"
}
```
Every person in the worklist that you work on gets a file, including `nothing_new` (then: status, searchedNoResult,
researchLogEntry). `living_detected` files contain only id, name, status, the living evidence and its source.

## Group files
- `new_people.json`: array of relatives not in the tree, deceased only, with real evidence. Each: `id` (your NEW block),
  same fields as the person schema where known, plus `relationships` tying them to an existing roster ID.
- `stories.json`: array of `{ "title", "date", "people": [ids], "body": "a few paragraphs, paraphrased", "sourceRefs": [full source objects] }`.
- `leads.json`: array of `{ "personId", "collection", "site", "searchTerms", "whatTheSnippetShows", "whyItMatters" }`.
