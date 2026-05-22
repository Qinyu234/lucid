import json
from .build_prompt import build_prompt
from .call_llm import call_llm


def expand(node, max_retry=2):

    # =========================
    # retry loop
    # =========================

    for _ in range(max_retry):

        result = call_llm(build_prompt(node))

        # =========================
        # parse
        # =========================

        try:
            data = json.loads(result)
        except:
            continue

        # =========================
        # schema validation (strict IPO)
        # =========================

        if not isinstance(data, dict):
            continue

        if not all(k in data for k in ["input", "process", "output"]):
            continue

        if not isinstance(data["input"], list):
            continue
        if not isinstance(data["process"], list):
            continue
        if not isinstance(data["output"], list):
            continue

        # =========================
        # clean normalization
        # =========================

        return {
            "input": [str(x) for x in data["input"]],
            "process": [str(x) for x in data["process"]],
            "output": [str(x) for x in data["output"]],
        }

    # =========================
    # fallback
    # =========================

    return {
        "input": [],
        "process": [],
        "output": []
    }