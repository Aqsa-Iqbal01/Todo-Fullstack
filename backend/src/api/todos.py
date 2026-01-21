from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from ..models.todo import Todo, TodoCreate, TodoRead, TodoUpdate
from ..models.user import User
from ..database.database import get_engine
from ..auth.auth_handler import get_current_user
from ..services.todo_service import TodoService
from datetime import datetime
import jwt
from jwt.exceptions import PyJWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

security = HTTPBearer()

router = APIRouter()

async def get_current_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get current user from JWT token"""
    token = credentials.credentials
    SECRET_KEY = os.getenv("JWT_SECRET")
    if not SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: JWT_SECRET is not set",
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/", response_model=List[TodoRead])
async def get_todos(current_user_email: str = Depends(get_current_user_from_token)):
    """Get all todos for the current user"""
    with Session(get_engine()) as session:
        # Get the user first
        user_statement = select(User).where(User.email == current_user_email)
        user = session.exec(user_statement).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Use TodoService to get todos
        todo_service = TodoService(session)
        todos = todo_service.get_user_todos(user.id)
        return todos

@router.post("/", response_model=TodoRead)
async def create_todo(todo: TodoCreate, current_user_email: str = Depends(get_current_user_from_token)):
    """Create a new todo for the current user"""
    with Session(get_engine()) as session:
        # Get the user first
        user_statement = select(User).where(User.email == current_user_email)
        user = session.exec(user_statement).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Use TodoService to create todo
        todo_service = TodoService(session)
        db_todo = todo_service.create_todo(todo, user.id)
        return db_todo

@router.put("/{todo_id}", response_model=TodoRead)
async def update_todo(todo_id: UUID, todo: TodoUpdate, current_user_email: str = Depends(get_current_user_from_token)):
    """Update an existing todo for the current user"""
    with Session(get_engine()) as session:
        # Get the user first
        user_statement = select(User).where(User.email == current_user_email)
        user = session.exec(user_statement).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Use TodoService to update todo
        todo_service = TodoService(session)
        updated_todo = todo_service.update_todo(todo_id, todo, user.id)
        if not updated_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or not authorized"
            )

        return updated_todo

@router.delete("/{todo_id}")
async def delete_todo(todo_id: UUID, current_user_email: str = Depends(get_current_user_from_token)):
    """Delete a todo for the current user"""
    with Session(get_engine()) as session:
        # Get the user first
        user_statement = select(User).where(User.email == current_user_email)
        user = session.exec(user_statement).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Use TodoService to delete todo
        todo_service = TodoService(session)
        deleted = todo_service.delete_todo(todo_id, user.id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or not authorized"
            )

        return {"message": "Todo deleted successfully"}

@router.patch("/{todo_id}/toggle", response_model=TodoRead)
async def toggle_todo_completion(todo_id: UUID, current_user_email: str = Depends(get_current_user_from_token)):
    """Toggle the completion status of a todo"""
    with Session(get_engine()) as session:
        # Get the user first
        user_statement = select(User).where(User.email == current_user_email)
        user = session.exec(user_statement).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Use TodoService to toggle todo completion
        todo_service = TodoService(session)
        toggled_todo = todo_service.toggle_todo_completion(todo_id, user.id)
        if not toggled_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or not authorized"
            )

        return toggled_todo