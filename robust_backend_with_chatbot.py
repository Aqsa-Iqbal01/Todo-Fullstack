#!/usr/bin/env python3
"""
Robust script to run the backend server with integrated chatbot functionality
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

    # Add the phase-3 directory to the Python path
    phase3_dir = root_dir / "phase-3"
    if str(phase3_dir) not in sys.path:
        sys.path.insert(0, str(phase3_dir))

    # Add all phase-3 subdirectories to the Python path
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
    print("Starting backend server with integrated chatbot...")
    print("Setting up Python paths...")

    # Setup paths before any imports
    setup_paths()

    try:
        # Force reimport of modules if they were previously imported with wrong paths
        modules_to_remove = [mod for mod in sys.modules.keys() if mod.startswith(('chatbot', 'mcp_server', 'adapters', 'services'))]
        for mod in modules_to_remove:
            del sys.modules[mod]

        # Import the main app
        from backend.src.main import app

        print("SUCCESS: Backend application loaded successfully")
        print("SUCCESS: Chatbot routes are already registered in main.py")
        print("SUCCESS: Starting server on port 8001...")
        print("\nThe chatbot endpoint will be available at: /api/chatbot")
        print("Visit http://localhost:8001/docs to see API documentation")

        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)

    except Exception as e:
        print(f"ERROR: Error starting server: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()