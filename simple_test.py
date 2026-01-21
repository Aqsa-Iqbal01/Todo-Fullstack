#!/usr/bin/env python3
"""
Simple test to verify chatbot functionality
"""

import sys
import os
from pathlib import Path

# Add the root directory and phase-3 directory to the path for chatbot imports
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Add phase-3 directory to the path
phase3_dir = root_dir / "phase-3"
sys.path.insert(0, str(phase3_dir))

# Add subdirectories of phase-3 to the path
sys.path.insert(0, str(phase3_dir / "mcp_server"))
sys.path.insert(0, str(phase3_dir / "mcp_server" / "tools"))
sys.path.insert(0, str(phase3_dir / "chatbot"))
sys.path.insert(0, str(phase3_dir / "adapters"))
sys.path.insert(0, str(phase3_dir / "services"))
sys.path.insert(0, str(phase3_dir / "config"))

# Add backend/src directory to the path
backend_src_dir = root_dir / "backend" / "src"
sys.path.insert(0, str(backend_src_dir))

print("Testing chatbot imports...")

try:
    from chatbot.chat_interface import chat_interface
    print("Success: Imported chat_interface")

    # Check if the chat interface has the required components
    if hasattr(chat_interface, 'process_user_input'):
        print("Success: chat_interface has process_user_input method")
    else:
        print("Error: chat_interface missing process_user_input method")

except ImportError as e:
    print(f"Error importing chat_interface: {e}")

try:
    from config.settings import settings
    print(f"Success: Settings loaded. Backend API URL: {settings.backend_api_url}")
except ImportError as e:
    print(f"Error importing settings: {e}")

try:
    from mcp_server.server import mcp_server
    print("Success: Imported mcp_server")
    print(f"Available tools: {mcp_server.get_available_tools()['tools']}")
except ImportError as e:
    print(f"Error importing mcp_server: {e}")

try:
    from services.todo_service import todo_service
    print("Success: Imported todo_service")
except ImportError as e:
    print(f"Error importing todo_service: {e}")

print("\nImport test completed successfully!")