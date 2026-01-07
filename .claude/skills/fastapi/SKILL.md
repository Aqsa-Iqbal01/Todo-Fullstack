---
name: fastapi
description: Comprehensive FastAPI development assistance including project setup, API endpoint creation, dependency injection, authentication, database integration, and deployment. Use when Claude needs to work with FastAPI for: (1) Creating new FastAPI projects, (2) Building API endpoints, (3) Adding authentication and authorization, (4) Database integration with SQLAlchemy/Pydantic, (5) Adding middleware, (6) Testing, or (7) Deployment configuration.
---

# Fastapi

## Overview

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. This skill provides comprehensive assistance for developing FastAPI applications including project structure, endpoint creation, database integration, authentication, and deployment.

## Quick Start Guide

### Creating a Basic FastAPI Application

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### Running the Application

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

## Core Capabilities

### 1. Project Structure

Create a standard FastAPI project structure:

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py          # Application instance and configuration
│   ├── api/             # API routes
│   │   ├── __init__.py
│   │   └── v1/          # API version
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── users.py
│   ├── models/          # Database models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/         # Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py
│   ├── database/        # Database configuration
│   │   ├── __init__.py
│   │   └── database.py
│   └── utils/           # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── requirements.txt
├── alembic/
├── alembic.ini
└── main.py              # Entry point for uvicorn
```

### 2. API Endpoints

#### GET Endpoints

```python
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 100):
    users = await UserModel.get_all(skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = await UserModel.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

#### POST Endpoints

```python
@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    db_user = await UserModel.get_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    created_user = await UserModel.create(user)
    return created_user
```

#### PUT and DELETE Endpoints

```python
@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    updated_user = await UserModel.update(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    success = await UserModel.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
```

## Database Integration

### SQLAlchemy Setup

```python
# app/database/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Pydantic Models and SQLAlchemy Models

```python
# app/models/user.py
from sqlalchemy import Column, Integer, String
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Integer, default=1)

# app/schemas/user.py
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: int

    class Config:
        from_attributes = True
```

## Authentication and Security

### JWT Token Authentication

```python
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_email(username)
    if user is None:
        raise credentials_exception
    return user
```

## Middleware and Error Handling

### CORS Middleware

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Don't use this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Custom Exception Handler

```python
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
```

## Testing

### Unit Testing with pytest

```python
# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
```

## Deployment Configuration

### Dockerfile

```Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Requirements.txt

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
alembic==1.13.1
python-multipart==0.0.6
```

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Appropriate for:** Python scripts for project generation, database migrations, testing utilities, or any executable code that performs automation, data processing, or specific operations.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Appropriate for:** FastAPI documentation, API reference documentation, database schemas, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Appropriate for:** Project templates, boilerplate code, configuration files, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.