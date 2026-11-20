"""Compare approved API payloads without changing official workflow topology."""
import argparse
import hashlib
import json
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def compare(reference, candidate, allowed):
    a, b = reference.get("prompt", reference), candidate.get("prompt", candidate)
    problems, edits = [], []
    if set(a) != set(b):
        problems.append("node set changed")
    for node in sorted(set(a) & set(b)):
        if a[node].get("class_type") != b[node].get("class_type"):
            problems.append(f"{node}: class_type changed")
        ai, bi = a[node].get("inputs", {}), b[node].get("inputs", {})
        if set(ai) != set(bi):
            problems.append(f"{node}: input field set changed")
        for field in sorted(set(ai) & set(bi)):
            old, new = ai[field], bi[field]
            if type(old) is type(new) and old == new:
                continue
            key = f"{node}.{field}"
            edits.append(key)
            if key not in allowed or not isinstance(old, str) or not isinstance(new, str):
                problems.append(f"{key}: unapproved or non-string input change")
    return {"approved": not problems, "changed_fields": edits, "problems": problems}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("reference")
    p.add_argument("candidate")
    p.add_argument("--allow", action="append", default=[], help="Exact node.input string whitelist; repeat")
    p.add_argument("--report", required=True)
    p.add_argument("--canvas")
    p.add_argument("--canvas-sha256")
    args = p.parse_args()
    result = compare(load(args.reference), load(args.candidate), set(args.allow))
    if args.canvas or args.canvas_sha256:
        if not (args.canvas and args.canvas_sha256):
            p.error("--canvas and --canvas-sha256 must be supplied together")
        actual = hashlib.sha256(Path(args.canvas).read_bytes()).hexdigest()
        result["canvas_sha256"] = actual
        if actual.lower() != args.canvas_sha256.lower():
            result["approved"] = False
            result["problems"].append("official canvas SHA256 mismatch")
    target = Path(args.report)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["approved"] else 2)


if __name__ == "__main__":
    main()
