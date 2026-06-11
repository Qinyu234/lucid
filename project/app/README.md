# Local Application

This directory contains the local GUI application interface for the CSF Expansion Engine.

## Structure

```
app/
├── main.py              # Main entry point
├── ui/
│   └── main_window.py   # PyQt6 main window
└── README.md            # This file
```

## Usage

### Running the GUI Application

```bash
python project/app/main.py
```

The GUI application provides:
- **Code View** - View code with complexity color indicators (green/yellow/red)
- **Flowchart** - Visualize state flow graphs
- **Tests** - View generated tests from flow analysis
- **Virtual Files** - Browse virtual file system created from inheritance trees

### Building the Executable

To build a standalone exe file:

```bash
# Install dependencies
pip install -r project/requirements.txt

# Build the exe
python project/build_exe.py

# The exe will be created at: project/dist/CSF_App.exe
```

## Features

### Interactive GUI
- File open dialog to select Python source files
- Menu bar with File, Analysis, and Tools menus
- Toolbar with quick access buttons
- Tabbed interface for different views
- Status bar showing current operation

### Analysis Pipeline
1. **Parse and Expand** - Parse source code and expand implicit structures
2. **Desugar** - Convert classes to functions, decompose inheritance
3. **Analyze Flows** - Analyze typeflow, stateflow, and dataflow
4. **Visualize Complexity** - Add complexity scores and color indicators
5. **Create Virtual Files** - Map inheritance trees to virtual files
6. **Generate Tests** - Auto-generate tests from flow analysis

### Color Indicators
- **Green** - High confidence, low complexity (good for AI generation)
- **Yellow** - Medium confidence, moderate complexity
- **Red** - Low confidence, high complexity (needs attention)

## Dependencies

- PyQt6 >= 6.0.0 - GUI framework
- PyInstaller >= 6.0.0 - For exe packaging
