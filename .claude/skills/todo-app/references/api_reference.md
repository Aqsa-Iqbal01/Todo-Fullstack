# Todo App Reference Guide

## API Documentation

This document provides comprehensive reference material for Todo application development.

## Backend API Endpoints

### Authentication Endpoints

#### Login
```
POST /api/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "userpassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "user-uuid",
    "email": "user@example.com"
  }
}
```

#### Register
```
POST /api/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "userpassword"
}
```

**Response:**
```json
{
  "id": "user-uuid",
  "email": "user@example.com"
}
```

### Todo Endpoints

#### Get All Todos
```
GET /api/todos
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "id": "todo-uuid",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "due_date": "2023-12-31T10:00:00",
    "user_id": "user-uuid",
    "created_at": "2023-11-01T10:00:00",
    "updated_at": "2023-11-01T10:00:00"
  }
]
```

#### Create Todo
```
POST /api/todos
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "New task",
  "description": "Task description",
  "due_date": "2023-12-31T10:00:00"
}
```

**Response:**
```json
{
  "id": "todo-uuid",
  "title": "New task",
  "description": "Task description",
  "completed": false,
  "due_date": "2023-12-31T10:00:00",
  "user_id": "user-uuid",
  "created_at": "2023-11-01T10:00:00",
  "updated_at": "2023-11-01T10:00:00"
}
```

#### Update Todo
```
PUT /api/todos/{todo_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "Updated task",
  "description": "Updated description",
  "completed": true,
  "due_date": "2023-12-31T10:00:00"
}
```

**Response:**
```json
{
  "id": "todo-uuid",
  "title": "Updated task",
  "description": "Updated description",
  "completed": true,
  "due_date": "2023-12-31T10:00:00",
  "user_id": "user-uuid",
  "created_at": "2023-11-01T10:00:00",
  "updated_at": "2023-11-02T10:00:00"
}
```

#### Delete Todo
```
DELETE /api/todos/{todo_id}
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```
Status: 204 No Content
```

#### Toggle Todo Completion
```
PATCH /api/todos/{todo_id}/toggle
```

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": "todo-uuid",
  "title": "Task title",
  "description": "Task description",
  "completed": true,
  "due_date": "2023-12-31T10:00:00",
  "user_id": "user-uuid",
  "created_at": "2023-11-01T10:00:00",
  "updated_at": "2023-11-02T10:00:00"
}
```

## Frontend Components

### Todo Interface

```ts
// types/index.ts
export interface Todo {
  id: string;
  title: string;
  description: string | null;
  completed: boolean;
  due_date: string | null;
  user_id: string;
  created_at: string;
  updated_at: string;
}
```

### API Client

```ts
// lib/api.ts
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  async login(email: string, password: string) {
    return api.post('/auth/login', { email, password });
  },

  async register(email: string, password: string) {
    return api.post('/auth/register', { email, password });
  },
};

export const todoAPI = {
  async getTodos() {
    return api.get('/todos');
  },

  async createTodo(todoData: Partial<Todo>) {
    return api.post('/todos', todoData);
  },

  async updateTodo(id: string, todoData: Partial<Todo>) {
    return api.put(`/todos/${id}`, todoData);
  },

  async deleteTodo(id: string) {
    return api.delete(`/todos/${id}`);
  },

  async toggleTodo(id: string) {
    return api.patch(`/todos/${id}/toggle`);
  },
};
```

## Authentication Flow

### Login Flow

1. User enters email and password
2. Frontend sends credentials to backend
3. Backend validates credentials
4. Backend returns JWT token
5. Frontend stores token in localStorage
6. Frontend redirects to dashboard

### Register Flow

1. User enters email and password
2. Frontend sends credentials to backend
3. Backend creates user account
4. Backend returns user information
5. Frontend redirects to login page

### Token Management

```ts
// lib/auth.ts
export const tokenManager = {
  setToken: (token: string) => {
    localStorage.setItem('token', token);
  },

  getToken: (): string | null => {
    return localStorage.getItem('token');
  },

  removeToken: () => {
    localStorage.removeItem('token');
  },

  isTokenExpired: (token: string): boolean => {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      const payload = JSON.parse(jsonPayload);
      const currentTime = Math.floor(Date.now() / 1000);

      return payload.exp < currentTime;
    } catch (error) {
      console.error('Error decoding token:', error);
      return true;
    }
  }
};
```

## State Management

### Todo State in Dashboard

```tsx
// app/dashboard/page.tsx
export default function DashboardPage() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [currentTodo, setCurrentTodo] = useState<Todo | null>(null);
  const [userName, setUserName] = useState<string | null>(null);
  const router = useRouter();

  // Load todos on component mount
  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const response = await todoAPI.getTodos();
        if (response.ok) {
          const data = await response.json();
          setTodos(data);
        }
      } catch (error) {
        console.error('Error fetching todos:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTodos();
  }, []);

  const handleCreateTodo = () => {
    setCurrentTodo(null);
    setShowModal(true);
  };

  const handleEditTodo = (todo: Todo) => {
    setCurrentTodo(todo);
    setShowModal(true);
  };

  const handleDeleteTodo = async (id: string) => {
    try {
      const response = await todoAPI.deleteTodo(id);
      if (response.ok) {
        setTodos(todos.filter(todo => todo.id !== id));
      }
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  const handleToggleTodo = async (id: string) => {
    try {
      const response = await todoAPI.toggleTodo(id);
      if (response.ok) {
        const updatedTodo = await response.json();
        setTodos(todos.map(todo =>
          todo.id === id ? updatedTodo : todo
        ));
      }
    } catch (error) {
      console.error('Error toggling todo:', error);
    }
  };

  // ... render JSX
}
```

## Security Considerations

### JWT Token Security

1. **Token Storage**: Store JWT in localStorage for simplicity in this example, but consider httpOnly cookies for production
2. **Token Expiration**: Implement token expiration checks
3. **Token Refresh**: Implement refresh token mechanism for long-lived sessions
4. **CSRF Protection**: Use anti-CSRF tokens for sensitive operations

### Input Validation

```python
# schemas/todo.py
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

    @field_validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        if len(v) > 200:
            raise ValueError('Title must be less than 200 characters')
        return v

    @field_validator('description')
    def description_must_not_be_too_long(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must be less than 1000 characters')
        return v
```

## Database Models

### Todo Model

```python
# models/todo.py
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)
    user_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="todos")
```

### User Model

```python
# models/user.py
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    todos = relationship("Todo", back_populates="user")
```

## Deployment Configuration

### Environment Variables

```env
# Backend (.env)
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Docker Configuration

```dockerfile
# Backend Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Frontend Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY app/package*.json ./
RUN npm install

COPY app/ .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

## Error Handling

### Frontend Error Handling

```tsx
// components/TodoList.tsx
const TodoList: React.FC<TodoListProps> = ({ todos, onEdit, onDelete, onToggle }) => {
  const [error, setError] = useState<string | null>(null);

  const handleDelete = async (id: string) => {
    try {
      await todoAPI.deleteTodo(id);
      onDelete(id);
    } catch (err) {
      setError('Failed to delete todo. Please try again.');
      console.error('Delete error:', err);
    }
  };

  // ... rest of component
};
```

### Backend Error Handling

```python
# api/routes/todo.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from models.todo import Todo as TodoModel
from schemas.todo import TodoCreate, TodoUpdate
from auth.auth import get_current_user

router = APIRouter()

@router.get("/")
async def get_todos(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        todos = db.query(TodoModel).filter(TodoModel.user_id == current_user.id).all()
        return todos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching todos"
        )
```