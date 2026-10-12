// `/` juga publik: halaman pertama = portal publik (index.vue meneruskan ke /publik).
const PUBLIC = ['/', '/login', '/publik', '/register', '/verify']

export default defineNuxtRouteMiddleware(async (to) => {
  const { user, fetchMe } = useAuth()
  if (!user.value) await fetchMe()
  const isPublic = PUBLIC.includes(to.path)
  if (!user.value && !isPublic) return navigateTo('/login')
  if (user.value && to.path === '/login') return navigateTo('/dashboard')
})
