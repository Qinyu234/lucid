"""
Code graph builder for Lucid
Based on ARCHITECTURE.html specification
Constructs dependency and access graphs from parsed code
"""

from typing import Dict, Any, List
from .nodes import Node, NodeType, EdgeType, create_function_node, create_class_node, create_variable_node, create_state_node, create_module_node, create_event_node


class CodeGraph:
    """
    Represents the code structure as a graph per ARCHITECTURE.html.
    Tracks functions, classes, variables, and their relationships.
    Uses in-memory graph (NetworkX style), not Neo4j too early.
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
        """Get all class nodes (mapped to MODULE per ARCHITECTURE)."""
        return [n for n in self.nodes.values() if n.type == NodeType.MODULE]
    
    def get_variables(self) -> List[Node]:
        """Get all variable nodes (mapped to STATE per ARCHITECTURE)."""
        return [n for n in self.nodes.values() if n.type == NodeType.STATE]
    
    def get_states(self) -> List[Node]:
        """Get all state nodes per ARCHITECTURE.html."""
        return [n for n in self.nodes.values() if n.type == NodeType.STATE]
    
    def get_events(self) -> List[Node]:
        """Get all event nodes per ARCHITECTURE.html."""
        return [n for n in self.nodes.values() if n.type == NodeType.EVENT]
    
    def get_modules(self) -> List[Node]:
        """Get all module nodes per ARCHITECTURE.html."""
        return [n for n in self.nodes.values() if n.type == NodeType.MODULE]
    
    def add_edge(self, source_id: str, target_id: str, edge_type: EdgeType) -> None:
        """
        Add an edge between nodes per ARCHITECTURE.html specification.
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            edge_type: Type of edge (defines, uses, triggers, depends_on, coupled_with)
        """
        if source_id in self.nodes:
            self.nodes[source_id].add_edge(edge_type, target_id)
    
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
    Build a code graph from parsed code data per ARCHITECTURE.html.
    
    Args:
        parsed_data: Parsed code from ingestion layer
        
    Returns:
        CodeGraph instance
    """
    graph = CodeGraph(parsed_data['file_path'])
    graph.language = parsed_data['language']
    
    # Create module node for the file itself
    module_node = create_module_node(parsed_data['file_path'], parsed_data['file_path'])
    graph.add_node(module_node)
    
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
        
        # Add depends_on edge from function to module
        graph.add_edge(node.id, module_node.id, EdgeType.DEPENDS_ON)
    
    # Create class nodes (mapped to MODULE per ARCHITECTURE)
    for cls in parsed_data.get('classes', []):
        node = create_class_node(
            cls['name'],
            cls['line'],
            cls['column'],
            parsed_data['file_path'],
            cls.get('base_class')
        )
        graph.add_node(node)
        
        # Add depends_on edge from class to file module
        graph.add_edge(node.id, module_node.id, EdgeType.DEPENDS_ON)
    
    # Create state nodes (variables per ARCHITECTURE)
    for var in parsed_data.get('variables', []):
        node = create_state_node(
            var['name'],
            var['line'],
            var['column'],
            parsed_data['file_path'],
            f"{parsed_data['file_path']}:{var['line']}"
        )
        node.meta['initial_value'] = var.get('value')
        graph.add_node(node)
    
    # Build proper relationships using ARCHITECTURE edge types
    _build_relationships(graph, parsed_data)
    
    return graph


def _build_relationships(graph: CodeGraph, parsed_data: Dict[str, Any]) -> None:
    """
    Build relationships between nodes per ARCHITECTURE.html specification.
    Uses proper edge types: defines, uses, triggers, depends_on, coupled_with.
    
    Args:
        graph: CodeGraph to populate
        parsed_data: Parsed code data
    """
    source_code = parsed_data.get('source_code', '')
    lines = source_code.split('\n')
    
    # Build function call relationships (coupled_with edge per ARCHITECTURE)
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
                            # Add coupled_with edge per ARCHITECTURE
                            graph.add_edge(func.id, other_func.id, EdgeType.COUPLED_WITH)
                            # Maintain backward compatibility with callees/callers
                            if other_func.id not in func.callees:
                                func.callees.append(other_func.id)
                            if func.id not in other_func.callers:
                                other_func.callers.append(func.id)
    
    # Build class inheritance relationships (coupled_with edge per ARCHITECTURE)
    classes = graph.get_classes()
    class_map = {c.name: c for c in classes}
    
    for cls in classes:
        base_class = cls.meta.get('base_class')
        if base_class and base_class in class_map:
            # Add coupled_with edge for inheritance
            graph.add_edge(cls.id, class_map[base_class].id, EdgeType.COUPLED_WITH)
            class_map[base_class].meta['inherited_by'] = cls.meta.get('inherited_by', [])
            class_map[base_class].meta['inherited_by'].append(cls.id)
    
    # Build defines and uses edges for state nodes per ARCHITECTURE
    states = graph.get_states()
    state_map = {s.name: s for s in states}
    
    for func in functions:
        func_name = func.name
        body_start = func.meta.get('body_start')
        body_end = func.meta.get('body_end')
        
        if body_start and body_end:
            # Analyze function body for state access
            for i in range(body_start - 1, min(body_end, len(lines))):
                line = lines[i]
                
                # Check for writes (defines edge per ARCHITECTURE)
                for state_name, state_node in state_map.items():
                    # Simple pattern matching for assignment
                    if f'{state_name} =' in line or f'{state_name}=' in line:
                        # Add defines edge from function to state
                        graph.add_edge(func.id, state_node.id, EdgeType.DEFINES)
                        # Maintain backward compatibility
                        if state_node.id not in func.writes:
                            func.writes.append(state_node.id)
                
                # Check for reads (uses edge per ARCHITECTURE)
                for state_name, state_node in state_map.items():
                    # Check if variable is used (but not assigned)
                    if state_name in line:
                        if f'{state_name} =' not in line and f'{state_name}=' not in line:
                            # Add uses edge from function to state
                            graph.add_edge(func.id, state_node.id, EdgeType.USES)
                            # Maintain backward compatibility
                            if state_node.id not in func.reads:
                                func.reads.append(state_node.id)
