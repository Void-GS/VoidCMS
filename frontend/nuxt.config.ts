import Components from 'unplugin-vue-components/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'
import svgLoader from 'vite-svg-loader'

export default defineNuxtConfig({
  /// ///
  // Core
  devServer: {
    port: 3000,
    host: '0.0.0.0'
  },
  app: {
    pageTransition: { name: 'page', mode: 'out-in' },
    head: {
      htmlAttrs: {
        lang: 'ru'
      },
      charset: 'utf-8',
      viewport:
        'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no'
    }
  },
  experimental: {
    headNext: true
  },
  devtools: { enabled: false },
  pages: true,
  ssr: true,
  css: ['assets/styles/app.scss'],
  modules: [
    '@pinia/nuxt',
    '@pinia-plugin-persistedstate/nuxt',
    '@nuxtjs/robots'
  ],
  plugins: ['plugins/naive-ui.ts', 'plugins/auth.ts', 'plugins/maska.ts'],
  /// ///
  // Config modules
  runtimeConfig: {
    public: {
      // AutoPick from .ENV
      api: '',
      media: '',
      hcaptcha: ''
    }
  },
  robots: {
    UserAgent: '*',
    Disallow: ['/management', '/profile', '/orders', '/order']
  },
  pinia: {
    autoImports: [
      'defineStore',
      'definePiniaStore',
      'acceptHMRUpdate',
      'storeToRefs'
    ]
  },
  /// ///
  // Build
  build: {
    transpile:
      process.env.NODE_ENV === 'production'
        ? [
            'naive-ui',
            'vueuc',
            '@css-render/vue3-ssr',
            '@juggle/resize-observer',
            'date-fns',
            '@css-render/plugin-bem'
          ]
        : ['@juggle/resize-observer']
  },
  vite: {
    plugins: [
      svgLoader(),
      Components({
        dts: true,
        resolvers: [NaiveUiResolver()] // Automatically register all components in the `components` directory
      })
    ],
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@import "@/assets/styles/variables.scss";'
        }
      }
    }
  }
})
