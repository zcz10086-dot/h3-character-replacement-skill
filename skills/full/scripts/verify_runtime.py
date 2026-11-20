"""Verify bundled runtime materials without installing or importing plugin code."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath


def digest(data):
    return hashlib.sha256(data).hexdigest()


def audit_archive(path):
    entries = {}
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError("CRC failure: " + bad)
        for item in archive.infolist():
            name = item.filename.replace("\\", "/")
            pure = PurePosixPath(name)
            if pure.is_absolute() or ".." in pure.parts or ":" in name or ((item.external_attr >> 16) & 0o170000) == 0o120000:
                raise ValueError("unsafe archive member: " + name)
            if not item.is_dir():
                if name in entries:
                    raise ValueError("duplicate member: " + name)
                entries[name] = {"size": item.file_size, "sha256": digest(archive.read(item))}
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1] / "assets" / "runtime"))
    args = parser.parse_args()
    root = Path(args.root)
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8-sig"))
    # The manifest is an inventory; do not trust existence alone.
    checks = []
    actual_files = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p != root / "manifest.json"}
    if actual_files != set(manifest["files"]):
        raise ValueError("inventory omits files or references missing files")
    for rel, expected in manifest["files"].items():
        path = root / rel
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("inventory path escapes root")
        data = path.read_bytes()
        if digest(data) != expected["sha256"] or len(data) != expected["size"]:
            raise ValueError("file differs: " + rel)
        checks.append(rel)
    for rel, expected in manifest["archives"].items():
        actual = audit_archive(root / rel)
        if actual != expected["members"]:
            raise ValueError("archive inventory differs: " + rel)
    for stage, count, output in ((1, 77, "1349"), (2, 62, "1247")):
        data = json.loads((root / "workflows" / ("stage%d.api.json" % stage)).read_text(encoding="utf-8"))
        graph = data.get("prompt", data)
        if len(graph) != count or graph[output]["class_type"] != "SaveVideo":
            raise ValueError("API template structure differs")
    mask = json.loads((root / "workflows" / "mask.api.json").read_text(encoding="utf-8"))
    mask_graph = mask.get("prompt", mask)
    if len(mask_graph) != 7 or mask_graph["19"]["class_type"] != "SAM3_VideoTrack":
        raise ValueError("mask template differs")
    with zipfile.ZipFile(root / "plugins-production.zip") as archive:
        plugins = {name.split("/")[0] for name in archive.namelist() if "/" in name}
        if len(plugins) != 20:
            raise ValueError("expected 20 complete plugin directories")
        actual = archive.read("ComfyUI-H3-Conditioning-Cache/h3_conditioning_cache.py")
        expected = (root / "overrides" / "h3_conditioning_cache.py").read_bytes()
        if actual != expected or digest(actual) != "763c6a6b4da82e4f7c6aa70426b1c6845860e870ad0569091c9e5668807d2d4a":
            raise ValueError("conditioning override differs")
    print(json.dumps({"status": "passed", "verified_files": checks, "archives_verified": len(manifest["archives"]), "api_nodes": [77, 62], "plugin_execution": "not performed"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
