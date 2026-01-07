# FastAPI Reference Guide

## API Documentation

This document provides comprehensive reference material for FastAPI development.

## Path Parameters

Path parameters are declared the same way as function parameters:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

## Query Parameters

Query parameters are declared as function parameters with default values:

```python
from typing import Union

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}
```

## Request Body

Pydantic models are used for request bodies:

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

## Request Body + Path + Query Parameters

You can combine all parameter types:

```python
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
```

## Response Model

You can declare a response model:

```python
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

## Dependencies

FastAPI supports dependency injection:

```python
from fastapi import Depends

async def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

## Security

### API Key Security

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/secure-endpoint")
async def secure_endpoint(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return {"message": "This is a secure endpoint"}
```

### OAuth2 with Password Flow

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

## Error Handling

### Custom HTTP Exceptions

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

### Custom Exception Handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )
```

## Middleware

### CORS Middleware

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing

### Testing with TestClient

```python
from fastapi.testclient import TestClient

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
```

## Database Integration

### SQLAlchemy Integration

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Pydantic Models

### Basic Model

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    full_name: str = None
    is_active: bool = True
```

### Model with Field Validation

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    description: str = None
```

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_email_task(email: str, message: str):
    # Simulate sending an email
    print(f"Sending email to {email}: {message}")

@app.post("/send-email/")
async def send_email(background_tasks: BackgroundTasks, email: str, message: str):
    background_tasks.add_task(send_email_task, email, message)
    return {"message": "Email will be sent shortly"}
```

## Upload Files

```python
from fastapi import File, UploadFile

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
```

## Environment Variables

### Using Pydantic Settings

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "your-secret-key"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```