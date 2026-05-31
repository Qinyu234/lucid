"""
parse_text implementation

Split text string into list of tokens by whitespace.
"""

from typing import Any


def fn(inputs: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    """
    Parse text into tokens.
    
    Args:
        inputs: Dictionary with 'text' key
        meta: Metadata dictionary
        
    Returns:
        Dictionary with 'tokens' key
    """
    try:
        text = inputs.get("text", "")
        
        if not isinstance(text, str):
            return {
                "error": "Input 'text' must be a string",
                "error_type": "type_error"
            }
        
        tokens = text.split()
        
        return {
            "tokens": tokens
        }
    except Exception as e:
        return {
            "error": str(e),
            "error_type": "runtime_error"
        }
