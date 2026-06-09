"""
AI Confidence Scorer
Calculates AI confidence scores based on complexity and other factors.
"""

from typing import Dict, Any


def calculate_ai_confidence(csf: Dict[str, Any], complexity_scores: Dict[str, float]) -> Dict[str, float]:
    """
    Calculate AI confidence scores for each node.
    
    Lower complexity = higher confidence (better for AI generation)
    
    Args:
        csf: Input CSF structure
        complexity_scores: Complexity scores for each node
        
    Returns:
        Dictionary mapping node_id to confidence score (0.0 to 1.0, higher is better)
    """
    confidence_scores = {}
    
    for node_id, complexity in complexity_scores.items():
        # Confidence is inverse of complexity
        # Lower complexity = higher confidence
        confidence = 1.0 - complexity
        
        # Adjust confidence based on other factors
        node = csf['nodes'].get(node_id)
        if node:
            # Factor: State complexity (if available)
            state_complexity = node['meta'].get('state_complexity', 0.0)
            confidence -= state_complexity * 0.2
            
            # Factor: Inheritance depth (deeper inheritance = lower confidence)
            inheritance_depth = node['meta'].get('inheritance_depth', 0)
            confidence -= inheritance_depth * 0.05
            
            # Factor: Number of dependencies (more dependencies = lower confidence)
            dep_count = len(node.get('dependencies', []))
            confidence -= min(dep_count / 20.0, 0.1)
        
        # Ensure confidence is in valid range
        confidence = max(0.0, min(1.0, confidence))
        confidence_scores[node_id] = confidence
    
    return confidence_scores


__all__ = ['calculate_ai_confidence']
