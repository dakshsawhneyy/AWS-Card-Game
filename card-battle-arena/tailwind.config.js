/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        "dark-bg": "#0e0e16",
        "card-bg": "#1f1f2e",
      },
    },
  },
  plugins: [],
}