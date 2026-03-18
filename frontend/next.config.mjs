/** @type {import('next').NextConfig} */
const isDev = process.env.NODE_ENV !== "production";

const nextConfig = {
  reactStrictMode: true,
  // Prevent dev/prod artifact collision:
  // - next dev   -> .next-dev
  // - next build/start -> .next
  // This avoids intermittent unstyled page (/_next/static/* 404)
  // when build/test runs while dev server is alive.
  distDir: isDev ? ".next-dev" : ".next",
};

export default nextConfig;

