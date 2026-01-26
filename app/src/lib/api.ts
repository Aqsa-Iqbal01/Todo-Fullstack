// lib/api.ts

/**
 * Todo API – frontend ALWAYS talks to Next.js API routes
 * (never directly to HuggingFace backend)
 */

export const todoAPI = {
  getTodos: () => {
    const token = localStorage.getItem('token');
    return fetch('/api/todos', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  createTodo: (data: any) => {
    const token = localStorage.getItem('token');
    return fetch('/api/todos', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
  },

  updateTodo: (id: string, data: any) => {
    const token = localStorage.getItem('token');
    return fetch(`/api/todos/${id}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
  },

  deleteTodo: (id: string) => {
    const token = localStorage.getItem('token');
    return fetch(`/api/todos/${id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  toggleTodo: (id: string) => {
    const token = localStorage.getItem('token');
    return fetch(`/api/todos/${id}/toggle`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
};