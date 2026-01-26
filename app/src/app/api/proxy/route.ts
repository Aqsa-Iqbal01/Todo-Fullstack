import { NextRequest } from 'next/server';

// Generic proxy route to handle various API calls
export async function GET(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const path = url.pathname.replace('/api/proxy', ''); // Extract the API path

    const backendUrl = process.env.BACKEND_URL || 'https://aqsa-iqbal-application-todo.hf.space';
    const fullUrl = `${backendUrl}${path}`;

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
    return Response.json({ error: 'Failed to fetch data' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const path = url.pathname.replace('/api/proxy', ''); // Extract the API path

    const backendUrl = process.env.BACKEND_URL || 'https://aqsa-iqbal-application-todo.hf.space';
    const fullUrl = `${backendUrl}${path}`;

    const token = request.headers.get('authorization')?.replace('Bearer ', '');
    const body = await request.json();

    const response = await fetch(fullUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    return Response.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return Response.json({ error: 'Failed to post data' }, { status: 500 });
  }
}

export async function PUT(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const path = url.pathname.replace('/api/proxy', ''); // Extract the API path

    const backendUrl = process.env.BACKEND_URL || 'https://aqsa-iqbal-application-todo.hf.space';
    const fullUrl = `${backendUrl}${path}`;

    const token = request.headers.get('authorization')?.replace('Bearer ', '');
    const body = await request.json();

    const response = await fetch(fullUrl, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    return Response.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return Response.json({ error: 'Failed to update data' }, { status: 500 });
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const path = url.pathname.replace('/api/proxy', ''); // Extract the API path

    const backendUrl = process.env.BACKEND_URL || 'https://aqsa-iqbal-application-todo.hf.space';
    const fullUrl = `${backendUrl}${path}`;

    const token = request.headers.get('authorization')?.replace('Bearer ', '');

    const response = await fetch(fullUrl, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      },
    });

    const data = await response.json();
    return Response.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return Response.json({ error: 'Failed to delete data' }, { status: response.status });
  }
}