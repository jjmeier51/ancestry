# Cognetti line: research round 6 (2026-10-08)

Requested by John: deep research into the Cognetti family line, to update meiertree.com.
Format: same as round 4 (`research_output/_work/BRIEF.md`); scope notes in `_work/BRIEF_COGNETTI.md`.
Baseline: the live site data as of 2026-10-08 (951 people, `_work/family_2026-10-08.js`), which already includes rounds 4 and 5.

## How to merge (for the site's coding agent)
- `people/<id>.json`: one file per existing site person (24), round-4 schema, new/changed info only. Merge `updates`,
  `bioAdditions`, `sources`, `media`, `conflicts`, `relationships`, `confidenceRecommendation`, `researchLogEntry`.
- `new_people.json`: 10 new deceased relatives (NEW-1501, NEW-1551..1559), each with `relationships` to site IDs.
- `stories.json` (4), `leads.json` (16), `media_manifest.csv` (11 items; 4 downloaded, all public domain, in `media/<id>/`).
- `progress.json`, `_work/merge_stats.json`: run state. Re-run `node _work/merge.js` after any edit to group files.

## Scope
In: the Cognetta ancestors of Dasà (Calabria), Frank Cognetti and Helen Ferlaino's American life, their eight children and
the children's spouses, collateral Cognettas, and the unrelated Nicastro Cognetti family (H0381, H0513).
Out: Helen's Ferlaino/Fiorillo/Colosimo ancestry (done in round 4) and living people (done in round 5; round-5 privacy rule applied).

## Headlines
1. **The Dasà Cognettas went to Stamford, Connecticut.** Ellis Island manifests (reached via the Statue of Liberty–Ellis Island
   Foundation search, backed by FamilySearch) show every Dasà Cognetta arriving 1903–1916 was bound for Stamford.
2. **A Giovanni Cognetta of Dasà had sons Nicola and Francesco.** On the SS Regina d'Italia (arr. 2 May 1910), Nicola Cognetta, 23,
   of Dasà, named "father Giovanni, Dasa" and was rejoining "brother Francesco, Branch St", Stamford. Giovanni was alive at Dasà in 1910.
   New person NEW-1501 (Nicola, b. c.1886–87, shoemaker).
3. **A candidate for Frank's own arrival:** Francesco Cognetta, 17, of Dasà, SS Citta di Milano, arr. 18 Jun 1905, going to his
   brother Nicola in Stamford. Candidate only: born c.1888 (Frank's censuses imply 1890–92) and 1905 (Frank said 1907/08).
   Supports the tree's Dasà/Giovanni parentage but does not prove it. Manifest images downloaded (`media/I282695503559/`, `media/I282697102020/`).
4. **Giovanni's 1930 death place "Nicasetro" is unsupported.** The Nicastro Cognetto family of the other Scranton Frank (H0381:
   b. 20 Sep 1894 Nicastro, WWI card read and downloaded; father Bruno, b. 1857, son of Pietro Giuseppe Cognetto & Giovanna Cuda)
   has no Giovanni and no link to ours was found. Keep them separate.
5. **Eight children, none lost young.** Leo's obituary says he was predeceased by five brothers and a sister; PA death indexes 1913–1940
   show no child deaths for Frank and Helen.
6. **Spouses documented from primary marriage licences:** Elizabeth Notarianni (H0499, 1914–1994, stenographer, parents Joseph Notarianni
   & Michelina Carabia, Cathedral Cemetery) and Marguerite Forgione (H0498, seamstress, parents Peter Forgione & Elizabeth D'Ettore,
   d. 2014 per FS tree). Both recommended unverified → confirmed. The same priest married Ralph (1940) and Sal (1943).
7. **New spouses:** Leo's wife Jean D. Rossi (1932–2023, NEW-1551, parents NEW-1558/1559, from his full obituary); Joseph F.'s wife
   Domenica "Aunt Min" (NEW-1552, m. 1946, d. 2009); Angeline married Nicholas Butchko (NEW-1557) and died 2009 aged 87 (obituary snippet only).
8. **Career details:** Leo: Korean War Army, 34 years at IBM. Joseph F.: lumber salesman from 1937, Lou Spector Award 1961. Anthony R.:
   director of the State Workmen's Insurance Fund, Workmen's Compensation Appeal Board commissioner, Jaycees and Keystone Heart Association
   president, buried Cathedral Cemetery (summaries; full obituary blocked). Ralph A.: full name Ralph Anthony; Royal Bottling (1940),
   beer-distributor salesman (1950), no WWII service.
9. **Helen (I282695503581):** married at 16, 7th-grade schooling, naturalized by 1940, owned 612 Philo St ($5,000 in 1930, $3,000 in 1940).
10. **Frank's death is still unknown:** not in any PA death index 1950–1966. Helen's 1965 death certificate (widow or married) would bracket it.

## Conflicts for John to decide
- Frank: immigration 1907/08 (censuses) vs candidate 1905 manifest; birth 1890–92 vs c.1888. Don't change unless identity is proved.
- Giovanni: death place "Nicasetro" vs alive at Dasà 1910, no record of a move.
- Ralph A.: site lists sons Frank, Peter, Anthony; 1950 census adds a daughter Helen (b. c.1940–41, possibly living, not researched).
- Anthony R.: education Keystone JC + Penn State (site) vs Penn State + University of Scranton (one obituary summary).
- Joseph F.: death place Moosic (site) vs VNA Hospice, Scranton (residence Moosic).
- Site wording: Leo's bio calls Mary Petriello John's great-grandmother (she is his grandmother); the children's bios say
  "great-granduncle/aunt" where it should be great-uncle/aunt.
- Merge duplicate I282695503588 into Ralph A. Cognetti I282695503685 (confirmed again).

## Top leads (paywalled or blocked)
1. Frank's WWI draft card, Lackawanna Co., 1917–18; his 1942 WWII registration; naturalization 1920–30 (US District Court, Scranton).
2. 1910 census, Stamford CT, Branch St: Francesco and Nicola Cognetta.
3. PA death certificates: Helen 1965 (file 027518); Salvatore Cognetti 1938 (file 80521), Frances Cognetti 1939 (16802), Giuseppe Cognetto
   1922 (79110), unplaced Scranton Cognettis who may be Frank's kin.
4. Dasà civil records (Antenati, blocked here): births c.1886–92, Giovanni's death 1930.
5. Full obituaries: Anthony R. (2008), Joseph F. and Domenica (2009), Angeline Butchko (2009), Marguerite Cognetti (2014).

## Blocked this round
Antenati, FamilySearch record/catalog search, Legacy.com, Find a Grave, NARA AAD and catalog API, loc.gov JSON, Steve Morse/JewishGen,
Wayback (429), Google Books API (429).
