"""MCP Tool for Updating Todos

This module implements the update_todo MCP tool that interfaces
with the todo service to update existing todo items.
"""
from typing import Dict, Any
import sys
import os

# Add the phase-3 directory to the path to allow absolute imports
phase3_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if phase3_dir not in sys.path:
    sys.path.insert(0, phase3_dir)

from services.todo_service import todo_service


async def update_todo_tool(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP tool for updating a todo

    Args:
        parameters: Parameters from the MCP request including:
                    - user_input: Original user input
                    - entities: Extracted entities from the input
                    - auth_token: Authentication token for API calls

    Returns:
        Result of the update operation
    """
    try:
        # Extract parameters
        user_input = parameters.get("user_input", "")
        entities = parameters.get("entities", {})
        auth_token = parameters.get("auth_token", "")

        # Extract entities that might be used for updating
        todo_titles = entities.get("todo_title", [])

        # Determine what needs to be updated based on the user input
        user_input_lower = user_input.lower()

        # Check if this is a completion request
        if any(word in user_input_lower for word in ['complete', 'done', 'finish', 'finished', 'mark as']):
            if todo_titles:
                # Try to find and complete the specified todo
                # Look for the best matching title among the extracted titles
                # Prioritize longer titles first (more specific) that actually exist in the todo list

                # First, get all existing todos to check against
                all_todos_result = await todo_service.get_todos(auth_token=auth_token)
                if all_todos_result["success"]:
                    existing_todos = all_todos_result["data"]
                    existing_titles = [todo.get("title", "").lower() for todo in existing_todos]

                    # Sort titles by length (longest first) to try more specific matches first
                    sorted_titles = sorted(todo_titles, key=len, reverse=True)

                    # Find the best matching title that exists in the user's todo list
                    title_to_complete = None
                    for extracted_title in sorted_titles:
                        # Look for exact match first
                        if extracted_title.lower() in existing_titles:
                            title_to_complete = extracted_title
                            break

                        # If no exact match, look for partial matches
                        for existing_title in existing_titles:
                            if extracted_title.lower() in existing_title or existing_title in extracted_title.lower():
                                # Use the existing title from the database
                                title_to_complete = existing_title
                                break

                        if title_to_complete:
                            break

                    # If we found a matching title, proceed with the update
                    if title_to_complete:
                        # Find the actual todo record using the matching title
                        find_result = await todo_service.find_todo_by_title(
                            title=title_to_complete,
                            auth_token=auth_token
                        )

                        if find_result["success"]:
                            todo = find_result["data"]
                            todo_id = todo.get("id")

                            # Toggle the todo status
                            result = await todo_service.toggle_todo_status(
                                todo_id=todo_id,
                                auth_token=auth_token
                            )

                            if result["success"]:
                                # Use the updated todo from the result, not the original
                                updated_todo = result["data"]
                                action_msg = "marked as complete" if updated_todo.get("completed") else "marked as incomplete"
                                return {
                                    "success": True,
                                    "message": f"I've {action_msg} '{updated_todo.get('title')}'.",
                                    "operation_result": updated_todo,  # This is the key fix
                                    "updated_todo": updated_todo,
                                    "action_taken": "update_todo_status",
                                    "original_input": user_input
                                }
                            else:
                                return {
                                    "success": False,
                                    "error": result.get("error", "Failed to update todo status"),
                                    "original_input": user_input
                                }
                        else:
                            return {
                                "success": False,
                                "error": f"I couldn't find a todo with title containing '{title_to_complete}'.",
                                "original_input": user_input
                            }
                    else:
                        return {
                            "success": False,
                            "error": f"I couldn't find a matching todo in your list. Available titles: {[t['title'] for t in existing_todos][:5]}",
                            "original_input": user_input
                        }
                else:
                    return {
                        "success": False,
                        "error": "Could not retrieve your existing todos to find a match.",
                        "original_input": user_input
                    }
            else:
                return {
                    "success": False,
                    "error": "I couldn't identify which todo you want to mark as complete.",
                    "original_input": user_input
                }

        # Check if this is a general update request (title, due date, etc.)
        elif any(word in user_input_lower for word in ['update', 'change', 'modify', 'edit']):
            if todo_titles:
                # For general updates, try to find the best matching title as well
                all_todos_result = await todo_service.get_todos(auth_token=auth_token)
                if all_todos_result["success"]:
                    existing_todos = all_todos_result["data"]
                    existing_titles = [todo.get("title", "").lower() for todo in existing_todos]

                    # Sort titles by length (longest first) to try more specific matches first
                    sorted_titles = sorted(todo_titles, key=len, reverse=True)

                    # Find the best matching title that exists in the user's todo list
                    target_title = None
                    for extracted_title in sorted_titles:
                        # Look for exact match first
                        if extracted_title.lower() in existing_titles:
                            target_title = extracted_title
                            break

                        # If no exact match, look for partial matches
                        for existing_title in existing_titles:
                            if extracted_title.lower() in existing_title or existing_title in extracted_title.lower():
                                # Use the existing title from the database
                                target_title = existing_title
                                break

                        if target_title:
                            break

                    if target_title:
                        # Find the actual todo record using the matching title
                        find_result = await todo_service.find_todo_by_title(
                            title=target_title,
                            auth_token=auth_token
                        )

                        if find_result["success"]:
                            todo = find_result["data"]
                            todo_id = todo.get("id")

                            # For general updates, we need to extract what specifically to update
                            import re
                            # Look for patterns like "update X to Y" or "change X to Y"
                            update_pattern = r'(?:update|change|modify|edit)\s+(.+?)\s+(?:to|with)\s+(.+)'
                            match = re.search(update_pattern, user_input_lower)

                            if match:
                                new_value = match.group(2).strip()

                                # We'll treat this as a title update for now
                                result = await todo_service.update_todo(
                                    todo_id=todo_id,
                                    title=new_value,
                                    auth_token=auth_token
                                )

                                if result["success"]:
                                    return {
                                        "success": True,
                                        "message": f"I've updated '{target_title}' to '{new_value}'.",
                                        "operation_result": result["data"],  # This is the key fix
                                        "updated_todo": result["data"],
                                        "action_taken": "update_todo_title",
                                        "original_input": user_input
                                    }
                                else:
                                    return {
                                        "success": False,
                                        "error": result.get("error", "Failed to update todo"),
                                        "original_input": user_input
                                    }
                            else:
                                return {
                                    "success": False,
                                    "error": "I couldn't understand what specific update you want to make. Please specify 'update [todo] to [new value]'.",
                                    "original_input": user_input
                                }
                        else:
                            return {
                                "success": False,
                                "error": f"I couldn't find a todo with title containing '{target_title}'.",
                                "original_input": user_input
                            }
                    else:
                        return {
                            "success": False,
                            "error": f"I couldn't find a matching todo in your list. Available titles: {[t['title'] for t in existing_todos][:5]}",
                            "original_input": user_input
                        }
                else:
                    return {
                        "success": False,
                        "error": "Could not retrieve your existing todos to find a match.",
                        "original_input": user_input
                    }
            else:
                # If no specific titles were extracted, try to extract from user input
                import re
                # Look for common update patterns
                update_patterns = [
                    r'(?:update|change|modify|edit)\s+(.+?)\s+(?:to|with)\s+(.+)',
                ]

                for pattern in update_patterns:
                    match = re.search(pattern, user_input, re.IGNORECASE)
                    if match:
                        title_to_update = match.group(1).strip()
                        new_value = match.group(2).strip()

                        # Find the todo by the extracted title
                        find_result = await todo_service.find_todo_by_title(
                            title=title_to_update,
                            auth_token=auth_token
                        )

                        if find_result["success"]:
                            todo = find_result["data"]
                            todo_id = todo.get("id")

                            # Update the todo
                            result = await todo_service.update_todo(
                                todo_id=todo_id,
                                title=new_value,
                                auth_token=auth_token
                            )

                            if result["success"]:
                                return {
                                    "success": True,
                                    "message": f"I've updated '{title_to_update}' to '{new_value}'.",
                                    "operation_result": result["data"],
                                    "updated_todo": result["data"],
                                    "action_taken": "update_todo_title",
                                    "original_input": user_input
                                }
                            else:
                                return {
                                    "success": False,
                                    "error": result.get("error", "Failed to update todo"),
                                    "original_input": user_input
                                }
                        else:
                            return {
                                "success": False,
                                "error": f"I couldn't find a todo with title containing '{title_to_update}'.",
                                "original_input": user_input
                            }

                return {
                    "success": False,
                    "error": "I couldn't identify which todo you'd like to update. Please specify 'update [todo] to [new value]'.",
                    "original_input": user_input
                }
        else:
            return {
                "success": False,
                "error": "I couldn't determine what update you want to make to your todos.",
                "original_input": user_input
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error in update_todo tool: {str(e)}",
            "original_input": parameters.get("user_input", "")
        }