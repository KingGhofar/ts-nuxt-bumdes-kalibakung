import { z } from 'zod'

const opt = z.string().trim().max(200).nullish()
const schema = z.object({
  nama: z.string().trim().min(1, 'Nama wajib diisi').max(200),
  email: z.email('Email tidak valid'),
  jabatan: opt, telepon: opt, unitKerja: opt, avatar: opt,
})

export default defineEventHandler(async (event) => {
  const data = await body(event, schema)
  const id = requireUserId(event)
  const exists = await prisma.user.findFirst({ where: { email: data.email.toLowerCase(), NOT: { id } } })
  if (exists) throw createError({ statusCode: 409, statusMessage: 'Email sudah dipakai akun lain' })
  return prisma.user.update({
    where: { id }, data: { ...data, email: data.email.toLowerCase() },
    select: { id: true, nama: true, email: true, jabatan: true, telepon: true, nik: true, unitKerja: true, avatar: true, role: true },
  })
})
