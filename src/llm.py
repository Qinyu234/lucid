# FUNCTION:
# wrapper around Ollama Qwen Coder

import requests

MODEL="qwen2.5-coder:7b"

SYSTEM="""
You are generating code for a growing project.

Rules:

Expand existing project only.

Keep architecture consistent.

Output CODE ONLY.

No markdown.

Do not explain.
"""

def generate(context):

    r=requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model":MODEL,
            "system":SYSTEM,
            "prompt":context,
            "stream":False,
            "options":{
                "temperature":0.2,
                "top_p":0.9
            }
        }
    )

    return r.json()["response"]