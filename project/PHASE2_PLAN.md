# Phase 2 Implementation Plan

## Overview
Implement Phase 2 features from ARCHITECTURE.html specification.

## Implementation Order

### Step 1: Implement chokidar file watching (Layer 4) - HIGH PRIORITY
**Goal:** Replace pattern implementation with actual chokidar integration
**Dependencies:** Node.js, chokidar npm package
**Tasks:**
- Install chokidar in Node.js environment
- Create Node.js script for file watching
- Implement IPC communication between Python and Node.js
- Integrate with VirtualFileSystem
- Test file watching functionality
**Estimated Time:** 2-3 hours

### Step 2: Implement Joern CPG integration (Layer 3) - HIGH PRIORITY
**Goal:** Replace custom def-use extraction with Joern CPG
**Dependencies:** Java, Joern installation
**Tasks:**
- Install and configure Joern
- Create Joern server connection wrapper
- Implement CPG generation for projects
- Implement def-use chain queries using Joern
- Migrate analysis layer to use Joern results
- Test with sample projects
**Estimated Time:** 4-6 hours

### Step 3: Implement ts-morph integration (Layer 1) - MEDIUM PRIORITY
**Goal:** Add TypeScript deep analysis
**Dependencies:** Node.js, ts-morph npm package
**Tasks:**
- Install ts-morph
- Create TypeScript analysis script
- Implement type information extraction
- Integrate with ingestion layer
- Test with TypeScript files
**Estimated Time:** 2-3 hours

### Step 4: Implement Cytoscape.js visualization (Layer 5) - HIGH PRIORITY
**Goal:** Add interactive graph visualization
**Dependencies:** Cytoscape.js, web interface
**Tasks:**
- Create web interface with Cytoscape.js
- Implement graph data serialization
- Create WebSocket/HTTP API for communication
- Implement zoom/pan/drill-down
- Add hover → file graph linkage
**Estimated Time:** 4-5 hours

### Step 5: Implement VIEW 02 Data Flow View - MEDIUM PRIORITY
**Goal:** Track value transformations
**Dependencies:** Graph layer
**Tasks:**
- Implement data flow analysis algorithm
- Track value assignments and transformations
- Render data flow chains
- Test with sample code
**Estimated Time:** 2-3 hours

### Step 6: Implement VIEW 03 Event Flow View - MEDIUM PRIORITY
**Goal:** Track event propagation
**Dependencies:** Graph layer
**Tasks:**
- Implement event detection algorithm
- Track event handlers and dispatchers
- Render event flow chains
- Test with event-driven code
**Estimated Time:** 2-3 hours

### Step 7: Implement VIEW 05 Impact View - MEDIUM PRIORITY
**Goal:** Show impact and performance hotspots
**Dependencies:** Runtime Trace Layer (Step 9)
**Tasks:**
- Implement impact analysis visualization
- Integrate with runtime trace data
- Create heatmap overlay
- Show performance hotspots
**Estimated Time:** 3-4 hours

### Step 8: Implement Layer 6 Interaction features - MEDIUM PRIORITY
**Goal:** Add interactive UI features
**Dependencies:** VSCode extension, Cytoscape.js
**Tasks:**
- Implement change preview
- Implement heatmap overlay
- Implement violation highlight
- Implement incremental graph update
**Estimated Time:** 3-4 hours

### Step 9: Implement Layer 3b Runtime Trace - LOW PRIORITY
**Goal:** Add dynamic analysis
**Dependencies:** OpenTelemetry, Jaeger
**Tasks:**
- Integrate OpenTelemetry
- Implement React Profiler API integration
- Set up Jaeger backend
- Implement Redux DevTools integration
- Overlay trace data on graph
**Estimated Time:** 6-8 hours

### Step 10: Complete VSCode extension integration - HIGH PRIORITY
**Goal:** Create full VSCode extension
**Dependencies:** TypeScript, VSCode Extension API
**Tasks:**
- Complete FileSystemProvider implementation
- Complete TextDocumentContentProvider implementation
- Integrate with VSCode diff engine
- Add webview panel with Cytoscape.js
- Package and test extension
**Estimated Time:** 5-6 hours

## Total Estimated Time: 30-40 hours

## Notes
- Steps can be implemented in parallel where dependencies allow
- Steps 1, 2, 4, 10 are high priority and should be done first
- Steps 5, 6, 7, 8 are medium priority
- Step 9 is low priority and can be done last
