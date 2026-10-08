export default defineEventHandler(event => prisma.user.findUnique({
  where: { id: requireUserId(event) },
  select: { id: true, nama: true, email: true, jabatan: true, telepon: true, nik: true, unitKerja: true, avatar: true, role: true },
}))
