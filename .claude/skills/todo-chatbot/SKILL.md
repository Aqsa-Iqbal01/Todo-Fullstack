---
name: todo-chatbot
description: Todo chatbot with MCP integration for natural language todo management. Use when Claude needs to work with the chatbot functionality for: (1) Setting up the chatbot with MCP server, (2) Processing natural language todo commands, (3) Managing intent classification for todo operations, (4) Handling chatbot API integration, (5) Running the complete chatbot system with proper configuration, (6) Troubleshooting chatbot functionality, or (7) Understanding the intent parsing and response handling system.
---

# Todo Chatbot with MCP Integration

## Overview

A comprehensive chatbot system that allows users to manage their todos through natural language commands. The system integrates with an MCP (Model Context Protocol) server to process natural language input and convert it into todo operations. This skill provides assistance for developing, configuring, and troubleshooting the chatbot functionality.

## Quick Start Guide

### Starting the Complete System

```bash
# 1. Install Dependencies
pip install -r backend/requirements.txt
pip install -r phase-3/requirements.txt

# 2. Start the Backend Server (runs on port 8004)
python run_backend_with_db_init.py

# 3. Start the MCP Server in a separate terminal (runs on port 8080)
cd phase-3
python -m start_mcp_server

# 4. Test the Chatbot
curl -X POST http://localhost:8004/api/chatbot \
  -H 'Authorization: Bearer YOUR_TOKEN_HERE' \
  -H 'Content-Type: application/json' \
  -d '{"message": "Add buy groceries to my list"}'
```

### System Architecture

The chatbot system consists of:
- **Frontend Interface**: React-based chat interface
- **Backend API**: FastAPI server handling authentication and todo operations
- **MCP Server**: Handles natural language processing and intent classification
- **Database**: SQLite/PostgreSQL for storing todos and user data

## Core Capabilities

### 1. Intent Classification System

The chatbot uses sophisticated intent classification to understand user commands:

```python
# phase-3/chatbot/intent_parser.py
from enum import Enum
import re

class Intent(Enum):
    CREATE_TODO = "CREATE_TODO"
    READ_TODOS = "READ_TODOS"
    UPDATE_TODO = "UPDATE_TODO"
    DELETE_TODO = "DELETE_TODO"
    GENERAL_CONVERSATION = "GENERAL_CONVERSATION"
    UNKNOWN = "UNKNOWN"

def classify_intent(message: str) -> Intent:
    """Classify the intent of a user message"""
    message_lower = message.lower().strip()

    # CREATE_TODO intents
    create_patterns = [
        r'\b(add|create|make|put|write down|jot down)\b.*\b(todo|task|item|list|note)\b',
        r'\b(create|add)\b.*\b(todo|task)\b',
        r'\b(add|put|create)\b.*\bto.*\b(list|my list|todos?)\b',
        r'\b(make|create)\b.*\bfor me\b',
        r'\b(want to|need to|should)\b.*\b(do|complete|finish|buy|get)\b',
        r'\b(buy|purchase|get|order)\b',
        r'\b(remind me to|tell me to)\b',
        r'\b(schedule|plan)\b.*\b(todo|task)\b',
        r'\b(set up|arrange|organize)\b.*\b(task|todo)\b'
    ]

    for pattern in create_patterns:
        if re.search(pattern, message_lower):
            return Intent.CREATE_TODO

    # READ_TODOS intents - more specific patterns
    read_patterns = [
        r'\b(show|display|list|see|view|check|get|fetch|retrieve)\b.*\b(my|all|current|existing)?\b.*\b(todos?|tasks?|items?|list|things to do|to-do list)\b',
        r'\b(what|whats|tell me|list out)\b.*\b(i have|on my list|to do|todo|tasks)\b',
        r'\b(my|current|existing)\b.*\b(todos?|tasks?|list)\b.*\b(are|is|look like|show me)\b',
        r'\b(dump|print|output)\b.*\b(todos?|tasks?|my list)\b',
        r'\b(status|progress|completed|done|finished)\b.*\b(todos?|tasks?|items)\b',
        r'\b(how many|number of)\b.*\b(todos?|tasks?)\b',
        r'\b(review|browse|go through)\b.*\b(my|the)\b.*\b(todos?|tasks?)\b'
    ]

    for pattern in read_patterns:
        if re.search(pattern, message_lower):
            return Intent.READ_TODOS

    # UPDATE_TODO intents
    update_patterns = [
        r'\b(mark|set|change|update|modify|complete|finish|done|cross off)\b.*\b(complete|done|finished|incomplete|not done|pending)\b',
        r'\b(complete|finish|done|mark as done)\b',
        r'\b(update|change|modify|edit)\b.*\b(status|state|completion)\b',
        r'\b(check off|tick off|cross out)\b',
        r'\b(mark as|set as)\b.*\b(complete|done|finished|pending|incomplete)\b',
        r'\b(activate|reactivate|reopen|uncomplete|unfinish)\b'
    ]

    for pattern in update_patterns:
        if re.search(pattern, message_lower):
            return Intent.UPDATE_TODO

    # DELETE_TODO intents
    delete_patterns = [
        r'\b(delete|remove|erase|eliminate|clear|cancel|get rid of|trash|dispose of)\b.*\b(todo|task|item|entry)\b',
        r'\b(remove|delete)\b.*\b(from|off)\b.*\b(list|my list|todos?)\b',
        r'\b(purge|clean up|clear out)\b.*\b(todos?|tasks?)\b',
        r'\b(drop|omit|skip)\b.*\b(this|that|the)\b.*\b(todo|task|item)\b',
        r'\b(finish permanently|get rid of|eliminate)\b.*\b(todo|task)\b'
    ]

    for pattern in delete_patterns:
        if re.search(pattern, message_lower):
            return Intent.DELETE_TODO

    # GENERAL_CONVERSATION intents - non-todo related
    general_patterns = [
        r'\b(weather|temperature|forecast|climate)\b',
        r'\b(joke|funny|humor|laugh|comedy)\b',
        r'\b(movie|film|tv|series|entertainment)\b',
        r'\b(sport|game|match|score|team|player)\b',
        r'\b(news|headline|current event|politics|world)\b',
        r'\b(food|restaurant|recipe|cooking|meal)\b',
        r'\b(music|song|artist|band|album)\b',
        r'\b(travel|vacation|trip|flight|hotel)\b',
        r'\b(time|date|clock|schedule|calendar)\b',
        r'\b(how are you|what are you|who are you|what do you do)\b',
        r'\b(thanks|thank you|appreciate|grateful)\b',
        r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b'
    ]

    for pattern in general_patterns:
        if re.search(pattern, message_lower):
            return Intent.GENERAL_CONVERSATION

    # If no specific intent is matched, return UNKNOWN
    return Intent.UNKNOWN
```

### 2. Chat Interface with MCP Integration

```python
# phase-3/chatbot/chat_interface.py
import requests
import json
from typing import Dict, Any
from .intent_parser import Intent, classify_intent
from ..config.settings import BACKEND_API_URL, MCP_SERVER_URL

class ChatInterface:
    def __init__(self):
        self.backend_url = BACKEND_API_URL
        self.mcp_server_url = MCP_SERVER_URL

    def process_message(self, message: str, user_id: str, token: str) -> Dict[str, Any]:
        """
        Process a user message and return a response
        """
        intent = classify_intent(message)

        # Prepare headers for backend requests
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        if intent == Intent.CREATE_TODO:
            return self._handle_create_todo(message, user_id, headers)
        elif intent == Intent.READ_TODOS:
            return self._handle_read_todos(user_id, headers)
        elif intent == Intent.UPDATE_TODO:
            return self._handle_update_todo(message, user_id, headers)
        elif intent == Intent.DELETE_TODO:
            return self._handle_delete_todo(message, user_id, headers)
        elif intent == Intent.GENERAL_CONVERSATION:
            return self._handle_general_conversation(message)
        else:  # UNKNOWN
            return self._handle_unknown_intent(message)

    def _handle_create_todo(self, message: str, user_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """
        Handle creating a new todo based on the message
        """
        # Extract the todo content from the message
        import re

        # Patterns to extract the todo content
        patterns = [
            r'(?:add|create|make|put|write down|jot down)\s+(.+?)(?:\s+to\s+|\s+in\s+|\s+on\s+|$)',
            r'(?:buy|get|purchase|order)\s+(.+?)(?:\s+and|$)',
            r'(?:remind me to|tell me to|need to|want to|should)\s+(do|complete|finish|buy|get)\s+(.+?)(?:\s+and|$)',
            r'.*?(?!add|create|make|put|write down|jot down|buy|get|purchase|order|remind me to|tell me to|need to|want to|should)\s+(.+?)(?:\s+please|now|today|$)'
        ]

        todo_content = ""
        for pattern in patterns:
            match = re.search(pattern, message.lower(), re.IGNORECASE)
            if match:
                # For patterns with multiple groups, use the last captured group
                groups = match.groups()
                todo_content = groups[-1].strip() if groups else ""
                break

        # If no content extracted, use the original message
        if not todo_content:
            # Remove common command words to get the core content
            todo_content = re.sub(r'^(add|create|make|put|write down|jot down|buy|get|purchase|order|remind me to|tell me to|need to|want to|should|please|now|today)\s*', '', message, flags=re.IGNORECASE).strip()

        # Create the todo via the backend API
        todo_data = {
            'title': todo_content.capitalize(),
            'description': f'Created from chat: "{message}"',
            'completed': False
        }

        try:
            response = requests.post(
                f"{self.backend_url}/todos",
                headers=headers,
                json=todo_data
            )

            if response.status_code == 200:
                return {
                    'success': True,
                    'message': f'Successfully added "{todo_content}" to your todo list!',
                    'intent': 'CREATE_TODO',
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to add todo: {response.text}',
                    'intent': 'CREATE_TODO'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error creating todo: {str(e)}',
                'intent': 'CREATE_TODO'
            }

    def _handle_read_todos(self, user_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """
        Handle reading todos
        """
        try:
            response = requests.get(
                f"{self.backend_url}/todos",
                headers=headers
            )

            if response.status_code == 200:
                todos = response.json()

                if not todos:
                    return {
                        'success': True,
                        'message': 'Your todo list is currently empty.',
                        'intent': 'READ_TODOS',
                        'data': []
                    }

                todo_list = []
                for todo in todos:
                    status = "✓ Completed" if todo.get('completed', False) else "○ Pending"
                    todo_list.append(f"- [{status}] {todo.get('title', 'Untitled')}")

                todo_str = "\n".join(todo_list)
                return {
                    'success': True,
                    'message': f'Here are your current todos:\n\n{todo_str}',
                    'intent': 'READ_TODOS',
                    'data': todos
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to retrieve todos: {response.text}',
                    'intent': 'READ_TODOS'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error retrieving todos: {str(e)}',
                'intent': 'READ_TODOS'
            }

    def _handle_update_todo(self, message: str, user_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """
        Handle updating a todo (marking as complete/incomplete)
        """
        try:
            # First, get all todos to identify which one to update
            todos_response = requests.get(
                f"{self.backend_url}/todos",
                headers=headers
            )

            if todos_response.status_code != 200:
                return {
                    'success': False,
                    'message': 'Could not retrieve your todos to update.',
                    'intent': 'UPDATE_TODO'
                }

            todos = todos_response.json()
            if not todos:
                return {
                    'success': False,
                    'message': 'You have no todos to update.',
                    'intent': 'UPDATE_TODO'
                }

            # Extract the todo title from the message
            import re
            # Look for keywords indicating completion
            if any(word in message.lower() for word in ['complete', 'done', 'finish', 'completed', 'marked']):
                # Find a matching incomplete todo
                todo_title = self._extract_todo_title(message, [t for t in todos if not t.get('completed', False)])
            else:
                # Assume it's marking as incomplete
                todo_title = self._extract_todo_title(message, todos)

            if not todo_title:
                return {
                    'success': False,
                    'message': 'Could not identify which todo to update. Please be more specific.',
                    'intent': 'UPDATE_TODO'
                }

            # Find the todo by title
            matching_todo = None
            for todo in todos:
                if todo_title.lower() in todo.get('title', '').lower():
                    matching_todo = todo
                    break

            if not matching_todo:
                return {
                    'success': False,
                    'message': f'Could not find a todo matching "{todo_title}".',
                    'intent': 'UPDATE_TODO'
                }

            # Toggle completion status
            new_status = not matching_todo.get('completed', False)
            update_response = requests.patch(
                f"{self.backend_url}/todos/{matching_todo['id']}/toggle",
                headers=headers
            )

            if update_response.status_code == 200:
                status_text = "completed" if new_status else "marked as pending"
                return {
                    'success': True,
                    'message': f'Successfully {status_text}: "{matching_todo.get("title", "")}"',
                    'intent': 'UPDATE_TODO',
                    'data': update_response.json()
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to update todo: {update_response.text}',
                    'intent': 'UPDATE_TODO'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error updating todo: {str(e)}',
                'intent': 'UPDATE_TODO'
            }

    def _handle_delete_todo(self, message: str, user_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """
        Handle deleting a todo
        """
        try:
            # First, get all todos to identify which one to delete
            todos_response = requests.get(
                f"{self.backend_url}/todos",
                headers=headers
            )

            if todos_response.status_code != 200:
                return {
                    'success': False,
                    'message': 'Could not retrieve your todos to delete.',
                    'intent': 'DELETE_TODO'
                }

            todos = todos_response.json()
            if not todos:
                return {
                    'success': False,
                    'message': 'You have no todos to delete.',
                    'intent': 'DELETE_TODO'
                }

            # Extract the todo title from the message
            import re
            todo_title = self._extract_todo_title(message, todos)

            if not todo_title:
                return {
                    'success': False,
                    'message': 'Could not identify which todo to delete. Please be more specific.',
                    'intent': 'DELETE_TODO'
                }

            # Find the todo by title
            matching_todo = None
            for todo in todos:
                if todo_title.lower() in todo.get('title', '').lower():
                    matching_todo = todo
                    break

            if not matching_todo:
                return {
                    'success': False,
                    'message': f'Could not find a todo matching "{todo_title}".',
                    'intent': 'DELETE_TODO'
                }

            # Delete the todo
            delete_response = requests.delete(
                f"{self.backend_url}/todos/{matching_todo['id']}",
                headers=headers
            )

            if delete_response.status_code == 200:
                return {
                    'success': True,
                    'message': f'Successfully deleted: "{matching_todo.get("title", "")}"',
                    'intent': 'DELETE_TODO',
                    'data': {'deleted_todo': matching_todo}
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to delete todo: {delete_response.text}',
                    'intent': 'DELETE_TODO'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error deleting todo: {str(e)}',
                'intent': 'DELETE_TODO'
            }

    def _handle_general_conversation(self, message: str) -> Dict[str, Any]:
        """
        Handle general conversation that is not related to todos
        """
        if any(word in message.lower() for word in ['weather', 'temperature', 'forecast']):
            return {
                'success': True,
                'message': "I specialize in helping you manage your todos. For weather information, please use a dedicated weather service.",
                'intent': 'GENERAL_CONVERSATION'
            }
        elif any(word in message.lower() for word in ['joke', 'funny', 'humor']):
            return {
                'success': True,
                'message': "I focus on helping you manage your todos effectively. For jokes and entertainment, I recommend checking out comedy websites or apps!",
                'intent': 'GENERAL_CONVERSATION'
            }
        elif any(word in message.lower() for word in ['movie', 'film', 'tv', 'entertainment']):
            return {
                'success': True,
                'message': "I'm designed to help you manage your todos. For movie recommendations or entertainment information, please use a dedicated service.",
                'intent': 'GENERAL_CONVERSATION'
            }
        else:
            return {
                'success': True,
                'message': "I'm here to help you manage your todos. I can add, view, update, and delete tasks for you. Try saying something like 'Add buy groceries to my list' or 'Show me my todos'.",
                'intent': 'GENERAL_CONVERSATION'
            }

    def _handle_unknown_intent(self, message: str) -> Dict[str, Any]:
        """
        Handle messages with unknown intent
        """
        return {
            'success': False,
            'message': "I'm not sure what you mean. I can help you manage your todos. Try saying something like 'Add buy groceries to my list' or 'Show me my todos'.",
            'intent': 'UNKNOWN'
        }

    def _extract_todo_title(self, message: str, todos: list) -> str:
        """
        Extract a todo title from a message by looking for matching titles in the todo list
        """
        import re

        # Remove common action words to get the core content
        cleaned_message = re.sub(r'\b(mark|set|change|update|modify|complete|finish|done|cross off|delete|remove|erase|add|create|make|put|show|display|list|see|view|get|fetch|retrieve)\b', '', message, flags=re.IGNORECASE)

        # Look for the longest matching substring in the available todos
        best_match = ""
        for todo in todos:
            title = todo.get('title', '')
            if title.lower() in cleaned_message.lower() and len(title) > len(best_match):
                best_match = title

        if best_match:
            return best_match

        # If no direct match, try to find a close match
        import difflib
        all_titles = [todo.get('title', '') for todo in todos]
        matches = difflib.get_close_matches(cleaned_message.strip(), all_titles, n=1, cutoff=0.3)

        return matches[0] if matches else ""

# Initialize the chat interface
chat_interface = ChatInterface()
```

### 3. MCP Server Configuration

```python
# phase-3/mcp_server/server.py
import asyncio
import json
from aiohttp import web, WSMsgType
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from ..chatbot.chat_interface import chat_interface

routes = web.RouteTableDef()

@routes.get('/health')
async def health_check(request):
    return web.json_response({'status': 'healthy'})

@routes.post('/chat')
async def handle_chat(request):
    data = await request.json()
    message = data.get('message', '')
    user_id = data.get('user_id', '')
    token = data.get('token', '')

    if not message:
        return web.json_response({
            'error': 'Message is required'
        }, status=400)

    if not token:
        return web.json_response({
            'error': 'Authentication token is required'
        }, status=400)

    # Process the message using the chat interface
    response = chat_interface.process_message(message, user_id, token)

    return web.json_response(response)

@routes.get('/ws')
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            try:
                data = json.loads(msg.data)
                message = data.get('message', '')
                user_id = data.get('user_id', '')
                token = data.get('token', '')

                if message and token:
                    response = chat_interface.process_message(message, user_id, token)
                    await ws.send_json(response)
                else:
                    await ws.send_json({
                        'error': 'Message and token are required'
                    })
            except json.JSONDecodeError:
                await ws.send_json({
                    'error': 'Invalid JSON'
                })
            except Exception as e:
                await ws.send_json({
                    'error': f'Server error: {str(e)}'
                })
        elif msg.type == WSMsgType.ERROR:
            print(f'WebSocket connection closed with exception {ws.exception()}')

    return ws

def create_app():
    app = web.Application()
    app.add_routes(routes)

    # Serve static files if needed
    app.router.add_static('/static/', path='static/', name='static')

    return app

if __name__ == '__main__':
    # Get port from environment or default to 8080
    port = int(os.getenv('MCP_PORT', 8080))
    host = os.getenv('MCP_HOST', 'localhost')

    app = create_app()
    print(f"MCP Server starting on {host}:{port}")

    web.run_app(app, host=host, port=port)
```

### 4. Configuration Settings

```python
# phase-3/config/settings.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Backend API configuration
BACKEND_API_URL = os.getenv('BACKEND_API_URL', 'http://localhost:8004/api')

# MCP Server configuration
MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'http://localhost:8080')

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./todo_app.db')

# JWT Secret
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-default-secret-key-change-in-production')

# Port configurations
BACKEND_PORT = int(os.getenv('BACKEND_PORT', 8004))
MCP_PORT = int(os.getenv('MCP_PORT', 8080))

# Debug mode
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

print(f"Configuration loaded:")
print(f"  BACKEND_API_URL: {BACKEND_API_URL}")
print(f"  MCP_SERVER_URL: {MCP_SERVER_URL}")
print(f"  DATABASE_URL: {DATABASE_URL}")
print(f"  BACKEND_PORT: {BACKEND_PORT}")
print(f"  MCP_PORT: {MCP_PORT}")
print(f"  DEBUG: {DEBUG}")
```

### 5. Environment Configuration

```bash
# phase-3/.env
BACKEND_API_URL=http://localhost:8004/api
MCP_SERVER_URL=http://localhost:8080
DATABASE_URL=sqlite:///./todo_app.db
JWT_SECRET_KEY=your-super-secret-and-long-random-string-for-production
BACKEND_PORT=8004
MCP_PORT=8080
DEBUG=true
```

### 6. Backend API Integration

```python
# backend/src/api/chatbot.py
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
import requests
from ..auth.auth_handler import get_current_user
from ..models.todo import Todo
from ..database.database import get_db
from sqlalchemy.orm import Session
import os
from ..config.settings import MCP_SERVER_URL

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

@router.post("/chatbot")
async def chatbot_endpoint(
    request: ChatMessage,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint to handle chatbot messages through MCP server
    """
    try:
        # Prepare headers with the user's token
        headers = {
            'Authorization': f'Bearer {current_user.get("token", "")}',
            'Content-Type': 'application/json'
        }

        # Send the message to the MCP server for processing
        mcp_response = requests.post(
            f"{MCP_SERVER_URL}/chat",
            json={
                'message': request.message,
                'user_id': current_user.get("id", ""),
                'token': current_user.get("token", "")
            },
            headers={'Content-Type': 'application/json'}  # Don't forward auth to MCP
        )

        if mcp_response.status_code == 200:
            result = mcp_response.json()
            return result
        else:
            # If MCP server is not available, return an error
            raise HTTPException(
                status_code=500,
                detail=f"MCP server error: {mcp_response.text}"
            )

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=500,
            detail="Cannot connect to MCP server. Please ensure the MCP server is running."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}"
        )

# For backward compatibility or direct processing without MCP
@router.post("/chatbot-direct")
async def chatbot_direct_endpoint(
    request: ChatMessage,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Direct chatbot processing without MCP server (fallback)
    """
    from ..phase-3.chatbot.intent_parser import classify_intent, Intent
    from ..phase-3.chatbot.chat_interface import ChatInterface

    chat_interface = ChatInterface()
    result = chat_interface.process_message(
        request.message,
        current_user.get("id", ""),
        current_user.get("token", "")
    )

    return result
```

### 7. Startup Script with Database Initialization

```python
# run_backend_with_db_init.py
import subprocess
import sys
import time
import threading
from backend.src.main import create_tables
from backend.src.database.database import engine
import os

def initialize_database():
    """Initialize the database tables"""
    print("Initializing database...")
    try:
        create_tables()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

def start_backend():
    """Start the backend server"""
    print("Starting backend server...")

    # Set environment variable for the correct port
    env = os.environ.copy()
    env['PORT'] = '8004'

    # Start the Uvicorn server
    subprocess.run([
        sys.executable, '-m', 'uvicorn',
        'backend.src.main:app',
        '--host', 'localhost',
        '--port', '8004',
        '--reload'
    ], env=env)

if __name__ == "__main__":
    print("Setting up Todo Chatbot System...")

    # Initialize the database first
    initialize_database()

    # Start the backend server in a separate thread
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()

    print("\n" + "="*60)
    print("TODO CHATBOT SYSTEM STARTUP COMPLETE")
    print("="*60)
    print("✓ Database initialized successfully")
    print("✓ Backend server starting on http://localhost:8004")
    print("\nNext steps:")
    print("1. Open a new terminal and start the MCP server:")
    print("   cd phase-3 && python -m start_mcp_server")
    print("2. Register or login to get an authentication token")
    print("3. Test the chatbot API with curl or the frontend")
    print("="*60)

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
```

## Common Commands and Operations

### Testing the System

```bash
# 1. Test if backend is running
curl http://localhost:8004/health

# 2. Register a new user
curl -X POST http://localhost:8004/api/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email": "test@example.com", "password": "securepassword123"}'

# 3. Login to get token
curl -X POST http://localhost:8004/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email": "test@example.com", "password": "securepassword123"}'

# 4. Test chatbot with obtained token
curl -X POST http://localhost:8004/api/chatbot \
  -H 'Authorization: Bearer YOUR_TOKEN_HERE' \
  -H 'Content-Type: application/json' \
  -d '{"message": "Add buy groceries to my list"}'
```

### Troubleshooting

If the chatbot is not working properly:

1. **Check if both servers are running:**
   - Backend on port 8004
   - MCP server on port 8080

2. **Verify configuration files:**
   - Check `phase-3/.env` has correct URLs
   - Verify `BACKEND_API_URL=http://localhost:8004/api`

3. **Check intent classification:**
   - Review `phase-3/chatbot/intent_parser.py`
   - Test with simple commands first

4. **Check database connectivity:**
   - Ensure the database is accessible
   - Verify table creation

## Resources

This skill includes the following directories:

### scripts/
- `run_backend_with_db_init.py`: Complete startup script with database initialization
- `start_mcp_server`: Script to start the MCP server

### references/
- Intent classification patterns and examples
- API documentation for chatbot endpoints
- Configuration examples

### assets/
- Environment configuration templates
- Default settings for development

---
**Note:** This skill works in conjunction with the existing todo-app skill for full functionality.