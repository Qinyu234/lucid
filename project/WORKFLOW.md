# Phase 1 (MVP) Implementation Workflow

Based on ARCHITECTURE.html specification

## Workflow Overview

This workflow documents the step-by-step process for implementing Phase 1 (MVP) of Lucid. Phase 2 will build upon this workflow framework.

## Prerequisites

### Environment Setup
1. **Python Environment**: Python 3.8+
2. **Node.js Environment**: Node.js 16+ (for ts-morph, chokidar)
3. **Java Environment**: Java 11+ (for Joern CPG)
4. **VSCode**: For extension development

### Tool Installation
```bash
# Python dependencies
pip install tree-sitter
pip install pytest

# Node.js dependencies (in separate directory)
npm install ts-morph
npm install chokidar
npm install cytoscape

# Joern CPG (separate installation)
# Download from https://joern.io/
```

## Phase 1 Workflow Steps

### Step 1: Environment Verification (1 hour)
**Goal:** Ensure all required tools are installed and accessible

**Tasks:**
- [ ] Verify Python 3.8+ is installed
- [ ] Verify Node.js 16+ is installed
- [ ] Verify Java 11+ is installed
- [ ] Install Tree-sitter Python library
- [ ] Install ts-morph Node.js library
- [ ] Install chokidar Node.js library
- [ ] Install Cytoscape.js Node.js library
- [ ] Install and configure Joern CPG
- [ ] Verify VSCode is available for extension development

**Verification:** Run tool version checks and test installations

---

### Step 2: Layer 1 - Ingestion (4-6 hours)
**Goal:** Implement code ingestion with AST, symbol table, and import relations

**Sub-steps:**

#### 2.1: Tree-sitter Integration (2 hours)
- [ ] Install Tree-sitter language grammars
- [ ] Create parser wrapper for Python
- [ ] Create parser wrapper for JavaScript
- [ ] Create parser wrapper for TypeScript
- [ ] Implement AST output format
- [ ] Add error handling for syntax errors
- [ ] Write unit tests for parser

#### 2.2: Symbol Table Extraction (1 hour)
- [ ] Implement AST traversal for symbol extraction
- [ ] Track function definitions with scopes
- [ ] Track class definitions with scopes
- [ ] Track variable definitions with scopes
- [ ] Add line number tracking
- [ ] Write unit tests for symbol table

#### 2.3: Import Relations Extraction (1 hour)
- [ ] Implement import statement detection
- [ ] Build module dependency graph
- [ ] Track import sources and destinations
- [ ] Handle relative imports
- [ ] Handle wildcard imports
- [ ] Write unit tests for import extraction

#### 2.4: ts-morph Integration (2 hours)
- [ ] Set up Node.js environment for ts-morph
- [ ] Create TypeScript parser wrapper
- [ ] Extract type information
- [ ] Extract interface definitions
- [ ] Integrate with symbol table
- [ ] Write unit tests for ts-morph integration

**Verification:** Run ingestion tests on sample Python, JavaScript, and TypeScript files

---

### Step 3: Layer 2 - Graph (2-3 hours)
**Goal:** Implement in-memory graph with proper edge types

**Sub-steps:**

#### 3.1: Graph Data Structure (1 hour)
- [ ] Define node types (StateNode, EventNode, ModuleNode, FunctionNode, ExternalEffectNode)
- [ ] Define edge types (defines, uses, triggers, depends_on, coupled_with)
- [ ] Implement in-memory graph storage
- [ ] Implement graph traversal
- [ ] Implement graph querying by node type
- [ ] Implement graph querying by edge type
- [ ] Write unit tests for graph operations

#### 3.2: Graph Builder (1-2 hours)
- [ ] Implement graph builder from AST
- [ ] Create nodes for functions
- [ ] Create nodes for classes (mapped to modules)
- [ ] Create nodes for variables (mapped to states)
- [ ] Create edges for writes (defines)
- [ ] Create edges for reads (uses)
- [ ] Create edges for other relationships
- [ ] Write unit tests for graph builder

**Verification:** Run graph tests on sample code files

---

### Step 4: Layer 3 - Analysis (6-8 hours)
**Goal:** Implement analysis layer with Joern CPG, contract detection, and impact analysis

**Sub-steps:**

#### 4.1: Joern CPG Integration (4-5 hours)
- [ ] Install and configure Joern
- [ ] Start Joern server
- [ ] Create Joern connection wrapper
- [ ] Implement CPG generation for Python
- [ ] Implement CPG generation for JavaScript/TypeScript
- [ ] Write def-use chain queries
- [ ] Implement query result parsing
- [ ] Add fallback to custom logic
- [ ] Write integration tests for Joern

#### 4.2: Contract Violation Detection (1-2 hours)
- [ ] Define access contract structure
- [ ] Implement contract storage
- [ ] Track writers for each state
- [ ] Track readers for each state
- [ ] Implement violation detection logic
- [ ] Add manual contract override support
- [ ] Write unit tests for contract detection

#### 4.3: Impact Analysis (1 hour)
- [ ] Implement risk level calculation
- [ ] Identify affected readers
- [ ] Identify affected writers
- [ ] Generate impact summary
- [ ] Add change preview support
- [ ] Write unit tests for impact analysis

**Verification:** Run analysis tests on sample code with intentional violations

---

### Step 5: Layer 4 - Virtual Layer (4-6 hours)
**Goal:** Implement virtual layer with VSCode API patterns and chokidar

**Sub-steps:**

#### 5.1: VSCode FileSystemProvider Pattern (1-2 hours)
- [ ] Implement FileSystemProvider interface
- [ ] Implement file reading
- [ ] Implement file writing
- [ ] Implement file creation
- [ ] Implement file deletion
- [ ] Implement directory listing
- [ ] Write unit tests with mock VSCode API

#### 5.2: TextDocumentContentProvider Pattern (1 hour)
- [ ] Implement TextDocumentContentProvider interface
- [ ] Implement virtual file content provision
- [ ] Implement content updates
- [ ] Implement change notifications
- [ ] Write unit tests with mock VSCode API

#### 5.3: VSCode Diff Engine Pattern (1 hour)
- [ ] Integrate VSCode diff engine
- [ ] Implement diff computation
- [ ] Implement patch application
- [ ] Handle merge conflicts
- [ ] Write unit tests for diff/patch

#### 5.4: chokidar Integration (1-2 hours)
- [ ] Install chokidar Node.js library
- [ ] Create file watcher wrapper
- [ ] Implement directory watching
- [ ] Detect file additions
- [ ] Detect file modifications
- [ ] Detect file deletions
- [ ] Trigger virtual layer regeneration
- [ ] Write integration tests for chokidar

**Verification:** Test virtual layer with mock VSCode API and file changes

---

### Step 6: Layer 5 - View (4-6 hours)
**Goal:** Implement view layer with Cytoscape.js and VSCode Webview Panel

**Sub-steps:**

#### 6.1: Cytoscape.js Integration (2-3 hours)
- [ ] Install Cytoscape.js library
- [ ] Create graph data serialization
- [ ] Implement Cytoscape.js rendering
- [ ] Implement zoom functionality
- [ ] Implement pan functionality
- [ ] Implement drill-down into nodes
- [ ] Style graph nodes and edges
- [ ] Write unit tests for Cytoscape.js

#### 6.2: VSCode Webview Panel (1-2 hours)
- [ ] Implement Webview Panel
- [ ] Display Cytoscape.js visualization
- [ ] Implement interactivity
- [ ] Implement extension communication
- [ ] Handle resize events
- [ ] Write unit tests with mock VSCode API

#### 6.3: Hover File Graph Linkage (1 hour)
- [ ] Implement hover detection
- [ ] Show file location on hover
- [ ] Show writers/readers on hover
- [ ] Implement click navigation
- [ ] Ensure hover performance
- [ ] Write unit tests for hover functionality

**Verification:** Test view layer with sample graphs

---

### Step 7: VIEW 01 - Structure View (1-2 hours)
**Goal:** Implement Structure View with AST + module graph

**Sub-steps:**
- [ ] Implement AST structure display
- [ ] Implement module graph display
- [ ] Add zoom functionality
- [ ] Show functions, classes, variables
- [ ] Show module relationships
- [ ] Write unit tests for Structure View

**Verification:** Test Structure View on sample code

---

### Step 8: VIEW 04 - Def-Use Contract View (2-3 hours)
**Goal:** Implement Def-Use Contract View (MVP target)

**Sub-steps:**
- [ ] Display state nodes
- [ ] Display writers in red
- [ ] Display readers in green
- [ ] Show file locations on hover
- [ ] Highlight violations
- [ ] Display risk level
- [ ] Display contract health status
- [ ] Write unit tests for Def-Use Contract View

**Verification:** Test Def-Use Contract View on sample code with violations

---

### Step 9: Testing & Verification (2-3 hours)
**Goal:** Comprehensive testing of all Phase 1 components

**Sub-steps:**
- [ ] Write unit tests for Layer 1 (Ingestion)
- [ ] Write unit tests for Layer 2 (Graph)
- [ ] Write unit tests for Layer 3 (Analysis)
- [ ] Write unit tests for Layer 4 (Virtual Layer)
- [ ] Write unit tests for Layer 5 (View)
- [ ] Write unit tests for VIEW 01
- [ ] Write unit tests for VIEW 04
- [ ] Write integration tests for end-to-end workflows
- [ ] Run all tests
- [ ] Verify test coverage > 80%
- [ ] Fix any failing tests

**Verification:** All tests pass with >80% coverage

---

## Phase 2 Workflow (Future)

Phase 2 will build upon this workflow framework by adding:

### Additional Layers
- Layer 3b: Runtime Trace (OpenTelemetry, Jaeger, React Profiler API, Redux DevTools)
- Layer 6: Interaction (change preview, heatmap overlay, violation highlight, incremental graph update)

### Additional Views
- VIEW 02: Data Flow View
- VIEW 03: Event Flow View
- VIEW 05: Impact View
- VIEW 06: Test View (Generation Layer input)

### Enhanced Features
- Cross-file analysis
- Interactive features
- Performance monitoring
- Test coverage tracking

## Workflow Principles

1. **Use Existing Tools**: Always use ARCHITECTURE-recommended tools (Tree-sitter, Joern CPG, Cytoscape.js, VSCode API, chokidar, ts-morph) instead of implementing from scratch
2. **Custom Implementation Only**: Implement custom logic only where existing tools don't provide the functionality (contract violation detection, impact analysis, hover linkage)
3. **Test-Driven**: Write tests for each component as it's implemented
4. **Incremental**: Complete each step before moving to the next
5. **Verifiable**: Each step has clear acceptance criteria and verification methods

## Estimated Total Time

Phase 1: 25-35 hours
- Step 1 (Environment): 1 hour
- Step 2 (Ingestion): 4-6 hours
- Step 3 (Graph): 2-3 hours
- Step 4 (Analysis): 6-8 hours
- Step 5 (Virtual Layer): 4-6 hours
- Step 6 (View): 4-6 hours
- Step 7 (VIEW 01): 1-2 hours
- Step 8 (VIEW 04): 2-3 hours
- Step 9 (Testing): 2-3 hours

## Success Criteria

Phase 1 is complete when:
- All 9 workflow steps are completed
- All acceptance criteria are met
- All tests pass with >80% coverage
- The implementation matches ARCHITECTURE.html specification
- All ARCHITECTURE-recommended tools are integrated
- Custom implementations are only where existing tools don't provide functionality
