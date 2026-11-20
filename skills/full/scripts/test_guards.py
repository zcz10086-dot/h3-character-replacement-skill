"""Offline invariants for workflow and project guards; no network or model files."""
import copy
import json
from pathlib import Path
import tempfile
from workflow_guard import compare
from project_check import validate


def main():
    results = []
    a = {"1": {"class_type": "OfficialNode", "inputs": {"text": "original", "window": 90, "video": ["2", 0]}}}
    b = copy.deepcopy(a)
    b["1"]["inputs"]["text"] = "new prompt"
    assert compare(a, b, {"1.text"})["approved"]
    results.append("approved string edit accepted")
    assert not compare(a, b, set())["approved"]
    results.append("unapproved string edit rejected")
    for field, value in (("window", 89), ("window", 90.0), ("video", ["3", 0])):
        b = copy.deepcopy(a)
        b["1"]["inputs"][field] = value
        assert not compare(a, b, {"1." + field})["approved"]
    results.append("number type/value and edge edits rejected")
    b = copy.deepcopy(a)
    b["3"] = copy.deepcopy(a["1"])
    assert not compare(a, b, set())["approved"]
    results.append("node addition rejected")
    with tempfile.TemporaryDirectory(prefix="h3-guard-test-") as d:
        media = Path(d) / "fixture.bin"
        media.write_bytes(b"fixture, not actual video")
        cfg = {"reference_binding": [{"picture": 1, "identity": "P1", "path": str(media)}],
               "source": str(media), "clean_source": str(media), "timing": {"source_frames": 10},
               "shots": [{"id": "s", "start": 0, "end": 10, "roles": ["P1"]}],
               "preprocessing": {"burned_subtitles": {"reviewed": True}, "watermarks": {"reviewed": True}},
               "workflow": {"window_frames": 90, "ref_image_size": "match"}}
        assert validate(cfg)["valid"]
        results.append("project frame coverage accepted; file existence only, not media decode")
        bad = copy.deepcopy(cfg)
        bad["shots"][0]["start"] = 1
        assert not validate(bad)["valid"]
        bad = copy.deepcopy(cfg)
        bad["shots"][0]["preserve_original"] = True
        assert not validate(bad)["valid"]
        results.append("frame gap and unexplained original preservation rejected")
    print(json.dumps({"passed": True, "tests": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
