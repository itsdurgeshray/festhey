import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  outputFileTracingRoot: dirname(fileURLToPath(import.meta.url)),
  // a separate output folder lets `next dev` run next to a production build without overwriting it
  distDir: process.env.NEXT_DIST_DIR || '.next',
  images: { unoptimized: true },
  async redirects() {
    // keep old static links like /fest.html working
    return [{ source: '/:page.html', destination: '/:page', permanent: true }, { source: '/index', destination: '/', permanent: true }];
  },
};
export default nextConfig;
