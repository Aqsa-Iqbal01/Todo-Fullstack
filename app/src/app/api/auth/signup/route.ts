import { NextRequest } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const { email, password, name } = await req.json();

    // Get the backend API URL from environment variables
    const BACKEND_API_URL = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'https://aqsa-iqbal-application-todo.hf.space';

    
    const response = await fetch(`${BACKEND_API_URL}/api/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        password: password,
        name: name
      }),
      redirect: 'manual'
    });

    
    if (response.status >= 300 && response.status < 400) {
      const location = response.headers.get('Location');
      if (location) {
        // Follow the redirect manually with the same headers
        const redirectResponse = await fetch(location, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: email,
            password: password,
            name: name
          })
        });
        return redirectResponse;
      }
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return Response.json(
        { error: 'Signup failed', details: errorData },
        { status: response.status }
      );
    }

    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    console.error('Signup error:', error);
    return Response.json(
      { error: 'An error occurred during signup' },
      { status: 500 }
    );
  }
}