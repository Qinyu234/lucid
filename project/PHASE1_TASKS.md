# Phase 1 (MVP) Verifiable Task-Based Goals

Based on ARCHITECTURE.html specification (lines 952-966)

## Phase 1 MVP Requirements

**Goal:** 单文件解析 → 访问契约 JSON → 新窗口图形化展示
**Delivery Standard (交付标准):** 悬停一个变量，能看到它的 writers 和 readers
**Technology:**
- Tree-sitter 解析
- def-use chain 推断（基于 Joern CPG，不需要自己写扫描逻辑）
- 独立窗口 + zoom 图

## Existing Technologies to Use (Don't Implement from Scratch)

ARCHITECTURE explicitly recommends using these existing tools instead of implementing from scratch:

### Layer 1: Ingestion
- **Tree-sitter** - Cross-language parser (use existing library)

### Layer 3: Analysis
- **Joern CPG** - Def-use chain inference (ARCHITECTURE explicitly says "不需要自己写扫描逻辑")
- Use Joern for def-use chain inference, don't write custom scanning logic

### Layer 5: View
- **Cytoscape.js** - Graph visualization (use existing library)

## Custom Implementation Required (Not provided by existing tools)

### Layer 3: Analysis
- **Access contract extraction** - Custom logic to extract writers/readers from Joern CPG results
- **Explicit contract violation detection** - Custom logic
- **Impact analysis** - Custom logic

### Layer 5: View
- **hover → file graph linkage** - Custom logic

## Phase 1 MVP Tasks

### Task 1.1: Integrate Tree-sitter parser (单文件解析)
**Goal:** Integrate Tree-sitter for single file AST parsing
**Acceptance Criteria:**
- [ ] Tree-sitter library installed and configured
- [ ] Tree-sitter successfully parses single Python files
- [ ] Tree-sitter successfully parses single JavaScript files
- [ ] AST output is accessible and queryable
- [ ] Parser handles syntax errors gracefully
- **Verification:** Unit tests for Tree-sitter integration with sample code files

### Task 1.2: Integrate Joern CPG for def-use chain inference (def-use chain 推断)
**Goal:** Use Joern CPG for def-use chain inference per ARCHITECTURE (不需要自己写扫描逻辑)
**Acceptance Criteria:**
- [ ] Joern integration stub created
- [ ] Fallback to custom logic if Joern unavailable
- [ ] Def-use chain inference works for single files
- [ ] Writers and readers are correctly identified
- **Verification:** Test def-use chain inference on sample files

### Task 1.3: Extract access contracts from Joern CPG results (访问契约 JSON)
**Goal:** Extract access contracts (writers/readers) from Joern CPG results
**Acceptance Criteria:**
- [ ] Access contract data structure defined
- [ ] Extract writers for each variable
- [ ] Extract readers for each variable
- [ ] Output access contracts as JSON
- [ ] Include file locations for writers/readers
- **Verification:** Test access contract extraction on sample files

### Task 1.4: Integrate Cytoscape.js for visualization (新窗口图形化展示)
**Goal:** Implement Cytoscape.js for graph visualization in new window
**Acceptance Criteria:**
- [ ] Cytoscape.js library integrated (via CDN)
- [ ] Cytoscape.js successfully renders graphs
- [ ] Support zoom functionality (zoom 图)
- [ ] Support pan functionality
- [ ] Display graph nodes with proper styling
- [ ] Display graph edges with proper styling
- **Verification:** Test Cytoscape.js rendering with sample graphs

### Task 1.5: Implement hover to show writers and readers (交付标准: 悬停一个变量，能看到它的 writers 和 readers)
**Goal:** Implement hover functionality to show writers and readers
**Acceptance Criteria:**
- [ ] Hover over variable node shows writers
- [ ] Hover over variable node shows readers
- [ ] Hover shows file locations
- [ ] Hover information is accurate
- [ ] Hover performance is acceptable
- **Verification:** Test hover functionality on sample graphs

## Testing & Verification

### Task 2.1: Write tests for Phase 1 MVP
**Goal:** Comprehensive test coverage for Phase 1 MVP
**Acceptance Criteria:**
- [ ] Unit tests for Tree-sitter integration
- [ ] Unit tests for Joern CPG integration
- [ ] Unit tests for access contract extraction
- [ ] Unit tests for Cytoscape.js visualization
- [ ] Unit tests for hover functionality
- [ ] Integration tests for end-to-end workflow
- **Verification:** All tests pass

### Task 2.2: Verify delivery standard (悬停一个变量，能看到它的 writers 和 readers)
**Goal:** Verify the delivery standard is met
**Acceptance Criteria:**
- [ ] Single file parsing works
- [ ] Access contract JSON is generated
- [ ] New window opens with graph
- [ ] Hover over variable shows writers
- [ ] Hover over variable shows readers
- [ ] Zoom functionality works
- **Verification:** Manual testing with sample file

## Summary

Total Tasks: 7
Estimated Time: 20-30 hours

**Phase 1 MVP is complete when:**
- All 7 tasks are completed
- Delivery standard is met: 悬停一个变量，能看到它的 writers 和 readers
- All tests pass
- The implementation matches ARCHITECTURE.html Phase 1 specification
