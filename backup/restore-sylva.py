"""Restore and verify the Sylva 3D snapshot from its downloaded release assets."""

import argparse
import gzip
import hashlib
import json
import shutil
import zipfile
from collections import defaultdict
from pathlib import Path, PurePosixPath


INVENTORY = "sylva-file-inventory.json.gz"


def file_hash(path):
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def local_path(root, name):
    relative = PurePosixPath(name)
    if relative.is_absolute() or '..' in relative.parts or ':' in name or '\\' in name:
        raise ValueError(f"Invalid archive path: {name}")
    return root.joinpath(*relative.parts)


def restore(downloads, destination):
    with gzip.open(downloads / INVENTORY, "rt", encoding="utf-8") as file:
        inventory = json.load(file)
    if destination.exists() and any(destination.iterdir()):
        raise ValueError(f"Choose an empty restore directory: {destination}")
    if downloads == destination or downloads.is_relative_to(destination):
        raise ValueError("Keep downloads outside the restore directory")

    entries = defaultdict(list)
    for name, record in inventory["files"].items():
        entries[record["archive"]].append((name, record))

    for archive in inventory["archives"]:
        path = local_path(downloads, archive["name"])
        if path.stat().st_size != archive["size"] or file_hash(path) != archive["sha256"]:
            raise ValueError(f"Damaged download: {path.name}")

    count = 0
    for archive in inventory["archives"]:
        name = archive["name"]
        files = entries[name]
        with zipfile.ZipFile(downloads / name) as package:
            for relative, record in files:
                if relative != record["member"]:
                    continue
                path = local_path(destination, relative)
                path.parent.mkdir(parents=True, exist_ok=True)
                with package.open(relative) as source, path.open("xb") as target:
                    shutil.copyfileobj(source, target, length=1024 * 1024)
            for relative, record in files:
                path = local_path(destination, relative)
                if relative != record["member"]:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(local_path(destination, record["member"]), path)
                if path.stat().st_size != record["size"] or file_hash(path) != record["sha256"]:
                    raise ValueError(f"Restored file failed verification: {relative}")
                count += 1
        print(f"Restored and verified {name}", flush=True)
    print(f"Verified {count:,} files in {destination}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("downloads", type=Path, help="Directory with the ZIPs and inventory")
    parser.add_argument("destination", type=Path, help="Empty directory to restore into")
    args = parser.parse_args()
    restore(args.downloads.resolve(), args.destination.resolve())


if __name__ == "__main__":
    main()
