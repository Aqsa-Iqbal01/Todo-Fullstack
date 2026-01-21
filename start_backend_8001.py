#!/usr/bin/env python3
"""
Script to run the backend server with chatbot functionality on port 8001
"""

import subprocess
import sys
import os
from pathlib import Path

def run_backend_on_port_8001():
    """Run the backend server on port 8001"""
    print("Setting up backend server to run on port 8001...")

    # Change to the backend/src directory
    backend_src_dir = Path(__file__).parent / "backend" / "src"

    if not backend_src_dir.exists():
        print("Error: Backend directory not found!")
        return False

    print(f"Backend directory: {backend_src_dir}")

    # Set environment variable to override the port
    env = os.environ.copy()
    env['PORT'] = '8001'

    print("Starting backend server on port 8001...")
    print("This includes the chatbot functionality at /api/chatbot")
    print("\nOnce running, you can test the chatbot with requests to:")
    print("http://localhost:8001/api/chatbot")

    try:
        # Run the uvicorn server
        cmd = [
            sys.executable, "-c",
            "import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=8001)"
        ]

        # Change to the backend src directory
        os.chdir(backend_src_dir)

        # Execute the command
        subprocess.run(cmd, env=env)

        return True
    except Exception as e:
        print(f"Error starting server: {e}")
        return False

def main():
    print("Backend Server Startup Script")
    print("="*40)
    print("This will run the backend server (including chatbot) on port 8001")
    print("")

    success = run_backend_on_port_8001()

    if not success:
        print("\nFailed to start the server!")
        print("Make sure you have installed the dependencies:")
        print("  cd backend && pip install -r requirements.txt")
    else:
        print("Server started successfully!")

if __name__ == "__main__":
    main()