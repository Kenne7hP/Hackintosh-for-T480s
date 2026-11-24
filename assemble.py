"""Assemble the pinned EFI tree into a new directory using Python 3.9+."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import urllib.request
import zipfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def assemble(destination, cache):
    source = Path(__file__).resolve().parent
    manifest = json.loads((source / "assets.json").read_text(encoding="utf-8"))
    if destination.exists():
        raise FileExistsError(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as temp:
        tree = Path(temp) / "build"
        shutil.copytree(source / "EFI", tree / "EFI")
        for name, asset in manifest.items():
            archive = cache / name if cache else Path(temp) / name
            if not cache:
                urllib.request.urlretrieve(asset["url"], archive)
            if digest(archive.read_bytes()) != asset["sha256"]:
                raise ValueError(f"Asset checksum mismatch for {name}")
            with archive.open("rb") as stream:
                bundle = zipfile.ZipFile(stream) if name.endswith(".zip") else None
                try:
                    for path, (member, checksum) in asset["files"].items():
                        data = bundle.read(member) if bundle else stream.read()
                        if digest(data) != checksum:
                            raise ValueError(f"Member checksum mismatch for {path}")
                        target = tree / path
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(data)
                finally:
                    if bundle:
                        bundle.close()
        tree.rename(destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--cache", type=Path, help="Read all pinned assets from this directory offline")
    args = parser.parse_args()
    assemble(args.destination, args.cache)
