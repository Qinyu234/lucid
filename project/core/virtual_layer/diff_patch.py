"""
Diff and patch utilities for virtual layer
Computes diffs between virtual and real files, applies patches back
"""

from typing import Dict, List, Tuple, Any


def compute_diff(original: str, modified: str) -> Dict[str, Any]:
    """
    Compute diff between original and modified content.
    
    Args:
        original: Original content
        modified: Modified content
        
    Returns:
        Diff dictionary with changes
    """
    original_lines = original.split('\n')
    modified_lines = modified.split('\n')
    
    changes = []
    
    # Simple line-by-line comparison
    max_len = max(len(original_lines), len(modified_lines))
    
    for i in range(max_len):
        orig_line = original_lines[i] if i < len(original_lines) else None
        mod_line = modified_lines[i] if i < len(modified_lines) else None
        
        if orig_line != mod_line:
            changes.append({
                'line': i + 1,
                'original': orig_line,
                'modified': mod_line,
                'type': 'modified' if orig_line and mod_line else ('added' if mod_line else 'removed')
            })
    
    return {
        'changes': changes,
        'total_changes': len(changes),
    }


def apply_patch(original: str, patch: Dict[str, Any]) -> str:
    """
    Apply a patch to original content.
    
    Args:
        original: Original content
        patch: Patch dictionary with changes
        
    Returns:
        Patched content
    """
    lines = original.split('\n')
    
    for change in patch.get('changes', []):
        line_num = change['line'] - 1  # Convert to 0-indexed
        
        if change['type'] == 'modified':
            if line_num < len(lines):
                lines[line_num] = change['modified']
        elif change['type'] == 'added':
            lines.insert(line_num, change['modified'])
        elif change['type'] == 'removed':
            if line_num < len(lines):
                lines.pop(line_num)
    
    return '\n'.join(lines)
