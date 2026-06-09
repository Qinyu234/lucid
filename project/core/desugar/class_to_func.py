"""
Class to Function Desugaring
Converts classes to functions by extracting methods as standalone functions with explicit self parameter.
"""

from typing import Dict, Any, List
from core.csf.schema import generate_node_id


def desugar_class_to_function(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert all class nodes to function nodes.
    
    This transformation:
    - Converts each class to a constructor function
    - Extracts methods as standalone functions with explicit self parameter
    - Preserves the original structure for virtual file mapping
    
    Args:
        csf: Input CSF structure
        
    Returns:
        CSF with classes converted to functions
    """
    new_nodes = {}
    class_to_constructor = {}  # Map class_id to constructor function_id
    method_to_function = {}   # Map method_id to standalone function_id
    
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'class':
            # Convert class to constructor function
            constructor_id = generate_node_id()
            constructor = {
                'id': constructor_id,
                'kind': 'function',
                'label': f'__constructor_{node["label"]}',
                'source_ref': node['source_ref'],
                'children': [],
                'dependencies': [],
                'mutations': [],
                'mutation_affects': [],
                'expansion_state': 'collapsed',
                'meta': {
                    'original_class_id': node_id,
                    'original_class_label': node['label'],
                    'is_constructor': True,
                    'desugared_from': 'class'
                }
            }
            new_nodes[constructor_id] = constructor
            class_to_constructor[node_id] = constructor_id
            
            # Convert methods to standalone functions
            for child_id in node['children']:
                child_node = csf['nodes'].get(child_id)
                if child_node and child_node['kind'] == 'function':
                    method_func_id = generate_node_id()
                    method_func = {
                        'id': method_func_id,
                        'kind': 'function',
                        'label': f'{node["label"]}_{child_node["label"]}',
                        'source_ref': child_node['source_ref'],
                        'children': child_node['children'],
                        'dependencies': child_node['dependencies'],
                        'mutations': child_node['mutations'],
                        'mutation_affects': child_node['mutation_affects'],
                        'expansion_state': child_node['expansion_state'],
                        'meta': {
                            'original_method_id': child_id,
                            'original_class_id': node_id,
                            'original_class_label': node['label'],
                            'self_parameter': 'self',
                            'desugared_from': 'method'
                        }
                    }
                    new_nodes[method_func_id] = method_func
                    method_to_function[child_id] = method_func_id
                    
                    # Add dependency on constructor
                    method_func['dependencies'].append(constructor_id)
        else:
            # Keep non-class nodes as-is
            new_nodes[node_id] = node
    
    # Update root_ids to replace class IDs with constructor IDs
    new_root_ids = []
    for root_id in csf['root_ids']:
        if root_id in class_to_constructor:
            new_root_ids.append(class_to_constructor[root_id])
        else:
            new_root_ids.append(root_id)
    
    # Update children references in all nodes
    for node in new_nodes.values():
        new_children = []
        for child_id in node['children']:
            if child_id in method_to_function:
                new_children.append(method_to_function[child_id])
            elif child_id in class_to_constructor:
                new_children.append(class_to_constructor[child_id])
            else:
                new_children.append(child_id)
        node['children'] = new_children
        
        # Update dependencies
        new_deps = []
        for dep_id in node['dependencies']:
            if dep_id in method_to_function:
                new_deps.append(method_to_function[dep_id])
            elif dep_id in class_to_constructor:
                new_deps.append(class_to_constructor[dep_id])
            else:
                new_deps.append(dep_id)
        node['dependencies'] = new_deps
    
    csf['nodes'] = new_nodes
    csf['root_ids'] = new_root_ids
    
    return csf


__all__ = ['desugar_class_to_function']
