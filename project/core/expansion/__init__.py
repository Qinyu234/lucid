# Structural Expansion Engine module

from typing import Dict, Any, Optional
from core.sync.parser import parse
from core.expansion.inheritance import expand_inheritance
from core.expansion.dependency import expand_dependencies
from core.expansion.nesting import flatten_nesting
from core.expansion.mutation import annotate_mutations
from core.expansion.deduplication import deduplicate_functions, track_function_reuse


def expand(source_path: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Run the full expansion pipeline on a source file.
    
    Args:
        source_path: Path to the source file
        options: Expansion options (default: all enabled)
            {
                "inheritance": True,
                "dependency_max_span": 2,
                "nesting_max_depth": 3,
                "mutations": True,
            }
    
    Returns:
        Expanded CSF dict
    """
    if options is None:
        options = {
            "inheritance": True,
            "dependency_max_span": 2,
            "nesting_max_depth": 3,
            "mutations": True,
            "deduplication": True,
            "reuse_tracking": True,
        }
    
    # Step 1: Parse source to CSF
    csf = parse(source_path)
    
    # Step 2: Expand inheritance
    if options.get("inheritance", True):
        csf = expand_inheritance(csf)
    
    # Step 3: Expand dependencies
    csf = expand_dependencies(csf, max_span=options.get("dependency_max_span", 2))
    
    # Step 4: Flatten nesting
    csf = flatten_nesting(csf, max_depth=options.get("nesting_max_depth", 3))
    
    # Step 5: Annotate mutations
    if options.get("mutations", True):
        csf = annotate_mutations(csf)
    
    return csf
