---
id: 001
title: Amend Constitution Phase III
stage: constitution
date: 2026-01-17
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: main
user: HAROON TRADERS
command: /sp.constitution
labels: [constitution, phase-iii, ai-chatbot, todo-app]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
# Constitution — Phase III: Todo AI Chatbot

## 1. Purpose
- Phase III introduces an AI-powered chatbot for managing todos using natural language.
- Phase III is an extension of the existing Todo Full-Stack application.
- Phase III MUST NOT disrupt or modify Phase II functionality.

## 2. Project Boundary
- Phase II project name is `todo-fullstack`.
- Phase III MUST live entirely inside:
  `todo-fullstack/phase-3/`
- Phase III code MUST be fully isolated from Phase II code.

## 3. Fixed Repository Structure
The repository structure is fixed and must not be violated:

/todo-fullstack/
├── backend/
├── frontend/
├── database/
└── phase-3/
    ├── chatbot/
    ├── mcp-server/
    ├── prompts/
    ├── services/
    ├── adapters/
    ├── tests/
    ├── config/
    └── README.md

- All AI, chatbot, and MCP logic MUST remain inside `phase-3/`.
- No chatbot logic is allowed in `backend/`, `frontend/`, or `database/`.

## 4. Phase II ↔ Phase III Integration Rules
- Phase III communicates with Phase II ONLY via HTTP APIs.
- Phase III MUST call APIs exposed by `todo-fullstack/backend`.
- Direct database access from Phase III to Phase II is strictly forbidden.
- Phase II is treated as an external, stable Todo Service.
- Existing Phase II APIs MUST NOT be modified.

## 5. Agentic Development Rules
- Development MUST follow the Agentic Dev Stack workflow:
  Specification → Plan → Tasks → Implementation
- Manual coding by the human is strictly forbidden.
- All code MUST be generated using Claude Code or AI agents.
- Human role is limited to:
  - Writing specifications
  - Reviewing generated output
  - Reporting errors
  - Approving changes

## 6. MCP (Model Context Protocol) Architecture
- Phase III MUST use Model Context Protocol (MCP).
- MCP server MUST be implemented inside:
  `phase-3/mcp-server/`
- MCP tools MUST represent Todo operations only:
  - create_todo
  - update_todo
  - delete_todo
  - list_todos
- MCP tools MUST internally call Phase II APIs.

## 7. Chatbot Behavior
- The chatbot MUST accept natural language input.
- The chatbot MUST infer user intent correctly.
- The chatbot MUST translate intent into MCP tool calls.
- The chatbot MUST remain stateless.
- Conversation context MUST be passed per request.

## 8. Security & Configuration
- All secrets and API keys MUST be stored in environment variables.
- No secrets may be hardcoded.
- Authentication and authorization are delegated to Phase II.
- Phase III MUST NOT handle user authentication directly.

## 9. Error Handling & Reliability
- All API and MCP errors MUST be logged.
- User-facing error messages MUST be clear and friendly.
- Silent failures are not allowed.
- Retry logic MUST be used for transient failures.

## 10. Testing Rules
- Tests MUST be located in `phase-3/tests/`.
- Phase II APIs MUST be mocked during testing.
- Tests MUST run independently of Phase II services.
- Intent parsing and MCP tool execution MUST be tested.

## 11. Documentation Rules
- `phase-3/README.md`
```

## Response snapshot

Updated the constitution to include Phase III requirements for the AI Chatbot extension, incorporating all the specified requirements while maintaining the existing Phase II structure and requirements.

## Outcome

- ✅ Impact: Constitution updated from v1.0.0 to v1.1.0 to include Phase III AI Chatbot requirements
- 🧪 Tests: None needed for constitution update
- 📁 Files: .specify/memory/constitution.md updated with new Phase III requirements
- 🔁 Next prompts: Ready to proceed with Phase III implementation planning
- 🧠 Reflection: Successfully integrated Phase III requirements while preserving existing functionality

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): Standard constitution update
- Next experiment (smallest change to try): Begin Phase III specification