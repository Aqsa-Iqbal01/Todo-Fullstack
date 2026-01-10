from sqlmodel import SQLModel, create_engine
from ..models.user import User
from ..models.todo import Todo
import os

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db?check_same_thread=False")

# For Vercel serverless functions, don't connect pool
if "postgresql" in DATABASE_URL:
    # PostgreSQL configuration for production
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Turn off SQL logging in production
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=1,  # Minimal pool for serverless
        max_overflow=0  # No overflow for serverless
    )
else:
    # SQLite for local development
    engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(bind=engine)