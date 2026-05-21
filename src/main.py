# =========================
# FUNCTION: Entry Seed
# PURPOSE:
# Start program growth from a minimal idea seed.
# Everything expands from here.
# =========================

from .runtime import run
import json

def load_idea(path="input/idea.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":

    idea = load_idea()

    tree = run(
        seed=idea,
        llm=None  # 这里后面接你的本地模型接口
    )

    print("Generation finished.")