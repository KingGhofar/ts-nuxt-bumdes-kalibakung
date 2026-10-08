export default defineEventHandler(async (event) => {
  const user = await prisma.user.findUnique({
    where: { id: requireUserId(event) },
    select: { id: true, nama: true, email: true, jabatan: true, avatar: true, role: true },
  })
  if (!user) throw createError({ statusCode: 401, statusMessage: 'Akun tidak ditemukan' })
  return user
})
