# Data Model: AI-Powered Todo Chatbot

## Overview
Data models for the AI-Powered Todo Chatbot (Phase III) that integrates with the existing Todo application (Phase II). The models focus on natural language processing and MCP protocol structures, while maintaining separation from Phase II data models.

## Core Entities

### IntentClassificationResult
Represents the result of natural language intent classification

**Fields**:
- `intent_type`: String (CREATE_TODO, READ_TODOS, UPDATE_TODO, DELETE_TODO)
- `confidence_score`: Float (0.0 to 1.0) representing model confidence
- `extracted_entities`: Dictionary containing extracted entities from the input
- `raw_input`: String (original user input)
- `timestamp`: DateTime (when classification was performed)

**Validation rules**:
- `intent_type` must be one of the predefined values
- `confidence_score` must be between 0.0 and 1.0
- `raw_input` must not be empty

### TodoEntity
Represents extracted todo information from natural language input

**Fields**:
- `title`: String (the main task description)
- `due_date`: Optional[DateTime] (deadline for the task)
- `status`: String (PENDING, COMPLETED, etc.)
- `priority`: String (HIGH, MEDIUM, LOW)
- `tags`: List[String] (optional tags for categorization)
- `confidence`: Float (0.0 to 1.0) for entity extraction confidence

**Validation rules**:
- `title` must not be empty
- `status` must be one of the valid status values
- `priority` must be one of HIGH, MEDIUM, LOW
- `due_date` must be a future date if provided

### ConversationContext
State information for ongoing conversations

**Fields**:
- `conversation_id`: String (unique identifier for the conversation)
- `user_id`: String (identifier for the authenticated user)
- `previous_inputs`: List[String] (recent user inputs in the conversation)
- `previous_responses`: List[String] (recent bot responses)
- `active_context`: Dictionary (current context information like referenced todo)
- `created_at`: DateTime (when conversation started)
- `last_activity_at`: DateTime (when last interaction occurred)

**Validation rules**:
- `conversation_id` must be unique
- `user_id` must be valid and authenticated
- `previous_inputs` and `previous_responses` should have limited length (e.g., last 5)

### MCPToolRequest
Structure for requests to MCP tools

**Fields**:
- `tool_name`: String (name of the MCP tool to call)
- `parameters`: Dictionary (parameters for the tool)
- `auth_token`: String (authentication token from user session)
- `conversation_context`: ConversationContext (context information)
- `request_id`: String (unique identifier for the request)

**Validation rules**:
- `tool_name` must correspond to a registered MCP tool
- `auth_token` must be valid
- `parameters` must match the expected schema for the tool

### MCPToolResponse
Structure for responses from MCP tools

**Fields**:
- `success`: Boolean (whether the operation succeeded)
- `result`: Any (result data from the tool)
- `error_message`: Optional[String] (error details if operation failed)
- `request_id`: String (corresponds to the request ID)
- `timestamp`: DateTime (when response was generated)

**Validation rules**:
- `success` and `error_message` are mutually exclusive
- If `success` is False, `error_message` must be provided

### ChatbotResponse
Structured response to user input

**Fields**:
- `message`: String (the main response message to the user)
- `intent_processed`: String (the intent that was processed)
- `entities_extracted`: List[TodoEntity] (entities that were identified)
- `next_prompt`: Optional[String] (follow-up prompt if needed)
- `operation_result`: Any (result from the performed operation)
- `timestamp`: DateTime (when response was generated)

**Validation rules**:
- `message` must not be empty
- `intent_processed` must be valid

## State Transitions

### Intent Classification Process
1. Raw Input Received → Input Preprocessing → Feature Extraction → Intent Classification → Result Validation → IntentClassificationResult

### Todo Operation Process
1. Intent Classification → Entity Extraction → MCP Tool Invocation → Phase II API Call → Result Processing → Response Generation → User Response

### Conversation Flow
1. New User Input → Intent Classification → Context Update → Action Execution → Response Generation → Context Storage

## Relationships

- `IntentClassificationResult` contains multiple `TodoEntity` objects when multiple entities are extracted
- `ConversationContext` contains multiple `IntentClassificationResult` objects representing the history
- `MCPToolRequest` leads to `MCPToolResponse` (one-to-one relationship)
- `ChatbotResponse` aggregates information from `MCPToolResponse` and other components

## Validation Rules Summary

- All user-facing text must be properly sanitized
- Authentication tokens must be validated before use
- Dates must be validated (due dates should be in the future)
- Confidence scores must be within valid ranges
- Unique identifiers must be truly unique
- Required fields must not be empty or null when not optional

## API Contract Implications

The data models inform the following API contracts:
- Intent classification endpoints need to accept raw text and return structured intent results
- Todo operation endpoints need to accept and return the entity structures defined above
- Conversation context endpoints need to handle the context persistence requirements
- MCP tool interfaces need to follow the request/response patterns defined