from score import score

def find_bad_task(tasks: dict) -> str | None:
    """
    返回最需要被修复的 task key
    （分数最低的那个）
    """
    if not tasks:
        return None

    worst_key = None
    worst_score = 1e9

    for k, t in tasks.items():
        sc = score(t)
        if sc < worst_score:
            worst_score = sc
            worst_key = k

    # 已经“足够好” → 不需要再修
    if worst_score >= 0.95:
        return None

    return worst_key