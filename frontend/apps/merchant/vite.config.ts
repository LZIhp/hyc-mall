import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@hyc/ui': fileURLToPath(new URL('../../packages/ui/src', import.meta.url)),
      '@hyc/request': fileURLToPath(new URL('../../packages/request/src', import.meta.url)),
    },
  },
  server: {
    port: 5174,
  },
})
