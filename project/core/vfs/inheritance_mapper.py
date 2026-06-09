"""
Inheritance Mapper
Maps inheritance trees from desugared CSF to virtual files.
"""

from typing import Dict, Any, List
from core.vfs.virtual_fs import VirtualFileSystem


def map_inheritance_to_vfs(csf: Dict[str, Any], vfs: VirtualFileSystem) -> None:
    """
    Map inheritance trees from CSF to virtual files.
    
    This transformation:
    - Creates a virtual file for each original class
    - Maps methods to the class virtual file
    - Creates inheritance chain metadata
    - Enables editing of virtual files instead of original code
    
    Args:
        csf: Desugared CSF structure
        vfs: VirtualFileSystem to populate
    """
    # Group functions by their original class
    class_to_functions = group_by_original_class(csf)
    
    # Create virtual files for each class
    for original_class_id, function_ids in class_to_functions.items():
        # Find the constructor function for this class
        constructor_id = None
        for func_id in function_ids:
            func_node = csf['nodes'].get(func_id)
            if func_node and func_node['meta'].get('is_constructor'):
                constructor_id = func_id
                break
        
        if constructor_id:
            constructor_node = csf['nodes'][constructor_id]
            class_label = constructor_node['meta'].get('original_class_label', 'Unknown')
            
            # Create virtual file for this class
            virtual_path = f"classes/{class_label}.py"
            virtual_file = vfs.create_file(virtual_path, file_type="code")
            
            # Generate content for the virtual file
            content = generate_class_virtual_file_content(csf, function_ids, class_label)
            virtual_file.update_content(content)
            
            # Set metadata
            virtual_file.set_metadata('original_class_id', original_class_id)
            virtual_file.set_metadata('constructor_id', constructor_id)
            virtual_file.set_metadata('function_ids', function_ids)
            virtual_file.set_metadata('inheritance_depth', constructor_node['meta'].get('inheritance_depth', 0))
            virtual_file.set_metadata('inheritance_chain', constructor_node['meta'].get('inheritance_chain', []))


def group_by_original_class(csf: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Group function nodes by their original class.
    
    Args:
        csf: Desugared CSF structure
        
    Returns:
        Dictionary mapping original_class_id to list of function node_ids
    """
    class_to_functions = {}
    
    for node_id, node in csf['nodes'].items():
        if node['kind'] == 'function':
            original_class_id = node['meta'].get('original_class_id')
            if original_class_id:
                if original_class_id not in class_to_functions:
                    class_to_functions[original_class_id] = []
                class_to_functions[original_class_id].append(node_id)
    
    return class_to_functions


def generate_class_virtual_file_content(csf: Dict[str, Any], function_ids: List[str], class_label: str) -> str:
    """
    Generate content for a class virtual file.
    
    Args:
        csf: Desugared CSF structure
        function_ids: List of function node_ids belonging to this class
        class_label: Original class label
        
    Returns:
        Generated Python code content
    """
    lines = []
    lines.append(f"# Virtual file for class: {class_label}")
    lines.append("# This file represents the desugared version of the class")
    lines.append("")
    lines.append(f"class {class_label}:")
    lines.append("    pass  # Placeholder for virtual class structure")
    lines.append("")
    lines.append("# Methods (desugared from original class):")
    lines.append("")
    
    for func_id in function_ids:
        func_node = csf['nodes'].get(func_id)
        if func_node and not func_node['meta'].get('is_constructor'):
            func_label = func_node['label']
            lines.append(f"# Method: {func_label}")
            lines.append(f"def {func_label}(self, *args, **kwargs):")
            lines.append("    pass  # Desugared method implementation")
            lines.append("")
    
    return "\n".join(lines)


__all__ = ['map_inheritance_to_vfs']
