import json
import os

def load_template(inputs: dict, meta: dict) -> dict:
    template_id = inputs.get("template_id")
    registry_path = inputs.get("registry_path")
    
    if template_id is None:
        raise ValueError("input 'template_id' is required")
    if registry_path is None:
        raise ValueError("input 'registry_path' is required")
    
    # Load registry
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    
    # Find template in registry
    template_location = None
    for tmpl in registry.get("templates", []):
        if tmpl["id"] == template_id:
            template_location = tmpl["location"]
            break
    
    if template_location is None:
        raise ValueError(f"template_id '{template_id}' not found in registry")
    
    # Resolve template location relative to project root (registry is in project/registry/)
    registry_dir = os.path.dirname(registry_path)
    project_root = os.path.dirname(registry_dir)
    template_path = os.path.join(project_root, template_location)
    
    # Load template
    with open(template_path, "r", encoding="utf-8") as f:
        template = json.load(f)
    
    # Check required fields
    required_fields = ["id", "inputs", "outputs", "implementations"]
    for field in required_fields:
        if field not in template:
            raise ValueError(f"template missing required field: {field}")
    
    return {"template": template}
