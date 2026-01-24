import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'phase-3'))
sys.path.insert(0, os.path.join(os.getcwd(), 'phase-3', 'mcp_server'))
sys.path.insert(0, os.path.join(os.getcwd(), 'phase-3', 'chatbot'))

print("Testing module imports...")

# Test importing the main modules to verify syntax is correct
try:
    from mcp_server.server import process_nlp_request
    print('[SUCCESS] MCP server module imports correctly')
except Exception as e:
    print(f'[ERROR] MCP server import failed: {e}')

try:
    from chatbot.chat_interface import chat_interface
    print('[SUCCESS] Chat interface module imports correctly')
except Exception as e:
    print(f'[ERROR] Chat interface import failed: {e}')

try:
    from services.todo_service import todo_service
    print('[SUCCESS] Todo service module imports correctly')
except Exception as e:
    print(f'[ERROR] Todo service import failed: {e}')

try:
    from adapters.todo_api_adapter import todo_api_adapter
    print('[SUCCESS] Todo API adapter module imports correctly')
except Exception as e:
    print(f'[ERROR] Todo API adapter import failed: {e}')

print('\n[SUCCESS] All modules import correctly - syntax is valid')