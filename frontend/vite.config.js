// frontend/vite.config.js

import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';
import path from 'path';

export default defineConfig({
  // 'base' важен для корректных путей к шрифтам и картинкам в CSS
  plugins: [
    tailwindcss(),
  ],
  base: '/static/dist/',
  build: {
    cssMinify: 'lightningcss',
    reportCompressedSize: false,
    chunkSizeWarningLimit: 2000,
    manifest: 'manifest.json', // Генерируем манифест
    outDir: 'dist',  // Сборка пойдет в корень проекта /static/dist
    emptyOutDir: true,
    rollupOptions: {
        input: {
          // Точка входа — ваш главный JS (или TS) файл
          main: path.resolve(__dirname, 'src/main.js'),
          contacts: path.resolve(__dirname, 'src/contacts_form.js'),
          price: path.resolve(__dirname, 'src/price_page.js'),
          filters: path.resolve(__dirname, 'src/filters.js'),
          video: path.resolve(__dirname, 'src/video.js'),
          event: path.resolve(__dirname, 'src/event_detail.js'),
          line_up: path.resolve(__dirname, 'src/line_up.js'),
          featured_slider: path.resolve(__dirname, 'src/featured_slider.js'),
          steps_section: path.resolve(__dirname, 'src/steps_section.js'),
          photo_slider: path.resolve(__dirname, 'src/photo_slider.js'),
          collage_slider: path.resolve(__dirname, 'src/collage_slider.js'),
        },
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    cors: true,
    // Чтобы в dev-режиме пути совпадали с теми, что ожидает Django
    origin: 'http://localhost:3000',
    watch: {
      ignored: ['**/node_modules/**', '**/dist/**'],
    },
  },
});
