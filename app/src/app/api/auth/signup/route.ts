import { NextRequest } from 'next/server';

// Mock user data (in memory)
let mockUsers: Array<{id: string, email: string, password: string, name: string}> = [
  {
    id: '1',
    email: 'user@example.com',
    password: 'password123',
    name: 'Test User'
  }
];

export async function POST(req: NextRequest) {
  try {
    const { email, password, name } = await req.json();

    // Check if user already exists
    const existingUser = mockUsers.find(u => u.email === email);

    if (existingUser) {
      return Response.json(
        { error: 'User already exists' },
        { status: 409 }
      );
    }

    // Create new user
    const newUser = {
      id: (mockUsers.length + 1).toString(),
      email,
      password, // In a real app, this would be hashed
      name
    };

    mockUsers.push(newUser);

    // Create a mock JWT token (in a real app, this would be properly signed)
    const tokenPayload = {
      sub: newUser.email,
      name: newUser.name,
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
        id: newUser.id,
        email: newUser.email,
        name: newUser.name
      }
    });
  } catch (error) {
    console.error('Signup error:', error);
    return Response.json(
      { error: 'An error occurred during signup' },
      { status: 500 }
    );
  }
}