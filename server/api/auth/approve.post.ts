import { z } from 'zod'

const schema = z.object({
  id: z.coerce.number().int().positive(),
  approved: z.boolean(),
})

export default defineEventHandler(async (event) => {
  const me = await prisma.user.findUnique({ where: { id: requireUserId(event) } })
  if (me?.role !== 'SUPER_ADMIN') throw createError({ statusCode: 403, statusMessage: 'Hanya Super Admin yang bisa menyetujui akun' })
  const { id, approved } = await body(event, schema)
  const target = await prisma.user.findUnique({ where: { id } })
  if (!target) throw createError({ statusCode: 404, statusMessage: 'Akun tidak ditemukan' })
  if (target.role === 'SUPER_ADMIN') throw createError({ statusCode: 400, statusMessage: 'Tidak bisa mengubah Super Admin' })
  if (!target.emailVerified) throw createError({ statusCode: 400, statusMessage: 'Email akun ini belum diverifikasi' })

  await prisma.user.update({ where: { id }, data: { approved } })
  return { ok: true }
})
