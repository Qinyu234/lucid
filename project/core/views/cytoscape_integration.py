"""
Cytoscape.js Integration for Lucid
Based on ARCHITECTURE.html specification
Layer 5: View - Interactive graph visualization using Cytoscape.js

This module provides a wrapper for Cytoscape.js integration.
Cytoscape.js is a JavaScript library for graph theory visualization.

Installation:
1. Install Node.js: https://nodejs.org/
2. Create a web interface for the visualization
3. Install Cytoscape.js: npm install cytoscape
4. Use this module to generate graph data for Cytoscape.js

Note: This is a stub implementation. Full integration requires:
- Web interface (HTML/CSS/JavaScript)
- Cytoscape.js library
- Graph data serialization
- WebSocket or HTTP API for communication
"""

from typing import Dict, Any, List, Optional
import json

class CytoscapeIntegration:
    """
    Cytoscape.js integration wrapper.
    Provides graph data generation for Cytoscape.js visualization.
    """
    
    def __init__(self):
        """
        Initialize Cytoscape.js integration.
        """
        self.available = self._check_cytoscape_available()
    
    def _check_cytoscape_available(self) -> bool:
        """
        Check if Cytoscape.js web interface is available.
        
        Returns:
            True if Cytoscape.js interface is available, False otherwise
        """
        # This would check if the web interface is running
        # For now, return False as it requires a web server
        return False
    
    def graph_to_cytoscape_format(self, graph: Any) -> Dict[str, Any]:
        """
        Convert Lucid graph to Cytoscape.js format.
        
        Args:
            graph: Lucid CodeGraph object
            
        Returns:
            Dictionary in Cytoscape.js format (elements: nodes, edges)
        """
        elements = {
            'nodes': [],
            'edges': []
        }
        
        # Convert nodes
        # This would iterate through graph nodes and convert to Cytoscape format
        # For now, return empty structure
        
        return {
            'elements': elements,
            'style': self._get_default_style(),
            'layout': self._get_default_layout()
        }
    
    def _get_default_style(self) -> Dict[str, Any]:
        """
        Get default Cytoscape.js style configuration.
        
        Returns:
            Dictionary containing style configuration
        """
        return {
            'width': '800px',
            'height': '600px',
            'background-color': '#f5f5f5'
        }
    
    def _get_default_layout(self) -> Dict[str, Any]:
        """
        Get default Cytoscape.js layout configuration.
        
        Returns:
            Dictionary containing layout configuration
        """
        return {
            'name': 'cose',
            'animate': True,
            'animationDuration': 1000
        }
    
    def generate_html_viewer(self, graph_data: Dict[str, Any]) -> str:
        """
        Generate HTML viewer for Cytoscape.js graph.
        
        Args:
            graph_data: Graph data in Cytoscape.js format
            
        Returns:
            HTML string containing the viewer
        """
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Lucid Graph Viewer</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.23.0/cytoscape.min.js"></script>
    <style>
        #cy {{
            width: 100%;
            height: 100%;
            position: absolute;
            left: 0;
            top: 0;
        }}
    </style>
</head>
<body>
    <div id="cy"></div>
    <script>
        var cy = cytoscape({{
            container: document.getElementById('cy'),
            elements: {elements},
            style: [
                {{
                    selector: 'node',
                    style: {{
                        'background-color': '#666',
                        'label': 'data(id)'
                    }}
                }},
                {{
                    selector: 'edge',
                    style: {{
                        'width': 3,
                        'line-color': '#ccc',
                        'target-arrow-color': '#ccc',
                        'target-arrow-shape': 'triangle'
                    }}
                }}
            ],
            layout: {{
                name: 'cose',
                animate: true
            }}
        }});

        // Hover event handlers for file graph linkage
        cy.on('mouseover', 'node', function(evt) {{
            var node = evt.target;
            var data = node.data();
            
            // Show file location and writers/readers on hover
            console.log('Hover over node:', data.id);
            console.log('File location:', data.file_location);
            console.log('Writers:', data.writers);
            console.log('Readers:', data.readers);
            
            // Display tooltip with hover information
            var tooltip = document.getElementById('tooltip');
            if (!tooltip) {{
                tooltip = document.createElement('div');
                tooltip.id = 'tooltip';
                tooltip.style.position = 'absolute';
                tooltip.style.background = 'white';
                tooltip.style.border = '1px solid #ccc';
                tooltip.style.padding = '10px';
                tooltip.style.borderRadius = '5px';
                tooltip.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
                tooltip.style.zIndex = '1000';
                document.body.appendChild(tooltip);
            }}
            
            tooltip.innerHTML = `
                <strong>${{data.id}}</strong><br>
                Location: ${{data.file_location || 'N/A'}}<br>
                Writers: ${{(data.writers || []).join(', ') || 'N/A'}}<br>
                Readers: ${{(data.readers || []).join(', ') || 'N/A'}}
            `;
            tooltip.style.left = evt.renderedPosition.x + 'px';
            tooltip.style.top = evt.renderedPosition.y + 'px';
            tooltip.style.display = 'block';
        }});

        cy.on('mouseout', 'node', function(evt) {{
            var tooltip = document.getElementById('tooltip');
            if (tooltip) {{
                tooltip.style.display = 'none';
            }}
        }});

        // Click event for navigation to file location
        cy.on('tap', 'node', function(evt) {{
            var node = evt.target;
            var data = node.data();
            
            console.log('Clicked node:', data.id);
            console.log('Navigating to:', data.file_location);
            
            // In a real VSCode extension, this would navigate to the file
            // For now, just log the navigation
            if (data.file_location) {{
                alert('Navigate to: ' + data.file_location);
            }}
        }});
    </script>
</body>
</html>
        """.format(elements=json.dumps(graph_data.get('elements', {})))
        
        return html
    
    def export_graph_json(self, graph: Any, output_path: str) -> bool:
        """
        Export graph to JSON for Cytoscape.js.
        
        Args:
            graph: Lucid CodeGraph object
            output_path: Path to save the JSON file
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            graph_data = self.graph_to_cytoscape_format(graph)
            with open(output_path, 'w') as f:
                json.dump(graph_data, f, indent=2)
            print(f"Graph exported to {output_path}")
            return True
        except Exception as e:
            print(f"Error exporting graph: {e}")
            return False


def install_cytoscape_instructions() -> str:
    """
    Get instructions for setting up Cytoscape.js.
    
    Returns:
        Setup instructions as string
    """
    return """
Cytoscape.js Setup Instructions:

1. Install Node.js:
   - Download from: https://nodejs.org/

2. Create a web project:
   mkdir lucid-visualization
   cd lucid-visualization
   npm init -y

3. Install Cytoscape.js:
   npm install cytoscape

4. Create an HTML file with Cytoscape.js integration
5. Use the CytoscapeIntegration class to generate graph data
6. Load the graph data in your HTML file

For more information, see: https://js.cytoscape.org/
"""


if __name__ == "__main__":
    # Test Cytoscape.js integration
    print("Cytoscape.js integration requires a web interface.")
    print(install_cytoscape_instructions())
