from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, todos
from .database.database import create_db_and_tables
from dotenv import load_dotenv
import os

# Only load environment variables locally
if os.environ.get("VERCEL_ENV") is None:
    load_dotenv()

app = FastAPI(title="Todo API", version="1.0.0")

# Configure CORS for production
frontend_url = os.getenv("FRONTEND_URL", "*")  # Set this in your Vercel environment variables
print(f"FRONTEND_URL environment variable: {frontend_url}")  # Debug log
cors_origins = [frontend_url] if frontend_url != "*" else ["*"]
print(f"CORS origins: {cors_origins}")  # Debug log

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(todos.router, prefix="/api/todos", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

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
