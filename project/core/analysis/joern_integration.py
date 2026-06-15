"""
Joern CPG Integration for Lucid
Based on ARCHITECTURE.html specification
Layer 3: Analysis - def-use chain inference based on Joern CPG

This module provides a wrapper for Joern CPG integration.
Joern is a Java-based tool for code property graph analysis.

Installation:
1. Install Java (JDK 11 or higher)
2. Install Joern: https://joern.io/
3. Start Joern server: joern
4. Use this module to interact with Joern

Note: This is a stub implementation. Full integration requires:
- Joern server running
- Joern query language knowledge
- Project-specific CPG generation
"""

from typing import Dict, Any, List, Optional
import subprocess
import json
import sys

class JoernIntegration:
    """
    Joern CPG integration wrapper.
    Provides def-use chain inference using Joern CPG.
    """
    
    def __init__(self, joern_server_url: str = "http://localhost:9000"):
        """
        Initialize Joern integration.
        
        Args:
            joern_server_url: URL of running Joern server
        """
        self.joern_server_url = joern_server_url
        self.available = self._check_joern_available()
    
    def _check_joern_available(self) -> bool:
        """
        Check if Joern server is available.
        
        Returns:
            True if Joern server is running, False otherwise
        """
        try:
            # Try to connect to Joern server
            # This is a placeholder - actual implementation would use HTTP requests
            return False
        except Exception:
            return False
    
    def generate_cpg(self, project_path: str) -> bool:
        """
        Generate Code Property Graph for a project.
        
        Args:
            project_path: Path to the project directory
            
        Returns:
            True if CPG generation successful, False otherwise
        """
        if not self.available:
            print("Joern server not available. Please start Joern server first.")
            return False
        
        try:
            # Placeholder for actual Joern CPG generation
            # Actual command would be something like:
            # joern --script generate_cpg.sc --params project_path
            print(f"Generating CPG for {project_path}...")
            return True
        except Exception as e:
            print(f"Error generating CPG: {e}")
            return False
    
    def query_def_use_chain(self, variable_name: str) -> Dict[str, Any]:
        """
        Query def-use chain for a variable using Joern CPG.
        
        Args:
            variable_name: Name of the variable to query
            
        Returns:
            Dictionary containing def-use chain information
        """
        if not self.available:
            print("Joern server not available. Using fallback implementation.")
            return self._fallback_def_use(variable_name)
        
        try:
            # Placeholder for actual Joern query
            # Actual query would be something like:
            # cpg.identifier("variable_name").defUseChain.toJson
            print(f"Querying def-use chain for {variable_name} using Joern...")
            return {
                'variable': variable_name,
                'source': 'joern_cpg',
                'definitions': [],
                'uses': [],
                'chains': []
            }
        except Exception as e:
            print(f"Error querying Joern: {e}")
            return self._fallback_def_use(variable_name)
    
    def _fallback_def_use(self, variable_name: str) -> Dict[str, Any]:
        """
        Fallback def-use implementation when Joern is not available.
        Uses the existing custom implementation.
        
        Args:
            variable_name: Name of the variable to query
            
        Returns:
            Dictionary containing def-use chain information
        """
        # This would use the existing custom implementation
        # from core.analysis.access_contract
        return {
            'variable': variable_name,
            'source': 'custom_fallback',
            'definitions': [],
            'uses': [],
            'chains': []
        }
    
    def get_all_variables(self) -> List[str]:
        """
        Get all variables from the CPG.
        
        Returns:
            List of variable names
        """
        if not self.available:
            print("Joern server not available.")
            return []
        
        try:
            # Placeholder for actual Joern query
            print("Querying all variables using Joern...")
            return []
        except Exception as e:
            print(f"Error querying variables: {e}")
            return []


def is_joern_installed() -> bool:
    """
    Check if Joern is installed on the system.
    
    Returns:
        True if Joern is installed, False otherwise
    """
    try:
        result = subprocess.run(['joern', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def install_joern_instructions() -> str:
    """
    Get instructions for installing Joern.
    
    Returns:
        Installation instructions as string
    """
    return """
Joern Installation Instructions:

1. Install Java (JDK 11 or higher):
   - Download from: https://www.oracle.com/java/technologies/downloads/
   - Or use system package manager (apt, brew, etc.)

2. Install Joern:
   - Download from: https://joern.io/
   - Extract the archive
   - Add to PATH

3. Start Joern server:
   joern

4. Verify installation:
   joern --version

For more information, see: https://joern.io/
"""


if __name__ == "__main__":
    # Test Joern integration
    print("Checking Joern installation...")
    if is_joern_installed():
        print("✓ Joern is installed")
        
        joern = JoernIntegration()
        if joern.available:
            print("✓ Joern server is running")
        else:
            print("✗ Joern server is not running")
            print("Start Joern server with: joern")
    else:
        print("✗ Joern is not installed")
        print(install_joern_instructions())
