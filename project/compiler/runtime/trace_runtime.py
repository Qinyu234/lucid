import json
import os
import time
import random

def start_trace(inputs: dict, meta: dict) -> dict:
    graph_id = inputs.get("graph_id")
    trace_dir = inputs.get("trace_dir")
    
    if graph_id is None:
        raise ValueError("input 'graph_id' is required")
    if trace_dir is None:
        raise ValueError("input 'trace_dir' is required")
    
    # Generate run_id (timestamp + random 4 digits)
    timestamp = int(time.time() * 1000)
    random_suffix = random.randint(1000, 9999)
    run_id = f"{timestamp}_{random_suffix}"
    
    # Create directory structure
    run_dir = os.path.join(trace_dir, run_id)
    node_traces_dir = os.path.join(run_dir, "node_traces")
    os.makedirs(node_traces_dir, exist_ok=True)
    
    # Write manifest.json
    manifest = {
        "run_id": run_id,
        "graph_id": graph_id,
        "started_at": timestamp
    }
    manifest_path = os.path.join(run_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    return {"run_id": run_id, "trace_path": run_dir}

def record_node(inputs: dict, meta: dict) -> dict:
    run_id = inputs.get("run_id")
    trace_path = inputs.get("trace_path")
    node_id = inputs.get("node_id")
    node_inputs = inputs.get("node_inputs")
    node_outputs = inputs.get("node_outputs")
    status = inputs.get("status")
    error = inputs.get("error")
    duration_ms = inputs.get("duration_ms")
    
    if trace_path is None:
        raise ValueError("input 'trace_path' is required")
    if node_id is None:
        raise ValueError("input 'node_id' is required")
    
    # Create node trace record
    trace_record = {
        "run_id": run_id,
        "node_id": node_id,
        "node_inputs": node_inputs,
        "node_outputs": node_outputs,
        "status": status,
        "error": error,
        "duration_ms": duration_ms
    }
    
    # Write to file
    node_traces_dir = os.path.join(trace_path, "node_traces")
    node_trace_path = os.path.join(node_traces_dir, f"{node_id}.json")
    with open(node_trace_path, "w", encoding="utf-8") as f:
        json.dump(trace_record, f, indent=2)
    
    return {"recorded": True}
