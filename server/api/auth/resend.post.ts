import { randomBytes, createHash } from 'node:crypto'
import { z } from 'zod'

const schema = z.object({ email: z.email('Email tidak valid') })
const COOLDOWN = 15 * 60 * 1000 // 15 menit antar kirim ulang

export default defineEventHandler(async (event) => {
  const { email } = await body(event, schema)
  const user = await prisma.user.findUnique({ where: { email: email.toLowerCase() } })

  // Jangan bocorkan apakah email terdaftar / sudah terverifikasi.
  if (!user) return { ok: true, message: 'Jika email terdaftar, link verifikasi sudah dikirim ulang.' }

  if (user.emailVerified) {
    if (!user.approved) return { ok: true, message: 'Email sudah terverifikasi dan sedang menunggu persetujuan admin.' }
    return { ok: true, message: 'Email sudah terverifikasi. Silakan login.' }
  }

  // Cooldown sederhana tanpa migrasi: token baru dibuat dengan masa 24 jam.
  // Bila token masih "segar" (< 15 menit), tahan dulu untuk cegah spam.
  if (user.verifyTokenExpires && user.verifyTokenExpires.getTime() > Date.now() + 24 * 3600 * 1000 - COOLDOWN)
    throw createError({ statusCode: 429, statusMessage: 'Kami baru saja mengirim email. Tunggu 15 menit sebelum meminta lagi, lalu cek folder Spam.' })

  const token = randomBytes(32).toString('hex')
  await prisma.user.update({
    where: { id: user.id },
    data: {
      verifyTokenHash: createHash('sha256').update(token).digest('hex'),
      verifyTokenExpires: new Date(Date.now() + 24 * 3600 * 1000), // 24 jam
    },
  })

  await sendVerifyEmail(user.email, user.nama, token)
  return { ok: true, message: 'Link verifikasi baru telah dikirim. Cek inbox dan folder Spam.' }
})
