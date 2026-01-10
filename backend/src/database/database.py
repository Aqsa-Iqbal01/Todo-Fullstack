from sqlmodel import SQLModel, create_engine
from ..models.user import User
from ..models.todo import Todo
import os
from urllib.parse import urlparse

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db?check_same_thread=False")

def create_engine_with_retry():
    """Create database engine with proper settings for Vercel serverless"""
    parsed_url = urlparse(DATABASE_URL)

    # For PostgreSQL, add connection parameters suitable for serverless
    if parsed_url.scheme.startswith('postgresql'):
        # Modify the URL to include better connection parameters for serverless
        if "?" not in DATABASE_URL:
            enhanced_url = f"{DATABASE_URL}?sslmode=require&connect_timeout=10"
        else:
            enhanced_url = f"{DATABASE_URL}&connect_timeout=10"

        engine = create_engine(
            enhanced_url,
            echo=False,  # Turn off SQL logging in production
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=1,
            max_overflow=0,
            pool_timeout=20,
            pool_reset_on_return='commit',
            connect_args={
                "connect_timeout": 10,
                "sslmode": "require"
            }
        )
    else:
        # SQLite for local development
        engine = create_engine(DATABASE_URL, echo=True)

    return engine

engine = create_engine_with_retry()

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(bind=engine)