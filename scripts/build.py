#!/usr/bin/env python3
"""Merge data/site.json + data/tree.json + data/research/*.json + data/stories.json
into data/family.js, the single file the website loads.

Usage:  python3 scripts/build.py            (run from the repository root)
        python3 scripts/build.py --check    (validate only, write nothing)

Research files overlay the tree: every key in data/research/<id>.json is
copied onto the person with that id (the "id" key itself is ignored).
"""
import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIDENCE = ("confirmed", "probable", "possible", "unverified")


def load(path, default):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    os.chdir(ROOT)

    site = load("data/site.json", {})
    tree = load("data/tree.json", {"people": [], "families": []})
    stories = load("data/stories.json", [])
    problems, warnings = [], []

    people = {p["id"]: p for p in tree.get("people", [])}
    families = tree.get("families", [])

    # Additions: people and families found by research beyond the GEDCOM, and parent corrections
    adds = load("data/additions.json", {})
    manual = load("data/additions-manual.json", {})
    for key in ("people", "families", "familyUpdates", "setParents"):
        adds[key] = list(adds.get(key, [])) + list(manual.get(key, []))
    for p in adds.get("people", []):
        if p["id"] in people:
            warnings.append("additions: person %s already in tree.json (skipped)" % p["id"])
        else:
            p = dict(p); p["source"] = "research"; people[p["id"]] = p
    fam_ids = {f["id"] for f in families}
    for f in adds.get("families", []):
        if f["id"] in fam_ids:
            problems.append("additions: family id %s duplicates a tree family" % f["id"])
        else:
            families.append(dict(f)); fam_ids.add(f["id"])
    fam_by_id = {f["id"]: f for f in families}
    for upd in adds.get("familyUpdates", []):
        f = fam_by_id.get(upd["id"])
        if not f:
            warnings.append("familyUpdates: unknown family %s" % upd["id"]); continue
        for k in ("husband", "wife", "marriage"):
            if k in upd: f[k] = upd[k]
        for c in upd.get("addChildren", []):
            if c not in f.setdefault("children", []): f["children"].append(c)
    for op in adds.get("setParents", []):
        child = op["child"]
        if child not in people:
            warnings.append("setParents: unknown child %s" % child); continue
        for f in families:
            if child in f.get("children", []): f["children"].remove(child)
        father, mother = op.get("father"), op.get("mother")
        target = None
        for f in families:
            if (f.get("husband") or None) == (father or None) and (f.get("wife") or None) == (mother or None): target = f; break
        if target is None:
            target = {"id": "CF%04d" % (len(families) + 1), "children": []}
            if father: target["husband"] = father
            if mother: target["wife"] = mother
            families.append(target)
        target.setdefault("children", []).append(child)
        if people[child].get("source") != "research":
            people[child].setdefault("corrections", []).append({"what": "parents", "reason": op.get("reason", ""), "previous": op.get("previous")})
    for f in families:
        for key in ("husband", "wife"):
            if f.get(key) and f[key] not in people:
                problems.append("family %s: %s %s is not a person" % (f["id"], key, f[key]))
        for c in f.get("children", []):
            if c not in people:
                problems.append("family %s: child %s is not a person" % (f["id"], c))

    research_count = 0
    for path in sorted(glob.glob("data/research/*.json")):
        pid = os.path.splitext(os.path.basename(path))[0]
        try:
            r = load(path, {})
        except json.JSONDecodeError as e:
            problems.append("%s: invalid JSON (%s)" % (path, e))
            continue
        if pid not in people:
            warnings.append("%s: no person with id %s in tree.json (skipped)" % (path, pid))
            continue
        link = r.get("link") or {}
        if link.get("confidence") and link["confidence"] not in CONFIDENCE:
            problems.append("%s: confidence must be one of %s" % (path, ", ".join(CONFIDENCE)))
        for m in r.get("media", []):
            f = m.get("file")
            if f and not m.get("url") and not os.path.exists(f):
                warnings.append("%s: media file not found: %s" % (path, f))
        if r.get("photo") and not os.path.exists(r["photo"]):
            warnings.append("%s: photo not found: %s" % (path, r["photo"]))
        for k, v in r.items():
            if k != "id":
                people[pid][k] = v
        research_count += 1
    for p in people.values():
        tags = list(p.get("treeTags", [])) + list(p.get("tags", []))
        if tags:
            p["tags"] = sorted(set(tags))

    for s in stories:
        for pid in s.get("people", []):
            if pid not in people:
                warnings.append("story %s: unknown person %s" % (s.get("id"), pid))

    if site.get("rootPerson") and site["rootPerson"] not in people and people:
        warnings.append("site.json rootPerson %s not found; first person will be used" % site["rootPerson"])

    for w in warnings:
        print("warning: " + w, file=sys.stderr)
    for p in problems:
        print("error: " + p, file=sys.stderr)
    if problems:
        sys.exit(1)

    data = dict(site)
    data["sample"] = bool(tree.get("sample"))
    # drop families that end up with nobody in them
    families = [f for f in families if (f.get("husband") or f.get("wife") or f.get("children"))]
    data["people"] = list(people.values())
    data["families"] = families
    data["counts"] = {"gedcom": sum(1 for p in people.values() if p.get("source") != "research"), "research": sum(1 for p in people.values() if p.get("source") == "research")}
    excluded = (load("data/story-exclusions.json", {}) or {}).get("excluded", {})
    data["stories"] = [s for s in stories if s.get("id") not in excluded]
    data["generated"] = __import__("datetime").date.today().isoformat()

    if args.check:
        print("ok: %d people (%d from research), %d families, %d research files, %d stories shown" % (len(people), sum(1 for p in people.values() if p.get("source") == "research"), len(families), research_count, len([s for s in stories if s.get("id") not in (load("data/story-exclusions.json", {}) or {}).get("excluded", {})])))
        return
    with open("data/family.js", "w", encoding="utf-8") as fh:
        fh.write("/* GENERATED by scripts/build.py — do not edit. Edit data/tree.json, data/research/*.json, data/stories.json, data/site.json instead. */\n")
        fh.write("window.FAMILY_DATA = ")
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write(";\n")
    print("Wrote data/family.js: %d people, %d families, %d research files, %d stories shown (%d excluded)" % (len(people), len(families), research_count, len(data["stories"]), len(stories) - len(data["stories"])))


if __name__ == "__main__":
    main()
