def render_conftest() -> str:
    return '''"""Auto-generated pytest path setup for generated workplace code."""

import sys
from pathlib import Path

_PROJECT = Path(__file__).resolve().parent
if str(_PROJECT) not in sys.path:
    sys.path.insert(0, str(_PROJECT))
'''
