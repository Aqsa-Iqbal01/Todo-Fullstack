"""MCP Tool for Deleting Todos

This module implements the delete_todo MCP tool that interfaces
with the todo service to delete existing todo items.
"""

from typing import Dict, Any
import sys
import os

# Add the phase-3 directory to the path to allow absolute imports
phase3_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if phase3_dir not in sys.path:
    sys.path.insert(0, phase3_dir)

from services.todo_service import todo_service


async def delete_todo_tool(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool for deleting a todo

    Args:
        parameters: Parameters from the MCP request including:
                    - user_input: Original user input
                    - entities: Extracted entities from the input
                    - auth_token: Authentication token for API calls

    Returns:
        Result of the delete operation
    """
    try:
        # Extract parameters
        user_input = parameters.get("user_input", "")
        entities = parameters.get("entities", {})
        auth_token = parameters.get("auth_token", "")

        # Extract potential todo titles from entities
        todo_titles = entities.get("todo_title", [])

        if todo_titles:
            # Try to find and delete the first matching todo
            title_to_delete = todo_titles[0]  # Use the first title found

            # Find the todo by title
            find_result = await todo_service.find_todo_by_title(
                title=title_to_delete,
                auth_token=auth_token
            )

            if find_result["success"]:
                todo = find_result["data"]
                todo_id = todo.get("id")
                todo_title = todo.get("title", title_to_delete)

                # Delete the todo
                result = await todo_service.delete_todo(
                    todo_id=todo_id,
                    auth_token=auth_token
                )

                if result["success"]:
                    return {
                        "success": True,
                        "message": f"I've removed '{todo_title}' from your todo list.",
                        "operation_result": {"deleted_todo_id": todo_id, "title": todo_title},  # Key fix
                        "deleted_todo_id": todo_id,
                        "action_taken": "delete_todo",
                        "original_input": user_input
                    }
                else:
                    return {
                        "success": False,
                        "error": result.get("error", f"Failed to remove '{todo_title}' from your list"),
                        "original_input": user_input
                    }
            else:
                return {
                    "success": False,
                    "error": f"I couldn't find a todo with title containing '{title_to_delete}'.",
                    "original_input": user_input
                }
        else:
            # If no specific title was extracted, try to extract it from the user input
            import re

            # Look for common delete patterns
            delete_patterns = [
                r'(?:delete|remove|cancel|clear|eliminate|get rid of)\s+(.+?)(?:\s+from|\s+off|\s+on|\s+the|\s+my|\s*$|,|\.|and)',
                r'(?:delete|remove)\s+(?:the\s+)?(.+?)(?:\s+todo|task|item|from\s+my\s+list|\s+list|$)',
            ]

            for pattern in delete_patterns:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    title_to_delete = match.group(1).strip()

                    # Find the todo by the extracted title
                    find_result = await todo_service.find_todo_by_title(
                        title=title_to_delete,
                        auth_token=auth_token
                    )

                    if find_result["success"]:
                        todo = find_result["data"]
                        todo_id = todo.get("id")

                        # Delete the todo
                        result = await todo_service.delete_todo(
                            todo_id=todo_id,
                            auth_token=auth_token
                        )

                        if result["success"]:
                            return {
                                "success": True,
                                "message": f"I've removed '{title_to_delete}' from your todo list.",
                                "operation_result": {"deleted_todo_id": todo_id, "title": title_to_delete},  # Key fix
                                "deleted_todo_id": todo_id,
                                "action_taken": "delete_todo",
                                "original_input": user_input
                            }
                        else:
                            return {
                                "success": False,
                                "error": result.get("error", f"Failed to remove '{title_to_delete}' from your list"),
                                "original_input": user_input
                            }
                    else:
                        return {
                            "success": False,
                            "error": f"I couldn't find a todo with title containing '{title_to_delete}'.",
                            "original_input": user_input
                        }

            # If we still couldn't find a specific todo, return an error
            return {
                "success": False,
                "error": "I couldn't identify which todo you'd like to remove. Please specify the title of the todo you want to delete.",
                "original_input": user_input
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error in delete_todo tool: {str(e)}",
            "original_input": parameters.get("user_input", "")
        }