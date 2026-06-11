"""
Test for color mapper functionality
验证颜色映射器功能
"""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.complexity.color_mapper import get_color_indicator


def test_color_mapping():
    """
    Test that colors are mapped correctly based on scores.
    测试颜色能够基于分数正确映射。
    """
    # Test high test tightness, low complexity (green)
    color_green = get_color_indicator(0.9, 0.1)
    assert color_green == "green", "High test tightness and low complexity should be green"
    
    # Test medium (yellow)
    color_yellow = get_color_indicator(0.5, 0.5)
    assert color_yellow == "yellow", "Medium should be yellow"
    
    # Test low test tightness, high complexity (red)
    color_red = get_color_indicator(0.1, 0.9)
    assert color_red == "red", "Low test tightness and high complexity should be red"


def test_color_boundaries():
    """
    Test that color boundaries are correct.
    测试颜色边界是正确的。
    """
    # Test boundary at 0.5
    color_boundary1 = get_color_indicator(0.5, 0.0)
    assert color_boundary1 in ["green", "yellow"], "Boundary should be green or yellow"
    
    # Test boundary at 0.0
    color_boundary2 = get_color_indicator(0.0, 0.0)
    assert color_boundary2 in ["yellow", "red"], "Boundary should be yellow or red"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
