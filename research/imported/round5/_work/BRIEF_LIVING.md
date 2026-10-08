# Research brief: living members of meiertree.com (round 5, 2026-10-08)

John's request: "Do deep research on all of the living members of meiertree.com. The goal is to find any and all
more information about them, especially publicly available media and other data online."

This round reuses the round-4 format (`/mnt/project-files/research_output/_work/BRIEF.md`: read its Evidence rules,
Media section, people JSON schema and Access notes; they all apply) with the changes below.

## Worklist
52 people with no death record who are living or presumed living: the 26 `skip` people of round 4, plus the 26
round-4 found living (`living_detected`). Built from the live `https://www.meiertree.com/data/family.js`
(2026-10-08, 899 people, no additions since round 4). Each worklist item = `{roster, siteRecord, round4File}`;
`round4File` is the round-4 living evidence (may be null). Some older people (b. 1928-1934) may in fact have died:
if you find a death/obituary, record it fully (status `deceased_detected`) — that is a major finding.

## Privacy rule (applied to everything this round; John can widen it)
COLLECT what a family-history site would publish:
- public photos and media (news photos, team/roster photos, official portraits, public social-media profile
  photos posted by the person or an organisation, wedding announcements), with links;
- news articles, sports records, halls of fame, awards, honours, military commissions/promotions/units as published;
- obituaries of relatives that name them (and what the obituary says about them: spouse, residence town/state);
- published marriage, engagement or birth announcements;
- public professional / community profiles (school staff pages, coaching bios, LinkedIn headline if visible without
  login, company pages, public-office pages), education and degrees as publicly stated, careers;
- anything notable (Wikipedia, books, patents, publications, music releases, elected office, records).
NEVER record: street addresses, phone numbers, email addresses, financial details (salaries, property values,
debts, court/financial filings), dates of birth beyond what the site already shows (year), SSNs, data-broker /
people-search results (Whitepages, Spokeo, BeenVerified, etc. — do not use them at all), DNA data, medical
details, criminal records of living people, or private social-media content. Town/state of residence as stated in
an obituary or news article is fine.
MINORS (anyone under 18, or of unknown age who appears to be a child, e.g. Luca Meier, grandchildren): name and
relationship only. Do not search for them; write a file with status `minor_limited` and nothing else.
Be careful with common names: identity needs >= 2 matching identifiers (name + relative / school / town / team /
year). A same-name stranger is worse than nothing. Name-only matches go in `searchedNoResult` or leads, not facts.

## Status values
`researched | nothing_new | deceased_detected | minor_limited | blocked`.

## Schema additions (in people/<id>.json, alongside the round-4 fields)
- `updates.education`: [ { "school", "years", "detail", "sourceRefs" } ]
- `updates.career`: [ { "role", "organization", "years", "detail", "sourceRefs" } ]
- `updates.awards`: [ { "title", "date", "detail", "sourceRefs" } ]
- `updates.residences`: town/city/state level only.
- `onlinePresence`: [ { "kind": "official_profile|news|sports_stats|wikipedia|social_public|publication|other",
  "title", "url", "accessed", "note" } ] — public pages about the person (no contact details).
- `newsArticles`: [ { "title", "publication", "date", "url", "summary", "accessed" } ]
Media rules as round 4. Most modern photos are copyrighted: record them (type, title, pageUrl, directUrl, rights,
`downloadable:false`) but download only public-domain / reuse-permitting CC items (e.g. US government / military
photos on dvidshub or army.mil are generally public domain; Wikimedia Commons CC items).

## Output (all under /mnt/project-files/research_output_living/)
- `people/<id>.json` per person; `media/<id>/` downloads;
- `_work/<group>/progress.json`, `new_people.json`, `stories.json`, `leads.json` (same formats as round 4).
- new_people this round may include newly found relatives (living or deceased). Living new people: name,
  relationship and the source naming them only (plus public notable facts if adult). Use your group's ID block.

## Where to look (living people)
General web search (WebSearch, many phrasings and nicknames: Tommy/Tom, Danny/Dan, Jamie, Kathy, Terry, Matt),
local newspapers (Scranton Times-Tribune, Wilkes-Barre, Bucks County Courier Times, Washington Post high-school
sports, Loudoun Times-Mirror, Fairfax Times, Connection Newspapers), legacy.com and funeral-home obituaries for
relatives, school and college athletics sites (East Stroudsburg, NC State, West Point, Army), MaxPreps,
hall-of-fame sites, VHSL records, school staff pages, Fairfax/Loudoun county school pages, DVIDS / army.mil,
Google Scholar, Internet Archive / Wayback, YouTube, Wikipedia. Data-broker sites: do not use.
