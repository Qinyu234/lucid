"""
Impact View for Lucid
Based on ARCHITECTURE.html specification
VIEW 05
「改这里，readers 里谁会受影响？热点在哪？」
writer 改动 → readers 影响面 → risk heatmap
+ trace → 高频 write/read → 性能热点叠加
"""

from typing import Dict, Any, List
from ..graph.builder import CodeGraph
from ..analysis.access_contract import analyze_impact


class ImpactView:
    """
    Impact View implementation.
    Shows impact of changes and performance hotspots.
    """
    
    def __init__(self, graph: CodeGraph, contracts: Dict[str, Any]):
        """
        Initialize Impact View.
        
        Args:
            graph: CodeGraph object
            contracts: Access contracts
        """
        self.graph = graph
        self.contracts = contracts
    
    def get_impact_analysis(self, state_name: str) -> Dict[str, Any]:
        """
        Get impact analysis for a state change.
        
        Args:
            state_name: Name of the state being changed
            
        Returns:
            Impact analysis dictionary
        """
        return analyze_impact(state_name, self.contracts)
    
    def get_high_impact_states(self, threshold: int = 5) -> List[Dict[str, Any]]:
        """
        Get states with high impact (many readers).
        
        Args:
            threshold: Minimum number of readers to be considered high impact
            
        Returns:
            List of high impact states
        """
        high_impact = []
        
        for state_name, contract in self.contracts.items():
            if len(contract.use_sites) >= threshold:
                high_impact.append({
                    'state': state_name,
                    'readers': len(contract.use_sites),
                    'writers': len(contract.write_sites)
                })
        
        return sorted(high_impact, key=lambda x: x['readers'], reverse=True)
    
    def get_performance_hotspots(self) -> List[Dict[str, Any]]:
        """
        Get performance hotspots from runtime trace.
        
        Returns:
            List of performance hotspots
        """
        # This would integrate with Runtime Trace Layer (Phase 2)
        # For now, return empty list as placeholder
        return []
    
    def render_impact_summary(self) -> str:
        """
        Render impact summary as text.
        
        Returns:
            String representation of impact summary
        """
        high_impact = self.get_high_impact_states()
        
        output = "Impact View (VIEW 05)\n"
        output += "「改这里，readers 里谁会受影响？热点在哪？」\n\n"
        
        if not high_impact:
            output += "No high impact states found.\n"
        else:
            output += "High Impact States:\n"
            for state in high_impact:
                output += f"  {state['state']}: {state['readers']} readers, {state['writers']} writers\n"
        
        return output
