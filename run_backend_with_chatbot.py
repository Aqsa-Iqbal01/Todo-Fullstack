#!/usr/bin/env python3
"""
Script to run the backend server with integrated chatbot functionality
"""

import subprocess
import sys
import os
from pathlib import Path

def run_backend_with_chatbot():
    """Run the backend server which includes the chatbot functionality"""
    print("Setting up backend server with integrated chatbot...")

    # Change to the backend/src directory
    backend_src_dir = Path(__file__).parent / "backend" / "src"

    if not backend_src_dir.exists():
        print("Error: Backend directory not found!")
        print(f"Expected path: {backend_src_dir}")
        return False

    print(f"Backend source directory: {backend_src_dir}")
    print("Checking if required modules can be imported...")

    # Try to import and verify the chatbot components are accessible
    original_path = sys.path[:]
    try:
        sys.path.insert(0, str(backend_src_dir))

        # Import the main app to check if everything loads correctly
        import main
        print("✓ Main backend application loaded successfully")

        # Check if chatbot routes are registered
        import api.chatbot
        print("✓ Chatbot API module loaded successfully")

        # Restore original path
        sys.path[:] = original_path

        print("\n✓ All components loaded successfully!")
        print("The chatbot endpoint will be available at: /api/chatbot")
        print("Supported commands include:")
        print("  - 'Add buy groceries to my list'")
        print("  - 'Show my todos'")
        print("  - 'Mark buy groceries as complete'")
        print("  - 'Delete the meeting with John'")

        # Set environment variables for the server
        env = os.environ.copy()
        env['PORT'] = '8001'  # Use port 8001 as requested
        env['BACKEND_API_URL'] = 'http://localhost:8001/api'  # Update API URL to match port

        print(f"\nStarting server on port 8001...")
        print("Visit http://localhost:8001/docs to see API documentation")
        print("Chatbot endpoint will be available at http://localhost:8001/api/chatbot")

        # Change to the backend src directory
        os.chdir(backend_src_dir)

        # Run uvicorn server
        cmd = [
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8001",
            "--reload"
        ]

        print(f"Executing: {' '.join(cmd)}")

        # Run the server
        result = subprocess.run(cmd, env=env)
        return result.returncode == 0

    except ImportError as e:
        print(f"✗ Import error: {e}")
        sys.path[:] = original_path
        return False
    except Exception as e:
        print(f"✗ Error running backend: {e}")
        sys.path[:] = original_path
        return False

def main():
    print("Backend Server with Integrated Chatbot")
    print("="*50)
    print("This will start the backend server with chatbot functionality")
    print("")

    print("Before running, make sure you have installed dependencies:")
    print("  cd backend && pip install -r requirements.txt")
    print("")

    success = run_backend_with_chatbot()

    if not success:
        print("\nFailed to start the server!")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have installed the backend dependencies:")
        print("   cd backend && pip install -r requirements.txt")
        print("2. Make sure you have set required environment variables like JWT_SECRET")
        print("3. Check that no other process is using port 8001")
    else:
        print("Server started successfully!")

if __name__ == "__main__":
    main()