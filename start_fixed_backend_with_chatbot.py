#!/usr/bin/env python3
"""
Fixed script to run the backend server with integrated chatbot functionality
This version ensures proper configuration for MCP server communication
"""

import os
import sys
from pathlib import Path
import subprocess
import time

def setup_environment():
    """Setup the environment variables and paths"""
    print("Setting up environment for backend server with chatbot...")

    # Set the BACKEND_API_URL for the phase-3 components to connect to
    os.environ['BACKEND_API_URL'] = 'http://localhost:8001/api'
    os.environ['MCP_PORT'] = '8080'
    os.environ['MCP_HOST'] = 'localhost'

    print(f"Environment variables set:")
    print(f"  BACKEND_API_URL = {os.environ.get('BACKEND_API_URL')}")
    print(f"  MCP_PORT = {os.environ.get('MCP_PORT')}")
    print(f"  MCP_HOST = {os.environ.get('MCP_HOST')}")

def main():
    print("Starting FIXED backend server with integrated chatbot...")
    print("Setting up Python paths and environment...")

    # Add the root directory and all necessary paths
    root_dir = Path(__file__).parent
    sys.path.insert(0, str(root_dir))

    # Add backend/src directory
    backend_src_dir = root_dir / "backend" / "src"
    sys.path.insert(0, str(backend_src_dir))

    # Add phase-3 directory and subdirectories
    phase3_dir = root_dir / "phase-3"
    sys.path.insert(0, str(phase3_dir))

    # Add all phase-3 subdirectories to ensure imports work
    subdirs = [
        "mcp_server",
        "mcp_server/tools",
        "chatbot",
        "adapters",
        "services",
        "config"
    ]

    for subdir in subdirs:
        full_path = phase3_dir / subdir
        if full_path.exists():
            sys.path.insert(0, str(full_path))

    # Set environment variables
    setup_environment()

    try:
        # Change to root directory for proper imports
        original_cwd = os.getcwd()
        os.chdir(root_dir)

        # Import the app with all paths set up
        from backend_with_chatbot import app

        print("SUCCESS: Backend application with chatbot loaded successfully")
        print("Chatbot routes are registered and MCP tools should be available")
        print("Starting server on port 8001...")
        print("\nThe chatbot endpoint will be available at: /api/chatbot")
        print("Make sure the MCP server is running on port 8002 for full functionality")

        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)

        os.chdir(original_cwd)

    except Exception as e:
        print(f"ERROR: Error starting server: {e}")
        import traceback
        traceback.print_exc()

        if 'original_cwd' in locals():
            os.chdir(original_cwd)

        return False

if __name__ == "__main__":
    main()