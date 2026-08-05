/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#172033',
        ocean: '#075985',
        mist: '#f4f7fb',
      },
    },
  },
  plugins: [],
}
