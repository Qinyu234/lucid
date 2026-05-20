import json

from call_ollama import call_ollama
from clean_tasks import clean_tasks
from safe_parse import safe_parse   

def decompose_task(task: dict, llm=None) -> list[dict]:
    if llm is None:
        llm = call_ollama

    prompt = f"""
你是代码结构优化器。

对以下 task 进行重构（不能改变 semantic 语义，只能优化结构）：

{json.dumps(task, ensure_ascii=False)}

输出必须严格符合 JSON 数组，每个元素包含：
- file_name
- semantic（必须与输入一致）
- imports
- functions
"""

    raw = llm(prompt)
    tasks = clean_tasks(safe_parse(raw))

    # 🔥 强制 schema lock（关键）
    for t in tasks:
        t["semantic"] = task.get("semantic", t.get("file_name", ""))
        t.setdefault("imports", [])
        t.setdefault("functions", [])

    return tasks