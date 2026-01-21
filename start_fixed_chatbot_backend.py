#!/usr/bin/env python3
"""
Fixed script to run the backend server with properly integrated chatbot functionality
This version ensures all paths are correctly set up for MCP tools to work.
"""

import os
import sys
from pathlib import Path

def setup_paths():
    """Setup all necessary paths for the application to work correctly."""
    # Add the root directory to the Python path
    root_dir = Path(__file__).parent
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))

    # Add backend/src directory to the Python path
    backend_src_dir = root_dir / "backend" / "src"
    if str(backend_src_dir) not in sys.path:
        sys.path.insert(0, str(backend_src_dir))

    # Add the phase-3 directory to the Python path - CRITICAL FOR CHATBOT
    phase3_dir = root_dir / "phase-3"
    if str(phase3_dir) not in sys.path:
        sys.path.insert(0, str(phase3_dir))

    # Add ALL phase-3 subdirectories to the Python path - CRITICAL FOR MCP TOOLS
    for subdir in ["chatbot", "mcp_server", "mcp_server/tools", "adapters", "services", "config", "prompts"]:
        subdir_path = phase3_dir / subdir
        if subdir_path.exists():
            subdir_str = str(subdir_path)
            if subdir_str not in sys.path:
                sys.path.insert(0, subdir_str)

    # Set environment variables to help with imports
    os.environ['PYTHONPATH'] = os.pathsep.join(sys.path)

    print(f"Root directory: {root_dir}")
    print(f"Phase-3 directory: {phase3_dir}")
    print(f"Backend src directory: {backend_src_dir}")
    print(f"Python path updated. Added {len(sys.path)} paths.")

def main():
    print("Starting FIXED backend server with integrated chatbot...")
    print("Setting up Python paths for MCP tools...")

    # Setup paths before any imports
    setup_paths()

    try:
        # Force reimport of modules if they were previously imported with wrong paths
        modules_to_remove = [mod for mod in sys.modules.keys() if mod.startswith(('chatbot', 'mcp_server', 'adapters', 'services', 'backend.src.api.chatbot'))]
        for mod in modules_to_remove:
            if mod in sys.modules:
                del sys.modules[mod]

        # Import the main app using the fixed backend with proper path setup
        from fixed_backend_with_chatbot import app

        print("SUCCESS: Backend application with chatbot loaded successfully")
        print("SUCCESS: MCP tools should now be available and connected")
        print("Starting server on port 8001...")
        print("\nThe chatbot endpoint will be available at: /api/chatbot")
        print("Visit http://localhost:8001/debug/paths to verify path setup")
        print("Visit http://localhost:8001/debug/env to verify environment setup")

        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)

    except Exception as e:
        print(f"ERROR: Error starting server: {e}")
        import traceback
        traceback.print_exc()

        # Try to provide more specific debugging info
        print("\nDEBUGGING INFO:")
        root_dir = Path(__file__).parent
        phase3_dir = root_dir / "phase-3"
        chatbot_dir = phase3_dir / "chatbot"
        print(f"Phase-3 directory exists: {phase3_dir.exists()}")
        print(f"Chatbot directory exists: {chatbot_dir.exists()}")
        print(f"Chat interface file exists: {(chatbot_dir / 'chat_interface.py').exists()}")

        return False

if __name__ == "__main__":
    main()