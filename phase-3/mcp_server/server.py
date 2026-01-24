"""MCP Server Implementation for Phase III AI Chatbot

This implements the Model Context Protocol server that handles
communication between the AI chatbot and the todo backend.
"""

import asyncio
import json
from typing import Dict, Any, Callable
from pydantic import BaseModel
import httpx
import sys
import os
from dotenv import load_dotenv

# Add the phase-3 directory to the path for proper imports
current_dir = os.path.dirname(__file__)
phase3_dir = os.path.dirname(os.path.dirname(current_dir))

# Add phase-3 and its subdirectories to the path
sys.path.insert(0, phase3_dir)
sys.path.insert(0, os.path.join(phase3_dir, 'mcp_server'))
sys.path.insert(0, os.path.join(phase3_dir, 'mcp_server', 'tools'))
sys.path.insert(0, os.path.join(phase3_dir, 'chatbot'))
sys.path.insert(0, os.path.join(phase3_dir, 'adapters'))
sys.path.insert(0, os.path.join(phase3_dir, 'services'))
sys.path.insert(0, os.path.join(phase3_dir, 'config'))

# Load environment variables from .env file if not in production
if not os.getenv("VERCEL_ENV"):
    phase3_dir = os.path.dirname(os.path.dirname(__file__))
    env_path = os.path.join(phase3_dir, '.env')
    load_dotenv(dotenv_path=env_path)

# Handle config import separately to avoid issues
try:
    from config.settings import settings
except ImportError:
    print("Config import failed, creating default settings...")
    # Create a minimal settings object as fallback
    class Settings:
        def __init__(self):
            self.backend_api_url = os.getenv("BACKEND_API_URL", "http://localhost:8004/api")
            self.require_auth = os.getenv("REQUIRE_AUTH", "true").lower() == "true"
            self.mcp_port = int(os.getenv("MCP_PORT", "8080"))
            self.mcp_host = os.getenv("MCP_HOST", "localhost")
            self.intent_threshold = float(os.getenv("INTENT_THRESHOLD", "0.7"))
            self.max_input_length = int(os.getenv("MAX_INPUT_LENGTH", "500"))
            self.api_retry_attempts = int(os.getenv("API_RETRY_ATTEMPTS", "3"))
            self.api_retry_delay = float(os.getenv("API_RETRY_DELAY", "1.0"))
            self.log_level = os.getenv("LOG_LEVEL", "INFO")

    settings = Settings()

# Import FastAPI after setting up paths
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# Import tools with error handling - using proper path setup
import sys
import os

# Set up the proper Python path for relative imports to work
current_dir = os.path.dirname(__file__)  # mcp_server directory
phase3_dir = os.path.dirname(os.path.dirname(current_dir))  # phase-3 directory

# Add the phase-3 directory to the path so relative imports work correctly
if phase3_dir not in sys.path:
    sys.path.insert(0, phase3_dir)

# Add the mcp_server directory to the path as well
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    # Import tools using the proper package structure
    from mcp_server.tools.create_todo import create_todo_tool
    from mcp_server.tools.update_todo import update_todo_tool
    from mcp_server.tools.delete_todo import delete_todo_tool
    from mcp_server.tools.list_todos import list_todos_tool

    print("Successfully imported MCP tools")

except ImportError as e:
    print(f"Failed to import tools: {e}")
    # Define mock tools as fallback
    async def create_todo_tool(parameters):
        return {"success": False, "error": "Tool not available", "original_input": parameters.get("user_input", "")}

    async def update_todo_tool(parameters):
        return {"success": False, "error": "Tool not available", "original_input": parameters.get("user_input", "")}

    async def delete_todo_tool(parameters):
        return {"success": False, "error": "Tool not available", "original_input": parameters.get("user_input", "")}

    async def list_todos_tool(parameters):
        return {"success": False, "error": "Tool not available", "original_input": parameters.get("user_input", "")}


class MCPServer:
    """Model Context Protocol server implementation"""

    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self._register_tools()

    def _register_tools(self):
        """Register all available MCP tools"""
        self.tools = {
            "create_todo": create_todo_tool,
            "update_todo": update_todo_tool,
            "delete_todo": delete_todo_tool,
            "list_todos": list_todos_tool,
        }

    async def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an incoming MCP request"""
        try:
            # Extract the tool name and parameters
            tool_name = request_data.get("tool_name")
            parameters = request_data.get("parameters", {})

            if tool_name not in self.tools:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}",
                    "result": None
                }

            # Execute the requested tool
            tool_func = self.tools[tool_name]
            result = await tool_func(parameters)

            return {
                "success": True,
                "error": None,
                "result": result
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error executing tool: {str(e)}",
                "result": None
            }

    def get_available_tools(self) -> Dict[str, Any]:
        """Return information about available tools"""
        return {
            "tools": list(self.tools.keys()),
            "description": "Todo management tools for creating, reading, updating, and deleting todos"
        }


# Global MCP server instance
mcp_server = MCPServer()


async def process_nlp_request(user_input: str, auth_token: str) -> Dict[str, Any]:
    """
    Process natural language input through intent parsing and MCP tools

    Args:
        user_input: Natural language input from user
        auth_token: Authentication token for backend API calls

    Returns:
        Dictionary with success status and result
    """
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from chatbot.intent_parser import IntentParser
    from chatbot.entity_extractor import EntityExtractor

    # Parse intent from user input
    intent_parser = IntentParser()
    intent = intent_parser.classify_intent(user_input)

    # Extract entities from user input
    entity_extractor = EntityExtractor()
    entities = entity_extractor.extract_entities(user_input)

    # Map intent to appropriate MCP tool
    tool_mapping = {
        "CREATE_TODO": "create_todo",
        "READ_TODOS": "list_todos",
        "UPDATE_TODO": "update_todo",
        "DELETE_TODO": "delete_todo"
    }

    if intent not in tool_mapping:
        return {
            "success": False,
            "error": f"Could not map intent: {intent}",
            "result": None,
            "intent": intent,
            "entities": entities
        }

    # Prepare parameters for the MCP tool
    tool_params = {
        "user_input": user_input,
        "intent": intent,
        "entities": entities,
        "auth_token": auth_token
    }

    # Execute the appropriate tool
    tool_name = tool_mapping[intent]
    request_data = {
        "tool_name": tool_name,
        "parameters": tool_params
    }

    result = await mcp_server.handle_request(request_data)
    result["intent"] = intent
    result["entities"] = entities

    return result


# Define Pydantic models for request validation
class ProcessRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]


class ProcessNLPRequest(BaseModel):
    input: str


# Create the FastAPI application for ASGI
app = FastAPI(title="MCP Todo Server", version="1.0.0")

# Configure CORS for communication with the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "MCP Todo Server is running", "available_endpoints": ["/mcp/tools", "/mcp/process_nlp"]}


@app.get("/mcp/tools")
async def get_tools():
    """Get available MCP tools"""
    return mcp_server.get_available_tools()


@app.post("/mcp/process")
async def process_request(request: ProcessRequest):
    """Process an MCP request"""
    result = await mcp_server.handle_request(request.dict())
    return result


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@app.post("/mcp/process_nlp")
async def process_nlp(request: ProcessNLPRequest, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Process natural language input"""
    auth_token = credentials.credentials
    result = await process_nlp_request(request.input, auth_token)
    return result


# For standalone running
try:
    import uvicorn
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8002)))
except ImportError:
    pass