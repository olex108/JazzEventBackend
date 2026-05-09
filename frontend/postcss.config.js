// frontend/postcss.config.js
export default {
  plugins: {
    '@tailwindcss/postcss': {}, // Используем новый пакет вместо старого 'tailwindcss'
    autoprefixer: {},
  },
}