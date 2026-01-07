---
name: todo-app
description: Comprehensive Todo application development assistance including full-stack implementation with authentication, CRUD operations, real-time updates, responsive UI, and deployment. Use when Claude needs to work with Todo applications for: (1) Creating new Todo app projects, (2) Implementing authentication (login/register), (3) Building CRUD operations for todos, (4) Managing user sessions, (5) Creating responsive UI components, (6) Integrating with backend APIs, (7) Adding task features like due dates, completion status, and descriptions, or (8) Implementing security best practices.
---

# Todo App

## Overview

A comprehensive full-stack Todo application with user authentication, CRUD operations, and responsive UI. This skill provides assistance for developing Todo applications with features like user authentication, task management, responsive design, and proper state management.

## Quick Start Guide

### Creating a Basic Todo App

```bash
# Backend (FastAPI)
pip install fastapi uvicorn sqlalchemy pydantic python-multipart python-jose[cryptography] passlib[bcrypt]

# Frontend (Next.js)
npx create-next-app@latest todo-app --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
cd todo-app
npm install axios react-icons
```

### Basic Todo Component Structure

```tsx
// components/TodoCard.tsx
interface Todo {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  due_date: string | null;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TodoCardProps {
  todo: Todo;
  onEdit: (todo: Todo) => void;
  onDelete: (id: string) => void;
  onToggle: (id: string) => void;
}

const TodoCard: React.FC<TodoCardProps> = ({ todo, onEdit, onDelete, onToggle }) => {
  // Implementation here
};
```

## Core Capabilities

### 1. Project Structure

Create a standard Todo app project structure:

```
todo-app/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application entry point
│   ├── models/             # Database models
│   │   ├── __init__.py
│   │   └── todo.py
│   ├── schemas/            # Pydantic schemas
│   │   ├── __init__.py
│   │   └── todo.py
│   ├── database/           # Database configuration
│   │   ├── __init__.py
│   │   └── database.py
│   ├── auth/               # Authentication logic
│   │   ├── __init__.py
│   │   └── auth.py
│   └── api/                # API routes
│       ├── __init__.py
│       └── routes/
│           ├── __init__.py
│           └── todo.py
├── app/                    # Next.js frontend
│   ├── src/
│   │   ├── app/            # App Router pages
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx    # Landing page
│   │   │   ├── login/      # Login page
│   │   │   ├── register/   # Register page
│   │   │   └── dashboard/  # Dashboard page
│   │   ├── components/     # Reusable components
│   │   │   ├── TodoList.tsx
│   │   │   ├── TodoCard.tsx
│   │   │   ├── TodoModal.tsx
│   │   │   └── Navbar.tsx
│   │   ├── lib/            # Utility functions
│   │   │   └── api.ts      # API client
│   │   ├── contexts/       # React contexts
│   │   │   └── ThemeContext.tsx
│   │   └── types/          # TypeScript types
│   │       └── index.ts
│   ├── public/
│   └── package.json
└── README.md
```

### 2. Authentication System

#### API Authentication Routes

```python
# backend/auth/auth.py
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.user import User as UserModel

SECRET_KEY = "your-secret-key"
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

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
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

    user = db.query(UserModel).filter(UserModel.email == username).first()
    if user is None:
        raise credentials_exception
    return user
```

#### Frontend Authentication API Client

```ts
// app/src/lib/api.ts
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

### 3. Todo Operations

#### Todo Model (Backend)

```python
# backend/models/todo.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.database import Base

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

#### Todo Schema (Backend)

```python
# backend/schemas/todo.py
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[datetime] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class Todo(TodoBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### 4. Frontend Components

#### Todo Card Component

```tsx
// app/src/components/TodoCard.tsx
import React from 'react';
import { Todo } from '@/types';

interface TodoCardProps {
  todo: Todo;
  onEdit: (todo: Todo) => void;
  onDelete: (id: string) => void;
  onToggle: (id: string) => void;
}

const TodoCard: React.FC<TodoCardProps> = ({ todo, onEdit, onDelete, onToggle }) => {
  const handleToggle = () => {
    onToggle(todo.id);
  };

  const handleEdit = () => {
    onEdit(todo);
  };

  const handleDelete = () => {
    onDelete(todo.id);
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  return (
    <div className={`rounded-2xl shadow-lg p-4 border-l-4 backdrop-blur-sm bg-white/30 dark:bg-gray-800/30 bg-gradient-to-br transform transition-all duration-300 hover:shadow-xl hover:-translate-y-1 ${
      todo.completed
        ? 'border-green-500 dark:border-green-600 from-green-50/50 to-emerald-50/50 dark:from-green-900/20 dark:to-emerald-900/20'
        : 'border-indigo-500 dark:border-indigo-600 from-blue-50/50 to-indigo-50/50 dark:from-indigo-900/20 dark:to-indigo-900/20'
    }`}>
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-start space-x-2">
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={handleToggle}
              className="sr-only"
              id={`toggle-${todo.id}`}
            />
            <label
              htmlFor={`toggle-${todo.id}`}
              className={`flex-shrink-0 mt-1 cursor-pointer rounded-full w-6 h-6 flex items-center justify-center transition-colors duration-300 ${
                todo.completed
                  ? 'bg-green-500 dark:bg-green-600 shadow-md'
                  : 'bg-gray-300 dark:bg-gray-600 border-2 border-dashed border-gray-400 dark:border-gray-500 shadow-md'
              }`}
            >
              {todo.completed && (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-white" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              )}
            </label>
            <div className="flex flex-col flex-1 min-w-0">
              <div className="flex items-center space-x-2 min-w-0 flex-1">
                <h3 className={`text-lg font-semibold min-w-0 truncate ${
                  todo.completed
                    ? 'line-through text-gray-600 dark:text-gray-400 decoration-gray-400 dark:decoration-gray-500'
                    : 'text-gray-800 dark:text-gray-200'
                }`}>
                  {todo.title}
                </h3>
                <span className={`px-2 py-1 text-xs font-semibold rounded-full flex-shrink-0 ${
                  todo.completed
                    ? 'bg-green-200 dark:bg-green-900/50 text-green-800 dark:text-green-200'
                    : 'bg-yellow-200 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-200'
                }`}>
                  {todo.completed ? 'Complete' : 'Pending'}
                </span>
                <div className="flex space-x-1">
                  <button
                    onClick={handleEdit}
                    className={`p-1.5 rounded-lg transition-all duration-200 hover:scale-110 ${
                      todo.completed
                        ? 'text-green-600 dark:text-green-400 hover:text-green-800 dark:hover:text-green-300 hover:bg-green-100 dark:hover:bg-green-800/50 shadow-sm'
                        : 'text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 hover:bg-indigo-100 dark:hover:bg-indigo-800/50 shadow-sm'
                    }`}
                    aria-label="Edit"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                    </svg>
                  </button>
                  <button
                    onClick={handleDelete}
                    className={`p-1.5 rounded-lg transition-all duration-200 hover:scale-110 flex-shrink-0 ${
                      todo.completed
                        ? 'text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 hover:bg-red-100 dark:hover:bg-red-800/50 shadow-sm'
                        : 'text-red-700 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300 hover:bg-red-100 dark:hover:bg-red-800/50 shadow-sm'
                    }`}
                    aria-label="Delete"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          {todo.description && (
            <p className={`mt-2 text-sm ${
              todo.completed
                ? 'text-gray-500 dark:text-gray-400'
                : 'text-gray-600 dark:text-gray-300'
            }`}>
              {todo.description}
            </p>
          )}
        </div>
      </div>

      <div className="flex items-center justify-between mt-4 pt-3 border-t border-gray-200/50 dark:border-gray-700/50">
        {todo.due_date && (
          <div className="flex items-center">
            <div className={`p-2 rounded-lg ${
              todo.completed
                ? 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400'
                : 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
            }`}>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <span className={`ml-2 text-xs font-medium ${
              todo.completed
                ? 'text-green-700 dark:text-green-400'
                : 'text-blue-700 dark:text-blue-400'
            }`}>
              Due: {formatDate(todo.due_date)}
            </span>
          </div>
        )}

        <div className="text-xs text-gray-500 dark:text-gray-400">
          {formatDate(todo.created_at)}
        </div>
      </div>

      {todo.updated_at !== todo.created_at && (
        <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 text-right">
          Updated: {formatDate(todo.updated_at)}
        </div>
      )}
    </div>
  );
};

export default TodoCard;
```

### 5. Dashboard Page with Statistics

```tsx
// app/src/app/dashboard/page.tsx
"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import TodoList from '@/components/TodoList';
import TodoModal from '@/components/TodoModal';
import Navbar from '@/components/Navbar';
import { todoAPI } from '@/lib/api';

interface Todo {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  due_date: string | null;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export default function DashboardPage() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [currentTodo, setCurrentTodo] = useState<Todo | null>(null);
  const [userName, setUserName] = useState<string | null>(null);
  const router = useRouter();

  // Check if user is authenticated and get user info
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    // Extract user info from token
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      const tokenData = JSON.parse(jsonPayload);
      const email = tokenData.sub || null;

      // Extract name from email (before @ symbol) or use email as fallback
      if (email) {
        const name = email.split('@')[0];
        setUserName(name);
      }
    } catch (error) {
      console.error('Error decoding token:', error);
      // Fallback: try to get user info from localStorage if stored there
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        try {
          const user = JSON.parse(storedUser);
          const name = user.email ? user.email.split('@')[0] : 'User';
          setUserName(name);
        } catch (parseError) {
          console.error('Error parsing stored user:', parseError);
          setUserName('User');
        }
      } else {
        setUserName('User');
      }
    }
  }, [router]);

  // Load todos
  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const response = await todoAPI.getTodos();
        if (response.ok) {
          const data = await response.json();
          setTodos(data);
        } else {
          console.error('Failed to fetch todos');
          // If unauthorized, redirect to login
          if (response.status === 401) {
            localStorage.removeItem('token');
            router.push('/login');
          }
        }
      } catch (error) {
        console.error('Error fetching todos:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTodos();
  }, [router]);

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
      } else {
        console.error('Failed to delete todo');
        // If unauthorized, redirect to login
        if (response.status === 401) {
          localStorage.removeItem('token');
          router.push('/login');
        }
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
      } else {
        console.error('Failed to toggle todo');
        // If unauthorized, redirect to login
        if (response.status === 401) {
          localStorage.removeItem('token');
          router.push('/login');
        }
      }
    } catch (error) {
      console.error('Error toggling todo:', error);
    }
  };

  const handleSaveTodo = async (todoData: Partial<Todo>) => {
    try {
      if (currentTodo) {
        // Update existing todo
        const response = await todoAPI.updateTodo(currentTodo.id, todoData);
        if (response.ok) {
          const updatedTodo = await response.json();
          setTodos(todos.map(todo =>
            todo.id === currentTodo.id ? updatedTodo : todo
          ));
        } else {
          console.error('Failed to update todo');
          // If unauthorized, redirect to login
          if (response.status === 401) {
            localStorage.removeItem('token');
            router.push('/login');
          }
        }
      } else {
        // Create new todo
        const response = await todoAPI.createTodo(todoData);
        if (response.ok) {
          const newTodo = await response.json();
          setTodos([...todos, newTodo]);
        } else {
          console.error('Failed to create todo');
          // If unauthorized, redirect to login
          if (response.status === 401) {
            localStorage.removeItem('token');
            router.push('/login');
          }
        }
      }
    } catch (error) {
      console.error('Error saving todo:', error);
    }
    setShowModal(false);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <Navbar />
        <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 mb-6">
              <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-indigo-600"></div>
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Loading your dashboard</h2>
            <p className="text-gray-600 max-w-md mx-auto">
              Preparing your personalized task management experience...
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Calculate statistics
  const totalTasks = todos.length;
  const completedTasks = todos.filter(todo => todo.completed).length;
  const pendingTasks = totalTasks - completedTasks;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Navbar />
      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-8 space-y-6 lg:space-y-0">
          <div className="flex-1">
            <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              Your Todo Dashboard
            </h1>
            {userName && (
              <p className="mt-2 text-gray-600 dark:text-white text-lg">
                Welcome back, <span className="font-semibold text-indigo-700 dark:text-indigo-300">{userName}</span>! Stay organized and boost your productivity
              </p>
            )}
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 min-w-fit">
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-4 border border-gray-200/50 dark:border-gray-700/50 shadow-sm">
              <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">{totalTasks}</div>
              <div className="text-sm text-gray-600 dark:text-gray-300">Total Tasks</div>
            </div>
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-4 border border-gray-200/50 dark:border-gray-700/50 shadow-sm">
              <div className="text-2xl font-bold text-green-600 dark:text-green-400">{pendingTasks}</div>
              <div className="text-sm text-gray-600 dark:text-gray-300">Pending</div>
            </div>
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-4 border border-gray-200/50 dark:border-gray-700/50 shadow-sm">
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{completedTasks}</div>
              <div className="text-sm text-gray-600 dark:text-gray-300">Completed</div>
            </div>
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-4 border border-gray-200/50 dark:border-gray-700/50 shadow-sm">
              <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">{completionRate}%</div>
              <div className="text-sm text-gray-600 dark:text-gray-300">Complete</div>
            </div>
          </div>
        </div>

        {/* Action Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8 space-y-4 sm:space-y-0">
          <div className="flex items-center space-x-4">
            <button
              onClick={handleCreateTodo}
              className="flex items-center bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-0.5"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Add New Task
            </button>
          </div>
        </div>

        {/* Progress Section */}
        {totalTasks > 0 && (
          <div className="mb-8 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-200/50 dark:border-gray-700/50 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Your Progress</span>
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{completionRate}% Complete</span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
              <div
                className="bg-gradient-to-r from-green-400 to-green-600 h-3 rounded-full transition-all duration-1000 ease-out"
                style={{ width: `${completionRate}%` }}
              ></div>
            </div>
          </div>
        )}

        {/* Todo List */}
        {todos.length === 0 ? (
          <div className="text-center py-16">
            <div className="mx-auto h-24 w-24 rounded-full bg-gradient-to-r from-indigo-100 to-purple-100 dark:from-indigo-900/30 dark:to-purple-900/30 flex items-center justify-center mb-6">
              <svg className="h-12 w-12 text-indigo-400 dark:text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="mt-4 text-xl font-medium text-gray-900 dark:text-white">No tasks yet</h3>
            <p className="mt-2 text-gray-600 dark:text-gray-300 max-w-md mx-auto">
              Get started by creating your first task. You'll be amazed at how much you can accomplish!
            </p>
            <div className="mt-8">
              <button
                onClick={handleCreateTodo}
                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-xl text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 hover:-translate-y-0.5"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
                Create Your First Task
              </button>
            </div>
          </div>
        ) : (
          <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-200/50 dark:border-gray-700/50 overflow-hidden">
            <div className="p-6 border-b border-gray-200/50 dark:border-gray-700/50">
              <h2 className="text-lg font-semibold text-gray-800 dark:text-white">Your Tasks</h2>
              <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">Click on any task to edit or manage it</p>
            </div>
            <div className="p-6">
              <TodoList
                todos={todos}
                onEdit={handleEditTodo}
                onDelete={handleDeleteTodo}
                onToggle={handleToggleTodo}
              />
            </div>
          </div>
        )}
      </div>

      {showModal && (
        <TodoModal
          todo={currentTodo}
          onSave={handleSaveTodo}
          onClose={() => setShowModal(false)}
        />
      )}
    </div>
  );
}
```

### 6. Responsive UI with Dark Mode

#### Theme Context

```ts
// app/src/contexts/ThemeContext.tsx
'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';

interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    // Check user preference or system preference
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null;
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme) {
      setTheme(savedTheme);
    } else if (prefersDark) {
      setTheme('dark');
    }
  }, []);

  useEffect(() => {
    // Apply theme to document
    document.documentElement.classList.remove('light', 'dark');
    document.documentElement.classList.add(theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
```

### 7. Security Best Practices

#### Secure Token Storage

```ts
// app/src/lib/auth.ts
export const tokenManager = {
  setToken: (token: string) => {
    // Store token in localStorage (for demo purposes)
    // In production, consider storing sensitive tokens in httpOnly cookies
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

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Appropriate for:** Scripts for project generation, database migrations, testing utilities, or any executable code that performs automation, data processing, or specific operations.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Appropriate for:** API documentation, database schemas, component libraries, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Appropriate for:** Project templates, boilerplate code, configuration files, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.