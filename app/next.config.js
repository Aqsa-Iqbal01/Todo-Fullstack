/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  // In production, API calls will go directly to the backend URL via environment variables
  // Rewrites are only needed for local development if you want to avoid CORS issues
};

module.exports = nextConfig;