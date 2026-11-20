"""Validate project frame coverage, reference identity and reviewed preprocessing."""
import argparse
import json
from pathlib import Path


def validate(c):
    errors = []
    binding = c.get("reference_binding", [])
    indexes = [x.get("picture") for x in binding]
    if not binding or indexes != list(range(1, len(binding) + 1)):
        errors.append("Picture indexes must be ordered, unique and 1-based")
    ids = [x.get("identity") for x in binding]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        errors.append("reference identities must be nonempty and unique")
    for entry in binding:
        path = entry.get("path", "")
        if not path or not Path(path).is_file():
            errors.append(f"reference file missing: Picture {entry.get('picture')}")
    shots = c.get("shots", [])
    if not shots:
        errors.append("no reviewed shots")
    cursor = 0
    names = set()
    for shot in shots:
        sid = shot.get("id")
        if not sid or sid in names:
            errors.append("shot id missing or duplicated")
        names.add(sid)
        start, end = shot.get("start"), shot.get("end")
        if type(start) is not int or type(end) is not int or start != cursor or end <= start:
            errors.append(f"invalid half-open contiguous range: {sid}")
        else:
            cursor = end
        if shot.get("preserve_original") and not shot.get("preserve_reason"):
            errors.append(f"original preservation requires explicit reviewed reason: {sid}")
        for role in shot.get("roles", []):
            if role not in ids:
                errors.append(f"unknown identity in {sid}: {role}")
    if cursor != c.get("timing", {}).get("source_frames"):
        errors.append("shot coverage != actual source_frames")
    for name in ("source", "clean_source"):
        if not Path(c.get(name) or "__missing__").is_file():
            errors.append(f"{name} file missing")
    prep = c.get("preprocessing", {})
    for name in ("burned_subtitles", "watermarks"):
        cfg = prep.get(name, {})
        if not cfg.get("reviewed"):
            errors.append(f"{name} policy has not been reviewed")
    wf = c.get("workflow", {})
    if wf.get("window_frames") != 90 or wf.get("ref_image_size") != "match":
        errors.append("official default 90/match invariants changed; review explicit authorization")
    return {"valid": not errors, "errors": errors, "covered_frames": cursor}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("config")
    p.add_argument("--report")
    a = p.parse_args()
    result = validate(json.loads(Path(a.config).read_text(encoding="utf-8-sig")))
    if a.report:
        out = Path(a.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["valid"] else 2)


if __name__ == "__main__":
    main()
