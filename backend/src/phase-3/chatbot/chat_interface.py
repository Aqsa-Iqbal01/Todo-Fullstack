"""Chat Interface for Phase III AI Chatbot

This module provides the main interface for the AI chatbot
that processes natural language input using MCP tools.
"""

import asyncio
import httpx
from typing import Dict, Any
from .intent_parser import IntentParser
from .entity_extractor import EntityExtractor
import sys
import os

# Add the phase-3 directory to the Python path so imports work correctly
phase_3_dir = os.path.dirname(os.path.dirname(__file__))
if phase_3_dir not in sys.path:
    sys.path.insert(0, phase_3_dir)

# Try to import OpenAI components for enhanced functionality
openai_available = False
try:
    from .openai_intent_parser import OpenAIIntentParser
    openai_intent_parser = OpenAIIntentParser()
    openai_available = True
    print("OpenAI integration is available")
except Exception as e:
    print(f"OpenAI integration not available: {e}")
    print("Falling back to rule-based parsing")

# Use HTTP client to communicate with MCP server running as a separate service
async def process_nlp_request(user_input: str, auth_token: str, conversation_id: str = None) -> dict:
    """
    Process NLP request by making HTTP call to MCP server
    """
    # Use environment variable or default to localhost:12345 with proper protocol
    mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:12345")

    # Prepare the request payload
    payload = {"input": user_input}
    if conversation_id:
        payload["conversation_id"] = conversation_id

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Clean and format the auth token properly
            clean_auth_token = auth_token.strip()
            if clean_auth_token.lower().startswith('bearer '):
                clean_auth_token = clean_auth_token[7:].strip()
            elif clean_auth_token.startswith('Bearer '):
                clean_auth_token = clean_auth_token[7:].strip()

            response = await client.post(
                f"{mcp_server_url}/mcp/process_nlp",
                json=payload,
                headers={
                    "Authorization": f"Bearer {clean_auth_token}",
                    "Content-Type": "application/json"
                }
            )

            if response.status_code == 200:
                result = response.json()
                return result
            else:
                return {
                    "success": False,
                    "result": {
                        "message": f"MCP server returned error: {response.status_code}",
                        "action_taken": "none",
                        "todo": None,
                        "error": f"HTTP {response.status_code}: {response.text}"
                    },
                    "intent": "ERROR",
                    "entities": {}
                }
    except Exception as e:
        return {
            "success": False,
            "result": {
                "message": f"MCP server is currently unavailable. Please check if the server is running on {mcp_server_url}. Error: {str(e)}",
                "action_taken": "none",
                "todo": None,
                "error": str(e)
            },
            "intent": "ERROR",
            "entities": {}
        }


class ChatInterface:
    """Main interface for the AI chatbot with optional OpenAI enhancement"""

    def __init__(self):
        self.intent_parser = IntentParser()
        self.entity_extractor = EntityExtractor()

    async def process_user_input(self, user_input: str, auth_token: str, conversation_id: str = None) -> Dict[str, Any]:
        """
        Process user input and return an appropriate response

        Args:
            user_input: Natural language input from the user
            auth_token: Authentication token for backend API calls
            conversation_id: Optional conversation ID for context

        Returns:
            Dictionary with response and action information
        """
        try:
            # First, classify the intent using the intent parser
            # Use OpenAI parser if available, otherwise fall back to local parser
            if openai_available and hasattr(self, 'openai_intent_parser') and self.openai_intent_parser is not None:
                intent = self.openai_intent_parser.classify_intent(user_input)
            else:
                intent = self.intent_parser.classify_intent(user_input)

            # Handle general conversation and greetings specially
            if intent == "GENERAL_CONVERSATION":
                # Provide appropriate responses for greetings and general conversation
                user_input_lower = user_input.lower().strip()

                # Check for greetings
                if any(greeting in user_input_lower for greeting in ['hi', 'hello', 'hey', 'greetings']):
                    return {
                        "success": True,
                        "message": "Hello! I'm your AI assistant. How can I help you manage your todos today?",
                        "intent": "GENERAL_CONVERSATION",
                        "entities": {},
                        "action_taken": "greeting_response"
                    }
                elif any(word in user_input_lower for word in ['help', 'what can', 'what do', 'how can']):
                    return {
                        "success": True,
                        "message": "I can help you manage your todos! You can ask me to: Add new todos (e.g., 'Add buy groceries to my list'), Show your todos (e.g., 'Show my todos'), Update todos (e.g., 'Mark buy groceries as complete'), or Delete todos (e.g., 'Delete the meeting with John').",
                        "intent": "GENERAL_CONVERSATION",
                        "entities": {},
                        "action_taken": "help_response"
                    }
                else:
                    # For other general conversation, provide a default response
                    return {
                        "success": True,
                        "message": "I'm your AI assistant for managing todos. You can ask me to add, show, update, or delete your tasks. For example: 'Add buy groceries to my list'.",
                        "intent": "GENERAL_CONVERSATION",
                        "entities": {},
                        "action_taken": "general_response"
                    }

            # For other intents, process through the MCP system
            result = await process_nlp_request(user_input, auth_token, conversation_id)

            # Format the response based on the result
            if result["success"]:
                response = {
                    "success": True,
                    "message": result.get("result", {}).get("message", "Operation completed successfully"),
                    "intent": result.get("intent", "UNKNOWN"),
                    "entities": result.get("entities", {}),
                    "action_taken": result.get("result", {}).get("action_taken", "unknown"),
                    "data": result.get("result", {}).get("todo") or result.get("result", {}).get("operation_result") or result.get("result", {}).get("todos")
                }
            else:
                # Check if the intent was UNKNOWN and provide a more helpful response
                if result.get("intent") == "UNKNOWN":
                    response = {
                        "success": True,
                        "message": "I'm not sure I understood that. I can help you manage your todos! Try commands like: 'Add buy groceries to my list', 'Show my todos', 'Mark buy groceries as complete', or 'Delete the meeting with John'.",
                        "intent": "UNKNOWN",
                        "entities": result.get("entities", {}),
                        "error": result.get("result", {}).get("error", "Processing failed")
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
            "DELETE_TODO": "Remove a todo from your list (e.g., 'Delete the meeting with John')",
            "GENERAL_CONVERSATION": "Handle greetings and general conversation (e.g., 'Hi', 'Hello', 'What can you do?')"
        }


# Global chat interface instance
chat_interface = ChatInterface()