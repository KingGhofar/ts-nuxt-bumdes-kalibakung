// Semua /api/** wajib login, kecuali login, registrasi, verifikasi, & endpoint publik.
const OPEN = ['/api/auth/login', '/api/auth/register', '/api/auth/verify', '/api/auth/resend', '/api/public']

export default defineEventHandler(async (event) => {
  const path = event.path.split('?')[0]
  if (!path.startsWith('/api/') || OPEN.some(p => path.startsWith(p))) return
  const id = await readUserId(event)
  if (!id) throw createError({ statusCode: 401, statusMessage: 'Belum login' })
  event.context.userId = id
})
