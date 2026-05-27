def register_leaf(node: dict, code: str, file_path: str):
    from datetime import datetime, timezone
    from pathlib import Path

    from src.pipeline.code_tree.generate_code.verify_shared_code import verify_shared_code
    from src.pipeline.memory.extract_keywords import extract_keywords
    from src.pipeline.memory.load_entries import load_entries
    from src.pipeline.memory.save_entries import save_entries
    from src.pipeline.memory.shared_dir import shared_dir
    from src.shared.lib.shutil_copy_util import shutil_copy_util
    from src.shared.logging.get_logger_util import get_logger_util
    from src.shared.validate.io_normalize_util import io_normalize_util

    module = node.get("function_name") or "unnamed"
    target = Path(shared_dir()) / f"{module}.py"
    ok, err = verify_shared_code(code, module)
    if not ok:
        get_logger_util().warning("shared register skipped module=%s err=%s", module, err)
        return
    if Path(file_path).exists():
        shutil_copy_util(file_path, str(target))
    semantic = node.get("semantic", "")
    entries = load_entries()
    entries = [e for e in entries if e.get("module") != module]
    entries.append(
        {
            "semantic": semantic,
            "keywords": extract_keywords(semantic),
            "module": module,
            "io": io_normalize_util(node.get("io")),
            "path": str(target),
            "updated": datetime.now(timezone.utc).isoformat(),
        }
    )
    save_entries(entries)
    get_logger_util().info("memory registered module=%s", module)
