# Sources and research done

*Copied verbatim from the project handoff (research/imported/Family_History_Handoff_2026-10.md), 2026-10-08. Later findings go in research/LOG.md and data/research/.*

## 6. Sources and research done

### 6.0 How the research was done, and what access worked

**History**

- **Before the project.** John's uploaded reports ("Old Records Reshape…" and "Johnny's Cousins, Not Ancestors, Settled Hauppauge") and the Bull Smith PDF came from research done before this project. Their own sources are listed inside them; see the verbatim copies in section 2.1.
- **During the project.** Three web-research rounds ran on 2026-10-07 (Rounds 1, 2 and 3). Each used parallel workers, one per family line, and wrote a report plus per-line notes files with a source link on every claim.

**Access that worked**

- FamilySearch public tree person pages, and the FamilySearch tree JSON endpoint. The JSON endpoint also serves unpublished profiles that can be reached through relatives' links.
- Landesarchiv Baden-Württemberg online images (collection L 10, Munzingen civil registers): free "plink" image links.
- Pennsylvania State Archives death-index PDFs (phmc.state.pa.us).
- Search-engine extracts of newspapers, obituaries and books.
- Internet Archive and Google Books for older genealogies (Pelletreau, Harvey, Bradsby, Howell and others).
- Wikimedia scans of Pelletreau.

**Access that was blocked** (automated access failed in every round)

- Ancestry
- Find a Grave
- FamilySearch historical-record **search**
- Antenati (the Italian state archives portal)
- Geni
- Legacy
- The SAR and DAR database searches

**Consequences**

- Several findings rest on public indexes and search extracts, and are therefore labelled probable rather than confirmed.
- Any future session should expect the same blocks unless it has a logged-in browser.

**Drive folder method.** Fetch the folder HTML with curl, parse the file IDs, download each from `https://drive.usercontent.google.com/download?id=<ID>&export=download`, and convert HEIC to JPG with Python `pillow-heif`.

**Living people** were deliberately not researched. Paige Cognetti, Mayor of Scranton, married into a Scranton Cognetti family; whether it is John's was not researched because the people involved are living.

The per-line source lists follow, including searches that came back empty so they are not repeated.

### 6.1 Meier, McGuire and German lines

Research files these come from:
- research/tree_transcription.md and Ancestry tree screenshots (section 2.2.2) (Ancestry tree, IMG_7791–7840)
- Johnny_Meier_Lineage_Report_2026-10.md (Round 1), _Round2_, _Round3_
- notes/meier_mcguire.md; notes/round2/meier_gaps.md; notes/round2/black_forest.md; notes/round3/meier_line.md; notes/round3/german_origins.md; notes/round3/irish_pa.md (McGuire/McAvoy/Higgins sections)
- John's upload "Old Records Reshape Johnny Meier's Family Tree" (the deep-dive report)

#### A. Sources consulted that gave results

##### German original registers (Landesarchiv Baden-Württemberg, Staatsarchiv Freiburg, collection L 10, free images)
- **L 10 Nr. 1590**: Munzingen, Catholic parish, civil-register duplicates (*Standesbücher*), 1810–1839; 549 images; record id 5-480946. Permalink format: `http://www.landesarchiv-bw.de/plink/?f=5-<record id>-<image no>`.
  - 5-480946-17: 1810 marriage with Joseph Birkenmaier as witness.
  - 5-480946-119: death of Veronica Heitzler, 29 Apr 1815 (Act 6).
  - 5-480946-215: marriage of Henericus Mayer × Juliana Senn, 16 Oct 1820 (marriages 1820 No. 3; extract 24 Jan 1821, signed Flamm).
  - 5-480946-220: birth of Maria Anna Creszentia Mayer, 3 Jul 1821, house No. 68.
  - 5-480946-376: 1832 death index (Birkenmayer infants).
  - 5-480946-440: birth of Friedrich Mayer, 2 Mar 1835 (births 1835 No. 10, fol. 100).
  - 5-480946-450: marriage of Fridrich Heitzler × Francisca Widlebacher, 7 Oct 1835.
  - 5-480946-464: marriage of Servatius Birkenmayer × M. Agatha Heizler, 17 Oct 1836 (Act. III; Landamt Freiburg licence 11 Oct 1836 No. 19140).
  - 5-480946-465: 1836 marriage index.
  - 5-480946-483: birth of Maria Anna Birkenmayer, 29 Mar 1837, bapt. 2 Apr (No. 12, fol. 135).
- **L 10 Nr. 1591**: Munzingen, Catholic parish, Standesbücher 1840–1870; 631 images; record id 5-480947.
  - 5-480947-62: birth of Joseph Birkenmayer, 15 Mar 1842, bapt. 19 Mar (No. 6).
  - 5-480947-125: death of Johann Ev. Birkenmayer, 17 Dec 1844 (No. 14), and the copied Basel death extract for Agatha Carolina Birkenmeyer, 1 Apr 1844 (No. 11).
  - 5-480947-286: death of Servatius Birkenmaier, 19 Apr 1853 (No. 8); death of Heinrich Birkenmaier, May 1853 (No. 9); death of twin Stephan, son of Anton Birkenmaier and his wife née Scherer, 1853.
  - 5-480947-440: marriage of Friedrich Mayer × Maria Anna Birkenmaier, 20 Oct 1862 (Ehebuch 1862 No. 2, p. 205; Landamt licence 2 Oct 1862; banns 12 and 19 Oct).
- The plink format was first seen cited on WikiTree Birkenmayer-2: https://www.wikitree.com/wiki/Birkenmayer-2

##### FamilySearch (public tree JSON and attached source images)
- **Method (round 3).** Scan all 4,562 FamilySearch Ancestors sitemaps (about 137 million URLs, about 18 GB, about 4 minutes) for target surnames; this gave 454,388 hits. Then pull each person through the public JSON endpoint `https://www.familysearch.org/service/tree/tree-data/published/persons/{ID}`. The endpoint also answers for unpublished profiles of deceased people that are linked from a published relative. Attached US source images download from `https://ancestors.familysearch.org/service/tree/tree-data/published/sources/{ID}/images/i/{n}/image.jpg`. The scan output was kept in an earlier session's scratch space (research3/dl/fs_u.txt) and was not preserved.
- **Chain that found the Meiers.** No Meier on the line has a published profile; the chain ran through relatives:
  - Addison Frances Pringle, LHHH-W68: https://ancestors.familysearch.org/en/LHHH-W68/addison-frances-pringle-1867-1943
  - → Florence Louise Pringle, LHHT-GQ4: https://ancestors.familysearch.org/en/LHHT-GQ4/florence-louise-pringle-1903
  - → William F Meier, LTHM-B3G: https://ancestors.familysearch.org/en/LTHM-B3G/william-f-meier-1905-1963
  - → Henry Joseph Meier Sr, LTHM-1XV: https://ancestors.familysearch.org/en/LTHM-1XV/henry-joseph-meier-sr-1866-1940
  - → Friedrich Mayer, G921-25N: https://ancestors.familysearch.org/en/G921-25N/friedrich-mayer-1835-1913
  - → Heinrich Mayer, G7PF-7J6: https://ancestors.familysearch.org/en/G7PF-7J6/heinrich-mayer-1796
- **Other Meier/Birkenmayer profiles.**
  - Michael Mayer: PW7H-2P6
  - Maria Anna Birkenmaier: G921-2R4 https://ancestors.familysearch.org/en/G921-2R4/maria-anna-birkenmaier-1837-1911
  - Anna Agnes Higgins: LBV1-4CM https://ancestors.familysearch.org/en/LBV1-4CM/anna-agnes-higgins-1867-1951
  - James C. Meier: GF3P-853 ("James E Meier 1929", an error) https://ancestors.familysearch.org/en/GF3P-853/james-e-meier-1929
  - William F. Meier Jr.: GF3P-DRK
  - Barbara Ann Meier: GV6C-8PM
  - The Ebringen family (ruled out): Mathias Birkemeier, KP4Y-KRW
- **McGuire-side profiles.**
  - Katherine Kay McGuire: G3PC-LJL
  - Her sisters: G3PC-RT7 and G3PC-FFK
  - Francis J. McGuire: GZQT-YKQ
  - James McGuire: GZQN-SCM, with his 1927 PA death certificate attached
  - Anna C. Jones: GZQT-T86
  - Edward McGuire: 994Z-27X / GZQN-GZT
  - Edward F. Jones & Margaret McIver: L85M-P2Q
  - William R. McAvoy: K6NQ-ZXZ
  - Catherine A. Murphy: K6NQ-ZX8
  - Martin Murphy & Alice Comerford: G7FL-HGY and L85M-PP2
  - Elizabeth (McAvoy) McGuire: KGQH-JNV
- **Indexed records.**
  - Freiburg archdiocese church index: QP3C-8JM1, QP3C-8J9D, QP3C-8J9S, QP3C-8J9H (1862 marriage); QP3C-SCW4 and QP3C-SCW6 (1857 marriage of Maria Anna Creszentia); QP3Z-8T76 (the Latin "Henricus Mayer" entry); QP3C-8J9F, QP3Z-QFWQ, QP3C-8J92, QP3C-Y3Q3 (Servatius × Agatha, indexed as 27 Oct 1836).
  - US records: 1930 census XH7Z-MLW; 1950 census 6X1W-JY84; 1926 marriage KMZX-RZ4 / KMZX-RZZ; 1892 docket VF4Z-ZZP / VF4Z-ZZ5; 1910 census MG8K-XG7; 1920 census M6Y8-TQV; 1940 census KQ7H-M4S; 1870 census MZPR-GLP; 1880 census MWNZ-PDS; 1923 McGuire licence KHF5-V74.
  - Find a Grave index on FS: QVG4-98K8 (Henry), QVG4-98JK (Anna), 4K6D-BN3Z (Frederick), 4KC1-M2T2 ("Mary Anne Berkmeier Meier").

##### US census images (read)
- **1870**, East Ward, Hazleton Borough, p. 42, 8 Jun 1870: the Meyer household. Image: source G7GQ-XGX image 0.
- **1880**, Hazleton Borough East Ward 1st Dist., ED 137, p. 13 (stamped 489), 11 Jun 1880, dwelling 111, family 133: the Myer household, including Gabriel Bergenmyer. Image: source G921-25N image 0.
- **1910**, Wilkes-Barre Ward 14, ED 158, sheet 20B, 28 Apr 1910, 14 Mill St (dwelling 376, family 388). Image: LRRX-MYZ image 2.
- **1920**, Wilkes-Barre Ward 15, ED 262, sheet 6A, 7–8 Jan 1920, 298 Barney St. Image: LRRX-MYZ image 0.
- **1930**, Wilkes-Barre Ward 15, ED 40-261, sheet 23B, 14 Apr 1930, 55 Cedar St. Image: GF3P-853 image 2.
- **1940**, Wilkes-Barre Ward 15, ED 40-330, sheet 3B, 3 Apr 1940, 16 Barney St. Image: LBV1-4CM image 0.
- **1950**, Wilkes-Barre ED 40-102, sheet 2, 7 Apr 1950, house 55. Image: GF3P-853 image 0.
- **1870**, Mahoning Twp., Montour Co. (P.O. Danville): the Edward McGuire household. Image: 994Z-27X image 0.
- **1950**, ED 40-18, Bear Creek Twp.: the Harry J. Meier family (not kin). https://1950census.archives.gov/iiif/2/1950census%2F43290879-Pennsylvania%2F43290879-Pennsylvania-136016%2F43290879-Pennsylvania-136016-0023.jpg/full/2400,/0/default.jpg
- **1950**, ED 40-151: Henry Meier, 27, wife Laura, 24, daughter Rosann, 3 (not Henry J.). https://1950census.archives.gov/iiif/2/1950census%2F43290879-Pennsylvania%2F43290879-Pennsylvania-053512%2F43290879-Pennsylvania-053512-0016.jpg/full/2400,/0/default.jpg
- **1950**, ED 40-126B: Oswald E. Meier, 65, widower, born Germany, landscaper, living with son-in-law Henry W. Lingertot (not kin). https://1950census.archives.gov/iiif/2/1950census%2F43290879-Pennsylvania%2F43290879-Pennsylvania-230745%2F43290879-Pennsylvania-230745-0004.jpg/full/2400,/0/default.jpg

##### Marriage records (Luzerne County, images read)
- Marriage licence docket No. 11054 (Orphans' Court): Henry J. Meier × Annie A. Higgins. Licence 10 Feb 1892; married 1 Mar 1892, Hazleton. The officiant is read as "Rev. Nich. Fo[rve?]" or "Rev. Nich. Gow…". Images: LTHM-1XV image 1 and LBV1-4CM image 1.
- Marriage licence application No. 10768, sworn 16 Apr 1926: William F. Meier × Florence Louise Pringle, married 20 Apr 1926 by Rev. D. W. McCarthy. Images: LTHM-B3G image 1 and LHHT-GQ4 image 2.
- Marriage licence No. 635, 19 Jun 1923: Frank J. McGuire × Elizabeth M. McAvoy, married 20 Jun 1923 by Rev. P. J. Colligan, Plymouth. Image: GZQT-YKQ image 2.

##### Pennsylvania death indexes (PA State Archives, scanned PDFs; read as images)
- 1911 M–N–O, PDF p.171: Meier, Mary A., file 113353, Hazleton, Dec. 30. https://www.phmc.state.pa.us/bah/dam/rg/di/r11_090_DeathIndexes/Death_1911/D-11%20M-N-O.pdf
- 1913 M–N–O, PDF p.174: Meier, Frederick, file 14339, Hazleton, Feb. 19; also Meier, Jacob, file 2939, Hazleton, Jan. 6. https://www.phmc.state.pa.us/bah/dam/rg/di/r11_090_DeathIndexes/Death_1913/D-13%20M-N-O.pdf
- 1958 M–N–O, PDF p.100 / printed p.1324: McGuire, Frank J, 59, Wilkes-Barre, 09-15-58, file 83855. https://www.phmc.state.pa.us/bah/dam/rg/di/r11_090_DeathIndexes/Death_1958/D-58%20M-N-O.pdf
- 1963 M–N–O, PDF p.150: Meier, William F, age 59, Wilkes-Barre, county 40, 07/04/63, file 071200, residence code 40001. https://www.phmc.state.pa.us/bah/dam/rg/di/r11_090_DeathIndexes/Death_1963/D-63%20M-N-O.pdf
- PA State Archives death-records page: https://www.pa.gov/agencies/phmc/pa-state-archives/research-online/vital-records/death-records

##### GEDBAS (genealogy.net): "Familien aus dem Dreisamtal" (compiler Klaus Kiesel, about 30,000 people), the Heitzmann file, and others
- Begelspacher / Wiederle / Lickert: 1444212307 (Matthias Begelspacher), 1444212308 (Barbara Wiederle), 1444212294 (Martin Begelspacher), 1444212306 (Josef, b. 1704).
- Schirk / Steiert / Thoma: 1444214156 (Ottilia Schirk), 1262182131 (Agatha Steiert at the Schirkenhof), 1444214165 (Christian Steiert, formerly Steinhart), 1444214166 (Maria Thoma), 1444214153 (Agatha Steiert, bapt. 1665).
- Heitzler, Ibental: 1262173156 (Jakob Heitzler and children), 1262174650 (Andreas, Vogt), 1262175038 (Jakob, 1781–1847), 1262178929 and 1262178930 (elder Josef and Katharina Schlupf), 1420120011 (teacher Joseph), 1420126661 and 1420126660 (Maria Anna, 1813, and Gremmelspacher), 1262187947 and 1420122854 (Josef "vom Jägerhof", mayor).
- Heitzler, Wehrlehof: 1262183134, 1262183135, 1262183140, 1262183142, 1262183143.
- Heitzler, other: 1262189414 (Agatha Heitzler c.1810, Stegen).
- Birkenmaier and Fürderer: 1420125755 (Johann Birkenmaier 1762–1847 × Gertrud Steinhart), 1013621643 (Mathias Birkenmaier c.1718–1803 × Maria Schmid), 1370130587 and 1370130568 (Munzingen Birkenmayer/Schuhmacher), 84206299 (Johann Birkenmeier, b. 1808, Basel mason), 1262179755 (Augustin Birkenmaier), 1262179509, 1262180212 and 1262179508 (Birkenmaier weavers, sawyers, day labourers), 1444211359 (Fürderer/Förderer).
- Other: 1370049904 (Rosalia Dämpfle), 1260449205 (Heinrich Julius Graf von Kageneck), 1439409820 (August Frederick Meier, b. 1889 Hazleton, Grace Reformed; same surname only).
- Searches by surname list: Kirchzarten Birkenmaier https://gedbas.genealogy.net/search/simple?firstname=&lastname=Birkenmaier&placename=Kirchzarten&timelimit=none ; Begelspacher https://gedbas.genealogy.net/search/simple?lastname=Begelspacher&placename=&timelimit=none ; Fürderer https://gedbas.genealogy.net/search/simple?firstname=&lastname=F%C3%BCrderer&placename=&timelimit=none ; Kaltenbach https://gedbas.genealogy.net/search/simple?lastname=Kaltenbach&placename=&timelimit=none

##### Ancestry index snippets (pages return HTTP 403; seen only through search-engine snippets)
- "James Meier" records, https://www.ancestry.com/genealogy/records/results?firstName=james&lastName=meier : b. 13 Jul 1928, PA; parents Wm F. Meier and Florence L. Pringle; d. 13 Aug 2008, Levittown.
- "Kathryn Meier" records, https://www.ancestry.com/genealogy/records/results?firstName=kathryn&lastName=meier : b. 22 Aug 1930, d. Sep 1970; parents "Frances" McGuire and Elizabeth McAvoy-McGuire.
- "Joseph Birkenmeier" records, https://www.ancestry.com/genealogy/records/results?firstName=joseph&lastName=birkenmeier : b. 15 Mar 1842 Münzingen; parents Servatius Birkenmayer and Agatha Heitzler; d. 3 Nov 1904 Sandusky. The record type was not seen (probably "Germany, Select Births and Baptisms" or a member tree).
- William Meier search, https://www.ancestry.com/search/categories/34/?name=William_Meier&birth=1904&death=1964 : William F Meier, b. 26 Dec 1905, d. 8 Jan 1964; William A. Meier, b. 1904, d. 10 Mar 1964 (probably other men).

##### Newspapers (Chronicling America / loc.gov API)
- Freeland Tribune:
  - 26 Sep 1889 p.1 (Fred Meyer of Hazleton and son Joseph)
  - 23 Jul 1891 (Annie Higgins × John Shovlin)
  - 5 Jan 1893 p.1 (Fred. Meier, Democratic conferee)
  - 25 Sep 1893 and 12 Sep 1895 (Higgins families of Freeland)
  - 23 Nov 1896, 22 Feb 1897 and 12 Jul 1897 (Mrs. Anna Meier and Rockafellow)
  - 14 Feb 1898 (Lattimer trial, "Andrew Meier")
  - 18 Feb 1903 (Joseph Meier Sr., Republican candidate for supervisor)
  - URL pattern: https://www.loc.gov/resource/sn87080287/YYYY-MM-DD/ed-1/?sp=1
- Scranton Tribune, 9 Jul 1897 p.8: https://www.loc.gov/resource/sn84026355/1897-07-09/ed-1/?sp=8
- Scranton Wochenblatt, 5 Jul 1895 p.7 and 12 Apr 1895 p.7 (Kirchzarten news, Graf Max von Kageneck): https://www.loc.gov/resource/sn86053936/1895-07-05/ed-1/?sp=7

##### Local transcriptions
- Genealogy Trails Luzerne:
  - 1933 deaths M–N (Florence Irene Meier): http://genealogytrails.com/penn/luzerne/1933_deaths/1933_m_n.html
  - 1940 deaths M–P (Anna Meier, Mrs. Frederick; McAvoys): http://genealogytrails.com/penn/luzerne/1940_deaths/m_n_o_p.html
  - 1931, 1935 and 1938 McAvoy deaths, and Bea Ginley McGuire (1938): /1931_deaths/1931_m_n.html, /1935_deaths/m_n_o_p.html, /1938_deaths/m_n_o_p.html
  - Luzerne baptisms (Christ Lutheran, Hazleton): http://genealogytrails.com/penn/luzerne/baptism_records.html
  - Hazleton deaths 2003: http://genealogytrails.com/penn/luzerne/2003_deaths_haz/2003_m.html
- PAGenWeb Luzerne:
  - 1912 almanac (William Meier, 45; 1912 McGuire deaths): https://pagenweb.org/~luzerne/mixed/klm1912.htm
  - Wills M (Anton Meier, Black Creek 1912; Joseph Meier, Foster 1912; William Meier, Book 32 p.106): https://www.pagenweb.org/~luzerne/wills/will-m.htm
  - 1893 and 1894 marriages (White Haven Meiers): https://www.pagenweb.org/~luzerne/newspaper/1893marr.htm , /1894mar.htm
  - 1946 WWII casualties (Harry Meier, "missing"): https://pagenweb.org/~luzerne/military/1946casmz.htm
  - Cemetery list (Holy Trinity German Catholic): https://pagenweb.org/~luzerne/township/cemetery/cemlist.htm
  - Census index: https://luzerne.pagenweb.org/census.htm
- Find a Grave memorial 139403232 (Addison F. Pringle; 1943 obituary naming "Mrs. William Meier" of Wilkes-Barre): https://www.findagrave.com/memorial/139403232/addison-f-pringle

##### Context and secondary sources
- Hilger, *Auswanderer aus dem Schwarzwald*, Badische Heimat 80, pp.598–603: https://regionalia.blb-karlsruhe.de/files/21412/BLB_Hilger_Auswanderer_Schwarzwald.pdf
- Langenbeck, *Hofnamen des Schwarzwaldes*, Alemannisches Jahrbuch 1962/63, pp.100–101: https://regionalia.blb-karlsruhe.de/files/19081/blb_Langenbeck_Hofnamen_Schwarzwald.pdf
- Buchenbach Mitteilungsblatt, 2 Feb 2023 (Jägerhofsäge): https://www.buchenbach.de/eip/media/mitteilungsblatt/mitteilungsblatt_403_1.pdf
- de.wikipedia, Kageneck (Adelsgeschlecht); archINFORM, Schloss Munzingen https://www.archinform.net/projekte/29492.htm ; en/de.wikipedia Kirchzarten and Buchenbach; Wikipedia: Baden Revolution, Breisgau, Höllental, Hazleton, Danville and Levittown PA; wissen.de Zarten; University of Tübingen (Tarodunum); LEO-BW Buchenbach; bpb (German emigration figures); Rome Sentinel (Herrenwies); oocities Bühlertal Migration; Wikipedia: Servatius of Tongeren.
- WikiTree API, Birchenmayer-2 (Maria Birchenmayer, 1698–1766, Zarten): https://api.wikitree.com/api.php?action=getProfile&key=Birchenmayer-2
- Wilkes University cemetery data page: https://klemow.wilkes.edu/cemetery.html
- Reclaim the Records, NYS Death Index CSVs 1880–1971 (archive.org): https://archive.org/details/reclaim-the-records-new-york-state-death-index-1880-1971 . This gave the Henry Meier deaths at Huntington, 21 Jul 1931 (#44888), and Hempstead, 24 May 1937 (#34005), and Henry K. Meier, 65, Huntington, 1955 (too young).

#### B. Searches that came back empty or were blocked (do not repeat)

##### Germany
- **Kirchzarten / Dreisamtal database (GEDBAS, about 30,000 people; about 90 Neuhäuser Birkenmaiers, 1600–1906).** Not found: Servatius; a Maria Anna Birkenmayer b. c.1837; Johann E. Birkenmaier 1771–1844; Magdalena Erb; Caecilia Hohler; a Friedrich/Fridericus Maier/Mayer/Meier/Meyer b. c.1835 (at Kirchzarten, Stegen, Buchenbach, Oberried, St. Märgen, St. Peter, Freiburg or Munzingen; the only Fridolin Maiers are from 1823 and 1827); a Heinrich Maier as a father in the 1830s (the only ones were born 1847, 1854 and 1900); a Heitzler–Fürderer marriage. These are now explained: the family was from Munzingen.
- **GEDBAS, all files.** Not found: Friedrich Meier/Maier/Mayer b. 1830–39 (only unrelated hits in Württemberg, Pfalz, Bukovina and Lodz); any Servatius; any Erb in the Breisgau or in Munzingen; any Hohler in Baden; a Stephan Birkenmaier; a Juliana Senn; a Heinrich Mayer of Freiburg or Munzingen; a Wenz of Munzingen; a Federer in Munzingen.
- **Online-OFB (online-ofb.de).** There is no Ortsfamilienbuch for Kirchzarten, Buchenbach, Stegen, Oberried, St. Märgen, St. Peter or Munzingen.
- **WikiTree API.** No Servatius; no Frederick/Friedrich Meier b. 1835; no Henry Meier b. 1866 (PA); no relevant Birkenmayer. WikiTree began blocking requests partway through round 3.
- **LABW emigrant database** (auswanderer-bw.de / leo-bw themenmodul; about 250,000 people, mainly 1850–1900, and only those who formally renounced citizenship): HTTP 403. auswanderer.lad-bw.de gave a TLS error.
- **Deutsche Auswanderer-Datenbank (Bremerhaven; DAD / *Germans to America*).** Searched Meier, Meyer, Maier, Mayer, Mayr, Meir and Myer for 1866–1869, with first-name prefixes Friedr, Fr, Heinr, Franz and Maria, plus a full A–Z first-name sweep of Meyer for 1867. No group matched Friedrich ~32, Maria ~30 and children ~5, ~4, ~2 and ~1. The nearest group (1867, IDs 4004342–47) is a different family with a wife Charlotte. Results are capped at 100; details are a paid service.
- **FamilySearch German church-record images** (Freiburg archdiocese): HTTP 403. The index pages at familysearch.org/ark return 401.
- **L 10 Nr. 1590 deaths 1816–1831.** The scan was not finished: these years are running text and the margin names were unreadable at the resolution used. Michael Mayer, Juliana Senn the elder, Joseph Heizler and Magdalena Erb were not found there yet.

##### United States: the Meiers
- **PA death index (Soundex M600 = Meier/Meyer/Maier/Mayer/Moore).**
  - 1939 M–O p.34: no Henry/Harry in Luzerne (county 40).
  - 1940 L–M pp.269–270 and p.1426: the only Henry J Meyer is in Erie (county 25), d. 18 Nov 1940; not ours.
  - 1941 M–N p.34: Henry Maier, Philadelphia, 2 Nov 1941, file 23300; Henry Meyer, Wilson borough (Northampton), 23 May 1941, file 49919; Harry J. Meyer, Philadelphia. None in Luzerne.
  - 1933 (Florence Irene): not found; nearest is Florence E. Moyer, file 89261.
  - Years after 1966 are not online.
- **NYS Death Index outside NYC, 1931–71.** No Henry J. Meier of a fitting age. No Kathryn/Katherine/Catherine Meier/Meyer/Maier/Myers in 1969–71, and no M600 woman aged 38–42 in 1970. NYC is not covered.
- **NJ death index 1930–48:** not online at Reclaim the Records (it has only 1901–03, 1916–29 and 1949 on).
- **Wilkes-Barre newspaper death lists 1929–40 and 1945:** no Henry, Harry or Anna (Higgins) Meier.
- **Chronicling America.** All PA titles, 29 Dec 1911–15 Jan 1912 and 18 Feb–10 Mar 1913: no Meier/Meyer/Myers/Maier obituary. Freeland Tribune: all 18 "Meier" pages read, and the 321 "Meyer" and 98 "Higgins" pages filtered. Scranton Wochenblatt checked. Birkenmayer variants: zero hits in any PA title, 1850–1963. There is no Meier–Higgins marriage notice, and the Hazleton dailies (Standard, Sentinel, Plain Speaker) are not digitized.
- **PAGenWeb Luzerne (about 1,700 pages crawled).** Covered: wills, 1893–95 marriages, the 1903, 1912 and 1915–16 almanacs, the St. Gabriel's Irish stones, census transcriptions 1860–1920 (including 1870 Hazle East/Drifton/Foster, 1880 and 1900 Hazle Twp., and 1920 Hazleton and West Hazleton), church histories, and the Christ Lutheran Hazleton records. No Frederick, Mary, Henry or Anna Meier and no Birkenmayer.
- **Genealogy Trails Luzerne.** Covered: death lists 1929–40 and 1945, Hazleton deaths 2003–11, the 1940 census index (no Meier on the M page), naturalization index pages, WWI and Korea pages, and the grave index. Nothing beyond the 1933 Florence Irene notice.
- **1950 census name index (NARA API).** Searched Meier, Meyer, Maier, Mier, Meir, Myer, Mayer, McGuire, Maguire and "Mc Guire" in Luzerne. The OCR index has only 14 Meier and about 11 McGuire pages for the whole county, and none was William, Florence, James, Kathryn, Francis or Elizabeth. (Round 3 found the 1950 Meier household through FamilySearch instead.)
- **Bradsby, *History of Luzerne County* (1893)**, full text at https://archive.org/details/historyofluzerne00brad : no Meier on this line. Its Hazleton Meyers (Raymond E., Robert H. "E. H.", Catherine E. Lonzer) are other families. The usgwarchives copy returned HTTP 503 in round 2.
- **archive.org.** No Hazleton or Wilkes-Barre city directories. Schuylkill directories exist only for 1867–68, 1881–82 and 1883–84; the 1867–68 Boyd's has no Meier/Mayer Friedrich in Tamaqua or Pottsville. No Tamaqua directory for 1904–06. No 1900 census image is attached to any profile in the family.
- **1889 *History of Erie County, Ohio*** biographies (B): no Birkenmeier. https://ohiogenealogyexpress.com/erie/erieco_1889_bios/erieco_1889_bios_b.html
- **Blocked (HTTP 403 or login):** Find a Grave (every page and search); the Wayback Machine; Ancestry; FamilySearch record and census search (needs login); pennsylvaniagravestones.org; sortedbyname.com (SSDI); the RootsWeb freepages Wilkes-Barre Almanac; the VA Gravesite Locator and Veterans Legacy Memorial; Castle Garden (connection reset). The Ellis Island site covers arrivals only from 1892 on. WWII draft cards are behind Ancestry, Fold3 and FamilySearch.
- **Not found at all:** obituaries for William F. (1963) and James C. (2008, Legacy.com and Times Leader); James's military service; Henry's and Friedrich's naturalization papers; Frederick and Mary A.'s Hazleton cemetery.
- **Wilkes University cemetery datasets:** they store only three-letter surname codes plus initials, so they are unusable.

##### United States: the McGuire, McAvoy and Higgins side
- No web hits for Peter McAvoy & Mary Doran, or for William Higgins & Mary Ann Reilly (including a William Higgins of New Philadelphia).
- FamilySearch Irish register images (Edward McGuire's baptism, the Owen McGuire entries) return 0-byte files because of image-rights restrictions.
- irishgenealogy.ie and askaboutireland.ie are blocked by a Cloudflare challenge.
- No online record of a Meier–Higgins link in Luzerne before round 3.

##### False leads already resolved (do not chase)
- FamilySearch "Henry Higgins (1866–1940)", MWTJ-M9C: Bethnal Green, London / Outremont, Quebec; unrelated.
- Harry J. Meier of Bear Creek Twp. (1950 census, ED 40-18): a New York family; not kin.
- Mrs. Frank McGuire (Bea Ginley), d. 26 Apr 1938, Forty Fort: a different Frank McGuire.
- The Ebringen Birkenmeyer family (New Orleans, 19 Feb 1855; St. Louis): not Maria Anna's family.
- Maria Anna Heitzler, b. 8 Apr 1813 (the teacher's daughter), and the Wehrlehof Joseph Heitzler: not Agatha's family.
- "Andrew Meier", wounded at Lattimer in 1897: a Slavic striker, not kin.
- The White Haven Meiers (George F., Gottlieb, Isaac, Frederick F., d. 1963): Lutheran/Reformed, probably a separate family.
- August Frederick Meier, b. 1889 Hazleton (Grace Reformed; parents August Meier & Dorothea Schimmelpfennig): Protestant; probably a different family.
- Philipp Birkenmaier (b. 1975, Tübingen; Chancellor Merz's chief of staff since Jan 2026): same surname only, and from Württemberg.
- Adolf Wehrle (1846–1915) and the Winterhalder sculptors (Philipp, 1667–1727; Clemens, 1668–1696) of Kirchzarten: same place only.

### 6.2 Pringle, Heffernan and the Pennsylvania lines (with Irish, Palatine German and French Huguenot roots)

Research files these come from: `research/tree_transcription.md`; Round 1/2/3 reports (`Johnny_Meier_Lineage_Report_2026-10.md`, `_Round2_`, `_Round3_`); `notes/pa_lines.md`; `notes/round2/irish_pa_gaps.md`; `notes/round3/irish_pa.md`; `notes/round3/english_french_origins.md`; `notes/round2/colonial_cousins.md`; `notes/round3/german_origins.md` (Grub/Doll parts); John's upload "Old Records Reshape Johnny Meier's Family Tree" (deep-dive); `Ancestry tree screenshots (section 2.2.2)`.

#### A. Primary records (images or official indexes read)

| Source | Citation / URL | What it gave |
|---|---|---|
| 1850 US census, Plymouth Twp, Luzerne Co. (NARA M432) | Enumerated 14 Sep 1850 by A. Atherton, page 140/141 (stamp 71); attached on FamilySearch to Andrew Pringle 1836–1900 (KG4S-XMF); John's screenshot IMG_7813 | Dwelling 944/fam 964: James Pringle 51 farmer $500 PA, Elizabeth 48, Alby 27, Noah 16, Andrew 14 (line 38), Leva Ann 11, Edwin 9. Dwelling 942/962: Hulda Pringle 46 $600 NY, Orange 23 teamster, Ransom 21, Caturah 17, Jane 14, Lucinda 10, Sarah 6, Lucy Ives 87 (insane), Philip Minchart 26 carpenter. Neighbours 943/963 Jenkins Jones 36 miner Wales; 945/965 Thomas Gould 39 farmer $2,500 |
| 1850 US census, Kingston Twp | 3 Aug 1850, dwelling 262: https://ancestors.familysearch.org/service/tree/tree-data/published/sources/9KXX-MH8/images/i/0/image.jpg | Stephen Scott 44 farmer b. Pa.; Julia Ann 41 b. Pa.; Henry 21; Catharine 14; Hannah 10; Caroline 9; Ann 4; neighbours Zeba Hoyt, Shoup, Steinhower, Beck, Davis |
| 1880 US census, Plymouth Twp (E. Dist., 3d Div.) | ED 145, p.4, 4 Jun 1880: https://ancestors.familysearch.org/service/tree/tree-data/published/sources/LHHH-W68/images/i/0/image.jpg ; https://familysearch.org/ark:/61903/1:1:MWNZ-S9X | Andrew Pringle 44 laborer; Katharine 43; John 20; Samuel 17; "Adason" 15 laborer; Orange 13 slate picker; Stella 5; next door Emma Pringle 15 servant; John Comerford household (Ireland) nearby. Also gives Catherine's parents as b. Penn. |
| 1880 census (Plymouth) | cited by Dwyer | "Catherine Heffressen", 66, with daughter Catherine Healy |
| 1860 census Plymouth | cited Round 2 | "Anna S. Heppen" 47 with son James and Jeremiah Boney 30 |
| 1870 census Plymouth | cited Round 2 | James Boney 22, miner, in a Heffernan household |
| 1900 census | cited Dwyer | John Heffernan immigration 1866 |
| 1910 census Plymouth/Larksville | cited Dwyer; FamilySearch residence events | Addison & Catherine Pringle's 8 children incl. Florence (6); family at Larksville |
| 1930 census Wilkes-Barre Ward 15, ED 40-261, sheet 23B, 14 Apr 1930 | https://ancestors.familysearch.org/service/tree/tree-data/published/sources/GF3P-853/images/i/2/image.jpg ; index https://familysearch.org/ark:/61903/1:1:XH7Z-MLW | William F. & Florence Meier at 55 Cedar St; Addison Pringle at 28 Huston St on same sheet |
| 1950 census Wilkes-Barre ED 40-102, sheet 2, 7 Apr 1950 | https://ancestors.familysearch.org/service/tree/tree-data/published/sources/GF3P-853/images/i/0/image.jpg ; index https://familysearch.org/ark:/61903/1:1:6X1W-JY84 | House 55: William F. 45, Florence 45, William Jr. 23, James C. 21, Barbara Ann 14 |
| Luzerne marriage-licence application No. 10768 (sworn 16 Apr 1926) | https://ancestors.familysearch.org/service/tree/tree-data/published/sources/LHHT-GQ4/images/i/2/image.jpg ; https://familysearch.org/ark:/61903/1:1:KMZX-RZZ ; groom https://ancestors.familysearch.org/service/tree/tree-data/published/sources/LTHM-B3G/images/i/1/image.jpg ; index KMZX-RZ4 | Florence Louise Pringle, clerk, b. Plymouth, 22, 28 Huston St; father Addison (carpenter, b. Penna); mother Catherine Heffernon; married 20 Apr 1926 by Rev. D. W. McCarthy |
| Luzerne marriage licence No. 1732 (1936), Francis Pringle | https://ancestors.familysearch.org/service/tree/tree-data/published/sources/LHHH-W68/images/i/2/image.jpg | Parents "Addison F." and "Catherine Heffernan" |
| Luzerne Register of Deaths p.208 (1904) | https://ancestors.familysearch.org/service/tree/tree-data/published/sources/LB2N-F9R/images/i/1/image.jpg | "Hefferan, Catharine, F, 90, b. Ireland, d. Plymouth 18 Apr, interred Plymouth 20 Apr, parents Thos & Ann Boney" |
| Philadelphia marriage application, 24 Nov 1914 | https://ancestors.familysearch.org/service/tree/tree-data/published/sources/L2G4-NQW/images/i/1/image.jpg | Dr. Andrew J. Heffernan × Lillian T. MacDonald; father Andrew H. b. Ireland, clerk; mother Mary Connole b. New York |
| PA death index 1943 P–R | https://www.phmc.state.pa.us/bah/dam/rg/di/r11_090_DeathIndexes/Death_1943/D-43%20P-R.pdf (PDF p.97 / printed p.1695) | ADDISON F PRINGLE, WLKS BRE, P652, co. 40, 9-2-43, file 82141 |
| PA death index 1947 P–R | https://www.phmc.state.pa.us/bah/dam/rg/di/r11_090_DeathIndexes/Death_1947/D-47%20P-R.pdf (PDF p.94 / printed p.1649) | CATHERINE E PRINGLE, WLKS BRE, co. 40, 4-23-47, file 35591 |
| PA death index 1933 M–N | https://www.phmc.state.pa.us/bah/dam/rg/di/r11_090_DeathIndexes/Death_1933/D-33%20M-N.pdf (pp.42, 44) | No Florence Irene Meier (nearest: Florence E. Moyer, d. 17 Oct 1933, file 89261 - different) |
| PA death certificate, Andrew H. Heffernan, 8 May 1919 | cited by Dwyer | d. 6 May 1919 Wilkes-Barre; burial St. Vincent's Plymouth 9 May 1919 |
| PA 1853 death & burial record, Benjamin Pringle | via WikiTree Pringle-3406 | Names "Sam Pringle & Martha" |
| Thomas Lamoreaux will | 15 Apr 1815, codicil 9 Nov 1826, registered 5 Oct 1829, Luzerne Co. Will Book A pp.341–3; transcription WikiTree Lamoreaux-21 (citing FamilySearch images) and http://www.pagenweb.org/~luzerne/patk/tomlam.htm | Names wife Keturah, daughter "Martha Pringle", all children; disinheritances |
| Philip Croop will, 1812 | Luzerne Will Book A p.128 (via WikiTree Croup-9) | "my dear brother Frederick Grupe" co-executor |
| Andreas Grub will, 11 Nov 1791 | Northampton Co. Register of Wills file #1430 (via WikiTree Grub-4) | Children and executors |
| Maria Elisabetha (Christmann) Grub will, 1810 | via WikiTree Grub-4 | "her son Frederick Krub" |
| Luzerne wills index P | https://pagenweb.org/~luzerne/wills/pwill.htm | Huldah Pringle 1887 (Plymouth Boro., vol. J p.499); Phebe Pringle 1867 (vol. D p.344); Ellen C. Pringle 1898; no Andrew G. Pringle |
| Strassburger & Hinke, *Pennsylvania German Pioneers* vol. 1 | https://archive.org/details/pennsylvaniagerm42stra (p.634 grub) | *Phoenix* 1 Oct 1754 List 222 (Andreas Grub; Johannes Young/Jung); *Samuel* 27 Aug 1739 List 69 A–C (Casper Doll 18, Stoffel 40, Philip 27, Christ. Shook 48, Simon Drum); *Samuel* 30 Aug 1737 List 44 (no Casper) |
| Church records of the Williams Twp. Congregation | https://archive.org/details/churchrecordsofw00will/page/19/mode/1up?q=Andreas | Andreas Grub 1759; separate Andreas & Catharina Grub 1748–51 |
| Registers of the French Church of New York (Coll. HSA vol. 1, 1886) | https://archive.org/details/collectionsofhug01hugu (pp.29–31) | Masse baptisms 1689, 1693, 1696; Mersereau marriages 1693; Daniel Lamoureux son bapt. 29 May 1720 |
| Lart, *Registers of the French Churches of Bristol, Stonehouse and Plymouth* (Huguenot Soc. London vol. 20) | https://archive.org/details/registersoffrenc20hugu/page/n40/mode/1up (p.9) | Daniel Lamoureux bapt. 1 Dec 1695; André "pillotte" of Meschers |
| Shaw, *Letters of Denization 1603–1700* | https://archive.org/details/lettersofdenizat01shaw/page/235/mode/1up (p.235) | André Lamoureux denization 22 Jun 1694 |
| Garner, *French Reformed Church, Cozes, Saintonge: Baptisms 1655–1668* | FamilySearch Books; FHL film 1868505 item 5 (pp.1, 48, 69) | André bapt. 1663; Suzanne La Tour bapt. 1666; 1656 Daniel/Jean Lamoureux |
| *Pa. Archives* 5th ser. vol. VIII p.120 | via WikiTree Croup-9 | Philip Grub, 5th Co. (Easton), 5th Battalion, Northampton militia 1777–80 |
| Time, 31 Mar 1923 | https://archive.org/details/sim_time_1923-03-31_1_5 | Leo Heffernan 250-mph flight |
| Army & Navy Journal 9 Oct 1915; 9 Jun 1917; 13 May 1933; Army Navy Air Force Journal 18 & 25 Feb 1956 | https://archive.org/details/sim_armed-forces-journal_1915-10-09_53_6 ; ..._1917-06-09_54_41 ; ..._1933-05-13_70_37 ; ..._1956-02-18_93_25 ; ..._1956-02-25_93_26 | Leo's career, retirement, death (7 vs 9 Feb 1956) |
| Air Corps News Letter 31 Mar 1928; 23 Sep 1930; 28 May 1932; 31 Jul 1933 | https://archive.org/details/sim_air-force-magazine_1928-03-31_12_5 ; _1930-09-23_14_11 ; _1932-05-28_16_6 ; _1933-07-31_17_7 | Technical School, France Field, retirement |
| Aviation 3 Jul 1922; Cavalry Journal Apr 1925; Journal of Education 26 Apr 1923; Elyria Chronicle-Telegram 24 Mar 1923 | https://archive.org/details/sim_aviation-week-space-technology_1922-07-03_13_1 ; https://archive.org/details/sim_armor_1925-04_34_139 ; https://archive.org/details/sim_journal-of-education_1923-04-26_97_17 ; https://archive.org/details/elyria-chronicle-telegram-1923-03-24 | Leo's 3rd Attack Group; article; "Outspeeding the Birds" |
| Editor & Publisher 23 Jan 1960; 5 Aug 1972 | https://archive.org/details/sim_editor-publisher_1960-01-23_93_4 ; https://archive.org/details/sim_editor-publisher_1972-08-05_105_32 | Heffernans still running Sunday Independent |
| Newspapers quoted by Dwyer | W-B Record 19 Apr 1904 (Catherine Boney obit); W-B Times 17 Nov 1904 (John Heffernan obit); W-B Record 31 Mar 1906 (Josephine nurse); Sunday Independent 1 Sep 1918 ("Married Fifty Years"); The Sun (NY) 29 Jul 1880 and W-B Record of the Times 30 Jul 1880 (Dillon shooting); W-B Times-Leader 17 Apr 1909; Evening News 16 Apr 1927 | as cited |
| Republican Farmer (Wilkes-Barre), 13 Mar 1833 | via WikiTree Tuthill-530 | Keturah Lamoreaux obituary, d. 10 Mar 1833 |
| NSW death certificate 5288/1869 | via Dwyer | Patrick Heffernan d. Orange NSW 10 Dec 1869 |

#### B. Compiled genealogies and county histories

| Source | URL | What it gave |
|---|---|---|
| Michael Dwyer, *Heffernans of Slieveardagh* (Welsh Hill Press, 2020) | https://archive.org/details/heffernans-of-slieveardagh | Killenaule/Gortnahoe register readings: Andrew bapt. 1842; Thomas bapt. 1808, m. 1833; Humphrey & Anastasia Ryan; Catherine Boney bapt. 1814; Branches 1–4; children of Andrew & Mary; transportations; photo credits (Leo 1917 portrait, Library of Congress; Thomas F. portrait, *Prominent Men, Wilkes-Barre* 1906) |
| H. C. Bradsby, *History of Luzerne County* (1893) | https://archive.org/details/historyofluzerne00brad ; transcriptions https://pagenweb.org/~luzerne/bios/sabios.htm and https://pagenweb.org/~luzerne/bios/wibios.htm | Catherine Scott sketch (p.~1327); John F. Connole (p.~795); Keating (pp.~1049–50); Croop (pp.584, 613–614, 812–813); Bisher/Ives (pp.716–717); John Pringle/Phoebe Davenport (pp.1483–84); Ransom Pringle; runaway apprentice ad |
| O. J. Harvey, *The Harvey Book* (1899) | https://archive.org/details/harveybookgiving00harv | Pringle origin (pp.134–136); Thomas Pringle; George Lane Pringle (p.137); Shupp/Croup (pp.343, 354); Lamoreaux/Davenport (pp.355–357); Keturah (p.360); Jacob Pringle (p.362); Noah (pp.370–371); Charity Mekeel (p.1020) |
| Harvey & Smith, *History of Wilkes-Barre* vols. III–VI | https://archive.org/details/historyofwilkesb03harv ; ..04harv ; ..05harv ; ..06harv (vol. VI p.460: https://archive.org/details/historyofwilkesb06harv/page/460/mode/1up); vol. V part 17: https://ldsgenealogy.com/PA/books/A-history-of-Wilkes-Barre-Luzerne-County-Pennsylvania-from-its-first-beginnings-to-the-present-time-including-chapters-of-newly-discovered-early-Wyoming-Valley-history-Volume-V-part-17.htm | Heffernan family (VI p.460); Dr. A. J. Heffernan (V p.346, "died 1912" error); Connole/Dailey doctors (VI pp.~422, 436, ~475); Pringle Borough (V p.165); A. J. Pringle (VI p.378); Asa Upson / Dutch Fishery (III); 1818 bridge strike and postmaster list (IV); Croop's Glen (V–VI); Sunday Independent circulation |
| Munsell, *History of Luzerne* (1880) | https://archive.org/details/historyofluzerne00muns | Croop mills; Ransom Pringle; James & Jonathan Croop |
| H. B. Wright, *Historical Sketches of Plymouth* (1873) | https://archive.org/details/historicalsketch00wrig_2 | Samuel Pringle (pp.308, 391; 1796 assessment); Davenport congress (pp.384–387); stone walls (pp.399–400) |
| Pearce, *Annals of Luzerne County* | https://archive.org/details/annalsofluzernec01pear | Judge Cooper anecdote (p.248); coal operators c.1843 (p.380) |
| Plumb, *History of Hanover Township* (1885) | https://ldsgenealogy.com/PA/books/History-of-Hanover-Township-including-Sugar-Notch-Ashley-and-Nanticoke-boroughs-and-also-a-history-of-Wyoming-Valley-in-Luzerne-County-Pennsylvania-part-38.htm | Abraham Sorber; Elizabeth Sorber m. John Croop; (all 40 parts: no Frederick Croup) |
| Giles & Franklin, *Thomas Davenport, Philipstown Pioneer* (1962) | https://archive.org/details/thomasdavenportp00gile ; HathiTrust https://babel.hathitrust.org/cgi/pt?id=wu.89066038563&view=1up&seq=395 | Davenport ancestry (pp.xiv–xix); Benjamin Pringle family (pp.280–281); Phoebe Davenport Pringle (pp.321–322); Temperance Pringle Davenport (p.329); Lamoreux marriages and 1752 deed (pp.355–361) |
| A. J. Lamoureux, *André Lamoureux, the Huguenot Emigrant, and Family* (1919) | https://archive.org/details/andrlamoureuxh00lamouoft | Lamoureux family; Cornbury release; "Pitter"; "Charity Danforth"; three-brothers myth disproved |
| D. K. Martin, *The Eighteenth Century Lamoureux Family of the Hudson Valley* (2008), pp.40–44 | (not online; cited via WikiTree) | Lamoreaux siblings; Masse origin |
| Clute, *Annals of Staten Island* (1877) pp.408–9 | https://archive.org/details/cu31924028834681 | Jean Mersereau tradition |
| Semans & Broome, *Broome, Latourette and Mercereau Families* | cited via WikiTree | Elisabet Dubois widow of Jean Mersereau |
| *The Prindle Genealogy* (1906) | https://archive.org/details/prindlegenealogy00prin | James Prindle (1736–1800) p.41; Benjamin & David Prindle, privates 1st Regt Orange Co. militia (appendix p.280); no Samuel c.1767, no Lamoreux marriages |
| Ruttenber & Clark, *History of Orange County* (1881) | https://archive.org/details/historyoforangec00rut | 1775–76 militia lists ("Thos. Lammoreux, ensign"); Articles of Association signers |
| Eager, *Outline History of Orange County* (1846) pp.527–529 | https://archive.org/details/outlinehistoryof00eage | Capt. J. Tuthill references (colonial group) |
| Alva M. Tuttle, *Tuttle-Tuthill Lines in America* (1968) pp.279, 311 | FamilySearch Books item 481721: https://www.familysearch.org/library/books/records/item/481721 (login) | Keturah ~1755 Woodbury Clove; parents |
| *History of the Susquehanna and Juniata Valleys* | https://ldsgenealogy.com/PA/books/History-of-that-part-of-the-Susquehanna-and-Juniata-valleys-embraced-in-the-counties-of-Mifflin-Juniata-Perry-Union-and-Snyder-in-the-commonwealth-of-Pennsylvania-V-1-Pt-2-part-26.htm | Capt. Casper Dull |
| *Musket, Saber & Missile* (Fort Bliss history); *Aviation in the U.S. Army 1919–1939*; *Home Field Advantage* | https://archive.org/details/musket-saber-missile-history-of-fort-bliss ; https://archive.org/details/aviationinusarmy0000maur | Leo Heffernan |
| GEDBAS file 53093 ("Helf-Maier", Karl-Hans Helf) | persons 1193192339, 1193191835, 1193192331, 1193192332, 1193191772, 1193191773, 1193191876, 1193191874, 1193191858, 1193191900 at https://gedbas.genealogy.net/person/show/<ID> | Jettenbach Grub ancestry 4 generations |
| GEDBAS other | 1184161404 (Erzweiler Dolls, file 20942); 1435014144 (Maria Engel Doll); 1402009472 (J. C. J. Schuch); 1420550403 (Simon Drumm, citing Burgert) | Doll/Schuch/Sorber leads |
| earlyaviators.com | https://www.earlyaviators.com/eheffern.htm | Leo Heffernan career |
| LDS Church History Biographical Database; Joseph Smith Papers | — | Andrew L. Lamoreaux |
| SAR Patriot database | P-232580 https://sarpatriots.sar.org/patriot/display/232580 ; ACN 75325 https://sarpatriots.sar.org/application/display/54603 ; ACN 58344 https://sarpatriots.sar.org/application/display/60180 ; P-149071, P-150954 (other Doll/Dull) | Thomas Lamoreaux patriot; John → Thomas; Keturah 1755 |
| DAR GRS | A068239 (Thomas Lamoreaux); A068227 (Jean/John Lamoreaux) | Patriot numbers |

#### C. Online trees and indexes (use with caution)

| Source | URL / ID | What it gave |
|---|---|---|
| FamilySearch published tree JSON | `https://www.familysearch.org/service/tree/tree-data/published/persons/{ID}`; IDs LHHT-GQ4 (Florence), LHHH-W68 (Addison), KG4S-XMF (Andrew G.), LHCS-RCM (Catherine Scott), KP7T-1HK (James Pringle), LWNW-RRV (Elizabeth Croup), 9KXX-MH8 (Stephen Scott), KG4S-GMT (Julia Ann), G99D-9DZ → L8MP-W4X (Samuel's Prindle parents) | Dates, burials, residences; errors flagged (Andrew H. "b. 31 Mar 1848"; William Thomas Heffernan b. 1848 RI; James Pringle "1799–1909"; Martha b. 1776; "Daniel Scott 1788–1811"; George Watson/Waterman merge) |
| FamilySearch sitemaps scan | 4,562 sitemap files (~18 GB) scanned for surnames (Round 3 method) | Found the published profiles above |
| WikiTree | Grub-4, Grub-81, Grub-87, Christmann-662, Croup-1, Croup-8, Croup-9, Croop-42, Doll-526, Doll-527, Doll-1206, Dietz-184, Dietz-563, Pringle-3405, -3406, -3407, Lamoreaux-21, -49, -112, -426, Lamoreux-10, Tuthill-530, Masse-21, Mersereau-1, -31, -32, Dubois-163, La_Tour-2, Heffernan-720, Connole-33 (https://www.wikitree.com/wiki/<ID>) | As cited per person |
| Find a Grave | 139403232 (Addison), 139403166 (Catherine E.), 139403710 (Andrew H.), 139403584 (Mary Connole), 139404421 (Dr. A. J.), 49215308 (Sr. Mary Antonia), 183145812 (John F. Connole), 162159301 (Anastasia Boney Connole), 42344464 (Thomas Lamoreaux), 269816651 (Keturah), 28284890 (Andreas Grub), 261051335 (M. E. Christmann Grub), 19353732 (Casper Doll), 21956570 (Capt. Casper Dull), 75273513 (Susan Croup Shupp) | Obituary texts / dates (read via earlier reports and snippets; direct fetch blocked) |
| Ancestry index snippets | https://www.ancestry.com/genealogy/records/results?firstName=james&lastName=meier | James C. Meier b. 13 Jul 1928, parents Wm F. Meier & Florence L. Pringle |
| PA-Roots Civil War rosters (Bates) | https://pa-roots.com/pacw/infantry/paregimentsnew.html ; 52nd Co. G https://pa-roots.com/pacw/infantry/52nd/52ndcog.html ; 149th Co. F https://pa-roots.com/pacw/infantry/149th/149thcof.html ; 203rd Co. K https://pa-roots.com/pacw/infantry/203rd/203dcok.html ; 9th Cav Co. D https://pa-roots.com/pacw/cavalry/9thcav/9thcavcod.html | Caleb Pringle; Andrew, Alvin, James, Jonathan Croop |
| PAGenWeb Luzerne | 1840 census index https://pagenweb.org/~luzerne/census/1840.htm ; Larksville https://pagenweb.org/~luzerne/patk/larks.htm | Stephen Scott Falls Twp (different man); Larksville ("Blindtown") collieries |
| Genealogy Trails 1933 deaths M–N | http://genealogytrails.com/penn/luzerne/1933_deaths/1933_m_n.html | Florence Irene Meier funeral notice 11 Oct 1933 |
| IrelandXO Gortnahoe board | https://irelandxo.com/ireland/tipperary/gortnahoe-tipperary/message-board/information-heffernans-gortnahoe | Corroboration of transportations |
| Surname/place references | John Grenham https://www.johngrenham.com/findasurname.php?surname=Connole ; Library Ireland https://libraryireland.com/names/oh/o-hifearnain.php and https://www.libraryireland.com/irish-families/odwyer.php ; Landed Estates https://landedestates.ie/estate/2874 ; Wikipedia Ballingarry Coal Mines https://en.wikipedia.org/wiki/Ballingarry_Coal_Mines ; ERIH Mardyke https://www.erih.net/i-want-to-go-there/site/mardyke-mine ; Wikipedia Pringle PA https://en.wikipedia.org/wiki/Pringle,_Pennsylvania ; Wikipedia Thomas Cooper https://en.wikipedia.org/wiki/Thomas_Cooper_(American_politician,_born_1759) ; Wikipedia Mersereau Ring https://en.wikipedia.org/wiki/Mersereau_Ring ; Wilkes University cemetery https://klemow.wilkes.edu/cemetery.html | Context |
| Other online trees | Wilsey https://freepages.rootsweb.com/~wilsey/genealogy/pafg277.htm (Samuel c.1770); Schenectady History https://www.schenectadyhistory.org/families/hmgfm/lamoreaux.html ; My Maine Heritage https://sites.rootsweb.com/~megen/reunion/ps409/ps409_195.html ; FamilySearch Bretten Dolls https://ancestors.familysearch.org/en/21R1-HGV/anna-catharina-doll-1734-1790 | Leads / warnings |
| POWER Library (Sunday Independent 1913–58) | https://powerlibrary.org/?p=173 | Identified as best route for obituaries (not yet searched) |
| Heritage Books, Prindle-Pringle Genealogy | https://heritagebooks.com/products/101-w0347 | Next lead (not consulted) |
| John's Ancestry tree screenshots | IMG_7791–7840; IMG_7792, 7794, 7797–7799, 7807, 7808, 7813, 7828 for this group | Tree values recorded per person |

#### D. Searches that came back empty or were blocked (do not repeat blindly)

- **SAR patriot search form**: blocked automated queries (Mod_Security); indexed pages showed no Casper Doll, Andreas/Frederick Grub, or John Young of Northampton – not exhaustive.
- **DAR GRS ancestor search**: JavaScript-only; unchecked for Doll, Young, Grub.
- **irishgenealogy.ie** (civil and church) and **askaboutireland.ie** (Griffith's): Cloudflare JS challenge (HTTP 403) to curl and WebFetch. Cashel & Emly registers are only images at registers.nli.ie anyway.
- **FamilySearch Irish register images** (e.g. Edward McGuire's baptism), **Samuel Pringle's HSP marriage image**, Nancy Holland obituary: 0-byte files (image-rights restrictions).
- **Find a Grave**: HTTP 403 to automated fetches (Round 2); memorials read via earlier reports/snippets.
- **FamilySearch search and HathiTrust**: JavaScript/Cloudflare (Round 2); Ancestry, Geni, Legacy blocked (Round 1). WikiTree began blocking API requests mid-session (Round 3).
- **Chronicling America**: almost no Wilkes-Barre titles; nothing on Andrew/Addison Pringle or the Connoles.
- **Catherine Boney's 1904 obituary text** (W-B Record 19 Apr 1904): no online transcription.
- **Connole in 1860 Elmira city census** (Joyce Tice transcription, 112 pages: https://joycetice.com/censusc/1860elmr.htm): not found. No Irish county found for Connole.
- **Dennis Dwyer (1807–1875)**: nothing online.
- **Andrew G. Pringle**: no Civil War, GAR, pension, will or occupation record (archive.org full text, Chronicling America PA titles, web; not in Luzerne wills index P); not in 2,656 PA-Roots company rosters.
- **Noah, Andrew, Alby, Edwin, Orange, Ransom Pringle**: none in the PA-Roots/Bates rosters (which omit 1862–63 emergency militia and out-of-state enlistments).
- **Divorce grounds (Pringle v. Pringle)**: not online.
- **Samuel Pringle's parents**: not in *The Prindle Genealogy* by keyword search (no Samuel c.1767, no Lamoreux marriages).
- **Stephen Scott's Connecticut town, Catherine Scott's siblings (Round 2)**: nothing; Stephen/Julia: no Find a Grave, will or obituary found online in Round 1.
- **Lina Ann (Pringle) Harrison**: nothing in Bradsby, Harvey, Luzerne wills index or web.
- **WWI/WWII service** of Andrew & Mary's grandsons and of Joseph V. and Francis Pringle: not found (draft cards need login).
- **Anastasia & Catherine Boney as sisters**: unproven; Dwyer gives Catherine's parents only.
- **John Young × Anna Maria Doll; Mary Young's baptism**: no online record; Plumb's History of Hanover (all 40 parts) has no Frederick Croup or relevant John Young.
- **Frederick & Mary Croup 1841 deaths**: no record online.
- **Andreas Grub French & Indian War service**: none found.
- **Dietz**: nothing new beyond the 1757 Tohickon baptism.
- **Elizabeth Mersereau's parents**: no document names them outright.
- **Bull Smith/Wells/Thompson/Davenport English origins**: claims fail (Davenport origin unknown).
- **Florence Pringle Meier's 1980 death**: not checked; online PA death index ends 1966.
- **1950 census name index (NARA OCR)**: did not find William/Florence/James (later found via FamilySearch images in Round 3).
- **Priests / athletes** among PA-line relatives: none found (Round 2).

### 6.3 Colonial Long Island, New England and English lines

**Colonial group: sources consulted, and searches that came back empty or were blocked.**

#### Project files read for this section
- `research/tree_transcription.md` — tree summary (Long Island lines “already researched”; Youngs/Horne/Wells/Topping/Sayre/Buswell tree entries; Justice Adam Smith vs PDF note).
- `Ancestry tree screenshots (section 2.2.2)` (handoff scratch file listing tree values from John’s Drive screenshots IMG_7791–7840; colonial cards IMG_7792–7799) — exact tree names/dates for every colonial person (e.g. Capt J Tuttle 1727–1802; James M Tuthill 1692–1772; HANNAH S REEVE 1699–1764 with gravestone photo; JAMES R REEVES 1672–1732 and Deborah H Satterly 1676–1754 with gravestone images; James F Smith 1688–1740; JERUSHA TOPPING 1698–1760 with Topping arms; “Justice, A Smith” 1649–1726 with Smithtown 350th logo; Elizabeth Thompson 1657–1718; Josiah Topping 1663–1726; Hannah Sayre 1668–1741; John Topping 1636–1686; Captain T I Topping 1608–1687; Emma C Aldridge 1610–1665 with ship image; Maj R B Sm(y)ith 1613–1692; Sarah F Hammond 1623–1708; Sir Samuel Smith 1575–1618 with St George’s cross; Rebecca Buswell 1593–1667; Margaret Buswell 1550–1612; John J Tuthill Jr. 1658–1754; Mehitable Wells 1666–1742; William Wells 1608–1671; Mary Maria YOUNGS 1619–1709; Rev. William Wells 1566–1620; Anne Elizabeth Hunt Kimball Welles 1568–1646; John Yonges 1598–1671; Vicar C. Yonges 1575–1626; Christopher Youngs 1562–1647; Johanna Horne 1544–1630; Edwardi Horne 1524–1624; Sir J W Horne 1500–1554; Jane/Jena Maloy 1500–1593; Thomas Younges 1475–1568).
- John’s Google Drive folder (https://drive.google.com/drive/folders/1nLAbzaMlKOSgimj590vLgkfDQMesBRVJ) (screenshots IMG_7815–7827; see section 2.2): Pelletreau *Records of the Town of Smithtown* page screenshots (pp. 45–47, 50, 356, App. 471–472; map of land laid out to Lieut. Richard Smith 26 Apr 1736 containing 196 acres 65 rods); F. K. Smith *The Family of Richard Smith* pp. 119–122 (Daggett; Charity Smith m. John Adams; Gloriana m. Joseph Bryant; Phebe m. Capt. Nathaniel Platt; Theodorus Bailey; Isaac Smith b. 30 Oct 1745 m. Margaret Field/Theal; “Shell Dick”); Joshua Smith house photo caption (“built c. 1761, remodeled in 1819, demolished in 1960. Hall woodwork now at the Henry Francis duPont Winterthur Museum”). All collateral.
- `research/Johnny_Meier_Lineage_Report_2026-10.md` (Round 1): corrections 3a–3f; cousins table; regional ties; records list §5.
- `research/Johnny_Meier_Lineage_Report_Round2_2026-10.md` (Round 2): §2 notable cousins; §3d Long Island; §4 stories.
- `research/Johnny_Meier_Lineage_Report_Round3_2026-10.md` (Round 3): England origins table; status changes (Temperance unchanged probable; John Tuthill stronger probable; Brewster probably disproven); §6 records.
- `research/notes/colonial_virginia.md` (Round 1 notes).
- `research/notes/round2/colonial_cousins.md` (Round 2 notes).
- `research/notes/round3/english_french_origins.md` (Round 3 notes; English parts used here; French parts belong to the Lamoreaux group).
- Upload “Family_ties_to_Hauppauge.md” (`uploads/hearth/66b73be3-…`), whole.
- Upload “Meier_family_tree_deep_dive.md” (“Old Records Reshape Johnny Meier’s Family Tree”, `uploads/hearth/3361cb6c-…`): Long Island cousins table, Pelletreau evidence, societies, colonial corrections.
- Upload “Richard_Bull_Smith_Lineage.pdf” (`uploads/hearth/1536d033-…`): one-page 13-generation chart “Descent from Richard ‘Bull’ Smith — Founder of Smithtown, Long Island • Your 10th great-grandfather” (text extracted; rows listed in colonial_lines.md).

#### Published books and articles (with what each gave)
| Source | Link / citation | What it gave |
|---|---|---|
| W. S. Pelletreau, *Records of the Town of Smithtown* (1898) | https://archive.org/details/recordsoftownofs00smitrich | Intro. p. vii (“we know absolutely nothing” of Bull Smith; Yorkshire tradition; Southampton home lot); Intro. pp. xii–xiii (Nissequogue home lots); pp. 37–38 (Sarah’s will); p. 39 & p. 231 (only Tuthill hits); pp. 44–46, 50 (Aaron, Abner, Ebenezer wills; “Dick ’Nezer Place”); pp. 58–59 (1688 deed to Job); pp. 82–83 (James’s 1725 earmark); pp. 236, 248 (Daniel 2d’s 1736 land; Joshua Smith House note); p. 297, 311–312, 361, 398–400 (James Smith’s 1736 tract and sales); pp. 330–331 (Job’s homestead → Job 3d → Woodhull Smith); p. 356 (Abner’s 10 acres; 1736 map); pp. 359–363 (Daniel 2d’s unexecuted will); pp. 385–386 (Happogs); App. pp. 461, 465, 466, 471, 472, 475, 476–478, 479, 480–481, 491 (Smith genealogy; Temperance Platt; James & Jerusha’s children; Bailey; Daggett; Lawrence/Carteret/Townley; Gen. John Smith); Intro note on Col. Abraham Gardiner’s wife Mary. Called Bull Smith’s wife “Sarah Folger of Boston” (superseded). |
| F. K. Smith, *The Family of Richard Smith of Smithtown* (1967) | ch. 1 text http://longislandgenealogy.com/RichardSmith.pdf ; borrow-only https://archive.org/details/familyofrichards00smit ; quoted at jrm Needham | pp. 15–20 (ship *John* 1635; London upbringing; *Speedwell* 1656); “James Smith (Job, Richard)… married Jerusha, daughter of Elnathan and Mary Topping…”; Hannah Brewster as Elizabeth Thompson’s mother (superseded); pp. 119–122 (Drive screenshots; Bailey/Platt/Daggett etc.); Abner Smith House picture |
| Alva M. Tuttle, *Tuttle-Tuthill Lines in America* (1968) | FamilySearch Books item 481721 https://www.familysearch.org/library/books/records/item/481721 ; quoted on WikiTree Tuthill-364 and Smith-141655 | p. 311 John Tuthill ~1730 s Jas 1692, m. 23 Nov 1752 Smithtown Temp da Jas & Jerusha (Topping) Smith; children; p. 279 James Tuthill b. ~1692 Oysterponds, m. Rachel Browne ~1714, to Ulster/Orange 1742–48, d. ~1772 |
| L. D. Akerly, *The Tuthill Family of Tharston … and Southold* (1898) | https://archive.org/details/tuthillfamilyoft00aker | Henry Tuthill’s 1618 will (pp. 3–4); arms; Hingham; John 1635; John Jr.’s offices; James “doubtless both of Brookhaven… and of Orange Co.”, Brookhaven land 1714/1721, rated 1741 not 1749, children Daniel, James, Benjamin (no John); Mary (1687–1780) m. Jonathan Horton; Azariah; Freegift |
| C. A. Hayes, *William Wells of Southold and his Descendants* (1878) | https://archive.org/details/williamwellsofso00byuhaye | Ch. I & pp. 9–15 (Rev. William Welles, prebendary; St Peter Mancroft baptism 10 Feb 1604/5); p. 18 (Richard Wells, *Globe*); pp. 27–28 (Mary “said to be Youngs”); p. 28n; ch. VII (Dr. Henry Wells) |
| *William Wells of Southold* (1986) | https://archive.org/details/williamwellsofso00well | NOT READ (borrow-only) |
| Selah Youngs, *Youngs Family* (1907) | https://archive.org/details/youngsfamilyvica00youn | Rev. John’s children and wives; no Mary Wells; no Horne; Christopher’s wife “Margaret” d. 1630 |
| G. R. Howell, *Early History of Southampton* (1887) | https://archive.org/details/earlyhistoryofso00howe | pp. 395–397 Topping genealogy (Capt. Elnathan of Sagg; Elnathan b. 20 Aug 1664 d. Sept 1751, children by will incl. Jerusha; Topping’s Purchase; Thomas’s three marriages, 1686 deed, death at Branford 1688; refugee tradition) |
| Banks, *The Sayre Family* (1901) | https://archive.org/details/sayrefamilylinea00bant | p. 30: Josiah & Hannah Topping had only Josiah and John (b. 1706); Daniel Sayre’s 1707 will; Stephen Sayre’s descent and death at Brandon, VA (*Richmond Enquirer* 10 Dec 1818) |
| B. F. Thompson, *History of Long Island* (1918 ed.) vol. 2 p. 310; vol. 3 pp. 292–297 | https://archive.org/details/historyoflongisl003thom | Thompson family account; John Thompson’s daughter Elizabeth m. Job Smith; Hannah Brewster/Mayflower claim (false); Thompson/Strong cousin paths; Rev. William Thompson of Braintree “traditionary”; Roger Ludlow; Setauket home lot |
| J. Champlin, “Thompson and Brewster,” *NYGBR* 46 (1915): 4–9 | https://archive.org/details/newyorkgenealog46gree | Disproved Rev. William of Braintree as father and the Mayflower Brewster wife; Francis Brewster “of London” to New Haven 1638 |
| D. L. Jacobus, “The Family of Rev. Nathaniel Brewster,” *TAG* 12:199–204, 13:221 | Summarized on WikiTree Thompson-213 https://www.wikitree.com/wiki/Thompson-213 (NOT read directly) | John Thompson’s wife Mary; Hannah Brewster m. Samuel Thompson; Elizabeth “highly probable” child; 1609/1688 dates bogus |
| Gardiner, *Lion Gardiner and his Descendants* (1890) | https://archive.org/details/liongardinerhisd00gard | p. 119 Col. Abraham Gardiner m. Mary Smith (dau. Nathaniel & Phoebe Howell Smith, descendant of “Major Richard Smith … ‘Bull Smith’”); pp. 147–149 path to Julia; p. 149 David Gardiner |
| T. Lawrence, *Historical Genealogy of the Lawrence Family* (1858) | https://archive.org/details/historicalgeneal00lawr | All Flushing Lawrence cousin paths |
| F. S. Hammond, *History and Genealogies of the Hammond Families in America* (1902) vol. 1 | https://archive.org/details/historygenealogi0001fred | Lavenham register (William bapt. 1575; marriage 1605; children; “Marie” 1628/1623); Thomas & Rose Trippe; John of Lavenham; John Hamonde of Melford; *Francis* 1634; Watertown; will; Quaker search pp. 50–51; Farnsworth and Warren paths; p. 59 Nowton theory |
| Ruttenber & Clark, *History of Orange County* (1881) | https://archive.org/details/historyoforangec00rut | Woodbury Clove and Upper Clove militia; Austin Smith offices 1775; Jeremiah Smith will; Articles of Association signers; Jonathan Tuthill captain |
| S. W. Eager, *Outline History of Orange County* (1846) pp. 527–529 | https://archive.org/details/outlinehistoryof00eage | “Capt. J. Tuthill”; 1769 apprentice case; 1788 “Capt. Tuthill” |
| F. B. Dexter, *Biographical Sketches of the Graduates of Yale College* vol. 1 pp. 434–5 | https://archive.org/details/biogsketchgrad01dextuoft | Rev. Abner Reeve; Deborah Topping |
| *Abstracts of Wills … City of New York* (NYHS) vols. III–VI | III https://archive.org/details/abstractswillso01kellgoog ; IV https://archive.org/details/abstractswillso02kellgoog ; V https://archive.org/details/abstractswillso04kellgoog ; VI https://archive.org/details/abstractswillso05kellgoog | III Liber 15 pp. 400–1 (John Tuthill III, 9 Jun 1740); IV Liber 18 pp. 391–2 (Elnathan Topping, 15/30 Sep 1751); V Liber 20 p. 25 (James Tuthill Jr., 17 Mar 1756); VI Liber 23 p. 130 (Daniel Tuthill, 1761) |
| *Smith Wills* (1898) | https://archive.org/details/cu31924029771726 | No Smith will names Temperance |
| *Names of Persons for whom Marriage Licenses were Issued* (NY) | https://archive.org/details/namesofpersonsfo00newy | No license pairing John Tuthill & Temperance Smith |
| Wood, *History of Hauppauge* (1920) | https://archive.org/details/historyofhauppau00wood_0 ; full text https://archive.org/download/historyofhauppau00wood_0/historyofhauppau00wood_0_djvu.txt | Hauppauge Smiths, houses, mill, graves, Blydenburghs, other Smith families, church lists |
| Tooker, *Indian Place-Names* (1911) entry 103 | https://archive.org/details/indianplacenames00tooker | “overflowed land” |
| *Colonel Rockwell’s Scrap-book* (1968) | https://archive.org/details/colonelrockwells0000vari | Joshua Smith House c.1761, demolition; Caleb II house; Abner Smith House on Village Way |
| C. E. Banks, *Planters of the Commonwealth* p. 183 | https://archive.org/details/plantersofcommon00bank/page/182/mode/2up | Henry Tuthill, *Mary Anne* of Yarmouth, 1637 |
| Gyll, *History of Wraysbury, Ankerwycke Priory and Magna Charta Island* (1862) pp. 58, 63 | — | Aldridge manor of Remingham and Cow |
| *Winthrop Papers* vol. 4 pp. 230–2 | https://babel.hathitrust.org/cgi/pt?id=uc1.31158002884053&view=1up&seq=282 | 1640 Smith–Hammond letters |
| E. H. L. Smith III, *NYGBR* 121:19–22 | via jrm I2516 | Sarah Hammond identification |
| Moriarty, *NEHGR* 79:82–84; *NEHGR* 69:251–2; Anderson, *Great Migration Begins* pp. 852–3; *Great Migration* vol. V | — | Elizabeth Paine’s Lavenham baptism and family |
| Green, *TAG* 56:143 | — | William Tuttle of New Haven from Ringstead |
| *Quaker History* 3–4:58–59 | — | Speedwell 1656 |
| Savage; Conn. Hist. Soc. Coll. 3:306 | — | Thomas Topping in the Connecticut charter |
| Charles E. Topping, *Topping Genealogy* (1980) p. 392 | via WikiTree Smith-141655 | Still gives Josiah Topping line (rejected) |
| Cuyler, *Recollections of a Long Life* | https://www.gutenberg.org/ebooks/12549 | Cuyler’s Horton descent |
| Appletons’ Cyclopaedia (1900) vol. 5 p. 760 | Wikisource | Selah Strong |
| Clergy of the Church of England Database, person 12847 | — | Rev. William Wells, vicar of North Elmham, d. 1680 |
| Norfolk RO PD 281/1; FreeREG (Tharston, Saxlingham Nethergate, Ringstead registers) | — | Tuthill baptisms/burials |
| FamilySearch England Christenings index; National Burial Index; Dunstable register (Beds CRO 1951); Bucks Bishop’s Transcripts | — | Topping and Aldridge entries |
| Southold Town Records v1 pp. 302, 310 | — | William Wells’s and Mary Mapes’s wills |
| Middlesex Probate 7167 | — | William Hammond’s will |

#### Web databases and pages
- jrm Needham database (quotes F. K. Smith 1967 and NYGBR): I2549 (James Smith/Jerusha), I2543 (Josiah Topping, no children), I2516 (Sarah Hammond), I2523 (Thompson/Brewster), I2515 (Elizabeth Smith Lawrence), I2596 (J. Lawrence Smith, Gen. John Smith), I2318 (Gen. Nathaniel Woodhull), I2322 (Jesse Woodhull), I2547 (Thomas Topping), I3699 (Deborah Smith Blydenburgh) — https://jrm.phys.ksu.edu/Genealogy/Needham/
- WikiTree: Tuthill-364, Tuthill-530, Tuthill-7, Tuthill-60, Tuttle-29, Smith-141655, Smith-1208, Thompson-213, Starr-3, Wells-639, Topping-121, Topping-199, Topping-248, Aldridge-218, Hammond-356, Paine-100, Paine-470 (via API getProfile/getAncestors).
- McCurdy family lineage: p14551, p12609, p16172, p14544, p7701, p14863 (mccurdyfamilylineage.com).
- My Maine Heritage (unsourced online tree): ps409_209, ps409_270 (sites.rootsweb.com/~megen/reunion/ps409/).
- Behling Brewster pages: homepages.rootsweb.com/~sam/brewster.html, brewsteri.html.
- Rootsweb Youngs index: sites.rootsweb.com/~riss/baldwin/bw/youngs_index.html (no Mary Wells).
- SAR: P-232580 (Thomas Lamoreaux), ACN 58344 (Keturah b. 1755 Woodbury Clove), P-120755 (Samuel Brewster), P-308220 (Daniel Tuthill 1743–1800), cemetery 375105 (Joseph Blydenburgh).
- Wikipedia: Richard Smith (settler); Smithtown, New York; Julia Gardiner Tyler; David Gardiner Tyler; Lyon Gardiner Tyler; Harrison Ruffin Tyler; Berkeley Plantation; Anna Harrison; Selah B. Strong; Jonathan Thompson (collector); Theodore L. Cuyler; James H. Baker (politician); Roger Ludlow; Youngs Memorial Cemetery; Cornelius Van Wyck Lawrence; Sir Willoughby Jones, 3rd Baronet; Daniel L. Braine; John Smith (New York senator); Lawrence Grant White; Samuel Dennis Warren; Edward Perry Warren; Mersereau Ring; Hudson River Chains; Joshua Smith (New York politician); Blydenburgh Park Historic District; Charles A. Floyd; Abraham Woodhull; Jesse Woodhull; Caleb Brewster; Anna Smith Strong; Sagtikos Manor; NY State Route 111; Order of the Founders and Patriots; Hereditary Order of Descendants of Colonial Governors.
- Other: NJGenWeb Azariah Horton bio (usgenwebsites.org/NJMorris/biographies/lewisbios1899/hortonazariah.htm); Online Books (B. F. Thompson); Stony Brook special collections (Woodhull); Underhill Society; We’re History (Harvard 1642); Brooklyn Historical (Governors’ letters 1665–67); Find a Grave 38871768 (Sen. Joshua B. Smith), cemetery 1978430 (Hauppauge Methodist/Rural Cemetery, 473 Townline Road); LOC HABS NY-5414 (loc.gov/pictures/item/ny0780/); LOC 1858 Chace map (loc.gov/item/2013593235/); David Rumsey 1873 Beers atlas plate; Suffolk County Parks (Blydenburgh County Park); Patch (Caleb Smith II; first schoolhouses); Founders Online (Washington’s 1790 diary); Ohio SCW and NSDCW eligibility pages; Miner Descent (societies); American Heritage (“The Great Shippe”); New Haven Colony Records.

#### Searches that came back empty (do not repeat without new angle)
- **No source names Bull Smith’s parents**; no knighted father (“Sir Samuel Smith”) in any source checked; no Rebecca/Margaret Buswell anywhere.
- **Bull Smith English origin**: Gloucestershire = wrong man; Bedfordshire = no source; “Myreshaw, Bradford” unsourced; Y-DNA no English match.
- **Smith/Hammond Virginia links**: none.
- **Revolutionary service in Virginia** in any colonial line: none.
- **Pelletreau full-text search for Tuthill/Tuttle**: only a 1704 county highway commissioner (p. 39) and a 19th-century Watchogue landowner (p. 231) — nothing tying John Tuttle or Temperance to Smithtown.
- **Colonial NY marriage licenses**: no license pairing John Tuthill/Tuttle & Temperance Smith.
- **NY will for James Smith (d. 1740)**: none found. **Smith Wills (1898)**: no will names Temperance.
- **Akerly**: does not name a John among James Tuthill’s children.
- **Graves** of Job Smith, James Smith, Jerusha, Temperance or John Tuttle: none found in Hauppauge or elsewhere.
- **Find a Grave for Judge Joshua Smith II or Joshua Smith I**: none found.
- **Wood (1920) Hauppauge**: no Pringle, Heffernan or Meier; no Topping, Strong or Lamoreaux; Tuttle and Thompson only as unrelated church-list names (Ezra Tuttle 1806; Daniel and Triphene Thompson); Hauppauge land shows no Job, Richard 2d, Adam or Jonathan branch.
- **Hayes 1878** found nothing on Mary Wells’s surname; **Youngs 1907** has no Mary Wells and no Horne; **Rootsweb Youngs index** no Mary Wells.
- **Lavenham register**: no “Sarah” baptism for William Hammond’s daughter.
- **Deborah Satterly**: only one found, b. c.1705 (McCurdy p12609).
- **Hammond notable descendants**: none verified in Round 1 (Farnsworth/Warren found in Round 2).
- **Dan Topping**: family origin not found.
- **Tapping Reeve’s mother Deborah Topping**: place in Topping line not traced.
- **James H. Baker’s** path from Azariah Horton not traced; **Harrison extensions** (John Scott Harrison; William Henry Harrison III) not researched; **Dr. Henry Wells’s** descent not worked out; **Selah Tuthill’s** parents unproven.
- **Bull Smith’s daughter Elizabeth**: no Carteret children.
- **Lamoreaux/Huguenot notable cousin**: none verified in Round 1 (belongs to Lamoreaux group).
- **No 19th–20th-century Long Island tie** for any colonial line (only two speculative Henry Meier deaths — Huntington 21 Jul 1931 #44888, Hempstead 24 May 1937 #34005 — belong to the Meier group).

#### Blocked or not directly read
- Ancestry, Find a Grave, FamilySearch record search, Antenati, Geni and Legacy blocked automated access in Round 1; SAR/DAR databases blocked automated searches (search by hand in a browser).
- F. K. Smith (1967) is borrow-only on archive.org (`familyofrichards00smit`); only chapter 1 text (longislandgenealogy.com) and quotations (jrm) were read. The entry under James Smith of Moriches is still unseen.
- Alva Tuttle (1968) read only through WikiTree quotations; FamilySearch Books item 481721 needs a login.
- Jacobus, *TAG* 12–13, read only as summarized on WikiTree Thompson-213 (American Ancestors login needed).
- *William Wells of Southold* (1986) borrow-only, unread.
- NYGBR 121 (Edward Smith on Sarah Hammond) read only via jrm.
- D. K. Martin (2008) and Charente-Maritime registers belong to the Lamoreaux group.

### 6.4 Italian lines (Petriello, Gianetta, Cognetti, Ferlaino, Fiorillo, Colosimo)

#### Italian lines: sources consulted

Project files: research/tree_transcription.md; Ancestry tree screenshots (section 2.2.2) (Italian section, screenshots IMG_7830–7840); the Round 1, 2 and 3 reports; notes/italian.md (R1); notes/round2/italian_gaps.md (R2); notes/round3/italian_origins.md (R3). John's uploaded reports ("Old Records Reshape Johnny Meier's Family Tree", "Family ties to Hauppauge") and the Bull Smith PDF contain no Italian-line content.

##### Ancestry tree (John's app screenshots)
- Italian section, IMG_7830–7840. It gives every tree-only name and date: Petriello, Di Marino, D'Ambrosio, Gialanella, Di Biase, Cognetta, Malvaso, Ferlaino, Fiorillo, Morrello and Guercio. It also shows record-image thumbnails, "Potential" hint cards and the coat of arms. See the people file for each person's "Tree display" value.

##### Italian civil records: Portale Antenati (images read in Round 3)
Base URL: `https://antenati.cultura.gov.it/ark:/12657/{register}/{image}`

**Guardia Lombardi (Archivio di Stato di Avellino)**
| Record | Gave | URL |
|---|---|---|
| Nati 1869, act 110 | Giovanni Petriello b. 25 Oct 1869, 3 pm; father Pietro fu Angelo, 33, contadino; mother Grazia di Marino di Gaetano | an_ua524165/5vaJMry ; an_ua524165/57dzpEo |
| Morti 1901, act 28 | Pietro Petriello d. 29 Mar 1901, Via Piazza, aged 64, son of the late Angelo and Lucia Marra, husband of Grazia Di Marino; declarant Francesco De Biasi, 72 | an_ua524116/LzaVz4G |
| Morti 1916, act 22 | Grazia Di Marino d. 9 May 1916 aged 71, daughter of the late Gaetano and Caterina Di Leo, widow of Pietro Petriello | an_ua524131/wj7o8Qr |
| Morti 1876, act 20 | Gaetano di Marino d. Mar 1876 (registered 6 Mar) aged 80, son of the late Pietro and Felicita Magnotta, husband of Caterina di Leo | an_ua524100/wbdvxng |
| Marriage index 1855 #23 | Giuseppe Petriello (son of Carmine and Maria Marra) m. Concetta [di] Marino (daughter of Gaetano and Maria d'Ambrosio), 26 Dec 1855 | an_ua376657/wRvYlYY |
| Marriage index 1855 #16 | Gaetana Petriello (daughter of Angiolo and Lucia Marra) m. Giuseppantonio Lucadamo (son of Ciriaco and Anna Mastrodonato), 23 Feb 1855 | an_ua376657/57Ekokq |
| Marriage index 1857 #21 | Maria di Marino (daughter of G[aetano] and Caterina di Leo) m. Nicola di Pietro, 12 Feb 1857 | an_ua376659/wWNxVgm |
| Allegati to the 1906 deaths | Death certificate from St. Anthony's Church, Dunmore PA, for a Guardiese | — |
| Marriage indexes 1850–54 | Downloaded locally (ital/img/mi185x_m*.jpg) but **not read** | — |

**Bisaccia (AS Avellino)**
| Record | Gave | URL |
|---|---|---|
| Matrimoni 1896, act 18 | Francesco Giannetta (27, possidente, son of the living Savino and Angelamaria Fede) m. Angelica Ferrantino (23, born Sant'Angelo dei Lombardi, foundling), 1 Aug 1896 | an_ua445513/5glz731 ; index an_ua445513/LN8A9jl |
| Matrimoni 1867, act 17 | Savino Giannetta (24, pecoraio, son of the late Francesco and Lucia Macchia(?)) m. Angelamaria Fede (18, daughter of Bartolomeo Fede, pecoraio, and Luigia(?) Roberto), 20 Jul 1867 | an_ua445486/wQPnvWn ; an_ua445486/0Apd713 |

**Dasà (AS Vibo Valentia / Catanzaro)**
| Record | Gave | URL |
|---|---|---|
| Nati 1855, act 18 | Giovanni Cognetta b. 22 Mar 1855; father Mastro Nicola Cognetta, 51, ceraiuolo; mother Donna Mariangela Cannatello, 32 | an_ua37922783/0JPovJv ; index an_ua37922783/0Zo8bdo |
| 1854–55 indexes | Lamanna and Malvaso surnames present in Dasà | — |

**San Mango d'Aquino (AS Catanzaro)**
| Record | Gave | URL |
|---|---|---|
| Nati 1840, act 79 | Domenico Fiorillo b. 27 Dec 1840; father Carmine, 32, bracciale; mother Giuseppina Ferlaino; witness Gaetano Colosimo, 40; Sindaco Dr. Bruno Sacco | an_ua37933123/LNZdd7O ; an_ua37933123/LevKKpD |
| Morti 1860, act 30 | Carmine (Gabriele) Fiorillo d. 17 Nov 1860 aged 52, bracciale, son of the late Domenico Fiorillo and Vittoria Marrelli/Morelli | an_ua37932559/wWyrDq2 |
| Matrimoni volumes an_ua37928564 / an_ua37928565 (c.1831–41) | Search for the Carmine Fiorillo × Giuseppina Ferlaino marriage **not completed** | — |

##### US records: FamilySearch published-tree source images (read in Round 2)
| Record | Gave | Link |
|---|---|---|
| 1931 Lackawanna Co. marriage license application No. 1107 (sworn 20 Jun 1931) | James Petrillo × Mollie Genett, with parents, addresses and consent | FS VF76-TJQ, VF76-TJ9; image …/sources/GQWR-TY6/images/i/1/image.jpg |
| 1910 census, Scranton Ward 10, ED 88, sheet 22A | John Petrillo household, 1030 Ash St | …/sources/GQWT-LP5/images/i/1/image.jpg |
| 1920 census, Scranton Ward 10, ED 142, sheet 13A | John Patrello household, 1028 Bunker Hill | …/sources/GQWT-4Z7/images/i/0/image.jpg |
| 1941 marriage license (Anthony Petrillo × Ann Jason) | Both of Anthony's parents dead | …/sources/GQWT-4Z7/images/i/1/image.jpg |
| 1920 census, Scranton Ward 2, ED 105, sheet 2A (2–3 Jan 1920) | Josephine "Farino" household, 1306 Diamond Ave | FS MFBR-YF8; image …/sources/L6CN-7HV/images/i/0/image.jpg |
| 1930 census | Frank and Helen Cognetti household: ages at marriage 21/16; immigration 1907; naturalized; 612 Philo St, valued $5,000; son "Leopoldo" | FS XH3R-XB1; image …/sources/G3NN-88N/images/i/0/image.jpg |
| 1950 census | Frank (59), conveyor repair; Angeline, Anthony, John and Mary at home | FS 6X1W-37K9; image …/sources/GJB1-P6Y/images/i/0/image.jpg |
| 1940 marriage license No. 817 (Ralph Cognetti) | Mother's maiden name "Farino"; father a mechanic; Ralph a salesman | FS VF7X-JLN; image …/sources/L6CN-7HV/images/i/1/image.jpg |
| 1943 marriage license No. 1716 (Sal Cognetti × Elizabeth Notarianni) | Mother's maiden name "Farino" | FS VF7J-VGC |
| Declaration of Intention No. 16537, US District Court, Scranton, 12 Jul 1920 ("Frank Gennetti") | Birth 2 May 1869 Bisaccia; SS *Italia*, c.15 Apr 1903; 133 Sand St | …/sources/LCPG-XKM/images/i/2/image.jpg |

The image prefix "…" is https://ancestors.familysearch.org/service/tree/tree-data/published.

##### FamilySearch Family Tree profiles and indexes (user-contributed)
- **Petriello/Petrillo:**
  - GQWR-TY6 (James; 7 sources)
  - GQWT-4Z7 (John)
  - GQWT-LLS (Maria Antonia)
  - GQWR-RPT and G44P-XYT (Pietro and Grazia; give Filomena b. 1885 Carife; give an impossible wife "Grazia Sasso 1796–1848")
  - GQWT-QQ8 (Grace)
  - L1QP-W1Q (Peter)
  - GQWT-QQ6 (Josephine)
  - GQWR-122 (Nicholas)
  - GQWT-ZPC (Rocco Frank)
  - L6MH-TCL (Rocco James, another family)
- **DiBiasi:** G4YR-BXY (Giovanni Pasquale and Rosa; unsourced "Lucera"; children 1891/1894 mis-attached); G4YT-QC3 (Domenico Antonio DiBiasi).
- **Giannetta:** GQ4M-KCR (Carmela "Mollie"); LCPG-XKM (Frank); LCPG-FC6 (Angelica; Mollie's siblings).
- **Cognetti:**
  - GJB1-P6Y (Frank; b. 1892, immigrated 1907; sourceless second wife "Philomena")
  - GJB1-GYW (Sal)
  - PW2S-1KJ (Anthony)
  - L6CN-7HV (Ralph; his children)
  - duplicate "Leupo" (1930)
  - P7MS-NB2 (the Nicastro Frank Cognetti, a different family)
  - GD4C-85X (Vincenzo Cognetta, Laureana di Borrello)
- **Indexes:**
  - SSDI JRHQ-NYH (Mollie C Petriello)
  - 1910 census MGZ8-YF8 (Giannetta)
  - naturalization 6KBJ-T9JV
  - Avellino civil records 6PG6-674L, 6PG6-674V
  - enlistments K8PX-Z8K (Sal) and K8G2-K1H (Rocco F.)
  - WWII draft cards Q2Q2-NKPY (Anthony) and Q2Q2-N2SB (Leo)
  - BillionGraves QK9P-G2LN (Domenico Antonio DiBiasi)
- **Unrelated example:** Antonio Adamo (b. 1880 San Mango, d. 1953 Scranton), LHG2-989, https://ancestors.familysearch.org/en/LHG2-989/antonio-adamo-1880-1953

Profile URL pattern: https://ancestors.familysearch.org/en/{ID}. Record pattern: https://familysearch.org/ark:/61903/1:1:{ID}.
**Method (Round 2):** scanned all 4,562 FamilySearch Ancestors sitemaps (about 5,000 profile URLs), then pulled `familysearch.org/service/tree/tree-data/published/persons/{ID}` JSON and the attached source images.

##### Geni / Ancestry / MyHeritage / WikiTree (index extracts)
- **Geni**, Giovanni "John" Petriello (1869–1939): https://www.geni.com/people/Giovanni-Petriello/6000000144788328847, with a duplicate at https://www.geni.com/people/Giovanni-Petriello/6000000070274241935. It gives his parents, wife and a children list, including Rocco James (wrong) and Frank W. b. Jul 1895. Read via search-engine extracts.
- **Ancestry index** "John Petrello 1869–1937": https://www.ancestry.com/genealogy/records/john-petrello-24-2bhjcmt
- **MyHeritage**, Mariangiola Cognetta née Cannatello, b. 1818 Dasà: https://www.myheritage.it/names/mariangiola_cognetta (search extract).
- **WikiTree** Cognetti-1 (Ralph A., from the SSDI and the 1930 census ED 12 p. 28A): https://www.wikitree.com/wiki/Cognetti-1. The WikiTree Petriello profiles are from Acquaviva (Bari) and Sassano (SA) and are unrelated.

##### Obituaries and articles
- **Joseph F. Cognetti** obituary (d. 25 May 2009): https://www.legacy.com/us/obituaries/thetimes-tribune/name/joseph-cognetti-obituary?pid=127764806
- **Anthony R. Cognetti** obituary (2008; "Helen Farina Cognetti"): https://www.legacy.com/us/obituaries/thetimes-tribune/name/anthony-cognetti-obituary?id=24081273
- **Leo S. Cognetti** obituary (2019; "Mary Petriello (John)"): https://www.echovita.com/us/obituaries/pa/exton/leo-s-cognetti-9386745
- **Victor L. Cognetti** obituary (the Nicastro family): https://www.legacy.com/us/obituaries/name/victor-cognetti-obituary?id=59852747
- **John T. Petriello Jr.** obituary (d. 29 Feb 2024): https://themontynews.org/single-post/john-t-petriello-jr-65
- **Cognetti Thanksgiving** article (2016): https://hinerfeldcommercial.com/2016/11/30/family-celebrates-50-years-of-thanksgiving-gatherings/
- **Candy Hall of Fame:** https://candyhalloffame.org/inductee/joseph-f-cognetti/ ; https://candyhalloffame.org/inductee/anthony-paul-cognetti
- **ABMC WWII Registry:** https://wwiiregistry.abmc.gov/honoree-search-results/page/34576
- **Later San Mango-born Scranton residents:** Francesco "Frank" Ferlaino (d. 2007), https://www.legacy.com/us/obituaries/thetimes-tribune/name/francesco-ferlaino-obituary?id=25181894 ; Gina Fiorillo (d. 2016), https://www.legacy.com/us/obituaries/thetimes-tribune/name/gina-fiorillo-obituary?id=16906825

##### Community, surname and place sources
- **paese.app** (US arrivals by comune, 1830–1912):
  - Surnames: magnotta, siconolfi, gialanella, di marino, di biase, petriello, di vivo, malvaso, cannatello, lamanna, fiorillo, cognetti (https://paese.app/cognomi/{surname})
  - Towns: Guardia Lombardi (https://paese.app/regioni/campania/avellino/guardia-lombardi), Dasà (https://paese.app/regioni/calabria/vibo-valentia/dasa), Bisaccia (https://paese.app/regioni/campania/avellino/bisaccia)
  - Note: "Guardea (TR)" in its tables is a geocoding error for Guardia.
- **italyheritage surname lists:**
  - Guardia Lombardi: https://www.italyheritage.com/genealogy/surnames/regions/campania/avellino/guardia-lombardi.htm
  - San Mango: https://www.italyheritage.com/genealogy/surnames/regions/calabria/catanzaro/san-mango-d-aquino.htm
- **indettaglio, Case Siconolfi:** http://italia.indettaglio.it/ita/campania/avellino_guardialombardi_casesiconolfi.html
- **Guardia–Dunmore community and Guardia history:**
  - Irpinia Stories: https://irpiniastories.wordpress.com/2022/08/11/ties-that-remain-celebrating-guardia-lombardi-in-pennsylvania/
  - Sister-city page: https://www.facebook.com/ScrantonDunmoreGuardia/
  - ProPublica (Association of Former Citizens of Guardia Lombardi): https://projects.propublica.org/nonprofits/organizations/133614685
  - AvellinoToday (Siconolfi sindaco): https://www.avellinotoday.it/politica/mozione-sfiducia-guardia-lombardi-siconolfi.html
  - Wikipedia: https://en.wikipedia.org/wiki/Guardia_Lombardi
  - Porfido et al. 2020: https://www.earth-prints.org/bitstream/2122/14394/1/geosciences_Porfido_et_al_2020.pdf
  - WNEP, St. Rocco feast: https://wnep.com/article/news/local/lackawanna-county/festival-and-feast-of-st-rocco-a-dunmore-tradition/523-cbeab741-2694-4e93-9676-0e421060fa07
  - We The Italians: https://www.wetheitalians.com/news/italians-lackawanna-county-wonderful-community-where-people-love-and-respect-each-other
- **San Mango d'Aquino:**
  - ItalianGenealogy.com forum topic 26645 (Biff83; 1306 Diamond Ave, Antonio Epifano): https://www.italiangenealogy.com/forum/topic/26645
  - San Mango d'Aquino Mutual Benefit Society, 1258 Providence Rd (Yelp): https://www.yelp.com/biz/san-mango-d-aquino-mutual-benefit-society-scranton
  - ItalianSide genealogy guide: https://www.italianside.com/calabria/catanzaro/san-mango-daquino/genealogy/
  - FamilySearch Wiki (civil registration from 1809; FS collections for 1809–1865 and 1866–1910): https://www.familysearch.org/en/wiki/San_Mango_d'Aquino,_Catanzaro,_Calabria,_Italy_Genealogy
  - it.wikipedia: https://it.wikipedia.org/wiki/San_Mango_d%27Aquino
- **ItalianParishRecords.org, San Mango d'Aquino stati delle anime 1674–1804** (14 years, 309–1,610 people per year) and cemetery index, indexed by Daniel Lupia and John Bifano (Epifano): https://www.italianparishrecords.org/search-by-region/calabria/catanzaro/san-mango-daquino. Every year was searched.
  - Found: Ferlaino 229, Colosimo 652, Guercio 163, Marsico 68, Vecchio 10.
  - **Zero** entries for Fiorillo, Fata, Morrello/Morello, Chiarello, Palladino and Briglio.
  - Cemetery: Anna Epifano Ferlaino (1906–1958); no Leopoldo or Giuseppina.
- **Other places:**
  - Dasà: https://it.wikipedia.org/wiki/Das%C3%A0
  - Bisaccia: https://it.wikipedia.org/wiki/Bisaccia_(Italia)
  - Girimonti research p306 (a different Maria Rosa Lamanna, Casino): https://girimonti.circolocalabrese.org/research/p306.htm
- **Coat-of-arms checks:**
  - comuni-italiani arms lists for CZ (https://www.comuni-italiani.it/079/stemmi.html), CS (/078/), VV (/102/) and KR (/101/)
  - it.wikipedia blazons for San Mango and Martirano Lombardo (https://it.wikipedia.org/wiki/Martirano_Lombardo)
- **Ruled-out people:**
  - Italiani.it (Judge Francesco Ferlaino): https://en.italiani.it/mattarella-remembers-the-judge-francesco-ferlaino-killed-in-1975/
  - Corrado Ferlaino: https://it.wikipedia.org/wiki/Corrado_Ferlaino
  - Paige Cognetti: https://en.wikipedia.org/wiki/Paige_Cognetti
  - Fields of Honor (PFC Frank A. Petriello): https://www.fieldsofhonor-database.com/case/35733-petriello-frank-anthony
  - James C. Petrillo: https://en.wikipedia.org/wiki/James_Petrillo

---

#### Searches that came back empty or were blocked (do not repeat blindly)

**Blocked or login-walled (Rounds 1–3)**
- FamilySearch historical-record search: HTTP 401. ARK record pages: 401 or login redirect. Italian civil-record images on FamilySearch: 403. Only records attached to published tree profiles could be read.
- Ancestry: blocked.
- Find a Grave search: 403.
- Portale Antenati: 403 in Round 1; it worked in Round 3.
- Legacy.com obituary pages: 403; text came only from search-engine extracts.
- Geni: 403 (search extracts only).
- MyHeritage: 403.
- The Casa Italiana NYU St. Rocco article is behind a 403/JavaScript wall.
- Ellis Island / Steve Morse: no usable unauthenticated passenger search.

**Coverage gaps on Antenati**
- Guardia: the 1862 and 1864 marriage registers are missing, and Nati 1870 has no index (63 images).
- Bisaccia: Nati 1869 is missing.
- Sant'Angelo dei Lombardi: covered only to 1865.
- San Mango d'Aquino: covered only to 1860.
- Dasà: no births for 1862–1910.
- An Antenati search for "Bisaccia" also returns Montenero di Bisaccia (Campobasso). Filter by province.

**Empty searches**
- **Pietro Petriello × Grazia Di Marino marriage:** not found in the Guardia marriage indexes for 1855–61, 1863, 1865 (part) and 1866–68.
- **Leopoldo Ferlaino and Giuseppina Fiorillo:**
  - No public record and no web hits (Round 1).
  - No published FS profile under Ferlaino, Farino, Farina or Fiorillo with a Scranton tie (Round 2).
  - No San Mango cemetery entry.
- **Frank Cognetti:**
  - His birthplace, WWI draft card and 1942 draft card are not attached to any published profile.
  - The web and paese.app give no Dasà link.
  - Web searches for his death and naturalization found nothing (Round 3).
- **Giovanni Cognetta (1855–1930):** no US trace; not in any Scranton census with Frank.
- **Helen Cognetti's death date:** her FS profile shows "Deceased" with no date.
- **Salvatore Cognetti:** no public record in Round 1 (found in Round 2 via FS).
- **James Petriello's 1998 obituary:** not found (Round 1).
- **John Petriello's ship manifest:** not reachable (Round 1).
- **Coat of arms:** 35+ comuni checked with no silver lion on black:
  - San Mango district: San Mango d'Aquino, Martirano, Martirano Lombardo, Conflenti, Motta Santa Lucia, Decollatura, Platania, Falerna, Gizzeria, Nocera Terinese, Serrastretta, Feroleto Antico, Pianopoli, Soveria Mannelli, Maida.
  - Savuto valley: Cleto, Lago, Amantea, Belmonte Calabro, Serra d'Aiello, Scigliano, Colosimi, Carpanzano, Malito, Pedivigliano, Grimaldi.
  - Other Catanzaro/Crotone: Lamezia Terme, Carlopoli, Petronà, Sersale, Tiriolo, Cropani.
  - Vibo Valentia: Dasà, Acquaro, Arena.
- **WikiTree:** no profiles for these families except Cognetti-1.
- **Notable-relative search** for the Petrillo children (musicians, politicians, athletes): nothing beyond WWII service.
- **Medals:** no WWI/WWII medals or citations found for Joseph F. or Anthony R. Cognetti beyond their service records. No clergy or athletes turned up in the direct lines.
- **Moraca:** the surname does not appear anywhere in the project files. No Moraca research has been done.

---
