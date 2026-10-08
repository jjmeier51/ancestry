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
    j = fw.api({"action": "getPerson", "key": r["key"], "fields": "Id,Name,Photo,PhotoData"})
    person = ((j or {}).get("person") or {})
    photo = person.get("Photo") or ""
    if not photo:
        continue
    want = re.sub(r"[^a-z0-9.]+", "-", photo.lower()).strip("-")
    hit = None
    for m in d.get("media", []):
        if m.get("file") and os.path.basename(m["file"]).endswith(want):
            hit = m
            break
    if hit:
        d["photo"] = hit["file"]
        hit["type"] = "photo"
        json.dump(d, open(f, "w"), indent=2, ensure_ascii=False); open(f, "a").write("\n")
        r["portrait"] = hit["file"]
        fixed += 1
        print(pid, r["key"], "->", hit["file"])
        continue
    # primary photo not among the attached images: fetch it
    path = (person.get("PhotoData") or {}).get("path")
    if not path:
        continue
    data = fw.get("https://www.wikitree.com" + path)
    if not data or len(data) < 1000 or len(data) > 6_000_000:
        continue
    os.makedirs(fw.TMP, exist_ok=True)
    fn = os.path.join(fw.TMP, f"{pid}-{want}")
    open(fn, "wb").write(data)
    import subprocess
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "attach_media.py"), "--no-build", pid, fn,
                    "--title", f"{r.get('wt_name') or r['key']} (WikiTree profile photo)", "--type", "photo",
                    "--source", f"WikiTree, profile {r['key']}; https://www.wikitree.com/photo/jpg/{os.path.splitext(photo)[0]}",
                    "--portrait"], check=False)
    r["portrait"] = f"media/{pid}/{pid.lower()}-{want}"
    fixed += 1
    print(pid, r["key"], "-> downloaded", photo)
json.dump(report, open(fw.REPORT, "w"), indent=1, ensure_ascii=False)
print("portraits set:", fixed)
