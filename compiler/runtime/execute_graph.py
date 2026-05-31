"""
execute_graph.py

Main execution entry point: load -> pass_runner -> dispatch root node.
Dispatch rules: node type -> corresponding execute_*.py
Interface: fn(inputs, meta) -> dict
"""

from __future__ import annotations
import time
import uuid
from pathlib import Path
from typing import Any

from compiler.accessor.schema_accessor import (
    get_root_id,
    get_node_by_id,
    get_node_type,
)
from compiler.passes.pass_runner import run_pipeline
from compiler.runtime.execute_seq import execute_seq
from compiler.runtime.trace_runtime import trace_node_execution, create_trace_dir


def execute_graph(
    inputs: dict[str, Any],
    meta: dict[str, Any],
    graph_path: str = "graph/l1/latest.json",
    traces_dir: str = "runtime/traces",
) -> dict[str, Any]:
    """
    Execute graph from root node.
    
    Args:
        inputs: Input dictionary for root node
        meta: Metadata dictionary (templates, rules, context, etc.)
        graph_path: Path to graph JSON file
        traces_dir: Directory to write execution traces
        
    Returns:
        Dictionary with 'outputs', 'errors', 'trace_id' keys
    """
    # Load graph
    from compiler.loader.load_graph import load_graph
    from compiler.loader.load_template import load_template_by_id
    from compiler.loader.load_rules import load_rules
    
    graph = load_graph(graph_path)
    rules = load_rules()
    
    # Update meta with loaded resources
    meta["graph"] = graph
    meta["rules"] = rules
    
    # Run validation passes
    try:
        pipeline_result = run_pipeline(graph, meta, until="validate")
        
        if pipeline_result["errors"]:
            return {
                "outputs": {},
                "errors": pipeline_result["errors"],
                "trace_id": None,
            }
    except ValueError as e:
        return {
            "outputs": {},
            "errors": [str(e)],
            "trace_id": None,
        }
    
    # Create trace directory
    trace_id = str(uuid.uuid4())
    trace_dir = create_trace_dir(traces_dir, trace_id)
    
    # Update meta with trace info
    meta["trace_id"] = trace_id
    meta["trace_dir"] = trace_dir
    
    # Get root node
    root_id = get_root_id(graph)
    root_node = get_node_by_id(graph, root_id)
    
    if root_node is None:
        return {
            "outputs": {},
            "errors": [f"Root node '{root_id}' not found"],
            "trace_id": trace_id,
        }
    
    # Dispatch based on node type
    node_type = get_node_type(root_node)
    
    start_time = time.time()
    
    try:
        if node_type == "control":
            # For Phase 1, only SEQ is implemented
            from compiler.accessor.schema_accessor import get_control_kind
            kind = get_control_kind(root_node)
            
            if kind == "SEQ":
                result = execute_seq(inputs, meta, root_node)
            else:
                result = {
                    "error": f"Control kind '{kind}' not yet implemented",
                    "error_type": "runtime_error",
                }
        else:
            result = {
                "error": f"Node type '{node_type}' not yet implemented",
                "error_type": "runtime_error",
            }
    except Exception as e:
        result = {
            "error": str(e),
            "error_type": "runtime_error",
        }
    
    duration = time.time() - start_time
    
    # Trace root node execution
    trace_node_execution(
        trace_dir,
        root_id,
        inputs,
        result,
        duration,
        "success" if "error" not in result else "error",
    )
    
    return {
        "outputs": result if "error" not in result else {},
        "errors": [result.get("error", "")] if "error" in result else [],
        "trace_id": trace_id,
    }
