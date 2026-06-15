"""
Def-Use Contract View for Lucid
Based on ARCHITECTURE.html specification
VIEW 04 · MVP Target
「谁能改这个 state？谁在用它？改了影响谁？」
state → writers（红）→ readers（绿）→ 悬停显示文件位置 → 违反高亮
"""

from typing import Dict, Any, List
from ..analysis.access_contract import AccessContract


class DefUseView:
    """
    Def-Use Contract View per ARCHITECTURE.html VIEW 04.
    MVP Target view showing access contracts.
    
    Flow: state → writers（红）→ readers（绿）→ 悬停显示文件位置 → 违反高亮
    """
    
    def __init__(self, access_contracts: Dict[str, AccessContract]):
        self.access_contracts = access_contracts
    
    def get_variable_info(self, variable_name: str) -> Dict[str, Any]:
        """
        Get def-use information for a specific variable per ARCHITECTURE VIEW 04.
        
        Args:
            variable_name: Name of the variable
            
        Returns:
            Dictionary with definition and use information including risk level
        """
        if variable_name not in self.access_contracts:
            return {
                'variable': variable_name,
                'found': False,
            }
        
        contract = self.access_contracts[variable_name]
        
        # Calculate risk level per ARCHITECTURE: more readers = higher risk
        reader_count = len(contract.use_sites)
        if reader_count == 0:
            risk_level = "none"
        elif reader_count <= 2:
            risk_level = "low"
        elif reader_count <= 5:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        return {
            'variable': variable_name,
            'found': True,
            'defined': contract.defined,
            'write_sites': [ws.location for ws in contract.write_sites],
            'write_count': len(contract.write_sites),
            'use_sites': [us.location for us in contract.use_sites],
            'use_count': len(contract.use_sites),
            'source': contract.source,
            'risk_level': risk_level,
            'is_healthy': contract.is_healthy(),
        }
    
    def get_all_variables(self) -> List[str]:
        """Get all variable names with access contracts."""
        return list(self.access_contracts.keys())
    
    def get_high_impact_variables(self, threshold: int = 5) -> List[Dict[str, Any]]:
        """
        Get variables that are used in many places (high impact) per ARCHITECTURE.
        Per ARCHITECTURE: more readers = higher risk.
        
        Args:
            threshold: Minimum number of use sites to be considered high impact
            
        Returns:
            List of variable names with metadata
        """
        high_impact = []
        for var_name, contract in self.access_contracts.items():
            if len(contract.use_sites) >= threshold:
                high_impact.append({
                    'variable': var_name,
                    'use_count': len(contract.use_sites),
                    'write_count': len(contract.write_sites),
                    'defined': contract.defined,
                    'risk_level': 'high' if len(contract.use_sites) > 10 else 'medium',
                })
        
        return sorted(high_impact, key=lambda x: x['use_count'], reverse=True)
    
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
    Render a def-use contract for a variable per ARCHITECTURE VIEW 04.
    Flow: state → writers（红）→ readers（绿）→ 悬停显示文件位置 → 违反高亮
    
    Args:
        variable_name: Name of the variable
        view: DefUseView instance
        
    Returns:
        Formatted string showing the access contract with risk level
    """
    info = view.get_variable_info(variable_name)
    
    if not info['found']:
        return f"Variable '{variable_name}' not found in analysis."
    
    lines = [
        f"Access Contract for '{variable_name}' (VIEW 04)",
        "=" * 50,
        f"Defined: {info['defined']}",
        f"Source: {info['source']}",
        f"Risk Level: {info['risk_level'].upper()}",
        f"Healthy: {'Yes' if info['is_healthy'] else 'No'}",
        "",
        f"Write Sites ({info['write_count']}):",  # Writers in red (conceptually)
    ]
    
    for site in info['write_sites']:
        lines.append(f"  - {site}")
    
    lines.append("")
    lines.append(f"Use Sites ({info['use_count']}):")  # Readers in green (conceptually)
    
    for site in info['use_sites']:
        lines.append(f"  - {site}")
    
    return '\n'.join(lines)


def render_summary(view: DefUseView) -> str:
    """
    Render a summary of all access contracts per ARCHITECTURE VIEW 04.
    
    Args:
        view: DefUseView instance
        
    Returns:
        Formatted summary string with risk analysis
    """
    lines = [
        "Def-Use Contract Summary (VIEW 04)",
        "=" * 50,
        f"Total variables analyzed: {len(view.get_all_variables())}",
        "",
    ]
    
    high_impact = view.get_high_impact_variables(threshold=3)
    if high_impact:
        lines.append("High Impact Variables (used 3+ times):")
        for var_info in high_impact[:10]:  # Top 10
            lines.append(f"  - {var_info['variable']}: {var_info['use_count']} uses, {var_info['write_count']} writes, risk={var_info['risk_level']}")
        lines.append("")
    
    write_only = view.get_write_only_variables()
    if write_only:
        lines.append("Write-Only Variables (potential dead code):")
        for var in write_only:
            lines.append(f"  - {var}")
        lines.append("")
    
    return '\n'.join(lines)
