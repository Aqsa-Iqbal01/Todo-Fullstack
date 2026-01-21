from sqlmodel import SQLModel, create_engine
from ..models.user import User
from ..models.todo import Todo
import os

# Get database URL from environment variable
from dotenv import load_dotenv
# Load .env file from backend directory
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
env_path = os.path.join(backend_dir, '.env')
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

# For Vercel serverless, always use SQLite to avoid PostgreSQL driver issues
if os.getenv("VERCEL_ENV"):
    DATABASE_URL = "sqlite:///./todo_app.db?check_same_thread=False"
    print("Using SQLite for Vercel deployment")
else:
    # For local development, use PostgreSQL if available, otherwise SQLite
    if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
        print(f"Using PostgreSQL: {DATABASE_URL}")
    elif DATABASE_URL:
        print(f"Using: {DATABASE_URL}")
    else:
        DATABASE_URL = "sqlite:///./todo_app.db?check_same_thread=False"
        print("Using SQLite for local development")

# Create engine - defer initialization until needed to avoid import issues
def get_engine():
    """Get database engine - initialize only when called to avoid import issues on Vercel"""
    return create_engine(
        DATABASE_URL,
        echo=False,  # Turn off SQL logging in production
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
    )

def create_db_and_tables():
    """Create database tables"""
    engine = get_engine()
    SQLModel.metadata.create_all(bind=engine)

# For compatibility with existing code, provide engine as a function
engine = get_engine