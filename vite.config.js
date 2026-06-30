import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  build: {
    outDir: 'www',
    emptyOutDir: false,
    lib: {
      entry: resolve(__dirname, 'main.js'),
      name: 'IntonareNative',
      fileName: 'main',
      formats: ['iife']
    }
  }
})