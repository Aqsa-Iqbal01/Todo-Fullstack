import { NextRequest } from 'next/server';

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

    // Forward the request to the backend's logout endpoint
    const response = await fetch(`${BACKEND_API_URL}/api/auth/logout`, {
      method: 'POST',
      headers: headers
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return Response.json(
        { error: 'Logout failed', details: errorData },
        { status: response.status }
      );
    }

    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    console.error('Logout error:', error);
    return Response.json(
      { error: 'An error occurred during logout' },
      { status: 500 }
    );
  }
}