import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from src.config import load_app_config
from src.llm import call_llm
from src.llm_parse import extract_json_object
from src.log import get_logger
from src.pipeline.growth_loop.filter.embed_model import embed_model
from src.pipeline.growth_loop.filter.cosine_similarity import cosine_similarity


def _paths():
    cfg = load_app_config()
    memory_path = Path(cfg.get("memory_file", "io/output/memory/leaves.json"))
    shared_dir = Path(cfg.get("shared_dir", "io/output/shared"))
    threshold = float(cfg.get("memory_similarity", 0.88))
    memory_path.parent.mkdir(parents=True, exist_ok=True)
    shared_dir.mkdir(parents=True, exist_ok=True)
    init_py = shared_dir / "__init__.py"
    if not init_py.exists():
        init_py.write_text("", encoding="utf-8")
    return memory_path, shared_dir, threshold


def load_entries() -> list:
    path, _, _ = _paths()
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def save_entries(entries: list):
    path, _, _ = _paths()
    with path.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def find_similar(semantic: str) -> dict | None:
    _, _, threshold = _paths()
    vec = embed_model(semantic)
    best = None
    best_score = 0.0

    for entry in load_entries():
        ev = embed_model(entry.get("semantic", ""))
        score = cosine_similarity(vec, ev)
        if score > best_score:
            best_score = score
            best = entry

    if best and best_score >= threshold:
        best = dict(best)
        best["_score"] = best_score
        return best

    return None


def ask_reuse(node: dict, candidate: dict, job_id: str | None = None) -> dict:
    prompt = f"""
Decide whether a new leaf task can reuse an existing shared implementation.

NEW TASK:
semantic: {node.get("semantic")}
io.in: {node.get("io", {}).get("in", [])}
io.out: {node.get("io", {}).get("out", [])}

EXISTING:
semantic: {candidate.get("semantic")}
module: shared.{candidate.get("module")}
io.in: {candidate.get("io", {}).get("in", [])}
io.out: {candidate.get("io", {}).get("out", [])}
similarity: {candidate.get("_score", 0)}

OUTPUT JSON ONLY:
{{"reuse": true, "reason": "short reason"}}

Rules:
- reuse true only if tasks are functionally the same
- minor wording differences may still reuse
- different io requirements should be reuse false
"""

    raw = call_llm("memory", prompt, job_id=job_id)
    data = extract_json_object(raw) or {}
    return {
        "reuse": bool(data.get("reuse")),
        "reason": str(data.get("reason", "")),
    }


def render_reuse_wrapper(module: str) -> str:
    return (
        f"from shared.{module} import run as _shared_run\n\n\n"
        "def run(ctx):\n"
        "    return _shared_run(ctx)\n"
    )


def register_leaf(node: dict, code: str, file_path: str):
    _, shared_dir, _ = _paths()
    module = node.get("function_name") or "unnamed"
    target = shared_dir / f"{module}.py"

    if Path(file_path).exists():
        shutil.copy2(file_path, target)

    entries = load_entries()
    entries = [e for e in entries if e.get("module") != module]
    entries.append({
        "semantic": node.get("semantic", ""),
        "module": module,
        "io": node.get("io", {"in": [], "out": []}),
        "path": str(target),
        "updated": datetime.now(timezone.utc).isoformat(),
    })
    save_entries(entries)

    get_logger().info("memory registered module=%s", module)
