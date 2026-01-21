#!/usr/bin/env python3
"""
Script to run the backend server with integrated chatbot functionality
"""

import os
import sys
from pathlib import Path

def main():
    print("Starting backend server with integrated chatbot...")
    print("Setting up Python paths...")

    # Add the root directory to the Python path
    root_dir = str(Path(__file__).parent)
    sys.path.insert(0, root_dir)

    # Add the backend/src directory to the Python path
    backend_src_dir = str(Path(__file__).parent / "backend" / "src")
    sys.path.insert(0, backend_src_dir)

    # Add phase-3 directory to the path for chatbot components
    phase3_dir = str(Path(__file__).parent / "phase-3")
    sys.path.insert(0, phase3_dir)

    # Add subdirectories of phase-3 to the path
    mcp_server_dir = str(Path(__file__).parent / "phase-3" / "mcp_server")
    sys.path.insert(0, mcp_server_dir)

    tools_dir = str(Path(__file__).parent / "phase-3" / "mcp_server" / "tools")
    sys.path.insert(0, tools_dir)

    chatbot_dir = str(Path(__file__).parent / "phase-3" / "chatbot")
    sys.path.insert(0, chatbot_dir)

    adapters_dir = str(Path(__file__).parent / "phase-3" / "adapters")
    sys.path.insert(0, adapters_dir)

    services_dir = str(Path(__file__).parent / "phase-3" / "services")
    sys.path.insert(0, services_dir)

    config_dir = str(Path(__file__).parent / "phase-3" / "config")
    sys.path.insert(0, config_dir)

    # Set the PYTHONPATH environment variable to help with relative imports
    os.environ['PYTHONPATH'] = f"{root_dir};{backend_src_dir};{phase3_dir}"

    try:
        # Change to the root directory instead of backend/src to help with absolute imports
        original_cwd = os.getcwd()
        os.chdir(root_dir)

        # Import the main app using the fixed backend with proper path setup
        from backend_with_chatbot import app

        print("SUCCESS: Backend application with chatbot loaded successfully")
        print("Chatbot routes are registered and MCP tools are available")
        print("Starting server on port 8001...")
        print("\nThe chatbot endpoint will be available at: /api/chatbot")

        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)

        # Restore original directory
        os.chdir(original_cwd)

    except Exception as e:
        print(f"ERROR: Error starting server: {e}")
        import traceback
        traceback.print_exc()

        # Restore original directory
        if 'original_cwd' in locals():
            os.chdir(original_cwd)

        return False

if __name__ == "__main__":
    main()