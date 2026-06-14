"""
Ingestion Layer - Code parsing and initial processing
Phase 1: Single file parsing
"""

from .parser import parse_file, parse_code_string

__all__ = ['parse_file', 'parse_code_string']
