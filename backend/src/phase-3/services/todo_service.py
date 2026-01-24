"""Todo Service for Phase III AI Chatbot

This module provides business logic for todo operations
using the API adapter to communicate with Phase II backend.
"""

from typing import Dict, Any, List, Optional
import sys
import os

# Add the phase-3 directory to the path to allow absolute imports
phase3_dir = os.path.dirname(os.path.dirname(__file__))
if phase3_dir not in sys.path:
    sys.path.insert(0, phase3_dir)

from adapters.todo_api_adapter import todo_api_adapter
from adapters.auth_adapter import auth_adapter


class TodoService:
    """Service layer for todo operations"""

    def __init__(self):
        self.api_adapter = todo_api_adapter
        self.auth_adapter = auth_adapter

    async def create_todo(self, title: str, description: str = "", due_date: Optional[str] = None,
                         status: str = "PENDING", priority: str = "MEDIUM", tags: List[str] = None,
                         completed: bool = False, auth_token: str = "") -> Dict[str, Any]:
        """
        Create a new todo

        Args:
            title: Title of the todo
            description: Description of the todo
            due_date: Due date in YYYY-MM-DD format
            status: Status of the todo
            priority: Priority level
            tags: List of tags
            auth_token: Authentication token

        Returns:
            Result of the operation
        """
        # Validate inputs
        if not title or len(title.strip()) == 0:
            return {
                "success": False,
                "error": "Todo title cannot be empty"
            }

        if len(title) > 200:
            return {
                "success": False,
                "error": "Todo title is too long (max 200 characters)"
            }

        # Call the API adapter to create the todo
        result = await self.api_adapter.create_todo(
            title=title,
            description=description,
            due_date=due_date,
            completed=completed,
            auth_token=auth_token
        )

        return result

    async def get_todos(self, auth_token: str = "", status_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Get user's todos

        Args:
            auth_token: Authentication token
            status_filter: Optional status filter

        Returns:
            Result of the operation
        """
        result = await self.api_adapter.list_todos(
            auth_token=auth_token,
            status_filter=status_filter
        )

        return result

    async def update_todo(self, todo_id: str, title: Optional[str] = None,
                         description: Optional[str] = None, due_date: Optional[str] = None,
                         status: Optional[str] = None, priority: Optional[str] = None,
                         auth_token: str = "") -> Dict[str, Any]:
        """
        Update an existing todo

        Args:
            todo_id: ID of the todo to update
            title: New title (optional)
            description: New description (optional)
            due_date: New due date (optional)
            status: New status (optional)
            priority: New priority (optional)
            auth_token: Authentication token

        Returns:
            Result of the operation
        """
        # Validate todo ID
        if not todo_id or len(todo_id.strip()) == 0:
            return {
                "success": False,
                "error": "Invalid todo ID"
            }

        result = await self.api_adapter.update_todo(
            todo_id=todo_id,
            title=title,
            description=description,
            due_date=due_date,
            status=status,
            priority=priority,
            auth_token=auth_token
        )

        return result

    async def delete_todo(self, todo_id: str, auth_token: str = "") -> Dict[str, Any]:
        """
        Delete a todo

        Args:
            todo_id: ID of the todo to delete
            auth_token: Authentication token

        Returns:
            Result of the operation
        """
        # Validate todo ID
        if not todo_id or len(todo_id.strip()) == 0:
            return {
                "success": False,
                "error": "Invalid todo ID"
            }

        result = await self.api_adapter.delete_todo(
            todo_id=todo_id,
            auth_token=auth_token
        )

        return result

    async def toggle_todo_status(self, todo_id: str, auth_token: str = "") -> Dict[str, Any]:
        """
        Toggle the completion status of a todo

        Args:
            todo_id: ID of the todo to toggle
            auth_token: Authentication token

        Returns:
            Result of the operation
        """
        # Validate todo ID
        if not todo_id or len(todo_id.strip()) == 0:
            return {
                "success": False,
                "error": "Invalid todo ID"
            }

        result = await self.api_adapter.toggle_todo_status(
            todo_id=todo_id,
            auth_token=auth_token
        )

        return result

    async def find_todo_by_title(self, title: str, auth_token: str = "") -> Dict[str, Any]:
        """
        Find a todo by title (case-insensitive partial match)

        Args:
            title: Title to search for
            auth_token: Authentication token

        Returns:
            Found todo or None
        """
        if not title:
            return {
                "success": False,
                "error": "Title cannot be empty"
            }

        # Get all todos
        todos_result = await self.get_todos(auth_token=auth_token)

        if not todos_result["success"]:
            return todos_result

        todos = todos_result["data"]

        # Search for partial matches
        for todo in todos:
            if title.lower() in todo.get("title", "").lower():
                return {
                    "success": True,
                    "data": todo
                }

        return {
            "success": False,
            "error": f"No todo found with title containing '{title}'"
        }


# Global todo service instance
todo_service = TodoService()