"""
load_rules.py

Load all rules JSON files from rules/ directory and return merged rules dict.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any


def load_rules(rules_dir: str | Path = "rules") -> dict[str, Any]:
    """
    Load all JSON files from rules directory and merge into single dict.
    
    Args:
        rules_dir: Path to rules directory
        
    Returns:
        Dictionary with all rules merged by file name
        
    Raises:
        FileNotFoundError: If rules directory doesn't exist
        json.JSONDecodeError: If any rule file is not valid JSON
    """
    rules_dir = Path(rules_dir)
    
    if not rules_dir.exists():
        raise FileNotFoundError(f"Rules directory not found: {rules_dir}")
    
    if not rules_dir.is_dir():
        raise ValueError(f"Rules path is not a directory: {rules_dir}")
    
    merged_rules = {}
    
    # Load all JSON files in rules directory
    for rule_file in rules_dir.glob("*.json"):
        with open(rule_file, "r", encoding="utf-8") as f:
            rule_data = json.load(f)
        
        # Use filename (without .json) as key
        rule_name = rule_file.stem
        merged_rules[rule_name] = rule_data
    
    return merged_rules


def load_rule_file(rule_name: str, rules_dir: str | Path = "rules") -> dict[str, Any]:
    """
    Load a specific rule file by name.
    
    Args:
        rule_name: Name of rule file (without .json extension)
        rules_dir: Path to rules directory
        
    Returns:
        Rule dictionary
        
    Raises:
        FileNotFoundError: If rule file doesn't exist
    """
    rules_dir = Path(rules_dir)
    rule_path = rules_dir / f"{rule_name}.json"
    
    if not rule_path.exists():
        raise FileNotFoundError(f"Rule file not found: {rule_path}")
    
    with open(rule_path, "r", encoding="utf-8") as f:
        return json.load(f)
