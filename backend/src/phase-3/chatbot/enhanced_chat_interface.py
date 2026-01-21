"""Enhanced Chat Interface for Phase III AI Chatbot with OpenAI Integration

This module provides the main interface for the AI chatbot
that processes natural language input using OpenAI and MCP tools.
"""

import asyncio
from typing import Dict, Any
import sys
import os

# Add the phase-3 directory to the Python path so imports work correctly
phase_3_dir = os.path.dirname(os.path.dirname(__file__))
if phase_3_dir not in sys.path:
    sys.path.insert(0, phase_3_dir)

from .openai_intent_parser import OpenAIIntentParser
from .entity_extractor import EntityExtractor

# Now import the process_nlp_request function
try:
    from mcp_server.server import process_nlp_request
except ImportError as e:
    print(f"Error importing process_nlp_request: {e}")
    print("Attempting to import from absolute path...")

    # Try to import from the absolute path
    mcp_server_dir = os.path.join(phase_3_dir, 'mcp_server')
    if mcp_server_dir not in sys.path:
        sys.path.insert(0, mcp_server_dir)

    try:
        from server import process_nlp_request
    except ImportError:
        print("Error: Could not import process_nlp_request. Creating mock function.")

        # Create a mock function if import fails
        async def process_nlp_request(user_input: str, auth_token: str) -> dict:
            return {
                "success": False,
                "result": {
                    "message": "MCP server is currently unavailable. Please check if the server is running.",
                    "action_taken": "none",
                    "todo": None,
                    "error": "Import error - service unavailable"
                },
                "intent": "ERROR",
                "entities": {}
            }


class EnhancedChatInterface:
    """Main interface for the AI chatbot with OpenAI integration"""

    def __init__(self):
        self.openai_intent_parser = OpenAIIntentParser()
        self.entity_extractor = EntityExtractor()

    async def process_user_input(self, user_input: str, auth_token: str, conversation_id: str = None) -> Dict[str, Any]:
        """
        Process user input and return an appropriate response using OpenAI

        Args:
            user_input: Natural language input from the user
            auth_token: Authentication token for backend API calls
            conversation_id: Optional conversation ID for context

        Returns:
            Dictionary with response and action information
        """
        try:
            # Parse intent from user input using OpenAI
            intent = self.openai_intent_parser.classify_intent(user_input)

            # Extract entities from user input using OpenAI
            entities = self.openai_intent_parser.extract_entities_openai(user_input)

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

            result = await process_nlp_request(user_input, auth_token)
            result["intent"] = intent
            result["entities"] = entities

            # Format the response based on the result
            if result["success"]:
                response = {
                    "success": True,
                    "message": result.get("result", {}).get("message", "Operation completed successfully"),
                    "intent": result.get("intent", "UNKNOWN"),
                    "entities": result.get("entities", {}),
                    "action_taken": result.get("result", {}).get("action_taken", "unknown"),
                    "data": result.get("result", {}).get("todo") or result.get("result", {}).get("todos")
                }
            else:
                response = {
                    "success": False,
                    "message": result.get("result", {}).get("error", "Sorry, I couldn't process your request"),
                    "intent": result.get("intent", "UNKNOWN"),
                    "entities": result.get("entities", {}),
                    "error": result.get("result", {}).get("error", "Processing failed")
                }

            return response

        except Exception as e:
            return {
                "success": False,
                "message": "Sorry, I encountered an error processing your request",
                "error": str(e),
                "intent": "ERROR",
                "entities": {}
            }

    def get_supported_intents(self) -> Dict[str, str]:
        """
        Get a list of supported intents with descriptions

        Returns:
            Dictionary mapping intents to descriptions
        """
        return {
            "CREATE_TODO": "Add a new todo to your list (e.g., 'Add buy groceries to my list')",
            "READ_TODOS": "View your existing todos (e.g., 'Show my todos' or 'What do I have to do?')",
            "UPDATE_TODO": "Update an existing todo (e.g., 'Mark buy groceries as complete')",
            "DELETE_TODO": "Remove a todo from your list (e.g., 'Delete the meeting with John')"
        }


# Global enhanced chat interface instance
enhanced_chat_interface = EnhancedChatInterface()