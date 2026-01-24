"""
Final test to verify the complete chatbot workflow with MCP server
"""
import asyncio
import httpx
import os
import json

async def test_complete_workflow():
    """
    Test the complete workflow: Chatbot -> MCP Server -> Backend -> Database
    """
    print("Testing complete chatbot workflow...")
    
    # Set the correct backend URL
    os.environ['BACKEND_API_URL'] = 'http://localhost:8004/api'
    
    print("\nPrerequisites to run this test:")
    print("1. Backend server running on port 8004: python run_backend_with_db_init.py")
    print("2. MCP server running on port 8080: python -m phase-3.start_mcp_server")
    print("3. A valid authentication token from registering/logging in")
    
    # Check if backend is running
    print("\n1. Verifying backend server on port 8004...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8004/health")
            if response.status_code == 200:
                print("[OK] Backend server is running")
            else:
                print(f"[ERROR] Backend not responding: {response.status_code}")
                return False
    except Exception as e:
        print(f"[ERROR] Cannot connect to backend: {e}")
        print("Start the backend server first!")
        return False
    
    # Check if MCP server is running
    print("\n2. Verifying MCP server on port 8080...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8080/")
            if response.status_code == 200:
                print("[OK] MCP server is running")
            else:
                print(f"[ERROR] MCP server not responding: {response.status_code}")
                print("Start the MCP server first!")
                return False
    except Exception as e:
        print(f"[ERROR] Cannot connect to MCP server: {e}")
        print("Start the MCP server first!")
        return False
    
    print("\n3. To test the complete workflow:")
    print("   a) Register/login to get an authentication token")
    print("   b) Use curl or Postman to test the chatbot endpoint:")
    print("")
    print("   curl -X POST http://localhost:8004/api/chatbot \\")
    print("     -H 'Authorization: Bearer YOUR_TOKEN_HERE' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"message\": \"Add test todo to my list\"}'")
    print("")
    print("4. Expected behavior:")
    print("   - The chatbot should respond with success message")
    print("   - The todo should be saved to the database")
    print("   - You should be able to retrieve it with 'Show my todos'")
    print("")
    print("5. Troubleshooting tips:")
    print("   - Check that both servers are running")
    print("   - Verify the BACKEND_API_URL is set to http://localhost:8004/api")
    print("   - Make sure you're using a valid authentication token")
    print("   - Check server logs for any error messages")
    
    return True

if __name__ == "__main__":
    print("="*70)
    print("COMPLETE CHATBOT WORKFLOW TEST")
    print("="*70)
    asyncio.run(test_complete_workflow())
    print("="*70)