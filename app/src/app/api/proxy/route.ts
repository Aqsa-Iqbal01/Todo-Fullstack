import { NextRequest } from 'next/server';

// Get the target API URL from environment variables
// This should point to your Hugging Face backend URL
const TARGET_API_URL = process.env.HF_BACKEND_URL ||
                      process.env.NEXT_PUBLIC_HF_BACKEND_URL ||
                      process.env.NEXT_PUBLIC_API_BASE_URL ||
                      '';

if (!TARGET_API_URL) {
  console.warn('HF_BACKEND_URL, NEXT_PUBLIC_HF_BACKEND_URL, or NEXT_PUBLIC_API_BASE_URL environment variable is not set');
}

export async function GET(req: NextRequest) {
  return handleProxyRequest(req);
}

export async function POST(req: NextRequest) {
  return handleProxyRequest(req);
}

export async function PUT(req: NextRequest) {
  return handleProxyRequest(req);
}

export async function DELETE(req: NextRequest) {
  return handleProxyRequest(req);
}

export async function PATCH(req: NextRequest) {
  return handleProxyRequest(req);
}

export async function OPTIONS(req: NextRequest) {
  return new Response(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}

async function handleProxyRequest(req: NextRequest) {
  if (!TARGET_API_URL) {
    return Response.json(
      { error: 'Backend API URL is not configured' },
      { status: 500 }
    );
  }

  try {
    // Extract the path from the original request
    const url = new URL(req.url);
    const pathname = url.pathname.replace('/api/proxy', ''); // Remove proxy prefix
    const queryString = url.search;

    // Construct the target URL - ensure it doesn't have duplicate /api segments
    let targetUrl = `${TARGET_API_URL}${pathname}${queryString}`;

    // If pathname already starts with /api and TARGET_API_URL ends with a path that includes /api,
    // avoid duplication
    if (TARGET_API_URL.includes('.space') && pathname.startsWith('/api')) {
      // For Hugging Face spaces, the backend might already be configured to handle /api routes
      targetUrl = `${TARGET_API_URL}${pathname}${queryString}`;
    }

    // Prepare headers for the target request
    const headers: Record<string, string> = {};
    req.headers.forEach((value, key) => {
      // Forward all headers except for hop-by-hop headers that shouldn't be forwarded
      if (!['host', 'connection', 'upgrade', 'keep-alive'].includes(key.toLowerCase())) {
        headers[key] = value;
      }
    });

    // Make the request to the target API
    const response = await fetch(targetUrl, {
      method: req.method,
      headers,
      body: req.method !== 'GET' && req.method !== 'HEAD' ? await req.blob() : undefined,
    });

    // Clone the response to read it safely
    const responseClone = response.clone();

    // Get response body - handle potential empty responses
    let responseBody;
    try {
      responseBody = await responseClone.blob();
    } catch (e) {
      // If there's an error reading the body, return an empty response
      responseBody = new Blob([]);
    }

    // Create response with appropriate headers
    const proxyResponse = new Response(responseBody, {
      status: response.status,
      headers: {
        'Content-Type': response.headers.get('Content-Type') || 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      },
    });

    return proxyResponse;
  } catch (error) {
    console.error('Proxy error:', error);
    return Response.json(
      { error: 'Proxy request failed', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}