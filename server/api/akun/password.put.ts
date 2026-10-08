import bcrypt from 'bcryptjs'
import { z } from 'zod'

const schema = z.object({
  lama: z.string().min(1, 'Password lama wajib diisi'),
  baru: z.string().min(8, 'Password baru minimal 8 karakter').max(100),
})

export default defineEventHandler(async (event) => {
  const { lama, baru } = await body(event, schema)
  const id = requireUserId(event)
  const user = await prisma.user.findUniqueOrThrow({ where: { id } })
  if (!(await bcrypt.compare(lama, user.password))) throw createError({ statusCode: 400, statusMessage: 'Password lama salah' })
  await prisma.user.update({ where: { id }, data: { password: await bcrypt.hash(baru, 10) } })
  return { ok: true }
})
