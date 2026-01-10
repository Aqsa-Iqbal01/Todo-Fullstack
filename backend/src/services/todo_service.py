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
        try:
            statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
            return self.session.exec(statement).first()
        except Exception as e:
            print(f"Error getting todo by ID: {e}")
            return None

    def create_todo(self, todo: TodoCreate, user_id: UUID) -> Todo:
        """Create a new todo for a user"""
        # Handle due_date conversion if it's provided
        due_date = todo.due_date
        if due_date is not None:
            # Ensure due_date is a datetime object
            if isinstance(due_date, str):
                # Try to parse the string date
                from datetime import datetime
                try:
                    # Handle different date formats that might come from frontend calendars
                    if "T" in due_date:
                        # It's an ISO format datetime string with timezone
                        if due_date.endswith('Z'):
                            # UTC timezone - replace Z with +00:00 for fromisoformat
                            due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                        elif '+' in due_date or (due_date.count('-') > 2 and len(due_date.split('-')[-1]) > 2):  # timezone offset like +05:00 or -05:00
                            # Already has timezone info
                            due_date = datetime.fromisoformat(due_date)
                        else:
                            # Local datetime without timezone, use fromisoformat directly
                            due_date = datetime.fromisoformat(due_date)
                    else:
                        # Date only format (e.g., "2023-12-25"), convert to datetime at midnight
                        due_date = datetime.fromisoformat(due_date + ' 00:00:00')
                except ValueError:
                    try:
                        # Try alternative parsing for different formats
                        # Import here to avoid circular imports if needed
                        from dateutil.parser import parse
                        due_date = parse(due_date)
                    except (ValueError, ImportError):
                        # If all parsing fails, set to None
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
        try:
            db_todo = self.get_todo_by_id(todo_id, user_id)
            if not db_todo:
                print(f"Todo with ID {todo_id} not found for user {user_id} or user not authorized")
                return None

            # Update fields that are provided in the update
            update_data = todo_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                if field == "due_date":
                    if value is not None and isinstance(value, str):
                        # Handle due_date conversion if it's provided as a string
                        try:
                            from datetime import datetime
                            # Handle different date formats that might come from frontend calendars
                            if "T" in value:
                                # It's an ISO format datetime string with timezone
                                if value.endswith('Z'):
                                    # UTC timezone - replace Z with +00:00 for fromisoformat
                                    parsed_date = datetime.fromisoformat(value.replace('Z', '+00:00'))
                                elif '+' in value or (value.count('-') > 2 and len(value.split('-')[-1]) > 2):  # timezone offset like +05:00 or -05:00
                                    # Already has timezone info
                                    parsed_date = datetime.fromisoformat(value)
                                else:
                                    # Local datetime without timezone, use fromisoformat directly
                                    parsed_date = datetime.fromisoformat(value)
                            else:
                                # Date only format (e.g., "2023-12-25"), convert to datetime at midnight
                                parsed_date = datetime.fromisoformat(value + ' 00:00:00')

                            setattr(db_todo, field, parsed_date)
                        except ValueError:
                            try:
                                # Try alternative parsing for different formats
                                from dateutil.parser import parse
                                parsed_date = parse(value)
                                setattr(db_todo, field, parsed_date)
                            except (ValueError, ImportError):
                                # If all parsing fails, set to None
                                setattr(db_todo, field, None)
                    else:
                        # If value is None or not a string, set directly
                        setattr(db_todo, field, value)
                else:
                    setattr(db_todo, field, value)

            from datetime import datetime
            db_todo.updated_at = datetime.utcnow()
            self.session.add(db_todo)
            self.session.commit()
            self.session.refresh(db_todo)
            return db_todo
        except Exception as e:
            print(f"Error updating todo: {e}")
            self.session.rollback()
            return None

    def delete_todo(self, todo_id: UUID, user_id: UUID) -> bool:
        """Delete a specific todo for a user"""
        try:
            db_todo = self.get_todo_by_id(todo_id, user_id)
            if not db_todo:
                print(f"Todo with ID {todo_id} not found for user {user_id} or user not authorized")
                return False

            self.session.delete(db_todo)
            self.session.commit()
            print(f"Todo with ID {todo_id} successfully deleted")
            return True
        except Exception as e:
            # Rollback the session in case of error
            self.session.rollback()
            print(f"Error deleting todo: {e}")
            return False

    def toggle_todo_completion(self, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        """Toggle the completion status of a specific todo for a user"""
        try:
            db_todo = self.get_todo_by_id(todo_id, user_id)
            if not db_todo:
                print(f"Todo with ID {todo_id} not found for user {user_id} or user not authorized")
                return None

            db_todo.completed = not db_todo.completed
            from datetime import datetime
            db_todo.updated_at = datetime.utcnow()
            self.session.add(db_todo)
            self.session.commit()
            self.session.refresh(db_todo)
            return db_todo
        except Exception as e:
            # Rollback the session in case of error
            self.session.rollback()
            print(f"Error toggling todo completion: {e}")
            return None