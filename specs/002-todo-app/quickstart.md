# Quickstart Guide: Full-Stack Secure Todo Web Application

## Prerequisites

- Node.js 18+ installed
- Python 3.11+ installed
- Access to Neon PostgreSQL database
- Vercel CLI installed (for deployment)

## Environment Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd ../app
   npm install
   ```

## Environment Variables

Create `.env` files in both the backend and app directories:

**Backend (.env)**:
```env
DATABASE_URL="postgresql://username:password@ep-xxxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
JWT_SECRET="your-super-secret-jwt-key-here-make-it-long-and-random"
NEON_DB_URL="postgresql://username:password@ep-xxxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
```

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000/api"
BACKEND_API_URL="http://localhost:8000/api"
```

## Database Setup

1. Run database migrations:
   ```bash
   cd backend
   python -m src.database.migrate
   ```

## Running the Application

1. Start the backend server:
   ```bash
   cd backend
   uvicorn src.main:app --reload --port 8000
   ```

2. In a new terminal, start the frontend:
   ```bash
   cd app
   npm run dev
   ```

3. Access the application at `http://localhost:3000`

## Deployment to Vercel

1. Set up Vercel project:
   ```bash
   cd app
   vercel
   ```

2. Configure environment variables in Vercel dashboard with the same variables from the `.env` files

3. The application will be deployed with the backend API routes integrated

## API Testing

Once the backend is running, you can test the API endpoints directly:

- Register: `POST http://localhost:8000/api/auth/register`
- Login: `POST http://localhost:8000/api/auth/login`
- Todos: `GET/POST/PUT/DELETE http://localhost:8000/api/todos`

## Troubleshooting

- If you encounter database connection issues, verify your Neon DB URL is correct
- For authentication problems, ensure JWT_SECRET is consistent between backend and any deployed environments
- For frontend-backend communication issues, check that BACKEND_API_URL is properly configured