/**
 * chokidar file watcher for Lucid
 * Based on ARCHITECTURE.html specification
 * Layer 4: Virtual Layer - File watching using chokidar
 * 
 * This Node.js script provides file watching capabilities using chokidar.
 * It communicates with Python via stdin/stdout JSON messages.
 */

const chokidar = require('chokidar');
const path = require('path');

// Configuration
const WATCH_PATH = process.argv[2] || process.cwd();
const DEBOUNCE_MS = 100;

// Event callbacks
const callbacks = {
    add: [],
    change: [],
    unlink: []
};

// Initialize watcher
const watcher = chokidar.watch(WATCH_PATH, {
    ignored: /(^|[\/\\])\../, // ignore dotfiles
    persistent: true,
    ignoreInitial: false,
    awaitWriteFinish: {
        stabilityThreshold: 2000,
        pollInterval: 100
    }
});

// Event handlers
watcher
    .on('add', (filePath) => {
        const event = {
            type: 'add',
            path: filePath,
            timestamp: Date.now()
        };
        console.log(JSON.stringify(event));
    })
    .on('change', (filePath) => {
        const event = {
            type: 'change',
            path: filePath,
            timestamp: Date.now()
        };
        console.log(JSON.stringify(event));
    })
    .on('unlink', (filePath) => {
        const event = {
            type: 'unlink',
            path: filePath,
            timestamp: Date.now()
        };
        console.log(JSON.stringify(event));
    })
    .on('error', (error) => {
        console.error('Watcher error:', error);
    });

// Start watching
console.log(JSON.stringify({
    type: 'ready',
    path: WATCH_PATH,
    timestamp: Date.now()
}));

// Handle graceful shutdown
process.on('SIGINT', () => {
    watcher.close();
    console.log(JSON.stringify({
        type: 'shutdown',
        timestamp: Date.now()
    }));
    process.exit(0);
});
