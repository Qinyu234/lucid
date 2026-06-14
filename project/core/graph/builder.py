"""
Code graph builder for Lucid
Constructs dependency and access graphs from parsed code
"""

from typing import Dict, Any, List
from .nodes import Node, NodeType, create_function_node, create_class_node, create_variable_node


class CodeGraph:
    """
    Represents the code structure as a graph.
    Tracks functions, classes, variables, and their relationships.
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.nodes: Dict[str, Node] = {}  # node_id -> Node
        self.by_name: Dict[str, List[str]] = {}  # name -> [node_ids]
        self.language: str = ""
    
    def add_node(self, node: Node) -> None:
        """Add a node to the graph."""
        self.nodes[node.id] = node
        if node.name not in self.by_name:
            self.by_name[node.name] = []
        self.by_name[node.name].append(node.id)
    
    def get_node(self, node_id: str) -> Node:
        """Get a node by ID."""
        return self.nodes.get(node_id)
    
    def get_nodes_by_name(self, name: str) -> List[Node]:
        """Get all nodes with a given name."""
        node_ids = self.by_name.get(name, [])
        return [self.nodes[nid] for nid in node_ids]
    
    def get_functions(self) -> List[Node]:
        """Get all function nodes."""
        return [n for n in self.nodes.values() if n.type == NodeType.FUNCTION]
    
    def get_classes(self) -> List[Node]:
        """Get all class nodes."""
        return [n for n in self.nodes.values() if n.type == NodeType.CLASS]
    
    def get_variables(self) -> List[Node]:
        """Get all variable nodes."""
        return [n for n in self.nodes.values() if n.type == NodeType.VARIABLE]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert graph to dictionary representation."""
        return {
            'file_path': self.file_path,
            'language': self.language,
            'nodes': {nid: node.to_dict() for nid, node in self.nodes.items()},
            'by_name': self.by_name,
        }


def build_code_graph(parsed_data: Dict[str, Any]) -> CodeGraph:
    """
    Build a code graph from parsed code data.
    
    Args:
        parsed_data: Parsed code from ingestion layer
        
    Returns:
        CodeGraph instance
    """
    graph = CodeGraph(parsed_data['file_path'])
    graph.language = parsed_data['language']
    
    # Create function nodes
    for func in parsed_data.get('functions', []):
        node = create_function_node(
            func['name'],
            func['line'],
            func['column'],
            parsed_data['file_path']
        )
        node.meta['parameters'] = func.get('parameters', [])
        node.meta['body_start'] = func.get('body_start')
        node.meta['body_end'] = func.get('body_end')
        graph.add_node(node)
    
    # Create class nodes
    for cls in parsed_data.get('classes', []):
        node = create_class_node(
            cls['name'],
            cls['line'],
            cls['column'],
            parsed_data['file_path'],
            cls.get('base_class')
        )
        graph.add_node(node)
    
    # Create variable nodes
    for var in parsed_data.get('variables', []):
        node = create_variable_node(
            var['name'],
            var['line'],
            var['column'],
            parsed_data['file_path'],
            var.get('value')
        )
        graph.add_node(node)
    
    # Build basic relationships
    _build_relationships(graph, parsed_data)
    
    return graph


def _build_relationships(graph: CodeGraph, parsed_data: Dict[str, Any]) -> None:
    """
    Build basic relationships between nodes.
    Tracks function calls, class inheritance, and variable scope.
    
    Args:
        graph: CodeGraph to populate
        parsed_data: Parsed code data
    """
    source_code = parsed_data.get('source_code', '')
    lines = source_code.split('\n')
    
    # Build function call relationships
    functions = graph.get_functions()
    function_map = {f.name: f for f in functions}
    
    for func in functions:
        func_name = func.name
        body_start = func.meta.get('body_start')
        body_end = func.meta.get('body_end')
        
        if body_start and body_end:
            # Analyze function body for calls
            for i in range(body_start - 1, min(body_end, len(lines))):
                line = lines[i]
                # Find function calls in this line
                for other_func_name, other_func in function_map.items():
                    if other_func_name != func_name:
                        # Check if this function is called
                        if f'{other_func_name}(' in line:
                            # Avoid duplicates
                            if other_func.id not in func.callees:
                                func.callees.append(other_func.id)
                            if func.id not in other_func.callers:
                                other_func.callers.append(func.id)
    
    # Build class inheritance relationships
    classes = graph.get_classes()
    class_map = {c.name: c for c in classes}
    
    for cls in classes:
        base_class = cls.meta.get('base_class')
        if base_class and base_class in class_map:
            # Add inheritance relationship
            cls.meta['inherits_from'] = class_map[base_class].id
            class_map[base_class].meta['inherited_by'] = cls.meta.get('inherited_by', [])
            class_map[base_class].meta['inherited_by'].append(cls.id)
