"""
Color Mapper
Maps confidence scores to color indicators (green=good, red=bad).
"""

from typing import Dict, Any


def get_color_indicator(confidence: float) -> str:
    """
    Get color indicator based on confidence score.
    
    Args:
        confidence: Confidence score (0.0 to 1.0, higher is better)
        
    Returns:
        Color indicator: 'green' for high confidence, 'yellow' for medium, 'red' for low
    """
    if confidence >= 0.7:
        return "green"
    elif confidence >= 0.4:
        return "yellow"
    else:
        return "red"


def get_hex_color(confidence: float) -> str:
    """
    Get hex color code based on confidence score.
    
    Args:
        confidence: Confidence score (0.0 to 1.0)
        
    Returns:
        Hex color code
    """
    if confidence >= 0.7:
        # Green gradient
        green_intensity = int(255 * (confidence - 0.7) / 0.3)
        return f"#00{green_intensity:02x}00"
    elif confidence >= 0.4:
        # Yellow gradient
        yellow_intensity = int(255 * (confidence - 0.4) / 0.3)
        return f"#{yellow_intensity:02x}{yellow_intensity:02x}00"
    else:
        # Red gradient
        red_intensity = int(255 * confidence / 0.4)
        return f"#{red_intensity:02x}0000"


def get_color_description(confidence: float) -> str:
    """
    Get human-readable color description.
    
    Args:
        confidence: Confidence score (0.0 to 1.0)
        
    Returns:
        Human-readable description
    """
    if confidence >= 0.9:
        return "Excellent (high confidence, low complexity)"
    elif confidence >= 0.7:
        return "Good (high confidence)"
    elif confidence >= 0.4:
        return "Medium (moderate confidence)"
    elif confidence >= 0.2:
        return "Poor (low confidence, high complexity)"
    else:
        return "Bad (very low confidence, very high complexity)"


__all__ = ['get_color_indicator', 'get_hex_color', 'get_color_description']
