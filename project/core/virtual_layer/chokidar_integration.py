"""
chokidar Integration for Lucid
Based on ARCHITECTURE.html specification
Layer 4: Virtual Layer - File watching using chokidar

This module provides a wrapper for chokidar integration.
chokidar is a Node.js file watcher library.

Installation:
1. Install Node.js: https://nodejs.org/
2. Install chokidar: npm install chokidar
3. Use this module to watch file changes

Note: This is a stub implementation. Full integration requires:
- Node.js environment
- chokidar library installation
- WebSocket or IPC for communication between Python and Node.js
"""

from typing import Dict, Any, List, Optional, Callable
import subprocess
import json
import threading
import time

class ChokidarIntegration:
    """
    chokidar integration wrapper.
    Provides file watching capabilities using chokidar.
    """
    
    def __init__(self):
        """
        Initialize chokidar integration.
        """
        self.available = self._check_chokidar_available()
        self.watcher_process = None
        self.callbacks = {
            'add': [],
            'change': [],
            'unlink': []
        }
    
    def _check_chokidar_available(self) -> bool:
        """
        Check if chokidar is available.
        
        Returns:
            True if chokidar is available, False otherwise
        """
        try:
            # Try to check if Node.js is installed
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode != 0:
                return False
            
            # Check if chokidar is installed
            # This would typically check package.json or node_modules
            return False
        except Exception:
            return False
    
    def watch_directory(self, directory_path: str) -> bool:
        """
        Watch a directory for file changes using chokidar.
        
        Args:
            directory_path: Path to the directory to watch
            
        Returns:
            True if watching started successfully, False otherwise
        """
        if not self.available:
            print("chokidar not available. Using fallback implementation.")
            return self._fallback_watch(directory_path)
        
        try:
            # Placeholder for actual chokidar watcher
            # Actual implementation would start a Node.js process with chokidar
            print(f"Starting chokidar watcher for {directory_path}...")
            return True
        except Exception as e:
            print(f"Error starting chokidar: {e}")
            return self._fallback_watch(directory_path)
    
    def _fallback_watch(self, directory_path: str) -> bool:
        """
        Fallback file watching when chokidar is not available.
        Uses Python's watchdog library or polling.
        
        Args:
            directory_path: Path to the directory to watch
            
        Returns:
            True if watching started successfully, False otherwise
        """
        try:
            # Try to use Python's watchdog library
            import watchdog.observers
            import watchdog.events
            
            class EventHandler(watchdog.events.FileSystemEventHandler):
                def __init__(self, callbacks):
                    self.callbacks = callbacks
                
                def on_created(self, event):
                    if not event.is_directory:
                        for callback in self.callbacks.get('add', []):
                            callback(event.src_path)
                
                def on_modified(self, event):
                    if not event.is_directory:
                        for callback in self.callbacks.get('change', []):
                            callback(event.src_path)
                
                def on_deleted(self, event):
                    if not event.is_directory:
                        for callback in self.callbacks.get('unlink', []):
                            callback(event.src_path)
            
            event_handler = EventHandler(self.callbacks)
            observer = watchdog.observers.Observer()
            observer.schedule(event_handler, directory_path, recursive=True)
            observer.start()
            
            print(f"Started fallback watcher for {directory_path}")
            return True
        except ImportError:
            print("watchdog not available. File watching disabled.")
            return False
        except Exception as e:
            print(f"Error starting fallback watcher: {e}")
            return False
    
    def on_file_added(self, callback: Callable[[str], None]) -> None:
        """
        Register callback for file added events.
        
        Args:
            callback: Function to call when a file is added
        """
        self.callbacks['add'].append(callback)
    
    def on_file_changed(self, callback: Callable[[str], None]) -> None:
        """
        Register callback for file changed events.
        
        Args:
            callback: Function to call when a file is changed
        """
        self.callbacks['change'].append(callback)
    
    def on_file_deleted(self, callback: Callable[[str], None]) -> None:
        """
        Register callback for file deleted events.
        
        Args:
            callback: Function to call when a file is deleted
        """
        self.callbacks['unlink'].append(callback)
    
    def stop_watching(self) -> None:
        """
        Stop file watching.
        """
        if self.watcher_process:
            self.watcher_process.terminate()
            self.watcher_process = None
            print("Stopped file watching")


def is_nodejs_installed() -> bool:
    """
    Check if Node.js is installed on the system.
    
    Returns:
        True if Node.js is installed, False otherwise
    """
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def install_chokidar_instructions() -> str:
    """
    Get instructions for installing chokidar.
    
    Returns:
        Installation instructions as string
    """
    return """
chokidar Installation Instructions:

1. Install Node.js:
   - Download from: https://nodejs.org/
   - Or use system package manager (apt, brew, etc.)

2. Install chokidar in your project:
   npm install chokidar

3. Verify installation:
   node --version
   npm list chokidar

For more information, see: https://github.com/paulmillr/chokidar
"""


if __name__ == "__main__":
    # Test chokidar integration
    print("Checking Node.js installation...")
    if is_nodejs_installed():
        print("✓ Node.js is installed")
        
        chokidar = ChokidarIntegration()
        if chokidar.available:
            print("✓ chokidar is available")
        else:
            print("✗ chokidar is not installed")
            print(install_chokidar_instructions())
    else:
        print("✗ Node.js is not installed")
        print("Install Node.js from: https://nodejs.org/")
