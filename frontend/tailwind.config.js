// frontend/tailwind.config.js

/** @type {import('tailwindcss').Config} */

export default {
  content: [
    // Шаблоны в корне
    "../templates/**/*.html",
    // Шаблоны внутри приложений (content, users и т.д.)
    "../**/templates/**/*.html",
    // JS файлы фронтенда
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}