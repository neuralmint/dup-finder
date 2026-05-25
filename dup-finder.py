#!/usr/bin/env python3
import os
import argparse
import hashlib

def calculate_checksum(filename):
    """Calculates the SHA-256 checksum of a file"""
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def find_duplicates(directory):
    """Finds duplicate files in a directory and its subdirectories"""
    files = {}
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            checksum = calculate_checksum(filepath)
            if checksum in files:
                files[checksum].append(filepath)
            else:
                files[checksum] = [filepath]
    return {checksum: paths for checksum, paths in files.items() if len(paths) > 1}

def main():
    parser = argparse.ArgumentParser(description="Finds duplicate files in a directory and its subdirectories")
    parser.add_argument("directory", help="The directory to search for duplicates")
    args = parser.parse_args()
    duplicates = find_duplicates(args.directory)
    if duplicates:
        print("Duplicate files found:")
        for checksum, paths in duplicates.items():
            print(f"  {checksum}:")
            for path in paths:
                print(f"    {path}")
    else:
        print("No duplicate files found")

if __name__ == "__main__":
    main()

# Donations:
#   BTC: bc1q6ud0w3036ye2vfzkftwywarqswqu3jehs4nqe7
#   ETH: 0x643E158D7615d19F1f0105B0cc5a1D976B456e4A
