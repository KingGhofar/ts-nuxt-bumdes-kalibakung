import bcrypt from 'bcryptjs'
import { z } from 'zod'

const schema = z.object({ email: z.email('Email tidak valid'), password: z.string().min(1, 'Password wajib diisi') })

export default defineEventHandler(async (event) => {
  const { email, password } = await body(event, schema)
  const user = await prisma.user.findUnique({ where: { email: email.toLowerCase() } })
  // Pesan sama untuk email/password salah: jangan bocorkan email terdaftar.
  if (!user || !(await bcrypt.compare(password, user.password)))
    throw createError({ statusCode: 401, statusMessage: 'Email atau password salah' })
  const token = await signToken(user)
  setAuthCookie(event, token)
  return { token, user: { id: user.id, nama: user.nama, email: user.email, jabatan: user.jabatan, avatar: user.avatar, role: user.role } }
})
