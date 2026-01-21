


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from pathlib import Path

# Add the root directory and phase-3 directory to the path for chatbot imports
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Add backend/src directory to the path
backend_src_dir = root_dir / "backend" / "src"
sys.path.insert(0, str(backend_src_dir))

# Add phase-3 directory to the path
phase3_dir = root_dir / "phase-3"
sys.path.insert(0, str(phase3_dir))

# Add subdirectories of phase-3 to the path
mcp_server_dir = phase3_dir / "mcp_server"
sys.path.insert(0, str(mcp_server_dir))

tools_dir = phase3_dir / "mcp_server" / "tools"
sys.path.insert(0, str(tools_dir))

chatbot_dir = phase3_dir / "chatbot"
sys.path.insert(0, str(chatbot_dir))

adapters_dir = phase3_dir / "adapters"
sys.path.insert(0, str(adapters_dir))

services_dir = phase3_dir / "services"
sys.path.insert(0, str(services_dir))

config_dir = phase3_dir / "config"
sys.path.insert(0, str(config_dir))

# Print paths for debugging
print(f"Root directory: {root_dir}")
print(f"Phase-3 directory: {phase3_dir}")
print(f"Python path: {sys.path[:5]}")  # Show first 5 paths

# Import the API modules directly instead of using relative imports
from backend.src.api import auth, todos
from backend.src.api.chatbot import router as chatbot_router
from backend.src.database.database import create_db_and_tables
from dotenv import load_dotenv

if os.environ.get("VERCEL_ENV") is None:
    load_dotenv()

app = FastAPI(title="Todo API with Chatbot", version="1.0.0")

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
    from backend.src.database.database import create_db_and_tables
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API with Chatbot"}

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)