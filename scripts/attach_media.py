#!/usr/bin/env python3
"""Attach a file (photo, document, record) or a link to a person.

Copies the file into media/<person-id>/ and records it in
data/research/<person-id>.json (creating that file if needed), then rebuilds.

Examples:
    python3 scripts/attach_media.py I12 ~/Downloads/1900-census.jpg \
        --title "1900 US Census, Rochester NY" --date 1900 --type record \
        --source "FamilySearch" --note "Household of Thomas Hartwell, Lyell Ave"
    python3 scripts/attach_media.py I12 --url https://www.findagrave.com/memorial/123 \
        --title "Find a Grave memorial" --type link
    python3 scripts/attach_media.py I12 portrait.jpg --portrait   # also set as profile photo
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPES = ("photo", "document", "record", "link", "audio", "video", "other")


def slug(s):
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-").lower()
    return s or "file"


def guess_type(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".svg"): return "photo"
    if ext in (".pdf", ".doc", ".docx", ".txt", ".md"): return "document"
    if ext in (".mp3", ".m4a", ".wav"): return "audio"
    if ext in (".mp4", ".mov", ".webm"): return "video"
    return "other"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("person", help="person id, e.g. I12")
    ap.add_argument("file", nargs="?", help="path of the file to attach")
    ap.add_argument("--url", help="attach a link instead of a file")
    ap.add_argument("--title", help="short title shown in the gallery")
    ap.add_argument("--date", default="", help="date of the item, e.g. 1900 or 1900-06-01")
    ap.add_argument("--type", choices=TYPES, help="defaults from the file extension")
    ap.add_argument("--source", default="", help="where it came from (archive, website, relative)")
    ap.add_argument("--note", default="", help="description / transcription")
    ap.add_argument("--people", default="", help="other person ids pictured, comma separated")
    ap.add_argument("--portrait", action="store_true", help="also use this image as the profile photo")
    ap.add_argument("--no-build", action="store_true")
    args = ap.parse_args()
    os.chdir(ROOT)
    if not args.file and not args.url:
        ap.error("give a file path or --url")

    rpath = os.path.join("data", "research", args.person + ".json")
    if os.path.exists(rpath):
        with open(rpath, encoding="utf-8") as fh:
            research = json.load(fh)
    else:
        research = {"id": args.person, "link": {"confidence": "unverified", "note": ""}, "tags": [], "summary": "",
                    "bio": "", "funFacts": [], "residences": [], "military": [], "notable": "", "media": [],
                    "sources": [], "researchLog": []}
    research.setdefault("media", [])

    item = {"type": args.type or ("link" if args.url else guess_type(args.file)), "title": args.title or "", "date": args.date,
            "source": args.source, "note": args.note}
    if args.url:
        item["url"] = args.url
        item["title"] = item["title"] or args.url
    else:
        dest_dir = os.path.join("media", args.person)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, slug(os.path.basename(args.file)))
        if os.path.abspath(args.file) != os.path.abspath(dest):
            shutil.copy2(args.file, dest)
        item["file"] = dest.replace(os.sep, "/")
        item["title"] = item["title"] or os.path.splitext(os.path.basename(args.file))[0].replace("-", " ").replace("_", " ")
        if args.portrait:
            research["photo"] = item["file"]
    if args.people:
        item["people"] = [p.strip() for p in args.people.split(",") if p.strip()]
    research["media"].append(item)
    with open(rpath, "w", encoding="utf-8") as fh:
        json.dump(research, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("Attached %s to %s (%s)" % (item.get("file") or item.get("url"), args.person, rpath))
    if not args.no_build:
        subprocess.check_call([sys.executable, os.path.join("scripts", "build.py")])


if __name__ == "__main__":
    main()
