from find_bad_task import find_bad_task
from retrieve_best import retrieve_best
from decompose_task import decompose_task


def step(state: dict) -> dict:
    tasks = state["tasks"]

    # 1. 找到最差 task
    bad_key = find_bad_task(tasks)

    # 没有问题则直接返回（收敛）
    if bad_key is None:
        return state

    old_task = tasks[bad_key]

    # 2. memory 优先
    memory = state["memory"]
    embed_fn = state.get("embed_fn")

    memory_hit = retrieve_best(
        old_task.get("semantic", ""),
        memory,
        embed_fn
    )

    if memory_hit:
        new_tasks = [memory_hit]
    else:
        # 3. fallback 到 LLM
        llm = state["llm"]
        new_tasks = decompose_task(old_task, llm)

    # 4. 更新 registry（替换旧节点）
    new_tasks_registry = dict(tasks)
    del new_tasks_registry[bad_key]

    for t in new_tasks:
        key = t.get("file_path") or t["file_name"].replace(".py", "")
        new_tasks_registry[key] = t

    # 5. 返回新 state（核心！）
    return {
        **state,
        "tasks": new_tasks_registry
    }