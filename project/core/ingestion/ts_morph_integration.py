"""
ts-morph Integration for Lucid
Based on ARCHITECTURE.html specification
Layer 1: Ingestion - TypeScript deep analysis using ts-morph

This module provides a wrapper for ts-morph integration.
ts-morph is a TypeScript library for AST manipulation and analysis.

Installation:
1. Install Node.js: https://nodejs.org/
2. Install TypeScript: npm install -g typescript
3. Install ts-morph: npm install ts-morph
4. Use this module to interact with ts-morph

Note: This is a stub implementation. Full integration requires:
- Node.js environment
- TypeScript/JavaScript project
- ts-morph library installation
"""

from typing import Dict, Any, List, Optional
import subprocess
import json
import sys

class TsMorphIntegration:
    """
    ts-morph integration wrapper.
    Provides TypeScript deep analysis using ts-morph.
    """
    
    def __init__(self):
        """
        Initialize ts-morph integration.
        """
        self.available = self._check_ts_morph_available()
    
    def _check_ts_morph_available(self) -> bool:
        """
        Check if ts-morph is available.
        
        Returns:
            True if ts-morph is available, False otherwise
        """
        try:
            # Try to check if Node.js and ts-morph are installed
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode != 0:
                return False
            
            # Check if ts-morph is installed in the project
            # This would typically check package.json or node_modules
            return False
        except Exception:
            return False
    
    def analyze_typescript_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a TypeScript file using ts-morph.
        
        Args:
            file_path: Path to the TypeScript file
            
        Returns:
            Dictionary containing TypeScript analysis results
        """
        if not self.available:
            print("ts-morph not available. Using fallback implementation.")
            return self._fallback_analysis(file_path)
        
        try:
            # Placeholder for actual ts-morph analysis
            # Actual implementation would use Node.js script with ts-morph
            print(f"Analyzing TypeScript file {file_path} using ts-morph...")
            return {
                'file_path': file_path,
                'source': 'ts_morph',
                'classes': [],
                'interfaces': [],
                'types': [],
                'imports': []
            }
        except Exception as e:
            print(f"Error analyzing with ts-morph: {e}")
            return self._fallback_analysis(file_path)
    
    def _fallback_analysis(self, file_path: str) -> Dict[str, Any]:
        """
        Fallback TypeScript analysis when ts-morph is not available.
        Uses the existing tree-sitter implementation.
        
        Args:
            file_path: Path to the TypeScript file
            
        Returns:
            Dictionary containing TypeScript analysis results
        """
        # This would use the existing tree-sitter implementation
        # from core.ingestion.parser
        return {
            'file_path': file_path,
            'source': 'tree_sitter_fallback',
            'classes': [],
            'interfaces': [],
            'types': [],
            'imports': []
        }
    
    def extract_type_information(self, file_path: str) -> Dict[str, Any]:
        """
        Extract type information from TypeScript file.
        
        Args:
            file_path: Path to the TypeScript file
            
        Returns:
            Dictionary containing type information
        """
        if not self.available:
            print("ts-morph not available.")
            return {}
        
        try:
            # Placeholder for actual type extraction
            print(f"Extracting type information from {file_path}...")
            return {}
        except Exception as e:
            print(f"Error extracting types: {e}")
            return {}


def is_nodejs_installed() -> bool:
    """
    Check if Node.js is installed on the system.
    
    Returns:
        True if Node.js is installed, False otherwise
    """
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def install_ts_morph_instructions() -> str:
    """
    Get instructions for installing ts-morph.
    
    Returns:
        Installation instructions as string
    """
    return """
ts-morph Installation Instructions:

1. Install Node.js:
   - Download from: https://nodejs.org/
   - Or use system package manager (apt, brew, etc.)

2. Install TypeScript:
   npm install -g typescript

3. Install ts-morph in your project:
   npm install ts-morph

4. Verify installation:
   node --version
   npm list ts-morph

For more information, see: https://ts-morph.com/
"""


if __name__ == "__main__":
    # Test ts-morph integration
    print("Checking Node.js installation...")
    if is_nodejs_installed():
        print("✓ Node.js is installed")
        
        ts_morph = TsMorphIntegration()
        if ts_morph.available:
            print("✓ ts-morph is available")
        else:
            print("✗ ts-morph is not installed")
            print(install_ts_morph_instructions())
    else:
        print("✗ Node.js is not installed")
        print("Install Node.js from: https://nodejs.org/")
