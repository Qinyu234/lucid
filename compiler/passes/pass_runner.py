"""
pass_runner.py

Sequentially execute a list of passes on a graph.
Supports 'until' parameter to stop at specific phase (validate/lower/optimize).
Validate phase failures stop immediately.
"""

from __future__ import annotations
from typing import Any, Callable
from pathlib import Path

# Static imports for deterministic pass loading
from compiler.passes import (
    validate_001_nodes,
    validate_002_edges,
    validate_003_types,
)


def run_pipeline(
    graph: dict[str, Any],
    meta: dict[str, Any],
    until: str | None = None,
    passes_dir: str | Path = "compiler/passes"
) -> dict[str, Any]:
    """
    Run pass pipeline on graph.
    
    Args:
        graph: Graph dictionary
        meta: Metadata dictionary (templates, rules, context, etc.)
        until: Stop at this phase ('validate', 'lower', 'optimize'), None runs all
        passes_dir: Directory containing pass modules
        
    Returns:
        Dictionary with 'graph', 'meta', 'errors', 'warnings' keys
        
    Raises:
        ValueError: If validation fails and until='validate'
    """
    passes_dir = Path(passes_dir)
    
    # Define pass order with static mapping to pass functions
    pass_order = [
        ("001_validate_nodes", _001_validate_nodes.run_pass),
        ("002_validate_edges", _002_validate_edges.run_pass),
        ("003_validate_types", _003_validate_types.run_pass),
        # ("010_lower_loop", lower_010_loop.run_pass),  # Phase 3
        # ("020_fold_constants", fold_020_constants.run_pass),  # Phase 6
    ]
    
    errors = []
    warnings = []
    
    for pass_name, run_pass in pass_order:
        # Check if we should stop at this phase
        if until == "validate" and pass_name.startswith("01"):
            pass  # Run all validate passes
        elif until == "validate" and not pass_name.startswith("01"):
            break
        elif until == "lower" and pass_name.startswith("02"):
            break
        elif until == "optimize" and pass_name.startswith("03"):
            break
        
        # Execute pass (statically imported)
        try:
            result = run_pass(graph, meta)
            
            if result.get("errors"):
                errors.extend(result["errors"])
                
                # Validate phase failures stop immediately
                if pass_name.startswith("00"):
                    raise ValueError(f"Validation failed in {pass_name}: {errors}")
            
            if result.get("warnings"):
                warnings.extend(result["warnings"])
            
            # Update graph if pass returned modified version
            if "graph" in result:
                graph = result["graph"]
                
        except Exception as e:
            errors.append(f"Pass {pass_name} failed: {str(e)}")
            
            # Validate phase failures stop immediately
            if pass_name.startswith("00"):
                raise ValueError(f"Validation failed in {pass_name}: {errors}")
    
    return {
        "graph": graph,
        "meta": meta,
        "errors": errors,
        "warnings": warnings,
    }
