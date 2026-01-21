# Research: AI-Powered Todo Chatbot

## Overview
This document contains research findings for the AI-Powered Todo Chatbot feature, addressing unknowns and technical decisions identified during the planning phase.

## Decision Log

### 1. MCP Server Implementation
**Decision**: Implement MCP server using Python with the `mcp` library
**Rationale**: Since the backend is already using Python/FastAPI, it makes sense to use Python for the MCP server as well. The `mcp` library provides native support for Model Context Protocol implementation.
**Alternatives considered**:
- Node.js implementation: Would require additional runtime
- Separate service in different language: Would increase complexity

### 2. Natural Language Processing Approach
**Decision**: Use a lightweight rule-based approach combined with ML libraries like spaCy or transformers for intent classification
**Rationale**: For the specific domain of todo management, we can achieve high accuracy with simpler models that are easier to maintain than large LLMs. Rule-based approaches work well for structured commands like "add buy groceries".
**Alternatives considered**:
- Full LLM integration: Higher cost and complexity for simple commands
- Pre-built NLP services (AWS Lex, Dialogflow): Adds external dependencies

### 3. Conversation Context Management
**Decision**: Implement stateless conversation context passed through API requests
**Rationale**: Aligns with the constitutional requirement that the chatbot remain stateless. Context can be serialized and passed as part of the request to maintain conversation flow.
**Alternatives considered**:
- Server-side session storage: Would violate statelessness requirement
- Client-side context management: Less reliable and secure

### 4. API Adapter Pattern
**Decision**: Create dedicated adapter classes to interface with Phase II backend APIs
**Rationale**: Provides clean separation and allows for easy mocking during testing. Makes it easier to adapt to any API changes in Phase II.
**Alternatives considered**:
- Direct HTTP calls from services: Would create tight coupling
- Shared client library: Would require modifying Phase II code

### 5. Authentication Handling
**Decision**: Create authentication adapter that delegates to Phase II authentication system
**Rationale**: Maintains compliance with constitution requirement to delegate authentication to Phase II while providing clean interface for Phase III components.
**Alternatives considered**:
- Implementing separate auth: Would violate constitution
- Bypassing auth: Would be insecure

### 6. Error Handling Strategy
**Decision**: Implement comprehensive error handling with graceful degradation and user-friendly messages
**Rationale**: Ensures robust operation when Phase II APIs are unavailable and provides good UX when natural language processing fails.
**Alternatives considered**:
- Minimal error handling: Would lead to poor user experience
- Generic error messages: Would not be helpful to users

## Technology Stack Recommendations

### Backend Technologies
- **Python 3.11**: For MCP server and backend services
- **FastAPI**: For API endpoints and service interfaces
- **spaCy or transformers**: For NLP and intent classification
- **httpx**: For async HTTP requests to Phase II backend
- **mcp library**: For Model Context Protocol implementation

### Testing Frameworks
- **pytest**: For unit and integration tests
- **pytest-mock**: For mocking dependencies
- **requests-mock**: For API response mocking

### Infrastructure
- **Phase III directory**: `phase-3/` as required by constitution
- **MCP Server**: Located at `phase-3/mcp-server/`
- **Chatbot Logic**: Located at `phase-3/chatbot/`
- **API Adapters**: Located at `phase-3/adapters/`

## Architecture Patterns

### Intent Classification
1. Preprocess user input (normalization, tokenization)
2. Extract features using NLP techniques
3. Classify intent using trained model (CREATE_TODO, READ_TODOS, UPDATE_TODO, DELETE_TODO)
4. Extract entities (title, due date, status) using named entity recognition

### MCP Tool Implementation
1. Each todo operation becomes an MCP tool
2. Tools validate inputs and call appropriate service methods
3. Services use API adapters to communicate with Phase II backend
4. Results are formatted according to MCP protocol

### API Communication
1. Use HTTP clients to call Phase II backend endpoints
2. Include authentication tokens from context
3. Handle errors gracefully with retry logic
4. Transform responses to MCP-compatible formats

## Risks and Mitigations

### Natural Language Understanding Limitations
- **Risk**: AI may misinterpret user intent
- **Mitigation**: Implement confidence scoring and ask for clarification when confidence is low

### Phase II API Availability
- **Risk**: Phase II backend may be unavailable
- **Mitigation**: Implement retry logic and graceful degradation with informative error messages

### Authentication Token Propagation
- **Risk**: Authentication tokens may not be properly passed
- **Mitigation**: Create secure token propagation mechanism with validation

## Implementation Approach

### Phase 1: Core Infrastructure
1. Set up MCP server structure
2. Implement basic API adapter for Phase II backend
3. Create authentication delegation mechanism

### Phase 2: NLP Components
1. Implement intent classification system
2. Create entity extraction for todo details
3. Build response generation system

### Phase 3: Integration
1. Connect NLP components to MCP tools
2. Implement conversation context handling
3. Add comprehensive error handling and logging

### Phase 4: Testing and Validation
1. Unit tests for all components
2. Integration tests with mocked Phase II APIs
3. End-to-end testing of chatbot functionality