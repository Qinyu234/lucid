"""
Color Mapper
Maps test tightness and operational complexity to color indicators (green=good, red=bad).
"""

from typing import Dict, Any


def get_color_indicator(test_tightness: float, operational_complexity: float) -> str:
    """
    Get color indicator based on test tightness and operational complexity.
    
    Args:
        test_tightness: Test coverage tightness (0.0 to 1.0, higher is better)
        operational_complexity: Operational complexity (0.0 to 1.0, lower is better)
        
    Returns:
        Color indicator: 'green' for well-tested/low-complexity, 'yellow' for medium, 'red' for poorly-tested/high-complexity
    """
    # Calculate overall score: high test tightness and low operational complexity = green
    # Low test tightness or high operational complexity = red
    overall_score = test_tightness - (operational_complexity * 0.5)
    
    if overall_score >= 0.5:
        return "green"
    elif overall_score >= 0.0:
        return "yellow"
    else:
        return "red"


def get_hex_color(test_tightness: float, operational_complexity: float) -> str:
    """
    Get hex color code based on test tightness and operational complexity.
    
    Args:
        test_tightness: Test coverage tightness (0.0 to 1.0)
        operational_complexity: Operational complexity (0.0 to 1.0)
        
    Returns:
        Hex color code
    """
    overall_score = test_tightness - (operational_complexity * 0.5)
    
    if overall_score >= 0.5:
        # Green gradient
        green_intensity = int(255 * min(overall_score - 0.5, 0.5) / 0.5)
        return f"#00{green_intensity + 128:02x}00"
    elif overall_score >= 0.0:
        # Yellow gradient
        yellow_intensity = int(255 * overall_score / 0.5)
        return f"#{yellow_intensity + 128:02x}{yellow_intensity + 128:02x}00"
    else:
        # Red gradient
        red_intensity = int(255 * (0.5 + overall_score) / 0.5)
        return f"#{red_intensity + 128:02x}0000"


def get_color_description(test_tightness: float, operational_complexity: float) -> str:
    """
    Get human-readable color description.
    
    Args:
        test_tightness: Test coverage tightness (0.0 to 1.0)
        operational_complexity: Operational complexity (0.0 to 1.0)
        
    Returns:
        Human-readable description
    """
    overall_score = test_tightness - (operational_complexity * 0.5)
    
    if overall_score >= 0.7:
        return "Excellent (well-tested, low complexity)"
    elif overall_score >= 0.5:
        return "Good (adequate test coverage)"
    elif overall_score >= 0.0:
        return "Medium (moderate test coverage, moderate complexity)"
    elif overall_score >= -0.3:
        return "Poor (insufficient tests, high complexity)"
    else:
        return "Bad (no tests, very high complexity)"


__all__ = ['get_color_indicator', 'get_hex_color', 'get_color_description']
