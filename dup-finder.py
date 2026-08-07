#!/usr/bin/env python3
"""Find duplicate files efficiently.

Strategy (avoid hashing every file):
  1. Walk the tree, group files by SIZE (cheap stat, no file read).
  2. Only files whose size matches another file can be duplicates -- hash
     just those, and group by SHA-256.

On typical trees this reads only the files that collide on size, instead of
hashing every file.
"""
import argparse
import hashlib
import os
import sys

_CHUNK = 65536


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(_CHUNK), b""):
            h.update(blk)
    return h.hexdigest()


def find_duplicates(root):
    by_size = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            try:
                size = os.path.getsize(p)
            except OSError:
                continue
            by_size.setdefault(size, []).append(p)

    dupes = {}
    for size, paths in by_size.items():
        if len(paths) < 2:
            continue  # unique size -> cannot be a duplicate
        by_digest = {}
        for p in paths:
            by_digest.setdefault(sha256_file(p), []).append(p)
        for digest, ps in by_digest.items():
            if len(ps) > 1:
                dupes[digest] = ps
    return dupes


def main():
    ap = argparse.ArgumentParser(description="Find duplicate files")
    ap.add_argument("directory")
    args = ap.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a directory", file=sys.stderr)
        sys.exit(1)

    dupes = find_duplicates(args.directory)
    if not dupes:
        print("No duplicate files found")
        return
    print("Duplicate files found:")
    for digest in sorted(dupes):
        print(f"  {digest}:")
        for p in dupes[digest]:
            print(f"    {p}")


if __name__ == "__main__":
    main()