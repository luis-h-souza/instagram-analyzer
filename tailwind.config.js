/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'instagram': '#E4405F',
        'instagram-dark': '#C13584',
        'primary': '#1DA1F2',
        'secondary': '#14171A',
      },
    },
  },
  plugins: [],
}
