#!/usr/bin/env python3
"""
Detailed test to see what happens when we try to add a task
"""

import sys
import os
from pathlib import Path
import asyncio

# Add all necessary paths
root_dir = Path(__file__).parent
for path in [root_dir, root_dir / "backend" / "src", root_dir / "phase-3",
             root_dir / "phase-3" / "chatbot", root_dir / "phase-3" / "mcp_server",
             root_dir / "phase-3" / "mcp_server" / "tools", root_dir / "phase-3" / "adapters",
             root_dir / "phase-3" / "services", root_dir / "phase-3" / "config"]:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

print("=== Detailed Task Addition Test ===")

try:
    from chatbot.chat_interface import chat_interface
    print("[SUCCESS] Chat interface imported successfully")

    async def detailed_test():
        print("\nTesting: 'add milk to my list'")

        result = await chat_interface.process_user_input(
            user_input="add milk to my list",
            auth_token=""  # Empty token to simulate unauthenticated user
        )

        print(f"Result: {result}")
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        print(f"Intent: {result.get('intent')}")
        print(f"Entities: {result.get('entities')}")
        print(f"Action taken: {result.get('action_taken')}")
        print(f"Data: {result.get('data')}")

        # Test with a simulated valid token structure
        print("\n--- Testing with simulated token ---")
        result_with_token = await chat_interface.process_user_input(
            user_input="add milk to my list",
            auth_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"  # Sample JWT
        )

        print(f"Result with token: {result_with_token}")

        return result

    # Run the test
    asyncio.run(detailed_test())

except Exception as e:
    print(f"[ERROR] Error running test: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Test Complete ===")
print("This test shows what happens when adding tasks with different authentication states.")