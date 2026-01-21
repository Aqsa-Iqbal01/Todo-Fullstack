import { NextRequest } from 'next/server';

// Mock user data
const mockUsers = [
  {
    id: '1',
    email: 'user@example.com',
    password: 'password123', // In a real app, this would be hashed
    name: 'Test User'
  }
];

export async function POST(req: NextRequest) {
  try {
    const { email, password } = await req.json();

    // Find user by email
    const user = mockUsers.find(u => u.email === email);

    if (!user) {
      return Response.json(
        { error: 'Invalid email or password' },
        { status: 401 }
      );
    }

    // Check password (in real app, compare hashed passwords)
    if (user.password !== password) {
      return Response.json(
        { error: 'Invalid email or password' },
        { status: 401 }
      );
    }

    // Create a mock JWT token (in a real app, this would be properly signed)
    const tokenPayload = {
      sub: user.email,
      name: user.name,
      iat: Math.floor(Date.now() / 1000),
      exp: Math.floor(Date.now() / 1000) + (60 * 60 * 24) // 24 hours
    };

    // Base64 encode the payload (simplified - not a real JWT)
    const payloadString = JSON.stringify(tokenPayload);
    const encodedPayload = Buffer.from(payloadString).toString('base64');

    // Create a mock JWT: header.payload.signature
    const mockToken = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.${encodedPayload}.mocksignature`;

    return Response.json({
      access_token: mockToken,
      token_type: 'bearer',
      user: {
        id: user.id,
        email: user.email,
        name: user.name
      }
    });
  } catch (error) {
    console.error('Login error:', error);
    return Response.json(
      { error: 'An error occurred during login' },
      { status: 500 }
    );
  }
}