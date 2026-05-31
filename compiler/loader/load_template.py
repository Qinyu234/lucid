"""
load_template.py

Load template from templates/<kind>/<id>/template.json and validate against template.schema.json.
Returns template dict accessed through schema_accessor functions.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from compiler.accessor.schema_accessor import (
    get_id,
    get_version,
    get_template_inputs,
    get_template_outputs,
    get_implementations,
    get_test_suite,
    get_schema_version,
)


def load_template(template_path: str | Path) -> dict[str, Any]:
    """
    Load template from JSON file and validate basic structure.
    
    Args:
        template_path: Path to template.json file
        
    Returns:
        Template dictionary
        
    Raises:
        FileNotFoundError: If template file doesn't exist
        json.JSONDecodeError: If template file is not valid JSON
        ValueError: If template structure is invalid
    """
    template_path = Path(template_path)
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")
    
    with open(template_path, "r", encoding="utf-8") as f:
        template = json.load(f)
    
    # Basic validation
    if not isinstance(template, dict):
        raise ValueError("Template must be a dictionary")
    
    # Validate required fields exist (using accessor functions)
    try:
        template_id = get_id(template)
        version = get_version(template)
        inputs = get_template_inputs(template)
        outputs = get_template_outputs(template)
        implementations = get_implementations(template)
        test_suite = get_test_suite(template)
        schema_version = get_schema_version(template)
    except KeyError as e:
        raise ValueError(f"Template missing required field: {e}")
    
    # Validate types
    if not isinstance(template_id, str):
        raise ValueError("template id must be a string")
    
    if not isinstance(version, str):
        raise ValueError("template version must be a string")
    
    if not isinstance(inputs, dict):
        raise ValueError("template inputs must be a dictionary")
    
    if not isinstance(outputs, dict):
        raise ValueError("template outputs must be a dictionary")
    
    if not isinstance(implementations, dict):
        raise ValueError("template implementations must be a dictionary")
    
    if not isinstance(test_suite, dict):
        raise ValueError("template test_suite must be a dictionary")
    
    # Validate implementations is not empty
    if not implementations:
        raise ValueError("template must have at least one implementation")
    
    return template


def load_template_by_id(template_id: str, kind: str = "functional", templates_dir: str | Path = "templates") -> dict[str, Any]:
    """
    Load template by ID from standard templates directory structure.
    
    Args:
        template_id: Template identifier
        kind: Template kind (functional, control, macro)
        templates_dir: Base templates directory
        
    Returns:
        Template dictionary
    """
    templates_dir = Path(templates_dir)
    template_path = templates_dir / kind / template_id / "template.json"
    
    return load_template(template_path)
