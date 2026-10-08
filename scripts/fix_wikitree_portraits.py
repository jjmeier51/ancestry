#!/usr/bin/env python3
"""For WikiTree-matched people who have WikiTree images attached but no portrait,
ask WikiTree (getPerson, field Photo) for the profile's primary photo and make the
matching attached image the person's portrait."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import find_wikitree as fw

report = json.load(open(fw.REPORT))
fixed = 0
for pid, r in report.items():
    if r.get("status") != "matched" or not r.get("photos"):
        continue
    f = os.path.join(ROOT, "data", "research", f"{pid}.json")
    d = json.load(open(f))
    if d.get("photo"):
        continue
    j = fw.api({"action": "getPerson", "key": r["key"], "fields": "Id,Name,Photo"})
    photo = (((j or {}).get("person") or {}).get("Photo") or "")
    if not photo:
        continue
    want = re.sub(r"[^a-z0-9.]+", "-", photo.lower()).strip("-")
    for m in d.get("media", []):
        if m.get("file") and os.path.basename(m["file"]).endswith(want):
            d["photo"] = m["file"]
            m["type"] = "photo"
            json.dump(d, open(f, "w"), indent=2, ensure_ascii=False); open(f, "a").write("\n")
            r["portrait"] = m["file"]
            fixed += 1
            print(pid, r["key"], "->", m["file"])
            break
json.dump(report, open(fw.REPORT, "w"), indent=1, ensure_ascii=False)
print("portraits set:", fixed)
