# Owner instructions and preferences (from the handoff)

*Copied verbatim from the project handoff (research/imported/Family_History_Handoff_2026-10.md), 2026-10-08. Later findings go in research/LOG.md and data/research/.*

## 1. Project instructions and preferences

### 1.1 Custom project instructions (verbatim)

No custom project instructions are configured.

The project's topic, as set on the project, is: **"To capture all of John Meier's family tree"**.

Two other settings were recorded:

- **Repositories.** No GitHub repository was connected to the project. When John asked whether one was connected, the answer was no.
- **Context source.** A Google Drive folder was added on 2026-10-07: https://drive.google.com/drive/folders/1nLAbzaMlKOSgimj590vLgkfDQMesBRVJ

### 1.2 John's requests, verbatim, in the order he made them

1. "I have uploaded MD and PDF files that give information into research that's already been done on my family tree. I also added a Google Drive folder to context that has my entire family tree and more info - but the MD and PDF files may override/update some of the tree. Do deep research into my entire lineage. Look for and not any individuals that stand out - war heroes, celebrities, athletes, politicians, etc. Also, if non direct relatives, identify distant relatives as well. Highlight any ties to Long Island, Northeastern PA, and Virginia."
2. "Do even deeper research into my lineage. Look far and wide for any individuals that stand out - war heroes, celebrities, politicians, etc. Also note and distant relatives. Do your best to fill in. Any gaps in my family tree. Also, do your best to find interesting information and facts about those people you identify in my tree."
3. "So can you concisely sum up my relation to the US presidents?"
4. "Also, who was James Clinch Smith? Where was he from and how am I related to him?"
5. "Thanks. Do more deep research on the gaps, fill them in, convert probably links to confirmed, and also find new information where applicable. Also, do more research to try and trace back the "Meier" lineage as far as it goes. Also, trace my roots back to specific areas, cities, and people in Italy, Germany, England, Germany, and France."
6. "Thanks. When did the "Mayer" name change to "Meier"?"
7. The handoff request that produced this document:

   > "I am moving this project's knowledge into a GitHub repository that another Claude session maintains. Produce a complete, self-contained handoff document of EVERYTHING you know about my family history from this project: the project instructions, every uploaded file, all memory, and all conclusions from our conversations. Do not summarise away details; completeness matters more than brevity. If it is too long for one reply, end with "CONTINUED" and I will say "continue". Use exactly the structure below."

   The structure he gave is sections 1 to 8 of this document. For section 3 it adds a JSON schema and rules for dates and places.

### 1.3 Preferences and working rules

Each rule below is either stated by John or followed consistently in the project's work.

1. **Uploads beat the tree.** John's uploaded Markdown and PDF reports override or update his Ancestry tree (the Drive screenshots) wherever they conflict. *(John, request 1.)*
2. **Look for standout people.** He wants individuals who stand out: war heroes, celebrities, athletes, politicians and similar. *(Requests 1 and 2.)*
3. **Include distant relatives.** Distant and non-direct relatives (cousins) should be identified and noted, not only direct ancestors. *(Requests 1 and 2.)*
4. **Regional ties.** Ties to **Long Island**, **Northeastern Pennsylvania** and **Virginia** should be highlighted. *(Request 1.)*
5. **Fill gaps and add color.** Gaps in the tree should be filled where possible, and interesting facts about the people found should be added. *(Request 2.)*
6. **Strengthen the evidence.** Probable links should be converted to confirmed where records allow, and new information found. *(Request 5.)*
7. **Push the Meier line back.** The Meier surname line should be traced as far back as it goes. *(Request 5.)*
8. **Pin down origins.** Roots should be traced to specific areas, towns and people in Italy, Germany, England and France. *(Request 5.)* Ireland was added by the research because the Heffernan line required it.
9. **Answer short questions concisely.** A request to "concisely sum up" gets a short answer. *(Request 3.)*
10. **Label confidence.** Every finding carries a confidence label (confirmed, probable or speculative) and a source. *(Practice in all three research rounds.)*
11. **Leave living people alone.** Living people are not researched beyond the names already in the tree. *(Practice in all three rounds; also applied to this handoff.)*
12. **Handoff format.** Completeness beats brevity, nothing is summarised away, the exact eight-section structure is used, long output is split across replies ending "CONTINUED", and John replies "continue". *(Request 7.)*
13. **Section 3 format.** One JSON object per person. Each person is identified by full name and birth year, or "b. unknown". Dates are ISO `YYYY-MM-DD` when exact, otherwise `YYYY`, `ABT YYYY`, `BEF YYYY` or `BET YYYY AND YYYY`. `AFT YYYY` is also used here, by extension. Places run from most specific to least, comma separated, ending with the country. Keys with nothing to say are omitted. *(Request 7.)*
14. **Moraca.** Section 4 must cover the lines Meier, Petriello, Cognetti, Colosimo, Ferlaino, McGuire, Moraca, Fiorillo and Pringle, plus any others. **Moraca appears nowhere in the project files**, which section 4 states. *(Request 7.)*

### 1.4 Conclusions given in conversation, which are not in any report file

These answers were given in the project's research thread in reply to requests 3, 4 and 6. They are reproduced in full here because no report file holds them.

**US presidents (request 3), the concise answer given**

- **Benjamin Harrison** (23rd president) is the **only president related by blood**. He is a 6th cousin 5 times removed (6C5R) through the Long Island colonial lines, via his grandmother Anna Symmes Harrison's Long Island ancestry, and a 7C4R by a second route.
- **William Henry Harrison** and **John Tyler** are related **by marriage only**. Their wives, First Ladies Anna Symmes Harrison (4C7R) and Julia Gardiner Tyler (5C6R), are John's blood cousins. The joke given was "Tippecanoe and Tyler Too": both First Ladies of that ticket are cousins, but neither president is.
- **Theodore Roosevelt** appointed John's 2nd-great-grand-uncle Thomas F. Heffernan postmaster of Wilkes-Barre in 1907, but is **not kin**. Taft reappointed Heffernan in 1911.

**James Clinch Smith (request 4), the answer given**

- James Clinch Smith (1856–1912) was from **Smithtown, Long Island**. He was a socialite who lived in **Paris**, and he died as a **first-class passenger on the Titanic** in April 1912. His body was not recovered.
- His sister **Bessie Smith** married the architect **Stanford White**.
- He is John's **6th cousin 5 times removed (6C5R)** through Richard "Bull" Smith: Bull Smith → Richard Smith Jr. (2d) → Sarah Smith Woodhull → Gen. Nathaniel Woodhull → Elizabeth Woodhull Nicoll → Eliza Nicoll Smith → Judge J. Lawrence Smith → James Clinch Smith. John descends from Bull Smith through Job Smith (see section 4, Smith line).

**When "Mayer" became "Meier" (request 6), the answer given**

- The Munzingen civil registers write the family as **Mayer** throughout (1820–1862).
- In America the spelling drifted. The 1870 census has "**Meyer**", the 1880 census "**Myer**", and the 1892 Hazleton marriage of Henry J. and Annie Higgins is the first record spelled "**Meier**". A later edit to that answer corrected an earlier claim: the 1892 spelling was written by the clerk, so Henry may not have chosen it himself.
- "Meier" is consistent from 1910 on, except for "Meyer" in the 1940 census.
- There was **no formal name change**. Why "ei" won out is a guess.

---
