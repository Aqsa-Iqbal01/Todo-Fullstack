import { NextRequest } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    // Extract the message from the request body
    const { message } = await req.json();

    // Extract the token from the Authorization header
    const authHeader = req.headers.get('authorization');
    let authToken = '';
    if (authHeader) {
      // Handle different possible formats: 'Bearer token', 'bearer token', 'token'
      const header = authHeader.trim();
      if (header.toLowerCase().startsWith('bearer ')) {
        authToken = header.substring(7).trim(); // Remove 'Bearer ' prefix
      } else if (header.toLowerCase() === 'bearer') {
        authToken = ''; // Just the word bearer, no token
      } else {
        authToken = header; // Assume it's just the token
      }
    }

    // Validate input
    if (!message || typeof message !== 'string') {
      return Response.json(
        { error: 'Invalid message provided' },
        { status: 400 }
      );
    }

    // Get the backend API URL from environment variables
    // For chatbot functionality, default to port 8001 where the MCP chatbot backend runs
    const BACKEND_API_URL = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'https://aqsa-iqbal-application-todo.hf.space';

    // Forward the request to the backend's MCP-based chatbot endpoint
    const response = await fetch(`${BACKEND_API_URL}/api/chatbot`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,  // Pass the auth token to the backend
      },
      body: JSON.stringify({
        message: message
      }),
      redirect: 'manual'
    });

    // If there's a redirect, handle it manually to preserve auth headers
    if (response.status >= 300 && response.status < 400) {
      const location = response.headers.get('Location');
      if (location) {
        // Follow the redirect manually with the same headers
        const redirectResponse = await fetch(location, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`,
          },
          body: JSON.stringify({
            message: message
          })
        });
        return redirectResponse;
      }
    }

    const data = await response.json();

    return Response.json(data);

  } catch (error) {
    console.error('Error processing chatbot request:', error);
    return Response.json(
      {
        success: false,
        error: {
          code: 'CHATBOT_PROCESSING_ERROR',
          message: 'Error processing your request'
        }
      },
      { status: 500 }
    );
  }
}