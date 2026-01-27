// API utility functions for the Todo App

// All API calls go through local routes to avoid mixed content issues
// The local API routes will proxy requests to the backend

// Auth API functions
export const authAPI = {
  login: async (email: string, password: string) => {
    // Use local API route to avoid mixed content issues
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    return response;
  },

  register: async (email: string, password: string) => {
    // Use local API route to avoid mixed content issues
    const response = await fetch('/api/auth/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    return response;
  },

  logout: async () => {
    // Use local API route to avoid mixed content issues
    const token = localStorage.getItem('token');
    const response = await fetch('/api/auth/logout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });
    return response;
  },
};

// Todo API functions
export const todoAPI = {
  getTodos: async () => {
    // Use local API route to avoid mixed content issues
    const token = localStorage.getItem('token');
    const response = await fetch('/api/todos', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });
    return response;
  },

  createTodo: async (todoData: any) => {
    // Use local API route to avoid mixed content issues
    const token = localStorage.getItem('token');
    const response = await fetch('/api/todos', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(todoData),
    });
    return response;
  },

  updateTodo: async (id: string, todoData: any) => {
    // Use local API route to avoid mixed content issues
    const token = localStorage.getItem('token');
    const response = await fetch(`/api/todos/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(todoData),
    });
    return response;
  },

  deleteTodo: async (id: string) => {
    // Use local API route to avoid mixed content issues
    const token = localStorage.getItem('token');
    const response = await fetch(`/api/todos/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });
    return response;
  },

  toggleTodo: async (id: string) => {
    // Use local API route to avoid mixed content issues
    const token = localStorage.getItem('token');
    const response = await fetch(`/api/todos/${id}/toggle`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });
    return response;
  },
}; 