from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, todos
from .api.chatbot import router as chatbot_router
from .database.database import create_db_and_tables
from dotenv import load_dotenv
import os


if os.environ.get("VERCEL_ENV") is None:
    load_dotenv()

app = FastAPI(title="Todo API", version="1.0.0")

# Configure CORS for production
frontend_url = os.getenv("FRONTEND_URL", "https://todo-app-fullstack-project.vercel.app")  
print(f"FRONTEND_URL environment variable: {frontend_url}")  # Debug log

# Explicitly allow your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "https://todo-app-fullstack-project.vercel.app", "http://localhost:3000", "http://localhost:3001"],  # Allow your frontend and common dev URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Important: Allow credentials to be passed
    allow_origin_regex=None,
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(todos.router, prefix="/api/todos", tags=["todos"])
app.include_router(chatbot_router, prefix="/api", tags=["chatbot"])

# For Vercel serverless, we'll create tables as needed per request
# rather than during startup

@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    import os
    from .database.database import DATABASE_URL
    # Only skip table creation on Vercel for PostgreSQL; create tables for SQLite even locally
    if os.getenv("VERCEL_ENV"):
        # On Vercel, skip if using PostgreSQL (managed DB), but not if somehow using SQLite
        # Also skip if DATABASE_URL is None (which indicates misconfiguration)
        if DATABASE_URL is None:
            print("ERROR: DATABASE_URL is not configured for Vercel deployment!")
            return
        elif "postgresql" in DATABASE_URL.lower():
            print("Skipping table creation on Vercel with PostgreSQL")
            return

    # Create tables for local development (SQLite) or Vercel with SQLite
    from .database.database import create_db_and_tables
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/test-cors")
def test_cors():
    """Test endpoint to check if CORS is working"""
    return {"message": "CORS test successful", "timestamp": "now"}

@app.get("/debug/env")
def debug_env():
    """Debug endpoint to check environment variables"""
    return {
        "FRONTEND_URL": os.getenv("FRONTEND_URL"),
        "VERCEL_ENV": os.getenv("VERCEL_ENV"),
        "DATABASE_URL_SET": bool(os.getenv("DATABASE_URL")),
        "JWT_SECRET_SET": bool(os.getenv("JWT_SECRET"))
    }

# This is important for Vercel
try:
    import uvicorn
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
except ImportError:
    pass
