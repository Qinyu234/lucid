def persist_leaf(node, code, file_path):
    from src.pipeline.memory import register_leaf

    return register_leaf(node, code, file_path)
