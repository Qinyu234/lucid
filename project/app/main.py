"""
Local Application Entry Point
Main entry point for the local CSF GUI application.
"""

import sys
from pathlib import Path

# Launch the GUI application
from app.ui.main_window import main

if __name__ == '__main__':
    main()
