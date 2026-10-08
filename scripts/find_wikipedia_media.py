#!/usr/bin/env python3
"""Look every deceased person in the tree up on Wikipedia/Wikidata and collect
portraits from Wikimedia Commons.

For each person with a surname and at least one known year the script searches
English Wikipedia for the name, fetches the Wikidata item of each candidate
article and accepts the match only when the Wikidata birth or death year agrees
with the tree (within one year) and the other known year does not contradict
it. Matches go to research/wikipedia-matches.json. With --attach the Commons
image (if any) is downloaded and attached as the person's portrait (or as a
photo when a portrait already exists) together with a link to the article,
through scripts/attach_media.py.

Living people (no death, born within 105 years) are skipped. Requests are
serial and paced (Wikimedia etiquette); HTTP 429 is honoured with a back-off,
and a person whose lookups failed is marked "retry" and done again next run.

Usage:
    python3 scripts/find_wikipedia_media.py             # search only
    python3 scripts/find_wikipedia_media.py --attach    # attach matched items
    python3 scripts/find_wikipedia_media.py --only I1,I2
"""
import argparse, json, os, re, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "meiertree.com family-tree site (https://meiertree.com)"
REPORT = os.path.join(ROOT, "research", "wikipedia-matches.json")
TMP = os.path.join(ROOT, ".cache", "wikimedia")
TODAY = time.strftime("%Y-%m-%d")
PACE = 3.0
FAILED = False


def get(url, params=None, retries=6):
    global FAILED
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            time.sleep(PACE)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                time.sleep(PACE)
                return None
            if e.code == 429 or e.code >= 500:
                wait = 20 * (i + 1)
                try:
                    wait = max(wait, int(e.headers.get("Retry-After", "0")))
                except Exception:
                    pass
                print(f"  . HTTP {e.code}, waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            print("  ! failed", url, e, file=sys.stderr)
            FAILED = True
            return None
        except Exception as e:  # noqa
            time.sleep(5 * (i + 1))
            if i == retries - 1:
                print("  ! failed", url, e, file=sys.stderr)
                FAILED = True
                return None
    FAILED = True
    return None


def getj(url, params=None):
    b = get(url, params)
    try:
        return json.loads(b) if b else None
    except Exception:
        return None


def year(s):
    if not s:
        return None
    m = re.search(r"\d{4}", str(s))
    return int(m.group(0)) if m else None


def load_people():
    s = open(os.path.join(ROOT, "data", "family.js")).read()
    j = json.loads(s[s.index("{"): s.rindex("}") + 1])
    return j["people"]


def is_living(p):
    if p.get("death") and (p["death"].get("date") or p["death"].get("place")):
        return False
    b = year((p.get("birth") or {}).get("date"))
    return b is not None and b > 1921


def names_for(p):
    given = re.sub(r"[\"'“”].*?[\"'“”]", "", p.get("given") or "").strip()  # drop nicknames
    given = re.sub(r"\s+", " ", given)
    sur = (p.get("surname") or "").strip()
    out = []
    if given and sur:
        out.append(f"{given} {sur}")
        first = given.split()[0]
        if first != given and len(first) > 2:
            out.append(f"{first} {sur}")
    for a in p.get("aka") or []:
        a = (a or "").strip()
        if a and a not in out and len(a.split()) >= 2 and not a.lower().startswith(("mr", "mrs", "sir ")):
            out.append(a)
    return out[:3]


def wd_year(claims, prop):
    for c in claims.get(prop, []):
        try:
            t = c["mainsnak"]["datavalue"]["value"]["time"]
            return int(t[1:5]) * (1 if t[0] == "+" else -1)
        except Exception:
            continue
    return None


def wd_image(claims):
    for c in claims.get("P18", []):
        try:
            return c["mainsnak"]["datavalue"]["value"]
        except Exception:
            continue
    return None


def candidates(query):
    """One API call: search + pageprops + intro for up to 5 articles."""
    j = getj("https://en.wikipedia.org/w/api.php", {
        "action": "query", "generator": "search", "gsrsearch": query, "gsrlimit": 5, "gsrnamespace": 0,
        "prop": "pageprops|extracts", "exintro": 1, "explaintext": 1, "exsentences": 2, "exlimit": 5,
        "format": "json"})
    out = []
    for pid, pg in (j or {}).get("query", {}).get("pages", {}).items():
        qid = (pg.get("pageprops") or {}).get("wikibase_item")
        if qid:
            out.append({"title": pg.get("title"), "qid": qid, "extract": pg.get("extract", "")})
    return out


def wikidata_many(qids):
    """One API call for up to 50 items: {qid: {human, birth, death, image}}."""
    out = {}
    if not qids:
        return out
    j = getj("https://www.wikidata.org/w/api.php", {
        "action": "wbgetentities", "ids": "|".join(qids), "props": "claims", "format": "json"})
    for qid, ent in (j or {}).get("entities", {}).items():
        claims = ent.get("claims", {}) if isinstance(ent, dict) else {}
        human = any(((c.get("mainsnak", {}).get("datavalue", {}) or {}).get("value", {}) or {}).get("id") == "Q5"
                    for c in claims.get("P31", []))
        out[qid] = {"human": human, "birth": wd_year(claims, "P569"), "death": wd_year(claims, "P570"),
                    "image": wd_image(claims)}
    return out


def commons_info(filename):
    j = getj("https://commons.wikimedia.org/w/api.php", {
        "action": "query", "prop": "imageinfo", "iiprop": "url|extmetadata|mime", "iiurlwidth": 1200,
        "titles": "File:" + filename, "format": "json"})
    for pid, pg in (j or {}).get("query", {}).get("pages", {}).items():
        ii = (pg.get("imageinfo") or [None])[0]
        if not ii:
            return None
        em = ii.get("extmetadata", {})
        clean = lambda k: re.sub("<[^>]+>", "", (em.get(k) or {}).get("value", "")).strip()
        return {"url": ii.get("thumburl") or ii.get("url"), "page": ii.get("descriptionurl"),
                "mime": ii.get("mime"), "license": clean("LicenseShortName"),
                "artist": clean("Artist"), "credit": clean("Credit")}
    return None


def match(p, wd):
    tb, td = year((p.get("birth") or {}).get("date")), year((p.get("death") or {}).get("date"))
    wb, wdd = wd["birth"], wd["death"]
    ok = (tb and wb and abs(tb - wb) <= 1) or (td and wdd and abs(td - wdd) <= 1)
    if not ok:
        return False
    if tb and wb and abs(tb - wb) > 2:
        return False
    if td and wdd and abs(td - wdd) > 2:
        return False
    return True


def place_words(p):
    words = []
    for k in ("birth", "death", "burial"):
        pl = ((p.get(k) or {}).get("place") or "").split(",")[0].strip()
        if pl and len(pl) > 3 and pl.lower() not in ("usa", "england", "germany", "italy", "ireland"):
            words.append(pl)
    return list(dict.fromkeys(words))[:2]


def lookup(p):
    """Return a match record, a 'none' record or a 'retry' record."""
    global FAILED
    FAILED = False
    names = names_for(p)
    queries = [f'"{n}"' for n in names]
    for w in place_words(p):
        if names:
            queries.append(f'"{names[0]}" {w}')
    seen = set()
    for q in queries:
        cands = [c for c in candidates(q) if c["qid"] not in seen]
        for c in cands:
            seen.add(c["qid"])
        wd = wikidata_many([c["qid"] for c in cands])
        for c in cands:
            w = wd.get(c["qid"])
            if not w or not w["human"]:
                continue
            if match(p, w):
                return {"status": "matched", "title": c["title"], "qid": c["qid"],
                        "url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(c["title"].replace(" ", "_")),
                        "wd_birth": w["birth"], "wd_death": w["death"], "image": w["image"] or None,
                        "extract": (c.get("extract") or "")[:400], "query": q, "checked": TODAY}
    if FAILED:
        return {"status": "retry", "checked": TODAY, "names": names}
    return {"status": "none", "checked": TODAY, "names": names}


def attach(p, r):
    pid = p["id"]
    research = os.path.join(ROOT, "data", "research", f"{pid}.json")
    existing = json.load(open(research)) if os.path.exists(research) else {}
    urls = {m.get("url") for m in existing.get("media", [])}
    base = [sys.executable, os.path.join(ROOT, "scripts", "attach_media.py"), "--no-build", pid]
    if r["url"] not in urls:
        subprocess.run(base + ["--url", r["url"], "--title", f"Wikipedia: {r['title']}", "--type", "link",
                               "--source", "Wikipedia", "--note", (r.get("extract") or "")[:300]], check=False)
    if r.get("image") and not r.get("portrait_file"):
        ci = commons_info(r["image"])
        mime = (ci or {}).get("mime") or ""
        if ci and ci.get("url") and mime.startswith("image/") and "svg" not in mime:
            os.makedirs(TMP, exist_ok=True)
            ext = ".jpg" if "jpeg" in mime else "." + mime.split("/")[-1]
            fn = os.path.join(TMP, re.sub(r"[^a-z0-9]+", "-", r["title"].lower()).strip("-") + "-portrait" + ext)
            data = get(ci["url"])
            if data and len(data) < 6_000_000:
                open(fn, "wb").write(data)
                args = base + [fn, "--title", f"{r['title']} (Wikimedia Commons)", "--type", "photo",
                               "--source", f"Wikimedia Commons, {ci.get('license') or 'see file page'}; {ci.get('page')}",
                               "--note", (ci.get("artist") or ci.get("credit") or "")[:200]]
                if not existing.get("photo"):
                    args.append("--portrait")
                subprocess.run(args, check=False)
                r["portrait_file"] = os.path.relpath(fn, ROOT)
                r["license"] = ci.get("license")
    r["attached"] = TODAY


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--attach", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", help="comma separated person ids")
    ap.add_argument("--tagged", action="store_true",
                    help="only people with a notable/public-role tag or a 'notable' text (likely to have articles)")
    args = ap.parse_args()
    TAGS = {"notable", "politician", "author", "clergy", "artist", "athlete", "pioneer", "military"}
    people = load_people()
    report = json.load(open(REPORT)) if os.path.exists(REPORT) else {}
    only = set(args.only.split(",")) if args.only else None
    done = 0
    for p in people:
        pid = p["id"]
        if only and pid not in only:
            continue
        if is_living(p) or not (p.get("surname") or "").strip():
            continue
        if not (year((p.get("birth") or {}).get("date")) or year((p.get("death") or {}).get("date"))):
            continue
        if args.tagged and not (p.get("notable") or TAGS & set(p.get("tags") or [])):
            continue
        r = report.get(pid)
        if r is None or r.get("status") == "retry":
            r = report[pid] = lookup(p)
            done += 1
            print(f"{pid:>16} {p.get('given', '')} {p.get('surname', '')}: {r['status']}"
                  + (f" -> {r['title']}" if r['status'] == 'matched' else ""), flush=True)
            if done % 10 == 0:
                json.dump(report, open(REPORT, "w"), indent=1, ensure_ascii=False)
            if args.limit and done >= args.limit:
                break
        if args.attach and r.get("status") == "matched" and not r.get("attached"):
            attach(p, r)
            json.dump(report, open(REPORT, "w"), indent=1, ensure_ascii=False)
    json.dump(report, open(REPORT, "w"), indent=1, ensure_ascii=False)
    m = sum(1 for r in report.values() if r.get("status") == "matched")
    rt = sum(1 for r in report.values() if r.get("status") == "retry")
    print(f"report: {len(report)} checked, {m} matched, {rt} to retry -> {REPORT}")


if __name__ == "__main__":
    main()
