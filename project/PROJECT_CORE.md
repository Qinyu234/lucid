# PROJECT CORE

## Lucid Architecture

Lucid is a code clarity tool that extracts the implicit access structure of every piece of state — who writes it, who reads it — and makes it explicitly queryable.

### Architecture Layers

```
Code → Ingestion → Graph → Analysis → Virtual Layer → Views → Generation (Phase 3)
```

### Layer Descriptions

**1. Ingestion Layer** (`core/ingestion/`)
- Parses source code files
- Supports multiple languages (Python, JavaScript, TypeScript, Go, Rust, Java, C/C++)
- Uses tree-sitter for accurate parsing
- Extracts functions, classes, variables, imports
- Entry point: `parse_file(file_path)`

**2. Graph Layer** (`core/graph/`)
- Builds code structure representation
- Creates nodes for functions, classes, variables
- Tracks relationships between nodes
- Entry point: `build_code_graph(parsed_data)`

**3. Analysis Layer** (`core/analysis/`)
- Extracts Access Contracts for each piece of state
- Tracks write sites (where variables are assigned)
- Tracks use sites (where variables are read)
- Performs def-use analysis
- Entry point: `extract_access_contracts(graph, source_code)`

**4. Virtual Layer** (`core/virtual_layer/`)
- Provides a projection layer over real code
- Enables safe editing without touching original files
- Supports diff/patch operations
- Auto-regenerates when real files change externally
- Entry point: `VirtualFileSystem`

**5. Views Layer** (`core/views/`)
- Provides different perspectives on code
- **Def-Use Contract View** (MVP): Shows where variables are assigned and read
- **Structure View**: Shows overall code structure
- Entry points: `DefUseView`, `StructureView`

### Core Concepts

**Access Contract** — for every piece of state:
```json
{
  "cartTotal": {
    "defined": "CartService.ts:12",
    "write_sites": ["CartService.addItem:L34", "CartService.removeItem:L89"],
    "use_sites": ["CartSummary.tsx:L45", "CheckoutButton.tsx:L67"],
    "source": "inferred"
  }
}
```

**Virtual Files** — a projection layer over the real code. Edit here; the tool diffs and patches back. If the real files change externally, the virtual layer regenerates automatically.

### Phase 1 Status

Phase 1 is in progress — single file parsing, writers/readers extraction, interactive graph view.

### CLI Usage

```bash
# Analyze a file and extract access contracts
python project/cli.py analyze source.py

# Show access contract for a specific variable
python project/cli.py analyze source.py --variable cartTotal

# Show summary of all access contracts
python project/cli.py analyze source.py --summary

# Show code structure
python project/cli.py structure source.py

# Create virtual file system
python project/cli.py virtual source.py
```

### Dependencies

- tree-sitter: Parser for multiple languages
- tree-sitter-languages: Language grammars
- pytest: Testing framework
- PyQt6: GUI framework
- PyInstaller: Package as exe
