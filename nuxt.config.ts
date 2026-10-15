import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2026-10-01',
  devtools: { enabled: false },
  css: ['~/assets/css/main.css'],
  vite: { plugins: [tailwindcss()] },
  runtimeConfig: {
    jwtSecret: '', // diisi dari NUXT_JWT_SECRET
    brevoUser: '', // BREVO_USER
    brevoApiKey: '', // BREVO_API_KEY
    brevoFromEmail: '', // BREVO_FROM_EMAIL
    brevoFromName: '', // BREVO_FROM_NAME
    appUrl: '', // APP_URL
  },
  app: {
    head: {
      title: 'BUMDes Desa Kalibakung',
      htmlAttrs: { lang: 'id' },
      meta: [{ name: 'viewport', content: 'width=device-width, initial-scale=1' }],
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap' },
      ],
    },
  },
})
