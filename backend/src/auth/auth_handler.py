from datetime import datetime, timedelta
from typing import Optional
import jwt
from jwt.exceptions import PyJWTError
import bcrypt
from sqlmodel import Session, select
from ..models.user import User, UserCreate
from ..database.database import get_engine
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET environment variable is not set. Please configure it in your .env file.")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    # Bcrypt has a 72 character limit for passwords
    
    if len(plain_password) > 72:
        plain_password = plain_password[:72]
    try:
        # Encode strings to bytes
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except ValueError as e:
        if "password cannot be longer than 72 bytes" in str(e):
            # This should not happen due to our truncation, but just in case
            password_bytes = plain_password[:72].encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        else:
            raise e

def get_password_hash(password: str) -> str:
    """Hash a password"""
    # Bcrypt has a 72 character limit for passwords
    if len(password) > 72:
        password = password[:72]
    try:
        # Encode password to bytes and hash it
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        # Return as string
        return hashed.decode('utf-8')
    except ValueError as e:
        if "password cannot be longer than 72 bytes" in str(e):
            # This should not happen due to our truncation, but just in case
            password_bytes = password[:72].encode('utf-8')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_bytes, salt)
            return hashed.decode('utf-8')
        else:
            raise e

def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate user by email and password"""
    engine = get_engine()
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str):
    """Get current user from JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        # In a real implementation, you would fetch user from database
        # For now, we'll return the email as a simple identifier
        return email
    except PyJWTError:
        return None