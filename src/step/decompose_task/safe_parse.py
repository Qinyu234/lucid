import json
import re

def safe_parse(text: str):
    # 1. 直接解析
    try:
        return json.loads(text)
    except Exception:
        pass

    # 2. 提取 JSON block（从第一个 { 或 [ 开始截取）
    start_candidates = [text.find("{"), text.find("[")]
    start_candidates = [i for i in start_candidates if i != -1]

    if not start_candidates:
        raise ValueError("No JSON found in LLM output")

    start = min(start_candidates)
    sliced = text[start:]

    # 3. 尝试截断到“最可能闭合结构”
    stack = []
    end = None

    for i, c in enumerate(sliced):
        if c in "{[":
            stack.append(c)
        elif c in "}]":
            if stack:
                stack.pop()
                if not stack:
                    end = i
                    break

    if end is not None:
        sliced = sliced[: end + 1]

    # 4. 再次尝试解析
    return json.loads(sliced)