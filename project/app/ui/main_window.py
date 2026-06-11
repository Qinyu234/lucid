"""
Main Window for CSF Application
Interactive GUI application for CSF analysis and visualization.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QTabWidget,
    QFileDialog, QSplitter, QStatusBar, QMenuBar,
    QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.sync.parser import parse
from core.expansion import expand
from core.desugar import desugar
from core.vfs import create_virtual_filesystem
from core.complexity import visualize_complexity
from core.flow import analyze_flows
from core.testing import generate_test_suite


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.current_folder = None
        self.csf = None
        self.vfs = None
        self.test_suite = None
        self.current_vfs_path = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("CSF Expansion Engine - Local App")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create toolbar
        toolbar = self.create_toolbar()
        main_layout.addLayout(toolbar)
        
        # Create tab widget for different views
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_code_tab()
        self.create_flowchart_tab()
        self.create_test_tab()
        self.create_virtual_files_tab()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_file_action = QAction("Open File", self)
        open_file_action.setShortcut(QKeySequence.StandardKey.Open)
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)
        
        open_folder_action = QAction("Open Project", self)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Analysis menu
        analysis_menu = menubar.addMenu("Analysis")
        
        desugar_action = QAction("Desugar", self)
        desugar_action.triggered.connect(self.run_desugar)
        analysis_menu.addAction(desugar_action)
        
        analyze_flows_action = QAction("Analyze Flows", self)
        analyze_flows_action.triggered.connect(self.run_analyze_flows)
        analysis_menu.addAction(analyze_flows_action)
        
        visualize_complexity_action = QAction("Visualize Complexity", self)
        visualize_complexity_action.triggered.connect(self.run_visualize_complexity)
        analysis_menu.addAction(visualize_complexity_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        generate_tests_action = QAction("Generate Tests", self)
        generate_tests_action.triggered.connect(self.run_generate_tests)
        tools_menu.addAction(generate_tests_action)
        
        create_vfs_action = QAction("Create Virtual Files", self)
        create_vfs_action.triggered.connect(self.run_create_vfs)
        tools_menu.addAction(create_vfs_action)
    
    def create_toolbar(self):
        """Create the toolbar."""
        toolbar = QHBoxLayout()
        
        # Open file button
        open_file_btn = QPushButton("Open File")
        open_file_btn.clicked.connect(self.open_file)
        toolbar.addWidget(open_file_btn)
        
        # Open folder button
        open_folder_btn = QPushButton("Open Folder")
        open_folder_btn.clicked.connect(self.open_folder)
        toolbar.addWidget(open_folder_btn)
        
        # Process button
        process_btn = QPushButton("Process All")
        process_btn.clicked.connect(self.process_all)
        toolbar.addWidget(process_btn)
        
        toolbar.addStretch()
        
        return toolbar
    
    def create_code_tab(self):
        """Create the code view tab."""
        code_tab = QWidget()
        layout = QVBoxLayout(code_tab)
        
        self.code_view = QTextEdit()
        self.code_view.setReadOnly(True)
        self.code_view.setPlaceholderText("Open a file to view code with complexity colors")
        layout.addWidget(self.code_view)
        
        self.tab_widget.addTab(code_tab, "Code View")
    
    def create_flowchart_tab(self):
        """Create the flowchart view tab."""
        flowchart_tab = QWidget()
        layout = QVBoxLayout(flowchart_tab)
        
        self.flowchart_view = QTextEdit()
        self.flowchart_view.setReadOnly(True)
        self.flowchart_view.setPlaceholderText("Flowchart visualization will appear here")
        layout.addWidget(self.flowchart_view)
        
        self.tab_widget.addTab(flowchart_tab, "Flowchart")
    
    def create_test_tab(self):
        """Create the test-driven workspace tab."""
        test_tab = QWidget()
        layout = QVBoxLayout(test_tab)
        
        self.test_view = QTextEdit()
        self.test_view.setReadOnly(True)
        self.test_view.setPlaceholderText("Generated tests will appear here")
        layout.addWidget(self.test_view)
        
        self.tab_widget.addTab(test_tab, "Tests")
    
    def create_virtual_files_tab(self):
        """Create the virtual files tab."""
        vfs_tab = QWidget()
        layout = QVBoxLayout(vfs_tab)
        
        # File selector
        file_selector_layout = QHBoxLayout()
        self.vfs_file_combo = QTabWidget()  # Using as a simple list
        file_selector_layout.addWidget(QLabel("Select File:"))
        self.vfs_file_selector = QTabWidget()
        file_selector_layout.addWidget(self.vfs_file_selector)
        layout.addLayout(file_selector_layout)
        
        # Editable text area for virtual file content
        self.vfs_view = QTextEdit()
        self.vfs_view.setReadOnly(False)
        self.vfs_view.setPlaceholderText("Select a virtual file to edit")
        self.vfs_view.textChanged.connect(self.on_vfs_content_changed)
        layout.addWidget(self.vfs_view)
        
        # Save button
        save_btn = QPushButton("Save Virtual File")
        save_btn.clicked.connect(self.save_virtual_file)
        layout.addWidget(save_btn)
        
        self.tab_widget.addTab(vfs_tab, "Virtual Files")
        
        self.current_vfs_path = None
    
    def open_file(self):
        """Open a file dialog to select a source file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Python File",
            "",
            "Python Files (*.py);;All Files (*)"
        )
        
        if file_path:
            # Verify file exists
            if not Path(file_path).exists():
                self.status_bar.showMessage(f"Error: File not found: {file_path}")
                return
            
            self.current_file = file_path
            self.status_bar.showMessage(f"Opened: {file_path}")
            
            # Load and display the file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.code_view.setText(content)
            except Exception as e:
                self.status_bar.showMessage(f"Error reading file: {str(e)}")
    
    def open_folder(self):
        """Open a folder dialog to select a source folder (document/project)."""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Project Folder",
            ""
        )
        
        if folder_path:
            # Verify folder exists
            if not Path(folder_path).exists():
                self.status_bar.showMessage(f"Error: Folder not found: {folder_path}")
                return
            
            self.current_folder = folder_path
            self.status_bar.showMessage(f"Opened project: {folder_path}")
            
            # List all files in the folder (document view)
            self.display_folder_contents(folder_path)
    
    def display_folder_contents(self, folder_path: str):
        """Display contents of a folder as a document view."""
        path = Path(folder_path)
        content = f"Project: {folder_path}\n"
        content += "=" * 60 + "\n\n"
        
        # List all files recursively
        all_files = sorted(path.rglob("*"))
        
        # Group by file type
        py_files = []
        other_files = []
        
        for file_path in all_files:
            if file_path.is_file():
                if file_path.suffix == '.py':
                    py_files.append(file_path)
                else:
                    other_files.append(file_path)
        
        # Display Python files
        if py_files:
            content += "Python Files:\n"
            for py_file in py_files:
                rel_path = py_file.relative_to(path)
                content += f"  - {rel_path}\n"
            content += "\n"
        
        # Display other files
        if other_files:
            content += "Other Files:\n"
            for other_file in other_files:
                rel_path = other_file.relative_to(path)
                content += f"  - {rel_path}\n"
            content += "\n"
        
        content += f"\nTotal: {len(py_files)} Python files, {len(other_files)} other files"
        
        self.code_view.setText(content)
    
    def process_all(self):
        """Run the complete processing pipeline."""
        if not self.current_file:
            self.status_bar.showMessage("No file selected")
            return
        
        self.status_bar.showMessage("Processing...")
        
        try:
            # Step 1: Parse and expand
            self.csf = expand(self.current_file)
            self.status_bar.showMessage(f"Parsed {len(self.csf['nodes'])} nodes")
            
            # Step 2: Desugar
            self.csf = desugar(self.csf)
            self.status_bar.showMessage("Desugared classes to functions")
            
            # Step 3: Analyze flows
            self.csf = analyze_flows(self.csf)
            self.status_bar.showMessage("Analyzed flows")
            
            # Step 4: Generate tests (required for complexity visualization)
            self.test_suite = generate_test_suite(self.csf)
            total_tests = (
                len(self.test_suite['unit_tests']) +
                len(self.test_suite['integration_tests']) +
                len(self.test_suite['state_transition_tests']) +
                len(self.test_suite['edge_case_tests'])
            )
            self.status_bar.showMessage(f"Generated {total_tests} tests")
            
            # Step 5: Visualize complexity (based on test tightness and operational complexity)
            self.csf = visualize_complexity(self.csf, self.test_suite)
            self.status_bar.showMessage("Visualized complexity based on test coverage")
            
            # Step 6: Create virtual file system
            self.vfs = create_virtual_filesystem(self.csf)
            self.status_bar.showMessage(f"Created {len(self.vfs.get_all_files())} virtual files")
            
            # Update views
            self.update_code_view()
            self.update_flowchart_view()
            self.update_test_view()
            self.update_vfs_view()
            
            self.status_bar.showMessage("Processing complete")
            
        except Exception as e:
            self.status_bar.showMessage(f"Error: {str(e)}")
    
    def run_desugar(self):
        """Run desugaring only."""
        if not self.current_file:
            self.status_bar.showMessage("No file selected")
            return
        
        try:
            self.csf = expand(self.current_file)
            self.csf = desugar(self.csf)
            self.update_code_view()
            self.status_bar.showMessage("Desugaring complete")
        except Exception as e:
            self.status_bar.showMessage(f"Error: {str(e)}")
    
    def run_analyze_flows(self):
        """Run flow analysis only."""
        if not self.csf:
            self.status_bar.showMessage("No CSF loaded. Process file first.")
            return
        
        try:
            self.csf = analyze_flows(self.csf)
            self.update_flowchart_view()
            self.status_bar.showMessage("Flow analysis complete")
        except Exception as e:
            self.status_bar.showMessage(f"Error: {str(e)}")
    
    def run_visualize_complexity(self):
        """Run complexity visualization only."""
        if not self.csf:
            self.status_bar.showMessage("No CSF loaded. Process file first.")
            return
        
        if not self.test_suite:
            self.status_bar.showMessage("No test suite generated. Generate tests first.")
            return
        
        try:
            self.csf = visualize_complexity(self.csf, self.test_suite)
            self.update_code_view()
            self.status_bar.showMessage("Complexity visualization complete")
        except Exception as e:
            self.status_bar.showMessage(f"Error: {str(e)}")
    
    def run_create_vfs(self):
        """Run virtual file system creation only."""
        if not self.csf:
            self.status_bar.showMessage("No CSF loaded. Process file first.")
            return
        
        try:
            self.vfs = create_virtual_filesystem(self.csf)
            self.update_vfs_view()
            self.status_bar.showMessage("Virtual file system created")
        except Exception as e:
            self.status_bar.showMessage(f"Error: {str(e)}")
    
    def update_code_view(self):
        """Update the code view with complexity colors."""
        if not self.csf:
            return
        
        # Display code with complexity indicators
        content = "Code View with Complexity Colors:\n"
        content += "=" * 60 + "\n\n"
        
        for node_id, node in self.csf['nodes'].items():
            if node['kind'] == 'function':
                color = node['meta'].get('color_indicator', 'unknown')
                complexity = node['meta'].get('complexity_score', 0.0)
                test_tightness = node['meta'].get('test_tightness', 0.0)
                operational_complexity = node['meta'].get('operational_complexity', 0.0)
                
                content += f"[{color.upper()}] {node['label']}\n"
                content += f"  Complexity: {complexity:.2f}, Test Tightness: {test_tightness:.2f}, Op Complexity: {operational_complexity:.2f}\n"
                content += "\n"
        
        self.code_view.setText(content)
    
    def update_flowchart_view(self):
        """Update the flowchart view."""
        if not self.csf:
            return
        
        from core.flow.state_visualizer import visualize_state, generate_state_graph_viz
        
        visualization = visualize_state(self.csf)
        dot_graph = generate_state_graph_viz(visualization)
        
        self.flowchart_view.setText("State Flow Graph (GraphViz DOT format):\n\n" + dot_graph)
    
    def update_test_view(self):
        """Update the test view."""
        if not self.test_suite:
            return
        
        content = "Generated Tests:\n"
        content += "=" * 60 + "\n\n"
        
        content += f"Unit Tests: {len(self.test_suite['unit_tests'])}\n"
        content += f"Integration Tests: {len(self.test_suite['integration_tests'])}\n"
        content += f"State Transition Tests: {len(self.test_suite['state_transition_tests'])}\n"
        content += f"Edge Case Tests: {len(self.test_suite['edge_case_tests'])}\n\n"
        
        for test in self.test_suite['unit_tests'][:5]:  # Show first 5
            content += f"- {test['name']}: {test['description']}\n"
        
        if len(self.test_suite['unit_tests']) > 5:
            content += f"... and {len(self.test_suite['unit_tests']) - 5} more\n"
        
        self.test_view.setText(content)
    
    def update_vfs_view(self):
        """Update the virtual files view with editable interface."""
        if not self.vfs:
            return
        
        # Clear existing tabs
        while self.vfs_file_selector.count() > 0:
            self.vfs_file_selector.removeTab(0)
        
        # Add each virtual file as a selectable option
        files = self.vfs.get_all_files()
        for path, virtual_file in files.items():
            # Use relative path for display
            relative_path = path.replace(self.vfs.root_path + '/', '')
            self.vfs_file_selector.addTab(QWidget(), relative_path)
        
        # If there are files, select the first one
        if files:
            self.vfs_file_selector.setCurrentIndex(0)
            self.load_virtual_file(list(files.keys())[0])
        
        self.vfs_file_selector.currentChanged.connect(self.on_vfs_file_selected)
    
    def on_vfs_file_selected(self, index):
        """Handle virtual file selection."""
        if index < 0:
            return
        
        files = self.vfs.get_all_files()
        if index < len(files):
            path = list(files.keys())[index]
            self.load_virtual_file(path)
    
    def load_virtual_file(self, path: str):
        """Load a virtual file into the editor."""
        virtual_file = self.vfs.get_file(path.replace(self.vfs.root_path + '/', ''))
        if virtual_file:
            self.current_vfs_path = path.replace(self.vfs.root_path + '/', '')
            self.vfs_view.setText(virtual_file.content)
            self.status_bar.showMessage(f"Loaded: {self.current_vfs_path}")
    
    def on_vfs_content_changed(self):
        """Handle content changes in the virtual file editor."""
        if self.current_vfs_path:
            self.status_bar.showMessage(f"Editing: {self.current_vfs_path} (unsaved)")
    
    def save_virtual_file(self):
        """Save the current virtual file."""
        if not self.current_vfs_path or not self.vfs:
            self.status_bar.showMessage("No file selected to save")
            return
        
        new_content = self.vfs_view.toPlainText()
        success = self.vfs.update_file(self.current_vfs_path, new_content)
        
        if success:
            self.status_bar.showMessage(f"Saved: {self.current_vfs_path}")
        else:
            self.status_bar.showMessage(f"Failed to save: {self.current_vfs_path}")


def main():
    """Main entry point for the GUI application."""
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
