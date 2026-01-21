"""Chatbot API Endpoint for Phase III

This module provides the API endpoint for the MCP-based chatbot
that processes natural language input and returns responses.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import asyncio
from typing import Dict, Any
from pydantic import BaseModel
from ..auth.auth_handler import get_current_user
import sys
import os

# Add the project root directory to the Python path so imports work correctly
project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
phase_3_dir = os.path.join(project_root, 'phase-3')

# Insert both directories to the path
if phase_3_dir not in sys.path:
    sys.path.insert(0, phase_3_dir)

# Now import the chat interface
try:
    from chatbot.chat_interface import chat_interface
except ImportError as e:
    print(f"Error importing chat_interface: {e}")
    print("Attempting to load with alternative path setup...")

    # Try adding more path variations
    alt_phase_3_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '..', 'phase-3')
    if os.path.exists(alt_phase_3_dir) and alt_phase_3_dir not in sys.path:
        sys.path.insert(0, alt_phase_3_dir)

    try:
        from chatbot.chat_interface import chat_interface
    except ImportError:
        print("Error: Could not import chat_interface from phase-3. Creating mock interface.")
        # Create a mock interface if import fails
        class MockChatInterface:
            async def process_user_input(self, user_input: str, auth_token: str, conversation_id: str = None):
                return {
                    "success": False,
                    "message": "Chatbot service is currently unavailable. Please check if the phase-3 components are properly set up.",
                    "intent": "ERROR",
                    "entities": {},
                    "error": "Import error - service unavailable"
                }

        chat_interface = MockChatInterface()


router = APIRouter()
security = HTTPBearer()


class ChatRequest(BaseModel):
    message: str


@router.post("/chatbot")
async def chat_endpoint(
    request: ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Process natural language input through the MCP-based chatbot

    Args:
        request: Chat request containing the user's message
        credentials: Authorization credentials

    Returns:
        Response from the chatbot
    """
    try:
        # Extract the token from credentials
        auth_token = credentials.credentials

        # Validate that the user is authenticated
        current_user = get_current_user(auth_token)
        if not current_user:
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        # Process the user input through the MCP-based chat interface
        result = await chat_interface.process_user_input(
            user_input=request.message,
            auth_token=auth_token
        )

        return {
            "success": result["success"],
            "response": {
                "message": result["message"],
                "intent_processed": result.get("intent", "UNKNOWN"),
                "entities_extracted": result.get("entities", {}),
                "operation_result": result.get("data")
            },
            "conversation_context": {"conversation_context": "mcp_based"}
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "CHATBOT_PROCESSING_ERROR",
                    "message": "Error processing your request"
                }
            }
        )


# Register the router
def register_chatbot_routes(app):
    """Register chatbot routes with the main application"""
    app.include_router(router, prefix="/api", tags=["chatbot"])