from pathlib import Path

from src.algorithm.algorithm_dir import algorithm_dir
from src.algorithm.load_index import load_index
from src.algorithm.register_seed_algorithms import register_seed_algorithms
from src.algorithm.save_index import save_index
from src.algorithm.seed_extended_algorithms import seed_extended_algorithms
from src.algorithm.seed_fixed_algorithms import seed_fixed_algorithms


def ensure_layout():
    root = algorithm_dir()
    categories = {
        "encoding": "Fixed-distribution source coding (advantage vs naive baselines)",
        "vision": "Fixed-layout perception (advantage vs full-frame processing)",
        "analytics": "Fixed-schema aggregation (advantage vs raw dumps)",
        "channel": "Fixed-channel models (advantage vs naive PHY)",
        "llm": "Fixed-vocab LLM decode / sampling (advantage vs naive baselines)",
        "rl": "Tabular RL on fixed state-action spaces",
        "robotics": "Fixed-map motion / kinematics primitives",
        "calculus": "Numerical calculus on uniform grids",
        "logic": "Boolean / truth-table evaluation on fixed schemas",
        "circuit": "Combinational logic netlist simulation",
        "info_theory": "Discrete entropy, MI, KL on fixed alphabets",
        "maxflow": "Max-flow on fixed sparse graphs",
        "collision": "2D collision tests on fixed geometry types",
    }

    for name, desc in categories.items():
        cat_dir = root / name
        cat_dir.mkdir(parents=True, exist_ok=True)
        init_py = cat_dir / "__init__.py"
        if not init_py.exists():
            init_py.write_text(f'"""{desc}"""\n', encoding="utf-8")

    index = load_index()
    needs_reseed = index.get("schema") != "fixed_task_v2"
    if not needs_reseed:
        for entry in index.get("algorithms", {}).values():
            if not entry.get("fixed_task") or not entry.get("relative_advantage"):
                needs_reseed = True
                break
        if not needs_reseed and len(index.get("algorithms", {})) < 23:
            needs_reseed = True

    if needs_reseed:
        index = {
            "schema": "fixed_task_v2",
            "profiles": {},
            "algorithms": {},
            "categories": {},
        }
        save_index(index)
        seed_fixed_algorithms(root)
        seed_extended_algorithms(root)
        register_seed_algorithms()
    else:
        for name, desc in categories.items():
            index.setdefault("categories", {}).setdefault(
                name,
                {"description": desc, "algorithms": []},
            )
        save_index(index)
