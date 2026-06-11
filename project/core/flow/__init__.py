"""
Flow Analysis Module
Analyzes typeflow, stateflow, and dataflow for code understanding and test generation.
"""

from typing import Dict, Any
from core.flow.typeflow import analyze_typeflow
from core.flow.stateflow import analyze_stateflow
from core.flow.dataflow import analyze_dataflow
from core.flow.state_visualizer import visualize_state
from core.flow.skeleton_generator import add_flowchart_metadata
from core.complexity import estimate_complexity


def analyze_flows(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run complete flow analysis on a CSF.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        CSF with flow analysis metadata added to nodes
    """
    # Analyze typeflow
    csf = analyze_typeflow(csf)
    
    # Analyze stateflow
    csf = analyze_stateflow(csf)
    
    # Analyze dataflow
    csf = analyze_dataflow(csf)
    
    # Add flowchart metadata for skeleton generation
    csf = add_flowchart_metadata(csf)
    
    # Estimate complexity (including semantic complexity from flows)
    csf = estimate_complexity(csf)
    
    return csf


__all__ = ['analyze_flows', 'analyze_typeflow', 'analyze_stateflow', 'analyze_dataflow', 'visualize_state', 'add_flowchart_metadata']
