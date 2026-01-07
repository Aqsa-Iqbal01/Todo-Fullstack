# Full-Stack Secure Todo Web Application

This is a full-stack todo application with user authentication and persistent storage. The application allows users to register, login, and manage their personal todo lists with full CRUD functionality.

## Tech Stack

- **Frontend**: Next.js 14+ with App Router, Tailwind CSS
- **Backend**: FastAPI with Python
- **Database**: Neon PostgreSQL (serverless)
- **Authentication**: Better Auth with JWT
- **Deployment**: Vercel

## Features

- User registration and secure login
- Create, read, update, and delete personal todos
- Mark todos as complete/incomplete
- Due dates for todos
- Responsive UI with modern design
- Data isolation between users

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── models/         # SQLModel database models
│   │   ├── api/            # API route handlers
│   │   ├── database/       # Database setup and connection
│   │   ├── auth/           # Authentication handlers
│   │   └── services/       # Business logic services
│   └── requirements.txt
├── app/                    # Next.js frontend
│   ├── src/
│   │   ├── app/           # App Router pages
│   │   ├── components/    # Reusable UI components
│   │   ├── lib/           # Utility functions
│   │   └── styles/        # Global styles
│   ├── package.json
│   └── next.config.js
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Create .env file in the backend directory
   echo "DATABASE_URL=your_neon_db_url" > .env
   echo "JWT_SECRET=your_super_secret_key" >> .env
   ```

5. Run the backend:
   ```bash
   uvicorn src.main:app --reload
   ```

### Frontend Setup

1. Navigate to the app directory:
   ```bash
   cd app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   # Create .env.local file in the app directory
   echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api" > .env.local
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user and get JWT token
- `POST /api/auth/logout` - Logout user

### Todos
- `GET /api/todos` - Get all todos for the authenticated user
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/{id}` - Update an existing todo
- `DELETE /api/todos/{id}` - Delete a todo
- `PATCH /api/todos/{id}/toggle` - Toggle completion status

## Environment Variables

### Backend (.env)
- `DATABASE_URL` - Neon PostgreSQL connection string
- `JWT_SECRET` - Secret key for JWT token signing

### Frontend (.env.local)
- `NEXT_PUBLIC_API_BASE_URL` - Base URL for API requests (e.g., http://localhost:8000/api)

## Deployment

The application is designed for deployment on Vercel. Both the Next.js frontend and FastAPI backend can be deployed together using the configuration in `vercel.json`.

## Development

This project was built using the Spec-Driven Development approach with the following phases:
1. Constitution - Defined non-negotiable principles
2. Specification - Detailed feature requirements
3. Planning - Technical architecture and design
4. Tasks - Implementation breakdown
5. Implementation - Actual coding

## License

This project is part of a hackathon and is intended for demonstration purposes.