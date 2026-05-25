from src.algorithm.load_index import load_index
from src.algorithm.save_index import save_index
from src.schema.io.normalize_io import normalize_io


def register_algorithm(entry: dict):
    fn = entry.get("function_name") or entry.get("name")
    if not fn:
        return

    fixed = entry.get("fixed_task") or {}
    profile_id = fixed.get("profile_id") or entry.get("profile_id")
    if not profile_id:
        return

    index = load_index()
    index.setdefault("schema", "fixed_task_v1")
    index.setdefault("profiles", {})
    index.setdefault("algorithms", {})

    profile = {
        "profile_id": profile_id,
        "distribution": fixed.get("distribution", ""),
        "business": fixed.get("business", ""),
        "constraints": fixed.get("constraints") or [],
    }
    index["profiles"][profile_id] = profile

    index["algorithms"][fn] = {
        "module": entry.get("module", f"algorithm.{fn}"),
        "function_name": fn,
        "category": entry.get("category", "general"),
        "semantic": entry.get("semantic", ""),
        "io": normalize_io(entry.get("io")),
        "fixed_task": profile,
        "relative_advantage": entry.get("relative_advantage") or {},
        "complexity": entry.get("complexity") or {},
        "references": entry.get("references") or [],
    }

    cat = entry.get("category", "general")
    cats = index.setdefault("categories", {})
    cat_entry = cats.setdefault(cat, {"description": "", "algorithms": []})
    if fn not in cat_entry["algorithms"]:
        cat_entry["algorithms"].append(fn)

    prof_algos = index["profiles"][profile_id].setdefault("algorithms", [])
    if fn not in prof_algos:
        prof_algos.append(fn)

    save_index(index)
