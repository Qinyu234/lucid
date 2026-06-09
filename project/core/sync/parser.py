"""
Code → CSF Parser
Parses Python source code into CSF (Canonical Structural Form).
"""

from pathlib import Path
from typing import Dict, Any
from core.csf.schema import empty_csf
from core.sync.visitor import CSFVisitor
from core.sync.incremental import incremental_update, parse_from_source


def parse(source_path: str) -> Dict[str, Any]:
    """
    Parse Python source file into CSF structure.
    
    Args:
        source_path: Path to the Python source file
        
    Returns:
        CSF dict representing the code structure
    """
    source = Path(source_path).read_text(encoding='utf-8')
    return parse_from_source(source, source_path)


__all__ = ['parse', 'incremental_update', 'parse_from_source']
