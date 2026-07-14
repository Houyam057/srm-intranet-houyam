import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

export default defineConfig({
  plugins: [vue()],

  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },

  server: {
    port: 8000,
    proxy: {
      "/api": {
        target: "http://localhost:8069",
        changeOrigin: true,
      },
      "/web": {
        target: "http://localhost:8069",
        changeOrigin: true,
      },
    },
  },
});