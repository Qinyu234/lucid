from call_ollama import call_ollama
from clean_tasks import clean_tasks
from safe_parse import safe_parse

def decompose_idea(idea: dict) -> list[dict]:
    prompt = f"""
拆解 Python 文件结构：

需求：{idea.get("goal","")}

只输出 JSON 数组：
- file_name
- functions
- imports
"""

    raw = call_ollama(prompt)
    tasks = clean_tasks(safe_parse(raw))

    for t in tasks:
        t.setdefault("semantic", t["file_name"])
        t.setdefault("file_path", t["file_name"].replace(".py", ""))

    return tasks