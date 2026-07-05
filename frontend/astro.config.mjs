import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import nodeAdapter from '@astrojs/node';

export default defineConfig({
  output: 'static',
  adapter: nodeAdapter({ mode: 'standalone' }),
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
