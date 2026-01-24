"""API Adapter for Phase II Backend Integration

This module handles communication with the Phase II backend APIs
to perform todo operations.
"""

import httpx
import asyncio
from typing import Dict, Any, List, Optional
import sys
import os

# Add the phase-3 directory to the path to allow absolute imports
phase3_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if phase3_dir not in sys.path:
    sys.path.insert(0, phase3_dir)

from config.settings import settings


class TodoAPIAdapter:
    """Adapter for communicating with Phase II backend APIs"""

    def __init__(self):
        self.base_url = settings.backend_api_url

    async def create_todo(self, title: str, description: str = "", due_date: Optional[str] = None,
                         completed: bool = False, auth_token: str = "") -> Dict[str, Any]:
        """
        Create a new todo via the backend API

        Args:
            title: Title of the todo
            description: Description of the todo
            due_date: Due date in YYYY-MM-DD format
            completed: Whether the todo is completed
            auth_token: Authentication token

        Returns:
            Response from the backend API
        """

        url = f"{self.base_url}/todos/"

        headers = {
            "Content-Type": "application/json",
        }

        # Add Authorization header if token is valid
        # Ensure token is not empty, None, or just whitespace
        if auth_token and auth_token.strip():
            # Clean the token by removing any leading/trailing whitespace or Bearer prefix if accidentally included
            clean_token = auth_token.strip()
            if clean_token.lower().startswith('bearer '):
                clean_token = clean_token[7:].strip()  # Remove 'Bearer ' prefix if present
            elif clean_token.startswith('Bearer '):
                clean_token = clean_token[7:].strip()  # Remove 'Bearer ' prefix if present

            headers["Authorization"] = f"Bearer {clean_token}"
            print(f"DEBUG: Setting authorization header with cleaned token length: {len(clean_token)}")  # Debug print
        else:
            print(f"DEBUG: auth_token is empty or invalid: '{auth_token}'")
            print(f"DEBUG: auth_token type: {type(auth_token)}")
            print(f"DEBUG: This may cause authentication failure when calling {url}")

        payload = {
            "title": title,
            "description": description,
            "due_date": due_date,
            "completed": completed  # Use the passed value
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload, headers=headers)

                if response.status_code in [200, 201]:
                    return {
                        "success": True,
                        "data": response.json(),
                        "status_code": response.status_code
                    }
                else:
                    # Log detailed error information for debugging
                    print(f"DEBUG: API call failed with status {response.status_code}")
                    print(f"DEBUG: Response text: {response.text}")
                    print(f"DEBUG: Request URL: {url}")
                    print(f"DEBUG: Headers sent: {dict(headers)}")  # Don't print the actual token for security

                    if response.status_code == 401:
                        return {
                            "success": False,
                            "error": "Authentication failed: Invalid or expired token. Please log in again.",
                            "status_code": response.status_code,
                            "data": response.text
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"Failed to create todo: {response.text}",
                            "status_code": response.status_code,
                            "data": response.text
                        }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
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
        url = f"{self.base_url}/todos/"

        headers = {}

        # Add Authorization header if token is valid
        # Ensure token is not empty, None, or just whitespace
        if auth_token and auth_token.strip():
            # Clean the token by removing any leading/trailing whitespace or Bearer prefix if accidentally included
            clean_token = auth_token.strip()
            if clean_token.lower().startswith('bearer '):
                clean_token = clean_token[7:].strip()  # Remove 'Bearer ' prefix if present
            elif clean_token.startswith('Bearer '):
                clean_token = clean_token[7:].strip()  # Remove 'Bearer ' prefix if present

            headers["Authorization"] = f"Bearer {clean_token}"
            print(f"DEBUG: Setting authorization header with cleaned token length: {len(clean_token)}")  # Debug print
        else:
            print(f"DEBUG: auth_token is empty or invalid: '{auth_token}'")
            print(f"DEBUG: auth_token type: {type(auth_token)}")
            print(f"DEBUG: This may cause authentication failure when calling {url}")

        params = {}
        if status_filter:
            params["status"] = status_filter

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers, params=params)

                if response.status_code == 200:
                    todos = response.json()

                    # Apply additional filtering if needed
                    if status_filter:
                        todos = [todo for todo in todos if todo.get('status', '').lower() == status_filter.lower()]

                    return {
                        "success": True,
                        "data": todos,
                        "status_code": response.status_code
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to retrieve todos: {response.text}",
                        "status_code": response.status_code,
                        "data": response.text
                    }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
                "status_code": None
            }

    async def update_todo(self, todo_id: int, title: Optional[str] = None,
                         description: Optional[str] = None, due_date: Optional[str] = None,
                         status: Optional[str] = None, priority: Optional[str] = None,
                         auth_token: str = "") -> Dict[str, Any]:
        """
        Update an existing todo via the backend API

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
        url = f"{self.base_url}/todos/{todo_id}"

        headers = {
            "Content-Type": "application/json",
        }

        # Add Authorization header if token is valid
        # Ensure token is not empty, None, or just whitespace
        if auth_token and auth_token.strip():
            # Clean the token by removing any leading/trailing whitespace or Bearer prefix if accidentally included
            clean_token = auth_token.strip()
            if clean_token.lower().startswith('bearer '):
                clean_token = clean_token[7:].strip()  # Remove 'Bearer ' prefix if present
            elif clean_token.startswith('Bearer '):
                clean_token = clean_token[7:].strip()  # Remove 'Bearer ' prefix if present

            headers["Authorization"] = f"Bearer {clean_token}"
            print(f"DEBUG: Setting authorization header with cleaned token length: {len(clean_token)}")  # Debug print
        else:
            print(f"DEBUG: auth_token is empty or invalid: '{auth_token}'")
            print(f"DEBUG: auth_token type: {type(auth_token)}")
            print(f"DEBUG: This may cause authentication failure when calling {url}")

        payload = {}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if due_date is not None:
            payload["due_date"] = due_date
        if status is not None:
            payload["status"] = status
        if priority is not None:
            payload["priority"] = priority

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.put(url, json=payload, headers=headers)

                if response.status_code == 200:
                    return {
                        "success": True,
                        "data": response.json(),
                        "status_code": response.status_code
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to update todo: {response.text}",
                        "status_code": response.status_code,
                        "data": response.text
                    }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
                "status_code": None
            }

    async def delete_todo(self, todo_id: int, auth_token: str = "") -> Dict[str, Any]:
        """
        Delete a todo via the backend API

        Args:
            todo_id: ID of the todo to delete
            auth_token: Authentication token

        Returns:
            Response from the backend API
        """
        url = f"{self.base_url}/todos/{todo_id}"

        headers = {}

        # Add Authorization header if token is valid
        # Ensure token is not empty, None, or just whitespace
        if auth_token and auth_token.strip():
            # Clean the token by removing any leading/trailing whitespace or Bearer prefix if accidentally included
            clean_token = auth_token.strip()
            if clean_token.lower().startswith('bearer '):
                clean_token = clean_token[7:].strip()  # Remove 'Bearer ' prefix if present
            elif clean_token.startswith('Bearer '):
                clean_token = clean_token[7:].strip()  # Remove 'Bearer ' prefix if present

            headers["Authorization"] = f"Bearer {clean_token}"
            print(f"DEBUG: Setting authorization header with cleaned token length: {len(clean_token)}")  # Debug print
        else:
            print(f"DEBUG: auth_token is empty or invalid: '{auth_token}'")
            print(f"DEBUG: auth_token type: {type(auth_token)}")
            print(f"DEBUG: This may cause authentication failure when calling {url}")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.delete(url, headers=headers)

                if response.status_code in [200, 204]:
                    return {
                        "success": True,
                        "data": None,
                        "status_code": response.status_code
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to delete todo: {response.text}",
                        "status_code": response.status_code,
                        "data": response.text
                    }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
                "status_code": None
            }

    async def toggle_todo_status(self, todo_id: int, auth_token: str = "") -> Dict[str, Any]:
        """
        Toggle the completion status of a todo

        Args:
            todo_id: ID of the todo to toggle
            auth_token: Authentication token

        Returns:
            Response from the backend API
        """
        url = f"{self.base_url}/todos/{todo_id}/toggle"

        headers = {}

        # Add Authorization header if token is valid
        # Ensure token is not empty, None, or just whitespace
        if auth_token and auth_token.strip():
            # Clean the token by removing any leading/trailing whitespace or Bearer prefix if accidentally included
            clean_token = auth_token.strip()
            if clean_token.lower().startswith('bearer '):
                clean_token = clean_token[7:].strip()  # Remove 'Bearer ' prefix if present
            elif clean_token.startswith('Bearer '):
                clean_token = clean_token[7:].strip()  # Remove 'Bearer ' prefix if present

            headers["Authorization"] = f"Bearer {clean_token}"
            print(f"DEBUG: Setting authorization header with cleaned token length: {len(clean_token)}")  # Debug print
        else:
            print(f"DEBUG: auth_token is empty or invalid: '{auth_token}'")
            print(f"DEBUG: auth_token type: {type(auth_token)}")
            print(f"DEBUG: This may cause authentication failure when calling {url}")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.patch(url, headers=headers)

                if response.status_code == 200:
                    return {
                        "success": True,
                        "data": response.json(),
                        "status_code": response.status_code
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to toggle todo status: {response.text}",
                        "status_code": response.status_code,
                        "data": response.text
                    }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
                "status_code": None
            }


# Global adapter instance
todo_api_adapter = TodoAPIAdapter()