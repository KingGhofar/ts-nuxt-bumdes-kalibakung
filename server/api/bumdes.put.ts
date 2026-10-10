import { z } from 'zod'

const opt = z.string().trim().max(2000).nullish()
const schema = z.object({
  nama: z.string().trim().min(1, 'Nama BUMDes wajib diisi').max(200),
  tahunBerdiri: z.coerce.number().int().min(1900).max(2100).nullish(),
  dasarHukum: opt, email: z.email('Email tidak valid').nullish().or(z.literal('')),
  telepon: opt, alamat: opt, deskripsi: opt, visi: opt, misi: opt, logo: opt, jamOperasional: opt,
  pengurus: z.array(z.object({
    nama: z.string().trim().min(1, 'Nama pengurus wajib diisi').max(100),
    jabatan: z.string().trim().min(1, 'Jabatan pengurus wajib diisi').max(100),
    keterangan: z.string().trim().max(200).nullish(),
    foto: z.string().max(200).nullish(),
  })).max(20).optional(),
})

export default defineEventHandler(async (event) => {
  const { pengurus, ...data } = await body(event, schema)
  const cur = await prisma.bumdes.findFirst()
  return prisma.$transaction(async (tx) => {
    const b = cur ? await tx.bumdes.update({ where: { id: cur.id }, data }) : await tx.bumdes.create({ data })
    if (pengurus) {
      // Daftar pengurus kecil: ganti seluruhnya lebih sederhana dari diff per baris.
      await tx.pengurus.deleteMany({ where: { bumdesId: b.id } })
      await tx.pengurus.createMany({ data: pengurus.map((p, urutan) => ({ ...p, urutan, bumdesId: b.id })) })
    }
    return b
  })
})
