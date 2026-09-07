import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
      dirs: ['src/components'],
    }),
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 8080,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:8090',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
      },
      '/algo': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/algo/, '/api'),
      },
      '/file': {
        target: 'http://localhost:5001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/file/, '/api'),
      },
    },
    hmr: {
      overlay: false
    },
    watch: {
      usePolling: true
    }
  },
  optimizeDeps: {
    include: ['vue', 'vue-router', 'pinia', '@vueuse/core', 'element-plus'],
  },
  build: {
    chunkSizeWarningLimit: 2000,
    rollupOptions: {
      output: {
        manualChunks: {
          'element-plus': ['element-plus'],
          'vendor': ['vue', 'vue-router', 'pinia'],
        },
      },
    },
  },
})
