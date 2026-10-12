import { createHash } from 'node:crypto'
import { z } from 'zod'

const schema = z.object({ token: z.string().min(20) })

export default defineEventHandler(async (event) => {
  const { token } = await body(event, schema)
  const hash = createHash('sha256').update(token).digest('hex')
  const user = await prisma.user.findFirst({ where: { verifyTokenHash: hash } })

  if (!user || !user.verifyTokenExpires || user.verifyTokenExpires < new Date())
    throw createError({ statusCode: 400, statusMessage: 'Link verifikasi tidak valid atau sudah kedaluwarsa.' })

  await prisma.user.update({
    where: { id: user.id },
    data: { emailVerified: true, verifyTokenHash: null, verifyTokenExpires: null },
  })
  return { ok: true, email: user.email, message: 'Email terverifikasi. Menunggu persetujuan admin.' }
})
