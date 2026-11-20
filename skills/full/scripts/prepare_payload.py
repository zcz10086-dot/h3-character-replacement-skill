"""Instantiate a user-supplied approved API template using explicit string replacements."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from workflow_guard import compare, load


def prepare(template, replacements):
    candidate = copy.deepcopy(template)
    prompt = candidate.get("prompt", candidate)
    allowed = set()
    for key, value in replacements.items():
        node, field = key.split(".", 1)
        if node not in prompt or field not in prompt[node].get("inputs", {}):
            raise ValueError("unknown input: " + key)
        if not isinstance(prompt[node]["inputs"][field], str) or not isinstance(value, str):
            raise ValueError("only existing string inputs may be replaced: " + key)
        prompt[node]["inputs"][field] = value
        allowed.add(key)
    result = compare(template, candidate, allowed)
    if not result["approved"]:
        raise ValueError("template invariants failed")
    return candidate, result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--template", required=True)
    p.add_argument("--replacements", required=True, help="JSON object keyed by node.input")
    p.add_argument("--output", required=True)
    p.add_argument("--report", required=True)
    a = p.parse_args()
    target, report = Path(a.output), Path(a.report)
    if target.resolve() == report.resolve() or target.exists() or report.exists():
        raise FileExistsError("outputs must be new distinct files")
    candidate, diff = prepare(load(a.template), load(a.replacements))
    diff["template_sha256"] = hashlib.sha256(Path(a.template).read_bytes()).hexdigest()
    diff["allowed_string_inputs"] = sorted(load(a.replacements))
    for path, data in ((target, candidate), (report, diff)):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
    print(json.dumps(diff, ensure_ascii=False))


if __name__ == "__main__":
    main()
