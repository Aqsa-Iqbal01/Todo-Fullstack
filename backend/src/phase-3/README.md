# Phase III: AI-Powered Todo Chatbot with MCP

This directory contains the implementation of the AI-powered todo chatbot for Phase III of the Todo Full-Stack application. The implementation follows the Model Context Protocol (MCP) architecture as specified in the project constitution.

## Architecture Overview

The chatbot is built with a modular architecture that includes:

- **MCP Server**: Implements the Model Context Protocol for AI integration
- **Chatbot Logic**: Natural language processing with intent classification and entity extraction
- **API Adapters**: Interfaces with Phase II backend APIs
- **Services**: Business logic layers for todo operations
- **Configuration**: Settings and constants management

## Components

### MCP Server (`mcp-server/`)
- Implements the MCP protocol for AI integration
- Manages tool registration and execution
- Handles communication between AI components and backend services

### Chatbot Logic (`chatbot/`)
- **Intent Parser**: Classifies user intent from natural language input
- **Entity Extractor**: Extracts relevant entities like todo titles, due dates, priorities
- **Chat Interface**: Main interface for processing user input

### API Adapters (`adapters/`)
- **Todo API Adapter**: Communicates with Phase II backend for todo operations
- **Auth Adapter**: Handles authentication delegation to Phase II

### Services (`services/`)
- **Todo Service**: Business logic for todo operations
- **Conversation Service**: Manages conversation context between requests

### Configuration (`config/`)
- **Settings**: Application configuration management
- **Constants**: Defined constants for intents, entities, and other values

## Features

The chatbot supports the following natural language commands:

### Creating Todos
- "Add buy groceries to my list"
- "Create a task to finish report by Friday"
- "Make a new todo for scheduling meeting"

### Reading Todos
- "Show my todos"
- "What do I have to do today?"
- "List all my pending tasks"

### Updating Todos
- "Mark buy groceries as complete"
- "Change due date of finish report to next Monday"
- "Update meeting with John to next Tuesday"

### Deleting Todos
- "Delete buy groceries"
- "Remove the meeting with John"
- "Cancel the appointment"

## MCP Tools

The system implements the following MCP tools as required by the specification:

- `create_todo`: Creates new todo items
- `list_todos`: Retrieves existing todo items
- `update_todo`: Updates existing todo items (including status toggling)
- `delete_todo`: Removes todo items

## Integration with Phase II

The chatbot communicates with Phase II backend APIs only via HTTP calls as required by the constitution:
- No direct database access
- All authentication delegated to Phase II
- Strict isolation maintained between Phase II and Phase III components

## Usage

The chatbot is integrated into the frontend application via the backend API endpoint at `/api/chatbot`. The frontend sends user input to this endpoint, which processes it through the MCP-based system and returns appropriate responses.