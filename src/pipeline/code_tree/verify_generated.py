def verify_generated(code, node):
    from src.pipeline.code_tree.generate_code.verify_code import verify_code

    return verify_code(code, node)
