/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  images: { unoptimized: true },
  async redirects() {
    // keep old static links like /fest.html working
    return [{ source: '/:page.html', destination: '/:page', permanent: true }, { source: '/index', destination: '/', permanent: true }];
  },
};
export default nextConfig;
