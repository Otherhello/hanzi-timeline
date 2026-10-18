import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// 说明：后续接入真实数据库时，可在此配置开发代理（方案 A）。
// 例如抓取小學堂：server.proxy = { '/api': { target: 'https://xiaoxue.iis.sinica.edu.tw', changeOrigin: true } }
export default defineConfig({
  plugins: [react()],
  // GitHub Pages 项目站点部署：用相对路径 base，任何仓库名下都能正确加载静态资源
  // （单页无客户端路由，相对路径是最稳妥的选择，无需关心仓库名）
  base: './',
  server: {
    port: 5173,
    // proxy: { '/api': { target: 'https://目标数据库', changeOrigin: true, rewrite: (p) => p.replace(/^\/api/, '') } },
  },
})
