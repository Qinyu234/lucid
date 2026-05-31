import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from compiler.runtime.execute_graph import execute_graph

script_dir = os.path.dirname(__file__)

result = execute_graph({
    "graph_path":    os.path.join(script_dir, "graph/latest.json"),
    "registry_path": os.path.join(script_dir, "registry/operator_registry.json"),
    "trace_dir":     os.path.join(script_dir, "runtime/traces/")
}, {})

if result["ok"]:
    print(f"OK  run_id={result['run_id']}")
    print(f"    outputs={result['outputs']}")
else:
    print("FAIL")
    for e in result["errors"]:
        print(f"  {e}")
    sys.exit(1)
