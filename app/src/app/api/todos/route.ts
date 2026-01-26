// app/api/todos/route.ts

import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_API_URL!;

// GET todos
export async function GET(req: NextRequest) {
  const token = req.headers.get('authorization');

  const res = await fetch(`${BACKEND_URL}/api/todos`, {
    headers: {
      Authorization: token || '',
    },
  });

  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}

// CREATE todo
export async function POST(req: NextRequest) {
  const token = req.headers.get('authorization');
  const body = await req.json();

  const res = await fetch(`${BACKEND_URL}/api/todos`, {
    method: 'POST',
    headers: {
      Authorization: token || '',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}