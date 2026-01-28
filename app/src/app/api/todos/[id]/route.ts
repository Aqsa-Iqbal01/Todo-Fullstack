import { NextRequest } from 'next/server';

export async function PUT(req: NextRequest, { params }: { params: { id: string } }) {
  try {
    // Extract the token from the Authorization header
    const authHeader = req.headers.get('authorization');
    let authToken = null;

    if (authHeader) {
      // Handle different possible formats: 'Bearer token', 'bearer token', 'token'
      const header = authHeader.trim();
      if (header.toLowerCase().startsWith('bearer ')) {
        authToken = header.substring(7).trim(); // Remove 'Bearer ' prefix
      } else if (header.toLowerCase() !== 'bearer' && header.trim() !== '') {
        authToken = header; // Assume it's just the token
      }
    }

    // Extract the todo data from the request body
    const todoData = await req.json();

    // Get the backend API URL from environment variables
    const BACKEND_API_URL = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'https://aqsa-iqbal-application-todo.hf.space';

    // Extract the ID from the URL
    const { id } = params;

    // Prepare headers for the backend request
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // Add authorization header only if token exists
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`;
    }

    // Forward the request to the backend's todos endpoint (without trailing slash to match backend's redirect target)
    // Handle redirects manually to preserve auth headers
    const response = await fetch(`${BACKEND_API_URL}/api/todos/${id}`, {
      method: 'PUT',
      headers: headers,
      body: JSON.stringify(todoData),
      redirect: 'manual'  // Handle redirects manually to preserve headers
    });

    // If there's a redirect, handle it manually to preserve auth headers
    if (response.status >= 300 && response.status < 400) {
      const location = response.headers.get('Location');
      if (location) {
        // Follow the redirect manually with the same headers
        const redirectResponse = await fetch(location, {
          method: 'PUT',
          headers: headers,
          body: JSON.stringify(todoData)
        });
        return redirectResponse;
      }
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return Response.json(
        { error: 'Failed to update todo', details: errorData },
        { status: response.status }
      );
    }

    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    console.error('Error updating todo:', error);
    return Response.json(
      {
        success: false,
        error: {
          code: 'UPDATE_TODO_ERROR',
          message: 'Error updating todo'
        }
      },
      { status: 500 }
    );
  }
}

export async function DELETE(req: NextRequest, { params }: { params: { id: string } }) {
  try {
    // Extract the token from the Authorization header
    const authHeader = req.headers.get('authorization');
    let authToken = null;

    if (authHeader) {
      // Handle different possible formats: 'Bearer token', 'bearer token', 'token'
      const header = authHeader.trim();
      if (header.toLowerCase().startsWith('bearer ')) {
        authToken = header.substring(7).trim(); // Remove 'Bearer ' prefix
      } else if (header.toLowerCase() !== 'bearer' && header.trim() !== '') {
        authToken = header; // Assume it's just the token
      }
    }

    // Get the backend API URL from environment variables
    const BACKEND_API_URL = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'https://aqsa-iqbal-application-todo.hf.space';

    // Extract the ID from the URL
    const { id } = params;

    // Prepare headers for the backend request
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // Add authorization header only if token exists
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`;
    }

    // Forward the request to the backend's todos endpoint (without trailing slash to match backend's redirect target)
    // Handle redirects manually to preserve auth headers
    const response = await fetch(`${BACKEND_API_URL}/api/todos/${id}`, {
      method: 'DELETE',
      headers: headers,
      redirect: 'manual'  // Handle redirects manually to preserve headers
    });

    // If there's a redirect, handle it manually to preserve auth headers
    if (response.status >= 300 && response.status < 400) {
      const location = response.headers.get('Location');
      if (location) {
        // Follow the redirect manually with the same headers
        const redirectResponse = await fetch(location, {
          method: 'DELETE',
          headers: headers
        });
        return redirectResponse;
      }
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return Response.json(
        { error: 'Failed to delete todo', details: errorData },
        { status: response.status }
      );
    }

    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    console.error('Error deleting todo:', error);
    return Response.json(
      {
        success: false,
        error: {
          code: 'DELETE_TODO_ERROR',
          message: 'Error deleting todo'
        }
      },
      { status: 500 }
    );
  }
}

