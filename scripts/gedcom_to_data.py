#!/usr/bin/env python3
"""Convert a GEDCOM (.ged) export into data/family.js for this website.

Usage:
    python3 scripts/gedcom_to_data.py path/to/export.ged -o data/family.js
    python3 scripts/gedcom_to_data.py export.ged --title "The Smith Family" --root @I1@

Works with exports from Ancestry, FamilySearch, MyHeritage, Gramps, RootsMagic
and most other genealogy programs (GEDCOM 5.5 / 5.5.1 / 7.0). Only the
standard library is used.
"""
import argparse
import json
import re
import sys
from collections import OrderedDict


def read_lines(path):
    """Yield (level, xref, tag, value) tuples; handles CONT/CONC continuation."""
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
    """Turn flat lines into nested records: [{tag, xref, value, children:[...]}]."""
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
    if d and d["value"]:
        out["date"] = d["value"].strip()
    if p and p["value"]:
        out["place"] = p["value"].strip()
    if not out and ev["value"].strip().upper() == "Y":
        return {}
    return out or None


def clean_id(xref):
    return xref.strip("@")


def parse_name(value):
    """'John Henry /Smith/ Jr.' -> given, surname, suffix"""
    m = re.match(r"^\s*([^/]*?)\s*/([^/]*)/\s*(.*)$", value)
    if m:
        return m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
    parts = value.strip().split()
    if len(parts) > 1:
        return " ".join(parts[:-1]), parts[-1], ""
    return value.strip(), "", ""


def convert(records, title=None, root=None):
    people, families, notes = [], [], {}
    for r in records:
        if r["tag"] == "NOTE" and r["xref"]:
            notes[r["xref"]] = r["value"]

    def note_text(node):
        texts = []
        for n in children(node, "NOTE"):
            texts.append(notes.get(n["value"].strip(), n["value"]) if n["value"].strip().startswith("@") else n["value"])
        return "\n\n".join(t.strip() for t in texts if t.strip())

    for r in records:
        if r["tag"] == "INDI":
            p = OrderedDict(id=clean_id(r["xref"]))
            name = child(r, "NAME")
            given, surname, suffix = parse_name(name["value"]) if name else ("", "", "")
            if name:
                g, s, ns = child(name, "GIVN"), child(name, "SURN"), child(name, "NSFX")
                if g and g["value"]: given = g["value"].strip()
                if s and s["value"]: surname = s["value"].strip()
                if ns and ns["value"]: suffix = ns["value"].strip()
                nick = child(name, "NICK")
                if nick and nick["value"]:
                    p["nickname"] = nick["value"].strip()
            p["given"], p["surname"] = given, surname
            if suffix:
                p["suffix"] = suffix
            sex = child(r, "SEX")
            p["sex"] = (sex["value"].strip().upper()[:1] if sex and sex["value"].strip() else "U")
            if p["sex"] not in ("M", "F"):
                p["sex"] = "U"
            for tag, key in (("BIRT", "birth"), ("DEAT", "death"), ("BURI", "burial")):
                ev = event(r, tag)
                if ev is not None:
                    p[key] = ev
            occ = child(r, "OCCU")
            if occ and occ["value"].strip():
                p["occupation"] = occ["value"].strip()
            extra = []
            for tag, label in (("RESI", "Residence"), ("IMMI", "Immigration"), ("EMIG", "Emigration"),
                               ("NATU", "Naturalization"), ("CENS", "Census"), ("EDUC", "Education"),
                               ("GRAD", "Graduation"), ("MILI", "Military service"), ("BAPM", "Baptism"),
                               ("CHR", "Christening"), ("EVEN", None)):
                for ev_node in children(r, tag):
                    ev = {"type": "event", "title": label or (child(ev_node, "TYPE") or {"value": "Event"})["value"] or "Event"}
                    d, pl = child(ev_node, "DATE"), child(ev_node, "PLAC")
                    if d and d["value"]: ev["date"] = d["value"].strip()
                    if pl and pl["value"]: ev["place"] = pl["value"].strip()
                    if ev_node["value"].strip() and ev_node["value"].strip().upper() != "Y":
                        ev["description"] = ev_node["value"].strip()
                    if "date" in ev or "place" in ev:
                        extra.append(ev)
            if extra:
                p["events"] = extra
            bio = note_text(r)
            if bio:
                p["bio"] = bio
            obje = child(r, "OBJE")
            if obje:
                f = child(obje, "FILE")
                if f and f["value"] and re.search(r"\.(jpe?g|png|gif|webp)$", f["value"], re.I):
                    p["photo"] = "images/" + f["value"].replace("\\", "/").split("/")[-1]
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

    head = next((r for r in records if r["tag"] == "HEAD"), None)
    if not title:
        surnames = {}
        for p in people:
            if p["surname"]:
                surnames[p["surname"]] = surnames.get(p["surname"], 0) + 1
        top = max(surnames, key=surnames.get) if surnames else "Our"
        title = "The %s Family" % top
    data = OrderedDict(title=title, subtitle="", rootPerson=clean_id(root) if root else (people[0]["id"] if people else ""),
                       people=people, families=families, stories=[], photos=[])
    return data


HEADER = """/*
 * Family data file — generated from a GEDCOM export by scripts/gedcom_to_data.py.
 * You can edit this file by hand: add "bio", "photo", "stories" and "photos".
 * Re-running the script will overwrite it, so keep hand edits in a copy or in
 * your genealogy program's notes.
 */
window.FAMILY_DATA = """


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("gedcom", help="path to the .ged file")
    ap.add_argument("-o", "--output", default="data/family.js", help="output file (default data/family.js)")
    ap.add_argument("--title", help="site title, e.g. 'The Smith Family'")
    ap.add_argument("--root", help="GEDCOM id of the home person, e.g. @I1@ or I1")
    args = ap.parse_args()

    records = build_tree(read_lines(args.gedcom))
    data = convert(records, title=args.title, root=args.root)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(HEADER)
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write(";\n")
    print("Wrote %s: %d people, %d families" % (args.output, len(data["people"]), len(data["families"])), file=sys.stderr)


if __name__ == "__main__":
    main()
