"""
trace_runtime.py

Record execution traces for each node: input / output / duration / status / error.
Write to runtime/traces/<run_id>/node_traces/<node_id>.json
"""

from __future__ import annotations
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any


def create_trace_dir(traces_dir: str, trace_id: str) -> Path:
    """
    Create trace directory structure for a run.
    
    Args:
        traces_dir: Base traces directory
        trace_id: Unique trace identifier
        
    Returns:
        Path to trace directory
    """
    trace_dir = Path(traces_dir) / trace_id
    node_traces_dir = trace_dir / "node_traces"
    
    node_traces_dir.mkdir(parents=True, exist_ok=True)
    
    # Create manifest
    manifest = {
        "trace_id": trace_id,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "started",
    }
    
    with open(trace_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    return trace_dir


def trace_node_execution(
    trace_dir: Path,
    node_id: str,
    inputs: dict[str, Any],
    outputs: dict[str, Any],
    duration: float,
    status: str,
    error: str | None = None,
) -> None:
    """
    Record execution trace for a single node.
    
    Args:
        trace_dir: Trace directory path
        node_id: Node identifier
        inputs: Node inputs
        outputs: Node outputs
        duration: Execution duration in seconds
        status: Execution status (success/error)
        error: Error message if status is error
    """
    node_traces_dir = trace_dir / "node_traces"
    node_trace_file = node_traces_dir / f"{node_id}.json"
    
    trace = {
        "node_id": node_id,
        "timestamp": datetime.utcnow().isoformat(),
        "inputs": inputs,
        "outputs": outputs,
        "duration": duration,
        "status": status,
    }
    
    if error:
        trace["error"] = error
    
    with open(node_trace_file, "w", encoding="utf-8") as f:
        json.dump(trace, f, indent=2)


def finalize_trace(trace_dir: Path, final_status: str) -> None:
    """
    Finalize trace by updating manifest status.
    
    Args:
        trace_dir: Trace directory path
        final_status: Final execution status
    """
    manifest_file = trace_dir / "manifest.json"
    
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    manifest["status"] = final_status
    manifest["completed_at"] = datetime.utcnow().isoformat()
    
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
