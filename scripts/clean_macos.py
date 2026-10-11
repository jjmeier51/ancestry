#!/usr/bin/env python3
"""Delete macOS junk files: AppleDouble `._*` files and `.DS_Store`.

Usage:
    python3 scripts/clean_macos.py [--dry-run] [PATH ...]

With no PATH the repository root (the parent of `scripts/`) is cleaned.
The `.git` directory is never touched.
"""
import argparse
import os
import sys

JUNK_NAMES = {".DS_Store", ".AppleDouble", ".Spotlight-V100", ".Trashes", ".fseventsd"}
SKIP_DIRS = {".git"}


def is_junk(name: str) -> bool:
    return name.startswith("._") or name in JUNK_NAMES


def clean(root: str, dry_run: bool) -> int:
    removed = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if is_junk(name):
                path = os.path.join(dirpath, name)
                print(("would delete " if dry_run else "deleted ") + path)
                if not dry_run:
                    try:
                        os.remove(path)
                    except OSError as e:
                        print(f"  failed: {e}", file=sys.stderr)
                        continue
                removed += 1
        # junk directories (e.g. .AppleDouble, .Trashes) are removed whole
        for d in list(dirnames):
            if d in JUNK_NAMES:
                path = os.path.join(dirpath, d)
                print(("would delete " if dry_run else "deleted ") + path + "/")
                if not dry_run:
                    import shutil
                    shutil.rmtree(path, ignore_errors=True)
                dirnames.remove(d)
                removed += 1
    return removed


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="*", help="directories to clean (default: repo root)")
    ap.add_argument("--dry-run", "-n", action="store_true", help="list without deleting")
    args = ap.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = args.paths or [repo_root]
    total = sum(clean(p, args.dry_run) for p in paths)
    print(f"{'would remove' if args.dry_run else 'removed'} {total} item(s)")


if __name__ == "__main__":
    main()
