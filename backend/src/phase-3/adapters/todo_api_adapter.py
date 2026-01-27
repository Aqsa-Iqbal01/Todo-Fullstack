"""API Adapter for Phase II Backend Integration

This module handles communication with the Phase II backend APIs
to perform todo operations.
"""

import asyncio
from typing import Dict, Any, List, Optional
import sys
import os
from datetime import datetime

# Add the phase-3 directory to the path to allow absolute imports
phase3_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if phase3_dir not in sys.path:
    sys.path.insert(0, phase3_dir)

from config.settings import settings

# Import the direct service modules instead of making HTTP requests
from ..database.database import get_engine
from ..models.user import User
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..services.todo_service import TodoService as DirectTodoService
from sqlmodel import Session, select
from ..auth.auth_handler import get_current_user
import uuid


class TodoAPIAdapter:
    """Adapter for communicating with Phase II backend APIs"""

    def __init__(self):
        self.base_url = settings.backend_api_url

    async def create_todo(self, title: str, description: str = "", due_date: Optional[str] = None,
                         status: str = "PENDING", priority: str = "MEDIUM", tags: List[str] = None,
                         auth_token: str = "") -> Dict[str, Any]:
        """
        Create a new todo via direct service call

        Args:
            title: Title of the todo
            description: Description of the todo
            due_date: Due date in YYYY-MM-DD format
            status: Status of the todo
            priority: Priority level
            tags: List of tags
            auth_token: Authentication token

        Returns:
            Response from the backend API
        """
        if tags is None:
            tags = []

        try:
            # Validate inputs
            if not title or len(title.strip()) == 0:
                return {
                    "success": False,
                    "error": "Todo title cannot be empty"
                }

            # Authenticate user from token
            if not auth_token or not auth_token.strip():
                return {
                    "success": False,
                    "error": "Authentication token is required"
                }

            # Clean the token by removing any leading/trailing whitespace or Bearer prefix if accidentally included
            clean_token = auth_token.strip()
            if clean_token.startswith('Bearer '):
                clean_token = clean_token[7:]  # Remove 'Bearer ' prefix if present
            elif clean_token.startswith('bearer '):
                clean_token = clean_token[7:]  # Remove 'bearer ' prefix if present

            # Get current user from token
            current_user_email = get_current_user(clean_token)
            if not current_user_email:
                return {
                    "success": False,
                    "error": "Authentication failed: Invalid or expired token. Please log in again."
                }

            # Get user from database
            # Initialize the database engine
            engine = get_engine()
            with Session(engine) as session:
                user = session.exec(select(User).where(User.email == current_user_email)).first()
                if not user:
                    return {
                        "success": False,
                        "error": "User not found"
                    }

                # Create todo using the direct service
                # Note: TodoCreate model only supports title, description, completed, and due_date
                # Status and priority are not supported in the model
                todo_create = TodoCreate(
                    title=title,
                    description=description,
                    due_date=due_date
                    # completed is not passed here since it defaults to False
                )

                todo_service = DirectTodoService(session)
                created_todo = todo_service.create_todo(todo_create, user.id)

                return {
                    "success": True,
                    "data": created_todo,
                    "status_code": 200
                }

        except Exception as e:
            print(f"Error in create_todo: {str(e)}")  # Add logging
            return {
                "success": False,
                "error": f"Failed to create todo: {str(e)}",
                "status_code": None
            }

    async def list_todos(self, auth_token: str = "", status_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve user's todos from the backend API

        Args:
            auth_token: Authentication token
            status_filter: Optional status filter

        Returns:
            Response from the backend API
        """
        try:
            # Authenticate user from token
            if not auth_token or not auth_token.strip():
                return {
                    "success": False,
                    "error": "Authentication token is required"
                }

            # Clean the token by removing any leading/trailing whitespace or Bearer prefix if accidentally included
            clean_token = auth_token.strip()
            if clean_token.startswith('Bearer '):
                clean_token = clean_token[7:]  # Remove 'Bearer ' prefix if present
            elif clean_token.startswith('bearer '):
                clean_token = clean_token[7:]  # Remove 'bearer ' prefix if present

            # Get current user from token
            current_user_email = get_current_user(clean_token)
            if not current_user_email:
                return {
                    "success": False,
                    "error": "Authentication failed: Invalid or expired token. Please log in again."
                }

            # Get user from database
            # Initialize the database engine
            engine = get_engine()
            with Session(engine) as session:
                user = session.exec(select(User).where(User.email == current_user_email)).first()
                if not user:
                    return {
                        "success": False,
                        "error": "User not found"
                    }

                # Get todos using the direct service
                todo_service = DirectTodoService(session)
                todos = todo_service.get_user_todos(user.id)

                # Apply status filter if specified
                if status_filter:
                    todos = [todo for todo in todos if hasattr(todo, 'status') and todo.status.lower() == status_filter.lower()]

                return {
                    "success": True,
                    "data": todos,
                    "status_code": 200
                }

        except Exception as e:
            print(f"Error in list_todos: {str(e)}")  # Add logging
            return {
                "success": False,
                "error": f"Failed to retrieve todos: {str(e)}",
                "status_code": None
            }

    async def update_todo(self, todo_id: str, title: Optional[str] = None,
                         description: Optional[str] = None, due_date: Optional[str] = None,
                         status: Optional[str] = None, priority: Optional[str] = None,
                         auth_token: str = "") -> Dict[str, Any]:
        """
        Update an existing todo via direct service call

        Args:
            todo_id: ID of the todo to update
            title: New title (optional)
            description: New description (optional)
            due_date: New due date (optional)
            status: New status (optional)
            priority: New priority (optional)
            auth_token: Authentication token

        Returns:
            Response from the backend API
        """
        try:
            # Validate inputs
            if not todo_id:
                return {
                    "success": False,
                    "error": "Todo ID is required"
                }

            # Convert string ID to UUID
            try:
                todo_uuid = uuid.UUID(todo_id)
            except ValueError:
                return {
                    "success": False,
                    "error": "Invalid todo ID format"
                }

            # Authenticate user from token
            if not auth_token or not auth_token.strip():
                return {
                    "success": False,
                    "error": "Authentication token is required"
                }

            # Clean the token by removing any leading/trailing whitespace or Bearer prefix if accidentally included
            clean_token = auth_token.strip()
            if clean_token.startswith('Bearer '):
                clean_token = clean_token[7:]  # Remove 'Bearer ' prefix if present
            elif clean_token.startswith('bearer '):
                clean_token = clean_token[7:]  # Remove 'bearer ' prefix if present

            # Get current user from token
            current_user_email = get_current_user(clean_token)
            if not current_user_email:
                return {
                    "success": False,
                    "error": "Authentication failed: Invalid or expired token. Please log in again."
                }

            # Get user from database
            # Initialize the database engine
            engine = get_engine()
            with Session(engine) as session:
                user = session.exec(select(User).where(User.email == current_user_email)).first()
                if not user:
                    return {
                        "success": False,
                        "error": "User not found"
                    }

                # Prepare update data - need to match the TodoUpdate model fields
                update_data = {}
                if title is not None:
                    update_data["title"] = title
                if description is not None:
                    update_data["description"] = description
                if due_date is not None:
                    update_data["due_date"] = due_date
                # Note: TodoUpdate model doesn't have status and priority fields, only completed
                # For now, let's only update the fields that exist in TodoUpdate model

                # Update todo using the direct service
                todo_update = TodoUpdate(**update_data)

                todo_service = DirectTodoService(session)
                updated_todo = todo_service.update_todo(todo_uuid, todo_update, user.id)

                if updated_todo:
                    return {
                        "success": True,
                        "data": updated_todo,
                        "status_code": 200
                    }
                else:
                    return {
                        "success": False,
                        "error": "Todo not found or not authorized to update"
                    }

        except Exception as e:
            print(f"Error in update_todo: {str(e)}")  # Add logging
            return {
                "success": False,
                "error": f"Failed to update todo: {str(e)}",
                "status_code": None
            }

    async def delete_todo(self, todo_id: str, auth_token: str = "") -> Dict[str, Any]:
        """
        Delete a todo via direct service call

        Args:
            todo_id: ID of the todo to delete
            auth_token: Authentication token

        Returns:
            Response from the backend API
        """
        try:
            # Validate inputs
            if not todo_id:
                return {
                    "success": False,
                    "error": "Todo ID is required"
                }

            # Convert string ID to UUID
            try:
                todo_uuid = uuid.UUID(todo_id)
            except ValueError:
                return {
                    "success": False,
                    "error": "Invalid todo ID format"
                }

            # Authenticate user from token
            if not auth_token or not auth_token.strip():
                return {
                    "success": False,
                    "error": "Authentication token is required"
                }

            # Clean the token by removing any leading/trailing whitespace or Bearer prefix if accidentally included
            clean_token = auth_token.strip()
            if clean_token.startswith('Bearer '):
                clean_token = clean_token[7:]  # Remove 'Bearer ' prefix if present
            elif clean_token.startswith('bearer '):
                clean_token = clean_token[7:]  # Remove 'bearer ' prefix if present

            # Get current user from token
            current_user_email = get_current_user(clean_token)
            if not current_user_email:
                return {
                    "success": False,
                    "error": "Authentication failed: Invalid or expired token. Please log in again."
                }

            # Get user from database
            # Initialize the database engine
            engine = get_engine()
            with Session(engine) as session:
                user = session.exec(select(User).where(User.email == current_user_email)).first()
                if not user:
                    return {
                        "success": False,
                        "error": "User not found"
                    }

                # Delete todo using the direct service
                todo_service = DirectTodoService(session)
                deleted = todo_service.delete_todo(todo_uuid, user.id)

                if deleted:
                    return {
                        "success": True,
                        "data": None,
                        "status_code": 200
                    }
                else:
                    return {
                        "success": False,
                        "error": "Todo not found or not authorized to delete"
                    }

        except Exception as e:
            print(f"Error in delete_todo: {str(e)}")  # Add logging
            return {
                "success": False,
                "error": f"Failed to delete todo: {str(e)}",
                "status_code": None
            }

    async def toggle_todo_status(self, todo_id: str, auth_token: str = "") -> Dict[str, Any]:
        """
        Toggle the completion status of a todo

        Args:
            todo_id: ID of the todo to toggle
            auth_token: Authentication token

        Returns:
            Response from the backend API
        """
        try:
            # Validate inputs
            if not todo_id:
                return {
                    "success": False,
                    "error": "Todo ID is required"
                }

            # Convert string ID to UUID
            try:
                todo_uuid = uuid.UUID(todo_id)
            except ValueError:
                return {
                    "success": False,
                    "error": "Invalid todo ID format"
                }

            # Authenticate user from token
            if not auth_token or not auth_token.strip():
                return {
                    "success": False,
                    "error": "Authentication token is required"
                }

            # Clean the token by removing any leading/trailing whitespace or Bearer prefix if accidentally included
            clean_token = auth_token.strip()
            if clean_token.startswith('Bearer '):
                clean_token = clean_token[7:]  # Remove 'Bearer ' prefix if present
            elif clean_token.startswith('bearer '):
                clean_token = clean_token[7:]  # Remove 'bearer ' prefix if present

            # Get current user from token
            current_user_email = get_current_user(clean_token)
            if not current_user_email:
                return {
                    "success": False,
                    "error": "Authentication failed: Invalid or expired token. Please log in again."
                }

            # Get user from database
            # Initialize the database engine
            engine = get_engine()
            with Session(engine) as session:
                user = session.exec(select(User).where(User.email == current_user_email)).first()
                if not user:
                    return {
                        "success": False,
                        "error": "User not found"
                    }

                # Toggle todo status using the direct service
                todo_service = DirectTodoService(session)
                toggled_todo = todo_service.toggle_todo_completion(todo_uuid, user.id)

                if toggled_todo:
                    return {
                        "success": True,
                        "data": toggled_todo,
                        "status_code": 200
                    }
                else:
                    return {
                        "success": False,
                        "error": "Todo not found or not authorized to toggle"
                    }

        except Exception as e:
            print(f"Error in toggle_todo_status: {str(e)}")  # Add logging
            return {
                "success": False,
                "error": f"Failed to toggle todo status: {str(e)}",
                "status_code": None
            }


# Global adapter instance
todo_api_adapter = TodoAPIAdapter()