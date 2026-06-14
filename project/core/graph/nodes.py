"""
Graph node definitions for Lucid code graph
"""

from typing import Dict, Any, List, Optional
from enum import Enum
import uuid


class NodeType(Enum):
    """Types of nodes in the code graph."""
    FUNCTION = "function"
    CLASS = "class"
    VARIABLE = "variable"
    MODULE = "module"
    PARAMETER = "parameter"


class Node:
    """Base class for graph nodes."""
    
    def __init__(self, node_type: NodeType, name: str, source_ref: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.type = node_type
        self.name = name
        self.source_ref = source_ref
        self.writes: List[str] = []  # List of variable IDs this node writes to
        self.reads: List[str] = []   # List of variable IDs this node reads from
        self.callees: List[str] = [] # List of function IDs this node calls
        self.callers: List[str] = [] # List of function IDs that call this node
        self.meta: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary representation."""
        return {
            'id': self.id,
            'type': self.type.value,
            'name': self.name,
            'source_ref': self.source_ref,
            'writes': self.writes,
            'reads': self.reads,
            'callees': self.callees,
            'callers': self.callers,
            'meta': self.meta,
        }


def create_function_node(name: str, line: int, column: int, file_path: str) -> Node:
    """
    Create a function node.
    
    Args:
        name: Function name
        line: Line number in source
        column: Column number in source
        file_path: Path to source file
        
    Returns:
        Function node
    """
    source_ref = {
        'file_path': file_path,
        'line': line,
        'column': column,
    }
    return Node(NodeType.FUNCTION, name, source_ref)


def create_class_node(name: str, line: int, column: int, file_path: str, base_class: Optional[str] = None) -> Node:
    """
    Create a class node.
    
    Args:
        name: Class name
        line: Line number in source
        column: Column number in source
        file_path: Path to source file
        base_class: Base class name if inheritance
        
    Returns:
        Class node
    """
    source_ref = {
        'file_path': file_path,
        'line': line,
        'column': column,
    }
    node = Node(NodeType.CLASS, name, source_ref)
    if base_class:
        node.meta['base_class'] = base_class
    return node


def create_variable_node(name: str, line: int, column: int, file_path: str, value: Optional[str] = None) -> Node:
    """
    Create a variable node.
    
    Args:
        name: Variable name
        line: Line number in source
        column: Column number in source
        file_path: Path to source file
        value: Initial value if available
        
    Returns:
        Variable node
    """
    source_ref = {
        'file_path': file_path,
        'line': line,
        'column': column,
    }
    node = Node(NodeType.VARIABLE, name, source_ref)
    if value:
        node.meta['initial_value'] = value
    return node
