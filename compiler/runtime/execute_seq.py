"""
execute_seq.py

Sequential execution of children nodes.
Previous node's outputs inject into next node's inputs.
Interface: fn(inputs, meta) -> dict
meta contains: children, graph, templates, context
"""

from __future__ import annotations
import time
from typing import Any

from compiler.accessor.schema_accessor import (
    get_children,
    get_node_by_id,
    get_node_type,
    get_node_inputs,
    get_node_outputs,
    get_root_id,
)


def execute_seq(inputs: dict[str, Any], meta: dict[str, Any], node: dict[str, Any]) -> dict[str, Any]:
    """
    Execute SEQ control node: sequentially execute children.
    
    Args:
        inputs: Input dictionary for SEQ node
        meta: Metadata dictionary (graph, templates, trace_dir, etc.)
        node: SEQ node dictionary
        
    Returns:
        Dictionary with outputs from last child
    """
    graph = meta["graph"]
    trace_dir = meta.get("trace_dir")
    children_ids = get_children(node)
    
    current_inputs = inputs
    outputs = {}
    
    for child_id in children_ids:
        child_node = get_node_by_id(graph, child_id)
        
        if child_node is None:
            return {
                "error": f"Child node '{child_id}' not found",
                "error_type": "runtime_error",
            }
        
        child_type = get_node_type(child_node)
        
        start_time = time.time()
        
        try:
            if child_type == "functional":
                # Execute functional node
                result = execute_functional_node(current_inputs, meta, child_node)
            elif child_type == "control":
                # Execute control node (recursive)
                from compiler.runtime.execute_seq import execute_seq
                kind = child_node.get("kind")
                
                if kind == "SEQ":
                    result = execute_seq(current_inputs, meta, child_node)
                else:
                    result = {
                        "error": f"Control kind '{kind}' not yet implemented",
                        "error_type": "runtime_error",
                    }
            else:
                result = {
                    "error": f"Node type '{child_type}' not yet implemented",
                    "error_type": "runtime_error",
                }
        except Exception as e:
            result = {
                "error": str(e),
                "error_type": "runtime_error",
            }
        
        duration = time.time() - start_time
        
        # Trace child execution
        if trace_dir:
            from compiler.runtime.trace_runtime import trace_node_execution
            trace_node_execution(
                trace_dir,
                child_id,
                current_inputs,
                result,
                duration,
                "success" if "error" not in result else "error",
            )
        
        # Check for error
        if "error" in result:
            return result
        
        # Set outputs as next inputs
        outputs = result
        current_inputs = result
    
    return outputs


def execute_functional_node(inputs: dict[str, Any], meta: dict[str, Any], node: dict[str, Any]) -> dict[str, Any]:
    """
    Execute functional node by calling its implementation.
    
    For Phase 1, returns schema-driven mock outputs.
    Mock outputs are generated from template schema, not hardcoded logic.
    
    Args:
        inputs: Input dictionary for node
        meta: Metadata dictionary
        node: Functional node dictionary
        
    Returns:
        Dictionary with outputs
    """
    from compiler.accessor.schema_accessor import (
        get_template_id,
        get_node_outputs,
        get_port_schema,
        get_shape,
        get_node_params,
    )
    
    template_id = get_template_id(node)
    node_outputs = get_node_outputs(node)
    node_params = get_node_params(node)
    
    # Schema-driven mock: generate outputs based on schema shapes
    outputs = {}
    
    for port_name, port_def in node_outputs.items():
        port_schema = get_port_schema(port_def)
        shape = get_shape(port_schema)
        
        # Generate deterministic mock value based on shape
        mock_value = generate_mock_value(shape, inputs, port_name, node_params)
        outputs[port_name] = mock_value
    
    return outputs


def generate_mock_value(shape: str, inputs: dict[str, Any], port_name: str, params: dict[str, Any]) -> Any:
    """
    Generate deterministic mock value based on schema shape.
    
    This is schema-driven, not code-driven. The same shape always produces
    the same mock value pattern, making it testable and replaceable.
    
    Args:
        shape: Schema shape type
        inputs: Node inputs (for context-dependent mocks)
        port_name: Output port name
        params: Node parameters (for constant nodes)
        
    Returns:
        Mock value matching the shape
    """
    # For constant template, use params value
    if params and "value" in params:
        return params["value"]
    
    # Schema-driven mock generation
    if shape == "string":
        return ""
    elif shape == "integer":
        return 0
    elif shape == "float":
        return 0.0
    elif shape == "boolean":
        return True
    elif shape == "list":
        return []
    elif shape == "dict":
        return {}
    else:
        # For unknown shapes, return None
        return None
