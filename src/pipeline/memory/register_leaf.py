def register_leaf(node: dict, code: str, file_path: str):
    import shutil
    from datetime import datetime, timezone
    from pathlib import Path

    from src.shared.get_logger import get_logger
    from src.pipeline.memory.extract_keywords import extract_keywords
    from src.pipeline.memory.load_entries import load_entries
    from src.pipeline.memory.save_entries import save_entries
    from src.pipeline.memory.shared_dir import shared_dir
    from src.shared.normalize_io import normalize_io
    from src.pipeline.code_tree.generate_code.verify_shared_code import verify_shared_code
    module = node.get('function_name') or 'unnamed'
    target = shared_dir() / f'{module}.py'
    ok, err = verify_shared_code(code, module)
    if not ok:
        get_logger().warning('shared register skipped module=%s err=%s', module, err)
        return
    if Path(file_path).exists():
        shutil.copy2(file_path, target)
    semantic = node.get('semantic', '')
    entries = load_entries()
    entries = [e for e in entries if e.get('module') != module]
    entries.append({'semantic': semantic, 'keywords': extract_keywords(semantic), 'module': module, 'io': normalize_io(node.get('io')), 'path': str(target), 'updated': datetime.now(timezone.utc).isoformat()})
    save_entries(entries)
    get_logger().info('memory registered module=%s', module)
