---
id: 1
title: Create Todo App Constitution
stage: constitution
date: 2026-01-06
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: 001-todo-auth-app
user: HAROON TRADERS
command: sp.constitution
labels: [constitution,setup,initial]
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
You are helping build a full-stack Todo web application as part of a hackathon project using Spec-Driven Development.

Create a detailed constitution.md file for this project. This constitution must define non-negotiable principles that ALL future specifications, plans, tasks, and implementations MUST strictly follow.

Key principles to include:
- Use exactly this tech stack: Frontend - Next.js 14+ with App Router and Tailwind CSS for beautiful, responsive, modern UI (clean, minimal, dark mode support, professional look with gradients, cards, smooth animations).
- Backend - FastAPI (Python) with SQLModel for models and migrations.
- Database - Neon DB (PostgreSQL, serverless) for persistent storage.
- Authentication - Better Auth library (secure JWT-based, email/password register/login).
- Deployment - Entire app in one repo, deployable on Vercel (Next.js for frontend + serverless API routes for FastAPI if needed, or separate Vercel functions).
- Code Quality: Type-safe (Pydantic/SQLModel), clean architecture, error handling, loading states, responsive design (mobile-first).
- Build on previous Phase 1: Extend the in-memory console Todo app logic (CRUD operations) to persistent DB with per-user todos.
- Security: Protected routes, JWT auth on all todo endpoints.
- UI Excellence: Attractive dashboard with todo list (cards/grid), add/edit modal, complete toggle, delete, due dates optional, empty state beautiful.
- No over-engineering: Keep simple but polished for hackathon demo.
- Testing: Basic manual test instructions in README.
```

## Response snapshot

Updated the constitution template with specific principles for the Todo web application, including tech stack adherence, code quality standards, full-stack integration requirements, security-first approach, UI/UX excellence, and minimalist implementation guidelines. The constitution now serves as a comprehensive guide for all future development on the project.

## Outcome

- ✅ Impact: Created foundational constitution document that will guide all future development
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific principles
- 🔁 Next prompts: Continue with feature specification based on this constitution
- 🧠 Reflection: The constitution establishes clear boundaries and requirements for the hackathon project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification