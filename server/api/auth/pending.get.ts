// Daftar akun menunggu persetujuan (sudah verifikasi email, approved=false).
// Endpoint akses disetujui SUPER_ADMIN di level route itu sendiri.
export default defineEventHandler(async (event) => {
  const me = await prisma.user.findUnique({ where: { id: requireUserId(event) } })
  if (me?.role !== 'SUPER_ADMIN') throw createError({ statusCode: 403, statusMessage: 'Hanya Super Admin yang bisa mengelola persetujuan akun' })
  const users = await prisma.user.findMany({
    where: { emailVerified: true, approved: false },
    orderBy: { createdAt: 'asc' },
    select: { id: true, nama: true, email: true, jabatan: true, createdAt: true },
  })
  return users
})
