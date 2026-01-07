<!--
Sync Impact Report:
- Version change: 0.1.0 → 1.0.0
- Modified principles: All placeholders replaced with Todo app specific principles
- Added sections: Tech Stack Requirements, Development Workflow, Security Standards
- Removed sections: None
- Templates requiring updates: N/A
- Follow-up TODOs: None
-->
# Todo Web Application Constitution

## Core Principles

### Tech Stack Adherence
All development MUST follow the specified technology stack: Frontend - Next.js 14+ with App Router and Tailwind CSS for beautiful, responsive, modern UI (clean, minimal, dark mode support, professional look with gradients, cards, smooth animations). Backend - FastAPI (Python) with SQLModel for models and migrations. Database - Neon DB (PostgreSQL, serverless) for persistent storage. Authentication - Better Auth library (secure JWT-based, email/password register/login). This ensures consistency and deployment compatibility on Vercel.

### Code Quality and Type Safety
All code MUST be type-safe using Pydantic/SQLModel, follow clean architecture principles, include proper error handling, loading states, and responsive design (mobile-first). This ensures maintainability, reduces runtime errors, and provides a smooth user experience across all devices.

### Full-Stack Integration
The application MUST be built as a unified codebase deployable on Vercel (Next.js for frontend + serverless API routes), extending the previous Phase 1 in-memory console Todo app logic to persistent DB with per-user todos. This ensures seamless deployment and maintains continuity with existing functionality.

### Security-First Approach
All endpoints handling todo data MUST require authentication and implement proper JWT validation. Protected routes, secure session management, and proper data isolation between users are mandatory. This protects user data and ensures privacy.

### UI/UX Excellence
The application MUST feature an attractive dashboard with todo list (cards/grid), add/edit modal, complete toggle, delete functionality, optional due dates, and beautiful empty state. The UI must be polished and professional for the hackathon demo.

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
- Better Auth for 



secure JWT-based authentication with email/password

### Deployment Requirements
- Single repository containing both frontend and backend
- Deployable on Vercel (Next.js frontend + serverless API functions)
- Environment variables for configuration
- Proper build and optimization settings

## Development Workflow

### Testing Standards
- Basic manual test instructions documented in README
- Type checking must pass before commits
- Error handling validated for all user flows
- Responsive behavior tested on multiple screen sizes

### Code Review Process
- All PRs must verify compliance with this constitution
- UI changes must meet design standards
- Security requirements must be validated
- Performance impact must be considered

### Quality Gates
- All code must pass type checking
- Authentication required on protected endpoints
- Database operations must use proper SQLModel patterns
- UI must be responsive and follow accessibility guidelines

## Security Standards

### Authentication Requirements
- Better Auth library must be used consistently
- All todo endpoints require valid JWT tokens
- User data must be properly isolated
- Session management must follow security best practices

### Data Protection
- User data must not be accessible to other users
- Proper input validation on all endpoints
- SQL injection prevention through ORM usage
- Secure handling of authentication tokens

## Governance

This constitution supersedes all other development practices for this project. All specifications, plans, tasks, and implementations MUST strictly follow these principles. Amendments require explicit documentation, team approval, and migration plan if needed. All PRs and reviews must verify compliance with these principles. Complexity must be justified against the "no over-engineering" principle for the hackathon deadline.

**Version**: 1.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-06
