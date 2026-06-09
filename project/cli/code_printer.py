"""
Code Printer for CSF
Prints generated code from template
"""
from core.template.generator import generate


def print_generated_code(template_id: str, csf: dict, params: dict = None) -> None:
    """
    Print generated code from template.
    
    Args:
        template_id: Template ID
        csf: CSF dict
        params: Optional additional parameters
    """
    result = generate(template_id, csf, params)
    
    if not result['ok']:
        print(f"Cannot generate code: missing constraints: {result.get('missing', [])}")
        return
    
    print("Generated code:")
    print(result['code'])
    
    if result['llm_needed']:
        print(f"\nLLM needed for: {', '.join(result['llm_needed'])}")
