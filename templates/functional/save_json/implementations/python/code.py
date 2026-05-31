"""
save_json implementation

Save data dictionary to JSON file.
"""

import json
from pathlib import Path
from typing import Any


def fn(inputs: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    """
    Save data to JSON file.
    
    Args:
        inputs: Dictionary with 'data' and 'path' keys
        meta: Metadata dictionary
        
    Returns:
        Dictionary with 'success' and 'path' keys
    """
    try:
        data = inputs.get("data")
        path = inputs.get("path")
        
        if not isinstance(data, dict):
            return {
                "error": "Input 'data' must be a dictionary",
                "error_type": "type_error"
            }
        
        if not isinstance(path, str):
            return {
                "error": "Input 'path' must be a string",
                "error_type": "type_error"
            }
        
        # Write to file
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        return {
            "success": True,
            "path": path
        }
    except Exception as e:
        return {
            "error": str(e),
            "error_type": "runtime_error"
        }
