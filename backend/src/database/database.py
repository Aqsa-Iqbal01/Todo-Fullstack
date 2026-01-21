from sqlmodel import SQLModel, create_engine
from ..models.user import User
from ..models.todo import Todo
import os
from dotenv import load_dotenv

# For Vercel deployment, environment variables should be set in the Vercel dashboard
# Only load .env file if we're not in Vercel environment
if not os.getenv("VERCEL_ENV"):
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    env_path = os.path.join(backend_dir, '.env')
    load_dotenv(dotenv_path=env_path)

# Determine DATABASE_URL based on environment
if os.getenv("VERCEL_ENV"):
    # For Vercel deployment, prioritize PostgreSQL URLs
    DATABASE_URL = os.getenv("POSTGRES_URL") or os.getenv("DATABASE_URL")
    if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
        print(f"Using PostgreSQL for Vercel deployment: {DATABASE_URL}")
    else:
        # This is problematic - Vercel can't use SQLite due to read-only filesystem
        print("ERROR: No PostgreSQL database URL found for Vercel deployment!")
        print("Please set either POSTGRES_URL or DATABASE_URL environment variable with PostgreSQL connection string")
        # Don't fall back to SQLite in Vercel - it won't work
        DATABASE_URL = None  # This will cause an error if used, which is better than silent failure
else:
    # For local development, check if PostgreSQL is available, otherwise use SQLite
    DATABASE_URL = os.getenv("DATABASE_URL")
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
    if DATABASE_URL is None:
        raise ValueError("DATABASE_URL is not set. Please configure your database environment variables.")

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

# For compatibility with existing code, provide engine as a function
def get_global_engine():
    """Get the global database engine instance"""
    return get_engine()