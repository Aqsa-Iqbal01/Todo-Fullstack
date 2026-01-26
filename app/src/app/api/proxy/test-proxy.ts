// Test script to verify the proxy is working with the Hugging Face backend
// This simulates what the frontend would do when making a login request

async function testProxy() {
  console.log('Testing proxy connection to Hugging Face backend...');

  try {
    // Test GET request to check if proxy is accessible
    console.log('\n1. Testing proxy accessibility...');
    const response1 = await fetch('/api/proxy/');
    console.log(`Response status: ${response1.status}`);
    console.log(`Response content-type: ${response1.headers.get('content-type')}`);

    // Test the specific login endpoint that was failing
    console.log('\n2. Testing login endpoint...');
    const loginResponse = await fetch('/api/proxy/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: 'user@example.com',
        password: 'password123'
      })
    });

    console.log(`Login response status: ${loginResponse.status}`);
    console.log(`Login response content-type: ${loginResponse.headers.get('content-type')}`);

    // Try to parse the response
    let responseData;
    try {
      responseData = await loginResponse.json();
      console.log('Login response data:', responseData);
    } catch (parseError) {
      console.log('Could not parse JSON response, getting text instead:');
      const textResponse = await loginResponse.text();
      console.log('Response text:', textResponse);
    }

    console.log('\n✓ Proxy test completed successfully!');

  } catch (error) {
    console.error('✗ Proxy test failed:', error.message);
  }
}

// Run the test
testProxy();