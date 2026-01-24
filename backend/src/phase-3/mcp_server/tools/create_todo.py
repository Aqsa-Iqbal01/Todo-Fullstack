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
            title = user_input

            # Remove common command verbs
            title = re.sub(r'\b(add|create|make|new|put|set|need to|want to|have to|must|should)\b', '', title, flags=re.IGNORECASE)

            # Remove common noun phrases related to todos
            title = re.sub(r'\b(todo|task|item|thing|grocery|shopping|list|to my|on my|in my)\b', '', title, flags=re.IGNORECASE)

            # Remove common prepositions that might remain
            title = re.sub(r'\b(to|on|in|at|by|for|with|from)\b', '', title, flags=re.IGNORECASE)

            # Clean up extra whitespace and punctuation
            title = title.strip(' ,.')

        # Extract other entities
        due_date = entities.get("due_date", [None])[0] if entities.get("due_date") else None
        priority = entities.get("priority", ["MEDIUM"])[0] if entities.get("priority") else "MEDIUM"

        # Use default values if no entities found
        description = ""  # No description extracted from simple commands
        status = "PENDING"  # Default status for new todos

        # Validate that we have a title
        if not title or not title.strip():
            # Try a more comprehensive extraction method
            import re

            # Pattern to match the main content after common commands
            patterns = [
                r'(?:add|create|make|new|put|set)\s+(.+?)(?:\s+to|\s+in|\s+on|\s+my|\s+the|$|,|\.|and)',
                r'(?:add|create|make|new|put|set)\s+(.+)',
                r'(?:buy|get|do|finish|complete|call|send|order|prepare|schedule|attend|watch|read|write)\s+(.+?)(?:\s+by|\s+for|\s+on|\s+at|\s+to|\s+from|\s+before|\s+after|,|\.|$)',
            ]

            for pattern in patterns:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    extracted_title = match.group(1).strip()
                    if extracted_title and len(extracted_title) > 0:
                        title = extracted_title
                        break

        # Final validation
        if not title or not title.strip():
            return {
                "success": False,
                "error": f"Could not determine a title for the new todo from your input: '{user_input}'. Please try a format like 'Add [your task] to my list'.",
                "original_input": user_input,
                "extracted_entities": entities
            }

        # Clean up the title
        title = title.strip().strip('.,!?').strip()

        # Call the todo service to create the todo
        result = await todo_service.create_todo(
            title=title,
            description=description,
            due_date=due_date,
            completed=False,  # New todos are not completed by default
            auth_token=auth_token
        )

        if result["success"]:
            return {
                "success": True,
                "message": f"I've added '{title}' to your todo list.",
                "todo": result["data"],
                "operation_result": result["data"],  # Add this to match other tools
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