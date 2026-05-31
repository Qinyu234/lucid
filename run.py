"""
run.py

Phase 1 execution pipeline:
- Load graph/l1/latest.json
- Load rules
- Run pass_runner (validate phase)
- Execute graph
- Write runtime/traces/<run_id>/
"""

from compiler.runtime.execute_graph import execute_graph
from compiler.runtime.trace_runtime import finalize_trace


def main():
    """Main execution entry point for Phase 1."""
    # Read input text
    with open("io/input/sample.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    # Prepare inputs for graph execution
    inputs = {
        "text": text,
    }
    
    # Prepare metadata
    meta = {
        "templates_dir": "templates",
        "operator_registry": {},  # Will be populated in Phase 2
    }
    
    # Execute graph
    result = execute_graph(
        inputs=inputs,
        meta=meta,
        graph_path="graph/l1/latest.json",
        traces_dir="runtime/traces",
    )
    
    # Finalize trace
    if result["trace_id"]:
        from pathlib import Path
        trace_dir = Path("runtime/traces") / result["trace_id"]
        final_status = "success" if not result["errors"] else "error"
        finalize_trace(trace_dir, final_status)
    
    # Print results
    print(f"Execution completed")
    print(f"Trace ID: {result['trace_id']}")
    print(f"Errors: {result['errors']}")
    print(f"Outputs: {result['outputs']}")
    
    return result


if __name__ == "__main__":
    main()
