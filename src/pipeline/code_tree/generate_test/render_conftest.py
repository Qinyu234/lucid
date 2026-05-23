def render_conftest() -> str:
    return '''"""Auto-generated pytest path setup for generated workplace code."""

import sys
from pathlib import Path

_WORKPLACE = Path(__file__).resolve().parent
_OUTPUT = _WORKPLACE.parent.parent
if str(_OUTPUT) not in sys.path:
    sys.path.insert(0, str(_OUTPUT))
'''
