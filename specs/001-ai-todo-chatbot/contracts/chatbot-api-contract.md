# API Contract: AI Chatbot Interface

## Overview
API contract for the AI-powered chatbot interface that processes natural language input for todo management. This contract defines the interface between the chatbot frontend and the backend processing system.

## Base URL
`/api/v1/chatbot`

## Authentication
All endpoints require authentication via JWT token passed in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

## Common Headers
- `Content-Type: application/json`
- `Accept: application/json`

## Endpoints

### POST /interact
Process a natural language input from the user and return the appropriate response.

#### Request
```json
{
  "message": "Add buy groceries to my list",
  "conversation_context": {
    "conversation_id": "uuid-string",
    "user_id": "user-identifier",
    "previous_inputs": ["previous message 1", "previous message 2"],
    "previous_responses": ["previous response 1", "previous response 2"],
    "active_context": {}
  }
}
```

#### Response (Success)
```json
{
  "success": true,
  "response": {
    "message": "I've added 'buy groceries' to your todo list.",
    "intent_processed": "CREATE_TODO",
    "entities_extracted": [
      {
        "title": "buy groceries",
        "due_date": null,
        "status": "PENDING",
        "priority": "MEDIUM",
        "tags": [],
        "confidence": 0.95
      }
    ],
    "next_prompt": null,
    "operation_result": {
      "todo_id": "new-todo-uuid",
      "action": "created"
    },
    "timestamp": "2026-01-17T10:30:00Z"
  },
  "conversation_context": {
    "conversation_id": "uuid-string",
    "user_id": "user-identifier",
    "previous_inputs": ["Add buy groceries to my list"],
    "previous_responses": ["I've added 'buy groceries' to your todo list."],
    "active_context": {},
    "updated_at": "2026-01-17T10:30:00Z"
  }
}
```

#### Response (Error)
```json
{
  "success": false,
  "error": {
    "code": "INTENT_CLASSIFICATION_FAILED",
    "message": "Unable to understand the intent of your message",
    "details": "The natural language processor could not classify the intent of your input"
  }
}
```

#### Validation
- `message` is required and must be between 1 and 1000 characters
- `conversation_context.conversation_id` must be a valid UUID or null (will be generated if null)
- `conversation_context.user_id` must match the authenticated user
- `conversation_context.previous_inputs` and `conversation_context.previous_responses` have maximum length of 10

### GET /conversation/{conversation_id}
Retrieve the current state of a conversation context.

#### Request
```
GET /api/v1/chatbot/conversation/{conversation_id}
Authorization: Bearer <jwt-token>
```

#### Response (Success)
```json
{
  "success": true,
  "conversation": {
    "conversation_id": "uuid-string",
    "user_id": "user-identifier",
    "previous_inputs": ["message 1", "message 2"],
    "previous_responses": ["response 1", "response 2"],
    "active_context": {},
    "created_at": "2026-01-17T10:00:00Z",
    "last_activity_at": "2026-01-17T10:30:00Z"
  }
}
```

#### Response (Error)
```json
{
  "success": false,
  "error": {
    "code": "CONVERSATION_NOT_FOUND",
    "message": "Conversation not found or access denied"
  }
}
```

#### Validation
- `conversation_id` must be a valid UUID
- User must be the owner of the conversation

### POST /intent/classify
Classify the intent of a natural language message without performing the action.

#### Request
```json
{
  "message": "Show me my todos for today",
  "user_context": {
    "timezone": "UTC",
    "preferences": {}
  }
}
```

#### Response (Success)
```json
{
  "success": true,
  "classification": {
    "intent_type": "READ_TODOS",
    "confidence_score": 0.92,
    "extracted_entities": {
      "filter": {
        "due_date": "today"
      }
    },
    "raw_input": "Show me my todos for today",
    "timestamp": "2026-01-17T10:30:00Z"
  }
}
```

#### Validation
- `message` is required and must be between 1 and 1000 characters
- `user_context.timezone` must be a valid timezone identifier

## Error Codes
- `AUTHENTICATION_REQUIRED`: No valid authentication token provided
- `AUTHORIZATION_DENIED`: User not authorized to access resource
- `INTENT_CLASSIFICATION_FAILED`: Unable to understand user intent
- `ENTITY_EXTRACTION_FAILED`: Unable to extract relevant entities from input
- `CONVERSATION_NOT_FOUND`: Referenced conversation does not exist
- `PHASE_II_API_ERROR`: Error communicating with Phase II backend
- `INVALID_INPUT`: Provided input does not meet validation requirements
- `RATE_LIMIT_EXCEEDED`: Too many requests from the same user
- `SERVICE_UNAVAILABLE`: Temporary service unavailability

## Rate Limits
- 100 requests per hour per user
- 10 requests per minute per conversation

## Response Format
All responses follow the same basic structure:
```json
{
  "success": boolean,
  "response|conversation|classification|error": object,
  "conversation_context": object (when applicable),
  "timestamp": string (ISO 8601 format)
}
```

## Status Codes
- `200`: Success
- `400`: Bad Request (validation error)
- `401`: Unauthorized (missing or invalid authentication)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found (resource does not exist)
- `429`: Too Many Requests (rate limit exceeded)
- `500`: Internal Server Error
- `502`: Bad Gateway (error from Phase II backend)
- `503`: Service Unavailable