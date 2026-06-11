#!/usr/bin/env python3
"""
CLI for CSF (Canonical Structural Form) Expansion Engine
"""

import sys
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.expansion import expand
from core.desugar import desugar
from core.vfs import create_virtual_filesystem
from core.complexity import visualize_complexity
from core.flow import analyze_flows
from core.testing import generate_test_suite
from cli.tree_printer import print_tree


def main():
    parser = argparse.ArgumentParser(description='CSF Expansion Engine CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # expand command
    expand_parser = subparsers.add_parser('expand', help='Expand a source file')
    expand_parser.add_argument('source_path', help='Path to source file')
    expand_parser.add_argument('--show-mutations', action='store_true', help='Show mutation affects')
    expand_parser.add_argument('--show-inherited', action='store_true', help='Show inherited virtual nodes')
    
    # desugar command
    desugar_parser = subparsers.add_parser('desugar', help='Desugar code (class to function, state explicit)')
    desugar_parser.add_argument('source_path', help='Path to source file')
    
    # analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze flows (typeflow, stateflow, dataflow)')
    analyze_parser.add_argument('source_path', help='Path to source file')
    
    # complexity command
    complexity_parser = subparsers.add_parser('complexity', help='Visualize complexity with color indicators')
    complexity_parser.add_argument('source_path', help='Path to source file')
    
    # vfs command
    vfs_parser = subparsers.add_parser('vfs', help='Create virtual file system from inheritance trees')
    vfs_parser.add_argument('source_path', help='Path to source file')
    
    # test command
    test_parser = subparsers.add_parser('test', help='Generate tests from flow analysis')
    test_parser.add_argument('source_path', help='Path to source file')
    
    args = parser.parse_args()
    
    if args.command == 'expand':
        csf = expand(args.source_path)
        print_tree(csf, show_mutations=args.show_mutations, show_inherited=args.show_inherited)
    elif args.command == 'desugar':
        csf = expand(args.source_path)
        csf = desugar(csf)
        print_tree(csf)
    elif args.command == 'analyze':
        csf = expand(args.source_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        print_tree(csf)
        print("\nFlow analysis complete.")
    elif args.command == 'complexity':
        csf = expand(args.source_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        test_suite = generate_test_suite(csf)
        csf = visualize_complexity(csf, test_suite)
        print_tree(csf)
        print("\nComplexity visualization complete (based on test coverage).")
    elif args.command == 'vfs':
        csf = expand(args.source_path)
        csf = desugar(csf)
        vfs = create_virtual_filesystem(csf)
        print(f"Created {len(vfs.get_all_files())} virtual files:")
        for path in vfs.get_all_files():
            print(f"  - {path}")
    elif args.command == 'test':
        csf = expand(args.source_path)
        csf = desugar(csf)
        csf = analyze_flows(csf)
        test_suite = generate_test_suite(csf)
        total_tests = (
            len(test_suite['unit_tests']) +
            len(test_suite['integration_tests']) +
            len(test_suite['state_transition_tests']) +
            len(test_suite['edge_case_tests'])
        )
        print(f"Generated {total_tests} tests:")
        print(f"  - Unit tests: {len(test_suite['unit_tests'])}")
        print(f"  - Integration tests: {len(test_suite['integration_tests'])}")
        print(f"  - State transition tests: {len(test_suite['state_transition_tests'])}")
        print(f"  - Edge case tests: {len(test_suite['edge_case_tests'])}")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
