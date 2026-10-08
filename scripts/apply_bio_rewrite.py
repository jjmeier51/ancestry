#!/usr/bin/env python3
"""Apply rewritten About texts to the research files.

Input: a directory of JSON files, each {"<id>": {"summary": "...", "bio": "..."}}.
For every person: the previous `bio` (the research-note style text) is moved to
`researchNotes` (shown on the profile under Research status as "Evidence
notes"), and `bio` / `summary` are replaced by the rewritten prose. A rewrite
is rejected (and reported) when it is empty, still contains record identifiers
or research-process phrases, or is wildly short compared with the original.

Usage: python3 scripts/apply_bio_rewrite.py <dir> [--dry]
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
BAD = re.compile(r"FamilySearch|WikiTree|\bFS\b|ark:|\bED\s?\d|sheet \d|\bRound \d|\[R4-|\(S\d+\)|docket|\bfile (no\.?|number)? ?\d|https?://|"
                 r"\bGEDCOM\b|the tree\b|the site\b|the roster|\bworker|snippet|not (yet )?(searched|researched|found)|unsourced|"
                 r"\bGeni\b", re.I)
IDS = re.compile(r"\b[A-Z0-9]{4}-[A-Z0-9]{3}\b|\b[A-Z][a-z]+-\d{2,6}\b")  # FamilySearch / WikiTree style ids (case-sensitive)


def check(pid, old, new):
    problems = []
    bio, summ = (new.get("bio") or "").strip(), (new.get("summary") or "").strip()
    if not bio:
        problems.append("empty bio")
    if not summ:
        problems.append("empty summary")
    if len(summ) > 260:
        problems.append("summary too long")
    for label, txt in (("bio", bio), ("summary", summ)):
        m = BAD.search(txt) or IDS.search(txt)
        if m:
            problems.append(f"{label} still has '{m.group(0)}'")
        if re.search(r"^\s*[-*#]|\*\*", txt, re.M):
            problems.append(f"{label} has markdown")
    if old and len(bio) < min(120, len(old) * 0.25):
        problems.append(f"bio very short ({len(bio)} vs {len(old)})")
    return problems


def main():
    src = sys.argv[1]
    dry = "--dry" in sys.argv
    keep_notes = "--keep-notes" in sys.argv   # the old bio is already prose: do not copy it into researchNotes
    allow = set()
    for i, a in enumerate(sys.argv):
        if a == "--allow": allow = set(sys.argv[i + 1].split(","))
    rewrites = {}
    for f in sorted(x for x in glob.glob(os.path.join(src, "*.json")) if not os.path.basename(x).startswith("_")):
        try:
            rewrites.update(json.load(open(f, encoding="utf-8")))
        except Exception as e:  # noqa
            print("bad file", f, e)
    applied, rejected = 0, []
    for pid, new in rewrites.items():
        path = f"data/research/{pid}.json"
        if not os.path.exists(path):
            rejected.append((pid, ["no research file"])); continue
        r = json.load(open(path, encoding="utf-8"))
        old = r.get("bio") or ""
        probs = [] if pid in allow else check(pid, old, new)
        if probs:
            rejected.append((pid, probs)); continue
        if dry:
            applied += 1; continue
        if old and old != new["bio"].strip() and not keep_notes:
            notes = r.get("researchNotes") or ""
            if old not in notes:
                r["researchNotes"] = (notes + "\n\n" if notes else "") + old
        r["bio"] = new["bio"].strip()
        r["summary"] = new["summary"].strip()
        r.setdefault("researchLog", []).append({"date": "2026-10-08", "note": "About text rewritten as narrative; the earlier research-note text is kept under Evidence notes."})
        json.dump(r, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False); open(path, "a").write("\n")
        applied += 1
    print(f"{'would apply' if dry else 'applied'} {applied}; rejected {len(rejected)}")
    for pid, probs in rejected:
        print(" ", pid, "; ".join(probs))
    json.dump([p for p, _ in rejected], open(os.path.join(src, "_rejected.json"), "w"))


if __name__ == "__main__":
    main()
