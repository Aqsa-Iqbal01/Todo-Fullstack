import { NextRequest } from 'next/server';

// Proxy for todos API
export async function GET(request: NextRequest) {
  try {
    const backendUrl = process.env.BACKEND_URL || 'https://aqsa-iqbal-application-todo.hf.space';
    const url = `${backendUrl}/api/todos`;

    const token = request.headers.get('authorization')?.replace('Bearer ', '');

    const response = await fetch(url, {
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
    return Response.json({ error: 'Failed to fetch todos' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const backendUrl = process.env.BACKEND_URL || 'https://aqsa-iqbal-application-todo.hf.space';
    const url = `${backendUrl}/api/todos`;

    const token = request.headers.get('authorization')?.replace('Bearer ', '');
    const body = await request.json();

    const response = await fetch(url, {
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
    return Response.json({ error: 'Failed to create todo' }, { status: 500 });
  }
}

export async function PUT(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const backendUrl = process.env.BACKEND_URL || 'https://aqsa-iqbal-application-todo.hf.space';
    const url = `${backendUrl}/api/todos/${params.id}`;

    const token = request.headers.get('authorization')?.replace('Bearer ', '');
    const body = await request.json();

    const response = await fetch(url, {
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
    return Response.json({ error: 'Failed to update todo' }, { status: 500 });
  }
}

export async function DELETE(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const backendUrl = process.env.BACKEND_URL || 'https://aqsa-iqbal-application-todo.hf.space';
    const url = `${backendUrl}/api/todos/${params.id}`;

    const token = request.headers.get('authorization')?.replace('Bearer ', '');

    const response = await fetch(url, {
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
    return Response.json({ error: 'Failed to delete todo' }, { status: 500 });
  }
}