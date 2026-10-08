# Research log

Newest entries at the top. Every research session adds an entry: date, what
was asked, what was searched, what was found (with sources), what was ruled
out, and next steps. Person ids refer to `data/tree.json`.

## 2026-10-08 — Living family: Petriello side documented, Meier side blocked

- Owner asked (8 Oct 2026) for research on his immediate living family:
  his own household, Thomas F. Meier Sr.'s family and his seven brothers and
  one sister from Levittown, and Sharon (Petriello) Meier's two brothers.
  Rule applied: public records and obituaries only; no people-search sites,
  no addresses or phone numbers; living people show birth years only.
- **Found:** John T. "Johnny" Petriello Sr. (Sharon's father) died 1 Mar
  2025 in Scranton, aged 92 (b. 19 May 1932, not 1933 as the tree had).
  His obituary (Solfanelli-Fiorillo Funeral Home) gives: US Air Force staff
  sergeant, Korean War; Tobyhanna Army Depot staffing specialist and
  handicapped-hiring program manager; 14 years Director of Personnel at
  Lackawanna College; wife Mary Cognetti Petriello living; children John Jr.
  (d. 2024), Sharon (Tommy Meier) and Paul (Rebecca); grandchildren incl.
  "Tommy (Laura), Johnny (Shannon) & Mathew" Meier; great-grandchild Luca
  Meier; siblings Ann Marie Genello and Jim Petriello (MaryEllen). Buried
  Cathedral Cemetery, Scranton. Text in research/people/I282695503435-obituary-2025.txt.
- **Found:** John T. Petriello Jr. (b. 29 Dec 1958 Scranton, d. 29 Feb 2024
  Skillman NJ), Merrill Lynch financial advisor 30 years, Mendham then
  Princeton; wife Joanne (38 years), children Marissa Westlake (Zachary),
  John (Samantha), James (Emily). Text in research/people/H0348-obituary-2024.txt.
- Mary Cognetti Petriello: living as of Mar 2025; aged 83 in Nov 2016
  (Cognetti Thanksgiving article); named in brothers Anthony (2008), Joseph
  (2009) and Leo (2019) Cognetti obituaries.
- Added to `data/additions-manual.json`: Ann Marie Genello and Jim Petriello
  (John Sr.'s siblings), Joanne Petriello and children Marissa Westlake, John
  and James, Rebecca Petriello and children Jack and Mollie. Source links
  attached to the people concerned.
- **Not found:** James C. Meier's Aug 2008 obituary (Bucks County Courier
  Times) and therefore the names of Thomas Sr.'s eight siblings. It is
  indexed only in paywalled archives (GenealogyBank/NewsBank, obitsarchive).
  Legacy.com, Dignity, Patch, Find a Grave (blocked) and FamilySearch gave
  nothing. Leads: Courier Times obituaries for Mary R. Meier (26 Nov 2003),
  Kathleen T. Meier (15 Aug 2006) and Fred Meier (15 Jul 2012), all
  Levittown. Kathryn (McGuire) Meier's Sept 1970 death notice (Times Leader)
  likewise not online for free.
- **Ask the owner:** names of his father's siblings (or a copy of James C.
  Meier's 2008 obituary); whether Shannon and Laura should be added as
  spouses/partners; whose son Luca is.

## 2026-10-08 — Owner's family details; story clean-up; phone crash fix

- Owner's statement (8 Oct 2026): full name John Joseph Meier, born 16 Jun
  1992 at Alexandria City Hospital, Alexandria VA, now living in Ashburn VA.
  Brothers added (`data/additions-manual.json`): Thomas Francis "Tommy"
  Meier Jr., b. 30 Jul 1990 Alexandria City Hospital; Matthew "Matt" Meier,
  b. 22 Jan 1998 Inova Loudoun Hospital, Ashburn VA. Both live in Ashburn.
- 22 imported "stories" that were research notes or corrections moved off
  the site (`data/story-exclusions.json`, text in `research/story-notes.md`).
  Rule recorded in CLAUDE.md: research process is never published as a story.
- Site: Stories and Timeline now render incrementally and content cards no
  longer use backdrop blur, after iOS Safari crashed ("A problem repeatedly
  occurred") on those pages.

## 2026-10-08 — Project handoff merged (861 people on the site)

- Imported the owner's three lineage reports and the 1.3 MB project handoff
  (`research/imported/`). The handoff's 586 person records were merged by
  `scripts/import_handoff.py`: 200 matched GEDCOM people (research names,
  dates, bios, residences, military, sources and open questions now overlay
  them), 386 new people and 205 new families were added in
  `data/additions.json`, and 28 parent links of GEDCOM people were corrected
  (each profile shows "Corrected from the Ancestry tree" with the reason).
  Confidence now: see the People page filter; everyone the research touched
  carries the handoff's label.
- Notable corrections applied: Jerusha Topping's parents are Elnathan Topping
  and Mary (not Josiah Topping and Hannah Sayre); James Smith's father is Job
  Smith (not "Justice Adam Smith"); Thomas Heffernan's parents are Humphrey
  Heffernan and Anastasia Ryan of Co. Tipperary (Patrick Heffernan/Neagle
  removed from the line); Kathryn McGuire's parents are Francis J. McGuire and
  Elizabeth McAvoy; James McGuire's parents are Edward McGuire and Mary Jane
  Gaffney; Mollie Petriello is Carmela Gianetta; John Tuthill's mother is
  Rachel Browne; Grazia Di Marino's mother is Caterina di Leo; Giovanni
  Cognetta's mother is Mariangela Cannatello; Carmine Fiorillo's mother is
  Vittoria Marrelli. Replaced tree parents remain in the tree, unverified.
- 158 stories from the handoff are on the Stories page (`data/stories.json`),
  with sources.
- Downloaded the 50 Ancestry screenshots from the owner's Drive folder,
  converted to JPEG and attached: census record and page to Andrew G. Pringle;
  Pelletreau and F. K. Smith book pages to Bull Smith; tree screenshots to the
  people whose branch they show; descent charts to the owner.
- Reference copies: `research/lines.md`, `research/sources.md`,
  `research/open-questions.md`, `research/owner-preferences.md`.
- Still to do: the handoff's media on Ancestry (104 items) are not downloaded;
  Munzingen parish books, PA death certificates and the other records in
  `research/open-questions.md` remain the next research targets.

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
