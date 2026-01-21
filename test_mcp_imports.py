#!/usr/bin/env python3
"""
Test script to verify MCP tools imports are working correctly
"""

import sys
import os
from pathlib import Path

# Add all necessary paths like the fixed backend does
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Add backend/src directory to the Python path
backend_src_dir = root_dir / "backend" / "src"
sys.path.insert(0, str(backend_src_dir))

# Add the phase-3 directory to the Python path - CRITICAL FOR CHATBOT
phase3_dir = root_dir / "phase-3"
sys.path.insert(0, str(phase3_dir))

# Add ALL phase-3 subdirectories to the path - CRITICAL FOR MCP TOOLS
for subdir in ["chatbot", "mcp_server", "mcp_server/tools", "adapters", "services", "config", "prompts"]:
    subdir_path = phase3_dir / subdir
    if subdir_path.exists():
        subdir_str = str(subdir_path)
        if subdir_str not in sys.path:
            sys.path.insert(0, subdir_str)

print("=== Testing MCP Tools Import ===")

# Test importing the chat interface
try:
    from chatbot.chat_interface import chat_interface
    print("✅ SUCCESS: Successfully imported chat_interface from chatbot module")

    # Check if it's the real interface or mock
    if hasattr(chat_interface, '__class__'):
        class_name = chat_interface.__class__.__name__
        print(f"✅ Interface class: {class_name}")

        if "Mock" in class_name:
            print("❌ WARNING: This is a MOCK interface - MCP tools are NOT connected!")
        else:
            print("✅ CONFIRMED: This is the REAL interface - MCP tools should be connected!")
    else:
        print(f"⚠️  Unknown interface type: {type(chat_interface)}")

except ImportError as e:
    print(f"❌ FAILED: Could not import chat_interface: {e}")

    # Try alternative import path
    try:
        phase3_chatbot_dir = phase3_dir / "chatbot"
        sys.path.insert(0, str(phase3_bot_dir))
        from chat_interface import chat_interface
        print("✅ SUCCESS: Imported chat_interface using alternative path")
    except ImportError as e2:
        print(f"❌ FAILED: Alternative import also failed: {e2}")
        print("\n🔧 SOLUTION: Run the fixed backend server to ensure proper path setup!")

# Test importing MCP server components
try:
    from mcp_server.server import MCPServer, process_nlp_request
    print("✅ SUCCESS: Successfully imported MCP server components")
except ImportError as e:
    print(f"❌ FAILED: Could not import MCP server: {e}")

# Test importing tools
try:
    from mcp_server.tools.create_todo import create_todo_tool
    print("✅ SUCCESS: Successfully imported create_todo tool")
except ImportError as e:
    print(f"❌ FAILED: Could not import create_todo tool: {e}")

try:
    from mcp_server.tools.list_todos import list_todos_tool
    print("✅ SUCCESS: Successfully imported list_todos tool")
except ImportError as e:
    print(f"❌ FAILED: Could not import list_todos tool: {e}")

print("\n=== Test Complete ===")
print("If you see MCP server and tool imports succeeding, MCP tools should be working.")
print("If you see failures, the paths are not set up correctly for MCP tools.")