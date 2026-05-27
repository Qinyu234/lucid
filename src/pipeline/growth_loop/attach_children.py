def attach_children(node, proposal, topology: str, boundary: dict | None = None):
    from src.shared.lib.attach_children_util import attach_children_util

    attach_children_util(node, proposal, topology, boundary)
