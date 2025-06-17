import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
// import vueDevTools from 'vite-plugin-vue-devtools'
// import Inspector from 'vite-plugin-vue-inspector'
// import Inspect from 'vite-plugin-inspect'
// https://vite.dev/config/
export default defineConfig({
  build: {
    sourcemap: true,
  },
  plugins: [
    vue(),
    vueJsx(),
    // vueDevTools(),
    // Inspector({
    //   enabled: true,
    //   toggleButtonVisibility: 'always',
    //   launchEditor: 'code',
    // }),
    // Inspect(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: '0.0.0.0', // 允许局域网访问
    port: 5173, // 可改为你希望使用的端口
    open: false, // 不自动打开浏览器（可选）
  },
})
