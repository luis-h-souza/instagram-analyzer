/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ["instagram.com", "scontent.cdninstagram.com"],
  },
};

module.exports = nextConfig;
