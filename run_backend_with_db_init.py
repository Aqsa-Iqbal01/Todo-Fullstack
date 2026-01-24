import subprocess
import sys
import time
import threading
from backend.src.database.database import create_db_and_tables
import os

def initialize_database():
    """Initialize the database tables"""
    print("Initializing database...")
    try:
        create_db_and_tables()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

def start_backend():
    """Start the backend server"""
    print("Starting backend server...")

    # Set environment variable for the correct port
    env = os.environ.copy()
    env['PORT'] = '8004'

    # Start the Uvicorn server
    subprocess.run([
        sys.executable, '-m', 'uvicorn',
        'backend.src.main:app',
        '--host', 'localhost',
        '--port', '8004'
    ], env=env)

if __name__ == "__main__":
    print("Setting up Todo Chatbot System...")

    # Initialize the database first
    initialize_database()

    # Start the backend server in a separate thread
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()

    print("\n" + "="*60)
    print("TODO CHATBOT SYSTEM STARTUP COMPLETE")
    print("="*60)
    print("✓ Database initialized successfully")
    print("✓ Backend server starting on http://localhost:8004")
    print("\nNext steps:")
    print("1. Open a new terminal and start the MCP server:")
    print("   cd phase-3 && python start_mcp_server.py")
    print("2. Register or login to get an authentication token")
    print("3. Test the chatbot API with curl or the frontend")
    print("="*60)

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)