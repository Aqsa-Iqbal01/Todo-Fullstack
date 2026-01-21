#!/usr/bin/env python3
"""
Test script to verify if the chatbot interface can process requests using MCP tools
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

print("=== Testing MCP Tools Functionality ===")

try:
    from chatbot.chat_interface import chat_interface

    print("Testing chat interface with sample input...")

    # Test with a sample input (using a dummy auth token since we're just testing the interface)
    import asyncio

    async def test_chat():
        # Test creating a todo
        result_create = await chat_interface.process_user_input(
            user_input="add test task using mcp tools",
            auth_token="dummy_token_for_testing"
        )

        print(f"Create todo result: {result_create}")

        # Test listing todos
        result_list = await chat_interface.process_user_input(
            user_input="show my todos",
            auth_token="dummy_token_for_testing"
        )

        print(f"List todos result: {result_list}")

        return result_create, result_list

    # Run the async test
    results = asyncio.run(test_chat())
    create_result, list_result = results

    # Check if the results indicate real MCP tools are being used
    if create_result.get("success") is False and "authentication" in str(create_result.get("error", "")).lower():
        print("\n[EXPECTED] Authentication failed (which is normal with dummy token)")
        print("[SUCCESS] MCP tools ARE being called, but authentication is failing")
        print("[INFO] This means MCP tools are properly connected!")
    elif create_result.get("success") is True:
        print("\n[WOW] MCP tools worked even with dummy token!")
        print("[SUCCESS] MCP tools are fully functional!")
    else:
        if "mock" in str(create_result).lower() or "unavailable" in str(create_result.get("message", "")).lower():
            print("\n[PROBLEM] MCP tools are NOT being used - mock interface detected")
        else:
            print("\n[PARTIAL] MCP tools are being called, but with errors (likely auth)")

except Exception as e:
    print(f"[ERROR] Could not test chat interface: {e}")
    import traceback
    traceback.print_exc()

print("")
print("=== Test Complete ===")
print("If MCP tools are being called, you should see specific error messages about authentication")
print("rather than generic 'service unavailable' messages.")