"""CLI: single-module import/contract report (replaces src.import_rules.analyze_module_contract)."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def main(argv: list[str] | None = None) -> int:
    from src.shared.validate.validate_module_contract_util import validate_module_contract_util

    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: python tools/analyze_module_contract.py <path/to/module.py>")
        return 2
    path = Path(argv[0])
    if not path.is_file():
        print(f"file not found: {path}")
        return 2
    for line in validate_module_contract_util(path):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
