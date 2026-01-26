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
    console.error('Backend API URL is not configured');
    return new Response(JSON.stringify({ error: 'Backend API URL is not configured' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    // Extract the path from the original request
    const url = new URL(req.url);
    let pathname = url.pathname;

    // Remove the /api/proxy prefix to get the actual API path
    if (pathname.startsWith('/api/proxy')) {
      pathname = pathname.replace('/api/proxy', '');
      // Ensure there's a leading slash if pathname is not empty after replacement
      if (pathname && !pathname.startsWith('/')) {
        pathname = '/' + pathname;
      } else if (!pathname || pathname === '/') {
        // If pathname is empty or just '/', set it to '/' to hit the root of the target API
        pathname = '/';
      }
    }

    const queryString = url.search;
    const targetUrl = `${TARGET_API_URL}${pathname}${queryString}`;

    console.log(`Proxying request: ${req.method} ${targetUrl}`);

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

    console.log(`Target response status: ${response.status}`);

    // Get the response body
    let responseBody;
    try {
      responseBody = await response.text(); // Use text() to handle both JSON and non-JSON responses
    } catch (e) {
      console.error('Error reading response body:', e);
      responseBody = '{}'; // Default empty JSON object if there's an error
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
    return new Response(JSON.stringify({
      error: 'Proxy request failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}