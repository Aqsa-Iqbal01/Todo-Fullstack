"""
Simple test to verify database connectivity and todo creation
"""
import asyncio
from sqlmodel import Session, select
from backend.src.models.todo import Todo
from backend.src.models.user import User
from backend.src.database.database import get_engine, create_db_and_tables
from backend.src.models.todo import TodoCreate
from backend.src.services.todo_service import TodoService
from uuid import UUID
import uuid


def test_database_connection():
    """Test basic database connection and operations"""
    print("Testing database connection...")
    
    try:
        # Create tables first
        print("Creating database tables...")
        create_db_and_tables()
        print("Tables created successfully!")
        
        # Get a session
        engine = get_engine()
        with Session(engine) as session:
            print("Database connection successful!")
            
            # Create a dummy user for testing
            from backend.src.models.user import User
            dummy_user = User(
                email="test@example.com",
                hashed_password="dummy_hash",
                full_name="Test User"
            )
            session.add(dummy_user)
            session.commit()
            session.refresh(dummy_user)
            print(f"Created test user with ID: {dummy_user.id}")
            
            # Now test creating a todo using the service
            todo_service = TodoService(session)
            todo_create = TodoCreate(
                title="Test Todo from Database Test",
                description="This is a test todo to verify database functionality",
                completed=False
            )
            
            created_todo = todo_service.create_todo(todo_create, dummy_user.id)
            print(f"Created todo: {created_todo.title} with ID: {created_todo.id}")
            
            # Verify the todo was saved by querying it back
            retrieved_todo = todo_service.get_todo_by_id(created_todo.id, dummy_user.id)
            if retrieved_todo:
                print(f"Successfully retrieved todo: {retrieved_todo.title}")
                print("Database test PASSED!")
                return True
            else:
                print("ERROR: Could not retrieve the todo we just created")
                return False
                
    except Exception as e:
        print(f"Database test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_database_connection()
    if success:
        print("\n✓ Database connectivity test passed!")
    else:
        print("\n✗ Database connectivity test failed!")