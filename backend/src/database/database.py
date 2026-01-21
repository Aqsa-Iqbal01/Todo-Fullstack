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

# For Vercel deployment, use PostgreSQL directly
if os.getenv("VERCEL_ENV"):
    # Vercel provides POSTGRES_URL for PostgreSQL databases
    # If POSTGRES_URL is available, use it; otherwise fall back to DATABASE_URL
    vercel_db_url = os.getenv("POSTGRES_URL") or os.getenv("DATABASE_URL")
    if vercel_db_url and vercel_db_url.startswith("postgresql"):
        DATABASE_URL = vercel_db_url
        print(f"Using PostgreSQL for Vercel deployment: {DATABASE_URL}")
    else:
        # If no PostgreSQL URL is provided, try to use the original DATABASE_URL
        if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
            print(f"Using PostgreSQL for Vercel deployment: {DATABASE_URL}")
        else:
            # This is problematic - Vercel can't use SQLite
            print("ERROR: No PostgreSQL database URL found for Vercel deployment!")
            print("Please set either POSTGRES_URL or DATABASE_URL environment variable with PostgreSQL connection string")
else:
    # For local development, check if PostgreSQL is available, otherwise use SQLite
    if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
        # Test if we can connect to PostgreSQL, if not, fall back to SQLite
        try:
            from sqlalchemy import create_engine
            temp_engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 5})
            with temp_engine.connect() as conn:
                pass  # Connection successful
            print(f"Using PostgreSQL: {DATABASE_URL}")
        except Exception as e:
            print(f"PostgreSQL connection failed: {e}, falling back to SQLite")
            DATABASE_URL = "sqlite:///./todo_app.db?check_same_thread=False"
            print("Using SQLite for local development")
    elif DATABASE_URL:
        print(f"Using: {DATABASE_URL}")
    else:
        DATABASE_URL = "sqlite:///./todo_app.db?check_same_thread=False"
        print("Using SQLite for local development")

# Create engine - defer initialization until needed to avoid import issues
def get_engine():
    """Get database engine - initialize only when called to avoid import issues on Vercel"""
    # Set appropriate connection arguments based on database type
    if "sqlite" in DATABASE_URL:
        connect_args = {"check_same_thread": False}
    else:
        # For PostgreSQL, especially in serverless, we may need different settings
        connect_args = {
            "connect_timeout": 10,
        }

    return create_engine(
        DATABASE_URL,
        echo=False,  # Turn off SQL logging in production
        connect_args=connect_args,
        # For serverless, we should pool_recycle connections quickly
        pool_recycle=300,  # Recycle connections every 5 minutes
        pool_pre_ping=True,  # Verify connections before use
    )

def create_db_and_tables():
    """Create database tables"""
    try:
        engine = get_engine()
        SQLModel.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Warning: Could not create tables: {e}")
        # In serverless environments, table creation might fail due to read-only filesystem
        # This is expected in Vercel deployments with external databases

# For compatibility with existing code, provide engine as an instance
engine = get_engine()