#!/usr/bin/env python3
"""
Startup script for the MCP Server
"""

import sys
import os
from pathlib import Path

def setup_paths():
    """Setup Python paths for the MCP server"""
    # Get the phase-3 directory
    current_dir = Path(__file__).parent
    phase3_dir = current_dir

    # Add all necessary directories to the Python path
    paths_to_add = [
        str(phase3_dir),
        str(phase3_dir / 'mcp_server'),
        str(phase3_dir / 'mcp_server' / 'tools'),
        str(phase3_dir / 'chatbot'),
        str(phase3_dir / 'adapters'),
        str(phase3_dir / 'services'),
        str(phase3_dir / 'config'),
    ]

    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)

def main():
    """Start the MCP server"""
    # Set environment variable for backend API URL before setting up paths
    os.environ['BACKEND_API_URL'] = 'http://localhost:8001/api'

    setup_paths()

    try:
        # Import the app after setting up paths
        from mcp_server.server import app

        # Start the server using uvicorn
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8002, reload=False)

    except Exception as e:
        print(f"Error starting MCP server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()