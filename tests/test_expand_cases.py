import json
from pathlib import Path


def test_expand_cases_match_middle_schema():
    from src.shared.validate.expand_output_util import expand_output_util

    path = Path("io/input/test_cases/expand_cases.json")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    cases = data.get("cases") or []
    assert cases, "no cases found"
    for case in cases:
        cid = case.get("id") or "unknown"
        payload = case.get("output")
        assert isinstance(payload, dict), f"{cid}: output must be object"
        vr = expand_output_util(payload)
        assert vr.ok, f"{cid}: schema invalid: {vr.errors}"

