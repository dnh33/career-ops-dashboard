import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
    server: {
      proxy: {
        '/api': 'http://localhost:18000',
      },
    },
  },
  server: {
    port: 4321,
    host: '0.0.0.0',
  },
});
