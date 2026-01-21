# Quickstart Guide: AI-Powered Todo Chatbot

## Overview
This guide provides instructions for setting up and running the AI-Powered Todo Chatbot (Phase III) that integrates with the existing Todo Full-Stack application (Phase II).

## Prerequisites
- Python 3.11+
- Node.js 18+ (for existing Phase II components)
- Access to Phase II backend APIs
- Valid authentication tokens for user accounts
- MCP (Model Context Protocol) compatible environment

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo-fullstack
```

### 2. Navigate to Phase III Directory
```bash
cd phase-3
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

If no requirements.txt exists yet, install the basic dependencies:
```bash
pip install fastapi uvicorn httpx python-multipart python-jose[cryptography] passlib[bcrypt] spacy
```

### 4. Set Up Environment Variables
Create a `.env` file in the `phase-3/` directory:

```env
PHASE_II_BASE_URL=https://your-phase-ii-backend.com/api
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8001
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
LOG_LEVEL=INFO
DEBUG=False
```

## Running the Application

### 1. Start the MCP Server
```bash
cd phase-3/mcp-server
uvicorn server:app --host 0.0.0.0 --port 8001
```

### 2. Start the Chatbot Service
```bash
cd phase-3/chatbot
uvicorn chat_interface:app --host 0.0.0.0 --port 8002
```

### 3. Alternatively, Use Docker Compose (if available)
```bash
docker-compose -f phase-3/docker-compose.yml up
```

## API Usage

### Interacting with the Chatbot
Send a POST request to the chatbot endpoint:

```bash
curl -X POST http://localhost:8002/api/v1/chatbot/interact \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "Add buy groceries to my list",
    "conversation_context": {
      "conversation_id": null,
      "user_id": "user-identifier",
      "previous_inputs": [],
      "previous_responses": [],
      "active_context": {}
    }
  }'
```

## Development

### Setting up Development Environment
```bash
# Install dev dependencies
pip install pytest pytest-mock black flake8 mypy

# Run linter
flake8 .
black .
mypy .

# Run tests
pytest
```

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.

# Run specific test file
pytest tests/unit/chatbot/test_intent_parser.py
```

## Architecture Overview

### Components
1. **MCP Server** (`phase-3/mcp-server/`): Implements Model Context Protocol
2. **Chatbot Logic** (`phase-3/chatbot/`): Handles natural language processing
3. **API Adapters** (`phase-3/adapters/`): Interfaces with Phase II backend
4. **Services** (`phase-3/services/`): Business logic layer
5. **Configuration** (`phase-3/config/`): Settings and constants

### Data Flow
1. User sends natural language input
2. Intent parser classifies the intent (CREATE, READ, UPDATE, DELETE)
3. Entity extractor pulls relevant information (title, due date, etc.)
4. MCP tools are invoked based on the intent
5. API adapters call Phase II backend services
6. Response is formatted and returned to the user

## Troubleshooting

### Common Issues
- **Authentication errors**: Ensure your JWT token is valid and has proper permissions
- **Connection errors**: Verify that Phase II backend is accessible at the configured URL
- **Intent classification failures**: Check that input messages follow expected patterns

### Debugging
Set `DEBUG=True` in your environment variables and check the logs:
```bash
tail -f phase-3/logs/app.log
```

## MCP Integration

### Registering Tools
MCP tools are automatically registered when the server starts. The following tools are available:
- `create_todo`: Creates a new todo item
- `list_todos`: Lists existing todo items
- `update_todo`: Updates an existing todo item
- `delete_todo`: Deletes a todo item

### Using MCP Tools
The chatbot automatically selects appropriate MCP tools based on intent classification.

## Testing the Integration

### With Phase II Backend
1. Ensure Phase II backend is running
2. Verify API endpoints are accessible
3. Test with a valid user account

### Mock Testing
For isolated testing without Phase II backend:
```bash
# Run tests with mocked Phase II API calls
pytest --mock-phase2-api
```

## Production Deployment

### Environment Variables for Production
```env
PHASE_II_BASE_URL=https://production-phase-ii.com/api
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=80
SECRET_KEY=production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
LOG_LEVEL=WARNING
DEBUG=False
```

### Docker Deployment
```bash
docker build -t todo-chatbot:latest -f phase-3/Dockerfile .
docker run -d -p 80:80 -e PHASE_II_BASE_URL=https://your-backend.com todo-chatbot:latest
```

## Next Steps
1. Review the data models in `data-model.md`
2. Examine the API contracts in `contracts/`
3. Look at the detailed implementation plan in `plan.md`
4. Check out the specific tasks in `tasks.md` (once generated)