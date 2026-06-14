"""
Def-Use Contract View for Lucid
Answers: Where is this assigned? Where is it read?
This is the MVP view for Phase 1
"""

from typing import Dict, Any, List
from ..analysis.access_contract import AccessContract


class DefUseView:
    """
    Def-Use Contract View.
    Shows where variables are defined (written) and where they are used (read).
    """
    
    def __init__(self, access_contracts: Dict[str, AccessContract]):
        self.access_contracts = access_contracts
    
    def get_variable_info(self, variable_name: str) -> Dict[str, Any]:
        """
        Get def-use information for a specific variable.
        
        Args:
            variable_name: Name of the variable
            
        Returns:
            Dictionary with definition and use information
        """
        if variable_name not in self.access_contracts:
            return {
                'variable': variable_name,
                'found': False,
            }
        
        contract = self.access_contracts[variable_name]
        
        return {
            'variable': variable_name,
            'found': True,
            'defined': contract.defined,
            'write_sites': [ws.location for ws in contract.write_sites],
            'write_count': len(contract.write_sites),
            'use_sites': [us.location for us in contract.use_sites],
            'use_count': len(contract.use_sites),
            'source': contract.source,
        }
    
    def get_all_variables(self) -> List[str]:
        """Get all variable names with access contracts."""
        return list(self.access_contracts.keys())
    
    def get_high_impact_variables(self, threshold: int = 5) -> List[str]:
        """
        Get variables that are used in many places (high impact).
        
        Args:
            threshold: Minimum number of use sites to be considered high impact
            
        Returns:
            List of variable names
        """
        high_impact = []
        for var_name, contract in self.access_contracts.items():
            if len(contract.use_sites) >= threshold:
                high_impact.append(var_name)
        
        return sorted(high_impact, key=lambda x: len(self.access_contracts[x].use_sites), reverse=True)
    
    def get_write_only_variables(self) -> List[str]:
        """
        Get variables that are written but never read (potential dead code).
        
        Returns:
            List of variable names
        """
        write_only = []
        for var_name, contract in self.access_contracts.items():
            if len(contract.write_sites) > 0 and len(contract.use_sites) == 0:
                write_only.append(var_name)
        
        return write_only


def render_def_use_contract(variable_name: str, view: DefUseView) -> str:
    """
    Render a def-use contract for a variable in a human-readable format.
    
    Args:
        variable_name: Name of the variable
        view: DefUseView instance
        
    Returns:
        Formatted string showing the access contract
    """
    info = view.get_variable_info(variable_name)
    
    if not info['found']:
        return f"Variable '{variable_name}' not found in analysis."
    
    lines = [
        f"Access Contract for '{variable_name}'",
        "=" * 50,
        f"Defined: {info['defined']}",
        "",
        f"Write Sites ({info['write_count']}):",
    ]
    
    for site in info['write_sites']:
        lines.append(f"  - {site}")
    
    lines.append("")
    lines.append(f"Use Sites ({info['use_count']}):")
    
    for site in info['use_sites']:
        lines.append(f"  - {site}")
    
    lines.append("")
    lines.append(f"Source: {info['source']}")
    
    return '\n'.join(lines)


def render_summary(view: DefUseView) -> str:
    """
    Render a summary of all access contracts.
    
    Args:
        view: DefUseView instance
        
    Returns:
        Formatted summary string
    """
    lines = [
        "Access Contract Summary",
        "=" * 50,
        f"Total variables analyzed: {len(view.get_all_variables())}",
        "",
    ]
    
    high_impact = view.get_high_impact_variables(threshold=3)
    if high_impact:
        lines.append("High Impact Variables (used 3+ times):")
        for var in high_impact[:10]:  # Top 10
            info = view.get_variable_info(var)
            lines.append(f"  - {var}: {info['use_count']} uses, {info['write_count']} writes")
        lines.append("")
    
    write_only = view.get_write_only_variables()
    if write_only:
        lines.append("Write-Only Variables (potential dead code):")
        for var in write_only:
            lines.append(f"  - {var}")
        lines.append("")
    
    return '\n'.join(lines)
