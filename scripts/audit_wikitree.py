#!/usr/bin/env python3
"""Re-check every WikiTree match in research/wikitree-matches.json against the
current matching rules (dates, first name, place consistency) and undo the
attachments of matches that no longer pass: media entries, downloaded files and
the portrait are removed and the report entry is marked "rejected".

Run after scripts/find_wikitree.py when the rules have been tightened, or with
--reject ID1,ID2 to reject specific matches by hand.
"""
import argparse, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import find_wikitree as fw  # noqa: E402

REPORT = fw.REPORT


def undo(pid, key):
    f = os.path.join(ROOT, "data", "research", f"{pid}.json")
    if not os.path.exists(f):
        return 0
    d = json.load(open(f))
    keep, removed = [], 0
    for m in d.get("media", []):
        src = (m.get("source") or "") + " " + (m.get("title") or "")
        if f"profile {key}" in src or f"WikiTree {key}" in src or f"wikitree.com/wiki/{key}" in (m.get("url") or ""):
            removed += 1
            if m.get("file"):
                fp = os.path.join(ROOT, m["file"])
                if os.path.exists(fp):
                    os.remove(fp)
                if d.get("photo") == m["file"]:
                    d.pop("photo", None)
        else:
            keep.append(m)
    d["media"] = keep
    if not d["media"]:
        d.pop("media", None)
    d.setdefault("researchLog", []).append({"date": fw.TODAY, "note": f"WikiTree profile {key} rejected on review (dates or places do not fit); its links and images removed."})
    json.dump(d, open(f, "w"), indent=2, ensure_ascii=False)
    open(f, "a").write("\n")
    return removed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reject", help="comma separated person ids to reject by hand")
    ap.add_argument("--keep", help="comma separated person ids to keep even if the rules reject them")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    keep = set(args.keep.split(",")) if args.keep else set()
    people = {p["id"]: p for p in fw.load_people()}
    report = json.load(open(REPORT))
    manual = set(args.reject.split(",")) if args.reject else set()
    rejected = 0
    for pid, r in report.items():
        if r.get("status") != "matched":
            continue
        p = people.get(pid)
        if not p:
            continue
        m = {"FirstName": (r.get("wt_name") or "").split(" ")[0], "LastNameAtBirth": p.get("surname"),
             "LastNameCurrent": p.get("surname"), "BirthDate": r.get("wt_birth"), "DeathDate": r.get("wt_death"),
             "BirthLocation": r.get("birth_place"), "DeathLocation": r.get("death_place")}
        ok = (fw.score(p, m) is not None or pid in keep) and pid not in manual
        if ok:
            continue
        rejected += 1
        print(f"reject {pid} {p.get('given')} {p.get('surname')} -> {r['key']} ({r.get('wt_birth')}–{r.get('wt_death')}; {r.get('birth_place')} / {r.get('death_place')})")
        if not args.dry:
            n = undo(pid, r["key"])
            r["status"] = "rejected"
            r["rejected"] = fw.TODAY
            r["removed_media"] = n
    if not args.dry:
        json.dump(report, open(REPORT, "w"), indent=1, ensure_ascii=False)
    print("rejected", rejected)


if __name__ == "__main__":
    main()
