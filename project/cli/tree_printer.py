"""
Tree Printer for CSF
Prints CSF as a text tree
"""


def print_tree(csf: dict, show_mutations: bool = False, show_inherited: bool = False) -> None:
    """
    Print CSF as a text tree.
    
    Args:
        csf: CSF dict
        show_mutations: Whether to show mutation_affects
        show_inherited: Whether to show virtual inherited nodes
    """
    def print_node(node_id: str, indent: int = 0) -> None:
        if node_id not in csf['nodes']:
            return
        
        node = csf['nodes'][node_id]
        meta = node.get('meta', {})
        
        # Skip virtual nodes unless show_inherited is True
        if meta.get('virtual') and not show_inherited:
            return
        
        # Build label
        label = f"{node['label']} [{node['kind']}]"
        
        # Add source location
        src = node['source_ref']
        label += f" (lines {src['line_start']}-{src['line_end']})"
        
        # Add virtual/inherited annotation
        if meta.get('inherited_from'):
            label += f" ← inherited from {meta['inherited_from']} [virtual]"
        elif meta.get('virtual'):
            label += " [virtual]"
        
        # Add nesting depth
        if meta.get('nesting_depth'):
            label += f", depth={meta['nesting_depth']}"
        
        # Add mutation info
        if show_mutations and node['mutation_affects']:
            affects_labels = [csf['nodes'][aid]['label'] for aid in node['mutation_affects'] if aid in csf['nodes']]
            if affects_labels:
                label += f" [mutation → affects: {', '.join(affects_labels)}]"
        
        # Print with indentation
        print("  " * indent + label)
        
        # Recursively print children
        for child_id in node['children']:
            print_node(child_id, indent + 1)
    
    # Print all root nodes
    for root_id in csf['root_ids']:
        print_node(root_id)
