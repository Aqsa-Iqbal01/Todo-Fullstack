// API utility functions for the Todo App

// Use backend API for production, with fallback to mock routes when backend is not available
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8004';

/**
 * Function to make authenticated API requests
 */
export const authenticatedRequest = async (
  endpoint: string,
  options: RequestInit = {}
) => {
  const token = localStorage.getItem('token');

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    (headers as any)['Authorization'] = `Bearer ${token}`;
  }

    let url = `${API_BASE_URL}${endpoint}`; // Use base URL for all API routes

  const response = await fetch(url, {
    ...options,
    headers,
  });

  return response;
};

/**
 * Function to make unauthenticated API requests
 */
export const unauthenticatedRequest = async (
  endpoint: string,
  options: RequestInit = {}
) => {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

    let url = `${API_BASE_URL}${endpoint}`; // Use base URL for all API routes

  const response = await fetch(url, {
    ...options,
    headers,
  });

  return response;
};

// Auth API functions
export const authAPI = {
  login: async (email: string, password: string) => {
    return unauthenticatedRequest('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  },

  register: async (email: string, password: string) => {
    return unauthenticatedRequest('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  },

  logout: async () => {
    return authenticatedRequest('/api/auth/logout', {
      method: 'POST',
    });
  },
};

// Todo API functions
export const todoAPI = {
  getTodos: async () => {
    return authenticatedRequest('/api/todos');
  },

  createTodo: async (todoData: any) => {
    return authenticatedRequest('/api/todos', {
      method: 'POST',
      body: JSON.stringify(todoData),
    });
  },

  updateTodo: async (id: string, todoData: any) => {
    return authenticatedRequest(`/api/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(todoData),
    });
  },

  deleteTodo: async (id: string) => {
    return authenticatedRequest(`/api/todos/${id}`, {
      method: 'DELETE',
    });
  },

  toggleTodo: async (id: string) => {
    return authenticatedRequest(`/api/todos/${id}/toggle`, {
      method: 'PATCH',
    });
  },
}; 