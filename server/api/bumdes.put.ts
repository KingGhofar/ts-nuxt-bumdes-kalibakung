import { z } from 'zod'

const opt = z.string().trim().max(2000).nullish()
const schema = z.object({
  nama: z.string().trim().min(1, 'Nama BUMDes wajib diisi').max(200),
  tahunBerdiri: z.coerce.number().int().min(1900).max(2100).nullish(),
  dasarHukum: opt, email: z.email('Email tidak valid').nullish().or(z.literal('')),
  telepon: opt, alamat: opt, deskripsi: opt, visi: opt, misi: opt, logo: opt,
})

export default defineEventHandler(async (event) => {
  const data = await body(event, schema)
  const cur = await prisma.bumdes.findFirst()
  return cur
    ? prisma.bumdes.update({ where: { id: cur.id }, data })
    : prisma.bumdes.create({ data })
})
