"""MCP Tool for Listing Todos

This module implements the list_todos MCP tool that interfaces
with the todo service to retrieve user's todo items.
"""

from typing import Dict, Any
import sys
import os

# Add the phase-3 directory to the path to allow absolute imports
phase3_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if phase3_dir not in sys.path:
    sys.path.insert(0, phase3_dir)

from services.todo_service import todo_service


async def list_todos_tool(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool for listing todos

    Args:
        parameters: Parameters from the MCP request including:
                    - user_input: Original user input
                    - entities: Extracted entities from the input
                    - auth_token: Authentication token for API calls

    Returns:
        Result of the list operation
    """
    try:
        # Extract parameters
        user_input = parameters.get("user_input", "")
        entities = parameters.get("entities", {})
        auth_token = parameters.get("auth_token", "")

        # Determine if user wants to filter by status
        status_filter = None
        user_input_lower = user_input.lower()

        # Check for status-related keywords in the input
        if any(keyword in user_input_lower for keyword in ['completed', 'done', 'finished']):
            status_filter = 'COMPLETED'
        elif any(keyword in user_input_lower for keyword in ['pending', 'incomplete', 'not done']):
            status_filter = 'PENDING'
        elif any(keyword in user_input_lower for keyword in ['in progress', 'active']):
            status_filter = 'IN_PROGRESS'

        # Call the todo service to get the todos
        result = await todo_service.get_todos(
            auth_token=auth_token,
            status_filter=status_filter
        )

        if result["success"]:
            todos = result["data"]

            if not todos:
                if status_filter:
                    message = f"You don't have any {status_filter.lower()} todos on your list."
                else:
                    message = "You don't have any todos on your list."

                return {
                    "success": True,
                    "message": message,
                    "todos": [],
                    "count": 0,
                    "action_taken": "list_todos",
                    "original_input": user_input,
                    "status_filter": status_filter
                }

            # Create a user-friendly message
            if status_filter:
                message = f"You have {len(todos)} {status_filter.lower()} todo{'s' if len(todos) != 1 else ''}: "
            else:
                message = f"You have {len(todos)} todo{'s' if len(todos) != 1 else ''}: "

            # Limit to first 5 todos in the message for readability
            todo_titles = [todo.get("title", "Untitled") for todo in todos[:5]]
            message += ", ".join(todo_titles)

            if len(todos) > 5:
                message += f" and {len(todos) - 5} more."

            return {
                "success": True,
                "message": message,
                "todos": todos,
                "count": len(todos),
                "action_taken": "list_todos",
                "original_input": user_input,
                "status_filter": status_filter
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Failed to retrieve todos"),
                "original_input": user_input
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error in list_todos tool: {str(e)}",
            "original_input": parameters.get("user_input", "")
        }