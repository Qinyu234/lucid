# =========================
# FUNCTION:
# call_llm
#
# PURPOSE:
# unified LLM interface (Ollama)
# =========================


import requests
import json


URL = "http://localhost:11434/api/generate" #Ollama
MODEL = "qwen2.5-coder"


def call_llm(prompt: str):

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "")

    except Exception as e:

        return ""