#!/usr/bin/env python3
"""Merge the round-4 overnight research (research/imported/round4) into the site data.

Reads one result file per person (people/<id>.json, schema in _work/BRIEF.md) and
folds the new information into data/research/<id>.json: vital-date refinements,
aliases, residences, events, facts, biography additions, fun facts, conflicts,
confidence recommendations, resolved and new open questions, sources, media
(downloaded public-domain files are copied under media/<id>/, everything else is
linked), negative searches and a research-log entry.

Then adds the 42 new relatives (new_people.json) to data/additions-manual.json
with the families implied by their relationships, appends the 30 stories to
data/stories.json (two research-correction pieces go to story-exclusions), and
writes research/leads-round4.md.

Rules: a found birth/death date replaces the tree's only when the tree has none,
when it refines the same year, or when the person is in RESOLVED_DATES (cases the
summary settles with primary records); every other disagreement is kept as a
"conflict" shown on the profile. Living people (status living_detected) get a
log line only. Idempotent: a second run is skipped for people already marked.
"""
import csv, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
ROUND = os.environ.get("ROUND", "round4")
SRC = os.path.join(ROOT, "research", "imported", ROUND)
MEDIA_SRC = os.environ.get("ROUND4_MEDIA", os.path.join(ROOT, ".cache", ROUND, "media"))
TODAY = "2026-10-08"
TAG = ROUND
LABEL = "Round " + re.sub(r"\D", "", ROUND)   # "Round 6"
RTAG = "R" + re.sub(r"\D", "", ROUND)          # source tags [R6-S1]
NOTES_ONLY = ROUND != "round4"   # later rounds: bioAdditions go to researchNotes; the About stays prose
LEADS_FILE = "research/leads-round4.md" if ROUND == "round4" else f"research/leads-{ROUND}.md"
PRESET_IDS = {"round5": {"NEW-1201": "H0383"}, "round6": {"NEW-1553": "M0089", "NEW-1554": "M0088"}}.get(ROUND, {})          # new people who already exist in the tree
SKIP_NEW = {"round5": {"NEW-1305", "NEW-1306", "NEW-1307"}}.get(ROUND, set())  # siblings whose parents are not in the tree
DIR_OVERRIDES = {"round5": {**{(f"NEW-{n}", None): "parent_of" for n in (1405, 1406, 1410, 1411)},
                            ("NEW-1409", "NEW-1408"): "parent_of", ("NEW-1409", "I282695503586"): "child_of", ("NEW-1409", "H0499"): "child_of",
                            ("NEW-1408", "NEW-1409"): "child_of",
                            **{(f"NEW-{n}", None): "child_of" for n in (1402, 1403, 1404, 1407, 1202, 1203, 1204, 1302, 1303, 1304)}}}.get(ROUND, {})
RESOLVED_DATES = {  # (person, field): dates the summary settles with primary evidence
    ("I282608064820", "death"),   # Henry J. Meier d. 20 Dec 1950 (1950 census + PA death index)
    ("I282608085064", "birth"),   # Theresa Meier b. 10 Sep 1868 (marriage record; 1870/1880 censuses)
    ("I282695503581", "birth"),   # Helen Ferlaino b. 8 Oct 1894 (San Mango baptism)
    ("I282608078175", "birth"),   # Johann Andreas Grub b. 12 Sep 1727 (register)
}
try:
    from PIL import Image
except Exception:  # noqa
    Image = None


def load(p, default):
    try:
        return json.load(open(p, encoding="utf-8"))
    except FileNotFoundError:
        return default


def save(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    open(p, "a").write("\n")


def year(s):
    m = re.search(r"\d{4}", str(s or ""))
    return int(m.group()) if m else None


def site_people():
    s = open("data/family.js", encoding="utf-8").read()
    return {p["id"]: p for p in json.loads(s[s.index("{"): s.rindex("}") + 1])["people"]}


def refs_to_text(text, have):
    """S1 -> [R4-S1] so the reference points at the appended source line."""
    if not text or not have:
        return text or ""
    return re.sub(r"\bS(\d{1,2})\b", lambda m: f"[{RTAG}-S{m.group(1)}]" if f"S{m.group(1)}" in have else m.group(0), text)


def fmt_source(s):
    cite = (s.get("citation") or "").strip()
    url = (s.get("url") or "").strip()
    cls = s.get("class")
    out = f"[{RTAG}-{s.get('ref', '')}] {cite}"
    if cls:
        out += f" ({cls})"
    if url:
        out += f" {url}"
    return out


def norm_date(d):
    if not d:
        return ""
    d = str(d).strip()
    d = re.sub(r"\s*\(.*?\)", "", d).strip()
    low = d.lower()
    for pre, rep in (("bapt.", "ABT"), ("baptized", "ABT"), ("abt", "ABT"), ("about", "ABT"), ("c.", "ABT"),
                     ("ca.", "ABT"), ("bef.", "BEF"), ("before", "BEF"), ("aft.", "AFT"), ("after", "AFT")):
        if low.startswith(pre):
            d = rep + " " + d[len(pre):].strip()
            break
    m = re.match(r"^(\d{1,2}) ([A-Za-z]{3})[a-z]* (\d{4})$", d)
    if m:
        mon = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}.get(m.group(2).lower())
        if mon:
            d = f"{m.group(3)}-{mon:02d}-{int(m.group(1)):02d}"
    return d


def copy_media(pid, m):
    """Copy a downloaded file into media/<pid>/; return the site-relative path or None."""
    lp = (m.get("localPath") or m.get("suggestedFile") or "").replace("research_output/", "")
    if not lp:
        return None
    src = os.path.join(MEDIA_SRC, lp.replace("media/", "", 1)) if lp.startswith("media/") else os.path.join(MEDIA_SRC, lp)
    if not os.path.exists(src):
        return None
    name = re.sub(r"[^a-z0-9.]+", "-", os.path.basename(lp).lower()).strip("-")
    dst = os.path.join("media", pid, name)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        shutil.copyfile(src, dst)
        if Image and os.path.getsize(dst) > 2_000_000 and dst.lower().endswith((".jpg", ".jpeg", ".png")):
            try:
                im = Image.open(dst)
                im.thumbnail((2400, 2400))
                if dst.lower().endswith(".png"):
                    im.save(dst, optimize=True)
                else:
                    im.convert("RGB").save(dst, quality=85, optimize=True)
            except Exception as e:  # noqa
                print("  resize failed", dst, e, file=sys.stderr)
    return dst


MEDIA_TYPE = {"portrait": "photo", "photo": "photo", "gravestone": "photo", "record": "record", "document": "document",
              "newspaper": "document", "book": "document", "map": "document", "link": "link"}


def import_person(pid, d, site, stats):
    path = f"data/research/{pid}.json"
    r = load(path, {"id": pid})
    if any(TAG in (e.get("note") or "") and "imported" in (e.get("note") or "") for e in r.get("researchLog", [])):
        return
    log = r.setdefault("researchLog", [])
    status = d.get("status")
    if status == "living_detected":
        log.append({"date": TODAY, "note": f"{LABEL} ({TAG} imported): identified as a living person; not researched further."})
        save(path, r); stats["living"] += 1
        return
    if status == "minor_limited":
        log.append({"date": TODAY, "note": f"{TAG}: a child; recorded by name and relationship only."})
        save(path, r); stats["living"] += 1
        return
    deceased = status == "deceased_detected"
    have = {s.get("ref") for s in d.get("sources", [])}
    p = site.get(pid, {})
    u = d.get("updates") or {}
    # vital events
    for key in ("birth", "death"):
        up = u.get(key)
        if not up or not (up.get("date") or up.get("place")):
            continue
        cur = r.get(key) or p.get(key) or {}
        nd, cd = norm_date(up.get("date")), cur.get("date") or ""
        apply_date = bool(nd) and (not cd or year(nd) == year(cd) or (pid, key) in RESOLVED_DATES or deceased)
        new = dict(cur)
        if apply_date:
            new["date"] = nd
        elif nd and year(nd) != year(cd):
            r.setdefault("conflicts", [])
            if not any(c.get("field") == f"{key}.date" for c in r["conflicts"]):
                r["conflicts"].append({"field": f"{key}.date", "site": cd, "found": nd,
                                       "assessment": LABEL + " found a different date; the tree value is kept until a certificate settles it."})
        if up.get("place") and (not cur.get("place") or apply_date):
            new["place"] = up["place"]
        if new != cur:
            r[key] = new; stats["vitals"] += 1
    if u.get("burial") and (u["burial"].get("place") or u["burial"].get("cemetery")):
        b = u["burial"]; place = ", ".join(x for x in (b.get("cemetery"), b.get("place")) if x)
        cur = r.get("burial") or p.get("burial") or {}
        if not cur.get("place"):
            r["burial"] = dict(cur, place=place, **({"date": norm_date(b["date"])} if b.get("date") else {}))
    for a in u.get("aka") or []:
        if a and a not in (r.get("aka") or []) and a not in (p.get("aka") or []):
            r.setdefault("aka", list(p.get("aka") or [])).append(a)
    if u.get("occupation"):
        if not (r.get("occupation") or p.get("occupation")):
            r["occupation"] = u["occupation"]
        elif u["occupation"] not in (r.get("occupation") or p.get("occupation") or ""):
            r.setdefault("facts", list(p.get("facts") or [])).append({"label": "Occupation (round 4)", "value": u["occupation"]})
    def with_refs(txt, refs):
        refs = [x for x in (refs or []) if x in have]
        return (txt or "") + ((" " if txt else "") + " ".join(f"[{RTAG}-{x}]" for x in refs) if refs else "")
    for key in ("residences", "events", "military"):
        items = u.get(key) or []
        if not items:
            continue
        cur = r.get(key) or list(p.get(key) or [])
        for it in items:
            it = dict(it); refs = it.pop("sourceRefs", None)
            if key == "events":
                it["description"] = with_refs(it.get("description"), refs)
                it["date"] = norm_date(it.get("date"))
            else:
                it["note"] = with_refs(it.get("note"), refs)
            if it not in cur:
                cur.append(it)
        r[key] = cur
    extra_events = []
    for e in u.get("education") or []:
        extra_events.append({"title": f"Education: {e.get('school', '')}", "date": e.get("years", ""), "place": "",
                             "description": with_refs(e.get("detail", ""), e.get("sourceRefs"))})
    for c in u.get("career") or []:
        extra_events.append({"title": f"{c.get('role', '')}, {c.get('organization', '')}".strip(", "), "date": c.get("years", ""), "place": "",
                             "description": with_refs(c.get("detail", ""), c.get("sourceRefs"))})
    for a in u.get("awards") or []:
        extra_events.append({"title": a.get("title", ""), "date": norm_date(a.get("date", "")), "place": "",
                             "description": with_refs(a.get("detail", ""), a.get("sourceRefs"))})
    if extra_events:
        cur = r.get("events") or list(p.get("events") or [])
        for it in extra_events:
            if it not in cur:
                cur.append(it)
        r["events"] = cur
    for f in u.get("facts") or []:
        cur = r.get("facts") or list(p.get("facts") or [])
        f = {"label": f.get("label", ""), "value": f.get("value", "")}
        if f not in cur:
            cur.append(f)
        r["facts"] = cur
    if d.get("bioAdditions"):
        add = refs_to_text(d["bioAdditions"].strip(), have)
        if NOTES_ONLY:
            notes = r.get("researchNotes") or ""
            if add not in notes:
                r["researchNotes"] = (notes + "\n\n" if notes else "") + f"{TAG}: " + add
                stats["bios"] += 1
        else:
            base = r.get("bio") or p.get("bio") or ""
            if add not in base:
                r["bio"] = (base + "\n\n" if base else "") + add
                stats["bios"] += 1
    for ff in d.get("funFacts") or []:
        cur = r.get("funFacts") or list(p.get("funFacts") or [])
        if ff not in cur:
            cur.append(ff)
        r["funFacts"] = cur
    for c in d.get("conflicts") or []:
        r.setdefault("conflicts", [])
        entry = {"field": c.get("field", ""), "site": c.get("siteValue", ""), "found": c.get("foundValue", ""),
                 "assessment": refs_to_text(c.get("assessment", ""), have)}
        if not any(x.get("field") == entry["field"] and x.get("found") == entry["found"] for x in r["conflicts"]):
            r["conflicts"].append(entry); stats["conflicts"] += 1
    cr = d.get("confidenceRecommendation")
    if cr and cr.get("recommended") and cr.get("recommended") != cr.get("current"):
        link = dict(r.get("link") or p.get("link") or {})
        old = link.get("confidence", cr.get("current"))
        link["confidence"] = cr["recommended"]
        link["note"] = ((link.get("note") or "").strip() + " " if link.get("note") else "") + f"{LABEL} ({old} → {cr['recommended']}): {refs_to_text(cr.get('justification', ''), have)}"
        r["link"] = link
        log.append({"date": TODAY, "note": f"Confidence {old} → {cr['recommended']}: {refs_to_text(cr.get('justification', ''), have)}"})
        stats["confidence"] += 1
    oq = list(r.get("openQuestions") or p.get("openQuestions") or [])
    for res in d.get("openQuestionsResolved") or []:
        q = (res.get("question") or "").strip()
        before = len(oq)
        oq = [x for x in oq if not (x.strip() == q or (len(q) > 25 and (x.strip().startswith(q[:40]) or q.startswith(x.strip()[:40]))))]
        log.append({"date": TODAY, "note": f"Resolved: {q} → {refs_to_text(res.get('answer', ''), have)}"})
        if len(oq) < before:
            stats["resolved"] += 1
    for q in d.get("openQuestionsNew") or []:
        if q and q not in oq:
            oq.append(q)
    if oq or "openQuestions" in r:
        r["openQuestions"] = oq
    for rel in d.get("relationships") or []:
        if rel.get("personId", "").startswith("NEW-"):
            continue
        if rel.get("type") in ("parent", "spouse", "child") and rel.get("strength") in ("proven", "probable") and rel.get("evidence"):
            log.append({"date": TODAY, "note": f"{LABEL} relationship evidence ({rel['type']} {rel['personId']}, {rel['strength']}): {refs_to_text(rel['evidence'], have)}"})
    srcs = r.get("sources") or list(p.get("sources") or [])
    for s in d.get("sources") or []:
        line = fmt_source(s)
        if line not in srcs:
            srcs.append(line)
    if srcs:
        r["sources"] = srcs
    # media
    media = r.get("media") or []
    for m in d.get("media") or []:
        title = (m.get("title") or "Untitled").strip()
        people = [x for x in (m.get("people") or []) if x != pid and not str(x).startswith("NEW-")]
        source = ", ".join(x for x in (m.get("repository"), m.get("rights")) if x)
        entry = None
        if m.get("downloaded") and m.get("downloadable"):
            dst = copy_media(pid, m)
            if dst:
                t = MEDIA_TYPE.get(m.get("type"), "record")
                entry = {"file": dst, "type": t, "title": title, "date": m.get("date") or "", "source": source,
                         "note": m.get("note") or "", "people": people}
                if m.get("pageUrl"):
                    entry["url"] = m["pageUrl"]
                if m.get("type") == "portrait" and not (r.get("photo") or p.get("photo")):
                    r["photo"] = dst; stats["portraits"] += 1
                stats["files"] += 1
        if entry is None and (m.get("pageUrl") or m.get("directUrl")):
            entry = {"url": m.get("pageUrl") or m.get("directUrl"), "type": "link", "title": title, "date": m.get("date") or "",
                     "source": source, "note": (m.get("note") or "") + ("" if m.get("downloaded") else " (not downloaded: rights " + str(m.get("rights")) + ")"), "people": people}
            stats["links"] += 1
        if entry and not any((x.get("file") and x.get("file") == entry.get("file")) or (x.get("url") and x.get("url") == entry.get("url") and not entry.get("file")) for x in media):
            media.append(entry)
    for key, kind in (("onlinePresence", "link"), ("newsArticles", "link")):
        for m in d.get(key) or []:
            url = m.get("url") or m.get("pageUrl")
            if not url or any(x.get("url") == url for x in media):
                continue
            title = m.get("title") or m.get("site") or m.get("outlet") or url
            src = ", ".join(x for x in (m.get("site") or m.get("outlet") or m.get("publication"), m.get("date")) if x)
            media.append({"url": url, "type": kind, "title": title, "date": m.get("date") or "", "source": src,
                          "note": (m.get("note") or m.get("summary") or "")[:300], "people": []})
            stats["links"] += 1
    if media:
        r["media"] = media
    if d.get("searchedNoResult"):
        log.append({"date": TODAY, "note": LABEL + " searched without result: " + "; ".join(d["searchedNoResult"])[:1500]})
    if d.get("researchLogEntry"):
        log.append({"date": TODAY, "note": d["researchLogEntry"]})
    log.append({"date": TODAY, "note": f"{LABEL} ({TAG} imported) from research/imported/{ROUND}/people/{pid}.json."})
    save(path, r)
    stats["people"] += 1


def split_name(name):
    name = name.strip()
    aka = []
    m = re.search(r"\((.*?)\)", name)
    if m:
        aka.append(m.group(1).strip()); name = re.sub(r"\s*\(.*?\)", "", name).strip()
    name = re.sub(r"\s+(the elder|1st|4th|I|Jr\.?|Sr\.?)$", lambda mm: "", name).strip()
    toks = name.split()
    if len(toks) == 1:
        return toks[0], "", aka
    # bracketed surname guesses like "[Feraco/Iera/Marrello?]" -> unknown
    if toks[-1].startswith("["):
        return " ".join(toks[:-1]), "", aka + [toks[-1].strip("[]")]
    return " ".join(toks[:-1]), toks[-1], aka


def import_new_people(site, stats):
    newp = load(os.path.join(SRC, "new_people.json"), [])
    man = load("data/additions-manual.json", {"people": [], "families": [], "familyUpdates": [], "setParents": []})
    man.setdefault("familyUpdates", []); man.setdefault("setParents", []); man.setdefault("merges", [])
    idmap = load(os.path.join(SRC, "_work", "new_ids.json"), {})
    idmap.update(PRESET_IDS)
    newp = [np_ for np_ in newp if np_["id"] not in SKIP_NEW]
    nxt = max([int(p["id"][1:]) for p in man["people"]] + [36]) + 1
    fnxt = max([int(f["id"][2:]) for f in man["families"]] + [9]) + 1
    s = open("data/family.js", encoding="utf-8").read()
    fams = json.loads(s[s.index("{"): s.rindex("}") + 1])["families"] + man["families"]
    for np_ in newp:
        if np_["id"] not in idmap:
            idmap[np_["id"]] = f"M{nxt:04d}"; nxt += 1
    def mid(x):
        return idmap.get(x, x)
    existing = {p["id"] for p in man["people"]} | set(site)
    for np_ in newp:
        pid = mid(np_["id"])
        if pid in existing:
            continue
        given, sur, aka = split_name(np_["name"])
        person = {"id": pid, "given": given, "surname": sur, "sex": np_.get("sex") or ("F" if re.search(r"\b(Mrs|Maria|Anna|Mary|Filomena|Antonia|Grazia|Margaret|Bethia|Deliverance|Christina|Cecilia|Giuseppa|Angela|Fenice|Giacinta|Cintia)\b", np_["name"]) else "M")}
        if aka: person["aka"] = aka
        for key in ("birth", "death"):
            v = np_.get(key) or {}
            if v.get("date") or v.get("place"):
                person[key] = {k: (norm_date(v[k]) if k == "date" else v[k]) for k in ("date", "place") if v.get(k)}
        if np_.get("burial"):
            b = np_["burial"]; person["burial"] = {"place": ", ".join(x for x in (b.get("cemetery"), b.get("place")) if x)}
        man["people"].append(person); existing.add(pid); stats["newPeople"] += 1
        # research file
        have = {x.get("ref") for x in np_.get("sources", [])}
        strengths = [r_.get("strength") for r_ in np_.get("relationships", [])]
        conf = "probable" if any(x in ("proven", "confirmed") for x in strengths) else ("possible" if "probable" in strengths else "possible")
        rels = "; ".join(f"{r_['type']} of {mid(r_['personId'])}" + (f" ({r_['strength']})" if r_.get("strength") else "") for r_ in np_.get("relationships", []))
        rf = {"id": pid, "link": {"confidence": conf, "note": f"Added by {LABEL.lower()} research (2026-10-08) from records; relationship: {rels}."},
              "tags": [], "summary": (np_.get("bio") or "").split(". ")[0][:220], "bio": refs_to_text(np_.get("bio", ""), have),
              "sources": [fmt_source(x) for x in np_.get("sources", [])], "manual": True,
              "researchLog": [{"date": TODAY, "note": f"{LABEL} ({TAG} imported): new relative {np_['id']} → {pid}; research/imported/{ROUND}/new_people.json."}]}
        for key in ("residences", "events", "facts", "funFacts"):
            if np_.get(key):
                rf[key] = np_[key]
        if np_.get("occupation"):
            rf["occupation"] = np_["occupation"]
        save(f"data/research/{pid}.json", rf)
    # families from relationships
    def fam_of_child(x):
        for f in fams:
            if x in f.get("children", []):
                return f
    def fam_of_couple(a, b):
        for f in fams:
            if {f.get("husband"), f.get("wife")} == {a, b}:
                return f
    def sex_of(x):
        for p in man["people"]:
            if p["id"] == x: return p.get("sex")
        return (site.get(x) or {}).get("sex")
    def new_family(**kw):
        nonlocal fnxt
        f = {"id": f"MF{fnxt:04d}", "children": []}; fnxt += 1
        f.update({k: v for k, v in kw.items() if v})
        man["families"].append(f); fams.append(f); return f
    def set_slot(f, person):
        slot = "husband" if sex_of(person) == "M" else "wife"
        if f.get(slot) and f[slot] != person:
            return False
        if f["id"].startswith("MF"):
            f[slot] = person
        else:
            upd = next((u for u in man["familyUpdates"] if u["id"] == f["id"]), None)
            if not upd:
                upd = {"id": f["id"]}; man["familyUpdates"].append(upd)
            upd[slot] = person; f[slot] = person
        return True
    def add_child(f, child):
        if child in f.get("children", []):
            return
        if f["id"].startswith("MF"):
            f["children"].append(child)
        else:
            upd = next((u for u in man["familyUpdates"] if u["id"] == f["id"]), None)
            if not upd:
                upd = {"id": f["id"]}; man["familyUpdates"].append(upd)
            upd.setdefault("addChildren", []).append(child); f.setdefault("children", []).append(child)
    order = {"spouse": 0, "parent": 1, "child": 2, "sibling": 3}
    byid = {np_["id"]: np_ for np_ in newp}
    def birth_year(x):
        if x in byid: return year((byid[x].get("birth") or {}).get("date"))
        for p in man["people"]:
            if p["id"] == x: return year((p.get("birth") or {}).get("date"))
        return year(((site.get(x) or {}).get("birth") or {}).get("date"))
    OVERRIDES = {  # reviewed by hand against the bios and dates (8 Oct 2026)
        **{(f"NEW-{n}", None): "parent_of" for n in (703, 704, 705, 706, 707, 708, 709, 710)},
        ("NEW-807", "I282824815569"): "parent_of", ("NEW-604", "H0289"): "parent_of", ("NEW-611", "NEW-604"): "parent_of",
        ("NEW-605", "H0517"): "parent_of", ("NEW-607", "H0495"): "parent_of",
        ("NEW-101", "H0012"): "child_of", ("NEW-101", "H0054"): "child_of", ("NEW-102", "H0012"): "child_of",
        ("NEW-103", "H0012"): "child_of", ("NEW-104", "H0027"): "child_of",
    }
    OVERRIDES.update(DIR_OVERRIDES)
    def direction(np_, r_):
        if r_["type"] in ("parent", "child"):
            o = OVERRIDES.get((np_["id"], r_["personId"])) or OVERRIDES.get((np_["id"], None))
            if o: return o
        """Workers used 'parent'/'child' in both directions. Decide who is the child: returns
        'child_of' (new person is the child of X) or 'parent_of' (new person is a parent of X)."""
        typ = r_["type"]; other = r_["personId"]
        if typ not in ("parent", "child"): return typ
        yb, yo = birth_year(np_["id"]), birth_year(other)
        if yb and yo and abs(yb - yo) >= 14:
            return "child_of" if yb > yo else "parent_of"
        bio = (np_.get("bio") or "") + " " + (r_.get("evidence") or "")
        oname = (byid.get(other, {}).get("name") or f"{(site.get(other) or {}).get('given', '')} {(site.get(other) or {}).get('surname', '')}").strip()
        first = oname.split()[0] if oname else ""
        if re.search(r"\b(daughter|son|child) of\b", bio, re.I) and (not first or first in bio): return "child_of"
        if re.search(r"\b(father|mother|parent|parents) of\b", bio, re.I) and (not first or first in bio): return "parent_of"
        if re.search(r"\b(daughter|son) of\b", bio, re.I): return "child_of"
        if re.search(r"\b(father|mother) of\b", bio, re.I): return "parent_of"
        # group conventions seen in the files: Irish (2xx) 'child' = is child of; Calabria (8xx) 'parent' = is parent of;
        # Long Island (6xx) literal (parent = X is my parent, child = X is my child)
        blk = np_["id"][4]
        if typ == "child": return "child_of" if blk in "2347" else "parent_of"
        return "parent_of" if blk in "2378" else "child_of"
    todo = []
    for np_ in newp:
        for r_ in np_.get("relationships", []):
            typ = direction(np_, r_)
            if typ in ("parent", "child"): typ = "child_of" if typ == "child" else "parent_of"
            todo.append((order.get(typ.split("_")[0], 9), mid(np_["id"]), typ, mid(r_["personId"]), np_["name"]))
    todo.sort()
    if os.environ.get("ROUND4_DRY"):
        for _, me, typ, other, name in todo:
            o = site.get(other) or next((p for p in man["people"] if p["id"] == other), {})
            print(f"PLAN {name[:40]:<40} ({me}) {typ:<10} {other} {o.get('given', '')} {o.get('surname', '')} {((o.get('birth') or {}).get('date', ''))}")
        return idmap, ["dry run"]
    notes = []
    for _, me, typ, other, name in todo:
        if typ in ("cousin", "niece", "grandchild", "nephew"):
            continue
        if typ == "spouse":
            f = fam_of_couple(me, other)
            if f: continue
            # a family of `other` with an empty opposite slot?
            cand = [f for f in fams if other in (f.get("husband"), f.get("wife")) and not f.get("husband" if sex_of(me) == "M" else "wife")]
            if cand: set_slot(cand[0], me)
            else: new_family(**{("husband" if sex_of(me) == "M" else "wife"): me, ("wife" if sex_of(me) == "M" else "husband"): other})
        elif typ == "parent_of":
            f = fam_of_child(other)
            if f and me in (f.get("husband"), f.get("wife")): continue
            if f and not f.get("husband" if sex_of(me) == "M" else "wife"):
                set_slot(f, me)
            elif f:
                notes.append(f"{name} ({me}) is given as a parent of {other}, but that person already has two parents in the tree; not changed.")
            else:
                nf = new_family(**{("husband" if sex_of(me) == "M" else "wife"): me}); add_child(nf, other)
        elif typ == "child_of":
            f = fam_of_child(me)
            if f and other in (f.get("husband"), f.get("wife")): continue
            cands = [f for f in fams if other in (f.get("husband"), f.get("wife"))]
            if f and f not in cands:
                # already placed under another couple: try to make `other` the missing parent of that family
                if not set_slot(f, other):
                    notes.append(f"{name} ({me}) is given as a child of {other}, but is already placed with other parents; not changed.")
                continue
            if cands:
                # prefer the couple whose other parent is also named in relationships
                wanted = {o for _, m2, t2, o, _ in todo if m2 == me and t2 == "child_of"}
                best = next((c for c in cands if {c.get("husband"), c.get("wife")} <= wanted | {None}), None)
                add_child(best or cands[0], me)
            else:
                nf = new_family(**{("husband" if sex_of(other) == "M" else "wife"): other}); add_child(nf, me)
        elif typ == "sibling":
            if fam_of_child(me): continue
            f = fam_of_child(other)
            if f: add_child(f, me)
            else: notes.append(f"{name} ({me}) is a sibling of {other}, whose parents are not in the tree; left unattached.")
    save("data/additions-manual.json", man)
    save(os.path.join(SRC, "_work", "new_ids.json"), idmap)
    return idmap, notes


def import_stories(idmap, stats):
    stories = load("data/stories.json", [])
    excl = load("data/story-exclusions.json", {"excluded": {}})
    new = load(os.path.join(SRC, "stories.json"), [])
    have = {s.get("title") for s in stories}
    n = max([int(s["id"][1:]) for s in stories if re.match(r"S\d+$", s.get("id", ""))] + [0])
    EXCLUDE = {"How William Wells's widow became 'Mary Youngs'": "research correction, not a family story",
               "A will that settles a mother: Captain Thomas Davenport, 1746": "evidence discussion, not a family story"}
    for st in new:
        if st["title"] in have:
            continue
        n += 1; sid = f"S{n:03d}"
        src = "; ".join(f"{x.get('citation', '')}{' ' + x['url'] if x.get('url') else ''}" for x in st.get("sourceRefs", []))
        stories.append({"id": sid, "title": st["title"], "date": st.get("date") or "", "people": [idmap.get(x, x) for x in st.get("people", [])],
                        "body": refs_to_text(st.get("body", ""), {x.get("ref") for x in st.get("sourceRefs", [])}), "source": src})
        if st["title"] in EXCLUDE:
            if isinstance(excl.get("excluded"), dict):
                excl["excluded"][sid] = EXCLUDE[st["title"]]
            else:
                excl.setdefault("excluded", []).append(sid)
        stats["stories"] += 1
    save("data/stories.json", stories); save("data/story-exclusions.json", excl)


def write_leads(idmap, site):
    leads = load(os.path.join(SRC, "leads.json"), [])
    out = [f"# Research leads from {ROUND} (8 Oct 2026)", "", "Records seen only as index entries or snippets; each needs the actual record (paywalled or orderable). Source: `research/imported/{ROUND}/leads.json`.", "",
           "| Person | Collection | Search terms | What the snippet shows | Why it matters |", "|---|---|---|---|---|"]
    for l in leads:
        pid = idmap.get(l.get("personId"), l.get("personId"))
        p = site.get(pid, {}); nm = f"{p.get('given', '')} {p.get('surname', '')}".strip() or pid
        cell = lambda x: (x or "").replace("|", "/").replace("\n", " ")
        out.append(f"| {nm} (`{pid}`) | {cell(l.get('collection'))} ({cell(l.get('site'))}) | {cell(l.get('searchTerms'))} | {cell(l.get('whatTheSnippetShows'))} | {cell(l.get('whyItMatters'))} |")
    open(LEADS_FILE, "w", encoding="utf-8").write("\n".join(out) + "\n")


def main():
    site = site_people()
    stats = {k: 0 for k in ("people", "living", "vitals", "bios", "conflicts", "confidence", "resolved", "files", "links", "portraits", "newPeople", "stories")}
    idmap, notes = import_new_people(site, stats)
    if os.environ.get("ROUND4_DRY"):
        return
    pdir = os.path.join(SRC, "people")
    for fn in sorted(os.listdir(pdir)):
        pid = fn[:-5]
        if pid not in site:
            print("skip unknown", pid); continue
        d = load(os.path.join(pdir, fn), None)
        if d:
            import_person(pid, d, site, stats)
    import_stories(idmap, stats)
    write_leads(idmap, site)
    print(json.dumps(stats, indent=1))
    for n in notes:
        print("note:", n)
    json.dump(notes, open(os.path.join(SRC, "_work", "import_notes.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
