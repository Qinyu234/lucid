#!/usr/bin/env python3
"""
CLI for CSF (Canonical Structural Form) Expansion Engine
"""

import sys
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.expansion import expand
from cli.tree_printer import print_tree
from cli.heatmap_printer import print_heatmap
from cli.code_printer import print_generated_code


def main():
    parser = argparse.ArgumentParser(description='CSF Expansion Engine CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # expand command
    expand_parser = subparsers.add_parser('expand', help='Expand a source file')
    expand_parser.add_argument('source_path', help='Path to source file')
    expand_parser.add_argument('--show-mutations', action='store_true', help='Show mutation affects')
    expand_parser.add_argument('--show-inherited', action='store_true', help='Show inherited virtual nodes')
    
    # heatmap command
    heatmap_parser = subparsers.add_parser('heatmap', help='Show constraint heatmap for a template')
    heatmap_parser.add_argument('source_path', help='Path to source file')
    heatmap_parser.add_argument('--template', required=True, help='Template ID')
    
    # generate command
    generate_parser = subparsers.add_parser('generate', help='Generate code from template')
    generate_parser.add_argument('source_path', help='Path to source file')
    generate_parser.add_argument('--template', required=True, help='Template ID')
    
    args = parser.parse_args()
    
    if args.command == 'expand':
        csf = expand(args.source_path)
        print_tree(csf, show_mutations=args.show_mutations, show_inherited=args.show_inherited)
    elif args.command == 'heatmap':
        csf = expand(args.source_path)
        print_heatmap(args.template, csf)
    elif args.command == 'generate':
        csf = expand(args.source_path)
        print_generated_code(args.template, csf)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
