import { NextRequest } from 'next/server';

// Proxy for auth API
export async function POST(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const path = url.pathname.split('/api/proxy/auth')[1]; 

    const backendUrl = process.env.BACKEND_URL || 'https://aqsa-iqbal-application-todo.hf.space';
    const fullUrl = `${backendUrl}/api/auth${path}`;

    const body = await request.json();

    const response = await fetch(fullUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    return Response.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return Response.json({ error: 'Failed to authenticate' }, { status: 500 });
  }
}

export async function GET(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const path = url.pathname.split('/api/proxy/auth')[1]; // Extract the specific auth path

    const backendUrl = process.env.BACKEND_URL || 'https://aqsa-iqbal-application-todo.hf.space';
    const fullUrl = `${backendUrl}/api/auth${path}`;

    const token = request.headers.get('authorization')?.replace('Bearer ', '');

    const response = await fetch(fullUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      },
    });

    const data = await response.json();
    return Response.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return Response.json({ error: 'Failed to authenticate' }, { status: 500 });
  }
}