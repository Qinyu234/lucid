"""
Heatmap Printer for CSF
Prints constraint heatmap for a template
"""
from core.template.registry import check_constraints, TEMPLATE_REGISTRY


def print_heatmap(template_id: str, csf: dict) -> None:
    """
    Print constraint heatmap for a template.
    
    Args:
        template_id: Template ID
        csf: CSF dict
    """
    result = check_constraints(template_id, csf)
    template = next((t for t in TEMPLATE_REGISTRY if t['id'] == template_id), None)
    
    if not template:
        print(f"Template not found: {template_id}")
        return
    
    print(f"Template: {template['name']}\n")
    print("Constraints:")
    
    for constraint in template['required_constraints']:
        constraint_id = constraint['id']
        label = constraint['label']
        status = result['heatmap'].get(constraint_id, 'red')
        symbol = "✓" if status == "green" else "✗"
        color = "[green]" if status == "green" else "[red]"
        
        print(f"  {symbol} {constraint_id:<15} {label:<20} {color}")
    
    print(f"\nReady: {'YES' if result['ready'] else 'NO'}（还差 {len(result['missing'])} 个约束）")
