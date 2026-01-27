import { NextRequest } from 'next/server';

export async function GET(req: NextRequest) {
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

    // Prepare headers for the backend request
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // Add authorization header only if token exists
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`;
    }

    // Forward the request to the backend's todos endpoint (without trailing slash to match backend expectation)
    // Handle redirects manually to preserve auth headers
    const response = await fetch(`${BACKEND_API_URL}/api/todos`, {
      method: 'GET',
      headers: headers,
      redirect: 'manual'
    });

    // If there's a redirect, handle it manually to preserve auth headers
    if (response.status >= 300 && response.status < 400) {
      const location = response.headers.get('Location');
      if (location) {
        // Follow the redirect manually with the same headers
        const redirectResponse = await fetch(location, {
          method: 'GET',
          headers: headers
        });
        return redirectResponse;
      }
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return Response.json(
        { error: 'Failed to fetch todos', details: errorData },
        { status: response.status }
      );
    }

    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    console.error('Error fetching todos:', error);
    return Response.json(
      {
        success: false,
        error: {
          code: 'FETCH_TODOS_ERROR',
          message: 'Error fetching todos'
        }
      },
      { status: 500 }
    );
  }
}

export async function POST(req: NextRequest) {
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

    // Prepare headers for the backend request
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // Add authorization header only if token exists
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`;
    }

    // Forward the request to the backend's todos endpoint (without trailing slash to match backend expectation)
    // Ensure redirect responses also preserve authentication
    const response = await fetch(`${BACKEND_API_URL}/api/todos`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(todoData),
      redirect: 'manual'  // Handle redirects manually to preserve headers
    });

    // If there's a redirect, we need to handle it manually to preserve auth headers
    if (response.status >= 300 && response.status < 400) {
      const location = response.headers.get('Location');
      if (location) {
        // Follow the redirect manually with the same headers
        const redirectResponse = await fetch(location, {
          method: 'POST',
          headers: headers,
          body: JSON.stringify(todoData)
        });
        return redirectResponse;
      }
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return Response.json(
        { error: 'Failed to create todo', details: errorData },
        { status: response.status }
      );
    }

    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    console.error('Error creating todo:', error);
    return Response.json(
      {
        success: false,
        error: {
          code: 'CREATE_TODO_ERROR',
          message: 'Error creating todo'
        }
      },
      { status: 500 }
    );
  }
}