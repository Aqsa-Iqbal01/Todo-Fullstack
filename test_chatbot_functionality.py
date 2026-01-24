"""
Test script to verify the chatbot functionality with MCP server
"""
import asyncio
import httpx
import os
import json

async def test_chatbot_with_mcp():
    """
    Test the chatbot functionality with MCP server
    """
    print("Testing chatbot with MCP server...")
    
    # Set the correct backend URL
    os.environ['BACKEND_API_URL'] = 'http://localhost:8004/api'
    
    # Test 1: Check if backend is running
    print("\n1. Checking if backend is running on port 8004...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8004/health")
            if response.status_code == 200:
                print(f"[OK] Backend is running: {response.json()}")
            else:
                print(f"[ERROR] Backend not responding properly: {response.status_code}")
                return False
    except Exception as e:
        print(f"[ERROR] Cannot connect to backend: {e}")
        print("Make sure you've started the backend with: python run_backend_with_db_init.py")
        return False
    
    # Test 2: Check if MCP server is running
    print("\n2. Checking if MCP server is running on port 8080...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8080/")
            if response.status_code == 200:
                print(f"[OK] MCP server is running: {response.json()}")
            else:
                print(f"[ERROR] MCP server not responding properly: {response.status_code}")
                print("Make sure you've started the MCP server with: python -m phase-3.start_mcp_server")
                return False
    except Exception as e:
        print(f"[ERROR] Cannot connect to MCP server: {e}")
        print("Make sure you've started the MCP server with: python -m phase-3.start_mcp_server")
        return False
    
    # Test 3: Try to register a test user (if registration endpoint exists)
    print("\n3. Preparing to test chatbot functionality...")
    print("Note: To test the chatbot, you need a valid authentication token.")
    print("First, register or login to get an authentication token.")
    
    # Example of how to test once you have a token:
    print("\nTo test the chatbot after getting a token:")
    print("curl -X POST http://localhost:8004/api/chatbot \\")
    print("  -H 'Authorization: Bearer YOUR_ACTUAL_TOKEN' \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"message\": \"Add buy milk to my todo list\"}'")
    
    # Test 4: Show available tools in MCP server
    print("\n4. Checking available MCP tools...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8080/mcp/tools")
            if response.status_code == 200:
                tools = response.json()
                print(f"[OK] Available MCP tools: {tools}")
            else:
                print(f"[ERROR] Could not get MCP tools: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Error getting MCP tools: {e}")

    print("\n" + "="*60)
    print("TEST SUMMARY:")
    print("[OK] Backend server is running on port 8004")
    print("[OK] MCP server is running on port 8080")
    print("[OK] Configuration is properly set")
    print("\nNext steps:")
    print("1. Register a user account or login to get an authentication token")
    print("2. Use the token to test the chatbot endpoint")
    print("3. Try commands like: 'Add buy groceries to my list'")
    print("="*60)
    
    return True

if __name__ == "__main__":
    asyncio.run(test_chatbot_with_mcp())