import bcrypt from 'bcryptjs'
import { randomBytes, createHash } from 'node:crypto'
import { z } from 'zod'

// Wajib Gmail (termasuk sub-domain Google).
const GMAIL = /^[a-z0-9._%+-]+@(?:gmail\.com|googlemail\.com)$/i

const schema = z.object({
  nama: z.string().trim().min(2, 'Nama minimal 2 karakter').max(100),
  email: z.email('Email tidak valid').refine(e => GMAIL.test(e), 'Gunakan alamat Gmail (gmail.com)'),
  password: z.string().min(8, 'Password minimal 8 karakter').max(100),
})

export default defineEventHandler(async (event) => {
  const { nama, email, password } = await body(event, schema)
  const normalized = email.toLowerCase()
  const exists = await prisma.user.findUnique({ where: { email: normalized } })
  if (exists) throw createError({ statusCode: 409, statusMessage: 'Email sudah terdaftar' })

  const token = randomBytes(32).toString('hex')
  const user = await prisma.user.create({
    data: {
      nama,
      email: normalized,
      password: await bcrypt.hash(password, 10),
      role: 'ADMIN',
      emailVerified: false,
      approved: false,
      verifyTokenHash: createHash('sha256').update(token).digest('hex'),
      verifyTokenExpires: new Date(Date.now() + 24 * 3600 * 1000), // 24 jam
    },
  })

  await sendVerifyEmail(user.email, user.nama, token)
  return { ok: true, message: 'Pendaftaran berhasil. Klik link verifikasi di email Anda.' }
})
