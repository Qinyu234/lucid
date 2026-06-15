# Lucid User Manual

## Overview

Lucid is a code analysis tool that helps you understand code structure, access patterns, and dependencies. It provides def-use contract analysis, impact analysis, and virtual file projection capabilities.

## Implementation Status

### MVP Features (Currently Available)
- **Layer 1: Ingestion** - Code → AST, symbol table, import relations
- **Layer 2: Graph** - In-memory graph with writes/reads edges
- **Layer 3: Analysis** - Access contracts, def-use chain inference, impact analysis
- **Layer 4: Virtual Layer** - Virtual file projection, diff/patch (pattern implementation)
- **Layer 5: View** - Text-based visualization
- **VIEW 01: Structure View** - Code structure overview
- **VIEW 04: Def-Use Contract View** - MVP target view

### Phase 2 Features (Not Yet Implemented)
- **Layer 3b: Runtime Trace** - Dynamic analysis with OpenTelemetry, Jaeger
- **Layer 6: Interaction** - Change preview, heatmap overlay, violation highlight
- **VIEW 02: Data Flow View** - Value transformation tracking
- **VIEW 03: Event Flow View** - Event propagation tracking
- **VIEW 05: Impact View** - Performance hotspots with runtime trace
- **Cytoscape.js Visualization** - Interactive graph visualization
- **VSCode Extension** - Full VSCode integration with FileSystemProvider
- **chokidar File Watching** - Actual file watcher integration
- **Joern CPG Integration** - Def-use chain inference using Joern
- **ts-morph Integration** - TypeScript deep analysis

### Future Features (Phase 3)
- **Layer 7: Generation** - Constrained code generation with LangGraph
- **VIEW 06: Test View** - Test coverage, contract compliance, performance monitoring

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd lucid
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
```

3. Activate the virtual environment:
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. Install dependencies:
```bash
cd project
pip install -r requirements.txt
```

## Quick Start

### Analyze a Single File

```python
from core.ingestion import parse_file
from core.graph import build_code_graph
from core.analysis import extract_access_contracts
from core.views import DefUseView, StructureView

# Parse a Python file
parsed = parse_file('path/to/your/file.py')

# Build the code graph
graph = build_code_graph(parsed)

# Extract access contracts
contracts = extract_access_contracts(graph, parsed['source_code'])

# Create views
def_use_view = DefUseView(contracts)
structure_view = StructureView(graph)

# View results
print(structure_view.render_structure())
print(def_use_view.render_summary())
```

### Command Line Usage

```bash
# Analyze a file
python -m core.cli analyze path/to/file.py

# Show structure
python -m core.cli structure path/to/file.py

# Show def-use contracts
python -m core.cli defuse path/to/file.py
```

## Core Concepts

### Layers

Lucid follows a layered architecture:

1. **Ingestion Layer**: Code → AST, symbol table, import relations
2. **Graph Layer**: In-memory graph with node and edge relationships
3. **Analysis Layer**: Graph → access contracts, def-use chains
4. **Virtual Layer**: Virtual file projection for safe editing
5. **View Layer**: Visualization of analysis results

### Node Types

- **StateNode**: Represents state with access contract (variables)
- **EventNode**: Event handlers/triggers
- **FunctionNode**: Function/method
- **ModuleNode**: Module/file
- **ExternalEffectNode**: External side effects

### Edge Types

- **defines**: Write site to state
- **uses**: Use site to state
- **triggers**: Event propagation
- **depends_on**: Module dependency
- **coupled_with**: Implicit coupling (inheritance, calls)

## API Reference

### Ingestion Layer

#### `parse_file(file_path: str) -> Dict[str, Any]`

Parse a source file and extract its structure.

**Parameters:**
- `file_path`: Path to the source file

**Returns:**
- Dictionary containing:
  - `language`: Detected programming language
  - `file_path`: Original file path
  - `source_code`: Raw source code
  - `ast`: Tree-sitter AST (if available)
  - `symbol_table`: Symbol table with definitions and scopes
  - `import_relations`: Import relations
  - `functions`: List of function definitions
  - `classes`: List of class definitions
  - `variables`: List of variable assignments
  - `imports`: List of import statements

**Example:**
```python
from core.ingestion import parse_file

parsed = parse_file('example.py')
print(f"Language: {parsed['language']}")
print(f"Functions: {len(parsed['functions'])}")
print(f"Symbol table: {parsed['symbol_table']}")
```

### Graph Layer

#### `build_code_graph(parsed_data: Dict[str, Any]) -> CodeGraph`

Build a code graph from parsed data.

**Parameters:**
- `parsed_data`: Output from `parse_file()`

**Returns:**
- `CodeGraph` object with nodes and edges

**Example:**
```python
from core.ingestion import parse_file
from core.graph import build_code_graph

parsed = parse_file('example.py')
graph = build_code_graph(parsed)

# Get all functions
functions = graph.get_functions()
for func in functions:
    print(f"Function: {func.name} at line {func.source_ref['line']}")

# Get all states (variables)
states = graph.get_states()
for state in states:
    print(f"State: {state.name}")
```

### Analysis Layer

#### `extract_access_contracts(graph: CodeGraph, source_code: str) -> Dict[str, AccessContract]`

Extract access contracts from the graph.

**Parameters:**
- `graph`: CodeGraph object
- `source_code`: Source code string

**Returns:**
- Dictionary mapping variable names to AccessContract objects

**Example:**
```python
from core.ingestion import parse_file
from core.graph import build_code_graph
from core.analysis import extract_access_contracts

parsed = parse_file('example.py')
graph = build_code_graph(parsed)
contracts = extract_access_contracts(graph, parsed['source_code'])

for var_name, contract in contracts.items():
    print(f"{var_name}:")
    print(f"  Writers: {len(contract.write_sites)}")
    print(f"  Readers: {len(contract.use_sites)}")
```

#### `check_explicit_contract_violation(contract: AccessContract, allowed_writers: List[str], allowed_readers: List[str]) -> Dict[str, Any]`

Check if an explicit contract is violated.

**Parameters:**
- `contract`: AccessContract to check
- `allowed_writers`: List of allowed writer contexts
- `allowed_readers`: List of allowed reader contexts

**Returns:**
- Violation report with violations found

**Example:**
```python
from core.analysis.access_contract import check_explicit_contract_violation

contract = contracts['my_variable']
violation = check_explicit_contract_violation(
    contract,
    allowed_writers=['ModuleA', 'ModuleB'],
    allowed_readers=['ModuleA', 'ModuleC']
)

if not violation['is_valid']:
    print("Contract violations found:")
    for v in violation['violations']:
        print(f"  - {v['message']}")
```

#### `analyze_impact(state_name: str, contracts: Dict[str, AccessContract]) -> Dict[str, Any]`

Analyze impact of changing a state variable.

**Parameters:**
- `state_name`: Name of the state being changed
- `contracts`: All access contracts

**Returns:**
- Impact analysis showing affected readers

**Example:**
```python
from core.analysis.access_contract import analyze_impact

impact = analyze_impact('my_variable', contracts)
print(f"Risk level: {impact['risk_level']}")
print(f"Affected readers: {impact['readers']}")
```

### View Layer

#### DefUseView (MVP)

View for def-use contract analysis (VIEW 04 - MVP Target).

**Methods:**
- `get_variable_info(variable_name: str)`: Get information about a variable
- `get_high_impact_variables(threshold: int = 5)`: Get variables with many readers
- `get_write_only_variables()`: Get variables written but never read
- `get_all_variables()`: Get all variable names

**Example:**
```python
from core.views import DefUseView

view = DefUseView(contracts)

# Get variable info
info = view.get_variable_info('my_variable')
print(f"Risk level: {info['risk_level']}")
print(f"Healthy: {info['is_healthy']}")

# Get high impact variables
high_impact = view.get_high_impact_variables(threshold=5)
for var in high_impact:
    print(f"{var['variable']}: {var['use_count']} uses")
```

#### StructureView (MVP)

View for code structure (VIEW 01).

**Methods:**
- `get_function_list()`: Get all functions
- `get_class_list()`: Get all classes
- `get_variable_list()`: Get all variables
- `get_module_list()`: Get all modules
- `render_structure()`: Render structure as text

**Example:**
```python
from core.views import StructureView

view = StructureView(graph)

# Get functions
functions = view.get_function_list()
for func in functions:
    print(f"{func['name']} at line {func['line']}")

# Render full structure
print(view.render_structure())
```

#### DataFlowView (Phase 2 - Stub)

View for data flow analysis (VIEW 02).

**Status:** Stub implementation, not yet functional.

#### EventFlowView (Phase 2 - Stub)

View for event flow analysis (VIEW 03).

**Status:** Stub implementation, not yet functional.

#### ImpactView (Phase 2 - Stub)

View for impact analysis and performance hotspots (VIEW 05).

**Status:** Stub implementation, not yet functional.

#### TestView (Phase 3 - Stub)

View for test coverage and contract compliance (VIEW 06 - Generation Layer input).

**Status:** Stub implementation, not yet functional.

### Virtual Layer (MVP - Pattern Implementation)

Manages virtual files for safe editing.

**Note:** Currently implements the pattern from ARCHITECTURE (VSCode FileSystemProvider API, TextDocumentContentProvider, diff engine, chokidar pattern). Actual VSCode extension and chokidar integration are Phase 2 features.

**Methods:**
- `add_file(path: str, content: str, metadata: Optional[Dict] = None)`: Add a virtual file
- `get_file(path: str)`: Get a virtual file
- `get_modified_files()`: Get paths of modified files
- `compute_all_diffs()`: Compute diffs for all modified files
- `reset_all()`: Reset all virtual files to original content

**Example:**
```python
from core.virtual_layer import VirtualFileSystem

vfs = VirtualFileSystem()

# Add a virtual file
vfs.add_file('virtual.py', source_code)

# Get the file and edit it
vfile = vfs.get_file('virtual.py')
vfile.apply_edit(new_content)

# Compute diffs
diffs = vfs.compute_all_diffs()
for path, diff in diffs.items():
    print(f"{path}:\n{diff}")
```

## Common Use Cases

### 1. Find High-Impact Variables

Identify variables that are used in many places (high risk to change):

```python
from core.ingestion import parse_file
from core.graph import build_code_graph
from core.analysis import extract_access_contracts
from core.views import DefUseView

parsed = parse_file('large_file.py')
graph = build_code_graph(parsed)
contracts = extract_access_contracts(graph, parsed['source_code'])
view = DefUseView(contracts)

high_impact = view.get_high_impact_variables(threshold=10)
print("High-impact variables (10+ readers):")
for var in high_impact:
    print(f"  {var['variable']}: {var['use_count']} uses, risk={var['risk_level']}")
```

### 2. Detect Write-Only Variables

Find variables that are written but never read (potential dead code):

```python
write_only = view.get_write_only_variables()
print("Write-only variables (potential dead code):")
for var in write_only:
    print(f"  {var}")
```

### 3. Analyze Impact Before Changes

See what will break if you modify a variable:

```python
from core.analysis.access_contract import analyze_impact

impact = analyze_impact('important_state', contracts)
print(f"Changing '{impact['state']}' will affect:")
print(f"  - {impact['total_readers']} readers")
print(f"  - Risk level: {impact['risk_level']}")
print(f"  - Affected functions: {impact['affected_functions']}")
```

### 4. Check Contract Violations

Enforce explicit access contracts:

```python
from core.analysis.access_contract import check_explicit_contract_violation

# Define allowed writers for a critical state
allowed_writers = ['AuthService', 'UserModule']
allowed_readers = ['AuthService', 'UserModule', 'Logger']

contract = contracts['user_token']
violation = check_explicit_contract_violation(
    contract,
    allowed_writers,
    allowed_readers
)

if not violation['is_valid']:
    print("SECURITY VIOLATION DETECTED!")
    for v in violation['violations']:
        print(f"  {v['message']}")
```

### 5. Explore Code Structure

Get an overview of the codebase:

```python
from core.ingestion import parse_file
from core.graph import build_code_graph
from core.views import StructureView

parsed = parse_file('module.py')
graph = build_code_graph(parsed)
view = StructureView(graph)

print(view.render_structure())
```

## Running Tests

Run the test suite to verify installation:

```bash
cd project
pytest
```

Run specific test modules:

```bash
pytest tests/test_ingestion.py
pytest tests/test_graph.py
pytest tests/test_analysis.py
pytest tests/test_virtual_layer.py
pytest tests/test_views.py
```

## Troubleshooting

### Import Errors

If you encounter import errors, make sure you're in the `project` directory:

```bash
cd project
python your_script.py
```

Or add the project directory to Python path:

```python
import sys
sys.path.append('path/to/lucid/project')
```

### Tree-sitter Not Available

If tree-sitter is not installed, the parser will fall back to regex-based parsing. For better accuracy, install tree-sitter:

```bash
pip install tree-sitter tree-sitter-languages
```

### Memory Issues with Large Files

For very large files, consider:
- Analyzing files individually instead of the entire codebase
- Using the virtual layer to work with projections
- Increasing system memory

## Architecture Reference

For detailed architecture information, see `ARCHITECTURE.html`.

### Implementation Phases

**MVP (Current):**
- Single-file analysis
- Text-based views
- Pattern implementations (not actual VSCode/chokidar integration)
- Custom def-use extraction (not Joern CPG)

**Phase 2 (Future):**
- Cross-file analysis
- Runtime trace layer
- Interactive features (change preview, heatmap, violation highlight)
- Cytoscape.js visualization
- Actual VSCode extension
- Joern CPG integration
- ts-morph integration
- chokidar file watching

**Phase 3 (Future):**
- Generation layer with LangGraph
- Test view with coverage tracking

## License

See LICENSE file for details.

## Support

For issues and questions, please refer to the project repository.
