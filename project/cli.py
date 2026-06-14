#!/usr/bin/env python3
"""
CLI for Lucid - A code clarity tool
Extracts implicit access structure of state (who writes it, who reads it)
"""

import sys
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.ingestion import parse_file
from core.graph import build_code_graph
from core.analysis import extract_access_contracts
from core.views import DefUseView, render_def_use_contract, render_summary, StructureView
from core.virtual_layer import VirtualFileSystem


def main():
    parser = argparse.ArgumentParser(description='Lucid - Code clarity tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # analyze command - main analysis pipeline
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a source file and extract access contracts')
    analyze_parser.add_argument('source_path', help='Path to source file')
    analyze_parser.add_argument('--variable', help='Show access contract for specific variable')
    analyze_parser.add_argument('--summary', action='store_true', help='Show summary of all access contracts')
    
    # structure command - show code structure
    structure_parser = subparsers.add_parser('structure', help='Show code structure (functions, classes, variables)')
    structure_parser.add_argument('source_path', help='Path to source file')
    
    # virtual command - create virtual file system
    virtual_parser = subparsers.add_parser('virtual', help='Create virtual file system for editing')
    virtual_parser.add_argument('source_path', help='Path to source file')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        # Run the full analysis pipeline
        parsed = parse_file(args.source_path)
        graph = build_code_graph(parsed)
        contracts = extract_access_contracts(graph, parsed['source_code'])
        view = DefUseView(contracts)
        
        if args.variable:
            # Show access contract for specific variable
            print(render_def_use_contract(args.variable, view))
        elif args.summary:
            # Show summary of all access contracts
            print(render_summary(view))
        else:
            # Show all variables
            print(f"Analyzed {len(view.get_all_variables())} variables:")
            for var in view.get_all_variables():
                info = view.get_variable_info(var)
                print(f"  - {var}: {info['write_count']} writes, {info['use_count']} uses")
    
    elif args.command == 'structure':
        # Show code structure
        parsed = parse_file(args.source_path)
        graph = build_code_graph(parsed)
        view = StructureView(graph)
        print(view.render_structure())
    
    elif args.command == 'virtual':
        # Create virtual file system
        parsed = parse_file(args.source_path)
        vfs = VirtualFileSystem()
        vfs.regenerate_from_source(args.source_path, parsed)
        print(f"Created {len(vfs.get_all_files())} virtual files:")
        for path in vfs.get_all_files():
            print(f"  - {path}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
