"""
Complexity Visualization
Estimates complexity and provides green/red color mapping for AI confidence visualization.
"""

from typing import Dict, Any
from core.complexity.complexity_estimator import estimate_complexity
from core.complexity.confidence_scorer import calculate_ai_confidence
from core.complexity.color_mapper import get_color_indicator


def visualize_complexity(csf: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate complexity and add color indicators to CSF nodes.
    
    Args:
        csf: Input CSF structure
        
    Returns:
        CSF with complexity scores and color indicators added to nodes
    """
    # Estimate complexity for each node
    complexity_scores = estimate_complexity(csf)
    
    # Calculate AI confidence scores
    confidence_scores = calculate_ai_confidence(csf, complexity_scores)
    
    # Add color indicators to nodes
    for node_id, node in csf['nodes'].items():
        complexity = complexity_scores.get(node_id, 0.5)
        confidence = confidence_scores.get(node_id, 0.5)
        
        node['meta']['complexity_score'] = complexity
        node['meta']['ai_confidence'] = confidence
        node['meta']['color_indicator'] = get_color_indicator(confidence)
    
    return csf


__all__ = ['visualize_complexity', 'estimate_complexity', 'calculate_ai_confidence', 'get_color_indicator']
