# Research brief: the Cognetti line (round 6, 2026-10-08)

John's request: "Do deep research into the Cognetti family line. Find new info, make confirmations, find media,
and sources. The goal is to update meiertree.com with more information."

This round reuses the round-4 format. READ FIRST: `/mnt/project-files/research_output/_work/BRIEF.md`
(Evidence rules, Media section, people JSON schema, group-file formats and Access notes all apply).
Changes for this round are below.

## Scope (default chosen by the coordinating session)
"Cognetti line" = John's maternal grandmother Mary Cognetti's paternal family:
- the Cognetta ancestors of Dasà, Calabria (Giovanni, Nicola, Francesco and their wives Lamanna, Cannatello,
  Malvaso, Croce), and the question of Frank's real birthplace/parents;
- Frank Cognetti (I282695503559) and Helen Ferlaino (US life only; her San Mango ancestry was done in round 4)
  and their children and children's spouses in Scranton;
- collateral Cognetta/Cognetti relatives not yet on the site (Frank's siblings, cousins, emigrants), deceased only;
- the "other" Scranton/Dunmore Frank Cognetti of Nicastro (H0381) and Bruno Cognetto (H0513), only to settle
  whether they are related (kept separate so far — do NOT merge without proof).
NOT in scope: Helen Ferlaino's ancestry (Ferlaino/Fiorillo/Colosimo/Moraca…, done in round 4); living people
(round 5 covered them: Mary Cognetti, Paige Cognetti, Anthony Paul, the M00xx grandsons — don't research them,
and apply the round-5 privacy rule in `/mnt/project-files/research_output_living/_work/BRIEF_LIVING.md` to anything
you incidentally find about living people).

## Baseline
The live site was re-downloaded today (951 people): `_work/family_2026-10-08.js`. It ALREADY CONTAINS round-4
and round-5 findings. Each worklist item is `{siteRecord, round4File, round5File}` — the siteRecord (bio,
researchNotes, researchLog, openQuestions, sources, facts) is the baseline. Report only what is NEW or CHANGED
relative to it. Prior narrative notes: research/notes/italian.md, research/notes/round2/italian_gaps.md,
research/notes/round3/italian_origins.md; round-4 Calabria worker: research_output/_work/italian_calabria/
(worker_report.md, leads.json, stories.json). Grep, don't read whole, research/handoff/Family_History_Handoff_2026-10.md.

## Output (all under /mnt/project-files/research_output_cognetti/)
- `people/<id>.json` (round-4 schema), `media/<id>/` downloads,
- `_work/<group>/progress.json`, `new_people.json`, `stories.json`, `leads.json`.
- ID blocks: italy_origins NEW-1501..1549, scranton_family NEW-1551..1599.
- Access checks made today: Antenati (incl. dam-antenati IIIF manifests) 403; loc.gov JSON 403 to curl (try
  WebFetch / other loc.gov URL forms once); FamilySearch published-tree JSON works (GJB1-P6Y = Frank).

## High-value open questions
1. Frank's arrival (1907/1908) manifest: name, age, comune, father/contact in Italy, destination contact in
   Scranton. Proves (or disproves) Dasà and Giovanni. Try Steve Morse/Ellis Island indexes, FamilySearch
   tree-attached records, any free transcriptions.
2. Frank's naturalization (between 1920 and 1930; Lackawanna County court or US District Court Scranton), WWI
   draft card (1917-18, he was c.26 in Scranton), WWII 1942 "old man's" registration, death (after Apr 1950;
   SSDI, obituaries, Cathedral Cemetery / other Scranton cemeteries).
3. Giovanni Cognetta's death in 1930 "Nicasetro" — Nicastro? Is the Dasà origin right at all? Are the two
   Scranton Frank Cognettis cousins?
4. Children: obituaries, military service (WWII), notable careers, Angeline's marriage/death, spouses' details,
   newspaper items (Scranton Republican/Times/Tribune), photos, yearbooks (rights!).
