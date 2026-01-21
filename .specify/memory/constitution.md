<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- Modified principles: Updated to include Phase III AI Chatbot requirements
- Added sections: Phase III AI Chatbot, MCP Architecture, Agentic Development, Natural Language Processing
- Removed sections: None
- Templates requiring updates: ✅ Updated
- Follow-up TODOs: None
-->

# Todo Web Application Constitution - Phase III: AI Chatbot Extension

## Core Principles

### Phase III Project Boundary
Phase III MUST live entirely inside `todo-fullstack/phase-3/`. All AI, chatbot, and MCP logic MUST remain inside `phase-3/`. No chatbot logic is allowed in `backend/`, `frontend/`, or `database/`. This ensures proper isolation and modularity of the AI chatbot functionality.

### Phase II ↔ Phase III Integration
Phase III communicates with Phase II ONLY via HTTP APIs. Phase III MUST call APIs exposed by `todo-fullstack/backend`. Direct database access from Phase III to Phase II is strictly forbidden. Phase II is treated as an external, stable Todo Service. Existing Phase II APIs MUST NOT be modified. This preserves the integrity of the existing system.

### Tech Stack Adherence
All development MUST follow the specified technology stack: Frontend - Next.js 14+ with App Router and Tailwind CSS for beautiful, responsive, modern UI (clean, minimal, dark mode support, professional look with gradients, cards, smooth animations). Backend - FastAPI (Python) with SQLModel for models and migrations. Database - Neon DB (PostgreSQL, serverless) for persistent storage. Authentication - Better Auth library (secure JWT-based, email/password register/login). Phase III additionally requires MCP (Model Context Protocol) architecture for AI integration. This ensures consistency and deployment compatibility on Vercel.

### Code Quality and Type Safety
All code MUST be type-safe using Pydantic/SQLModel, follow clean architecture principles, include proper error handling, loading states, and responsive design (mobile-first). Phase III code must also follow agentic development practices with proper error logging and retry mechanisms. This ensures maintainability, reduces runtime errors, and provides a smooth user experience across all devices.

### Full-Stack Integration
The application MUST be built as a unified codebase deployable on Vercel (Next.js for frontend + serverless API routes), extending the previous Phase 1 in-memory console Todo app logic to persistent DB with per-user todos. Phase III extends this with an AI-powered chatbot for natural language todo management. This ensures seamless deployment and maintains continuity with existing functionality.

### MCP Architecture Compliance
Phase III MUST use Model Context Protocol (MCP). MCP server MUST be implemented inside `phase-3/mcp-server/`. MCP tools MUST represent Todo operations only: `create_todo`, `update_todo`, `delete_todo`, `list_todos`. MCP tools MUST internally call Phase II APIs. This ensures standardized AI integration.

### Agentic Development Rules
Development MUST follow the Agentic Dev Stack workflow: Specification → Plan → Tasks → Implementation. Manual coding by the human is strictly forbidden. All code MUST be generated using Claude Code or AI agents. Human role is limited to: Writing specifications, Reviewing generated output, Reporting errors, Approving changes. This ensures consistent automation practices.

### Natural Language Processing
The chatbot MUST accept natural language input. The chatbot MUST infer user intent correctly. The chatbot MUST translate intent into MCP tool calls. The chatbot MUST remain stateless. Conversation context MUST be passed per request. This enables intuitive user interaction with the todo system.

### Security-First Approach
All endpoints handling todo data MUST require authentication and implement proper JWT validation. Protected routes, secure session management, and proper data isolation between users are mandatory. Phase III must delegate authentication and authorization to Phase II. All secrets and API keys MUST be stored in environment variables. No secrets may be hardcoded. This protects user data and ensures privacy.

### UI/UX Excellence
The application MUST feature an attractive dashboard with todo list (cards/grid), add/edit modal, complete toggle, delete functionality, optional due dates, and beautiful empty state. The UI must be polished and professional for the hackathon demo. Phase III extends this with an AI chatbot interface for natural language interaction.

### Minimalist Implementation
All features MUST follow "no over-engineering" principle - keep simple but polished for hackathon demo. Only implement essential functionality with high-quality execution rather than complex features. This ensures timely delivery and focus on quality.

## Tech Stack Requirements

### Frontend Standards
- Next.js 14+ with App Router for modern routing and server-side rendering
- Tailwind CSS for consistent, responsive styling with dark mode support
- Modern UI patterns: cards, gradients, smooth animations, mobile-first responsive design
- Proper loading states, error boundaries, and accessibility compliance

### Backend Standards
- FastAPI for type-safe, high-performance API endpoints
- SQLModel for database models and migrations with proper relationships
- Neon DB (PostgreSQL) for persistent storage with connection pooling
- Better Auth for secure JWT-based authentication with email/password

### Phase III AI & MCP Standards
- MCP (Model Context Protocol) server implementation in `phase-3/mcp-server/`
- Natural language processing for intent recognition
- State management for conversation context
- Proper error handling and retry logic for API calls

### Deployment Requirements
- Single repository containing both frontend and backend
- Phase III isolated in `phase-3/` directory
- Deployable on Vercel (Next.js frontend + serverless API functions)
- Environment variables for configuration
- Proper build and optimization settings

## Development Workflow

### Testing Standards
- Basic manual test instructions documented in README
- Type checking must pass before commits
- Error handling validated for all user flows
- Responsive behavior tested on multiple screen sizes
- Phase II APIs MUST be mocked during Phase III testing
- Tests MUST run independently of Phase II services
- Intent parsing and MCP tool execution MUST be tested

### Code Review Process
- All PRs must verify compliance with this constitution
- UI changes must meet design standards
- Security requirements must be validated
- Performance impact must be considered
- Phase III code must be properly isolated in `phase-3/` directory
- MCP integration must follow specified architecture patterns

### Quality Gates
- All code must pass type checking
- Authentication required on protected endpoints
- Database operations must use proper SQLModel patterns
- UI must be responsive and follow accessibility guidelines
- MCP tools must properly interface with Phase II APIs
- Natural language processing must correctly interpret user intents
- Error handling must be comprehensive for both API and AI components

## Security Standards

### Authentication Requirements
- Better Auth library must be used consistently
- All todo endpoints require valid JWT tokens
- User data must be properly isolated
- Session management must follow security best practices
- Phase III must delegate authentication to Phase II

### Data Protection
- User data must not be accessible to other users
- Proper input validation on all endpoints
- SQL injection prevention through ORM usage
- Secure handling of authentication tokens
- Natural language input must be sanitized appropriately

### Phase III Specific Security
- All secrets and API keys MUST be stored in environment variables
- No secrets may be hardcoded in Phase III components
- MCP server must validate all incoming requests
- Conversation context must not expose sensitive user data

## Governance

This constitution supersedes all other development practices for this project. All specifications, plans, tasks, and implementations MUST strictly follow these principles. Phase III development MUST adhere to the specified directory structure and integration rules. Amendments require explicit documentation, team approval, and migration plan if needed. All PRs and reviews must verify compliance with these principles. Complexity must be justified against the "no over-engineering" principle for the hackathon deadline.

**Version**: 1.1.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-17