# Research log

Newest entries at the top. Every research session adds an entry: date, what
was asked, what was searched, what was found (with sources), what was ruled
out, and next steps. Person ids refer to `data/tree.json`.

## 2026-10-08 — Kathy, Nancy and Terry Meier: John's leads; Anthony Russo Jr.

- John supplied: Kathy m. Richard "Rick" McGinley, near Doylestown, children
  Ryan, Daniel, Kate (`M0107`–`M0109`); Nancy and Tony Russo in Doylestown,
  son Anthony Jr. the Archbishop Wood/Temple/Michigan State QB; Terry
  (Theresa) in Yardley, divorced, children Kaysie, Rylie, Bobby Borgman
  (`M0110`–`M0112`); Kathryn McGuire Meier died of breast cancer in 1970.
- Public confirmation of the Russo–Meier link: Temple's 2020 roster bio of
  Anthony Russo names parents Nancy and Tony Russo, sisters Chelsea (26),
  Emily (23) and Gina (18), and "uncle Dan Meier, played football at North
  Carolina State"; MSU's 2021 bio repeats parents and uncle. Wikipedia gives
  his birth 6 Dec 1997, Doylestown. Full athletic bio written for `M0032`
  (Catholic League record 35 TD 2015; Temple 2016–20, school completions
  records; MSU 2021; XFL/IFL 2023, third-team All-IFL). Sisters' birth
  years estimated from the bio ages.
- Still nothing public for Kathy/Rick McGinley or Terry Borgman (Doylestown,
  Yardley and Bucks County searches with the new surnames; one name check on
  "Kaysie Borgman"); nothing for Susan and Jack. Exact birth dates of the
  eight siblings are not in public records online; only data-broker sites
  carry them and those are not used. Lead unchanged: James C. Meier's Aug
  2008 Courier Times obituary (Newspapers.com/GenealogyBank).

## 2026-10-08 — Susan, Nancy, Jack and Terry Meier (third pass); Research status moved; date-parser bug

- John asked for more on his father's siblings Susan, Nancy, Jack and Terry
  (`M0015`–`M0018`). Searched again (see each researchLog): Legacy.com,
  Patch/Dignity Levittown lists, in-law family obituaries (Borgman, Russo,
  McGinley), every public profile of Danny Meier, the ESU lettermen list,
  Neshaminy archives. Nothing public exists for them online; the 2008
  Courier Times obituary of James C. Meier (Newspapers.com/GenealogyBank)
  is still the one record that would give married names and towns. Family
  information from John is the practical route.
- Bonus from the ESU media guide text: Thomas Sr.'s 1980 line (45-71, 521
  yds, 3 TD; 7 TD/42 pts; two rushing TDs vs Bloomsburg; 58- and 55-yard
  catches) added to `I282604492836`. Jack Meier did not letter at ESU.
- Site: the Research status card now sits at the very bottom of every
  profile, full width (`profile-foot`), after Family and the relationship
  calculator.
- Bug fixed: dates written `1974-75` were parsed as month 75 and crashed the
  profile (Danny Meier's page rendered only About and Life; the error was
  swallowed by the view transition). `parseDate` now treats them as a
  two-year span, months/days are range-checked, and the router logs and
  shows a notice when a view throws. All profiles smoke-tested.

## 2026-10-08 — Round 6 (Cognetti line) imported

- John uploaded a sixth overnight run on the Cognetti line (24 existing people,
  10 new relatives, 4 stories, 16 leads, 11 media items, 4 manifest/draft-card
  images), archived under `research/imported/round6/` and merged with
  `ROUND=round6 scripts/import_round4.py` (24 files; new ids `M0097`–`M0106`
  in `_work/new_ids.json`). The importer now labels its notes by round
  (`LABEL`, `RTAG`) instead of "Round 4" everywhere.
- Fixes on top of the import: the run's Joseph Notarianni and Michelina
  Carabia duplicated `M0089`/`M0088` from round 5 (dates and licence folded
  into them, `PRESET_IDS` set so a re-run is idempotent); a childless
  duplicate Forgione couple family dropped; three confidence values that the
  run wrote as prose reset to the scale; `I282695503588` ("Ralph abt 1913")
  merged into Ralph Anthony Cognetti; the six children's bios corrected from
  "great-granduncle/aunt" to great-uncle/aunt and Mary Cognetti Petriello
  from great-grandmother to grandmother (she is John's grandmother).
- Findings now in the About texts: the Dasà Cognettas went to Stamford CT
  (1905 Francesco, 17, to brother Nicola; 1910 Nicola, 23, "father Giovanni,
  Dasa", to brother Francesco, Branch St) — a candidate for Frank's arrival,
  kept at probable; Giovanni's "Nicasetro" death place unsupported; the
  Nicastro Cognetto family (H0381/H0513) documented from the 1917 draft card
  and kept separate; marriage licences for Marguerite Forgione (1940) and
  Elizabeth Notarianni (1943), both now confirmed; Leo (Korean War, 34 years
  IBM, wife Jean Rossi 1932–2023), Joseph F. (lumber salesman 1937, D.C.
  Sales 1956, Lou Spector Award 1961, wife Domenica "Aunt Min"), Anthony R.
  (State Workmen's Insurance Fund director, Workmen's Compensation Appeal
  Board), Ralph (Royal Bottling 1940, no WWII service), Angeline (m.
  Nicholas Butchko, d. 2009), Helen (married at 16, 612 Philo St); all eight
  children lived to adulthood (Leo's obituary; no child deaths 1913–40).
- Two stories trimmed of research-process wording (S197 last paragraph,
  S200 priest's surname). Leads: `research/leads-round6.md` (Frank's WWI
  card, 1942 registration and naturalization; 1910 Stamford census; PA death
  certificates incl. Helen 1965; Dasà civil records; full obituaries).
- For John to decide: adding Ralph's daughter Helen (b. c.1941, 1950 census;
  possibly living) as a person; Frank's arrival 1905 vs 1907/08 and birth
  c.1888 vs 1890–92 (unchanged); Anthony R.'s colleges (Keystone/Penn State
  vs Penn State/Scranton); Joseph F.'s death place (hospice in Scranton while
  living at Moosic; the bio says both).

## 2026-10-08 — Tommy Jr. and Matt accolades; View As mode; tighter tree

- Tommy Jr. (`M0001`): Broad Run football 2006–07 (MaxPreps), first-team
  All-Dulles District catcher 2008 (school coaching page), UVA Wise rosters
  2009-10/2011-12, UVA Wise record book (2012: 50 starts tied record, .992
  fielding, 238 PO, 266 TC, 185 AB, 69 H, 11-14 SB; 2011: 8 SH), 2021 state
  title coverage; All-MSC 2012/2013 and 2012 Gold Glove only from his own
  public profile (flagged as reported).
- Matt (`M0002`): Frostburg State bio (No. 51, 2016–19 season lines, 330 HS
  tackles, captain, Ron E. Pyles award, parents named), VHSL 2015 Group 5A
  defensive second-team all-state (WRIC release), WUSA9 2015 feature.
- Site: "View as" chooser on first visit (Johnny, Tommy Jr., Matt, Sharon,
  Tommy Sr.; `viewAs`/`viewAsLabels` in `data/site.json`), remembered in
  localStorage for an hour; the tree roots at the viewer and every
  relationship sentence is from their point of view; "Viewing as" chip in the
  tree HUD reopens it. Tree spacing tightened (node 180px, sibling gap 12,
  couple gap 14).

## 2026-10-08 — Round 5 (living members) imported

- John supplied a second overnight run covering the 52 living or presumed
  living people (archived under `research/imported/round5/`). Imported with
  `ROUND=round5 scripts/import_round4.py`: 49 files applied, 30 note blocks
  added to `researchNotes` (not to the About), 14 conflicts, 8 confidence
  changes, 47 public links (news, rosters, school pages, obituaries), 2
  files, 18 new relatives `M0079`–`M0096` (Cognetti, Ruth, Notarianni,
  Arnold and Genello families; three Petriello in-law siblings skipped
  because their parents are not in the tree), 8 stories.
- Five "living" people were dead or duplicates: Elizabeth "Betsy" McGuire
  (`H0062`, d. 8 Nov 2016 Altoona), Nancy Stahl Meier (`H0384`, d. 13 May
  2009), John F. Cognetti (`I282695503584`, d. 8 Nov 2013), Mary Carol Ruth
  (`H0500`, d. 24 Dec 1978); "Levyso" Cognetti merged into Leo S. (`H0346`).
  Also merged: Ann Marie Petriello → `M0003`, "James Jr." → `M0004`.
  Harold E. Arnold (`H0383`, 1927–1997) was Betsy's husband, not her
  mother's second husband: family HF0001 re-pointed.
- Privacy as in the summary: no addresses, phones, full birth dates of
  living people, data-broker sites or anything on minors beyond names.
- Left for John: delete the unlinked Cassie Hayes (`I282625149693`); whether
  he and Shannon married on 12 Sep 2025 (a deleted wedding page suggested
  so; site still says engaged); Tim Meier's West Point class year; the
  unconfirmed Paul Petriello (golf coach), Laura De Santis (teacher) and
  Sal Cognetti Jr. candidates; Nancy Holland's death date (1 Apr vs 4 Jan
  2007). Leads: `research/leads-round5.md`.
- The 46 profiles round 5 touched were sent for the same narrative rewrite
  as the rest (notes folded into the About; detail stays in Evidence notes).

## 2026-10-08 — About texts rewritten as narrative

- John: the About sections read like pasted research notes (record ids,
  census sheet numbers, "Round 1" remarks). All 703 biographies were
  rewritten as plain narrative (14 parallel batches, instructions in the
  session scratchpad: facts only from the existing text, no identifiers,
  no research-process language, hedges kept, living people unchanged in
  substance). Summaries rewritten to one sentence. The previous text is kept
  verbatim in `researchNotes`, shown on the profile as the collapsible
  "Evidence notes (research detail)" under Research status, so nothing was
  lost. `scripts/apply_bio_rewrite.py` validated and applied them (rejects
  texts that still contain ids or process words). Rule for future research:
  write findings into `researchNotes`, facts, events and sources; keep
  `bio` as prose.

## 2026-10-08 — Round 4 overnight research imported

- John supplied the output of a separate overnight research run (four zip
  archives + SUMMARY.md): 873 per-person result files (524 researched, 323
  nothing new, 26 living), 1,066 source citations, 129 media items (92 files
  copied), 42 new relatives, 30 stories, 78 leads. Archived read-only under
  `research/imported/round4/` (SUMMARY.md, appendix.md with every confidence
  change and conflict, people/*.json, new_people.json, stories.json,
  leads.json, media_manifest.csv).
- `scripts/import_round4.py` merged it: vital-date refinements (414), bio
  additions (499), 176 confidence changes applied with the justification in
  the link note and research log, 182 conflicts recorded (shown on profiles
  as "Conflicting evidence"), 40 open questions resolved, sources appended as
  `[R4-S#]` references, negative searches logged. Dates that disagree with
  the tree were applied only when the summary settles them with primary
  records (Henry J. Meier d. 20 Dec 1950; Theresa Meier b. 10 Sep 1868;
  Helen Ferlaino b. 8 Oct 1894; Johann Andreas Grub b. 12 Sep 1727);
  everything else stays a conflict.
- New relatives `M0037`–`M0078` (ids mapped in `_work/new_ids.json`), with
  families built from their relationships (direction reviewed by hand: the
  worker groups used parent/child labels inconsistently). Includes a new
  direct ancestor, Deliverance King (`M0069`), first wife of John Tuthill
  (1635–1717) and mother of John Jr.
- Duplicate records merged (new `merges` op in `build.py`): Clarissa→Theresa
  Meier, Filomena→Helen Ferlaino, Mollie Petriello→Carmela Gianetta,
  Mariantonia→Mariangela Cannatello, Anna Tuthill Symmes→Anna Symmes
  Harrison. Hannah Reeve moved from James to Joshua Tuthill (Akerly 1898).
  Not applied (John's call, see SUMMARY "Conflicts that need your
  judgment"): splitting H0078 (two Grub wives) and the two Charity Pringles,
  Katie→Grace Petrillo, detaching the Youngs/Horne block, Sir Samuel Smith,
  the Buswells and Mary Steele (kept with downgraded confidence per site
  convention), Carmine Fiorillo's mother (Maria vs Vittoria Marrelli),
  Frederick Meier's birth day (11 Jan vs 11 Nov 1862).
- Stories: 28 added to the site; two kept out as research notes ("How
  William Wells's widow became 'Mary Youngs'", "A will that settles a
  mother"). Leads: `research/leads-round4.md`.

## 2026-10-08 — Tree-wide media hunt (WikiTree, Wikipedia/Commons)

- John asked for media and photos for everyone. Two new scripts:
  `scripts/find_wikitree.py --attach` (WikiTree public API; 636 deceased
  people checked, 109 matched after audit, 20 rejected, 2 ambiguous: profile
  links, 34 Find a Grave links quoted in the profiles, 37 images of which the
  profile's primary photo becomes the portrait) and
  `scripts/find_wikipedia_media.py --tagged --attach` (Wikipedia/Wikidata/
  Commons for the 44 tagged people: 7 matched — Anna Harrison, Cornelius V. W.
  Lawrence, Nathaniel Woodhull, David Gardiner Tyler, Theodorus Bailey,
  Daniel L. Braine, John F. Farnsworth — with Commons portraits).
  `scripts/audit_wikitree.py` re-checks matches against the rules (dates
  within 1–2 years, first name, place words in common) and undoes rejected
  ones; manual keeps I282695486653 and H0192, manual rejects listed in the
  report. Second Wikipedia pass on the notable cousins added Commons portraits for Benjamin, William Henry and John Scott Harrison, John Cleves Symmes, Lawrence Grant White, Cornelius Lawrence, Willoughby Jones and Tapping Reeve, and links for Judson LaMoure and S. D. Warren. Totals now: 27 portraits, 129 people with media, 309 items.
- Wikimedia throttles this container's shared IP (HTTP 429 after nearly every
  call) so the Wikipedia pass is slow; WikiTree is ~1 req/s with occasional
  429s. Wikipedia search found no articles for Bull Smith (covered only in the
  Smithtown article), Thomas Topping, Thomas Lamoreaux or James Clinch Smith.
- The GEDCOM lists 104 Ancestry photos (`ancestryMedia`, including portraits of
  John and James C. Meier) that Ancestry's media service will not serve
  without login (HTTP 403). John needs to export them or add them to the
  Drive folder.
- Not yet tried: Chronicling America / newspapers for obituaries, FamilySearch
  (login), Find a Grave direct (403 here; only links via WikiTree).

## 2026-10-08 — Jamie Meier at Waynewood Elementary

- Owner's lead: Jamie was principal of Waynewood Elementary (Alexandria,
  Fort Hunt). Confirmed: principal by Mar 2006 (Connection), Academic
  Excellence Award four straight years to 2012 (Mount Vernon Gazette), Girl
  Scout appreciation Jun 2011 (Patch), retired Jun 2017 after 31 years in
  FCPS and 11 as principal (Covering the Corridor; successor Katie Reynolds,
  Gazette Sep 2017), Waynewood Citizens Association Citizen of the Year
  21 Feb 2018 (Patch: 30-mile commute from Chantilly, daily classroom
  visits, crossing-guard duty). `M0014` bio, events, facts and six links
  updated. Still unknown: his FCPS posts 1986–2006.

## 2026-10-08 — Deeper research on Thomas Sr. and his siblings

- Owner's leads: Jamie (Chantilly VA, wife Marie, daughters Sarah and
  Samantha, elementary principal, assistant football coach, East Stroudsburg
  football); Kathy m. Rick McGinley; Nancy m. Anthony "Tony" Russo (children
  Anthony, Chelsea, Gianna, Emily); Terry m. a Borgman, divorced; Laura's
  surname is De Santis; Thomas Sr. head coach George Mason HS and Herndon HS,
  Langley administrator, retired 2014, East Stroudsburg football with Jamie,
  met Sharon there.
- **Thomas F. Meier Sr. (`I282604492836`)** verified: ESU 2018 media guide
  lists Tom Meier as a 1978–80 letterman; 1980 passing 45-71-521-3 TD, 7 TD
  scored (42 pts), 2 rushing TD vs Bloomsburg, 58- and 55-yd TD catches.
  Washington Post 20 Sep 1990 ("family affair": first-year Herndon coach,
  brother Danny at West Potomac, brother Jamie on Danny's staff), 21 Sep
  1991 (second brothers matchup, 49-6 in 1990), 24 Sep 1993 (No. 7 Herndon
  beats Robinson in OT), 9 Oct 2003 (Guyer homecoming). Connection 2012
  profiles of Jon Carman (22-8 in 1991–93, 8-2 in 1993) and Brandon Guyer
  (7-4 in 2003, ended six-year playoff drought). Herndon HS lists football
  district titles 1985 and 1990 (his first season). MaxPreps: 2006-07 head
  coach Tom Meier 6-4, Joe Sheaffer from 2007. Langley's Saxon Scope names
  Thomas Meier assistant principal and renovation-committee coordinator
  2011–14. George Mason seasons: not in the Post archive (only a Feb 1985
  story on the programme's Group A struggles). The Washington Post archive
  is readable through the r.jina.ai text proxy (direct fetches 403); ledes
  only, body paywalled on some pieces. Media: three guide pages attached,
  16 links.
- **Jamie (`M0014`)**: ESU letterman 1977–80, split end; All-PSAC East first
  team 1979 (26-476-4; 215 yds at Bloomsburg, 11th-best single game in school
  history; 102 at Cortland); 1980 leader 37-496-1; 69-yd TD from Frank Bell
  1977. Washington Post 21 Dec 1989: "Jamie {Meier, Danny's brother and
  offensive coordinator}" on the 1989 state-title trick play. Connection
  7 Jun 2006: "Jaime Meier, an elementary-school principal" (school not
  named; FCPS site search found no Meier principal page). Given name set to
  James, aka Jaime. Wife Marie `M0028`, daughters `M0029`–`M0030`, `MF0007`.
- Added in-laws from the owner: Rick McGinley `M0027` (`MF0006`), Tony Russo
  `M0031` and children `M0032`–`M0035` (`MF0008`), Terry's former husband
  Borgman `M0036` (`MF0009`, status `divorced`; site now labels former
  spouses). Laura `M0020` surname → De Santis. Sharon: East Stroudsburg
  added (owner).
- Searched and found nothing public for Kathy/Rick McGinley, Nancy/Tony
  Russo and children, Terry/Borgman, Susie, Jack (web search; no
  people-search sites). A LinkedIn "Rick McGinley" in Newtown PA exists but
  is unverified and not recorded. A Mike Meier (Robinson senior) was a 2006
  Post All-Met honorable-mention running back while Danny was Robinson's
  principal; noted on `M0023` as probable, unconfirmed.
- Still wanted: James C. Meier's Aug 2008 Courier Times obituary (would give
  married names and towns for all eight); season records for Tom at George
  Mason and Herndon (VHSL/Post archive); Jamie's school; Susie and Jack's
  married names/towns.

## 2026-10-08 — Danny Meier researched; maps feature

- **Daniel F. "Danny" Meier (`M0013`)**, the owner's uncle: nose guard for Lou
  Holtz at NC State 1972–75; head coach Orange HS (Hillsborough NC, 1-9 to
  21-9 in three seasons); first head coach of West Potomac HS 1985–91 (68-16,
  Virginia AAA champions 1989 and 1990, VHSL Coach of the Year both years,
  All-Met Coach of the Year 1985); Chantilly HS 1992–96 (47-12, AAA Div. 6
  champions 1996, 13-1). Resigned July 1997 for administration: counsellor
  and assistant principal at Herndon, principal Rocky Run MS 2001–03,
  principal Robinson Secondary 2003–Apr 2013 (retired after 29 years with
  FCPS and became Robinson's head football coach), then interim principal
  at Woodson, Madison, Herndon, Whitman MS, Oakton, McLean. West Potomac
  Athletic Hall of Fame 2019. Wife Annie; children Mike (c.1989, Army),
  Timmy (c.1991) and Joe (c.1993, West Point cadets in 2013), Mary (c.1995);
  Fairfax Station VA (2013). Birth year revised from the owner's 1956 to
  1953/54 (ages in the 1985, 1997 and 2013 articles). Sources: Washington
  Post 1985/1997/2013, Connection Newspapers 2013, Patch 2013, The Highlander
  2018, West Potomac HOF 2019. Family added as `M0022`–`M0026`, `MF0005`.
- Owner states James C. Meier never remarried (open question closed).
- The other six siblings (Kathy, Jamie, Susie, Nancy, Jack, Terry): nothing
  found on free sources with the surname and Levittown; they need married
  names, towns or professions from the owner to search effectively.
- A 2012 Washington Examiner item about a Fairfax land-investment lawsuit
  names Fairfax school administrators Daniel and Thomas Meier. Deliberately
  not recorded on the site or in research files (unverified allegations about
  living people); the owner was told in chat.
- **Site:** every place is now tappable and opens a map sheet (Leaflet from
  cdnjs, OpenStreetMap tiles with a dark filter, no API key). Coordinates are
  pre-resolved by `scripts/geocode_places.py` (Nominatim, 1 request/s) into
  `data/places.json` and shipped in the bundle; unknown places fall back to a
  live Nominatim lookup. Run the geocoder after adding places.

## 2026-10-08 — Owner's father's siblings, fiancée, nephew

- Owner listed his father's seven siblings with estimated birth years
  (Levittown, PA): Kathryn "Kathy" c.1955, Daniel "Danny" c.1956, James
  "Jamie" c.1958, Susan "Susie" c.1960, Nancy c.1961, John "Jack" c.1962,
  Theresa/Teresa "Terry" c.1963, plus Thomas Francis "Tommy" Sr. 1959. That
  is three brothers and four sisters; the earlier "seven brothers and a
  sister" is superseded. Added as `M0012`–`M0018` under James C. and Kathryn
  (McGuire) Meier. Exact dates, married names and living status still open.
- Owner: engaged to Shannon McCarthy (`M0019`, family `MF0003`, status
  engaged). Tommy Jr. is married to Laura (`M0020`); their son is Luca
  (`M0021`). The site now labels an engaged couple "Fiancé/Fiancée".

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
