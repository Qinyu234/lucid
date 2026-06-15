"""
Graph node definitions for Lucid
Based on ARCHITECTURE.html specification
"""

from typing import Dict, Any, List, Optional
from enum import Enum
import uuid


class NodeType(Enum):
    """Types of nodes in the code graph per ARCHITECTURE.html."""
    STATE = "state"              # StateNode: piece of state with access contract
    EVENT = "event"              # EventNode: event handler/trigger
    FUNCTION = "function"        # FunctionNode: function/method
    MODULE = "module"            # ModuleNode: module/file
    EXTERNAL_EFFECT = "external_effect"  # ExternalEffectNode: external side effects


class EdgeType(Enum):
    """Types of edges in the code graph per ARCHITECTURE.html."""
    DEFINES = "defines"          # write site to state (def edge)
    USES = "uses"                # use site to state (use edge)
    TRIGGERS = "triggers"        # event propagation
    DEPENDS_ON = "depends_on"    # module dependency
    COUPLED_WITH = "coupled_with"  # implicit coupling


class Node:
    """Base class for graph nodes."""
    
    def __init__(self, node_type: NodeType, name: str, source_ref: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.type = node_type
        self.name = name
        self.source_ref = source_ref
        self.writes: List[str] = []  # List of state IDs this node writes to
        self.reads: List[str] = []   # List of state IDs this node reads from
        self.callees: List[str] = [] # List of function IDs this node calls
        self.callers: List[str] = [] # List of function IDs that call this node
        self.meta: Dict[str, Any] = {}
        # Edge storage per ARCHITECTURE.html specification
        self.edges: Dict[EdgeType, List[str]] = {
            EdgeType.DEFINES: [],
            EdgeType.USES: [],
            EdgeType.TRIGGERS: [],
            EdgeType.DEPENDS_ON: [],
            EdgeType.COUPLED_WITH: [],
        }
    
    def add_edge(self, edge_type: EdgeType, target_id: str) -> None:
        """Add an edge of specific type to a target node."""
        if target_id not in self.edges[edge_type]:
            self.edges[edge_type].append(target_id)
    
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
            'edges': {edge_type.value: targets for edge_type, targets in self.edges.items()},
            'meta': self.meta,
        }


def create_state_node(name: str, line: int, column: int, file_path: str, 
                      defined_location: str = None) -> Node:
    """
    Create a state node (StateNode per ARCHITECTURE.html).
    Represents a piece of state with access contract.
    
    Args:
        name: State/variable name
        line: Line number in source
        column: Column number in source
        file_path: Path to source file
        defined_location: Where the state is first defined
        
    Returns:
        State node
    """
    source_ref = {
        'file_path': file_path,
        'line': line,
        'column': column,
    }
    node = Node(NodeType.STATE, name, source_ref)
    if defined_location:
        node.meta['defined'] = defined_location
    node.meta['write_sites'] = []
    node.meta['use_sites'] = []
    node.meta['source'] = 'inferred'  # inferred or explicit
    return node


def create_event_node(name: str, line: int, column: int, file_path: str) -> Node:
    """
    Create an event node (EventNode per ARCHITECTURE.html).
    Represents event handlers/triggers.
    
    Args:
        name: Event name
        line: Line number in source
        column: Column number in source
        file_path: Path to source file
        
    Returns:
        Event node
    """
    source_ref = {
        'file_path': file_path,
        'line': line,
        'column': column,
    }
    node = Node(NodeType.EVENT, name, source_ref)
    return node


def create_function_node(name: str, line: int, column: int, file_path: str) -> Node:
    """
    Create a function node (FunctionNode per ARCHITECTURE.html).
    
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


def create_module_node(name: str, file_path: str) -> Node:
    """
    Create a module node (ModuleNode per ARCHITECTURE.html).
    Represents a module/file.
    
    Args:
        name: Module/file name
        file_path: Path to source file
        
    Returns:
        Module node
    """
    source_ref = {
        'file_path': file_path,
        'line': 0,
        'column': 0,
    }
    node = Node(NodeType.MODULE, name, source_ref)
    return node


def create_external_effect_node(name: str, description: str) -> Node:
    """
    Create an external effect node (ExternalEffectNode per ARCHITECTURE.html).
    Represents external side effects (API calls, I/O, etc.).
    
    Args:
        name: Effect name
        description: Description of the external effect
        
    Returns:
        External effect node
    """
    source_ref = {
        'file_path': 'external',
        'line': 0,
        'column': 0,
    }
    node = Node(NodeType.EXTERNAL_EFFECT, name, source_ref)
    node.meta['description'] = description
    return node


# Backward compatibility - map old VARIABLE to STATE
def create_variable_node(name: str, line: int, column: int, file_path: str, 
                        value: Optional[str] = None) -> Node:
    """
    Create a variable node (mapped to StateNode for ARCHITECTURE compliance).
    
    Args:
        name: Variable name
        line: Line number in source
        column: Column number in source
        file_path: Path to source file
        value: Initial value if available
        
    Returns:
        State node (for ARCHITECTURE compliance)
    """
    source_ref = {
        'file_path': file_path,
        'line': line,
        'column': column,
    }
    node = Node(NodeType.STATE, name, source_ref)
    if value:
        node.meta['initial_value'] = value
    return node


# Backward compatibility - map old CLASS to MODULE
def create_class_node(name: str, line: int, column: int, file_path: str, 
                     base_class: Optional[str] = None) -> Node:
    """
    Create a class node (mapped to Module for ARCHITECTURE compliance).
    
    Args:
        name: Class name
        line: Line number in source
        column: Column number in source
        file_path: Path to source file
        base_class: Base class name if inheritance
        
    Returns:
        Module node (for ARCHITECTURE compliance)
    """
    source_ref = {
        'file_path': file_path,
        'line': line,
        'column': column,
    }
    node = Node(NodeType.MODULE, name, source_ref)
    if base_class:
        node.meta['base_class'] = base_class
    return node
