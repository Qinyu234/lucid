from read_json import read_json
from decompose_idea import decompose_idea
from build_registry import build_registry
from step import step
from load_memory import load_memory
from embed import embed
from call_ollama import call_ollama
from build_tree import build_tree


def run():
    # 1. load idea
    idea = read_json("input/idea.json")

    # 2. initialize task registry
    tasks = decompose_idea(idea)
    tasks = build_registry(tasks)

    # 3. load runtime context（关键修复点）
    memory = load_memory()
    embed_fn = embed

    # 4. iterative evolution (fixed-point loop)
    while True:

        state = {
            "tasks": tasks,
            "memory": memory,
            "embed_fn": embed_fn,
            "llm": call_ollama,
        }

        state = step(state)
        new_tasks = state["tasks"]

        # convergence condition
        if new_tasks == tasks:
            break

        tasks = new_tasks
        memory = state["memory"]  # 可选：如果你 step 会更新 memory

    # 5. output final result
    tree = build_tree(tasks)
    print(tree)


if __name__ == "__main__":
    run()