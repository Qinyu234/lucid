"""
Desugaring Module
Transforms code by desugaring classes to functions, decomposing inheritance, and making state explicit.
"""

from typing import Dict, Any
from core.desugar.class_to_func import desugar_class_to_function
from core.desugar.inheritance_decompose import decompose_inheritance
from core.desugar.state_explicit import make_state_explicit


def desugar(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run the full desugaring pipeline on a CSF.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        Desugared CSF with classes converted to functions, inheritance decomposed, and state explicit
    """
    # Step 1: Convert classes to functions
    csf = desugar_class_to_function(csf)
    
    # Step 2: Decompose inheritance
    csf = decompose_inheritance(csf)
    
    # Step 3: Make state explicit
    csf = make_state_explicit(csf)
    
    return csf


__all__ = ['desugar', 'desugar_class_to_function', 'decompose_inheritance', 'make_state_explicit']
