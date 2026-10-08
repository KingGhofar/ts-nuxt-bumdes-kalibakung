import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2026-10-01',
  devtools: { enabled: false },
  css: ['~/assets/css/main.css'],
  vite: { plugins: [tailwindcss()] },
  runtimeConfig: {
    jwtSecret: '', // diisi dari NUXT_JWT_SECRET
  },
  app: {
    head: {
      title: 'BUMDes Maju Jaya',
      htmlAttrs: { lang: 'id' },
      link: [{ rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap' }],
    },
  },
})
