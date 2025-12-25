import type { NextConfig } from "next";

const isProd = process.env.NODE_ENV === 'production';

const nextConfig: NextConfig = {
  output: isProd ? 'export' : undefined,
  async rewrites() {
    // Rewrites are not supported in export mode, so we only use them in dev
    if (isProd) return [];

    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:5000/api/:path*',
      },
    ]
  },
};

export default nextConfig;
