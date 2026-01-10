from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..models.user import User
from datetime import datetime


class TodoService:
    def __init__(self, session: Session):
        self.session = session

    def get_user_todos(self, user_id: UUID) -> List[Todo]:
        """Get all todos for a specific user"""
        statement = select(Todo).where(Todo.user_id == user_id)
        return self.session.exec(statement).all()

    def get_todo_by_id(self, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        """Get a specific todo by ID for a specific user"""
        statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        return self.session.exec(statement).first()

    def create_todo(self, todo: TodoCreate, user_id: UUID) -> Todo:
        """Create a new todo for a user"""
        # Handle due_date conversion if it's provided
        due_date = todo.due_date
        if due_date:
            # Ensure due_date is a datetime object
            if isinstance(due_date, str):
                # Try to parse the string date
                from datetime import datetime
                try:
                    # Handle ISO format dates (e.g., "2023-12-25T10:30:00" or "2023-12-25")
                    if "T" in due_date:
                        # It's an ISO format datetime string
                        from dateutil.parser import parse
                        due_date = parse(due_date)
                    else:
                        # It's a date string, convert to datetime
                        due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                except ValueError:
                    # If parsing fails, set to None
                    due_date = None

        db_todo = Todo(
            title=todo.title,
            description=todo.description,
            completed=getattr(todo, 'completed', False),  # Safely get completed field with default
            due_date=due_date,
            user_id=user_id
        )
        self.session.add(db_todo)
        self.session.commit()
        self.session.refresh(db_todo)
        return db_todo

    def update_todo(self, todo_id: UUID, todo_update: TodoUpdate, user_id: UUID) -> Optional[Todo]:
        """Update a specific todo for a user"""
        db_todo = self.get_todo_by_id(todo_id, user_id)
        if not db_todo:
            return None

        # Update fields that are provided in the update
        update_data = todo_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "due_date" and value is not None and isinstance(value, str):
                # Handle due_date conversion if it's provided as a string
                try:
                    # Handle ISO format dates (e.g., "2023-12-25T10:30:00" or "2023-12-25")
                    if "T" in value:
                        # It's an ISO format datetime string
                        from dateutil.parser import parse
                        parsed_date = parse(value)
                        setattr(db_todo, field, parsed_date)
                    else:
                        # It's a date string, convert to datetime
                        from datetime import datetime
                        parsed_date = datetime.fromisoformat(value.replace('Z', '+00:00'))
                        setattr(db_todo, field, parsed_date)
                except ValueError:
                    # If parsing fails, set to None
                    setattr(db_todo, field, None)
            else:
                setattr(db_todo, field, value)

        db_todo.updated_at = datetime.utcnow()
        self.session.add(db_todo)
        self.session.commit()
        self.session.refresh(db_todo)
        return db_todo

    def delete_todo(self, todo_id: UUID, user_id: UUID) -> bool:
        """Delete a specific todo for a user"""
        db_todo = self.get_todo_by_id(todo_id, user_id)
        if not db_todo:
            return False

        self.session.delete(db_todo)
        self.session.commit()
        return True

    def toggle_todo_completion(self, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        """Toggle the completion status of a specific todo for a user"""
        db_todo = self.get_todo_by_id(todo_id, user_id)
        if not db_todo:
            return None

        db_todo.completed = not db_todo.completed
        db_todo.updated_at = datetime.utcnow()
        self.session.add(db_todo)
        self.session.commit()
        self.session.refresh(db_todo)
        return db_todo