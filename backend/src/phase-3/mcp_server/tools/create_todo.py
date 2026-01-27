"""MCP Tool for Creating Todos

This module implements the create_todo MCP tool that interfaces
with the todo service to create new todo items.
"""

from typing import Dict, Any
import sys
import os

# Add the phase-3 directory to the path to allow absolute imports
phase3_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if phase3_dir not in sys.path:
    sys.path.insert(0, phase3_dir)

from services.todo_service import todo_service


async def create_todo_tool(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool for creating a new todo

    Args:
        parameters: Parameters from the MCP request including:
                    - user_input: Original user input
                    - entities: Extracted entities from the input
                    - auth_token: Authentication token for API calls

    Returns:
        Result of the create operation
    """
    try:
        # Extract parameters
        user_input = parameters.get("user_input", "")
        entities = parameters.get("entities", {})
        auth_token = parameters.get("auth_token", "")

        # Extract todo title from entities or derive from user input
        title = ""
        if "todo_title" in entities and len(entities["todo_title"]) > 0:
            title = entities["todo_title"][0]  # Take the first extracted title
        else:
            # Derive title from user input if not explicitly extracted
            # Remove common command words to isolate the title
            import re
            title = re.sub(r'\b(add|create|make|new|put|set)\b', '', user_input, flags=re.IGNORECASE)
            title = re.sub(r'\b(todo|task|item|thing|grocery|shopping|list)\b', '', title, flags=re.IGNORECASE)
            title = title.strip(' ,.')

        # Extract other entities
        due_date = entities.get("due_date", [None])[0] if entities.get("due_date") else None
        priority = entities.get("priority", ["MEDIUM"])[0] if entities.get("priority") else "MEDIUM"

        # Use default values if no entities found
        description = ""  # No description extracted from simple commands
        status = "PENDING"  # Default status for new todos

        # Validate that we have a title
        if not title:
            return {
                "success": False,
                "error": "Could not determine a title for the new todo from your input",
                "original_input": user_input,
                "extracted_entities": entities
            }

        # Call the todo service to create the todo
        # Note: The service and underlying models only support title, description, due_date
        # Status and priority are not supported by the TodoCreate model
        result = await todo_service.create_todo(
            title=title,
            description=description,
            due_date=due_date,
            auth_token=auth_token
            # status and priority are not supported by the underlying data model
        )

        if result["success"]:
            return {
                "success": True,
                "message": f"I've added '{title}' to your todo list.",
                "todo": result["data"],
                "action_taken": "create_todo",
                "original_input": user_input
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Failed to create todo"),
                "original_input": user_input
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error in create_todo tool: {str(e)}",
            "original_input": parameters.get("user_input", "")
        }