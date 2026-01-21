from sqlmodel import SQLModel
from ..models.user import User
from ..models.todo import Todo
import os
from urllib.parse import urlparse
from sqlalchemy import create_engine, event
from sqlalchemy.pool import StaticPool
import sqlite3

# Get database URL from environment variable
from dotenv import load_dotenv
import os
# Load .env file from backend directory
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
env_path = os.path.join(backend_dir, '.env')
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

# For Vercel serverless functions, use SQLite in memory or file-based
# PostgreSQL drivers often cause issues in serverless environments
if not DATABASE_URL or os.getenv("VERCEL_ENV"):
    # Use SQLite for Vercel deployment to avoid psycopg2 issues
    DATABASE_URL = "sqlite:///./todo_app_vercel.db?check_same_thread=False"
    print("Using SQLite database for Vercel deployment")
else:
    print(f"Using database: {DATABASE_URL}")

def create_engine_with_retry():
    """Create database engine with proper settings for Vercel serverless"""

    # For Vercel, always use SQLite to avoid driver issues
    if os.getenv("VERCEL_ENV"):
        engine = create_engine(
            DATABASE_URL,
            echo=False,  # Turn off SQL logging in production
            connect_args={
                "check_same_thread": False  # Required for SQLite
            },
            poolclass=StaticPool,  # Use static pool for serverless
        )
    else:
        # For local development, handle both SQLite and PostgreSQL
        parsed_url = urlparse(DATABASE_URL)

        if parsed_url.scheme.startswith('postgresql'):
            # Import psycopg2 only when not on Vercel
            try:
                from sqlalchemy import create_engine
                engine = create_engine(
                    DATABASE_URL,
                    echo=False,
                    pool_pre_ping=True,
                    pool_recycle=300,
                    pool_size=1,
                    max_overflow=0,
                    connect_args={
                        "connect_timeout": 10,
                        "sslmode": "require"
                    }
                )
            except ImportError:
                # Fallback to SQLite if psycopg2 is not available
                fallback_url = "sqlite:///./todo_app_local.db?check_same_thread=False"
                print(f"Falling back to SQLite: {fallback_url}")
                engine = create_engine(fallback_url, echo=True, connect_args={"check_same_thread": False})
        else:
            # SQLite for local development
            engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

    return engine

engine = create_engine_with_retry()

def create_db_and_tables():
    """Create database tables - works in serverless environment"""
    try:
        SQLModel.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise