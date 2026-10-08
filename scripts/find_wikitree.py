#!/usr/bin/env python3
"""Match deceased people in the tree to WikiTree profiles and collect their
photos, documents and Find a Grave links.

WikiTree's public API (https://api.wikitree.com) needs no login for open
profiles. For each deceased person with a surname and at least one year the
script calls searchPerson with first name, surname and the known dates
(dateSpread 2). A candidate is accepted when the surname matches, the first
name agrees, every year both sides know is within two years and at least one
is within one year. For an accepted profile it attaches a link to the profile,
any Find a Grave memorial links quoted in the profile's biography, and up to
four WikiTree images (the profile's primary photo becomes the person's portrait
when the person has none).

Results: research/wikitree-matches.json (status matched / none / ambiguous /
retry). Re-running skips people already settled; --attach performs the
downloads for matched people not yet attached.

Usage:
    python3 scripts/find_wikitree.py              # search only
    python3 scripts/find_wikitree.py --attach     # search + attach
    python3 scripts/find_wikitree.py --only I1,I2 --attach
"""
import argparse, json, os, re, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "meiertree.com family-tree site (https://meiertree.com)"
API = "https://api.wikitree.com/api.php"
REPORT = os.path.join(ROOT, "research", "wikitree-matches.json")
TMP = os.path.join(ROOT, ".cache", "wikitree")
TODAY = time.strftime("%Y-%m-%d")
PACE = 1.0
FAILED = False
FIELDS = "Id,Name,FirstName,MiddleName,LastNameAtBirth,LastNameCurrent,BirthDate,DeathDate,BirthLocation,DeathLocation,Photo,Privacy,IsLiving,Gender"


def get(url, params=None, retries=5):
    global FAILED
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
            time.sleep(PACE)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                time.sleep(PACE)
                return None
            wait = 20 * (i + 1)
            print(f"  . HTTP {e.code}, waiting {wait}s", file=sys.stderr)
            time.sleep(wait)
        except Exception as e:  # noqa
            time.sleep(5 * (i + 1))
            if i == retries - 1:
                print("  ! failed", url[:120], e, file=sys.stderr)
    FAILED = True
    return None


def api(params):
    params = dict(params, format="json")
    b = get(API, params)
    try:
        j = json.loads(b) if b else None
        return j[0] if isinstance(j, list) and j else j
    except Exception:
        return None


def year(s):
    if not s:
        return None
    m = re.search(r"\d{4}", str(s))
    return int(m.group(0)) if m and m.group(0) != "0000" else None


def load_people():
    s = open(os.path.join(ROOT, "data", "family.js")).read()
    j = json.loads(s[s.index("{"): s.rindex("}") + 1])
    return j["people"]


def is_living(p):
    if p.get("death") and (p["death"].get("date") or p["death"].get("place")):
        return False
    b = year((p.get("birth") or {}).get("date"))
    return b is not None and b > 1921


def norm(s):
    return re.sub(r"[^a-z]", "", (s or "").lower())


def first_token(given):
    given = re.sub(r"[\"'“”(].*?[\"'“”)]", "", given or "").strip()
    toks = [t for t in re.split(r"[\s.]+", given) if t]
    return toks[0] if toks else ""


def score(p, m):
    """Return a numeric score or None when the candidate is excluded."""
    sur = norm(p.get("surname"))
    if sur not in (norm(m.get("LastNameAtBirth")), norm(m.get("LastNameCurrent"))):
        return None
    ft = norm(first_token(p.get("given")))
    mf = norm(m.get("FirstName"))
    if ft and mf and not (mf.startswith(ft) or ft.startswith(mf) or
                           (len(ft) > 3 and len(mf) > 3 and ft[:4] == mf[:4])):
        return None
    tb, td = year((p.get("birth") or {}).get("date")), year((p.get("death") or {}).get("date"))
    mb, md = year(m.get("BirthDate")), year(m.get("DeathDate"))
    s = 0
    close = False
    compared = 0
    for a, b in ((tb, mb), (td, md)):
        if a and b:
            d = abs(a - b)
            if d > 2:
                return None
            s += 3 - d
            compared += 1
            close = close or d <= 1
    if not close:
        return None
    if ft and mf and mf == ft:
        s += 1
    # places must agree: whenever both sides name any place, they need a word in common
    # (town, county, state or country); with a single comparable year this is required and
    # the first name must match exactly.
    stop = {"county", "united", "states", "usa", "township", "city", "colony", "kingdom", "house", "near"}
    tree_words = set()
    for k in ("birth", "death", "burial"):
        for w in re.split(r"[,\s()]+", ((p.get(k) or {}).get("place") or "")):
            if len(w) > 3 and w.lower() not in stop:
                tree_words.add(w.lower())
    wt_words = set(w.lower() for w in re.split(r"[,\s()]+", (m.get("BirthLocation") or "") + " " + (m.get("DeathLocation") or ""))
                   if len(w) > 3 and w.lower() not in stop)
    if tree_words and wt_words and not (tree_words & wt_words):
        return None
    if compared < 2:
        if not (tree_words & wt_words):
            return None
        if not (ft and mf and mf == ft):
            return None
    return s


def lookup(p):
    global FAILED
    FAILED = False
    params = {"action": "searchPerson", "LastName": p.get("surname", ""), "dateSpread": 2,
              "fields": FIELDS, "limit": 10}
    ft = first_token(p.get("given"))
    if ft:
        params["FirstName"] = ft
    tb, td = year((p.get("birth") or {}).get("date")), year((p.get("death") or {}).get("date"))
    if tb:
        params["BirthDate"] = f"{tb}-01-01"
    if td:
        params["DeathDate"] = f"{td}-01-01"
    j = api(params)
    if j is None:
        return {"status": "retry", "checked": TODAY}
    matches = [m for m in j.get("matches", []) if m.get("Name")]
    scored = []
    for m in matches:
        sc = score(p, m)
        if sc is not None:
            scored.append((sc, m))
    if not scored:
        return {"status": "none", "checked": TODAY, "total": j.get("total", 0)}
    scored.sort(key=lambda x: -x[0])
    best = scored[0]
    others = [m for sc, m in scored[1:] if sc == best[0]]
    if others:
        return {"status": "ambiguous", "checked": TODAY,
                "candidates": [m["Name"] for sc, m in scored[:5]]}
    m = best[1]
    return {"status": "matched", "checked": TODAY, "key": m["Name"], "wt_id": m.get("Id"),
            "wt_name": " ".join(x for x in (m.get("FirstName"), m.get("MiddleName"), m.get("LastNameAtBirth")) if x),
            "wt_birth": m.get("BirthDate"), "wt_death": m.get("DeathDate"),
            "birth_place": m.get("BirthLocation"), "death_place": m.get("DeathLocation"),
            "photo": m.get("Photo") or None, "url": "https://www.wikitree.com/wiki/" + m["Name"]}


def full_image_url(ph):
    """Turn the API's thumbnail path into the full-size image URL."""
    t = ph.get("URL_300") or ""
    mm = re.match(r"/photo\.php/thumb/(.+?)/\d+px-", t)
    if mm:
        return "https://www.wikitree.com/photo.php/" + mm.group(1)
    return None


def attach(p, r):
    pid = p["id"]
    research = os.path.join(ROOT, "data", "research", f"{pid}.json")
    existing = json.load(open(research)) if os.path.exists(research) else {}
    urls = {m.get("url") for m in existing.get("media", [])}
    files = {os.path.basename(m.get("file") or "") for m in existing.get("media", [])}
    base = [sys.executable, os.path.join(ROOT, "scripts", "attach_media.py"), "--no-build", pid]
    key = r["key"]
    # profile link
    if r["url"] not in urls:
        subprocess.run(base + ["--url", r["url"], "--title", f"WikiTree profile {key}", "--type", "link",
                               "--source", "WikiTree",
                               "--note", f"{r.get('wt_name', '')}, {r.get('wt_birth', '')} – {r.get('wt_death', '')}"], check=False)
    # Find a Grave links from the biography
    j = api({"action": "getPerson", "key": key, "fields": "Id,Name,Bio", "bioFormat": "text"})
    bio = ((j or {}).get("person") or {}).get("bio") or ""
    fg = sorted(set(re.findall(r"https?://(?:www\.)?findagrave\.com/memorial/\d+[^\s\]\|<\"']*", bio)))
    r["findagrave"] = fg
    for u in fg[:2]:
        u = u.rstrip(".,)")
        if u not in urls:
            subprocess.run(base + ["--url", u, "--title", "Find a Grave memorial", "--type", "link",
                                   "--source", f"Find a Grave (cited on WikiTree {key})"], check=False)
    # photos
    j = api({"action": "getPhotos", "key": key, "limit": 6})
    photos = (j or {}).get("photos") or []
    got = 0
    os.makedirs(TMP, exist_ok=True)
    for ph in photos:
        if got >= 4:
            break
        if (ph.get("Type") or "photo") != "photo":
            continue
        src = full_image_url(ph)
        if not src:
            continue
        name = re.sub(r"[^a-z0-9.]+", "-", (ph.get("ImageName") or "").lower()).strip("-")
        if not name or name in files:
            continue
        fn = os.path.join(TMP, f"{pid}-{name}")
        if not os.path.exists(fn):
            data = get(src)
            if not data or len(data) < 1000 or len(data) > 6_000_000:
                continue
            open(fn, "wb").write(data)
        title = ph.get("Title") or r.get("wt_name") or key
        is_primary = bool(r.get("photo")) and ph.get("ImageName") == r.get("photo")
        doc = bool(re.search(r"\b(will|pp?\.?\s*\d|page|record|census|deed|probate|register|map|book|certificate|"
                             r"marriage|baptism|burial|obituary|letter|document|index|list|chart|tree|passenger)\b",
                             title, re.I)) and not is_primary
        args = base + [fn, "--title", f"{title} (WikiTree)", "--type", "document" if doc else "photo",
                       "--source", f"WikiTree, profile {key}; https://www.wikitree.com{ph.get('URL', '')}"]
        if ph.get("Date") and ph["Date"] != "0000-00-00":
            args += ["--date", ph["Date"][:4] if ph["Date"].endswith("00-00") else ph["Date"]]
        if is_primary and not existing.get("photo"):
            args.append("--portrait")
            existing["photo"] = "set"
        subprocess.run(args, check=False)
        got += 1
    r["photos"] = got
    r["attached"] = TODAY


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--attach", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only")
    args = ap.parse_args()
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
        r = report.get(pid)
        if r is None or r.get("status") == "retry":
            r = report[pid] = lookup(p)
            done += 1
            print(f"{pid:>16} {p.get('given', '')} {p.get('surname', '')}: {r['status']}"
                  + (f" -> {r['key']} ({r.get('wt_birth')}–{r.get('wt_death')})" if r['status'] == 'matched' else ""),
                  flush=True)
            if done % 10 == 0:
                json.dump(report, open(REPORT, "w"), indent=1, ensure_ascii=False)
            if args.limit and done >= args.limit:
                break
        if args.attach and r.get("status") == "matched" and not r.get("attached"):
            attach(p, r)
            json.dump(report, open(REPORT, "w"), indent=1, ensure_ascii=False)
    json.dump(report, open(REPORT, "w"), indent=1, ensure_ascii=False)
    c = {}
    for r in report.values():
        c[r.get("status")] = c.get(r.get("status"), 0) + 1
    print("report:", c, "->", REPORT)


if __name__ == "__main__":
    main()
