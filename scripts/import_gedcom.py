#!/usr/bin/env python3
"""Import a GEDCOM (.ged) file into data/tree.json.

Usage:
    python3 scripts/import_gedcom.py data/source/export.ged
    python3 scripts/import_gedcom.py export.ged -o data/tree.json

Then run  python3 scripts/build.py  to regenerate data/family.js.

Only the core tree (people, families, vital events, residences, notes) is
imported. Research enrichment lives in data/research/<id>.json and is never
touched by this script, so re-importing is safe. Works with GEDCOM 5.5 /
5.5.1 / 7.0 exports from Ancestry, FamilySearch, MyHeritage, Gramps, etc.
"""
import argparse
import json
import re
import sys
from collections import OrderedDict


def read_lines(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    out = []
    pat = re.compile(r"^\s*(\d+)\s+(@[^@]+@\s+)?(\S+)(?:\s(.*))?$")
    for line in text.splitlines():
        if not line.strip():
            continue
        m = pat.match(line)
        if not m:
            continue
        level, xref, tag, value = int(m.group(1)), (m.group(2) or "").strip(), m.group(3), m.group(4) or ""
        if tag == "CONT" and out:
            out[-1][3] += "\n" + value
            continue
        if tag == "CONC" and out:
            out[-1][3] += value
            continue
        out.append([level, xref, tag, value])
    return out


def build_tree(lines):
    root = {"children": []}
    stack = [root]
    for level, xref, tag, value in lines:
        node = {"tag": tag, "xref": xref, "value": value, "children": []}
        while len(stack) > level + 1:
            stack.pop()
        stack[-1]["children"].append(node)
        stack.append(node)
    return root["children"]


def child(node, tag):
    for c in node["children"]:
        if c["tag"] == tag:
            return c
    return None


def children(node, tag):
    return [c for c in node["children"] if c["tag"] == tag]


def event(node, tag):
    ev = child(node, tag)
    if not ev:
        return None
    out = {}
    d, p = child(ev, "DATE"), child(ev, "PLAC")
    if d and d["value"].strip():
        out["date"] = d["value"].strip()
    if p and p["value"].strip():
        out["place"] = p["value"].strip()
    if not out and ev["value"].strip().upper() == "Y":
        return {}
    return out or None


def clean_id(xref):
    return xref.strip("@")


def parse_name(value):
    m = re.match(r"^\s*([^/]*?)\s*/([^/]*)/\s*(.*)$", value)
    if m:
        return m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
    parts = value.strip().split()
    if len(parts) > 1:
        return " ".join(parts[:-1]), parts[-1], ""
    return value.strip(), "", ""


EVENT_TAGS = [
    ("IMMI", "Immigration"), ("EMIG", "Emigration"), ("NATU", "Naturalization"),
    ("CENS", "Census"), ("EDUC", "Education"), ("GRAD", "Graduation"),
    ("MILI", "Military service"), ("_MILT", "Military service"), ("BAPM", "Baptism"),
    ("CHR", "Christening"), ("CONF", "Confirmation"), ("RETI", "Retirement"),
    ("PROB", "Probate"), ("WILL", "Will"), ("EVEN", None),
]


def convert(records):
    people, families, notes = [], [], {}
    for r in records:
        if r["tag"] == "NOTE" and r["xref"]:
            notes[r["xref"]] = r["value"]

    def note_text(node):
        texts = []
        for n in children(node, "NOTE"):
            v = n["value"].strip()
            texts.append(notes.get(v, v) if v.startswith("@") else n["value"])
        return "\n\n".join(t.strip() for t in texts if t.strip())

    for r in records:
        if r["tag"] == "INDI":
            p = OrderedDict(id=clean_id(r["xref"]))
            name = child(r, "NAME")
            given, surname, suffix = parse_name(name["value"]) if name else ("", "", "")
            if name:
                g, s, ns = child(name, "GIVN"), child(name, "SURN"), child(name, "NSFX")
                if g and g["value"].strip(): given = g["value"].strip()
                if s and s["value"].strip(): surname = s["value"].strip()
                if ns and ns["value"].strip(): suffix = ns["value"].strip()
                nick = child(name, "NICK")
                if nick and nick["value"].strip():
                    p["nickname"] = nick["value"].strip()
            p["given"], p["surname"] = given, surname
            if suffix:
                p["suffix"] = suffix
            sex = child(r, "SEX")
            p["sex"] = sex["value"].strip().upper()[:1] if sex and sex["value"].strip() else "U"
            if p["sex"] not in ("M", "F"):
                p["sex"] = "U"
            for tag, key in (("BIRT", "birth"), ("DEAT", "death"), ("BURI", "burial")):
                ev = event(r, tag)
                if ev is not None:
                    p[key] = ev
            occs = [o["value"].strip() for o in children(r, "OCCU") if o["value"].strip()]
            if occs:
                p["occupation"] = "; ".join(OrderedDict.fromkeys(occs))
            residences = []
            for res in children(r, "RESI"):
                d, pl = child(res, "DATE"), child(res, "PLAC")
                item = {}
                if d and d["value"].strip(): item["date"] = d["value"].strip()
                if pl and pl["value"].strip(): item["place"] = pl["value"].strip()
                elif res["value"].strip(): item["place"] = res["value"].strip()
                if item:
                    residences.append(item)
            if residences:
                p["residences"] = residences
            extra = []
            for tag, label in EVENT_TAGS:
                for ev_node in children(r, tag):
                    typ = child(ev_node, "TYPE")
                    ev = {"title": label or (typ["value"].strip() if typ and typ["value"].strip() else "Event")}
                    if label and typ and typ["value"].strip():
                        ev["title"] = typ["value"].strip()
                    d, pl = child(ev_node, "DATE"), child(ev_node, "PLAC")
                    if d and d["value"].strip(): ev["date"] = d["value"].strip()
                    if pl and pl["value"].strip(): ev["place"] = pl["value"].strip()
                    if ev_node["value"].strip() and ev_node["value"].strip().upper() != "Y":
                        ev["description"] = ev_node["value"].strip()
                    if "date" in ev or "place" in ev or "description" in ev:
                        extra.append(ev)
            if extra:
                p["events"] = extra
            note = note_text(r)
            if note:
                p["notes"] = note
            people.append(p)
        elif r["tag"] == "FAM":
            f = OrderedDict(id=clean_id(r["xref"]))
            h, w = child(r, "HUSB"), child(r, "WIFE")
            if h: f["husband"] = clean_id(h["value"])
            if w: f["wife"] = clean_id(w["value"])
            m = event(r, "MARR")
            if m is not None:
                f["marriage"] = m
            d = event(r, "DIV")
            if d is not None:
                f["divorce"] = d
            f["children"] = [clean_id(c["value"]) for c in children(r, "CHIL")]
            families.append(f)
    return people, families


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("gedcom")
    ap.add_argument("-o", "--output", default="data/tree.json")
    args = ap.parse_args()
    people, families = convert(build_tree(read_lines(args.gedcom)))
    data = OrderedDict(_comment="Generated by scripts/import_gedcom.py from %s. Do not hand-edit; put research in data/research/<id>.json." % args.gedcom.split("/")[-1],
                       source=args.gedcom.split("/")[-1], people=people, families=families)
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("Wrote %s: %d people, %d families. Now run: python3 scripts/build.py" % (args.output, len(people), len(families)), file=sys.stderr)


if __name__ == "__main__":
    main()
