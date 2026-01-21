#!/usr/bin/env python3
"""
Script to restart the backend server with integrated chatbot functionality using the fixed configuration
"""

import subprocess
import sys
import os
import signal
import time
from pathlib import Path

def stop_existing_servers():
    """Stop any existing servers running on port 8001"""
    try:
        # Find the process using port 8001
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        lines = result.stdout.split('\n')

        for line in lines:
            if ':8001' in line and 'LISTENING' in line:
                # Extract PID
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]  # PID is the last column
                    if pid.isdigit() and pid != '0':
                        print(f"Stopping existing process on port 8001 (PID: {pid})...")
                        try:
                            os.kill(int(pid), signal.SIGTERM)
                            time.sleep(2)  # Wait for graceful shutdown
                        except ProcessLookupError:
                            print(f"Process {pid} already terminated")
                        except PermissionError:
                            print(f"Permission denied stopping process {pid}. Trying taskkill...")
                            subprocess.run(['taskkill', '/F', '/PID', pid], check=False)
    except Exception as e:
        print(f"Error stopping existing servers: {e}")

def main():
    print("Preparing to restart backend server with integrated chatbot...")

    # Stop existing servers
    stop_existing_servers()

    print("Starting backend server with enhanced path configuration...")

    # Run the updated start script
    try:
        # Change to the project directory
        project_dir = Path(__file__).parent
        os.chdir(project_dir)

        # Import and run the updated start script
        import start_chatbot_backend
        start_chatbot_backend.main()

    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()