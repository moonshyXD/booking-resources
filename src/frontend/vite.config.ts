import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Чтобы dev-сервер был доступен с хоста при запуске внутри Docker
    host: true,
    port: 5173,
    strictPort: true,
  },
})
