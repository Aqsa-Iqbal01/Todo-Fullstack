from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel
from ..models.user import User, UserCreate, UserRead
from ..auth.auth_handler import (
    get_password_hash,
    authenticate_user,
    create_access_token
)
from ..database.database import engine
from datetime import timedelta


class UserLogin(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(user: UserCreate):
    """Register a new user"""
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == user.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        db_user = User(
            email=user.email,
            password_hash=get_password_hash(user.password)
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

@router.post("/login")
def login(user_credentials: UserLogin):
    """Login user and return JWT token"""
    email = user_credentials.email
    password = user_credentials.password

    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email
        }
    }

@router.post("/logout")
def logout():
    """Logout user"""
    # In a real implementation, you might want to blacklist the token
    return {"message": "Successfully logged out"}