from sqlmodel import SQLModel, create_engine
from ..models.user import User
from ..models.todo import Todo
import os

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db?check_same_thread=False")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(bind=engine)