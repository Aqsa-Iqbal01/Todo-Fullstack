import { NextRequest } from 'next/server';

// Test route to verify proxy functionality
export async function GET(req: NextRequest) {
  try {
    // Extract the path from the original request
    const url = new URL(req.url);
    const targetPath = url.searchParams.get('path') || '/';

    // Use the same target URL as the proxy
    const TARGET_API_URL = process.env.HF_BACKEND_URL ||
                          process.env.NEXT_PUBLIC_HF_BACKEND_URL ||
                          process.env.NEXT_PUBLIC_API_BASE_URL ||
                          'https://aqsa-iqbal-application-todo.hf.space';

    if (!TARGET_API_URL) {
      return Response.json(
        { error: 'Backend API URL is not configured' },
        { status: 500 }
      );
    }

    console.log(`Testing connection to: ${TARGET_API_URL}${targetPath}`);

    // Test the connection to the backend
    const response = await fetch(`${TARGET_API_URL}${targetPath}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.text(); // Get response as text to handle any format

    return Response.json({
      status: 'success',
      backend_url: TARGET_API_URL,
      target_path: targetPath,
      response_status: response.status,
      response_data: data.substring(0, 500) + (data.length > 500 ? '...' : '') // Limit response size
    });
  } catch (error) {
    console.error('Test error:', error);
    return Response.json({
      status: 'error',
      message: error instanceof Error ? error.message : 'Unknown error',
      backend_url: process.env.HF_BACKEND_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'Not set'
    }, { status: 500 });
  }
}